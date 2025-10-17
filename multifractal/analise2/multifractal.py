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
    data = data[30000:-30000]
    
    time = np.linspace(0,Nslice/30,Nslice)

    Npoints = len(data)
    N_files = Npoints // Nslice

    signals = np.zeros((N_files, Nslice))
    data_trimmed = data[:N_files * Nslice] # corta os 16 extras
    signals = data_trimmed.reshape((N_files, Nslice))

    return time, signals



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

    return tau, alpha, f_alp, A, hq


def graf2(q_list, s_list, A, hq, tau, alpha, f_alp):

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    fig.suptitle('Monofractal', fontsize=25)

    for i in range(len(q_list)):

        log_x = np.log(s_list)
        log_y = np.log(A[:,i])
        ax[0,0].scatter(log_x, log_y, marker='.', label = f'q = {q_list[i]}')    
        ax[0,0].plot(log_x, log_y)
    ax[0,0].set_xlabel(r'$ln(s)$', fontsize='16')
    ax[0,0].set_ylabel(r'$F(q,s)$', fontsize='16')
    #ax[0,0].legend(loc='best')


    ax[0,1].scatter(q_list, hq, color='blue')
    ax[0,1].set_xlabel(r'$q$', fontsize='16')
    ax[0,1].set_ylabel(r'$h(q)$', fontsize='16')
    

    ax[1,0].scatter(q_list, tau, color='red')
    ax[1,0].set_xlabel(r'$q$', fontsize='16')
    ax[1,0].set_ylabel(r'$\tau(q)$', fontsize='16')

    ax[1,1].scatter(alpha, f_alp, color='green')
    ax[1,1].set_xlabel(r'$\alpha$', fontsize='16')
    ax[1,1].set_ylabel(r'$f(\alpha)$', fontsize='16')
    
    plt.savefig('fig2.png', dpi=300)
    plt.show()


frequency = 1000

path_45cm = f"../../data/desbalanceamento_45cm/F5-{frequency}.txt"
path_90cm = f"../../data/desbalanceamento_90cm/F6-{frequency}.txt"
path_saud = f"../../data/saudavel/Saud{frequency}.txt"


Nslice = 2000
theta = 1
q_list = np.linspace(-10,10,21)
s_list = np.array([4, 6, 8, 10, 12, 14, 16, 18, 20])

N = Nslice

list_path = [path_45cm, path_90cm, path_saud]
for k in range(3):

    path = list_path[k]
    time, signals = fatiamento(path, Nslice)
    N_signals = len(signals)
    N_signals = 100

    for j in range(N_signals):
        sig = signals[j]
        tau, alpha, f_alpha, A, hq = run_mfdfa(q_list, s_list, theta, sig)

        match k:
            case 0:
                np.savetxt(f"alpha_sa_{j}.dat", np.column_stack((alpha, f_alpha)))
                np.savetxt(f"q_hq_sa_{j}.dat", np.column_stack((q_list, hq)))
                shutil.move(f"alpha_sa_{j}.dat", f"f{frequency}rpm/alpha_sa_{j}.dat")
                shutil.move(f"q_hq_sa_{j}.dat", f"f{frequency}rpm/q_hq_sa_{j}.dat")
            case 1:
                np.savetxt(f"alpha_45_{j}.dat", np.column_stack((alpha, f_alpha)))
                np.savetxt(f"q_hq_45_{j}.dat", np.column_stack((q_list, hq)))
                shutil.move(f"alpha_45_{j}.dat", f"f{frequency}rpm/alpha_45_{j}.dat")
                shutil.move(f"q_hq_45_{j}.dat", f"f{frequency}rpm/q_hq_45_{j}.dat")
            case 2:
                np.savetxt(f"alpha_90_{j}.dat", np.column_stack((alpha, f_alpha)))
                np.savetxt(f"q_hq_90_{j}.dat", np.column_stack((q_list, hq)))
                shutil.move(f"alpha_90_{j}.dat", f"f{frequency}rpm/alpha_90_{j}.dat")
                shutil.move(f"q_hq_90_{j}.dat", f"f{frequency}rpm/q_hq_90_{j}.dat")


    print("Processando...")

graf2(q_list, s_list, A, hq, tau, alpha, f_alpha)