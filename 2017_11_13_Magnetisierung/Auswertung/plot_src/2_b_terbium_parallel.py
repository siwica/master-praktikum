#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import pandas as pd
import sys

from collections import OrderedDict

from matplotlib import rcParams

from calibration import magnetic_field, magnetization

DATA_PATH = '../data'
PLOTS_PATH = '../plots'
CALC_PATH = '../calc'

DATA_FILE_NAMES = ['2_b_1_terbium_parallel_50G_measurement_3.dat',
                   '2_b_2_terbium_parallel_100G.dat',
                   '2_b_3_terbium_parallel_150G_measurement_2.dat']

LEGEND_NAMES = [r'\textrm{parallel, cooled in field at 50 G}',
                r'\textrm{parallel, cooled in field at 100 G}',
                r'\textrm{parallel, cooled in field at 150 G}']

OFFSETS = [-0.01, -0.04, -0.01]

# import module from the ../calc directory
sys.path.append(os.path.join(os.path.dirname(__file__), CALC_PATH))
import calibration_squid_solenoid


def read_data(filename, names=['temperature', 'voltage'], decimal=',',
              comment='#'):
    """
    Reads a data file and returns the resulting Pandas Dataframe.
    """
    return pd.read_table(
        os.path.join(os.path.dirname(__file__), DATA_PATH, filename),
        delim_whitespace=True,
        names=names,
        decimal=decimal,
        comment=comment)


def main():
    # set plot styles
    plt.rc('text', usetex=True)
    rcParams.update({'figure.autolayout': True})

    # Read dataframe and add fields for magnetization and magnetic
    # field
    dfs = OrderedDict([(name, read_data(name)) for name in DATA_FILE_NAMES])
    for df in dfs.values():
        df['magnetization'] = magnetization(df['voltage'], orientation='parallel')
        df['magnetic_field'] = magnetic_field(df['voltage'], orientation='parallel')
        df['magnetic_field_rolling_mean'] = df['magnetic_field'].rolling(30).mean()
        df['temperature_rolling_mean'] = df['temperature'].rolling(30).mean()
        df['magnetic_field_derivation'] = (
            df['magnetic_field_rolling_mean'].diff() /
            df['temperature_rolling_mean'].diff())
        print(df.loc[df['magnetic_field_derivation'].idxmin()])

    for idx, (name, df) in enumerate(dfs.items()):
        df['magnetic_field'] = df['magnetic_field'] + OFFSETS[idx]
        plt.plot(df['temperature'], df['magnetic_field'],
                 label=LEGEND_NAMES[idx])

    # plt.xlim(70, 2700)
    # plt.ylim(-1000, 300000)
    # plt.ylim(-1, 2)
    plt.legend(loc='best')
    plt.xlabel('$T$ in $K$')
    plt.ylabel(r'$B/T$ in $G/K$')
    plt.axis()
    # plt.show()
    plt.savefig('../plots/2_b_parallel.eps')


if __name__ == '__main__':
    main()
