# coding: utf-8
import pandas as pd
df1 = pd.read_csv('STORM_data_flooded_streets_2010-2016.csv')
locations = df1.loc[:,'location']
locations = pd.Series(locations.unique())
loc_split = locations.str.split('&')

for i in range(len(loc_split)):
    loc_split[i] = [a.strip() for a in loc_split[i]]

sorted_loc_split = loc_split
for i in range(len(sorted_loc_split)):
    sorted_loc_split[i].sort()

loc_split_strs = loc_split.astype(str)
sorted_loc_strs = sorted_loc_split.astype(str)
df = pd.concat([loc_split_strs, sorted_loc_strs], axis=1)
