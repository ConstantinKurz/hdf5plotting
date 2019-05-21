import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize


def polytrope_func(rho_data, k, g):
    # print k * rho_data ** g, rho_data
    return k * rho_data ** g


def k(k0, rho, gamma0, gamma1):
    return (k0 * rho ** gamma0) / rho ** gamma1


def poly_rmd(gamma0, k_0):
    return 0.001 ** ((gamma0 - 1) / (1 - gamma0)) * k_0 ** (1 / (1 - gamma0))


k_list = []
gamma_list = []
home = os.environ["HOME"]
uc = 2.99792458 * 10 ** (10)
uG = 6.67428 * 10 ** (-8)
uMs = 1.98892 * 10 ** (33)
urho = ((uc ** 6) / (uG ** 3 * uMs ** 2)) * 1000
# conversion to nuc. saturation density
Scaling_NucDens = 0.0004379896294784459
# myeos
# ([0, 8.41121e-04, 1.05969e-03, 1.4E-003, 3E-003,
#                         3.07289e-03, 3.33234e-03, 3.51321e-03, 3.75131E-003])  # 1.4832361E-003 , 2.9512464E-003


# rho values for different pieces
rhovalue_cac = np.array([0, 8.41121e-04, 1.05969e-03, 1.2E-003, 3.0383273518862558E-003, 3.1e-03, 3.2e-03,
                         3.4e-3, 3.51321e-03, 3.6e-3, 3.75131E-003])  # 1.4832361E-003 , 2.9512464E-003
rhovalue = rhovalue_cac / Scaling_NucDens
rhovalue = rhovalue_cac

print("rho values:", rhovalue * Scaling_NucDens)
# print("Rescalded rho values:", rhovalue)

# read data
filenamePizza = home + "/Desktop/Masterarbeit/EOS/myeos.pizza"
filename = home + "/Desktop/Masterarbeit/EOS/myeos.dat"
filenameConstants = "myeosconstants.dat"
lin_data = np.genfromtxt(filename)  # / Scaling_NucDens
num_lines = sum(1 for line in open(filename))
# data
rho_data = lin_data[:, 2]
p_data = lin_data[:, 1]
rho_real = rho_data
p_real = p_data
"""
print rho_data, '\n'
print(p_data)
print len(rho_data)
"""
# split data according to rhovalue and write into files
for i in range(0, len(rhovalue)):
    filenamePolytrope = home + "/Desktop/Masterarbeit/EOS/eosPolytropes" + str(i) + ".dat"
    print(i)
    with open(filenamePolytrope, "w+") as f:
        for j in range(1, num_lines - 1):
            # print rhovalue[i], lin_data[j,2], rhovalue[i + 1]
            if rhovalue[i] < lin_data[j, 2] <= rhovalue[i + 1]:
                # print i, lin_data[j,2]
                f.write(
                    "{0:3.8e}".format(lin_data[j, 2]) + "   " + "{0:3.8e}".format(lin_data[j, 1]) + "\n")  # rho press #
    # f.close

# fit first polytrope, add values to list and plot afterwards
filenamePolytrope0 = home + "/Desktop/masterarbeit/EOS/eosPolytropes0.dat"
lin_data_polytrope = np.genfromtxt(filenamePolytrope0)
rho_data = lin_data_polytrope[:, 0]
p_data = lin_data_polytrope[:, 1]

# print(rho_data, '\n')
# print(p_data)

# fit p_data using polytropes_func and rho_data
params, params_covariance = optimize.curve_fit(polytrope_func, rho_data, p_data,
                                               maxfev=1000000)
k0 = params[0]
k_list.append(k0)
gamma0 = params[1]
gamma_list.append(gamma0)

# compute difference between fitted p and real p
diffp = abs(polytrope_func(rho_data, k0, gamma0) - p_data)
p_fit = polytrope_func(rho_data, k0, gamma0)

plt.subplot(2, 1, 1)
plt.scatter(rho_data / Scaling_NucDens, p_data / Scaling_NucDens, s=4, color="blue")
plt.plot(rho_data / Scaling_NucDens, polytrope_func(rho_data, k0, gamma0) / Scaling_NucDens,
         label=str(0) + ': (' + '{}'.format(rhovalue[0]) + ", "
               + '{}'.format(rhovalue[1]) + "]", color="red")

