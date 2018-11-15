import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize


home = os.environ["HOME"]
#rhovalue = [4.1243520175976893E-007, 3.61457E-004, 8.411213E-004, 1.05969E-003, 1.47347E-003]
#rhovalue = [2.9508767E-003, 3.07289e-003, 3.3234E-003, 3.51321E-003, 3.75131E-003]
aveN = 0
rho_in = 1.47347E-003
filename = home + "/masterarbeit/tov_solver_stefan/myeos.dat"
filenamemixed = home + "/masterarbeit/tov_solver_stefan/eosmixed.dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))
count_lines = 6600


def p_interpol(rho):
    return (3.9328093165110178E-004 - 3.9301757601068707E-004) / (2.9508767E-003-1.47347E-003)\
           * (rho-1.47347E-003) + 3.9301757601068707E-004


for j in range(1, count_lines):
    aveN += (lin_data[j+1, 1] - lin_data[j, 1])
    ave = aveN/count_lines

print("average: ", ave)

with open(filenamemixed, "w" "r+") as f:
    while rho_in < 2.9508767E-003:
        rho_in += ave
        if rho_in > 2.9508767E-003:
            break
        press = p_interpol(rho_in)
        f.write(str(rho_in) + " " + str(press) + "\n")
f.close()












