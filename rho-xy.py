import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import h5py
import os
import scidata.carpet.hdf5 as hdf5
import plotsettingsalp
from scipy import interpolate
import matplotlib.ticker as ticker
from matplotlib.ticker import NullFormatter
import matplotlib.gridspec as gridspec
from pylab import *
import matplotlib.patches as patches
home = os.environ["HOME"]
nullfmt = NullFormatter()  # no labels


def get_data(df, it, rl):
    grid = df.get_reflevel(iteration=it, reflevel=rl)
    x, y = grid.mesh()
    dat = df.get_reflevel_data(grid, iteration=it)
    return x, y, dat

filename = home + "/simulations/sim_g3k200_1501_nosph/alp.xy.h5"
print "Opening dataset " + str(filename)
datafilealp = hdf5.dataset(filename)
print "Completed opening from dataset"

filename = home + "/simulations/sim_g3k200_1501_nosph/rho.xy.h5"
print "Opening dataset " + str(filename)
datafilerho = hdf5.dataset(filename)
print "Completed opening dataset"

# define the colormap
cmap = [plt.cm.gist_earth, plt.cm.afmhot]

# units
uc = 2.99792458 * 10 ** (10)
uG = 6.67428 * 10 ** (-8)
uMs = 1.9884 * 10 ** (33)
utime = uG * uMs / uc ** 3 * 1000
ulenght = (uG * uMs / uc ** 2) / 100000
urho = (uc ** 6) / (uG ** 3 * uMs ** 2)
normalnuc = 2.705 * 10 ** (14)

# plot
plotmax = [1, 15.5]
plotmin = [0.3, 9]
wcon = 0.2
wcon1 = 0.5

ianf = 1
iend = 200
for it in range(ianf, iend):
    # Grid
    plt.figure(0)

    ivec = [it, it, it]
    itr_list = datafilerho.iterations
    # conver to ctu
    ctu_list = np.array(itr_list)
    ax = plt.gca()
    itr = itr_list[it]


    x5, y5, ye5 = get_data(datafilerho, itr, 0)
    x4, y4, ye4 = get_data(datafilerho, itr, 0)
    clevels = [10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5]


    ye_col = ax.pcolormesh(-ulenght * x5, -ulenght * y5, np.log10(urho * ye5), shading='gouraud',
                                   vmin=plotmin, vmax=plotmax, cmap=cmap[0])
    ax.pcolormesh(ulenght * x5, ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin,
                         vmax=plotmax, cmap=cmap[0])
    ax.pcolormesh(-ulenght * x5, ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin,
                         vmax=plotmax, cmap=cmap[0])
    ax.pcolormesh(ulenght * x5, -ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin,
                          vmax=plotmax, cmap=cmap[0])
    ax.contour(ulenght * x5, ulenght * y5, np.log10(urho * ye5), levels=clevels, colors="black",
                       linewidths=wcon, linestyles='-')
    ax.contour(-ulenght * x5, -ulenght * y5, np.log10(urho * ye5), levels=clevels, colors="black",
                       linewidths=wcon, linestyles='-')
    ax.contour(-ulenght * x5, ulenght * y5, np.log10(urho * ye5), levels=clevels, colors="black",
                       linewidths=wcon, linestyles='-')
    ax.contour(ulenght * x5, -ulenght * y5, np.log10(urho * ye5), levels=clevels, colors="black",
                       linewidths=wcon, linestyles='-')
    #      ax.contour(ulenght*x5,ulenght*y5,np.log10(urho*ye5),levels=[np.log10(3*normalnuc)],colors="red",linewidths=wcon1,linestyles='-')
    #      ax.contour(-ulenght*x5,-ulenght*y5,np.log10(urho*ye5),levels=[np.log10(3*normalnuc)],colors="red",linewidths=wcon1,linestyles='-')
    #cbar = plt.colorbar(ye_col, ticks=[9, 10, 11, 12, 13, 14, 15], ax=plt.gca())
    #cbar.set_label(r'$\rm log(\rho) \,[g/cm^3]$')


            #saveFig = home + "/Videos/test/picture" + str(ivec[0] - ianf) + ".png"
    #plt.savefig(saveFig, dpi=300)
plt.show()
# saveFig="./output/"+name2+"-"+name1+"-"+str(ivec[0])+"a.pdf"
# plt.savefig(saveFig)
# plt.show()
#plt.close()
