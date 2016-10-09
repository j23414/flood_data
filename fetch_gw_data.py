from get_server_data import get_server_data, parse_wml2_data, create_site, get_site_data
import sqlite3
site_number = "364715076030801"
start_date = "2005-03-11"
url = "http://waterservices.usgs.gov/nwis/dv/?format=waterml,2.0&sites={}&startDT={}" .format(site_number, start_date)
soup = get_server_data(url)
site = get_site_data(soup)
con = sqlite3.connect('floodData.sqlite')
create_site(con, site)
# gw_data = parse_wml2_data(soup)