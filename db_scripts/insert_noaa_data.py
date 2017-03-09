# coding: utf-8
import pandas as pd
from get_server_data import data_dir, get_db_table_as_df, append_non_duplicates
import numpy as np

df = pd.read_csv("{}noaa_data/raw/911363.csv".format(data_dir))
sites = get_db_table_as_df('sites')
variables = get_db_table_as_df('variables')
s = sites[['SiteID', 'SiteCode']]
s.set_index('SiteCode', inplace=True, drop=True)
df['SiteID'] = s.lookup(df['STATION'], np.repeat("SiteID", len(df['STATION'])))

col_names = ['PRCP', "AWND", "WSF2", "WDF2"]
for c in col_names:
    df_var = df[[c, 'DATE', 'SiteID']]
    variable_id = variables[variables.VariableCode == c]['VariableID'].values[0]
    df_var['VariableID'] = variable_id
    df_var['Datetime'] = pd.to_datetime(df['DATE'], format=("%Y%m%d"))
    df_var['Value'] = df_var[c]
    df_var['QCID'] = 0
    del df_var[c]
    del df_var['DATE']
    df_var = df_var[['Value', 'Datetime', 'VariableID', 'SiteID', 'QCID']]
    print df_var.head()
    append_non_duplicates('datavalues', df_var, ['SiteID', 'Datetime', 'VariableID'])

