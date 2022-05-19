from turtle import width
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import curve_fit, minimize, leastsq, Bounds
import pandas as pd


time_points = np.array(["t=0","t=180","t=210","t=240","t=300","t=360"])
data = {'TauONy': [0.12111371, 0.11351539, 0.11132977, 0.09662176, 0.07795376, 0.05007534], 'error':[0.00114606, 0.00121654,5.7388e-04, 5.4577e-04, 9.5683e-04, 3.9227e-04]}
errors = np.array([0.00114606, 0.00121654,5.7388e-04, 5.4577e-04, 9.5683e-04, 3.9227e-04])

TauON = pd.DataFrame(data, index= np.array(["t=0","t=180","t=210","t=240","t=300","t=360"]))

#x_pos = len(TauON['TauONy'])
font1 = {'family':'serif','color':'black','size':14}
#font2 = {'family':'serif','color':'black','size':15}
# Build the plot
fig, ax = plt.subplots()
ax.bar([1,2,3,4,5,6], height = TauON['TauONy'], width= 0.4, yerr=TauON['error'], align='center', alpha=0.5, ecolor='black', edgecolor='black', capsize=10)
ax.set_ylabel(r'$\tau_y^{ON}$')
ax.set_xticks([1,2,3,4,5,6])
ax.set_xticklabels(["t=0 (EL)","t=180 (LL)","t=210 (EE)","t=240 (ME)","t=300 (LE)","t=360 (S)"])
#ax.set_xticklabels(['EL','LL','EE','ME','LE','S'])
#ax.set_xticklabels(TauON.index)
ax.set_title(r'Fitted $\tau_y^{ON}$ values for different induction times',fontdict = font1)
ax.yaxis.grid(True)

# Save the figure and show
#plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()