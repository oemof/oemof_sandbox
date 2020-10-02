# -*- coding: utf-8 -*-

"""
Date: 17.09.2020
Author: Franziska Pleissner

This file shows a comparison between the collector heat, which is calculated
with the oemof-thermal component and the collector heat, which is measured.
It uses the irradiance data, which are measured at the same spot and the same
time as the collector heat data.
"""

############
# Preamble #
############

# Import packages
from oemof.thermal.concentrating_solar_power import csp_precalc

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# Define the used directories
abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__)))
results_path = abs_path + '/results/'
data_path = abs_path + '/data/validation_data/'

# Read parameter values from parameter file
file_path_param = data_path + 'validation_parameters.csv'
param_df = pd.read_csv(file_path_param, index_col=1)
param_value = param_df['value']

# Define some needed parameters
currentdate = datetime.today().strftime('%Y%m%d')
number_of_time_steps = int(param_value['number_timesteps'])

# Import weather and demand data
dataframe = pd.read_csv(
    data_path + 'validation_timeseries.csv').head(number_of_time_steps)
dataframe['Date'] = pd.to_datetime(dataframe['Date'])
dataframe.set_index('Date', inplace=True)
dataframe = dataframe.asfreq('H')

# Calculate collector data
collector_precalc_data_normal = csp_precalc(
    param_value['latitude'],
    param_value['longitude'],
    param_value['collector_tilt'],
    param_value['collector_azimuth'],
    param_value['cleanliness'],
    param_value['eta_0'],
    param_value['c_1'],
    param_value['c_2'],
    param_value['inlet_temp_mean'],
    param_value['outlet_temp_mean'],
    dataframe['Ambient_temperature_in_degC'],
    param_value['a_1'],
    param_value['a_2'],
    param_value['a_3'],
    param_value['a_4'],
    param_value['a_5'],
    param_value['a_6'],
    loss_method='Andasol',
    irradiance_method='normal',
    dni=dataframe['dni_in_W_per_m2'])

collector_precalc_data_horizontal = csp_precalc(
    param_value['latitude'],
    param_value['longitude'],
    param_value['collector_tilt'],
    param_value['collector_azimuth'],
    param_value['cleanliness'],
    param_value['eta_0'],
    param_value['c_1'],
    param_value['c_2'],
    param_value['inlet_temp_mean'],
    param_value['outlet_temp_mean'],
    dataframe['Ambient_temperature_in_degC'],
    param_value['a_1'],
    param_value['a_2'],
    param_value['a_3'],
    param_value['a_4'],
    param_value['a_5'],
    param_value['a_6'],
    loss_method='Andasol',
    E_dir_hor=dataframe['E_dir_hor_in_W_per_m2'])

collector_precalc_data_normal.to_csv(
    results_path + 'validation_precalc_data_normal_{0}.csv'.format(currentdate))

collector_precalc_data_horizontal.to_csv(
    results_path + 'validation_precalc_data_horizontal_{0}.csv'.format(
        currentdate))

result_df = pd.DataFrame()
result_df['method normal'] = collector_precalc_data_normal[
    'collector_heat']
result_df['method horizontal'] = collector_precalc_data_horizontal[
    'collector_heat']
result_df['Andasol data'] = dataframe[
    'collector_field_heat_output_in_W_per_m2']
new_row = pd.Series(
    data={'method normal': result_df['method normal'].sum(),
          'method horizontal': result_df['method horizontal'].sum(),
          'Andasol data': result_df['Andasol data'].sum()},
    name='Sums')
result_df_csv = result_df.append(new_row, ignore_index=False)
result_df_csv.to_csv(results_path + 'validation.csv')

results_summer_1 = result_df[4080:4248]
results_summer_2 = result_df[4248:4416]
results_winter = result_df[672:840]

result_df.plot(kind='line', linewidth=2)
plt.title('specific collector heat output', size=25)
plt.ylabel('collector heat output [W/m2]', size=25)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,
           prop={'size': 25})
plt.yticks(size=25)
figure = plt.gcf()
figure.set_size_inches(30, 15)
plt.savefig(results_path + 'validation_results_{0}.png'.format(currentdate),
            dpi=150, bbox_inches='tight')

results_summer_1.plot(kind='line', linewidth=3)
plt.title('specific collector heat output (20.06-26.06.2019)', size=25)
plt.ylabel('collector heat output [W/m2]', size=25)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,
           prop={'size': 25})
plt.yticks(size=25)
figure = plt.gcf()
figure.set_size_inches(30, 15)
plt.savefig(
    results_path + 'validation_results_summer_1_{0}.png'.format(currentdate),
    dpi=150,
    bbox_inches='tight')

results_summer_2.plot(kind='line', linewidth=3)
plt.title('specific collector heat output (27.06-03.07.2019)', size=25)
plt.ylabel('collector heat output [W/m2]', size=25)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,
           prop={'size': 25})
plt.yticks(size=25)
figure = plt.gcf()
figure.set_size_inches(30, 15)
plt.savefig(
    results_path + 'validation_results_summer_2_{0}.png'.format(currentdate),
    dpi=150,
    bbox_inches='tight')

results_winter.plot(kind='line', linewidth=3)
plt.title('specific collector heat output (29.01-04.02.2019)', size=25)
plt.ylabel('collector heat output [W/m2]', size=25)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0,
           prop={'size': 25})
plt.yticks(size=25)
figure = plt.gcf()
figure.set_size_inches(30, 15)
plt.savefig(
    results_path + 'validation_results_winter_{0}.png'.format(currentdate),
    dpi=150,
    bbox_inches='tight')
