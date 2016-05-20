#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata
import matplotlib.mlab as mlab
from scipy.misc import factorial
from scipy.optimize import curve_fit
from scipy.stats import norm

#import everything from tools.py
from tools import *


#set up figure
fig = figure(figsize=(8, 8), dpi=200)
rc('font', family='serif')
rc('xtick', labelsize='xx-small')
rc('ytick', labelsize='xx-small')

gs = GridSpec(3, 3)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

#set up data
exerc='derrors'

runname=exerc+'/CODA'


sigmai = read_da(runname, 1, 1)
print "sigmai: ", mean(sigmai)," +-", std(sigmai)
alpha = read_da(runname, 2, 1)
print "a: ", mean(alpha)," +-", std(alpha)
beta = read_da(runname, 3, 1)
print "b: ", mean(beta)," +-", std(beta)

ax11 = subplot(gs[0,0])
ax22 = subplot(gs[1,1])
ax33 = subplot(gs[2,2])


hist1d(ax11, sigmai, 0.68, xlabel="sigmai")
#ax11.plot([0,1],[4.0, 4.0],"b-")

hist1d(ax22, alpha, 0.68, xlabel="alpha")
#ax22.plot([0,1],[80, 80],"b-")

hist1d(ax33, beta, 0.68, "beta")
#ax33.plot([0,100],[0.1, 0.1], "b-")

###
ax21 = subplot(gs[1,0])
ax22 = subplot(gs[2,0])
ax33 = subplot(gs[2,1])

hist2d(ax21, sigmai, alpha, [0.95, 0.68], xlabel="sigmai", ylabel="alpha")
hist2d(ax22, sigmai, beta, [0.95, 0.68], xlabel="sigmai", ylabel="beta")
hist2d(ax33, alpha, beta, [0.95, 0.68], xlabel="alpha", ylabel="beta")


def phi(xx):
    return (1.0 + math.erf(xx / sqrt(2.0))) / 2.0
    


def model(x, sigmai, alpha, beta):
    y = []
    for i in range(len(x)):
        val = beta + alpha*(x[i]-2.3)
        y.append(val)

    return y


sigmaib = mean(sigmai)
alphab = mean(alpha)
betab = mean(beta)

ax0 = subplot(gs[0, 2])
xs = np.linspace(1.8, 2.6, 100)
ax0.plot(xs, model(xs, sigmaib, alphab, betab), "r-")

#error limits for f
dmins = []
dmaxs = []
for i in range(len(xs)):
    #xmin = xs[i]
    #xmax = xs[i+1]
    dist = []
    for j in range(len(sigmai)):
        val = model([xs[i]], sigmai[j], alpha[j], beta[j])[0]
        dist.append(val)

    dmean = mean(dist)
    dsig = std(dist)
    dmin = dmean - dsig
    dmax = dmean + dsig
    
    dmins.append(dmin)
    dmaxs.append(dmax)
     
#ax0.plot(xs, dmins, "b-")
#ax0.plot(xs, dmaxs, "b-")
ax0.fill_between(xs, dmins, dmaxs, color="darkorange", alpha=0.7)

#plot data
obsx = [2.01284,1.87506,2.20412,2.32015,2.31175,2.17898,2.24304,2.14613,2.36173,2.31175,2.16137,2.31387,2.15534,2.26007,2.11394,2.49831,2.38382,2.35218,2.26951,2.27875,2.57403,2.20952,2.18184,2.58546,2.24797,1.95424,2.36922,2.4624,2.42488,1.82607,2.53148]
obsy = [6.26717,6.39794,7.72016,7.65321,7.64345,7.30103,7.13033,7.60746,9.07918,8.32222,8.14613,8.02119,7.19033,8.32222,7.59106,8.71181,8.37107,8.52504,7.8451,7.95665,9.47712,7.72835,7.91645,9.27875,8.24304,7.13033,8.27875,8.72016,8.57978,6.52504,9.40654]
errx = [0.0791813,0.0211868,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211945,0.0211792,0.0211945,0.0211945,0.0211945,0.0211945,0.0211792,0.0211945,0.0211945,0.0211792,0.0211945,0.0211868,0.0211945,0.0211792,0.0211792,0.0211868,0.0211792]
erry = [0.0831657,0.0880456,0.314194,0.161466,0.0495657,0.238561,0.321726,0.048455,0.349485,0.105427,0.162256,0.252575,0.0421605,0.174227,0.0111382,0.0898039,0.343987,0.185534,0.0816016,0.342365,0.150515,0.0448054,0.212984,0.117042,0.0373168,0.150515,0.223579,0.150515,0.223579,0.170269,0.077451]



ax0.errorbar(obsx, obsy, xerr=errx, yerr=erry, fmt='.')
#ax0.plot(xx, obsz, "k.")

zmean = mean(obsy)
xmin = min(obsx)
xmax = max(obsx)
zmean1 = model([xmin], sigmaib, alphab, betab)[0]
zmean2 = model([xmax], sigmaib, alphab, betab)[0]
print zmean1, zmean2

#zstd = std(obsy)
zstd = sigmaib
ax0.plot([xmin, xmax], [zmean1-zstd, zmean2-zstd], "r--")
ax0.plot([xmin, xmax], [zmean1+zstd, zmean2+zstd], "r--")
ax0.set_xlim(min(obsx)*0.95, max(obsx)*1.05)



savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')
