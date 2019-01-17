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


def get_data(df, it, rl):
    grid = df.get_reflevel(iteration=it, reflevel=rl)
    x, y = grid.mesh()
    dat = df.get_reflevel_data(grid, iteration=it)
    return x, y, dat


namesim = home + "/simulations/myeosspherical/l2m2t10/yz"
name = "/vel[0]"
filename = namesim + name + ".yz.h5"
print "Opening dataset " + str(filename)
datafilevx = hdf5.dataset(filename)
print "Completed opening dataset"

name = "/vel[1]"
filename = namesim + name + ".yz.h5"
print "Opening dataset " + str(filename)
datafilevy = hdf5.dataset(filename)
print "Completed opening dataset"

name = "/vel[2]"
filename = namesim + name + ".yz.h5"
print "Opening dataset " + str(filename)
datafilevz = hdf5.dataset(filename)
print "Completed opening dataset"

name = "/rho"
filename = namesim + name + ".yz.h5"
print "Opening dataset " + str(filename)
datafilerhoxy = hdf5.dataset(filename)
print "Completed opening dataset"

# define the colormap
cmap = [plt.cm.gist_earth, plt.cm.afmhot]

# units
uc = 2.99792458 * 10 ** (10)
uG = 6.67428 * 10 ** (-8)
uMs = 1.98892 * 10 ** (33)
utime = uG * uMs / uc ** 3 * 1000
ulenght = (uG * uMs / uc ** 2) / 100000
urho = (uc ** 6) / (uG ** 3 * uMs ** 2)
normalnuc = 2.705 * 10 ** (14)
umrechnmasse = 1.98892 * 10 ** (30)

# plot
plotmax = [0.35, 16.5]
plotmin = [0, 9.5]
wcon = 0.3
wcon1 = 3

