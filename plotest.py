
import numpy as np
import matplotlib.pyplot as plt
import os
import h5py
home = os.environ["HOME"]
filename = "/media/hanauske/79e09806-79c8-4fad-ad62-dabe9db9d8d8/VARTC/ET/output/migration/alp.xy.h5"
print ("Opening dataset " + str(filename))
datafilealp = h5py.File(filename, 'r')
print ("Completed opening dataset")
print("Keys: %s" % datafilealp.keys())
a_group_key = list(datafilealp.keys())[0]
dataalp = list(datafilealp[a_group_key])
filename = "/media/hanauske/79e09806-79c8-4fad-ad62-dabe9db9d8d8/VARTC/ET/output/migration/rho.xy.h5"
print("Opening dataset " + str(filename))
datafilerho = h5py.File(filename, 'r')
print ("Completed opening dataset")
print("Keys: %s" % datafilerho.keys())
a_group_key = list(datafilerho.keys())[0]
datarho = list(datafilerho[a_group_key])