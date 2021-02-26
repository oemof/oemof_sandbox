# -*- coding: utf-8 -*-
"""
author: pyosch
"""
import pandas as pd
import numpy as np
import oemof.thermal.heat_pump as heat_pump


# generate test data
temperature = pd.DataFrame(np.random.randint(-10, 20, size=(96, 1)),
                           columns=["temperature"],
                           index=pd.date_range(start='2017', periods=96,
                                               freq='15 min', name='index'))

print(temperature.head())

# cop calculation for heat pumps
cop = heat_pump.get_cop(temperature.temperature)

print(cop.head())
