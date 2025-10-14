import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("DADOS_BC_45cm_1000rpm/DADOS_BC_0.dat")
plt.scatter(data[:,0], data[:,1])
plt.show()