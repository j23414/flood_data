
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

event_df.tail()


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

# event_df = event_df[event_df['max_days_away']<10]
print event_df.shape
event_df


# ## Now we'll get the rainfall, groundwater, tide, and wind for the events
# First we need to get all of the data for the variables, aggregate it in various ways up to a daily time step and combine it into a dataframe

# In[21]:

feature_df = pd.DataFrame()


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


# In[34]:

event_df.to_csv('{}event_data.csv'.format(data_dir))


# In[35]:

event_df.iloc[[21,22],3:]


# ### Combining with the non-flooding event data
# First we have to combine all the dates in the "dates" column of the event_df into one array so we can filter those out of the overall dataset.

# In[36]:

flooded_dates = [np.datetime64(i) for i in event_df.index]
flooded_dates = np.array(flooded_dates)
fl_event_dates = np.concatenate(event_df['dates'].tolist())
all_fl_dates = np.concatenate([fl_event_dates, flooded_dates])


# In[37]:

non_flooded_records = feature_df[feature_df.index.isin(all_fl_dates) != True]
non_flooded_records['num_flooded'] = 0
non_flooded_records['flooded'] = False
non_flooded_records['event_name'] = np.nan
non_flooded_records['event_date'] = non_flooded_records.index
non_flooded_records.reset_index(drop=True, inplace=True)
non_flooded_records.head()


# Combine with flooded events

# In[38]:

event_df.reset_index(inplace=True)
flooded_records = event_df
flooded_records['event_date'] = event_df['index']
flooded_records['flooded'] = True
flooded_records.head()


# In[39]:

reformat = pd.concat([flooded_records, non_flooded_records], join='inner')
reformat.reset_index(inplace=True, drop=True)
reformat.head()


# In[40]:

reformat['rain_hourly_max_time'] = reformat['rain_hourly_max_time'].astype('str')  # sqlite does not support native date format
reformat['rain_15_min_max_time'] = reformat['rain_15_min_max_time'].astype('str')
reformat.to_sql(name="for_model", con=con, index=False, if_exists='replace')


# In[ ]:



