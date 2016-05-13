#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata

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
runname='CODA'

var1 = read_da(runname, 1)
var2 = read_da(runname, 2)

#print some statistics of var1
print "mean:", mean(var1)
print " std:", std(var1)


#basic trace plot
ax1 = subplot(gs[0,0])
ax1.minorticks_on()
ax1.set_xlim(-1, 500)
ax1.set_ylim(-20, 100)
ax1.set_ylabel('var1')

ax1.plot(var1, "k-")
ax1.plot([0,500], [mean(var1), mean(var1)], "b--")
ax1.plot([0,500], [mean(var1)-std(var1), mean(var1)-std(var1)], "b", linestyle="dotted")
ax1.plot([0,500], [mean(var1)+std(var1), mean(var1)+std(var1)], "b", linestyle="dotted")


#histogram
ax2 = subplot(gs[0,1])
ax3 = subplot(gs[1,0])
hist1d(ax2, var1, 0.95, xlabel='var1')

#var 2 with both 1s and 2s lims
hist1d(ax3, var2, 0.68, xlabel='var2')
hist1d(ax3, var2, 0.95, xlabel='var2')


#2d histograms
ax4 = subplot(gs[1,1])
hist2d(ax4, var1, var2, [0.95, 0.68], binsize=80, smooth=1.5,
        xlabel='var1', ylabel='var2')



savefig('fig.pdf', bbox_inches='tight')
#savefig('fig.png', bbox_inches='tight')

