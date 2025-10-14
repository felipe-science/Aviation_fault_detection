import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt




def func_reta(x,a,b):
    return a*x+b

# Ajuste de curvas
def ajuste_curva(xd, yd):
    
    param,pcov = curve_fit(func_reta,xd,yd)

    a = param[0]
    b = param[1]

    
    '''
    pontosx = linspace(xd[0],xd[-1],1000)
    pontosy = []
    for x in pontosx:
        pontosy.append(func_reta(x,a,b))

    scatter(xd,yd, color='green')
    plot(pontosx,pontosy, color = 'black', linestyle = 'dashed', label=f"df={round(a,2)}")
    title("Dimensão Fractal - Curva de Condutância", fontsize='16')
    xlabel("log(1/l)", fontsize='15')
    ylabel("log(N)", fontsize='15')
    tick_params(labelsize='12')
    legend(loc='best', fontsize=16)
    savefig("fig_saud_1000rpm.png")
    show()

    print("\nDimensao Fractal = ",a)
    '''

    return a, b


def median_std(diretorio):

    files_dat = [f for f in os.listdir(diretorio) if f.endswith(".dat")]
    N = len(files_dat)

    values_a = np.zeros([N])
    for i in range(N):

        data = np.loadtxt(f"{diretorio}/{files_dat[i]}")
        xdata = data[:,0]
        ydata = data[:,1]

        a, b = ajuste_curva(xdata, ydata)
        values_a[i] = a

    media = np.median(values_a)
    desvi = np.std(values_a)

    return media, desvi

dire1 = "DADOS_BC_saud_1000rpm"
dire2 = "DADOS_BC_45cm_1000rpm"
dire3 = "DADOS_BC_90cm_1000rpm"
dire4 = "DADOS_BC_saud_1700rpm"
dire5 = "DADOS_BC_45cm_1700rpm"
dire6 = "DADOS_BC_90cm_1700rpm"


dados1, std1 = median_std(dire1)
dados2, std2 = median_std(dire2)
dados3, std3 = median_std(dire3)
dados4, std4 = median_std(dire4)
dados5, std5 = median_std(dire5)
dados6, std6 = median_std(dire6)


plt.hist(dados1, bins=100, edgecolor='black', alpha=0.5)
plt.hist(dados2, bins=100, edgecolor='black', alpha=0.5)
plt.hist(dados3, bins=100, edgecolor='black', alpha=0.5)
plt.hist(dados4, bins=100, edgecolor='black', alpha=0.5)
plt.hist(dados5, bins=100, edgecolor='black', alpha=0.5)
plt.hist(dados6, bins=100, edgecolor='black', alpha=0.5)

plt.xlim(1.44,1.48)

# Adicionar título e rótulos
plt.title("Histograma dos Dados")
plt.xlabel("Valor")
plt.ylabel("Frequência")

# Mostrar o gráfico
plt.show()


print(f"saud_1000: {np.mean(dados1)}    {std1}")
print(f"45cm_1000: {np.mean(dados2)}")
print(f"90cm_1000: {np.mean(dados3)}")

print(f"saud_1700: {np.mean(dados4)}")
print(f"45cm_1700: {np.mean(dados5)}")
print(f"90cm_1700: {np.mean(dados6)}")