import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from tqdm import tqdm
from statsmodels.nonparametric.smoothers_lowess import lowess


def get_good_files(ep_output_folder):
    full_output_file = glob(f'{ep_output_folder}/**full_output*.csv*')[0]
    df = pd.read_csv(full_output_file, skiprows=[0, 2], parse_dates=True)
    df = df.query('qc_co2_flux == 0')
    good_files = df['filename'].values
    return good_files


def merge_good_files(good_files, ep_output_folder):
    good_spectras = pd.DataFrame()
    good_cospectras = pd.DataFrame()
    for f in tqdm(good_files):
        pattern = f'{f[5:13]}-{f[-8:-4]}'
        try:
            full_sectra_file = glob(
                f'{ep_output_folder}/eddypro_full_cospectra/*{pattern}*.csv')[0]
        except IndexError as ie:
            #         print(f'no file for {pattern} found in cospectra folder. skipping timestamp.')
            continue
        df = pd.read_csv(full_sectra_file, skiprows=12,
                         index_col=0, na_values=-9999)
        df = df.dropna()
        good_spectras[pattern] = df['f_nat*spec(ts)']
        good_cospectras[pattern] = df['f_nat*cospec(w_ts)']
    return good_spectras, good_cospectras


def plot_spectras(df, outfile=None):
    plt.figure()
    plt.plot(df.median(axis=1), 'k-', label='data with QC flag 0')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f (Hz)')
    plt.ylabel('spectra (T)')
    plt.legend()
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=300, bbox_inches='tight')
    plt.show()


def plot_cospectras(df, outfile=None):
    plt.figure()
    plt.plot(df.median(axis=1), 'k.', alpha=.05, label='data with QC flag 0')

    smoothed = lowess(df.median(axis=1).values,
                      df.index, is_sorted=True, frac=0.025, it=0)
    plt.plot(smoothed[:, 0], smoothed[:, 1], 'b')

    x = np.linspace(0.2, 5)
    y1 = .006*x**(-4/3)
    y2 = .01*x**(-10/3)
    plt.plot(x, y1, 'r--', label='-4/3 slope')
    plt.plot(x, y2, 'r:', label='-10/3 slope')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('f (Hz)')
    plt.ylabel('cospectra (w/T)')
    plt.legend()
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    good_files = get_good_files(
        r'E:\flux_data_processing\10hz_data\MOFO_understory\ep_output\13m_canopy_height')
    good_spectras, good_cospectras = merge_good_files(
        good_files, r'E:\flux_data_processing\10hz_data\MOFO_understory\ep_output\13m_canopy_height')
    plot_spectras(good_spectras)
    plot_cospectras(good_cospectras)


if __name__ == '__main__':
    main()
