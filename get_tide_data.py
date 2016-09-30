import bs4
import pandas as pd
import requests
import matplotlib.pyplot as plt
import sqlite3
from get_server_data import *


def save_as_sqlite(df, table_name):
    con = sqlite3.connect('tides.sqlite')
    df.to_sql(table_name, con)


def get_tide_data_from_server(yr, station_num):
    print("fetching data for station:{}      for year: {}".format(station_num, yr))
    url = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date={0}0101&" \
          "end_date={0}1231&station={1}&product=high_low&datum=NAVD&units=metric&" \
          "time_zone=lst&application=web_services&format=xml".format(yr, station_num)
    return get_server_data(url)


def get_tide_df(yrs, station_num):
    data_tag = "hl"
    value_tag = 'v'
    map = {'date': 't', 'type': 'ty', 'value': value_tag}

    df = pd.DataFrame()
    for y in yrs:
        soup = get_tide_data_from_server(y, station_num)
        df = df.append(parse_data(soup, map, data_tag, value_tag, True, station_num))
    df = make_date_index(df, 'date')
    return df


start_year = 2015
end_year = 2016
years = range(start_year, end_year)
station = '8638610'
df = get_tide_df(years, station)
df.groupby(df.index.month).mean().plot.bar()
plt.show()
type_summary = df.groupby(df.type).mean()
ave_tidal_range = type_summary.loc['HH'] - type_summary.loc['LL']
print("Average tidal range is {} meters".format(str(ave_tidal_range[0])))
save_as_sqlite(df, 'tide_levels')
