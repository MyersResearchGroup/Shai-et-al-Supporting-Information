# %% Importing modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from lmfit import minimize, Parameters, Parameter, report_fit
from scipy.integrate import odeint
#from SALib.sample import latin

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
df = pd.read_excel (r'C:\Users\elros\Dropbox\SYNTHETIC BIOLOGY\SD2 Project\Parameterizing Gates\Delay Circuit\TestingONOFF.xlsx')        
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

j = 0

print(names[j])
y_measured = outputs[j]
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
params = Parameters()

# params.add('x10', value=x10, vary=False)
# params.add('x20', value=x20, vary=False)
# params.add('TauONx', value=0.2, min=0.0001, max=2000.)
# params.add('x_SS', value=1000, min=0.0001, max=10000.)
# params.add('TauONy', value=0.3, min=0.0001, max=2000.)
# params.add('TauOFFy', value=0.3, min=0.0001, max=2000.)

# [ ] finish this
# TODO: Use this line of code to randomly generate initial estimates
#param_values = latin.sample(problem, n_search, seed=456767)

params.add('x10', value=x10, min=0.0001, max=2000.)
params.add('x20', value=x20,  min=0.0001, max=2000.)
params.add('TauONx', value=0.2, min=0.0001, max=2000.)
params.add('x_SS', value=0, min=0.0001, max=2000)
params.add('TauONy', value=0.3, min=0.0001, max=2000.)
params.add('TauOFFy', value=0.153232023, min=0.0001, max=2000.)

# %% fit model
result = minimize(residual, params, args=(t_measured, x2_measured), method='leastsq')  # leastsq nelder
#  check results of the fit
data_fitted = g(t_measured, y0, result.params)
#data_fitted = g(np.linspace(0., 9., 100), y0, result.params)
# plot fitted data
plt.plot(t_measured, data_fitted[:, 0], '-', linewidth=2, color='green', label='x fitted data')
plt.plot(t_measured, data_fitted[:, 1], '-', linewidth=2, color='red', label='y fitted data')
#plt.plot(np.linspace(0., 9., 100), data_fitted[:, 1], '-', linewidth=2, color='red', label='fitted data')
plt.legend()
plt.xlim([0, max(t_measured)])
plt.ylim([0, 1.1 * max(data_fitted[:, 1])])
# display fitted statistics
report_fit(result)

plt.show()
# %%

# %%
