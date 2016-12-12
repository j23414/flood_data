from norfolk_flood_data.focus_intersection import int_flood_dates
import pandas as pd
from get_server_data import get_table_for_variable


def filter_df_by_dates(df, dates=int_flood_dates):
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


def get_plottable_df(variable_id, agg_typ, site_id=None):
    df = get_table_for_variable(variable_id)
    if site_id:
        df = df[df.SiteID == site_id]
    df = resample_df(df, agg_typ)
    if variable_id == 5:
        # take out days with no rain
        df = df[df.Value != 0]
    df = normalize(df)
    df = rank(df)
    df = percentile(df)
    df = filter_df_by_dates(df)
    df['Value'].fillna(0, inplace=True)
    return df


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
    df['SiteID'] = ori_df.SiteID[0]
    df['VariableID'] = ori_df.VariableID[0]
    return df



