import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. Gerar um sinal sintético (exemplo)
# ==========================================

# Defina o número de pontos
N = 5000

# Gerar um sinal fractal simples: ruído browniano (integral do ruído branco)
# O ruído browniano tem dimensão fractal teórica D = 1.5
np.random.seed(42)
x = np.cumsum(np.random.randn(N))  # Caminhada aleatória

# ==========================================
# 2. Método da Variabilidade
# ==========================================

def variation_method(x):
    N = len(x)
    delta = [1, 2, 3, 5, 8, 12, 20, 33, 54, 90, 150]
    varia = [np.mean(np.abs(x[d:] - x[:-d])) for d in delta]
    return np.array(delta), np.array(varia)

# Calcular V(delta)
delta, varia = variation_method(x)

# ==========================================
# 3. Ajuste linear em escala log-log
# ==========================================

logd = np.log(delta)
logV = np.log(varia)

# Ajuste linear
coeffs = np.polyfit(logd, logV, 1)
H = coeffs[0]
D = 2 - H

print(f"H = {H:.3f}, Dimensão fractal D = {D:.3f}")

# ==========================================
# 4. Plotar resultados
# ==========================================

plt.figure(figsize=(7,5))

plt.loglog(delta, varia, 'o-', label='V(δ) experimental')
plt.loglog(delta, np.exp(coeffs[1]) * delta**H, '--', label=f"ajuste linear (H={H:.2f})")

plt.xlabel("δ (escala)")
plt.ylabel("V(δ)")
plt.title("Método da Variabilidade - Sinal Sintético")
plt.legend()
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.tight_layout()
plt.show()


print(varia)