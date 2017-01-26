import os
import pandas as pd
directory = os.path.dirname(__file__)
intersection_name = 'E VIRGINIA BEACH BOULEVARD & TIDEWATER DRIVE'
flood_df = pd.read_csv(os.path.join(directory, 'STORM_data_flooded_streets_2010-2016_no_duplicates_clean.csv'))
all_flood_dates = flood_df._date.str.strip().unique()
int_df = flood_df[flood_df.location == intersection_name]
int_df.loc[:, '_date'] = pd.to_datetime(int_df.loc[:, '_date'])
int_flood_dates = int_df._date
events = int_df.event.str.split('(', expand=True)[0].str.strip()
events.reset_index(drop=True, inplace=True)
int_flood_dates.reset_index(drop=True, inplace=True)
