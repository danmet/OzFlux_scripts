import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from utils import nc_to_df, concat_data


def plot_minmaxmean(data, window, outfile=None):
    """
    Function to plot time series of daily min, max and mean VPD and Ta.

    Parameters
    ----------
    data : pandas dataframe
        dataframe containing VPD and Ta column
    window: interger
        number of days used to calculate running mean
    outfile (optional):
        path where plot will be saved

    Returns:
    --------
    Pyplot figure and optional saves figure to file
    """

    fig, (ax1, ax2) = plt.subplots(figsize=(8, 6), nrows=2, sharex=True)

    ax1.plot(data['VPD'].resample('d').min(), 'b-', lw=1, alpha=.3, label='')
    ax1.plot(data['VPD'].resample('d').min().rolling(
        window).mean(), 'b-', lw=1, label='min')
    ax1.plot(data['VPD'].resample('d').max(), 'r-', lw=1, alpha=.3, label='')
    ax1.plot(data['VPD'].resample('d').max().rolling(
        window).mean(), 'r-', lw=1, label='max')
    ax1.plot(data['VPD'].resample('d').mean(), 'k-', lw=1, alpha=.3, label='')
    ax1.plot(data['VPD'].resample('d').mean().rolling(
        window).mean(), 'k-', lw=1, label='mean')
    ax1.legend(loc='upper left', ncol=3)
    ax1.set_ylabel(u'VPD (kPa)')

    ax2.plot(data['Ta'].resample('d').min(), 'b-', lw=1, alpha=.3, label='')
    ax2.plot(data['Ta'].resample('d').min().rolling(
        window).mean(), 'b-', lw=1, label='min')
    ax2.plot(data['Ta'].resample('d').max(), 'r-', lw=1, alpha=.3, label='')
    ax2.plot(data['Ta'].resample('d').max().rolling(
        window).mean(), 'r-', lw=1, label='max')
    ax2.plot(data['Ta'].resample('d').mean(), 'k-', lw=1, alpha=.3, label='')
    ax2.plot(data['Ta'].resample('d').mean().rolling(
        window).mean(), 'k-', lw=1, label='mean')
    ax2.legend(loc='upper left', ncol=3)
    ax2.set_ylabel(u'Air temperature (℃)')

    plt.tight_layout()
    plt.show()

    if outfile:
        plt.savefig(outfile, dpi=300, bbox_inches='tight')


def main():
    data_path = Path('./data')
    data = concat_data(data_path, '*L6.nc*')
    plot_minmaxmean(data, 7)


if __name__ == '__main__':
    main()
