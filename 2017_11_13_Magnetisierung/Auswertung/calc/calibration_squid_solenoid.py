#!/usr/bin/env python

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.odr import Model, ODR, RealData


DATA_PATH = '../data'


def regression_func(p, x):
        m, b = p
        return m*x + b


def voltage_current_regression():
    # read data from datafile
    df = pd.read_table(
        os.path.join(os.path.dirname(__file__), DATA_PATH, '1_a_soneloid.dat'),
        delim_whitespace=True,
        names=['current', 'voltage_min', 'voltage_max'],
        decimal=',',
        comment='#'
    )

    # add columns for voltage mean and error
    df['voltage_mean'] = 0.5 * (df['voltage_min'] + df['voltage_max'])
    df['voltage_error'] = df['voltage_max'] - df['voltage_min']

    # Create a model for fitting.
    linear_model = Model(regression_func)

    x = np.array(df['current'])
    y = np.array(df['voltage_mean'])
    sy = np.array(df['voltage_error'])

    data = RealData(x, y, sy=sy)

    odr = ODR(data, linear_model, beta0=[0., 1.])
    out = odr.run()

    return out

#
#    x_fit = np.linspace(0, 400, 1000)
#    y_fit = linear_func(out.beta, x_fit)
#
#    plt.errorbar(x, y, yerr=sy, linestyle='None', marker='x')
#    plt.plot(x_fit, y_fit)
#    plt.show()

if __name__ == '__main__':
    voltage_current_regression().pprint()
