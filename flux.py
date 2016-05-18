#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata
import matplotlib.mlab as mlab


#import everything from tools.py
from tools import *


#set up figure
fig = figure(figsize=(8, 6), dpi=200)
rc('font', family='serif')
rc('xtick', labelsize='xx-small')
rc('ytick', labelsize='xx-small')

gs = GridSpec(2, 2)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

#set up data
runname='flux/CODA'

var1 = read_da(runname, 1, 1)
var2 = read_da(runname, 1, 2)
var3 = read_da(runname, 1, 3)

#print some statistics of var1
print "mean:", mean(var1)
print " std:", std(var1)


#basic trace plot
ax1 = subplot(gs[0,0])
ax1.minorticks_on()
ax1.set_xlim(-1, 500)
#ax1.set_ylim(-5, 10)
ax1.set_ylabel('var1')

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
x = np.linspace(0,20,100)
#y1 = mlab.normpdf(x, -4.0, 2.0)
#ax2.plot(x, y1, "r-")
#
#
##prior
y2 = np.ones(100)
#y2[0:50] = 0.0
ax2.plot(x, y2, "-", color="blue")
#
##P(data | model)*P(model)
#y3 = y1 * y2
#y3 = y3 / sum(y3[1:]*np.diff(x))
#ax2.plot(x, y3, "g--", linewidth=2.5)


#test priors for limits 0-2 and 0-100

ax3 = subplot(gs[1,0])
autocorr(ax3, var1)




savefig('flux/fig.pdf', bbox_inches='tight')
savefig('flux/fig.png', bbox_inches='tight')
#savefig('fig.png', bbox_inches='tight')

