import matplotlib

params = {
    'figure.figsize'    : [24, 8.5],
    'legend.fontsize'   : 24,
    'text.usetex'       : True,
    'axes.titlesize' : 26,
    'axes.labelsize' : 26,  
#    'lines.linewidth' : 3 ,
#    'lines.markersize' : 10 ,
    'xtick.labelsize' : 22 ,
    'ytick.labelsize' : 22 
}

matplotlib.rcParams.update(params)
