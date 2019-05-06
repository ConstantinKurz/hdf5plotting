import numpy as np
import random
import matplotlib.pyplot as plt
import os.path
from scipy import optimize
from lmfit import Model

global gamma0
global k0
global rho0


def polytrope_func(rho_data,k, g):
    return k * rho_data ** g


def press_func(rho_data, gamma):
    return k0 * rho0 ** gamma0 / rho0 ** gamma * rho_data ** gamma


def press_func_multifit(X, gamma):
    rho_data, k0, gamma0, rho = X
    return (k0 * rho ** gamma0 / rho ** gamma) * rho_data ** gamma


def k(k0, rho, gamma0, gamma1):
    return k0 * rho ** gamma0 / rho ** gamma1


k_list = []
gamma = []
home = os.environ["HOME"]
# rho values for different pieces
rhovalue = [0, 3.61457e-04, 8.41121e-04, 1.05969e-03, 1.48347e-03, 2.95087e-03,
            3.07289e-03,  3.33234e-03,  3.51321e-03]
# read data
filename = home + "/Desktop/Masterarbeit/EOS/myeos.dat"
filenameConstants = home + "/Desktop/Masterarbeit/EOS/myeosconstants.dat"
lin_data = np.genfromtxt(filename)
num_lines = sum(1 for line in open(filename))
# scatterplot all data
rho_data = lin_data[:, 0]
p_data = lin_data[:, 1]
plt.scatter(rho_data, p_data)

# split data according to rhovalue and write into files
for i in range(0,len(rhovalue) - 1):
    filenamePolytrope = home + "/Desktop/Masterarbeit/EOS/eosPolytropes" + str(i) + ".dat"
    print(i)
    with open(filenamePolytrope, "w+") as f:
        for j in range(1, num_lines - 1):
            #print rhovalue[i], lin_data[j,2], rhovalue[i + 1]
            if rhovalue[i] < lin_data[j, 2] <= rhovalue[i+1]:
                f.write(str(lin_data[j, 2]) + "   " + str(lin_data[j, 1]) + "\n")  # rho press #
    #f.close

# fit first polytrope, add values to list and plot afterwards
filenamePolytrope0 = home + "/Desktop/Masterarbeit/EOS/eosPolytropes0.dat"
lin_data_polytrope = np.genfromtxt(filenamePolytrope0)
rho_data = lin_data_polytrope[:, 0]
p_data = lin_data_polytrope[:, 1]
print(rho_data, p_data )
# fit p_data using polytropes_func and rho_data
params, params_covariance = optimize.curve_fit(polytrope_func, rho_data, p_data)
print("Gamma0:", params[0], "K0:", params[1], "\n")
gamma.append(params[0])
k_list.append(params[1])
plt.plot(rho_data, polytrope_func(rho_data, gamma[0], k_list[0]), label='Fitted function' + str(0), color="red")
#print params


# fit for all pieces, append k and gamma respectively and fit again afterwards
for i in range(1, len(rhovalue) -1):

    #print(type(gamma))
    # read from created files
    filenamePolytrope = home + "/Desktop/Masterarbeit/EOS/eosPolytropes{}".format(i) + ".dat"
    lin_data_polytrope = np.genfromtxt(filenamePolytrope)
    rho_data = lin_data_polytrope[:, 0] #RHO
    p_data = lin_data_polytrope[:, 1] #PRESS
    k0 = k_list[i-1]
    gamma0 = gamma[i-1]
    rho0 = rhovalue[i]
    """
   # k_local = np.empty(len(rho_data)) ; k_local.fill(k_list[i-1])
   # rho_local = np.empty(len(rho_data)) ; rho_local.fill(rhovalue[i])
   # gamma_local = np.empty(len(rho_data)); gamma_local.fill(gamma[i-1])
    """
    print (i, "\n")
    #print ("rho:","\n", rho_data,"\n","press:", "\n", p_data, "\n")
    # fit press with initial fit obtained above
    #gmodel = Model(press_func, independent_vars=["rho_data", "k0", "gamma0", "rho0"], params=["gamma"])
    gmodel = Model(press_func)
    params = gmodel.make_params()
    """
    print(gmodel.independent_vars)
    print(params)
    print(np.isnan(p_data).any(), np.isnan(rho_data).any())
    """
    #result = gmodel.fit(p_data, params, rho_data=rho_data, nan_policy='omit')
    params, params_covariance = optimize.curve_fit(press_func, rho_data, p_data)
    print(params, params_covariance)

    """
    #result = gmodel.fit(p_data, rho_data=rho_data, k0=k_list[i-1], gamma0=gamma[i-1], rho0=rhovalue[i])
    #print(result.fit_report())
    #gmodel.fit(1, 2, k0=1, gamma0=1, rho0=1)
    """
    gamma.append(params[0])
    k_list.append(k(k_list[i-1], rhovalue[i], gamma[i-1], gamma[i]))
    print(gamma, k_list)
    plt.plot(rho_data, polytrope_func(rho_data, gamma[i-1], k_list[i-1]), label='Fitted function' + str(i))
    plt.show()
