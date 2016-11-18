import pandas as pd
intersection_name = 'E VIRGINIA BEACH BOULEVARD & TIDEWATER DRIVE'
df = pd.read_csv('norfolk_flood_data/STORM_data_flooded_streets_2010-2016_no_duplicates_clean.csv')
int_df = df[df.location == intersection_name]
int_df.loc[:, '_date'] = pd.to_datetime(int_df.loc[:, '_date'])
dates = int_df._date
events = int_df.event.str.split('(', expand=True)[0].str.strip()
events.reset_index(drop=True, inplace=True)
dates.reset_index(drop=True, inplace=True)
