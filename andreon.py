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
exerc='andreon'

runname=exerc+'/CODA'


sigmai = read_da(runname, 1, 1)
print "sigmai: ", mean(sigmai)," +-", std(sigmai)
alpha = read_da(runname, 2, 1)
print "alpha: ", mean(alpha)," +-", std(alpha)
beta = read_da(runname, 3, 1)
print "beta: ", mean(beta)," +-", std(beta)

ax11 = subplot(gs[0,0])
ax22 = subplot(gs[1,1])
ax33 = subplot(gs[2,2])

#set limits
#ax11.set_xlim(0,3)
#ax22.set_xlim(0.8,1)
#ax33.set_xlim(0,40)

hist1d(ax11, sigmai, 0.68)
#ax11.plot([0,1],[4.0, 4.0],"b-")

hist1d(ax22, alpha, 0.68)
#ax22.plot([0,1],[80, 80],"b-")

hist1d(ax33, beta, 0.68)
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
        val = alpha + 0.1 + beta*(x[i]-0.03)
        y.append(val)

    return y

sigmaib = mean(sigmai)
alphab = mean(alpha)
betab = mean(beta)

ax0 = subplot(gs[0, 2])
xs = np.linspace(0, 0.06, 100)
ax0.plot(xs, model(xs, sigmaib, alphab, betab), "r-")

#error limits for f
dmins = []
dmaxs = []
for i in range(len(xs)):
    #xmin = xs[i]
    #xmax = xs[i+1]
    dist = []
    for j in range(len(sigmai)):
        val = alpha[j] + 0.1 + beta[j]*(xs[i]-0.03)
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
obsz = [ 0.10252,0.104427,0.0948906,0.0998974,0.0965595,0.0946522,0.0948906,0.0903606,0.102758,0.0970364,0.102282,0.0958443,0.0948906,0.0891685,0.087738,0.100136,0.100613,0.104904,0.0891685,0.0896454,0.0958443,0.0884533,0.0960827,0.0908375,0.108957,0.0994205,0.0967979,0.104666,0.0994205,0.102758,0.104427,0.0886917,0.101328,0.0936985,0.0910759,0.0958443]
prec = [1.47519e+06,1.08683e+07,361444,2.74717e+06,961169,5.49316e+06,9.18274e+06,4.05387e+06,9.56531e+06,7.43802e+06,3.79491e+06,986799,530210,3.08642e+07,9.3711e+06,3.22708e+06,1.24567e+07,1.38408e+06,4.07424e+07,626562,3.18878e+06,1.49938e+06,4.65814e+06,7.78547e+07,1.89378e+06,7.3046e+06,3.9472e+06,5.66893e+06,2.02152e+06,1.78536e+07,9.56531e+06,2.29568e+06,1.18147e+06,889997,9e+06,1.12375e+06]
xx = [0.0462,0.0215,0.021,0.0482,0.0477,0.014,0.0127,0.0368,0.0109,0.0406,0.04,0.0356,0.0352,0.0037,0.0375,0.0369,0.0341,0.0285,-0.0052,0.0246,0.0221,0.0203,0.0215,0.02,0.0176,0.0165,0.0156,0.0126,0.0105,0.011,0.01,0.0072,0.0049,-0.0011,-0.0014,-0.0026]

err = 1.0/sqrt(prec)

ax0.errorbar(xx, obsz, yerr=err, fmt='.')
#ax0.plot(xx, obsz, "k.")

zmean = mean(obsz)
zmean1 = model([0.0], sigmaib, alphab, betab)[0]
zmean2 = model([0.05], sigmaib, alphab, betab)[0]
print zmean1, zmean2

zstd = std(obsz)
ax0.plot([-0.0, 0.05], [zmean1-zstd, zmean2-zstd], "r--")
ax0.plot([-0.0, 0.05], [zmean1+zstd, zmean2+zstd], "r--")
ax0.set_xlim(min(xx)*0.95, max(xx)*1.05)



savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')
