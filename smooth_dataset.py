from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import datetime

parcel = 2

df = pd.read_csv('data/agroclimatology_parcel_{}.csv'.format(parcel))

# convert date column to datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# set date column as index
df.set_index('fecha', inplace=True)

# remove duplicate dates
df = df[~df.index.duplicated(keep='first')]
df.sort_index(inplace=True)

# introduce all missing dates
idx = pd.date_range(df.index[0], df.index[-1])
df = df.reindex(idx, fill_value=np.nan)

# find all values that has a percentage change greater or lower than X and assign them to NaN
df['eto_pct_change'] = df['eto'].pct_change()
df.loc[df['eto_pct_change'] < -0.5, 'eto'] = np.nan
df.loc[df['eto_pct_change'] > 0.5, 'eto'] = np.nan

# interpolate points of data that have a 100% change in value with respect to the previous point
df['eto'] = df['eto'].interpolate(method='linear')

# smooth data
df['eto'] = df['eto'].rolling(7).mean()

# remove pct_change column
df.drop('eto_pct_change', axis=1, inplace=True)

# save to csv with index column name
df.to_csv('data/agroclimatology_smooth_parcel_{}.csv'.format(parcel), index_label='fecha')

# plot
df.plot(y='eto')
plt.show()
