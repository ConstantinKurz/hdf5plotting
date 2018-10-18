import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize
import sys


print sys.stdout.encoding
home = os.environ["HOME"]
rhovalue = [4.1243520175976893E-007, 5.9539982726418438E-004, 1.2026915650335159E-003, 1.2963084417077087E-003, 2.9600808600748546E-003, 3.2125886980602552E-003, 3.7500560471732491E-003]
i = 0
filename = home + "/Desktop/Stefan_TOV_Solver/myeos.dat"
filenameConstants = home + "/Desktop/Stefan_TOV_Solver/constants.dat"
filenamePolytrope = home + "/Desktop/Stefan_TOV_Solver/myeospolytrope" + str(i) + ".dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))
print(rhovalue[i], lin_data[1, 2], rhovalue[i+1])


def polytrope_func(x, k, y):
    return k * (x ** y)


while i <= 6:
    with open(filenamePolytrope, "r+") as f:
        for j in range(num_lines):
            if rhovalue[i] <= lin_data[j, 2] <= rhovalue[i+1]:
                f.write(lin_data[j, :])
                filenamePolytrope = filenamePolytrope.encode("latin-1")

            else:
                print("fail")
                print(rhovalue[i], lin_data[j, 2], rhovalue[i + 1], str(j))
    f.close()
    lin_data_polytrope = np.genfromtxt(filenamePolytrope)
    x_data = lin_data_polytrope[:, 2]
    y_data = lin_data_polytrope[:, 1]
    open(filenameConstants)
    result = params, params_covariance = optimize.curve_fit(polytrope_func, x_data, y_data)
    filenameConstants.write(result, "\n")
    plt.scatter(x_data, y_data)
    plt.plot(x_data, polytrope_func(x_data, params[0], params[1]), label='Fitted function')
    plt.xlabel('rho')
    plt.ylabel("press")
    plt.show()
i = i + 1
