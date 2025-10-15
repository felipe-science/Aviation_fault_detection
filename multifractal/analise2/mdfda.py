import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def multifractal_cascade(N=1000000, levels=10, H=0.7):
   
    signal = np.ones(1)  # Começa com um único valor

    for _ in range(levels):
        # Gera pesos aleatórios baseados em uma distribuição log-normal
        w1 = np.random.lognormal(mean=H, sigma=0.2)
        w2 = np.random.lognormal(mean=H, sigma=0.2)
        
        # Normaliza os pesos para manter a soma = 1
        norm_factor = w1 + w2
        w1 /= norm_factor
        w2 /= norm_factor

        # Aplica a cascata multiplicativa
        signal = np.concatenate([w1 * signal, w2 * signal])

    # Interpola para obter um sinal de tamanho N
    time_series = np.interp(np.linspace(0, 1, N), np.linspace(0, 1, len(signal)), signal)

    return time_series

def fractional_gaussian_noise(length=10000, H=0.7):
    ruido = np.random.randn(length)
    sinal = np.cumsum(ruido)
    sinal = (sinal - np.min(sinal)) / (np.max(sinal) - np.min(sinal))
    return sinal

def monofractal_signal(length, alpha):
    
    ruido_branco = np.random.normal(0, 1, length)
    sinal = np.cumsum(ruido_branco)  
    sinal = (sinal - np.min(sinal)) / (np.max(sinal) - np.min(sinal))
    
    return sinal

def generate_multifractal_signal(n):
    # Definir parâmetros para o ruído multifractal
    hurst = 0.7  # Hurst exponent (modificar conforme necessário)
    t = np.linspace(0, 1, n)
    
    # Criar o ruído multifractal com base no expoente Hurst
    noise = np.cumsum(np.random.randn(n))  # Ruído branco
    noise = noise / np.std(noise)  # Normalizar
    
    # Transformar o sinal com uma dinâmica multifractal simples (escala multifractal)
    multifractal_signal = np.sign(noise) * np.abs(noise) ** hurst
    return multifractal_signal

def graf1(y):

    n = 10
    theta = 0

    y_mave = moving_average(y, n, theta)
    epsilon = detrend(y, y_mave)
    Fvn = rms(epsilon, n)

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    ax[0,0].plot(y, label = r'$y$', color='blue')
    ax[0,0].set_xlabel('Step', fontsize='14')
    ax[0,0].set_ylabel('Position', fontsize='14')
    ax[0,0].set_title('Signal', fontsize='18')
    ax[0,0].legend(loc='best')

    ax[0,1].plot(y, label = r'$y$', color='blue')
    ax[0,1].plot(y_mave, label = r'$\tilde{y}$', color='red')
    ax[0,1].set_xlabel('Step', fontsize='14')
    ax[0,1].set_ylabel('Position', fontsize='14')
    ax[0,1].set_title('Moving Average', fontsize='18')
    ax[0,1].legend(loc='best')

    ax[1,0].plot(y, color='blue', label = r'$y$')
    ax[1,0].plot(y_mave, color='red', label = r'$\tilde{y}$')
    ax[1,0].plot(epsilon, color='green', label = 'detrend')
    ax[1,0].set_xlabel('Step', fontsize='14')
    ax[1,0].set_ylabel('Position', fontsize='14')
    ax[1,0].set_title('Detrend', fontsize='18')
    ax[1,0].legend(loc='best')


    ax[1,1].plot(Fvn, color='blue', label = r'$y$')
    ax[1,1].set_xlabel(r'$n$', fontsize='14')
    ax[1,1].set_ylabel(r'$F_\nu(n)$', fontsize='14')
    ax[1,1].set_title('RMS', fontsize='18')
    
    plt.savefig('fig1.png', dpi=300)
    plt.show()


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
    ax[0,1].set_ylim(0,1)

    ax[1,0].scatter(q_list, tau, color='red')
    ax[1,0].set_xlabel(r'$q$', fontsize='16')
    ax[1,0].set_ylabel(r'$\tau(q)$', fontsize='16')

    ax[1,1].scatter(alpha, f_alp, color='green')
    ax[1,1].set_xlabel(r'$\alpha$', fontsize='16')
    ax[1,1].set_ylabel(r'$f(\alpha)$', fontsize='16')
    ax[1,1].set_xlim(0,1)
    ax[1,1].set_ylim(0.5,1.5)

    plt.savefig('fig2.png', dpi=300)
    plt.show()
    

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




def create_matrix(q_list, s_list, y):


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




#y = multifractal_cascade()
#y = monofractal_signal(length=10000, alpha=1.0)
#y = fractional_gaussian_noise()
y = np.loadtxt('brownian_serie.dat', float)
N = len(y)
theta = 1

q_list = np.linspace(-5,5,11)
s_list = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

A = create_matrix(q_list, s_list, y)

hq = []
log_s = np.log(s_list)
for i in range(len(q_list)):
    F = A[:,i]
    log_F = np.log(F)
    slope, intercept, r_value, p_value, std_err = linregress(log_s, log_F)
    hq.append(slope)


tau = hq*q_list-1
alpha = np.gradient(tau,q_list)
f_alp = q_list*alpha - tau

graf1(y)
graf2(q_list, s_list, A, hq, tau, alpha, f_alp)