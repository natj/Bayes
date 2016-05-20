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

gs = GridSpec(4, 4)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

#set up data
exerc='planck'

runname=exerc+'/CODA'


sigmai = read_da(runname, 1, 1)
print "sigmai: ", mean(sigmai)," +-", std(sigmai)
alpha = read_da(runname, 2, 1)
print "a: ", mean(alpha)," +-", std(alpha)
beta = read_da(runname, 3, 1)
print "b: ", mean(beta)," +-", std(beta)
gamma = read_da(runname, 4, 1)
print "gamma: ", mean(gamma)," +-", std(gamma)

ax11 = subplot(gs[0,0])
ax22 = subplot(gs[1,1])
ax33 = subplot(gs[2,2])
ax44 = subplot(gs[3,3])


hist1d(ax11, sigmai, 0.68, xlabel="sigmai")

hist1d(ax22, alpha, 0.68, xlabel="alpha")

hist1d(ax33, beta, 0.68, "beta")

hist1d(ax44, gamma, 0.68, "gamma")

###
ax21 = subplot(gs[1,0])
ax22 = subplot(gs[2,0])
ax33 = subplot(gs[2,1])

ax41 = subplot(gs[3,0])
ax42 = subplot(gs[3,1])
ax43 = subplot(gs[3,2])

hist2d(ax21, sigmai, alpha, [0.95, 0.68], xlabel="sigmai", ylabel="alpha")
hist2d(ax22, sigmai, beta, [0.95, 0.68], xlabel="sigmai", ylabel="beta")
hist2d(ax33, alpha, beta, [0.95, 0.68], xlabel="alpha", ylabel="beta")

hist2d(ax41, gamma, sigmai, [0.95, 0.68], xlabel="gamma", ylabel="sigmai")
hist2d(ax42, gamma, alpha, [0.95, 0.68], xlabel="gamma", ylabel="alpha")
hist2d(ax43, gamma, beta, [0.95, 0.68], xlabel="gamma", ylabel="beta")

savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')

def phi(xx):
    return (1.0 + math.erf(xx / sqrt(2.0))) / 2.0

def model(x, x2, sigmai, alpha, beta, gamma):
    y = []
    for i in range(len(x)):
        val = alpha-4.0 + beta*(x[i]-15.0) + gamma*log(x2[i])
        y.append(val)

    return y


sigmaib = mean(sigmai)
alphab = mean(alpha)
betab = mean(beta)
gammab = mean(gamma)

ax0 = subplot(gs[0, 2])
xs = np.linspace(14.0, 16.0, 100)
xs2 = np.linspace(1.0, 1.5, 100)

ax0.plot(xs, model(xs, xs2,  sigmaib, alphab, betab, gammab), "r-")

