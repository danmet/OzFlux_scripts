import pandas as pd
import xarray as xr
import numpy as np
from pathlib import Path


def nc_to_df(netcdf_file):
    """
    Helper function to load .nc file into pandas dataframe.
    """
    ds = xr.open_dataset(netcdf_file)
    df = ds.to_dataframe()
    # remove lat, lon from index
    df = df.reset_index([0, 1])
    df = df.replace(-9999, np.nan)
    return df


def concat_data(data_path, pattern):
    """
    Helper function to merge .nc file into one pandas dataframe.
    """
    data = pd.DataFrame()
    for f in data_path.glob(pattern):
        df = nc_to_df(f)
        data = pd.concat([data, df], sort=False)
    return data.sort_index()
