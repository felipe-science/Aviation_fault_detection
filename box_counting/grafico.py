import os
from numpy import loadtxt, linspace
from pylab import scatter, plot, show, title, xlabel, ylabel, tick_params, legend, savefig, grid
from scipy.optimize import curve_fit

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

diretorio = "DADOS_BC_saud_2200rpm"

files_dat = [f for f in os.listdir(diretorio) if f.endswith(".dat")]


media_a = 0.0
for i in range(len(files_dat)):

    data = loadtxt(f"{diretorio}/{files_dat[i]}")
    xdata = data[:,0]
    ydata = data[:,1]

    a, b = ajuste_curva(xdata, ydata)
    media_a+=a

print(media_a/len(files_dat))