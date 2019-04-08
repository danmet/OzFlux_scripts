import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import nc_to_df


def plot_variable(data, var, ax, window):
    """
    Helper function to plot indivdual variable on subplot.
    """
    ax.plot(data[f'{var}_SOLO'].resample('d').mean().rolling(
        window, center=True).mean(), 'k-', label=f'{var} SOLO')
    ax.plot(data[f'{var}_LL'].resample('d').mean().rolling(
        window, center=True).mean(), 'b-', label=f'{var} LL')
    ax.plot(data[f'{var}_LT'].resample('d').mean().rolling(
        window, center=True).mean(), 'r-', label=f'{var} LT')
    ax.legend(ncol=3)
    ax.set_ylabel(f'${var}\ (umol\ m^{-2}\ s^{-1})$')
    ax.set_xlabel('')


def plot_time_series(netcdf_file, window, outfile=None):
    """
    Function to plot time series of NEE, GPP and ER derived using SOLO, LL and
    LT.

    Parameters
    ----------
    netcdf_file : string
        path to source netcdf file
    window: interger
        number of days used to calculate running mean
    outfile (optional):
        path where plot will be saved

    Returns:
    --------
    Pyplot figure and optional saves figure to file
    """
    data = nc_to_df(netcdf_file)

    fig, (ax1, ax2, ax3) = plt.subplots(figsize=(10, 6), nrows=3, sharex=True)

    plot_variable(data, 'GPP', ax1, window)
    plot_variable(data, 'NEE', ax2, window)
    plot_variable(data, 'ER', ax3, window)

    plt.tight_layout()
    plt.show()

    if outfile:
        plt.savefig(outfile, dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    plot_time_series('./data/CumberlandPlain_2018_L6.nc', window=7)