# fit for all pieces, append k and gamma respectively and fit again afterwards
for i in range(1, len(rhovalue) - 1):
    # read from created files
    filenamePolytrope = home + "/Desktop/Masterarbeit/EOS/eosPolytropes0.dat"
    filenamePolytrope = home + "/Desktop/Masterarbeit/EOS/eosPolytropes{}".format(i) + ".dat"
    lin_data_polytrope = np.genfromtxt(filenamePolytrope)
    rho_data = lin_data_polytrope[:, 0]  # [1.5,2,3,8]
    p_data = lin_data_polytrope[:, 1]  # [.25,0.2,4,5]
    k0 = k_list[i - 1]
    gamma0 = gamma_list[i - 1]
    rho0 = rhovalue[i]


    def press_func(x, gamma1):
        # fit function using interation constants k0, gamma0, rho0
        # print("func values:", k0, gamma0, rho0, gamma1, x)
        # print("press:",(k0 * rho0 ** gamma0 / (rho0 ** gamma1)) * x ** gamma1)
        return (k0 * rho0 ** gamma0 / (rho0 ** gamma1)) * x ** gamma1


    params, params_covariance = optimize.curve_fit(press_func, rho_data, p_data
                                                   , maxfev=10000)
    # compute difference between fitted p and real p

    diffp = np.append(diffp, abs(p_data - polytrope_func(rho_data, k_list[i - 1],
                                                         gamma_list[i - 1])))
    p_fit = np.append(p_fit, polytrope_func(rho_data, k_list[i - 1], gamma_list[i - 1]))

    # append new values 
    gamma1 = params[0]
    gamma_list.append(gamma1)
    # Scaling not used in ETK
    k1 = k(k0, rho0, gamma0, gamma1)
    k_list.append(k1)
    # print("k1 info:", k1, k0, rho0, gamma0, gamma1)
    # plot piecewise polytropes

    # plt.subplot(2, 1, 1)
    # plt.axis([0, 10, 0, 3.5])
    plt.scatter(rho_data / Scaling_NucDens, p_data / Scaling_NucDens, s=4, color="blue")
    plt.plot(rho_data / Scaling_NucDens, polytrope_func(rho_data, k1, gamma1) / Scaling_NucDens,
             label=str(i) + ': (' + '{}'.format(rhovalue[i]) + ", "
                   + '{}'.format(rhovalue[i + 1]) + "]")
    plt.xlabel(" Density $[\\rho_0]$")
    plt.ylabel(" Pressure $[\\rho_0]$")

# info and print
print("gamma:")
print(gamma_list)
print("k:")
print(k_list)
print(3.7513160394899588E-003 * urho)
print(4.1243520175976893E-007 / Scaling_NucDens)
# some additional info
# print(len(rhovalue_cac - 2))
# print(len(gamma_list))
# print(len(k_list))


# write pizza file
with open(filenamePizza, "w+") as f:
    f.write("name=" + "\n")
    f.write("type=pwpoly" + "\n")
    f.write("poly_rmd=" + str(poly_rmd(gamma_list[0], k_list[0])) + "\n")
    f.write("max_rmd=1e100" + "\n")
    for i in range(0, 9):
        print(i)
        f.write(
            "{0:3.8e}".format(rhovalue_cac[i] * urho) + "   " + "{0:3.8e}".format(gamma_list[i]) + "\n")
# for j in range(1, 6600):
#    print("diff: ", diffp[j], "fit: ", p_fit[j], "real: ", p_real[j], \
#          "it: ", j)

# plot difference
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
           ncol=2, fancybox=True, shadow=True)
plt.title("Fitted Polytropes")
plt.subplot(2, 1, 2)
plt.title("Diff")
plt.ylabel(" Pressure Diff $[\\rho_0]$")
plt.xlabel(" Density $[\\rho_0]$")
plt.plot(rho_real[:6600] / Scaling_NucDens, diffp[:6600] / Scaling_NucDens)
plt.show()
