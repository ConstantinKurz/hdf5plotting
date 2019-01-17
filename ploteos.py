import numpy as np
import matplotlib.pyplot as plt
import os.path

sz = 1
home = os.environ["HOME"]
filename = home + "/masterarbeit/tov_solver_stefan/myeos.dat"
lin_data_polytrope = np.genfromtxt(filename)
x_data = lin_data_polytrope[:, 2]
y_data = lin_data_polytrope[:, 1]
plt.scatter(x_data, y_data, sz)
plt.xlabel('$ \ rho[1/fm^3]$')
plt.ylabel("$p[MeV/fm^3]$")
plt.legend()
plt.show()
