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

DATA_FILE_NAMES = ['2_a_1_terbium_perpendicular_0G.dat',
                   '2_a_2_terbium_perpendicular_150G.dat',
                   '2_a_3_terbium_perpendicular_150G.dat']

OFFSETS = [-0.11, -0.07, 0.07]

LEGEND_NAMES = [r'\textrm{cooled without field, not subsequntly magnetized}',
                r'\textrm{cooled without field, subsequntly magnetized with~} B=150G',
                r'\textrm{cooled in field of~} B=150 G']


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
        df['magnetization'] = magnetization(df['voltage']) 
        df['magnetic_field'] = magnetic_field(df['voltage'])
        df['magnetic_field_rolling_mean'] = df['magnetic_field'].rolling(30).mean()
        df['temperature_rolling_mean'] = df['temperature'].rolling(30).mean()
        df['magnetic_field_derivation'] = (
            df['magnetic_field_rolling_mean'].diff() /
            df['temperature_rolling_mean'].diff())


        # print(df.loc[df['magnetic_field_derivation'].idxmin()])

        # fig = plt.figure()

    for idx, (name, df) in enumerate(dfs.items()):
        # df['magnetic_field'] = df['magnetic_field'] + OFFSETS[idx]
        # plt.plot(df['temperature'], df['magnetic_field'],
        #          label=LEGEND_NAMES[idx])
        # plt.plot(df['temperature'], df['magnetic_field']
        plt.plot(df['temperature'], df['magnetic_field_derivation'],
                 label=LEGEND_NAMES[idx])

    # plt.xlim(70, 2700)
    # plt.ylim(-1000, 300000)
    # plt.ylim(-1, 2)
    plt.xlabel('$T$ in $K$')
    plt.ylabel(r'$B$ in $G$')
    plt.legend(loc='best')
    plt.savefig('../plots/2_a_perpendicular.eps')


if __name__ == '__main__':
    main()
