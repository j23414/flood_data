from get_server_data import *


def get_tide_data_from_server(yr, station_num):
    print("fetching data for station:{}      for year: {}".format(station_num, yr))
    url = "http://tidesandcurrents.noaa.gov/api/datagetter?begin_date={0}0101&" \
          "end_date={0}1231&station={1}&product=high_low&datum=NAVD&units=metric&" \
          "time_zone=lst&application=web_services&format=xml".format(yr, station_num)
    return get_server_data(url)


def get_tide_site_data(soup, src_org):
    site_code = soup.find('metadata')['id']
    site_name = soup.find('metadata')['name']
    site_lat = soup.find('metadata')['lat']
    site_lon = soup.find('metadata')['lon']
    return {'SiteCode': site_code,
            'SiteName': site_name,
            'SourceOrg': src_org,
            'Lat': site_lat,
            'Lon': site_lon}


def get_tide_df(yrs, station_num):
    data_tag = "hl"
    value_tag = 'v'
    map = {'datetime': 't', 'variable_type': 'ty', 'value': value_tag}

    df = pd.DataFrame()
    for y in yrs:
        soup = get_tide_data_from_server(y, station_num)
        df = df.append(parse_data(soup, map, data_tag, value_tag, True, station_num))
    df = make_date_index(df, 'datetime')
    return df


start_year = 2015
end_year = 2016
years = range(start_year, end_year)
station = '8638610'
# df = get_tide_df(years, station)