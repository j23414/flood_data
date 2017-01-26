import numpy as np
import pandas as pd
import os
from get_server_data import get_id, append_non_duplicates, make_date_index
from data_utils import hampel_filter, account_for_elev

data_dir = '../hrsd_data'


def qc_shallow_well_data(df):
    column_name = 'Shallow Well_NAVD 88 (ft)'
    df = account_for_elev(df, elev_threshold=7.5, col=column_name)
    df = hampel_filter(df, column_name, 30, threshold=3)
    df['Time Stamp'] = pd.to_datetime(df.loc[:, 'Time Stamp'], format="%m/%d/%Y %H:%M:%S")
    df.set_index('Time Stamp', inplace=True, drop=True)
    df = df.resample('H', how=np.average)
    df.reset_index(inplace=True)
    return df


def get_file_list(site_nums):
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
    df = pd.read_csv("{}/inserted/{}".format(data_dir, data_file))

    site_code = data_file.split('_')[0]
    site_info = site_info_table[site_info_table.SiteCode == site_code].to_dict('records')[0]
    site_id = get_id('Site', site_info)

    if df.columns[1].startswith('Rain'):
        variable_code = 'Rainfall'
    elif df.columns[1].startswith('Shallow Well') or df.columns[1].startswith('Level_NAVD88_ft'):
        variable_code = 'Shallow_well_depth'
        # for shallow well data run hampel filter, cutoff at 7.5 ft and resample at hourly time step
        df = qc_shallow_well_data(df)
    else:
        raise ValueError('I do not now what variable you are trying to insert')
    
    variable_info = variable_info_table[
        variable_info_table.VariableCode == variable_code].to_dict('records')[0]
    variable_id = get_id('Variable', variable_info)
    df.columns = ['Datetime', 'Value']
    df['VariableID'] = variable_id
    df['SiteID'] = site_id
    if variable_id == 6:
        df['QCID'] = 1
    df = make_date_index(df, 'Datetime')
    append_non_duplicates('datavalues', df, ['SiteID', 'Datetime', 'VariableID'])
