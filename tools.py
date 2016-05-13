import scipy.ndimage as ndimage
import numpy as np
import math
from pylab import *
from scipy.interpolate import griddata






#read data in CODA format using genfromtxt
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

#find using iteration the level of some arbitratry distribution where 
# we have some fraction of points
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


#using previous level finder locate the edges corresponding to these
# limits
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
            #print "j:",j
            i2 = j
            xhi = bin_edges[i2]
            break
            
    return xlo, xhi, i1, i2, hlim

def hist1d(ax, var, level, xlabel='var'):
    ax.minorticks_on()
    ax.set_xlabel(xlabel)

    #compute histogram
    hist, bin_edges = np.histogram(var, bins=50, normed=True)
    bins = bin_edges[0:-1] + np.diff(bin_edges)

    #compute limits
    xlo1, xhi1, i1, i2, hlim = conf_lims(hist, bin_edges, level)
    rd = 3
    print "xlo:", round(xlo1,rd), " ",i1, " xhi:", round(xhi1,rd), " ", i2, " level:",round(hlim, rd)

    ax.plot(bins, hist, "k-")
    ax.fill_between(bins[i1:i2], hist[i1:i2], np.zeros(i2-i1), color='darkorange', alpha=0.8)

    return


def hist2d(ax, var1, var2, levels, binsize=50, smooth=1.5, xlabel='varx', ylabel='vary'):

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    hdata, xedges, yedges = np.histogram2d(var1, var2, bins=binsize)

    xr0 = xedges[0]
    xr1 = xedges[-1]
    yr0 = yedges[0]
    yr1 = yedges[-1]
    #print "xr0 xr1 yr0 yr1", xr0, xr1, yr0, yr1

    #print "hdata.max():", hdata.max()
    hdata = hdata/hdata.max()
    extent = [xr0, xr1, yr0, yr1]
    
    if smooth == 0:
        hdata_smooth = hdata
    else:
        hdata_smooth = ndimage.gaussian_filter(hdata, sigma=smooth, order=0)

    hdata_masked = np.ma.masked_where(hdata_smooth <= 0.0, hdata)
    im = ax.imshow(hdata_masked,
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
    
    icount = 0
    for level in levels:

        levels = [1.0-level]
        cs = ax.contour(hdata_smooth,
                levels,
                colors = 'k',
                origin='lower',
                extent=extent)
        zc = cs.collections[0]
        plt.setp(zc, linewidth=1)
   

        #change linestyle for second contour
        if icount > 0:
            for c in cs.collections:
                c.set_dashes([(0, (1.0, 1.0))])

        icount += 1

    return



