# coding: utf-8
import matplotlib.pyplot as plt
from hr_db_scripts.main_db_script import get_table_for_variable_code, get_db_table_as_df
from db_scripts.main_db_script import fig_dir, db_filename
import pandas as pd

raindf = get_table_for_variable_code('rainfall')
tide = get_table_for_variable_code('six_min_tide')


def get_df_for_dates(df, dates):
    l = []
    for d in dates:
        l.append(df[d])
    cdf = pd.concat(l)
    return cdf.pivot(columns='SiteID', values='Value')


def plot_rain_tide(dates):
    evrain = get_df_for_dates(raindf, dates)
    evtide = get_df_for_dates(tide, dates)
    evtidf = evtide.resample('15T').mean()
    evrainc = evrain.cumsum()
    if '2013-10-09' in dates:
        del evrainc[14]
    y_label = 'Tide Level (ft above MSL)/\nCumulative Rainfall (in)'
    x_label = 'Date'
    ax = pd.concat([evrainc, evtidf], axis=1).plot(legend=None)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(ymax=13)
    plt.tight_layout()
    plt.savefig("{}event_plot_scaled{}".format(fig_dir, dates[0]), dpi=300)
    plt.show()

hr_dates = ['2016-09-02', '2016-09-03', '2016-09-04']
plot_rain_tide(hr_dates)
th_dates = ['2013-10-08', '2013-10-09', '2013-10-10']
plot_rain_tide(th_dates)
# matth_dates = ['2016-10-08', '2016-10-09', '2016-10-10']
# plot_rain_tide(matth_dates)


