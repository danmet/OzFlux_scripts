import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import nc_to_df


def plot_variable(data, var, ax, window):
    """
    Helper function to plot indivdual variable on subplot.
    """
    data[f'{var}_SOLO'].resample('d').mean().rolling(
        window, center=True).mean().plot(color='k', ax=ax, label=f'{var} SOLO')
    data[f'{var}_LL'].resample('d').mean().rolling(
        window, center=True).mean().plot(color='b', ax=ax, label=f'{var} LL')
    data[f'{var}_LT'].resample('d').mean().rolling(
        window, center=True).mean().plot(color='r', ax=ax, label=f'{var} LT')
    ax.legend(ncol=3)
    ax.set_ylabel(f'${var}\ (umol\ m^{-2}\ s^{-1})$')


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

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312, sharex=ax1)
    ax3 = fig.add_subplot(313, sharex=ax1)

    plot_variable(data, 'GPP', ax1, window)
    plot_variable(data, 'NEE', ax2, window)
    plot_variable(data, 'ER', ax3, window)

    plt.xlabel('')
    plt.tight_layout()
    plt.show()

    if outfile:
        plt.savefig(outfile, dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    plot_time_series('./data/CumberlandPlain_2018_L6.nc', window=7)
