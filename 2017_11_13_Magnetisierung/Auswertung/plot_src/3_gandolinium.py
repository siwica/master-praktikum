#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import pandas as pd
import sys

from matplotlib import rcParams

from calibration import magnetic_field, magnetization

DATA_PATH = '../data'
PLOTS_PATH = '../plots'
CALC_PATH = '../calc'

DATA_FILE_NAMES = ['2_c_gadolinium_turned_1000G.dat']

LEGEND_NAMES = [r'\textrm{cooled in field at 150 G}']

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
    dfs = {name: read_data(name) for name in DATA_FILE_NAMES}
    for df in dfs.values():
        df['magnetization'] = magnetization(df['voltage'])
        df['magnetic_field'] = magnetic_field(df['voltage'])
        
        # fig = plt.figure()

    for idx, (name, df) in enumerate(dfs.items()):
        plt.plot(df['temperature'], df['magnetic_field'],
                 label=LEGEND_NAMES[idx])

    # plt.xlim(70, 2700)
    # plt.ylim(-1000, 300000)
    # plt.ylim(-1, 2)
    plt.legend(loc='best')
    plt.xlabel('$T$ in $K$')
    plt.ylabel(r'$B$ in $G$')
    plt.axis()
    # plt.show()
    plt.savefig('../plots/3_gandolinium.eps')


if __name__ == '__main__':
    main()
