#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata
import matplotlib.mlab as mlab
from scipy.misc import factorial


#import everything from tools.py
from tools import *


#set up figure
fig = figure(figsize=(8, 6), dpi=200)
rc('font', family='serif')
rc('xtick', labelsize='xx-small')
rc('ytick', labelsize='xx-small')

gs = GridSpec(4, 2)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

#set up data
exerc='scatter'

runname=exerc+'/CODA'


var1 = read_da(runname, 1, 1)
var2 = read_da(runname, 1, 2)
var3 = read_da(runname, 1, 3)

var1b = read_da(runname, 2, 1)
var2b = read_da(runname, 2, 2)
var3b = read_da(runname, 2, 3)


#print some statistics of var1
print "mean:", mean(var1)
print " std:", std(var1)


#basic trace plot
ax1 = subplot(gs[0,0])
ax1.minorticks_on()
ax1.set_xlim(-1, 500)
#ax1.set_ylim(-5, 10)
ax1.set_ylabel('vcent')

ax1.plot(var1, "k-")
ax1.plot([0,500], [mean(var1), mean(var1)], "b--")
ax1.plot([0,500], [mean(var1)-std(var1), mean(var1)-std(var1)], "b", linestyle="dotted")
ax1.plot([0,500], [mean(var1)+std(var1), mean(var1)+std(var1)], "b", linestyle="dotted")

#histogram
ax2 = subplot(gs[0,1])
hist1d(ax2, var1, 0.95, xlabel='m')
hist1d(ax2, var2, 0.95, xlabel='m')
hist1d(ax2, var3, 0.95, xlabel='m')

# analytical

# poisson function, parameter lamb is the fit parameter
#def poisson(k, lamb):
#    return (lamb**k/factorial(k)) * np.exp(-lamb)
#
x = np.linspace(9000,12000,100)
y1 = mlab.normpdf(x, np.mean(var1), np.std(var1))
ax2.plot(x, y1, "r-")


##prior
y2 = np.ones(100)*0.001
#y2[0:50] = 0.0
ax2.plot(x, y2, "-", color="blue")
#
##P(data | model)*P(model)
#y3 = y1 * y2
#y3 = y3 / sum(y3[1:]*np.diff(x))
#ax2.plot(x, y3, "g--", linewidth=2.5)

#basic trace plot
print "sigmac"
print "mean:", mean(var1b)
print " std:", std(var1b)


ax3 = subplot(gs[1,0])
ax3.minorticks_on()
ax3.set_xlim(-1, 500)
ax3.set_ylabel('sigmac')

ax3.plot(var1b, "k-")
ax3.plot([0,500], [mean(var1b), mean(var1b)], "b--")
ax3.plot([0,500], [mean(var1b)-std(var1b), mean(var1b)-std(var1b)], "b", linestyle="dotted")
ax3.plot([0,500], [mean(var1b)+std(var1b), mean(var1b)+std(var1b)], "b", linestyle="dotted")


#histogram
ax4 = subplot(gs[1,1])
hist1d(ax4, var1b, 0.95, xlabel='m')
hist1d(ax4, var2b, 0.95, xlabel='m')
hist1d(ax4, var3b, 0.95, xlabel='m')

##prior
x = np.linspace(500,3000,100)
y2 = np.ones(100)*0.001
#y2[0:50] = 0.0
ax4.plot(x, y2, "-", color="blue")

y1 = mlab.normpdf(x, np.mean(var1b), np.std(var1b))
ax4.plot(x, y1, "r-")

ax5 = subplot(gs[2,0])
autocorr(ax5, var1)
autocorr(ax5, var2)
autocorr(ax5, var3)
#ax6 = subplot(gs[2,1])
#autocorr(ax6, var1b)
#autocorr(ax6, var2b)
#autocorr(ax6, var3b)

ax7 = subplot(gs[3,0])
hist2d(ax7, var1, var1b, [0.95, 0.68], xlabel="vcent", ylabel="sigmav")

#
#ax8 = subplot(gs[3,1])
#hist2d(ax8, var1, var1c, [0.95, 0.68], xlabel="s", ylabel="bkg2")

savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')

