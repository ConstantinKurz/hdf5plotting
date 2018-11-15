import numpy as np
import matplotlib.pyplot as plt
import os.path


home = os.environ["HOME"]
filename_rho = home + "/simulations/myeoskollaps/rho.x.asc"
lin_data_polytrope = np.genfromtxt(filename_rho)
x_data = lin_data_polytrope[11:136, 12]
filename_press = home + "/simulations/myeoskollaps/press.x.asc"
lin_data_polytrope = np.genfromtxt(filename_press)
y_data = lin_data_polytrope[11:136, 12]
plt.scatter(x_data, y_data)
plt.xlabel('$ \ rho[1/fm^3]$')
plt.ylabel("$p[MeV/fm^3]$")
plt.legend()
plt.show()
