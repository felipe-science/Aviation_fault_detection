import numpy as np
import matplotlib.pyplot as plt

def variation_method(x):
    x = (x - np.mean(x)) / np.std(x)  # normalização recomendada
    delta = np.array([1,2,3,5,8,12,20,33,54,90,150])
    varia = np.array([np.mean(np.abs(x[d:] - x[:-d])) for d in delta])
    return delta, varia

# Carregar sinal real
x = np.loadtxt("../data/desbalanceamento_90cm/F6-1700.txt", float)
delta, varia = variation_method(x)

# Analisar apenas faixa mais linear (exemplo)
idx = (delta >= 3) & (delta <= 33)

logd = np.log(delta[idx])
logV = np.log(varia[idx])

coeffs = np.polyfit(logd, logV, 1)
H = coeffs[0]
D = 2 - H
print(f"H = {H:.3f}, D = {D:.3f}")

# Plot
plt.figure(figsize=(7,5))
plt.loglog(delta, varia, 'o-', label='V(delta)')
plt.loglog(delta[idx], np.exp(coeffs[1]) * delta[idx]**H, '--', label=f"Ajuste linear (H={H:.2f})")
plt.xlabel("δ")
plt.ylabel("V(δ)")
plt.legend()
plt.grid(True, which='both', ls='--')
plt.show()
