
# coding: utf-8

# In[1]:

from get_server_data import get_db_table_as_df


# In[ ]:

flood_locations = get_db_table_as_df('flood_locations')
flood_events = get_db_table_as_df('flood_events')
for_model = get_db_table_as_df('for_model')
daily_obs = get_db_table_as_df('')

