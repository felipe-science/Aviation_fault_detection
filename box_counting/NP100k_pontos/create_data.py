import numpy as np
import matplotlib.pyplot as plt
import shutil

path_45cm_1000rpm = "../../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rmp = "../../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../../data/saudavel/Saud2200.txt"

path_file = [path_45cm_1000rpm, path_45cm_1700rpm, path_90cm_1000rpm, path_90cm_1700rpm, path_90cm_2200rpm, path_saudavel1000rmp, path_saudavel1700rpm, path_saudavel2200rpm]
path_save = ['file_45_1000', 'file_45_1700', 'file_90_1000', 'file_90_1700', 'file_90_2200', 'file_sa_1000', 'file_sa_1700', 'file_sa_2200']

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



for i in range(len(path_file)):

    time, signals = fatiamento(path_file[i], Nslice)
    time = time/(5*666)

    print(path_file[i])

    for j in range(len(signals)):

        sig = signals[j]

        minimo = min(sig)
        sig = sig+abs(minimo)
        maximo = max(sig)
        sig = sig*(1/(abs(maximo)))


        f = open(f"file_{j}.dat", "w")
        for k in range(len(sig)):
            f.write(f"{time[k]} {sig[k]}\n")
        f.close()

        shutil.move(f"file_{j}.dat", f"{path_save[i]}/data_{j}.dat")

    #plt.plot(time, sig)
    #plt.show()