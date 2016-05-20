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
exerc='errors'

runname=exerc+'/CODA'


A = read_da(runname, 1, 1)
print "A: ", mean(A)," +-", std(A)
B = read_da(runname, 2, 1)
print "B: ", mean(B)," +-", std(B)
mu = read_da(runname, 3, 1)
print "mu: ", mean(mu)," +-", std(mu)
sigma = read_da(runname, 4, 1)
print "sigma: ", mean(sigma)," +-", std(sigma)

ax11 = subplot(gs[0,0])
ax22 = subplot(gs[1,1])
ax33 = subplot(gs[2,2])
ax44 = subplot(gs[3,3])

#set limits
ax11.set_xlim(0,0.4)
ax22.set_xlim(0.8,1)
ax33.set_xlim(0,40)
ax44.set_xlim(0,30)

#ax1.plot(x,y,"k.")
hist1d(ax11, A, 0.68)
ax11.plot([0,1],[4.0, 4.0],"b-")

hist1d(ax22, B, 0.68)
ax22.plot([0,1],[80, 80],"b-")

hist1d(ax33, mu, 0.68)
ax33.plot([0,100],[0.1, 0.1], "b-")

hist1d(ax44, sigma, 0.68)
ax44.plot([0,100],[0.1, 0.1],"b-")


def erfcc(x):
    """Complementary error function."""
    z = abs(x)
    t = 1. / (1. + 0.5*z)
    r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+
    	t*(.09678418+t*(-.18628806+t*(.27886807+
    	t*(-1.13520398+t*(1.48851587+t*(-.82215223+
    	t*.17087277)))))))))
    if (x >= 0.):
    	return r
    else:
    	return 2. - r

def phi(xx):
    #return mlab.norm.cdf(x)
    #return norm.cdf(x)
    #print (1.0 + math.erf(xx / sqrt(2.0))) / 2.0
    return (1.0 + math.erf(xx / sqrt(2.0))) / 2.0
    #return (1.0 + erfcc(xx / sqrt(2.0))) / 2.0
    

#print A
#print B
#print mu
#print sigma

def model(x, A, B, mu, sigma):
    y = []
    for i in range(len(x)):
        val = A + (B-A)*phi((x[i]-mu)/sigma)
        y.append(val)

    return y

Ab = mean(A)
Bb = mean(B)
mub = mean(mu)
sigmab = mean(sigma)

ax0 = subplot(gs[0:2, 2:4])
xs = np.linspace(2, 98, 100)
ax0.plot(xs, model(xs, Ab, Bb, mub, sigmab), "r-")

#error limits for f
dmins = []
dmaxs = []
for i in range(len(xs)):
    #xmin = xs[i]
    #xmax = xs[i+1]
    dist = []
    for j in range(len(A)):
        val = A[j] + (B[j]-A[j])*phi((xs[i]-mu[j])/sigma[j])
        #val = model(xs[i], A[j], B[j], mu[j], sigma[j])
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

Es = np.array([2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98])
ninj = np.array([96,239,295,327,345,316,349,281,298,235,217,185,140,121,79,81,61,45,41,32,32,31,22,18,11])
nrec = np.array([23,71,115,159,200,221,291,244,277,221,210,182,136,119,79,81,61,44,41,32,32,31,22,18,11])

nrecninj = []
for i in range(len(ninj)):
    nrecninj.append(float(nrec[i])/float(ninj[i]))

ax0.plot(Es, nrecninj, "k.")


savefig(exerc+'/fig.pdf', bbox_inches='tight')
savefig(exerc+'/fig.png', bbox_inches='tight')
