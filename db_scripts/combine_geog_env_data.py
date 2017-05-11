
# coding: utf-8

# In[1]:

from get_server_data import get_db_table_as_df, db_filename
import sqlite3
import pandas as pd
import numpy as np


# In[2]:

flood_locations = get_db_table_as_df('flood_locations')
flood_events = get_db_table_as_df('flood_events', date_col=['event_date', 'dates'])
for_model = get_db_table_as_df('for_model', date_col=['event_date'])
daily_obs = get_db_table_as_df('dntwn_nor_daily_observations', date_col=['Datetime'])


# In[3]:

flood_locations.head()


# In[4]:

daily_obs.set_index('Datetime', inplace=True)
daily_obs.head()


# In[5]:

daily_obs.shape


# In[6]:

flood_events.head()


# In[7]:

for_model.set_index('event_date', inplace=True)
for_model.head()


# In[8]:

flood_locations.shape


# In[9]:

lst = []
for index, row in flood_locations.iterrows():
    l = row['location'].strip()
    loc_data = daily_obs.copy()
    loc_data['flooded'] = 0
    if l != '':
        event_dates = flood_events[flood_events['location'] == l]['event_date']
        all_fld_dates = flood_events[flood_events['event_date'].isin(event_dates)]['dates']
        all_fld_dates = np.append(all_fld_dates, event_dates)
        all_fld_dates = pd.to_datetime(np.unique(all_fld_dates))

        fld_data = for_model[for_model.index.isin(event_dates)]
    
        loc_data = loc_data[~loc_data.index.isin(all_fld_dates)]
        loc_data = pd.concat([loc_data, fld_data])
    
        # add geog data
    for k in row.keys():
        loc_data[k] = row[k]
    lst.append(loc_data)
#         print l
#         print loc_data.head()
        


# In[10]:

all_locations = pd.concat(lst)
all_locations.reset_index(inplace=True)


# In[11]:

all_locations.shape


# In[12]:

new_cols = all_locations.columns.tolist()
new_cols[0] = 'Date'
all_locations.columns = new_cols
print all_locations.shape
all_locations.tail()


# In[13]:

con = sqlite3.connect(db_filename)
all_locations.to_sql(con=con, name='for_model_geog', if_exists='replace')