#error limits for f
dmins = []
dmaxs = []
for i in range(len(xs)):
    #xmin = xs[i]
    #xmax = xs[i+1]
    dist = []
    for j in range(len(sigmai)):
        val = model([xs[i]], [xs2[i]], sigmai[j], alpha[j], beta[j], gamma[j])[0]
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
Ez = [1.17,1.076,1.083,1.055,1.118,1.268,1.087,1.123,1.12,1.087,1.161,1.167,1.093,1.114,1.107,1.163,1.106,1.071,1.147,1.155,1.077,1.155,1.163,1.164,1.171,1.149,1.041,1.041,1.094,1.045,1.047,1.047,1.198,1.121,1.039,1.069,1.07,1.074,1.075,1.076,1.083,1.264,1.034,1.029,1.037,1.037,1.026,1.022,1.027,1.036,1.028,1.022,1.025,1.028,1.022,1.026,1.026,1.021,1.107,1.132,1.136,1.152,1.166,1.17,1.262,1.227,1.227,1.172,1.213,1.11,1.199]
errlogM = [0.01,0.012,0.009,0.011,0.034,0.006,0.01,0.011,0.01,0.008,0.013,0.029,0.022,0.009,0.008,0.007,0.011,0.004,0.015,0.02,0.012,0.012,0.039,0.009,0.015,0.018,0.005,0.01,0.006,0.007,0.007,0.009,0.009,0.009,0.013,0.01,0.012,0.008,0.007,0.008,0.01,0.012,0.025,0.026,0.036,0.027,0.025,0.023,0.028,0.019,0.023,0.022,0.03,0.029,0.011,0.02,0.025,0.024,0.008,0.007,0.004,0.01,0.021,0.023,0.021,0.023,0.013,0.016,0.011,0.017,0.021]
errlogYSZ = [0.035,0.03,0.042,0.043,0.038,0.037,0.034,0.027,0.03,0.025,0.04,0.052,0.032,0.045,0.05,0.065,0.051,0.04,0.046,0.047,0.057,0.051,0.025,0.02,0.04,0.035,0.046,0.037,0.03,0.04,0.026,0.037,0.026,0.019,0.019,0.046,0.061,0.046,0.054,0.03,0.024,0.044,0.037,0.027,0.022,0.031,0.027,0.035,0.013,0.043,0.025,0.037,0.015,0.012,0.052,0.051,0.049,0.035,0.036,0.067,0.039,0.054,0.064,0.061,0.041,0.023,0.043,0.059,0.036,0.041,0.054]
obslogM = [14.992,14.907,14.725,14.751,14.801,14.959,14.916,15.028,14.868,14.73,14.772,14.754,14.907,14.82,14.701,14.729,14.919,14.795,14.807,14.836,14.593,14.845,14.892,15.144,14.935,14.877,14.624,14.654,14.913,14.572,14.751,14.601,15.102,15.065,14.699,14.589,14.692,14.7,14.561,14.864,14.868,15.032,14.68,14.775,14.919,14.737,14.724,14.679,14.786,14.565,14.633,14.564,14.939,14.875,14.379,14.432,14.499,14.615,14.858,14.711,14.928,14.853,14.801,14.674,14.864,15.196,14.837,14.73,14.873,14.726,14.669]
obslogYSZ = [-3.775,-3.947,-4.183,-4.299,-3.989,-3.72,-4.035,-3.762,-3.903,-4.131,-3.871,-4.185,-3.936,-4.077,-4.223,-4.197,-4.036,-4.155,-4.029,-4.028,-4.395,-4.075,-3.879,-3.548,-3.818,-4.001,-4.469,-4.324,-3.86,-4.507,-4.172,-4.433,-3.636,-3.658,-4.292,-4.358,-4.48,-4.301,-4.429,-4.045,-3.963,-3.709,-4.41,-4.333,-4.035,-4.32,-4.356,-4.423,-4.144,-4.706,-4.475,-4.588,-4.08,-4.081,-4.989,-4.763,-4.705,-4.576,-3.951,-4.208,-3.862,-4.053,-4.255,-4.243,-3.888,-3.441,-4.019,-4.073,-3.983,-4.241,-4.158]

obsy = gammab*log(Ez)+obslogYSZ
obsx = obslogM
ax0.errorbar(obsx, obsy, xerr=errlogM, yerr=errlogYSZ, fmt='.')
ax0.set_xlim(14.35, 15.3)
ax0.set_ylim(-5, -3.2)

ax0b = subplot(gs[1, 3])
obsx2 = Ez
obsy2 = obsy

zmean = mean(obsy)
xmin = min(obsx)
xmax = max(obsx)
xmin2 = min(Ez)
xmax2 = max(Ez)
zmean1 = model([xmin], [xmin2], sigmaib, alphab, betab, gammab)[0]
zmean2 = model([xmax], [xmax2], sigmaib, alphab, betab, gammab)[0]
print zmean1, zmean2

#zstd = std(obsy)
zstd = sigmaib
ax0.plot([xmin, xmax], [zmean1-zstd, zmean2-zstd], "r--")
ax0.plot([xmin, xmax], [zmean1+zstd, zmean2+zstd], "r--")
#ax0.set_xlim(min(obsx)*0.95, max(obsx)*1.05)



savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')
