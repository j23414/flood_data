
# coding: utf-8

# ## Intro

# There are a couple comments from the reviewers that I want to clear up in this notebook:
# 
# 1. How sensitive are the RF results to different parameter values such as number of trees? (from reviewer 1)
# 2. Why not just use rainfall as a proxy for flood severity? Why go to all the work of building these more complex model if most of the information just comes from the rainfall?
# 3. Not what the reviewers asked for but for my own peace of mind, are the two models being tested on the same data?

# In[1]:

from hr_db_scripts.main_db_script import get_db_table_as_df
from db_scripts.main_db_script import db_filename


# In[2]:

def get_tables(table_suffix):


    rf_trn_tbl = 'rf{}trn'.format(table_suffix)
    rf_tst_tbl = 'rf{}tst'.format(table_suffix)
    ps_trn_tbl = 'poisson{}trn'.format(table_suffix)
    ps_tst_tbl = 'poisson{}tst'.format(table_suffix)

    rf_trn = get_db_table_as_df(rf_trn_tbl, dbfilename=db_filename)
    rf_tst = get_db_table_as_df(rf_tst_tbl, dbfilename=db_filename)
    ps_trn = get_db_table_as_df(ps_trn_tbl, dbfilename=db_filename)
    ps_tst = get_db_table_as_df(ps_tst_tbl, dbfilename=db_filename)
    return {'rf_trn': rf_trn, 'rf_tst': rf_tst, 'ps_trn': ps_trn, 'ps_tst': ps_tst}


# ### Question 3: are the models being tested on the same data?

# In[3]:

suffix = '_revisions_'
tables = get_tables(suffix)


# In[4]:

(tables['rf_trn']['all_trn'] != tables['ps_trn']['all_trn']).sum()


# In[5]:

(tables['rf_tst']['all_tst'] != tables['ps_tst']['all_tst']).sum()


# It looks like they weren't the same... Now we need to see how that affects the results

# ### Now the code has been refactored so they are the same

# In[6]:

suffix = '_revisions1_'
tables1 = get_tables(suffix)


# In[7]:

(tables1['rf_trn']['all_trn'] != tables1['ps_trn']['all_trn']).sum()


# In[8]:

(tables1['rf_tst']['all_tst'] != tables1['ps_tst']['all_tst']).sum()


# ### Question: do the results differ with the restructuring of the code?

# In[9]:

(tables1['rf_trn']['all_trn'] != tables['rf_trn']['all_trn']).sum()


# In[14]:

(tables1['rf_trn']['all_pred_trn'] != tables['rf_trn']['all_pred_trn']).sum()


# In[11]:

(tables1['rf_tst']['all_tst'] != tables['rf_tst']['all_tst']).sum()


# In[12]:

(tables1['ps_trn']['all_trn'] != tables['ps_trn']['all_trn']).sum()


# In[13]:

(tables1['ps_tst']['all_tst'] != tables['ps_tst']['all_tst']).sum()


# So now they are all the same
