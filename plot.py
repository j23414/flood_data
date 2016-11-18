import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from norfolk_flood_data.focus_intersection import dates
from db_scripts.get_server_data import get_table_for_variable, Variable
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D


def resample_df(df, agg_typ):
    ori_df = df
    if agg_typ == 'mean':
        df = df.resample('D').mean()
    elif agg_typ == 'max':
        df = df.resample('D').max()
    elif agg_typ == 'min':
        df = df.resample('D').min()
    elif agg_typ == 'sum':
        df = df.resample('D').sum()
    df['SiteId'] = ori_df.SiteID[0]
    df['VariableID'] = ori_df.VariableID[0]
    return df


def filter_dfs(df, dates):
    return df.loc[pd.to_datetime(dates)]


def percentile(df):
    df['val_percentile'] = (df.Value.rank()/max(df.Value.rank()))*100
    return df


def rank(df):
    df['val_rank'] = max(df.Value.rank()) + 1 - df.Value.rank()
    return df


def normalize(df):
    max_val = df.Value.max()
    min_val = df.Value.min()
    val_range = max_val - min_val
    df['scaled'] = (df.Value-min_val)/val_range
    return df


def get_plottable_df(variable_id, agg_typ, dates, site_id=None):
    df = get_table_for_variable(variable_id)
    if site_id:
        df = df[df.SiteID == site_id]
    df = resample_df(df, agg_typ)
    df = normalize(df)
    df = rank(df)
    df = percentile(df)
    print df.val_rank.max()
    df = filter_dfs(df, dates)
    df['Value'].fillna(0, inplace=True)
    return df


def plot_variable(variable_id, agg_typ, dates, site_id=None, plt_var='value'):
    """
    plots bar charts for a given variable given a list of dates
    :param plt_var:
    :param variable_id: 4-tide level, 5-rainfall, 6-shallow well depth
    :param agg_typ: how to aggregate the data on the daily time step ('min', 'max', 'mean', 'sum')
    :param dates: list of dates
    :param site_id: site_id on which to filter (mostly for rainfall since there are multiple gauges
    :return:
    """
    df = get_plottable_df(variable_id, agg_typ, dates, site_id)
    v = Variable(variable_id)
    if plt_var == 'scaled':
        return plot_bars(df, 'scaled', v.variable_name, agg_typ, 'Scaled')
    elif plt_var == 'rank':
        return plot_bars(df, 'val_rank', v.variable_name, agg_typ, v.units)
    elif plt_var == 'value':
        return plot_bars(df, 'Value', v.variable_name, agg_typ, v.units)


def autolabel(ax, rects, labs):
    # attach some text labels
    i = 0
    for rect in rects:
        height = rect.get_height()
        height = 0 if math.isnan(height) else height
        try:
            label = int(labs[i])
        except ValueError:
            if math.isnan(labs[i]):
                label = 'NA'
        ax.text(rect.get_x()+rect.get_width()/2, 0.25+height, label, rotation=75, ha='center',
                va='bottom')
        i += 1


def plot_bars(df, col, variable_name, agg_typ, units):
    fig = plt.figure()
    ind = np.arange(len(df.index))
    gs = gridspec.GridSpec(2, 2, width_ratios=[3.5, 1], height_ratios=[1, 1])
    ax0 = plt.subplot(gs[:, 0])
    bars = ax0.bar(ind, df[col])
    autolabel(ax0, bars, df.val_percentile)
    ax0.set_xticks(ind+0.5)
    ax0.set_xticklabels(df.index.strftime("%Y-%m-%d"), rotation=90)
    ax0.set_ylabel(units)
    ax0.set_xlabel('Date')
    ax0.set_xlim(0, len(ind))
    ax0.set_ylim(0, df[col].max()*1.1)
    ax0.set_title("{} {}".format(variable_name, agg_typ))

    ax1 = plt.subplot(gs[-1])
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.xaxis.set_ticklabels([])
    ax1.yaxis.set_ticklabels([])
    ax1.text(0.5, 0.5, "percentile",
             multialignment='center', rotation=20, ha='center', va='bottom')
    ax1.set_title('Legend')
    width = 0.5
    ax1.bar((1-width)/2, 0.5, width=width)
    fig.tight_layout()
    plt.savefig("../Manuscript/pres/11.18.mtg/{}_{}.png".format(variable_name, col), dpi=300)
    plt.close()
    return df


def plot_together(df_list):
    i = 0
    fig, ax = plt.subplots(figsize=(15, 5))
    cols = '#a6cee3', '#d95f02', '#1f78b4'
    for df in df_list:
        v = Variable(df.VariableID.dropna()[0])
        size = 2
        ind = np.arange(0, len(df.index)*size, size) + i*size*.25
        ax.bar(ind, df.val_percentile, label=v.variable_name, color=cols[i], width=size*.25)
        i += 1
    ax.set_ylim(0, 110)
    ax.set_xlim(0)
    ax.set_ylabel('Percentile')
    ax.set_xticks(ind-.2*size)
    ax.set_xticklabels(df.index.strftime("%Y-%m-%d"), rotation=90, ha='left')
    lgd = ax.legend(bbox_to_anchor=(0.5, -0.3), loc='upper center')
    fig.tight_layout()
    fig.savefig("../Manuscript/pres/11.18.mtg/all.png", dpi=300, bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()


def plot_3d():
    plot_tide_data = get_plottable_df(4, 'max', dates)
    plot_gw_data = get_plottable_df(6, 'mean', dates)
    plot_rain_data = get_plottable_df(5, 'sum', dates, site_id=6)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x0 = plot_tide_data.val_percentile
    x1 = plot_gw_data.val_percentile
    x2 = plot_rain_data.val_percentile
    ax.scatter(x0, x1, x2)
    ax.set_xlabel('Tide Percentile')
    ax.set_ylabel('Shallow Well Percentile')
    ax.set_zlabel('Rainfall Percentile')
    ax.set_xlim(100, 0)
    plt.show()


plot_tide_data = get_plottable_df(4, 'max', dates)
plot_gw_data = get_plottable_df(6, 'mean', dates)
plot_rain_data = get_plottable_df(5, 'sum', dates, site_id=6)
df_list = [plot_tide_data, plot_gw_data, plot_rain_data]
plot_together(df_list)

print dates