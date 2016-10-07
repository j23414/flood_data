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

def create_site(con, site):
    sql = """INSERT INTO sites(SiteName, SiteCode, Lat, Lon)
            Values(?,?,?,?)"""
    cur = con.cursor()
    cur.execute(sql, site)
    cur.commit()

def parse_wml2_data(soup):
    """
    :param soup: bs4 soup object of wml2 time series
    :return:
    """
    variable_block = soup.find_all('wml2:observationmember')
    res_list =[]
    site_data = get_site_data(soup)
    for v in variable_block:
        variable_name = v.find("om:observedproperty")["xlink:title"]
        variable_type = v.find("om:name")["xlink:title"]
        uom = v.find("wml2:uom")["xlink:title"]
        value_tags_list = v.find_all('wml2:point')
        for value_tag in value_tags_list:
            datetime = value_tag.find('wml2:time').text
            val = value_tag.find('wml2:value').text
            res = {'variable_name': variable_name,
                   'variable_type': variable_type,
                   'units': uom,
                   'datetime': datetime,
                   'value': val,
                   }
            res_list.append(res)
    df = pd.DataFrame(res_list)
    df = make_date_index(df, 'datetime')
    df['value'] = pd.to_numeric(df['value'])
    return df


def get_site_data(soup):
    site_code = soup.find('gml:identifier').text
    site_name = soup.find('om:featureofinterest')['xlink:title']
    lat = soup.find('gml:pos').text.split(' ')[0]
    lon = soup.find('gml:pos').text.split(' ')[1]
    return (site_code, site_name, lat, lon)


def make_date_index(df, field):
    df[field] = pd.DatetimeIndex(df[field])
    df.set_index(field, drop=True, inplace=True)
    return df


def save_as_sqlite(df, table_name):
    con = sqlite3.connect('data.sqlite')
    df.to_sql(table_name, con)
