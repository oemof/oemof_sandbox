"""
Example, which shows the difference between the new approach and a fix efficiency.
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_collector_heat(data_precalc, periods, eta_0):
    '''
    Plot showing the difference between a constant efficiency and the efficiency depending on the ambient temperature for the same irradiance and hour of the day.
    '''

    heat_calc = data_precalc['collectors_heat']
    irradiance_on_collector = data_precalc['col_ira']
    heat_compare = irradiance_on_collector * eta_0
    t = list(range(1, periods+1))


    fig, ax = plt.subplots()
    ax.plot(t, heat_calc, label='CSP precalculation')
    ax.plot(t, heat_compare, label='constant efficiency')
    ax.set(xlabel='time (h)', ylabel='Q_coll in kWh',
           title='Heat of the collector')
    ax.grid()
    ax.legend()
    plt.savefig('compare_precalculations.png')

    return
