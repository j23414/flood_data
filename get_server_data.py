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


def get_id(typ, con, data):
    """
    gets either the siteid or variableid from the db
    :param typ: String. Either "Site" or "Variable"
    :param con: aqlite connection. connection to db
    :param data: Dict. the site or variable data
    :return: int. id of site or variable
    """
    data_df = pd.DataFrame(data, index=[0])
    code_name = '{}Code'.format(typ)
    table_name = '{}s'.format(typ.lower())
    id_name = '{}ID'.format(typ)
    code = data[code_name]
    check_by = [code_name] if typ == 'Site' else [code_name, 'VariableType']
    df = append_non_duplicates(con, table_name, data_df, check_by)
    table = get_db_table_as_df(con, table_name)
    if typ == 'Variable':
        id_row = table[(table[code_name] == code) & (table['VariableType'] == data['VariableType'])]
    else:
        id_row = table[table[code_name] == code]
    id_num = id_row[id_name].values[0]
    return id_num


def parse_wml2_data(wml2url, src_org):
    """
    parses wml2 data into pandas dataframe and adds the data, including the site and variable, into
    the database if not already in there
    :param wml2url: String. the service response in wml2 format
    :param src_org: String. the organization e.g. "USGS"
    :return: dataframe of the time series
    """
    soup = get_server_data(wml2url)
    res_list = []
    con = sqlite3.connect('floodData.sqlite')
    site_data = get_site_data(soup, src_org)
    site_id = get_id('Site', con, site_data)

    variable_block = soup.find_all('wml2:observationmember')
    for v in variable_block:
        value_tags_list = v.find_all('wml2:point')
        variable_data = get_variable_data(v)
        variable_id = get_id('Variable', con, variable_data)
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
    df['Value'] = pd.to_numeric(df['Value'])
    df = make_date_index(df, 'Datetime')
    append_non_duplicates(con, 'datavalues', df, ['SiteID', 'Datetime', 'VariableID'])
    return df


def get_site_data(soup, src_org):
    site_code = soup.find('gml:identifier').text
    site_name = soup.find('om:featureofinterest')['xlink:title']
    site_lat = soup.find('gml:pos').text.split(' ')[0]
    site_lon = soup.find('gml:pos').text.split(' ')[1]
    return {'SiteCode': site_code,
            'SiteName': site_name,
            'SourceOrg': src_org,
            'Lat': site_lat,
            'Lon': site_lon
            }


def get_variable_data(soup):
    variable_code = soup.find("om:observedproperty")["xlink:href"].split("=")[1]
    variable_name = soup.find("om:observedproperty")["xlink:title"]
    variable_type = soup.find("om:name")["xlink:title"]
    uom = soup.find("wml2:uom")["xlink:title"]
    return {'VariableCode': variable_code,
            'VariableName': variable_name,
            'VariableType': variable_type,
            'Units': uom
            }


def make_date_index(df, field):
    df.loc[:, field] = pd.DatetimeIndex(df.loc[:, field])
    df.set_index(field, drop=True, inplace=True)
    return df


def save_as_sqlite(df, table_name):
    con = sqlite3.connect('data.sqlite')
    df.to_sql(table_name, con)


def append_non_duplicates(con, table, df, check_col):
    db_df = get_db_table_as_df(con, table)
    if not db_df.empty:
        if table == 'datavalues':
            df.reset_index(inplace=True)
            db_df.reset_index(inplace=True)
        merged = df.merge(db_df,
                          how='outer',
                          on=check_col,
                          indicator=True)
        non_duplicated = merged[merged._merge == 'left_only']
        filter_cols = [col for col in list(non_duplicated) if "_y" not in col and "_m" not in col]
        non_duplicated = non_duplicated[filter_cols]
        cols_clean = [col.replace('_x', '') for col in list(non_duplicated)]
        non_duplicated.columns = cols_clean
        non_duplicated = non_duplicated[df.columns]
        non_duplicated.to_sql(table, con, if_exists='append', index=False)
        return non_duplicated
    else:
        index = True if table == 'datavalues' else False
        df.to_sql(table, con, if_exists='append', index=index)
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
