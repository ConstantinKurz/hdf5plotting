import h5py
import os
import numpy as np
import matplotlib.pyplot as plt

home = os.environ["HOME"]
filename = home + "/masterarbeit/Hanauske_Tut_Out/collapse/alp.x.h5"
f5 = h5py.File(filename)
for nm in f5:
    if not hasattr(f5[nm], "shape"):
        continue
    print("nm=", nm)
    #d = np.copy(f5[nm])
    #print(d)
    plt.plot(nm)
    plt.figure()
    plt.show()