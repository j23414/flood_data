import sqlite3
import requests
import bs4
import pandas as pd


def get_server_data(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    return soup


def parse_data(soup, map, data_tag, val_tag, in_tag, station_id, gw=False):
    """
    parses xml data into a pandas dataframe according to a map dict
    :param soup: the xml data as a BeautifulSoup object
    :param map: a dictionary mapping desired pandas df column names to tags in xml
    :param data_tag: the tag under which a single data point is contained
    :param in_tag: bool - whether the info is in the tag itself (as an attribute) or outside the tag
    :param val_tag: the tag that the data value is under (
            so that it can be made a numeric not a str)
    :return: pandas dataframe with parsed data
    """
    datapoints = soup.find_all(data_tag)
    df = pd.DataFrame(columns=['station_id']+map.keys())
    for d in datapoints:
        data_dict = dict()
        for key, val in map.iteritems():
            if in_tag:
                v = d[val]
            else:
                try:
                    v = getattr(d, val).string
                except TypeError:
                    print("unknown file structure")
            v = float(v) if val == val_tag else v
            data_dict[key] = v
        df = df.append(data_dict,
                       ignore_index=True)
    df.station_id = station_id
    return df


def entry_exists(typ, con, code, **kwargs):
    cur = con.cursor()
    sql = """Select 1 FROM {}s WHERE {}Code = "{}" """.format(typ.lower(), typ, code)
    if typ == 'Variable':
        sql = """Select 1 FROM variables WHERE VariableCode  = "{}"
                                    AND VariableType = "{}" """\
            .format(code, kwargs['variable_type'])

    res = cur.execute(sql)

    return len(res.fetchall())


def get_id(typ, con, soup, code, **kwargs):
    if entry_exists(typ, con, code, **kwargs):
        sql = """SELECT {0}ID FROM {1}s WHERE {0}Code = "{2}" """.format(typ, typ.lower(), code)
        if typ == "Variable":
            sql = """SELECT {0}ID FROM {1}s WHERE {0}Code = "{2}" AND
                        {0}Type = "{3}" """.format(typ, typ.lower(), code, kwargs['variable_type'])
        cur = con.cursor()
        res = cur.execute(sql)
        id = res.next()[0]
        return id
    else:
        get_data_fxn = globals()["get_{}_data".format(typ.lower())]
        data = get_data_fxn(soup)
        create_fxn = globals()["create_{}".format(typ.lower())]
        create_fxn(con, data)
        return get_id(typ, con, soup, code, **kwargs)


def create_data_value(con, datavalue):
    sql = """INSERT INTO datavalues(Value, Datetime, VariableID, SiteID)
            Values(?,?,?,?)"""
    create(con, sql, datavalue)


def create_site(con, site):
    sql = """INSERT INTO sites(SiteCode, SiteName, Lat, Lon)
            Values(?,?,?,?)"""
    create(con, sql, site)


def create_variable(con, variable):
    sql = """INSERT INTO variables(VariableCode, VariableName, VariableType, Units)
            Values(?,?,?,?)"""
    create(con, sql, variable)


def create(con, sql, data):
    cur = con.cursor()
    cur.execute(sql, data)
    con.commit()


def parse_wml2_data(wml2url):
    """
    :param soup: bs4 soup object of wml2 time series
    :return:
    """
    soup = get_server_data(wml2url)
    res_list = []
    con = sqlite3.connect('floodData.sqlite')
    site_code = get_site_data(soup)[0]
    site_id = get_id('Site', con, soup, site_code)

    variable_block = soup.find_all('wml2:observationmember')
    for v in variable_block:
        value_tags_list = v.find_all('wml2:point')
        variable_data = get_variable_data(v)
        variable_code = variable_data[0]
        variable_type = variable_data[2]
        variable_id = get_id('Variable', con, v, variable_code, variable_type=variable_type)
        for value_tag in value_tags_list:
            datetime = value_tag.find('wml2:time').text
            val = value_tag.find('wml2:value').text
            res = {'VariableID': variable_id,
                   'SiteID': site_id,
                   'Value': val,
                   'Datetime': datetime,
                   }
            res_list.append(res)
    df = pd.DataFrame(res_list)
    df = make_date_index(df, 'Datetime')
    df['Value'] = pd.to_numeric(df['Value'])

    # check against current datavalues table in db to avoid storing duplicates
    df = remove_duplicates(con, df)
    df.to_sql('datavalues', con, if_exists='append')
    return df


def get_site_data(soup):
    site_code = soup.find('gml:identifier').text
    site_name = soup.find('om:featureofinterest')['xlink:title']
    lat = soup.find('gml:pos').text.split(' ')[0]
    lon = soup.find('gml:pos').text.split(' ')[1]
    return site_code, site_name, lat, lon


def get_variable_data(soup):
    variable_code = soup.find("om:observedproperty")["xlink:href"].split("=")[1]
    variable_name = soup.find("om:observedproperty")["xlink:title"]
    variable_type = soup.find("om:name")["xlink:title"]
    uom = soup.find("wml2:uom")["xlink:title"]
    return variable_code, variable_name, variable_type, uom


def make_date_index(df, field):
    df.loc[:, field] = pd.DatetimeIndex(df.loc[:, field])
    df.set_index(field, drop=True, inplace=True)
    return df


def save_as_sqlite(df, table_name):
    con = sqlite3.connect('data.sqlite')
    df.to_sql(table_name, con)


def remove_duplicates(con, df):
    db_df = get_db_table_as_df(con, 'datavalues')
    if not db_df.empty:
        df.reset_index(inplace=True)
        db_df.reset_index(inplace=True)
        merged = df.merge(db_df,
                          how='outer',
                          on=['SiteID', 'VariableID', 'Datetime'],
                          indicator=True)
        non_duplicated = merged[merged._merge == 'left_only']
        non_duplicated = make_date_index(non_duplicated, 'Datetime')
        non_duplicated.loc[:, 'Value'] = non_duplicated['Value_x']
        non_duplicated = non_duplicated[['SiteID', 'VariableID', 'Value']]
        return non_duplicated
    else:
        return df


def get_db_table_as_df(con, name):
    sql = """SELECT * FROM {};""".format(name)
    if name == 'datavalues':
        date_col = 'Datetime'
    else:
        date_col = None
    df = pd.read_sql(sql, con, parse_dates=date_col)
    if name == 'datavalues':
        df = make_date_index(df, 'Datetime')
    return df
