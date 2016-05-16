#plotting tool for CODA stuff

import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata


fig = figure(figsize=(6, 4), dpi=200)
rc('font', family='serif')
rc('xtick', labelsize='xx-small')
rc('ytick', labelsize='xx-small')


gs = GridSpec(2, 2)
#gs.update(hspace = 0.3)
#gs.update(wspace = 0.3)

runname='CODA'
fdir=''

def read_da(runname, vari):
    vari = vari-1 #scale to [0,inf[ from human format [1,inf[

    fname = runname+'index.txt'
    da_index = np.genfromtxt(fname, delimiter="  ", comments='#')

    #print "reading var: ", da_index[vari,0]
    i1 = da_index[vari, 1]-1
    i2 = da_index[vari, 2] 
    #print "   from ", i1, ":", i2

    fname = runname+'chain1.txt'
    da = np.genfromtxt(fname, delimiter="  ", comments='#')
    chain = np.array(da[i1:i2, 1])
    #print chain[0], " ", chain[-1]
    return chain


def limit_iter(hist, level):
    acc = 0.001
    diff = 1.0
    iter=0
    sum0 = sum(hist)

    left=0.0
    right=1.0
    midpoint=0.5

    while np.abs(diff) > acc and iter < 50:
        midpoint = (right + left) / 2.0
        upmid = 0.0
        for i in range(len(hist)):
            if hist[i] > midpoint:
                upmid += hist[i]
        ratio = upmid/sum0

        diff = ratio - level
        if diff < 0.0: 
            right = midpoint
        else:
            left = midpoint

        iter += 1
            
    return midpoint


def conf_lims(hist, bin_edges, level):

    bins = bin_edges[0:-1] + np.diff(bin_edges)
    hlim = limit_iter(hist, level)

    i1 = 0
    xlo = bin_edges[i1]
    for j in range(len(bin_edges)):
        if hist[j] >= hlim:
            i1 = j
            xlo = bin_edges[i1]
            break

    i2 = len(bin_edges)-1
    xhi = bin_edges[i2]
    for j in reversed(range(len(bin_edges))):
        if hist[j-1] >= hlim:
            print "j:",j
            i2 = j
            xhi = bin_edges[i2]
            break
            
    return xlo, xhi, i1, i2, hlim


var1 = read_da(runname, 1)

print "mean:", mean(var1)
print " std:", std(var1)

ax1 = subplot(gs[0,0])
ax1.minorticks_on()
ax1.plot(chain, "k-")



###################################################
ax2 = subplot(gs[0,1])
ax2.minorticks_on()

#compute histogram
hist, bin_edges = np.histogram(var1, bins=50, normed=True)
bins = bin_edges[0:-1] + np.diff(bin_edges)

#compute limits
xlo1, xhi1, i1, i2, hlim = conf_lims(hist, bin_edges, 0.95)
print "xlo:", xlo1, " ",i1, " xhi:", xhi1, " ", i2, " level:",hlim

ax2.plot(bins, hist, "k-")
fill_between(bins[i1:i2], hist[i1:i2], np.zeros(i2-i1), color='darkorange', alpha=0.8)


#hist2d

ax3 = subplot(gs[1,0])
var1 = read_da(runname, 1)
var2 = read_da(runname, 2)



hdata, xedges, yedges = np.histogram2d(var1, var2, bins=50)

xr0 = xedges[0]
xr1 = xedges[-1]
yr0 = yedges[0]
yr1 = yedges[-1]
print "xr0 xr1 yr0 yr1", xr0, xr1, yr0, yr1

print "hdata.max():", hdata.max()
hdata = hdata/hdata.max()
extent = [xr0, xr1, yr0, yr1]

hdata_smooth = ndimage.gaussian_filter(hdata, sigma=1.5, order=0)
#hdata_smooth = hdata
hdata_masked = np.ma.masked_where(hdata_smooth <= 0.0, hdata)
im = ax3.imshow(hdata_masked,
               interpolation='nearest',
               origin='lower',
               extent=extent,
               cmap='Reds',
               vmin=0.0,
               #vmax=1.0e-10,
               aspect='auto')

#colorbar(im,
#         shrink=0.88,
#         pad=0.0)

levels = [0.05]
cs1 = ax3.contour(hdata_smooth,
                levels,
                colors = 'k',
                origin='lower',
                extent=extent)
zc = cs1.collections[0]
plt.setp(zc, linewidth=1)


levels = [0.32]
cs = ax3.contour(hdata_smooth.T,
                levels,
                colors = 'k',
                origin='lower',
                extent=extent)
zc = cs.collections[0]
plt.setp(zc, linewidth=1)

for c in cs.collections:
    c.set_dashes([(0, (1.0, 1.0))])





savefig('fig.pdf', bbox_inches='tight')

