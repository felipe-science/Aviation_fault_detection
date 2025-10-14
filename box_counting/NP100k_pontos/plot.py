import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(8, 8))
data = np.loadtxt("file_45_1000/data_0.dat")
plt.plot(data[:,0], data[:,1])
plt.show()