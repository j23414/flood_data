
# coding: utf-8

# ## Intro
# This notebook aggregates the environmental data by event whereas before we were looking at the data by date. 

# ### Calculate number of locations that flooded

# In[1]:

get_ipython().magic(u'matplotlib inline')
from focus_intersection import subset_floods, flood_df, subset_locations
from get_server_data import get_table_for_variable, get_db_table_as_df, data_dir, db_filename
import pandas as pd
import numpy as np
import sqlite3
con = sqlite3.connect(db_filename)
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:

flood_locations = get_db_table_as_df('flood_locations')
len(flood_locations['location'].unique())


# In this case we are just focusing on the subset of points that is in the downtown area thus the "subset_floods."

# In[3]:

subset_locations = flood_locations['location']
flood_events = get_db_table_as_df('flood_events')
flood_events['event_date'] = pd.to_datetime(flood_events['event_date'])
flood_events['event_name'] = flood_events['event_name'].str.strip()
flood_events['dates'] = pd.to_datetime(flood_events['dates'])
subset_floods = flood_events[flood_events['location'].isin(subset_locations)]


# In[4]:

grouped = subset_floods.groupby(['event_date', 'event_name'])


# Get the number of dates the event spanned, the number of unique locations that were flooded during the event and the total number of locations flooded on all event dates. 

# In[5]:

event_total_flooded = grouped.size()
event_dates = grouped['dates'].unique()
num_event_dates = grouped['dates'].nunique()
num_locations = grouped['location'].nunique()


# In[6]:

event_df = pd.concat([event_dates, event_total_flooded, num_event_dates, num_locations], axis=1)
event_df.columns = ['dates', 'num_flooded', 'num_dates', 'num_locations']


# In[7]:

event_df.head()


# ### Where num_flooded does not equal num_locations _investigation_
# Let's checkout one of the events where the num_flooded is greater than the num_locations. I would expect this to mean that one location was flooded on multiple days of the same event. But for '2014-07-24' the event is only on one day so that isn't what I expected.

# In[8]:

idx = pd.IndexSlice
event_df.sort_index(inplace=True)
event_df.loc[idx['2014-07-24', :], :]


# In[9]:

fl_724 = subset_floods[subset_floods['dates'] == '2014-07-24']
fl_724[fl_724['location'].duplicated(keep=False)]


# So _here's_ what is happening. The location name is the same in two rows but there are two different event types: "flooded street" and "flooded underpass."
# Now that I think about it, that may explain all the differences between the num_location and num_flooded columns. Let's try another one, this time one that spans more than one day: Irene.

# In[10]:

event_df.sort_index(inplace=True)
event_df.loc[idx[:, 'Irene'], :]


# In[11]:

irene = subset_floods[subset_floods['event_name'].str.contains('Irene')].sort_values('location')
irene[irene['location'].duplicated(keep=False)]


# Looks like that's it. Which is not what I was hoping to show. I was thinking that that tell me something about the variety of locations that were flooded over the days but that's not the case.

# Let's try this one more time with Hurricane Joaquin

# In[12]:

jqn = flood_df[flood_df['event'].str.contains('Joaquin')]


# In[13]:

jqn[jqn['location'].duplicated(keep=False)]


# So that is interesting. Even though for hurricanes Matthew and Joaquin, the seven and six days respectively, none
# of the flooded locations were reported twice for one event. Very interesting. So to me, this means we really should be looking at these things by 'event' and not by '\_date'. It also means that the num_locations col doesn't add any information. So imma delete that.

# In[14]:

del event_df['num_locations']


# ### Looking into date in "event" column versus dates in "\_date" column
# Sometimes the date listed in the "event" column is quite different than the date(s) listed in the "\_date" column. A good example of this is the event "unnamed (2/25/2016)" where the dates in the "\_date" column are 2016-05-05, 2016-05-06, and 2016-05-31"

# In[15]:

flood_df[flood_df['event'].str.contains('2/25/2016')]


# So to look at this more closely, I will calculate the difference in days between the "event" column date and the dates in the "\_date" column.

# When I tried to calculate the time between the 'event_date' and the 'dates' to see how far off these were I found that two events had the same 'event_date'. So I think it's appropriate to drop the 'unnamed' one based on the fact that the dates in the "\_date" column are further from the "event_date".

# In[16]:

event_df.sort_index(inplace=True)
event_df.loc[idx['2016-07-30', :], :]


# In[17]:

i = event_df.loc[['2016-07-30', 'unnamed'],:].index
event_df.drop(i, inplace=True)
i = event_df.loc[idx['2014-09-13', "NAPSG"],:].index
event_df.drop(i, inplace=True)


# In[18]:

event_df.reset_index(inplace=True)
event_df.set_index('event_date', inplace=True)
event_df


# In[19]:

