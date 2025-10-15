import numpy as np
import matplotlib.pyplot as plt

datasu = np.loadtxt("alpha_sa.dat", float)
data45 = np.loadtxt("alpha_45.dat", float)
data90 = np.loadtxt("alpha_90.dat", float)


alfa_su = datasu[:,0]
alfa_45 = data45[:,0]
alfa_90 = data90[:,0]

f_su = datasu[:,1]
f_45 = data45[:,1]
f_90 = data90[:,1]

plt.scatter(alfa_su, f_su, label='sa')
plt.scatter(alfa_45, f_45, label='45')
plt.scatter(alfa_90, f_90, label='90')
plt.plot(alfa_su, f_su)
plt.plot(alfa_45, f_45)
plt.plot(alfa_90, f_90)
plt.legend(loc='best')
plt.show()

print(f"saudavel: Δα = {abs(alfa_su[0] - alfa_su[-1])}")
print(f"45cm: Δα = {abs(alfa_45[0] - alfa_45[-1])}")
print(f"90cm: Δα = {abs(alfa_90[0] - alfa_90[-1])}")