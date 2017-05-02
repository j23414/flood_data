# coding: utf-8
from db_scripts.get_server_data import data_dir, db_filename
import pandas as pd
import sqlite3
from db_scripts.data_utils import hampel_filter
from db_scripts.data_utils import hampel_filter
from db_scripts.data_utils import hampel_filter
data_dir
get_ipython().magic(u'ls (data_dir)')
get_ipython().magic(u'ls ')
get_ipython().magic(u'ls data_dir')
import os
os.listdir(data_dir)
df = pd.read_csv('{}hrsd_data/raw/MMPS-125.csv')
df = pd.read_csv('{}hrsd_data/raw/MMPS-125.csv'.format(data_dir))
df.head()
df.set_index('Datetime')
df.set_index('Datetime', inplace=True)
df['Value'].plot()
df.head()
import matplotlib.pyplot as plt
plt.show()
df.tail()
df['VariableID'] = 6
df['SiteID'] = 12
df.head()
df.sort_index(inplace=True)
df.plot()
plt.show()
df['Value'].plot()
plt.show()
df_filt = hampel_filter(df, 'Value', 60)
df_filt.head()
df_filt['Value'].plot()
plt.show()
df_filt = hampel_filter(df, 'Value', 120)
df_filt['Value'].plot()
plt.show()
df['Value'].resample('H').std().plot.box()
df.head()
df.index = pd.to_datetime(df.index)
df['Value'].resample('H').std().plot.box()
plt.show()
df['Value'].resample('H').std().describe()
df['Value'].resample('2H').std().describe()
df['Value'].resample('3H').std().describe()
df['Value'].resample('D').std().describe()
df['Value'].resample('7D').std().describe()
df['Value'].resample('30D').std().describe()
df['Value'].resample('0.1D').std().describe()
df['Value'].resample('2T').std().describe()
df['Value'].resample('4T').std().describe()
df['Value'].resample('30T').std().describe()
df['Value'].resample('60T').std().describe()
df['Value'].resample('30T').std().describe()
type(df['Value'].resample('30T').std().describe())
a = df['Value'].resample('30T').std().describe()
a.T
a = df['Value'].resample('60T').std().describe()
b = df['Value'].resample('30T').std().describe()
a
b
a.name = 60
a
b.name = 30
pd.concat([a, b])
pd.concat([a, b], axis = 1)
pd.concat([a, b], axis = 1).T
r = range(start=30, stop=30*12*30, step=30)
import numpy as np
r = np.arange(start=30, stop=30*12*30, step=30)
r
for t in r:
    a = df['Value'].resample('{}T'.format(t)).std().describe()
    l.append(a)
    
l = []
for t in r:
    a = df['Value'].resample('{}T'.format(t)).std().describe()
    l.append(a)
    
l[:5]
for t in r:
    a = df['Value'].resample('{}T'.format(t)).std().describe()
    a.name = t
    l.append(a)
    
df_stds = pd.concat(l, axis=1)
df_stds.head()
df_std = df_std.T
df_stds = df_stds.T
df_stds
df_stds.ix['Value',:]
359*2
df_stds.ix[!'Value',:]
df_stds.index != 'Value'
df_stds = df_stds[df_stds.index != 'Value']
df_stds
df.stds['mean'].plot()
df_stds['mean'].plot()
plt.show()
df_stds.plot()
plt.show()
df_stds.head()
df_stds.ix[1:, :].plot()
df_stds.iloc[1:, :].plot()
plt.show()
df_stds.iloc[2:, :].plot()
plt.show()
df_stds.iloc[2:, :].head()
df_stds.iloc[:,2:].head()
df_stds.iloc[:,1:].head()
df_stds.iloc[:,1:].plot()
plt.show()
df_stds.iloc[:,1:-1].plot()
plt.show()
df_stds.iloc[:,1:].plot()
plt.show()
df_stds.iloc[:,1:-1].plot()
plt.show()
df_stds.iloc[:,1:].plot()
plt.show()
df_stds.iloc[:,1:-1].plot()
plt.show()
df_stds.iloc[:30,1:-1].plot()
plt.show()
df_filt = hampel_filter(df, 'Value', 600)
df_filt['Value'].plot()
plt.show()
df_filt = hampel_filter(df, 'Value', 800)
df_filt['Value'].plot()
plt.show()
df_filt = df[df['Value']>-5]
df_filt1 = hampel_filter(df, 'Value', 600)
df_filt1.plot()
df_filt1['Value'].plot()
