import numpy as np
import matplotlib.pyplot as plt



dalpha_sa_1000 = []
dalpha_45_1000 = []
dalpha_90_1000 = []
dalpha_sa_1700 = []
dalpha_45_1700 = []
dalpha_90_1700 = []


Nfile = 1
for i in range(Nfile):

    data_sa_1000 = np.loadtxt(f"f1000rpm/alpha_sa_{i}.dat", float)
    data_45_1000 = np.loadtxt(f"f1000rpm/alpha_45_{i}.dat", float)
    data_90_1000 = np.loadtxt(f"f1000rpm/alpha_90_{i}.dat", float)

    data_sa_1700 = np.loadtxt(f"f1700rpm/alpha_sa_{i}.dat", float)
    data_45_1700 = np.loadtxt(f"f1700rpm/alpha_45_{i}.dat", float)
    data_90_1700 = np.loadtxt(f"f1700rpm/alpha_90_{i}.dat", float)

    alpha_sa_1000 = data_sa_1000[:,0]
    alpha_45_1000 = data_45_1000[:,0]
    alpha_90_1000 = data_90_1000[:,0]
    alpha_sa_1700 = data_sa_1700[:,0]
    alpha_45_1700 = data_45_1700[:,0]
    alpha_90_1700 = data_90_1700[:,0]

    dalpha_sa_1000.append(abs(alpha_sa_1000[0] - alpha_sa_1000[-1]))
    dalpha_45_1000.append(abs(alpha_45_1000[0] - alpha_45_1000[-1]))
    dalpha_90_1000.append(abs(alpha_90_1000[0] - alpha_90_1000[-1]))
    dalpha_sa_1000.append(abs(alpha_sa_1000[0] - alpha_sa_1000[-1]))
    dalpha_45_1000.append(abs(alpha_45_1000[0] - alpha_45_1000[-1]))
    dalpha_90_1000.append(abs(alpha_90_1000[0] - alpha_90_1000[-1]))

    dalpha_sa_1700.append(abs(alpha_sa_1700[0] - alpha_sa_1700[-1]))
    dalpha_45_1700.append(abs(alpha_45_1700[0] - alpha_45_1700[-1]))
    dalpha_90_1700.append(abs(alpha_90_1700[0] - alpha_90_1700[-1]))
    dalpha_sa_1700.append(abs(alpha_sa_1700[0] - alpha_sa_1700[-1]))
    dalpha_45_1700.append(abs(alpha_45_1700[0] - alpha_45_1700[-1]))
    dalpha_90_1700.append(abs(alpha_90_1700[0] - alpha_90_1700[-1]))



print(f"media_sa_1000 = {np.mean(dalpha_sa_1000)}")
print(f"media_45_1000 = {np.mean(dalpha_45_1000)}")
print(f"media_90_1000 = {np.mean(dalpha_90_1000)}")
print(f"media_sa_1700 = {np.mean(dalpha_sa_1700)}")
print(f"media_45_1700 = {np.mean(dalpha_45_1700)}")
print(f"media_90_1700 = {np.mean(dalpha_90_1700)}")

plt.hist(dalpha_sa_1000, bins=30, edgecolor='black', label = 'saudavel')
plt.hist(dalpha_45_1000, bins=30, edgecolor='black', label = '45cm')
plt.hist(dalpha_90_1000, bins=30, edgecolor='black', label = '90cm')
plt.legend(loc='best')
plt.savefig("f1000.png")
plt.show()

plt.hist(dalpha_sa_1700, bins=30, edgecolor='black', label = 'saudavel')
plt.hist(dalpha_45_1700, bins=30, edgecolor='black', label = '45cm')
plt.hist(dalpha_90_1700, bins=30, edgecolor='black', label = '90cm')
plt.legend(loc='best')
plt.savefig("f1700.png")
plt.show()

#print(f"saudavel: Δα = {abs(alfa_su[0] - alfa_su[-1])}")
#print(f"45cm: Δα = {abs(alfa_45[0] - alfa_45[-1])}")
#print(f"90cm: Δα = {abs(alfa_90[0] - alfa_90[-1])}")

