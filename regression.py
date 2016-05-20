#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata
import matplotlib.mlab as mlab
from scipy.misc import factorial
from scipy.optimize import curve_fit

#import everything from tools.py
from tools import *


#set up figure
fig = figure(figsize=(8, 6), dpi=200)
rc('font', family='serif')
rc('xtick', labelsize='xx-small')
rc('ytick', labelsize='xx-small')

gs = GridSpec(3, 2)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

#set up data
exerc='regression'

runname=exerc+'/CODA'


x = read_da(runname, 1, 1)
y = read_da(runname, 2, 1)

ax1 = subplot(gs[0,0])
ax1.plot(x,y,"k.")

def my_where(xmin, xmax, x, y):
    rx = []
    ry = []
    for i in range(len(x)):
        if (xmin < x[i] < xmax):
            rx.append(x[i])
            ry.append(y[i])
    return rx, ry
rx, ry = my_where(-4, -3, x, y)
#ax1.plot(rx, ry, "r.")

xgrid = linspace(-4, 4, 100)
xfit = []
yfit = []
for i in range(len(xgrid)-1):
    xmin = xgrid[i]
    xmax = xgrid[i+1]
    rx, ry = my_where(xmin, xmax, x, y)
    ymean = np.mean(ry)
    xfit.append(xmin + (xmax-xmin)*0.5)
    yfit.append(ymean)

ax1.plot(xfit, yfit, "r-")


ygrid = linspace(-4, 4, 100)
xfit2 = []
yfit2 = []
for i in range(len(ygrid)-1):
    ymin = ygrid[i]
    ymax = ygrid[i+1]
    #print "ymin:", ymin, " ymax", ymax
    ry, rx = my_where(ymin, ymax, y, x)
    ymean = np.mean(rx)
    xfit2.append(ymin + (ymax-ymin)*0.5)
    yfit2.append(ymean)

#print xfit2, yfit2
ax1.plot(xfit2, yfit2, "g-")

def line(x, a, b):
    return a*x + b

popt, pcov = curve_fit(line, x, y)
afit, bfit = popt
print "afit:", afit, " bfit:", bfit

xline = np.linspace(-4, 4, 100)
yline = line(xline, afit, bfit)
ax1.plot(xline, yline, "b--")
ax1.plot(xline, line(xline, 1.0, 0.0), "y", linestyle="dotted")

ax2 = subplot(gs[1,0])
resid1 = y - line(x, afit, bfit)
#resid2 = y - line(x, afit, bfit)
#resid3 = y - line(x, afit, bfit)
ax2.plot(x, resid1, "b.", alpha=0.5)

ax3 = subplot(gs[1,1])
hist1d(ax3, resid1, 0.68)


ax4 = subplot(gs[2,0])
residxy = y - line(x, 1.0, 0.0)
ax4.plot(x, residxy, "b.", alpha=0.5)

ax5 = subplot(gs[2,1])
hist1d(ax5, residxy, 0.68)


savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')
