import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize
import sys


#Units
ctomev = 1/1.6022e33 # dyne/cm^2 to MeV/fm^3
ctopetk = 7.514e5*.467 # divide by this factor holds for all MeV/fm^3 values
ctorhoetk = 939.5/7.514e5/.4627 # multiply by this factor hold for all 1/fm^3 values
home = os.environ["HOME"]
filename = home + "/masterarbeit/EOS/SLypp.dat"
filenameETK = home + "/masterarbeit/EOS/SLyppETK.dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))
print num_lines
p_data = lin_data[:, 3]
rho_data = lin_data[:, 1]
hybrid_gamma = [1.58425, 1.28733, 0.62223, 1.35692, 3.005, 2.988, 2.851]
hybrid_rho = [3.951156e-11, 6.125960e-07, 4.254672e-06, 2.367449e-04, 8.114721e-04, 1.619100e-03]
k0 = 1.685819e2
k_list = [k0]
local_tiny = 1e-10
"""
mymu /= 7.514e5*.4627;
myp[neos]/=7.514e5*.4627;
// myrho[neos]*=939.5/7.514e5/.4627;
"""


def k(rho, gamma0, gamma1, k0):

    return k0 * ((rho**gamma0) / (rho**gamma1))


def edens(p, gamma, rho):

    return p / ((gamma - 1.) * rho )


def mu(energyd, rho):

    return rho * (1. + energyd)


# need to know gamma for calc of eps
for i in range(len(hybrid_gamma) - 1):
    k_list.append(k(hybrid_rho[i], hybrid_gamma[i], hybrid_gamma[i + 1], k_list[i]))
    print i, k_list[i]
    print k_list
i = 0
with open(filenameETK, "wr+") as f:
    while i <= 5:
        for j in range(11, num_lines):
            pmev = lin_data[j, 3] * ctomev
            rhoetk = lin_data[j, 1] * ctorhoetk
            if hybrid_rho[i] <= rhoetk <= hybrid_rho[i + 1]:
                energydens = edens(pmev, hybrid_gamma[i], rhoetk)
                # otherwise neg energydens --> code would crash
                if energydens < local_tiny:
                    energydens = 0.
                chempot = mu(energydens, rhoetk)
                f.write("    " + "{0:3.8e}".format(lin_data[j, 1]) + "    " + "{0:3.8e}".format(pmev)
                        + "    " + "{0:3.8e}".format(energydens) + "    " + "{0:3.8e}".format(chempot) + "\n")
            elif lin_data[j, 1] > hybrid_rho[len(hybrid_rho) -1]:
                energydens = edens(pmev, hybrid_gamma[len(hybrid_gamma) - 1], lin_data[j, 1])
                chempot = mu(energydens, lin_data[j, 1])
                f.write("    " + "{0:3.8e}".format(lin_data[j, 1]) + "    " + "{0:3.8e}".format(pmev)
                        + "    " + "{0:3.8e}".format(energydens) + "    " + "{0:3.8e}".format(chempot) + "\n")
            else:
                print(hybrid_rho[i], lin_data[j, 1], hybrid_rho[i + 1], str(j), str(i))
                i = i + 1
f.close()







