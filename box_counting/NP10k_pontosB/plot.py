import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("file_45_1000/data_100.dat")
plt.plot(data[:,0], data[:,1])
plt.show()