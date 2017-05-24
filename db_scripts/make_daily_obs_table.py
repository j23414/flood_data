import pandas as pd
from get_server_data import raw_db_filename, get_table_for_variable
# ## Now we'll get the rainfall, groundwater, tide, and wind for the events
# First we need to get all of the data for the variables, aggregate it in various ways up to a daily time step and combine it into a dataframe

# In[21]:

feature_df = pd.DataFrame()


# #### Rainfall

# In[22]:

rain_df = get_table_for_variable('rainfall').sort_index()

# aggregate the rainfall in various ways
rain_grouped = rain_df.groupby('SiteID')

rain_daily = rain_grouped.resample('D').agg({'Value':np.sum, 'SiteID':np.mean, 'VariableID':np.mean})
rain_daily.reset_index(level=0, drop=True, inplace=True)
feature_df['rain_daily_sum'] = rain_daily.resample('D').mean()['Value']

rain_hourly_totals = rain_grouped.rolling(window=4).sum()
rain_hourly_totals.reset_index(level=0, drop=True, inplace=True)
rhr_mx = rain_hourly_totals.resample('D').max()
feature_df['rain_hourly_max'] = rhr_mx['Value']
feature_df['rain_hourly_max_time'] = rain_hourly_totals.groupby(pd.Grouper(freq='D')).idxmax()['Value']

r15_mx = rain_df.resample('D').max()
feature_df['rain_15_min_max'] = r15_mx['Value']
feature_df['rain_15_min_max_time'] = rain_df.groupby(pd.Grouper(freq='D')).idxmax()['Value']

rain_prev_3_days = rain_daily.shift(1).rolling(window=3).sum()
feature_df['rain_prev_3_days'] = rain_prev_3_days.resample('D').mean()['Value']


# #### Groundwater

# In[23]:

gw_df = get_table_for_variable('groundwater').sort_index()
feature_df['gw_daily_avg'] = gw_df.resample('D').mean()['Value']


# #### Tide

# In[24]:

tide_df = get_table_for_variable('tide').sort_index()
feature_df['tide_daily_avg'] = tide_df.resample('D').mean()['Value']


# #### Tide when rain is at max

# In[25]:

def round_down_near_24(datetimes): # round down the times near midnight so the tide levels stay on the correct day
    close_time_idx = datetimes.indexer_between_time('23:29', '23:59')
    adjusted_times = datetimes[close_time_idx] - pd.Timedelta(minutes=30)
    dt = pd.Series(datetimes)
    dt[close_time_idx] = adjusted_times
    dt = pd.DatetimeIndex(dt)
    return dt


# In[26]:

def cln_n_rnd_times(datetimes):
    times = pd.DatetimeIndex(datetimes)
    rnd_dn = round_down_near_24(times)
    rnd_hr = rnd_dn.round(freq='H')
    return rnd_hr


# In[27]:

feature_df['rain_15_min_max_time'] = np.where(feature_df['rain_daily_sum']>0, feature_df['rain_15_min_max_time'], np.datetime64('NaT'))
feature_df['rain_hourly_max_time'] = np.where(feature_df['rain_daily_sum']>0, feature_df['rain_hourly_max_time'], np.datetime64('NaT'))
r15mx_times = cln_n_rnd_times(feature_df['rain_15_min_max_time'])
# there is only one value per day anyway but we resample so it just has the day, no time information
feature_df['tide_r15mx'] = tide_df.loc[r15mx_times]['Value'].resample('D').max()
rhrmx_times = cln_n_rnd_times(feature_df['rain_hourly_max_time'])
feature_df['tide_rhrmx'] = tide_df.loc[rhrmx_times]['Value'].resample('D').max()


# #### Wind

# In[28]:

wind_dir_df = get_table_for_variable('wind_dir').sort_index()
wind_vel_df = get_table_for_variable('wind_vel').sort_index()
wind_daily = get_table_for_variable(9).sort_index()
wind_daily_dir = get_table_for_variable(13).sort_index()
# wind_dir_noaa = get_table_for_variable

two_min_daily_avg_wdir = wind_dir_df.resample('D').mean()['Value']
daily_wdir_avg = wind_daily_dir.resample('D').mean()['Value']
feature_df['wind_dir_daily_avg'] = pd.concat([two_min_daily_avg_wdir, daily_wdir_avg],  axis=1).mean(axis=1)

daily_wind_avg = wind_daily.resample('D').mean()['Value']
two_min_daily_avg = wind_vel_df.resample('D').mean()['Value']
feature_df['wind_vel_daily_avg'] = pd.concat([daily_wind_avg, two_min_daily_avg],  axis=1).mean(axis=1)

feature_df['wind_vel_hourly_max_avg'] = wind_vel_df.resample('H').max().resample('D').mean()['Value']


# In[29]:

feature_df = feature_df["2010-01-01": "2016-10-31"]
feature_df.head()


# ### Save Daily Observations to DB

# In[30]:

feature_df.to_sql(con=con, name="dntwn_nor_daily_observations", if_exists="replace")