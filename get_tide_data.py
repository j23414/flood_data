import bs4
import pandas as pd
import requests
import matplotlib.pyplot as plt
import sqlite3


def save_as_sqlite(df, table_name):
    con = sqlite3.connect('tides.sqlite')
    df.to_sql(table_name, con)


def get_tide_data_from_server(yr, station_num):
    print "fetching data for station:{}      for year: {}".format(station_num, yr)
    url = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date={0}0101&" \
          "end_date={0}1231&station={1}&product=high_low&datum=NAVD&units=metric&" \
          "time_zone=lst&application=web_services&format=xml".format(yr, station_num)

    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')
    return soup


def parse_data(soup, map, data_tag, val_tag, in_tag):
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
    station_id = soup.metadata['id']
    for d in datapoints:
        data_dict = dict()
        for key, val in map.iteritems():
            if in_tag:
                v = d[val]
            else:
                try:
                    v = getattr(d, val).string
                except TypeError:
                    print "unknown file structure"
            v = float(v) if val == val_tag else v
            data_dict[key] = v
        df = df.append(data_dict,
                       ignore_index=True)
    df.station_id = station_id
    return df


def get_tide_df(yrs, station_num):
    data_tag = "hl"
    value_tag = 'v'
    map = {'date': 't', 'type': 'ty', 'value': value_tag}

    df = pd.DataFrame()
    for y in yrs:
        soup = get_tide_data_from_server(y, station_num)
        df = df.append(parse_data(soup, map, data_tag, value_tag, True))
    df = make_date_index(df, 'date')
    return df


def make_date_index(df, field):
    df[field] = pd.DatetimeIndex(df[field])
    df.set_index(field, drop=True, inplace=True)
    return df

start_year = 1980
end_year = 2016
years = range(start_year, end_year)
station = '8638610'
df = get_tide_df(years, station)
df.groupby(df.index.month).mean().plot.bar()
plt.show()
type_summary = df.groupby(df.type).mean()
ave_tidal_range = type_summary.loc['HH'] - type_summary.loc['LL']
print "Average tidal range is {} meters".format(str(ave_tidal_range[0]))
save_as_sqlite(df, 'tide_levels')
