# coding: utf-8
import pandas as pd
df  = pd.read_csv('MMPS-125_filt.csv')
df['Value'].plot()
import matplotlib.pyplot as plt
plt.show()
from db_scripts.get_server_data import data_dir db_filename
from db_scripts.get_server_data import data_dir,raw_db_filename
from db_scripts.data_utils import hampel_filter
df_raw = pd.read_csv('{}/hrsd_data/raw/MMPS-125.csv'.format(data_dir))
df_raw['Value'].plot()
plot.show()
plt.show()
df_raw.set_index('Datetime', inplace=1)
df.set_index('Datetime', inplace=1)
df_filt = df_raw[df_raw['Value'] < -5]
df_filt.plot()
df_filt.head()
df_filt = df_raw[df_raw['Value'] > -5]
df_raw.index = pd.to_datetime(df_raw.index)
df_filt = df_raw[df_raw['Value'] > -5]
df_filt.plot()
plt.show()
df_filt['Value'].plot()
plt.show()
df_filt1 = hampel_filter(df_filt, 'Value', 600)
df_filt1['Value'].plot()
plt.show()
pd.date_range('2012-12-19', '2012-12-22')
pd.date_range('2012-12-19', '2012-12-22', freq='2T')
r = pd.date_range('2012-12-19', '2012-12-22', freq='2T')
df_filt1.loc[r]
df_filt1.loc[r, 'Value'].plot()
plt.show()
r = pd.date_range('2012-12-19 11:30', '2012-12-22', freq='2T')
df_filt1.loc[r, 'Value'].plot()
plt.show()
r = pd.date_range('2012-12-19 10:30', '2012-12-22', freq='2T')
df_filt1.loc[r, 'Value'].plot()
plt.show()
import numpy as np
df_filt1.loc[r, 'Value'] = np.nan
df_filt1.loc[r, 'Value'].plot()
df_filt1.loc[r, 'Value']
df_filt1.loc[r, 'Value'] = np.nan
r
df_filt1.ix[r, 'Value'] = np.nan
df_filt1.loc[r, 'Value']
df_filt1.set_value(r, 'Value', np.nan)
df_filt1.index.head()
df_filt1.loc[r, 'Value'] = 0
r
df_filt1.loc[r[0], 'Value'] = 0
df_filt1.loc[r, 'Value']
a = df_filt1.loc[r, 'Value']
a['Value'] = np.nan
a
a.set_value(a.index, np.nan)
df_filt1[df_filt1.index.isin(r)]
df_filt1[~df_filt1.index.isin(r)]
df_filt2 = df_filt1[~df_filt1.index.isin(r)]
df_filt2['Value'].plot()
df_filt2.to_csv('MMPS-125_filt1.csv')
