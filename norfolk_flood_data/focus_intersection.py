import pandas as pd
intersection_name = 'E VIRGINIA BEACH BOULEVARD & TIDEWATER DRIVE'
df = pd.read_csv('STORM_data_flooded_streets_2010-2016_no_duplicates_clean.csv')
int_df = df[df.location == intersection_name]
