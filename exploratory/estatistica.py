import os
import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from scipy.signal import find_peaks


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

def max_density(time, signals):

    N_files = len(signals)
    max_density = np.zeros([N_files])
    
    for i in range(N_files):
        sig = signals[i, :]
        peaks, _ = find_peaks(sig, height=0.1)

        max_density[i] = len(peaks) / abs(time[0] - time[-1])

    return max_density

def make_graphic():
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

def make_histogram(frequency, data1, data2, data3):
    
    plt.style.use(['science'])
    plt.figure(figsize=(8,6))

    plt.hist(data1, bins=15, color='skyblue', edgecolor='black', alpha=0.5, label=f'45cm')
    plt.hist(data2, bins=15, color='salmon', edgecolor='black', alpha=0.5, label=f'90cm')
    plt.hist(data3, bins=15, color='lightgreen', edgecolor='black', alpha=0.5, label=f'Saudável')
    plt.xlabel('peaks/second', fontsize=25)
    plt.ylabel('Frequency', fontsize=25)
    plt.title(f'{frequency} rpm', fontsize=30)
    plt.legend(loc='upper left', fontsize=20)
    plt.tick_params(axis='both', labelsize=20)
    plt.savefig(f"his_{frequency}rmp.png", dpi=300)
    #plt.show()


path_45cm_1000rpm = "../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rmp = "../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../data/saudavel/Saud2200.txt"


Nslice = 20000

time, signals_45cm_1000 = fatiamento(path_45cm_1000rpm, Nslice)
time, signals_45cm_1700 = fatiamento(path_45cm_1700rpm, Nslice)

time, signals_90cm_1000 = fatiamento(path_90cm_1000rpm, Nslice)
time, signals_90cm_1700 = fatiamento(path_90cm_1700rpm, Nslice)
time, signals_90cm_2200 = fatiamento(path_90cm_2200rpm, Nslice)

time, signals_saud1000 = fatiamento(path_saudavel1000rmp, Nslice)
time, signals_saud1700 = fatiamento(path_saudavel1000rmp, Nslice)
time, signals_saud2200 = fatiamento(path_saudavel1000rmp, Nslice)

md_45cm_1000 = max_density(time, signals_45cm_1000)
md_90cm_1000 = max_density(time, signals_90cm_1000)
md_saud_1000 = max_density(time, signals_saud1000)

md_45cm_1700 = max_density(time, signals_45cm_1700)
md_90cm_1700 = max_density(time, signals_90cm_1700)
md_saud_1700 = max_density(time, signals_saud1700)

make_histogram(1000, md_45cm_1000, md_90cm_1000, md_saud_1000)
make_histogram(1700, md_45cm_1700, md_90cm_1700, md_saud_1700)

make_graphic()


