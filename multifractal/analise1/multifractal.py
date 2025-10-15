import math
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
import shutil


def moving_average(y, s, theta):
    N = len(y)
    y_moving_avg = np.zeros(N)
    past = int(np.floor((s - 1) * theta))
    future = int(np.ceil((s - 1) * (1 - theta)))
    
    for t in range(N):
        start = max(0, t - past)
        end = min(N, t + future + 1)
        y_moving_avg[t] = np.mean(y[start:end])
    
    return y_moving_avg

def detrend(y, y_moving_average):
    return y - y_moving_average

def rms(epsilon, s):
   
    N = len(epsilon)
    Ns = math.floor(N/s - 1)
   
    Fv_s = []
    for vi in range(Ns):
        v = vi+1
        l = (v-1)*s

        ini = l
        fin = s+l
        ev = epsilon[ini:fin]
        r_m_s = rms = np.sqrt(np.mean(ev ** 2))
        Fv_s.append(r_m_s)    
    return Fv_s

def calculate_fluctuation(Fv, q, s):

    Fv = np.array(Fv)
    
    Ns = max(0, math.floor((N / s) - 1)) 
    if(q != 0):
        return (np.mean(Fv**q))**(1/q)
    else:
        return np.exp(np.mean(np.log(Fv)))


def create_matrix(q_list, s_list, theta, y):


    Fs = [] # F para cada s, dentro tem os F(q)
    for s in s_list:

        y_moving_average = moving_average(y, s, theta)
        epsilon = detrend(y, y_moving_average)
        Fvs = rms(epsilon, s)

        aux = []
        for q in q_list:
            Fvs = rms(epsilon, s)
            Fluc = calculate_fluctuation(Fvs, q, s)
            aux.append(Fluc)

        Fs.append(aux)

    line = len(s_list)
    colu = len(q_list)
    A = np.zeros([line, colu])
    for i in range(line):
        aux = Fs[i]
        for j in range(colu):
            A[i,j] = aux[j]
    return A




def fatiamento(path, Nslice):

    data = np.loadtxt(path, float)
    
    time = np.linspace(0,Nslice/30,Nslice)

    Npoints = len(data)
    N_files = Npoints // Nslice

    signals = np.zeros((N_files, Nslice))
    data_trimmed = data[:N_files * Nslice] # corta os 16 extras
    signals = data_trimmed.reshape((N_files, Nslice))

    return time, signals


path_45cm_1000rpm = "../../data/desbalanceamento_45cm/F5-1000.txt"
path_45cm_1700rpm = "../../data/desbalanceamento_45cm/F5-1700.txt"

path_90cm_1000rpm = "../../data/desbalanceamento_90cm/F6-1000.txt"
path_90cm_1700rpm = "../../data/desbalanceamento_90cm/F6-1700.txt"
path_90cm_2200rpm = "../../data/desbalanceamento_90cm/F6-2200.txt"

path_saudavel1000rpm = "../../data/saudavel/Saud1000.txt"
path_saudavel1700rpm = "../../data/saudavel/Saud1700.txt"
path_saudavel2200rpm = "../../data/saudavel/Saud2200.txt"




def run_mfdfa(q_list, s_list, theta, sig):

    N = len(sig)
    A = create_matrix(q_list, s_list, theta, sig)

    hq = np.zeros([len(q_list)])
    log_s = np.log(s_list)
    for i in range(len(q_list)):
        F = A[:,i]
        log_F = np.log(F)
        slope, intercept, r_value, p_value, std_err = linregress(log_s, log_F)
        hq[i] = slope


    tau = hq*q_list-1
    alpha = np.gradient(tau,q_list)
    f_alp = q_list*alpha - tau

    return tau, alpha, f_alp


Nslice = 10000
theta = 1
q_list = np.linspace(-5,5,11)
s_list = np.array([64, 128, 256, 512, 1024, 2048])

N = Nslice

list_path = [path_saudavel1700rpm, path_45cm_1700rpm, path_90cm_1700rpm]
for k in range(3):

    path = list_path[k]
    time, signals = fatiamento(path, Nslice)
    N_signals = len(signals)
    
    for j in range(N_signals):
        sig = signals[j]
        tau, alpha, f_alpha = run_mfdfa(q_list, s_list, theta, sig)

        match k:
            case 0:
                np.savetxt(f"alpha_sa_{j}.dat", np.column_stack((alpha, f_alpha)))
                shutil.move(f"alpha_sa_{j}.dat", f"f1700rpm/alpha_sa_{j}.dat")
            case 1:
                np.savetxt(f"alpha_45_{j}.dat", np.column_stack((alpha, f_alpha)))
                shutil.move(f"alpha_45_{j}.dat", f"f1700rpm/alpha_45_{j}.dat")
            case 2:
                np.savetxt(f"alpha_90_{j}.dat", np.column_stack((alpha, f_alpha)))
                shutil.move(f"alpha_90_{j}.dat", f"f1700rpm/alpha_90_{j}.dat")
