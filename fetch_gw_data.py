from get_server_data import parse_wml2_data, get_server_data, get_site_data, remove_duplicates
import pandas as pd
import sqlite3
site_number = "364715076030801"
start_date = "2005-03-11"
url = "http://waterservices.usgs.gov/nwis/dv/?format=waterml,2.0&sites={}&startDT={}" .format(site_number, start_date)
# gw_data = parse_wml2_data(url, "USGS")
soup = get_server_data(url)
site_info = get_site_data(soup, 'USGS')
check_by = ['SiteCode']
d = {'SiteCode': site_info[0],
                   'SiteName':site_info[1],
                   'SourceOrg': site_info[2],
                   'Lat': site_info[3],
                   'Lon': site_info[4]
                   }
df = pd.DataFrame(d, index=[0])
con = sqlite3.connect('floodData.sqlite')
dub = remove_duplicates(con, 'sites', df, check_by)
dub.to_sql('sites', con, if_exists='append', index=False)