days_away = []
max_days = []
for d in event_df.index:
    try:
        ar = event_df.loc[d, 'dates'] - np.datetime64(d)
        ar = ar.astype('timedelta64[D]')
        days = ar / np.timedelta64(1, 'D')
        days_away.append(days)
        max_days.append(days.max())
    except ValueError:
        print d
event_df['days_away_from_event'] = days_away
event_df['max_days_away'] = max_days
print event_df.shape
event_df.head()


# I don't trust the events that have higher days away so I will disregard any event with a "max_days_away" greater than 10. Five events fall under this category.

# In[20]:

event_df = event_df[event_df['max_days_away']<10]
print event_df.shape
event_df


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

rain_prev_3_days = rain_grouped.resample('D').sum().rolling(window=3).sum()
rain_prev_3_days.reset_index(level=0, drop=True, inplace=True)
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


# ### Combine env. data with event data

# In[31]:

def add_event_data(evnt_data, evnt_df, col_name, func, idx):
    res = func(evnt_data[col_name])
    evnt_df.loc[idx, col_name] = res
    return evnt_df


# Now for each event we get an aggregate of the different variables for the given dates

# In[32]:

event_df = pd.concat([event_df, pd.DataFrame(columns=feature_df.columns)])

for ind in event_df.index:
    # get the dates of the event and include the date in the "event" column
    ds = event_df.loc[ind, 'dates']
    ind = np.datetime64(ind)
    ds = np.append(ds, ind) if not ind in ds else ds
    
    event_data = feature_df.loc[ds]
 
    # combining data on event scale
    # get max over the event for these features
    max_cols = ['rain_hourly_max', 'rain_15_min_max', 'wind_vel_daily_avg', 'wind_vel_hourly_max_avg']
    
    # get mean over the event for these features
    mean_cols = ['gw_daily_avg', 'tide_daily_avg', 'wind_dir_daily_avg']
    
    # get sum over the event for these features
    sum_cols = ['rain_daily_sum']
    
    # do something else for these features
    other_cols = ['rain_prev_3_days', 'rain_hourly_max_time', 'rain_15_min_max_time', 'tide_rhrmx', 'tide_r15mx']
    
    
    for feat in feature_df.columns:
        if feat in max_cols:
            event_df = add_event_data(event_data, event_df, feat, np.max, ind)
        elif feat in mean_cols:
            event_df = add_event_data(event_data, event_df, feat, np.mean, ind)
        elif feat in sum_cols:
            event_df = add_event_data(event_data, event_df, feat, np.sum, ind)
        elif feat in other_cols:
            if feat=='rain_prev_3_days':
                event_df.loc[ind, feat] = event_data.loc[ind, feat]
            elif feat == 'rain_hourly_max_time' or feat == 'tide_rhrmx':
                max_ind = event_data['rain_hourly_max'].idxmax()
                event_df.loc[ind, feat] = event_data.loc[max_ind, feat]
            elif feat == 'rain_15_min_max_time' or feat == 'tide_r15mx':
                max_ind = event_data['rain_15_min_max'].idxmax()
                event_df.loc[ind, feat] = event_data.loc[max_ind, feat]
        else:
            raise ValueError("I don't know how to aggregate this variable on an event scale")
        
event_df.head()


# In[33]:

event_df.to_csv('{}event_data.csv'.format(data_dir))


# ### Combining with the non-flooding event data
# First we have to combine all the dates in the "dates" column of the event_df into one array so we can filter those out of the overall dataset.

# In[34]:

flooded_dates = [np.datetime64(i) for i in event_df.index]
flooded_dates = np.array(flooded_dates)
fl_event_dates = np.concatenate(event_df['dates'].tolist())
all_fl_dates = np.concatenate([fl_event_dates, flooded_dates])


# In[35]:

non_flooded_records = feature_df[feature_df.index.isin(all_fl_dates) != True]
non_flooded_records['num_flooded'] = 0
non_flooded_records['flooded'] = False
non_flooded_records['event_name'] = np.nan
non_flooded_records['event_date'] = non_flooded_records.index
non_flooded_records.reset_index(drop=True, inplace=True)
non_flooded_records.head()


# Combine with flooded events

# In[36]:

event_df.reset_index(inplace=True)
flooded_records = event_df
flooded_records['event_date'] = event_df['index']
flooded_records['flooded'] = True
flooded_records.head()


# In[37]:

reformat = pd.concat([flooded_records, non_flooded_records], join='inner')
reformat.reset_index(inplace=True, drop=True)
reformat.head()


# In[38]:

reformat.to_csv("{}reformat_by_event.csv".format(data_dir), index=False)
reformat['rain_hourly_max_time'] = reformat['rain_hourly_max_time'].astype('str')  # sqlite does not support native date format
reformat['rain_15_min_max_time'] = reformat['rain_15_min_max_time'].astype('str')
reformat.to_sql(name="for_model", con=con, index=False, if_exists='replace')

