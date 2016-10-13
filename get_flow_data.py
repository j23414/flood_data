from get_server_data import *
site_number = "0204288771"
parameter_id = '00060'
start_date = '2015-07-17'
url = "http://waterservices.usgs.gov/nwis/iv/?format=waterml,2.0&sites={}&startDT={}&parameterCd={}".format(site_number, start_date, parameter_id)
flow_data = parse_wml2_data(url, "USGS")

