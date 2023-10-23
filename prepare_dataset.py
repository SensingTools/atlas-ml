import pandas as pd
import numpy as np
import datetime

parcel = 1

# combine datasets into one
sentinel2_df = pd.read_csv('data/teledeteccion_sentinel2_parcel_{}.csv'.format(parcel))
copernicus_df = pd.read_csv('data/teledeteccion_copernicus_parcel_{}.csv'.format(parcel))
agroclimatology_df = pd.read_csv('data/agroclimatology_smooth_parcel_{}.csv'.format(parcel), usecols=['fecha', 'eto'])
soil_sensors_df = pd.read_csv('data/soil_sensors_parcel_{}.csv'.format(parcel))

# combine datasets into one having the same index
sentinel2_df['date'] = pd.to_datetime(sentinel2_df['date'])
sentinel2_df.set_index('date', inplace=True)
sentinel2_df.sort_index(inplace=True)

soil_sensors_df['date'] = pd.to_datetime(soil_sensors_df['date'])
soil_sensors_df.set_index('date', inplace=True)
soil_sensors_df.sort_index(inplace=True)

copernicus_df['date'] = pd.to_datetime(copernicus_df['date'])
copernicus_df.set_index('date', inplace=True)
copernicus_df.sort_index(inplace=True)

agroclimatology_df['fecha'] = pd.to_datetime(agroclimatology_df['fecha'])
agroclimatology_df.set_index('fecha', inplace=True)
agroclimatology_df.sort_index(inplace=True)

# find min and max dates of agroclimatology_df
min_date = agroclimatology_df.index[0]
max_date = agroclimatology_df.index[-1]

# remove duplicate dates
sentinel2_df = sentinel2_df[~sentinel2_df.index.duplicated(keep='first')]
copernicus_df = copernicus_df[~copernicus_df.index.duplicated(keep='first')]
agroclimatology_df = agroclimatology_df[~agroclimatology_df.index.duplicated(keep='first')]
soil_sensors_df = soil_sensors_df[~soil_sensors_df.index.duplicated(keep='first')]

# introduce all missing dates
idx = pd.date_range(agroclimatology_df.index[0], agroclimatology_df.index[-1])
sentinel2_df = sentinel2_df.reindex(idx, fill_value=np.nan)
copernicus_df = copernicus_df.reindex(idx, fill_value=np.nan)
agroclimatology_df = agroclimatology_df.reindex(idx, fill_value=np.nan)
soil_sensors_df = soil_sensors_df.reindex(idx, fill_value=np.nan)

# given the parcel study of best sensors, we need to remove the columns that are not needed (or so we have been told)
# TODO: needs further study
if parcel == 1:
    # keep columns that contain the string '90cm'
    soil_sensors_df = soil_sensors_df.filter(regex='90cm')
elif parcel == 2:
    # keep columns that contain the string '60cm', could be 120cm
    soil_sensors_df = soil_sensors_df.filter(regex='60cm')

# combine datasets into one
df = pd.concat([agroclimatology_df, sentinel2_df, copernicus_df, soil_sensors_df], axis=1)

# for simplicity, we will keep only columns of mean and eto
# TODO: needs further study
df = df.filter(regex='mean|eto')

# drop all rows that are not in min and max dates of agroclimatology_df
df = df.loc[(df.index >= min_date) & (df.index <= max_date)]

# save to csv with index column name
df.to_csv('data/parcel_{}_combined.csv'.format(parcel), index_label='date')
