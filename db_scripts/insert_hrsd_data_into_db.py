import pandas as pd
import os
from get_server_data import get_id, append_non_duplicates, make_date_index


data_dir = '../hrsd_data'


def get_file_list(site_nums):
    global data_dir
    data_files = []
    for site_num in site_nums:
        for dirpath, dirnames, filenames in os.walk(data_dir):
            for filename in filenames:
                if filename.startswith('MMPS-{}'.format(site_num)) and filename.endswith('.csv'):
                    data_files.append(filename)
    return data_files

data_files = get_file_list(['170'])
site_info_table = pd.read_csv("{}/site_info.csv".format(data_dir))
variable_info_table = pd.read_csv("{}/variable_info.csv".format(data_dir))
for data_file in data_files:
    df = pd.read_csv("{}/{}".format(data_dir, data_file))

    site_code = data_file.split('_')[0]
    site_info = site_info_table[site_info_table.SiteCode == site_code].to_dict('records')[0]
    site_id = get_id('Site', site_info)

    if df.columns[1].startswith('Rain'):
        variable_code = 'Rainfall'
    elif df.columns[1].startswith('Shallow Well') or df.columns[1].startswith('Level_NAVD88_ft'):
        variable_code = 'Shallow_well_depth'
    else:
        raise ValueError('I do not now what variable you are trying to insert')
    
    variable_info = variable_info_table[
        variable_info_table.VariableCode == variable_code].to_dict('records')[0]
    variable_id = get_id('Variable', variable_info)
    df.columns = ['Datetime', 'Value']
    df['VariableID'] = variable_id
    df['SiteID'] = site_id
    df = make_date_index(df, 'Datetime')
    append_non_duplicates('datavalues', df, ['SiteID', 'Datetime', 'VariableID'])