import pandas as pd
import matplotlib.pyplot as plt
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


def rank(df):
    df['val_rank'] = max(df.Value.rank()) + 1 - df.Value.rank()
    return df


def normalize(df):
    max_val = df.Value.max()
    min_val = df.Value.min()
    val_range = max_val - min_val
    df['scaled'] = (df.Value-min_val)/val_range
    return df


def plot_variable(variable_id, agg_typ, dates, site_id=None, plt_var=False):
    """
    plots bar charts for a given variable given a list of dates
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
        ax.text(rect.get_x()+rect.get_width()/2.5, 0.25+height, int(labs[i]), rotation=75, ha='center', va='bottom')
        i += 1


def plot_bars(df, col, variable_name, agg_typ, units):
    fig, ax = plt.subplots()
    ind = np.arange(len(df.index))
    bars = ax.bar(ind, df[col])
    autolabel(ax, bars, df.val_rank)
    ax.set_xticks(ind+0.5)
    ax.set_xticklabels(df.index.strftime("%Y-%m-%d"), rotation=90)
    ax.set_ylabel(units)
    ax.set_xlim(0, len(ind))
    ax.set_ylim(0, df[col].max()*1.1)
    ax.set_title("{} {}".format(variable_name, agg_typ))
    fig.tight_layout()
    plt.savefig("../Manuscript/pres/11.18.mtg/{}_{}.png".format(variable_name, col))
    plt.show()


plot_variable(5, 'sum', dates, site_id=6, plt_var='value')

print dates
