# -*- coding: utf-8 -*-
import pandas as pd
import warnings


def get_cop(temperature, heatpump_type="Air", water_temp=60):
    """ Calculation of the coefficient of performance depending
    on the outside temperature

    Parameters
    ----------
    temperature: time series
        containing the outside temperature
    heatpump_type: string
        defines the technology used. Ground is more efficient than Air.
    water_temp: int
        temperature needed for the heating system

    References
    ----------
    ..  [1]: 'https://www.researchgate.net/publication/
            255759857_A_review_of_domestic_heat_pumps'
        Research paper about domestic heatpumps, containing the formulas used
    """

    cop_lst = []

    if heatpump_type == "Air":
        for tmp in temperature:
            if (water_temp - tmp) < 15 or (water_temp - tmp) > 60:
                msg = "'{0}'°C exceeds the limit of the formula used:\
                15 <= (water_temp - tmp) <= 60"
                warnings.warn(msg.format((water_temp - tmp)))

            cop = (6.81 - 0.121 * (water_temp - tmp)
                   + 0.00063 * (water_temp - tmp)**2)
            cop_lst.append(cop)

    elif heatpump_type == "Ground":
        for tmp in temperature:
            if (water_temp - tmp) < 20 or (water_temp - tmp) > 60:
                msg = "'{0}'°C exceeds the limit of the formula used:\
                20 <= (water_temp - tmp) <= 60"
                warnings.warn(msg.format((water_temp - tmp)))

            cop = (8.77 - 0.15 * (water_temp - tmp)
                   + 0.000734 * (water_temp - tmp)**2)
            cop_lst.append(cop)

    else:
        msg = "'{0}' is not a valid heatpump type. Use 'Air' or 'Ground'."
        raise ValueError(msg.format(heatpump_type))

    cop = pd.DataFrame({"cop": cop_lst}, index=temperature.index)

    return cop
