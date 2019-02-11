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

filename = home + "/simulations/test_dx0.1_sph3/output-0000/myeostest/alp.yz.h5"
print "Opening dataset " + str(filename)
datafilealp = hdf5.dataset(filename)
print "Completed opening from dataset"

filename = home + "/simulations/test_dx0.1_sph3/output-0000/myeostest/rho.yz.h5"
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
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.2)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ivec = [it, it, it]
    itr_list = datafilerho.iterations
    # conver to ctu
    ctu_list = np.array(itr_list)

    # for i in ivec:
    for j, ax in enumerate(plt.gcf().axes):
        i = ivec[j]
        print "Plotting at ", i

        ax.axis([-25, 25, -25, 25])
        ax.set_ylabel(r'$\rm z \,[km]$')
        ax.set_xlabel(r'$\rm y \,[km]$')
        itr = itr_list[i]

        ax.minorticks_on()

        if j == 0:
            x5, y5, ye5 = get_data(datafilealp, itr, 0)
            x4, y4, ye4 = get_data(datafilealp, itr, 0)
            clevels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        if j == 1:
            x5, y5, ye5 = get_data(datafilerho, itr, 0)
            x4, y4, ye4 = get_data(datafilerho, itr, 0)
            clevels = [10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5]

        if j == 1:
            ye_col = ax.pcolormesh(-ulenght * x5, -ulenght * y5, np.log10(urho * ye5), shading='gouraud',
                                   vmin=plotmin[j], vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(ulenght * x5, ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin[j],
                         vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(-ulenght * x5, ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin[j],
                         vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(ulenght * x5, -ulenght * y5, np.log10(urho * ye5), shading='gouraud', vmin=plotmin[j],
                          vmax=plotmax[j], cmap=cmap[j])
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
            cbar = plt.colorbar(ye_col, ticks=[9, 10, 11, 12, 13, 14, 15], ax=ax)
            cbar.set_label(r'$\rm log(\rho) \,[g/cm^3]$')

        if j == 0:
            ye_col = ax.pcolormesh(-ulenght * x5, -ulenght * y5, ye5, shading='gouraud', vmin=plotmin[j],
                                   vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(ulenght * x5, ulenght * y5, ye5, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.pcolormesh(-ulenght * x5, ulenght * y5, ye5, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.pcolormesh(ulenght * x5, -ulenght * y5, ye5, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.contour(ulenght * x5, ulenght * y5, ye5, levels=clevels, colors="black", linewidths=wcon, linestyles='-')
            ax.contour(-ulenght * x5, -ulenght * y5, ye5, levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            ax.contour(-ulenght * x5, ulenght * y5, ye5, levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            ax.contour(ulenght * x5, -ulenght * y5, ye5, levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            cbar = plt.colorbar(ye_col, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], ax=ax)
            cbar.set_label(r'$\rm \alpha $')

            saveFig = home + "/Videos/test/dx_0.1_yz" + str(ivec[0] - ianf) + ".png"
    plt.savefig(saveFig, dpi=300)
    #plt.show()
# saveFig="./output/"+name2+"-"+name1+"-"+str(ivec[0])+"a.pdf"
# plt.savefig(saveFig)(Pert_Amplitude[star] *
# plt.show()
plt.close()