ianf = 0
iend = 320
for it in range(ianf, iend, 1):
    print "Plotting at ", it
    # Grid
    plt.figure(0)
    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1], wspace=0.2)
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])

    ivec = [it, it, it]
    itr_list = datafilerhoxy.iterations
    ctu_list = np.array(itr_list)
    timeperit = 4
    ms_list = timeperit * utime * ctu_list

    # for i in ivec:
    for j, ax in enumerate(plt.gcf().axes):
        i = ivec[j]
        itr = itr_list[i]

        ax.axis([-18, 18, -18, 18])
        ax.set_ylabel(r'$\rm y \,[km]$')
        ax.set_xlabel(r'$\rm x \,[km]$')
        ax.minorticks_on()

        if j == 0:
            x, y, fx = get_data(datafilevx, itr, 0)
            x, y, fy = get_data(datafilevy, itr, 0)
            x, y, fz = get_data(datafilevz, itr, 0)
            f = (fx * fx + fy * fy + fz * fz) ** (0.5)
            print "Max v", np.max(f)
            print "Min v", np.min(f)
            clevels = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        if j == 1:
            x, y, f = get_data(datafilerhoxy, itr, 0)
            clevels = np.linspace(13.8, 16.5, 15)
            print "Max Log(rho)", np.max(np.log10(urho * f))
            print "Min Log(rho)", np.min(np.log10(urho * f))

        if j == 1:
            ye_col = ax.pcolormesh(-ulenght * x, -ulenght * y, np.log10(urho * f), shading='gouraud', vmin=plotmin[j],
                                   vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(ulenght * x, ulenght * y, np.log10(urho * f), shading='gouraud', vmin=plotmin[j],
                          vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(-ulenght * x, ulenght * y, np.log10(urho * f), shading='gouraud', vmin=plotmin[j],
                          vmax=plotmax[j], cmap=cmap[j])
            ax.pcolormesh(ulenght * x, -ulenght * y, np.log10(urho * f), shading='gouraud', vmin=plotmin[j],
                          vmax=plotmax[j], cmap=cmap[j])
            ax.contour(ulenght * x, ulenght * y, np.log10(urho * f), levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            ax.contour(-ulenght * x, -ulenght * y, np.log10(urho * f), levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            ax.contour(-ulenght * x, ulenght * y, np.log10(urho * f), levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            ax.contour(ulenght * x, -ulenght * y, np.log10(urho * f), levels=clevels, colors="black", linewidths=wcon,
                       linestyles='-')
            #      ax.contour(ulenght*x,-ulenght*y,np.log10(urho*f),levels=[np.log10(urho*0.00048298863)],colors="cyan",linewidths=wcon1,linestyles='-')
            ax.contour(ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(3.0 * normalnuc)], colors="red",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(3.0 * normalnuc)], colors="red",
                       linewidths=wcon1, linestyles='-')
            ax.contour(ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(3.0 * normalnuc)], colors="red",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(3.0 * normalnuc)], colors="red",
                       linewidths=wcon1, linestyles='-')
            ax.contour(ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(1.0 * normalnuc)], colors="lime",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(1.0 * normalnuc)],
                       colors="lime", linewidths=wcon1, linestyles='-')
            ax.contour(ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(1.0 * normalnuc)], colors="lime",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(1.0 * normalnuc)], colors="lime",
                       linewidths=wcon1, linestyles='-')
            ax.contour(ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(4.5 * normalnuc)], colors="cyan",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(4.5 * normalnuc)],
                       colors="cyan", linewidths=wcon1, linestyles='-')
            ax.contour(ulenght * x, -ulenght * y, np.log10(urho * f), levels=[np.log10(4.5 * normalnuc)], colors="cyan",
                       linewidths=wcon1, linestyles='-')
            ax.contour(-ulenght * x, ulenght * y, np.log10(urho * f), levels=[np.log10(4.5 * normalnuc)], colors="cyan",
                       linewidths=wcon1, linestyles='-')
            cbar = plt.colorbar(ye_col, ticks=[9, 10, 11, 12, 13, 14, 15, 16], ax=ax)
            cbar.set_label(r'$\rm log(\rho \,[g/cm^3])$')

        if j == 0:
            ye_col = ax.pcolormesh(-ulenght * x, -ulenght * y, f, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                                   cmap=cmap[j])
            ax.pcolormesh(ulenght * x, ulenght * y, f, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.pcolormesh(-ulenght * x, ulenght * y, f, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.pcolormesh(ulenght * x, -ulenght * y, f, shading='gouraud', vmin=plotmin[j], vmax=plotmax[j],
                          cmap=cmap[j])
            ax.contour(ulenght * x, ulenght * y, f, levels=clevels, colors="black", linewidths=wcon, linestyles='-')
            ax.contour(-ulenght * x, -ulenght * y, f, levels=clevels, colors="black", linewidths=wcon, linestyles='-')
            ax.contour(-ulenght * x, ulenght * y, f, levels=clevels, colors="black", linewidths=wcon, linestyles='-')
            ax.contour(ulenght * x, -ulenght * y, f, levels=clevels, colors="black", linewidths=wcon, linestyles='-')
            cbar = plt.colorbar(ye_col, ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1], ax=ax)
            cbar.set_label(r'$\rm \sqrt{{v_{\!x}}^2+{v_{\!y}}^2+{v_{\!z}}^2} \, [c]$')

    ms = ms_list[i]
    ct = float("{0:.2f}".format(ms))
    ax.set_title(r'$\rm t= ' + str(ct) + '  \,ms$', fontsize=26)
    saveFig = namesim + "/outputRhoVel/img-" + "{:0>3d}".format(ivec[0] - ianf) + ".jpg"
    plt.savefig(saveFig, dpi=100, bbox_inches="tight", pad_inches=0.05, format="jpg")
    saveFig = namesim + "/outputRhoVel/img-" + "{:0>3d}".format(ivec[0] - ianf) + ".pdf"
    plt.savefig(saveFig, bbox_inches="tight", pad_inches=0.05, format="pdf")
# plt.show()
plt.close()