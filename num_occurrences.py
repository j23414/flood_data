import pandas as pd
df = pd.read_csv('STORM_data_flooded_streets_2010-2016.csv')
df_orig = df
df_dups = pd.read_csv('duplicates.csv')

dup = []
for i in range(len(df.location)):
    loc_orig = df.location[i]
    loc_orig = loc_orig.strip()
    for j in range(len(df_dups.a)):
        loc_dup = df_dups.a[j]
        if loc_orig == loc_dup:
            df.location[i] = df_dups.b[j]
            dup.append(df_dups.a[j])
            print df_dups.a[j]
            continue
pd.Series(dup).to_csv('duplicates_removed.csv')
df.to_csv('STORM_data_flooded_streets_2010-2016_no_duplicates.csv')
