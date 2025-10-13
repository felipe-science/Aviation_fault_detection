import numpy as np
import matplotlib.pyplot as plt
import shutil

path_45cm_1000rpm = "../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rmp = "../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../data/saudavel/Saud2200.txt"


def fatiamento(path, Nslice):

    data = np.loadtxt(path, float)
    
    time = np.linspace(0,Nslice/30,Nslice)

    Npoints = len(data)
    N_files = Npoints // Nslice

    signals = np.zeros((N_files, Nslice))
    data_trimmed = data[:N_files * Nslice] # corta os 16 extras
    signals = data_trimmed.reshape((N_files, Nslice))

    return time, signals


Nslice = 100000

time, signals = fatiamento(path_saudavel2200rpm, Nslice)
time = time/666

for k in range(len(signals)):

    f = open(f"data_{k}.dat", "w")
    sig = signals[-1]+2
    for i in range(len(time)):
        f.write(f"{time[i]} {sig[i]}\n")
    f.close()

    shutil.move(f"data_{k}.dat", f"file_sa_2200/data_{k}.dat")

    #plt.plot(time, sig)
    #plt.show()