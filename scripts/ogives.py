import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from tqdm import tqdm


def build_ogive_df(path_to_ogive_folder)
    # 
    path_to_ogive_folder = Path(path_to_ogive_folder)

    df_out = pd.DataFrame()

    for f in tqdm(path_to_ogive_folder.glob('*binned_ogives*.csv')):
        obs_time = f.stem[:13]
        _df = pd.read_csv(f, skiprows=11, index_col=1, na_values=-9999)
        _df = _df.dropna(subset=['og(w_ts)'])
        df_out[obs_time] = _df['og(w_ts)']


    plt.plot(df_out.median(axis=1), 'k-', label='median')
    plt.fill_between(df_out.index,
                    df_out.quantile(q=.95, axis=1),
                    df_out.quantile(q=.05, axis=1),
                    color='k', alpha=.1, label='5th-95th percentile')

    plt.axvline((1/(30*60)), c='k', ls=':', label='30 min')
    plt.axvline(1/(60*60), c='k', ls='-.', label='60 min')
    plt.axvline(1/(120*60), c='k', ls='--', label='120 min')

    plt.legend()

    plt.xscale('log')
    plt.xlabel('f (Hz)')
    plt.ylabel('Ogive w/ts');