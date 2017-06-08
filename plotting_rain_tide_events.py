# coding: utf-8
import matplotlib.pyplot as plt
from hr_db_scripts.main_db_script import get_df_for_dates
from db_scripts.main_db_script import fig_dir
import pandas as pd


def plot_rain_tide(dates):
    evrain = get_df_for_dates('rainfall', dates[0], dates[-1])
    if '2013-10-09' in dates:
        del evrain[14]
    evrain = evrain.mean(axis=1)
    evrain.rename('rain', inplace=True)
    evtide = get_df_for_dates('six_min_tide', dates[0], dates[-1]).resample('15T').mean()
    evtide = evtide.mean(axis=1)
    evtide.rename('tide', inplace=True)
    evgw = get_df_for_dates('shallow_well_depth', dates[0], dates[-1]).resample('15T').mean()
    evgw = evgw.mean(axis=1)
    evgw.rename('gw', inplace=True)
    evrainc = evrain.cumsum()

    y_label = 'Tide Level (ft above MSL)/\nCumulative Rainfall (in)'
    x_label = 'Date'
    ax = pd.concat([evrainc, evtide, evgw], axis=1).plot()
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(ymax=13)
    plt.tight_layout()
    plt.savefig("{}event_plot_gw{}".format(fig_dir, dates[0]), dpi=300)
    plt.show()

hr_dates = ['2016-09-02', '2016-09-03', '2016-09-04']
plot_rain_tide(hr_dates)
th_dates = ['2013-10-08', '2013-10-09', '2013-10-10']
plot_rain_tide(th_dates)
matth_dates = ['2016-10-08', '2016-10-09', '2016-10-10']
plot_rain_tide(matth_dates)
jqn_dates = ['2015-09-30', '2015-10-01', '2015-10-02', '2015-10-03', '2015-10-04', '2015-10-05']
plot_rain_tide(jqn_dates)

