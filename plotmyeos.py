import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize
import sys


print sys.stdout.encoding
home = os.environ["HOME"]
rhovalue = [4.1243520175976893E-007, 1e-003, 1.2026915650335159E-003, 2.0E-003, 2.5600808600748546E-003, 3.0125886980602552E-003, 3.7500560471732491E-003]
i = 0
filename = home + "/masterarbeit/tov_solver_stefan/myeos.dat"
filenameConstants = home + "/simulations/polytropics/constants.dat"
filenamePolytrope = home + "/simulations/polytropics/myeospolytrope" + str(i) + ".dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))


def polytrope_func(x, k, y):
    return k * (x ** y)


while i <= 0:
    with open(filenamePolytrope, "w" "r+") as f:
        for j in range(num_lines):
            if rhovalue[i] <= lin_data[j, 2] < rhovalue[i+1] and lin_data[j, 2] != 0:
                f.write(str(lin_data[j, 2]) + " " + str(lin_data[j, 1]) + "\n")  # rho press #
    f.close()
    lin_data_polytrope = np.genfromtxt(filenamePolytrope)
    x_data = lin_data_polytrope[:, 0]
    y_data = lin_data_polytrope[:, 1]
    with open(filenameConstants, "w+" "r+") as fConstants:
        params, params_covariance = optimize.curve_fit(polytrope_func, x_data, y_data)
        fConstants.write("interval: " + "[ " + str(rhovalue[i]) + " , " + str(rhovalue[i+1]) + " ); " + "constant: " + str(params[0])\
                 + "; index : " + str(params[1]) + "\n")
        print("params:", str(params), str(i))
        plt.scatter(x_data, y_data)
        plt.plot(x_data, polytrope_func(x_data, params[0], params[1]), label='Fitted function', color="r")
        plt.xlabel('rho')
        plt.ylabel("press")
        plt.legend()
        plt.show()
    i = i + 1
