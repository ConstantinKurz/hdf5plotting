import numpy as np
import matplotlib.pyplot as plt
import os.path
from scipy import optimize


home = os.environ["HOME"]
rhovalue = [3.951156E-11, 61259E-07, 4.254672E-06, 2.367449E-004, 8.114721E-004, 1.619100e-003]
gammavalue = [1.58425, 1.28733, 0.62223, 1.35692, 3.005, 2.988, 2.851]
i = 0
filename = home + "/simulations/myeosparma.dat"

rho = 3.915156E-11
k0 = 1.68e2
j = 1
p = 0
k = list()
k.append(k0)


def polytrope_func(rho, k_func, gamma):
    return k_func * (rho ** gamma)


print(len(gammavalue))
while j in range(len(gammavalue)):
    k.append(k[j - 1] * rhovalue[j - 1] ** (gammavalue[j - 1] - gammavalue[j]))
    j += 1
print k
hybrid_local_gamma = gammavalue[0]
hybrid_local_k = k[0]
with open(filename, "w+" ) as f:
    while rho < 1.6191e-003:
        while p in range(1, len(gammavalue) - 1):
            if rho > rhovalue[p]:
                hybrid_local_gamma = gammavalue[p + 1]
                hybrid_local_k = k[p + 1]
        f.write(str(rho) + " " + str(polytrope_func(rho, hybrid_local_k, hybrid_local_gamma)) + "\n")
        rho += 2.1001191487368301e-11
lin_data = np.genfromtxt(filename)
x_data = lin_data[:, 1]
y_data = lin_data[:, 1]
plt.scatter(x_data, y_data, sz)
plt.xlabel('$ \rho[1/fm^3]$')
plt.ylabel('$p[MeV/fm^3]$')
plt.legend
plt.savefi(home + "/simulations/parmasly.png", dpi = 300)



