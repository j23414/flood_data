
# coding: utf-8

# ## Intro
# When we expanded the dataset to include all of downtown Norfolk, some of the new flooding events
# recorded at the expanded circle of points considered occurred when there was very little or no
# rainfall recorded in the three days previous to the date of the recorded flood.
# This is some code to examine the flooding events where no rainfall occurred but flooding was
# still recorded

from db_scripts.get_server_data import data_dir, fig_dir
import pandas as pd
import matplotlib.pyplot as plt
import math
from mpl_toolkits.basemap import Basemap
import numpy as np

df = pd.read_csv("{}{}".format(data_dir, "reformatted_for_model_downtown_nor.csv"))
flooded_df = df[df.flooded & (df['rainfall_prev_3_days'] < 0.1)]
no_rain_dates = flooded_df['Datetime']
no_rain_dates.reset_index(drop=True, inplace=True)
all_df = pd.read_csv(
    '{}norfolk_flooded_roads_data/'
    'STORM_data_flooded_streets_2010-2016_no_duplicates_clean_lat_lon.csv'.format(data_dir))
all_df['_date'] = pd.to_datetime(all_df['_date'])
no_rain_floods = all_df[all_df['_date'].isin(no_rain_dates)]
locs = no_rain_floods['location']
subset_df = pd.read_csv('{}subset_points_data.txt'.format(data_dir))
subset_locs = locs[locs.isin(subset_df['location'])]
subset_locs.value_counts()

# plot the points
ncols = 4
nrows = int(math.ceil(float(len(no_rain_dates))/ncols))
fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=(6.75, 4))
ax_list = axs.ravel()
for i in range(len(no_rain_dates)):
    plot_df = all_df[all_df['_date'] == no_rain_dates[i]]
    # comment next line out to plot all 12 locations where such floods have occurred
#     plot_df = plot_df[plot_df['location'].isin(subset_locs)]  
    lats = all_df['lat']
    lons = all_df['lon']
    ax = ax_list[i]
    
    m = Basemap(resolution='f', projection='tmerc', lat_0 = lats.mean(), lon_0 = lons.mean(), ax=ax,
                llcrnrlon=lons.min()*1.0004,llcrnrlat=lats.min()*0.9999,
                urcrnrlon=lons.max()*0.9999,urcrnrlat=lats.max()*1.0003)
             
    m.drawcoastlines()
    m.drawmapboundary(fill_color='#abc6f2')
    m.fillcontinents(color = 'coral', lake_color='#abc6f2')
    
    latlabels = [1, 0, 0, 1] if i in [0, 4] else [0, 0, 0, 0]
    lonlabels = [1, 0, 0, 1] if i in [2, 3, 4, 5] else [0, 0, 0, 0]
    m.drawparallels(np.arange(34,38,0.05), labels=latlabels)
    meridians = m.drawmeridians(np.arange(-77, -75, 0.1), labels=lonlabels)
    for mer in meridians:
        try:
            meridians[mer][1][0].set_rotation(10)
        except:
            pass
    
    x, y = m(plot_df['lon'].tolist(), plot_df['lat'].tolist())
    ax.set_title(no_rain_dates[i])
    m.plot(x, y, 'bo', markersize=5)

ax_list[6].axis('off')
ax_list[7].axis('off')
plt.savefig('{}floods_with_no_rain'.format(fig_dir), dpi=300)
plt.show()
