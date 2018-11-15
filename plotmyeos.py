import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize


home = os.environ["HOME"]
rhovalue = [4.1243520175976893E-007, 3.61457E-004, 8.411213E-004, 1.05969E-003, 1.47347E-003]
#rhovalue = [2.9508767E-003, 3.07289e-003, 3.3234E-003, 3.51321E-003, 3.75131E-003]
i = 0
filename = home + "/masterarbeit/tov_solver_stefan/myeos.dat"
filenameConstants = home + "/simulations/polytropics/constants.dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))
sz = 1


def polytrope_func(x, k, y):
    return k * (x ** y)


while i <= 3:
    filenamePolytrope = home + "/simulations/polytropics/myeospolytrope" + str(i) + ".dat"
    with open(filenamePolytrope, "w" "r+") as f:
        print i
        for j in range(1, num_lines):
            if rhovalue[i] <= lin_data[j, 2] <= rhovalue[i+1]:
                f.write(str(lin_data[j, 2]) + "   " + str(lin_data[j, 1]) + "\n")  # rho press #
    lin_data_polytrope = np.genfromtxt(filenamePolytrope)
    x_data = lin_data_polytrope[:, 0]
    y_data = lin_data_polytrope[:, 1]
    with open(filenameConstants, "a") as fConstants:
        params, params_covariance = optimize.curve_fit(polytrope_func, x_data, y_data, maxfev=10000)
        fConstants.write("interval" + str(i) + ": " + "[ " + str(rhovalue[i]) + " , " + str(rhovalue[i + 1]) + " ]; " +
                         "constant: " + str(params[0]) + " index : " + str(params[1]) + "\n")
        plt.scatter(x_data, y_data, sz)
        plt.plot(x_data, polytrope_func(x_data, params[0], params[1]), label='Fitted function' + str(i))
        plt.xlabel('rho')
        plt.ylabel("press")
        plt.legend()
        plt.show()
    i = i + 1
