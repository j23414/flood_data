# coding: utf-8
from hr_db_scripts.main_db_script import get_table_for_variable_code
import pandas as pd
import sqlite3


def get_df_for_dates(df, dates):
    l = []
    for d in dates:
        l.append(df[d])
    cdf = pd.concat(l)
    return cdf.pivot(columns='SiteID', values='Value')

con = sqlite3.connect('floodData.sqlite')
table = "flood_events"
fe = pd.read_sql_query(con=con, sql=sql)
fe_hg = fe[fe.location.isin(hg.location)]
fe_hg.event_name.unique()
fe[fe.location.isin(hg_1.location)]
fe_hg.groupby('event_name').count()
fe_hg.groupby('event_name')['location'].count().sort_values()
fe_hg = fe[fe.location.isin(hg.location)]
fe_hg.groupby('event_name')['location'].count().sort_values(ascending=False)
raindf = get_table_for_variable_code('rainfall')

hr = get_df_for_dates(raindf, ['2016-09-02', '2016-09-03', '2016-09-04'])
th = get_df_for_dates(raindf, ['2010-10-08', '2010-10-09', '2010-10-10'])
crn = get_table_for_variable_code('rainfall_cummulative')
thc = th.cumsum()
th = get_df_for_dates(raindf, ['2013-10-08', '2013-10-09', '2013-10-10'])
thc = th.cumsum()
del thc[14]
crn = pivot(columns='SiteID', values='Value')
crn = crn.pivot(columns='SiteID', values='Value')
crn.resample('15T')
crn.resample('15T').mean()
cr = crn.resample('15T').mean()
cr['2010-10-10'] += cr['2010-10-09'].max()
cr['2013-10-10'] += cr['2013-10-09'].max()
tide = get_table_for_variable_code('hourly_height')
hr_dates = ['2016-09-04']
hr_dates = ['2016-09-02','2016-09-03','2016-09-04']
hrtid = get_df_for_dates(tide, hr_dates)
hrc = hr.cumsum()
hrtid.resample('15T').mean()
tide = get_table_for_variable_code('six_min_tide')
hrtid = get_df_for_dates(tide, hr_dates)
hrtidf = hrtid.resample('15T').mean()
th_dates = ['2013-10-08', '2013-10-09', '2013-10-10']
th = get_df_for_dates(raindf, th_dates)
tht = get_df_for_dates(tide, th_dates)
thtf = tht.resample('15T').mean()
