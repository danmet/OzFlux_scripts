import pandas as pd
import xarray as xr
import numpy as np


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
