from get_server_data import get_server_data, parse_data
site_number = "364715076030801"
url = "http://waterservices.usgs.gov/nwis/dv/?format=waterml,2.0&sites={}&startDT=2005-03-11" .format(site_number)
soup=get_server_data(url)
gw_data=parse_data(soup,{"date":"wml2:time","value":"wml2:value"},data_tag='wml2:point',val_tag="wml2:value",in_tag=False)