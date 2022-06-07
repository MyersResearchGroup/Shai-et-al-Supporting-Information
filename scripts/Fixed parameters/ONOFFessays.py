#!/usr/bin/env python

import numpy as np
from numpy.core.fromnumeric import mean
from numpy.core.records import array
from scipy.optimize import curve_fit, minimize, leastsq, Bounds
from scipy.optimize import Bounds
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

### Fitting function used ONLY for ON to OFF experiments, to obtain TauOFF_YFP from gradient (equation S19)
def line_curve(t, m, c):
    return m*t+c

# %% Importing measured (or training) data
p = Path('.')

## Here, choose uncomment option 1 for LuxR-characterized parameterization or 2 for AraC-characterized parameterization
#### OPTION 1 LuxR gate characterization####
#df = pd.read_excel (p.absolute() / 'experimental_results' / 'Timer (Modified)_20210809_090959 OFF LuxR 2 plasmids - Cropped.xlsx')
#gate_name = 'LuxR'

#### OPTION 2 AraC gate characterization ####
df = pd.read_excel (p.absolute() / 'experimental_results' / 'shai timer_20210812_090202 OFF AraC 2 plasmidsd - Cropped.xlsx')
gate_name = 'AraC'  
#df = pd.read_excel (r'C:\Users\elros\Dropbox\SYNTHETIC BIOLOGY\SD2 Project\Parameterizing Gates\Delay Circuit\TestingONOFF.xlsx')
    
#### inducer concentration column
inputs = df.Time
inputs = inputs.tolist()
inputs = np.asarray(inputs)
inputs = np.array(range(1,len(inputs)+1))

#### gate columns
names = []
outputs = []

NoInducerConc = list(df['No inducer'])
x_ss = mean(NoInducerConc)

for column in df.columns[2:]:
    names.append(column.split())
    outputs.append(list(df[column]))
    

###############
# This section was used to test the optimizer using a random generated set of points
# y = booby_func(inputs, 2.5, 1.3, 0.5)
# rng = np.random
# y_noise = 0.2 * rng.normal(size=inputs.size)
# ydata = y + y_noise
# plt.plot(inputs, ydata, 'b-', label='data')
###############

colors_array = list(matplotlib.colors.cnames.keys())
markers_array = list(matplotlib.markers.MarkerStyle.markers.keys())

# # If we want to plot experimental results as a log graph to obtain the gradient of the curve then:
# converter_list = []
# for j in range(len(outputs)):
#     temp_list = outputs[j]
#     for x in range(len(temp_list)):
#         temp_list[x] = -np.log(temp_list[x]-x_ss)
#     converter_list.append(temp_list)    


for i in range(len(outputs)):
    plt.plot(inputs, outputs[i], 'b' + markers_array[i+2], label=names[i])
    popt, pcov = curve_fit(line_curve, inputs, outputs[i], method='trf', maxfev=15000)
    #print(popt)
    plt.plot(inputs, line_curve(inputs, *popt), 'r-')
    curvegradient = np.gradient(outputs[i])
    Tau_OFF = curvegradient
    #Tau_OFF = curvegradient/outputs[1]
    mean_Tau_OFF = np.mean(Tau_OFF)
    SD_Tau_OFF = np.std(Tau_OFF)

    #mean_gradient = np.mean(curvegradient)


    print(names[i])
    print(mean_Tau_OFF)
    print(SD_Tau_OFF)
    print('--------------')
    #print(curvegradient)

plt.legend(loc='best')
plt.show()
