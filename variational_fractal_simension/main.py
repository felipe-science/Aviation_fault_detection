import numpy as np
import matplotlib.pyplot as plt


path_45cm_1000rpm = "../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rmp = "../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../data/saudavel/Saud2200.txt"


path_file = [path_45cm_1000rpm, path_45cm_1700rpm, path_90cm_1000rpm, path_90cm_1700rpm, path_90cm_2200rpm, path_saudavel1000rmp, path_saudavel1700rpm, path_saudavel2200rpm]
name_file = ['f45cm_1000rpm', 'f45cm_1700rpm', 'f90cm_1000rpm', 'f90cm_1700rpm', 'f90cm_2200rpm', 'saud_1000rpm', 'saud_1700rpm', 'saud_2200rpm']


def variation_method(path):
    x = np.loadtxt(path, float)
    x = (x - np.mean(x)) / np.std(x)
    x = x[0:1000]
    N = len(x)
    delta = [1, 2, 3, 5, 8, 12, 20, 33, 54, 90, 150]
    varia = [np.mean(np.abs(x[d:] - x[:-d])) for d in delta]
    return delta, varia



k = 3
path = path_file[k]
name = name_file[k]


delta, varia = variation_method(path)

logd = np.log(delta)
logV = np.log(varia)

coeffs = np.polyfit(logd, logV, 1)
H = coeffs[0]
D = 2 - H
print(f"H = {H:.3f}, Dimensão fractal D = {D:.3f}     name = {name}")


plt.scatter(logd, logV)
plt.plot(logd, logV)
plt.show()



print(varia)