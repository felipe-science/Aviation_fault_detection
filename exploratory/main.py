import numpy as np
import matplotlib.pyplot as plt

data_desbalanceamento45 = np.loadtxt("../data/desbalanceamento_45cm/F5-1000.txt")


plt.plot(data_desbalanceamento45)
plt.show()