# %% Importing modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters, Parameter, report_fit
from scipy.integrate import odeint
from SALib.sample import latin
from pathlib import Path

# %% Define ODE function (f), Solution to ODE function (g), and residual function to be minimized (residual)
def f(y, t, paras):
    """
    Your system of differential equations
    """
    x1 = y[0]
    x2 = y[1]
    try:
        TauONx = paras['TauONx'].value
        x_SS = paras['x_SS'].value
        TauONy = paras['TauONy'].value
        TauOFFy = paras['TauOFFy'].value

    except KeyError:
        TauONx, x_SS, TauONy, TauOFFy = paras
    # the model equations
    f0 = TauONx*(x_SS - x1)
    f1 = TauONy * x1 - TauOFFy * x2
    return [f0, f1]

def g(t, x0, paras):
    """
    Solution to the ODE x'(t) = f(t,x,k) with initial condition x(0) = x0
    """
    x = odeint(f, x0, t, args=(paras,))
    return x

def residual(paras, t, data):
    """
    compute the residual between actual data and fitted data
    """
    x0 = paras['x10'].value, paras['x20'].value
    model = g(t, x0, paras)

    # you only have data for one of your variables
    x2_model = model[:, 1]
    return (x2_model - data).ravel()

# %% Importing measured (or training) data
p = Path('.')

## Here, choose uncomment option 1 for LuxR-characterized parameterization or 2 for AraC-characterized parameterization
#### OPTION 1 LuxR gate characterization####
df = pd.read_excel (p.absolute() / 'experimental_results' / 'Timer (Modified)_20210808_125346 ON LuxR 2 plasmids - Cropped.xlsx')
gate_name = 'LuxR'

#### OPTION 2 AraC gate characterization ####
#df = pd.read_excel (p.absolute() / 'experimental_results' / 'shai timer_20210811_123450_ON AraC 2 plasmids - Cropped.xlsx')
#gate_name = 'AraC'      

#### inducer concentration column
inputs = df.Time
inputs = inputs.tolist()
inputs = np.asarray(inputs)
inputs = np.array(range(1,len(inputs)+1))
names = []
outputs = []
for column in df.columns[2:]:
    names.append(column.split())
    outputs.append(list(df[column]))

fitted_results = pd.DataFrame(index=['TauONx','TauONy','TauOFFy','x_ss'])

for k in range(len(outputs)):

    print(names[k])
    y_measured = outputs[k]
    inputs = np.array(range(1,len(y_measured)+1))

    # initial conditions
    x10 = 54.
    x20 = 54.
    y0 = [x10, x20]

    x2_measured = np.array(y_measured)
    x2_measured = x2_measured[~np.isnan(x2_measured)]
    t_measured = np.array(range(1,len(x2_measured)+1))

    plt.figure()
    plt.scatter(t_measured, x2_measured, marker='o', color='b', label='measured data', s=75)

    # %% Set parameters including bounds; you can also fix parameters (use vary=False)
    problem = {
    'num_vars':2,
    'names': ['x10','x20'],
    'bounds':[[0.0, 100.], [0.0, 100.]],
    'groups':['group1','group2']
    }
    n_search = 25
    param_values = latin.sample(problem, n_search, seed=456767)

    df_params = pd.DataFrame()

    for i in range(len(problem["names"])):
        df_params[problem["names"][i]] = param_values[:,i]

    reduced_chi = np.inf

    for j in range(n_search):
        # set parameters incluing bounds
        params = Parameters()
        params.add('x10', value=df_params["x10"][j], min=0.0001, max=2000.)
        params.add('x20', value=df_params["x20"][j], min=0.0001, max=2000.)
        params.add('TauONx', value=0.100830362, vary=False)
        params.add('x_SS', value=1000, vary=False)
        params.add('TauONy', value=0.100830362, min=0.0001, max=2000.)
        params.add('TauOFFy', value=0.0929173, vary=False)

    # %% fit model
        result = minimize(residual, params, args=(t_measured, x2_measured), method='leastsq')  # leastsq nelder
        new_chi = result.redchi
        if new_chi < reduced_chi:
            reduced_chi = new_chi
            final_result = result
            x10 = df_params["x10"][j]
            x20 = df_params["x20"][j]
            y0 = [x10, x20]

    result = final_result
    #  check results of the fit
    data_fitted = g(t_measured, y0, result.params)

    # plot fitted data
    plt.plot(t_measured, data_fitted[:, 1], '-', linewidth=2, color='red', label='fitted data')
    plt.legend()
    plt.xlim([0, max(t_measured)])
    plt.ylim([0, 1.1 * max(data_fitted[:, 1])])
    # display fitted statistics
    report_fit(result)
    print('N# free variables = ' + str(result.nfree))

    fitted_results[names[k][0]] = [result.params['TauONx'].value, result.params['TauONy'].value, result.params['TauOFFy'].value, result.params['x_SS'].value]

    plt.show()

print(fitted_results)
#fitted_results.to_excel('p.absolute() / ' + gate_name + 'freeFitParameterValues.xlsx')