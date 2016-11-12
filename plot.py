import pandas as pd
import matplotlib.pyplot as plt
from norfolk_flood_data.focus_intersection import dates
from db_scripts.get_server_data import get_table_for_variable, Variable
import numpy as np


def resample_df(df, typ):
    if typ == 'mean':
        df = df.resample('D').mean()
    elif typ == 'max':
        df = df.resample('D').max()
    elif typ == 'min':
        df = df.resample('D').min()
    elif typ == 'sum':
        df = df.resample('D').sum()
    return df


def filter_dfs(df, dates):
    return df.loc[pd.to_datetime(dates)]


def plot_variable(variable_id, typ, dates, **kwargs):
    df = get_table_for_variable(variable_id)
    if variable_id == 5:
        df = df[df.SiteID == kwargs['site_id']]
    v = Variable(variable_id)
    df = resample_df(df, typ)
    df = filter_dfs(df, dates)
    plot_bars(df, v.variable_name, typ, dates, v.units)


def plot_bars(df, variable_name, typ, dates, units):
    fig, ax = plt.subplots()
    ind = np.arange(len(df.index))
    ax.bar(ind, df.Value)
    ax.set_xticks(ind+0.5)
    ax.set_xticklabels(df.index, rotation=90)
    ax.set_ylabel(units)
    ax.set_xlim(0, len(ind))
    ax.set_title("{} {}".format(variable_name, typ))
    fig.tight_layout()
    plt.show()


plot_variable(5, 'sum', dates, site_id=6.)

print dates
