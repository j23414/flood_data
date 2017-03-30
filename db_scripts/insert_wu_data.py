import pandas as pd
from get_server_data import data_dir, append_non_duplicates


# add wind direction data to database
rawdf = pd.read_csv('{}wu/norf_data.csv'.format(data_dir))
rawdf.columns = rawdf.columns.str.strip()
siteid = 11
varid = 13
qcid = 0
df = pd.DataFrame()
df['Datetime'] = rawdf['EST']
df['SiteID'] = siteid
df['VariableID'] = varid
df['QCID'] = qcid
df['Value'] = rawdf['WindDirDegrees']
append_non_duplicates('datavalues', df, ['SiteID', 'Datetime', 'VariableID'])
