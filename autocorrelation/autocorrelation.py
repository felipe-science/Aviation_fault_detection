import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots


def autocorrelation(signal):
    signal_mean = signal - np.mean(signal)
    correlation = np.correlate(signal_mean, signal_mean, mode='full')
    correlation = correlation[correlation.size // 2:]  # mantém só parte positiva
    correlation /= correlation[0]  # normaliza: valor máximo = 1
    return correlation


def fatiamento(path, Nslice):

    data = np.loadtxt(path, float)
    
    time = np.linspace(0,Nslice/30,Nslice)

    Npoints = len(data)
    N_files = Npoints // Nslice

    signals = np.zeros((N_files, Nslice))
    data_trimmed = data[:N_files * Nslice] # corta os 16 extras
    signals = data_trimmed.reshape((N_files, Nslice))

    return time, signals



path_45cm_1000rpm = "../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rmp = "../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../data/saudavel/Saud2200.txt"


time, signals_45cm_1000 = fatiamento(path_45cm_1000rpm, 200)
time, signals_45cm_1700 = fatiamento(path_45cm_1700rpm, 200)

time, signals_90cm_1000 = fatiamento(path_90cm_1000rpm, 200)
time, signals_90cm_1700 = fatiamento(path_90cm_1700rpm, 200)
time, signals_90cm_2200 = fatiamento(path_90cm_2200rpm, 200)

time, signals_saud1000 = fatiamento(path_saudavel1000rmp, 200)
time, signals_saud1700 = fatiamento(path_saudavel1000rmp, 200)
time, signals_saud2200 = fatiamento(path_saudavel1000rmp, 200)


plt.style.use(['science'])
plt.figure(figsize=(8,6))

plt.plot(time, signals_45cm_1000[0], label = '45cm - 1000 rpm')
plt.plot(time, signals_90cm_1000[0], label = '90cm - 1000 rpm')
plt.plot(time, signals_saud1000[0], label = 'Saudavel - 1000 rpm')
plt.xlabel("time (s)", fontsize=25)
plt.ylabel("Signal", fontsize=25)
plt.tick_params(axis='both', labelsize=20)
plt.legend(loc='best', fontsize=20)
plt.savefig("fig1000rpm.png", dpi=300)
plt.show()

plt.style.use(['science'])
plt.figure(figsize=(8,6))

plt.plot(time, signals_45cm_1700[0], label = '45cm - 1700 rpm')
plt.plot(time, signals_90cm_1700[0], label = '90cm - 1700 rpm')
plt.plot(time, signals_saud1700[0], label = 'Saudavel - 1700 rpm')
plt.xlabel("time (s)", fontsize=25)
plt.ylabel("Signal", fontsize=25)
plt.tick_params(axis='both', labelsize=20)
plt.legend(loc='best', fontsize=20)
plt.savefig("fig1700rpm.png", dpi=300)
plt.show()
