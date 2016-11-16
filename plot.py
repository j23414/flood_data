import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from norfolk_flood_data.focus_intersection import dates
from db_scripts.get_server_data import get_table_for_variable, Variable
import numpy as np


def resample_df(df, agg_typ):
    if agg_typ == 'mean':
        df = df.resample('D').mean()
    elif agg_typ == 'max':
        df = df.resample('D').max()
    elif agg_typ == 'min':
        df = df.resample('D').min()
    elif agg_typ == 'sum':
        df = df.resample('D').sum()
    return df


def filter_dfs(df, dates):
    return df.loc[pd.to_datetime(dates)]

def percentile(df):
    df['val_percentile'] = 1-(df.Value.rank()/max(df.Value.rank()))

def rank(df):
    df['val_rank'] = max(df.Value.rank()) + 1 - df.Value.rank()
    return df


def normalize(df):
    max_val = df.Value.max()
    min_val = df.Value.min()
    val_range = max_val - min_val
    df['scaled'] = (df.Value-min_val)/val_range
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
    df = get_table_for_variable(variable_id)
    if site_id:
        df = df[df.SiteID == site_id]
    v = Variable(variable_id)
    df = resample_df(df, agg_typ)
    df = normalize(df)
    df = rank(df)
    print df.val_rank.max()
    df = filter_dfs(df, dates)
    if plt_var == 'scaled':
        plot_bars(df, 'scaled', v.variable_name, agg_typ, 'Scaled')
    elif plt_var == 'rank':
        plot_bars(df, 'val_rank', v.variable_name, agg_typ, v.units)
    elif plt_var == 'value':
        plot_bars(df, 'Value', v.variable_name, agg_typ, v.units)


def autolabel(ax, rects, labs):
    # attach some text labels
    i = 0
    for rect in rects:
        height = rect.get_height()
        try:
            label = int(labs[i])
        except ValueError:
            if labs[i] == np.NaN:
                label = 'NA'
        ax.text(rect.get_x()+rect.get_width()/2, 0.25+height, label, rotation=75, ha='center', va='bottom')
        i += 1


def plot_bars(df, col, variable_name, agg_typ, units):
    df = df.dropna()
    fig = plt.figure()
    ind = np.arange(len(df.index))
    gs = gridspec.GridSpec(2, 2, width_ratios=[3.5, 1], height_ratios=[1, 1])
    ax0 = plt.subplot(gs[:, 0])
    bars = ax0.bar(ind, df[col])
    autolabel(ax0, bars, df.val_rank)
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
    ax1.text(0.5, 0.5, "rank out of \n{} \nobservations".format(int(df.val_rank.max())),
             multialignment='center', rotation=20, ha='center', va='bottom')
    ax1.set_title('Legend')
    width = 0.5
    ax1.bar((1-width)/2, 0.5, width=width)
    fig.tight_layout()
    plt.savefig("../Manuscript/pres/11.18.mtg/{}_{}.png".format(variable_name, col), dpi=300)
    plt.show()


plot_variable(4, 'max', dates, plt_var='value')

print dates
