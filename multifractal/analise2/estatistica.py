import numpy as np
import matplotlib.pyplot as plt

Nfile = 100
frequency = 1000
prefix = f"f{frequency}rpm"

# Labels das condições
condicoes = ["sa", "45", "90"]

# Inicializar dicionários para armazenar médias
media_q = {c: np.zeros(21) for c in condicoes}
media_h = {c: np.zeros(21) for c in condicoes}
media_a = {c: np.zeros(21) for c in condicoes}
media_f = {c: np.zeros(21) for c in condicoes}

for i in range(Nfile):
    for c in condicoes:
        # Carregar arquivos
        data_hq = np.loadtxt(f"{prefix}/q_hq_{c}_{i}.dat")
        data_af = np.loadtxt(f"{prefix}/alpha_{c}_{i}.dat")

        # Somar valores (usando soma vetorizada)
        media_q[c] += data_hq[:, 0]
        media_h[c] += data_hq[:, 1]
        media_a[c] += data_af[:, 0]
        media_f[c] += data_af[:, 1]

# Calcular média final
for c in condicoes:
    media_q[c] /= Nfile
    media_h[c] /= Nfile
    media_a[c] /= Nfile
    media_f[c] /= Nfile

# Cores e rótulos para o gráfico
rotulos = {"sa": "saudável", "45": "45 cm", "90": "90 cm"}
cores = {"sa": "tab:blue", "45": "tab:orange", "90": "tab:green"}

# --- Plot 1: f(α)
plt.figure()
for c in condicoes:
    plt.plot(media_a[c], media_f[c], label=rotulos[c], color=cores[c])
    plt.scatter(media_a[c], media_f[c], color=cores[c], s=20)
plt.legend()
plt.xlabel(r"mean($\alpha$)")
plt.ylabel(r"mean($f$)")
plt.title("Curva multifractal média")
plt.show()

# --- Plot 2: h(q)
plt.figure()
for c in condicoes:
    plt.plot(media_q[c], media_h[c], label=rotulos[c], color=cores[c])
    plt.scatter(media_q[c], media_h[c], color=cores[c], s=20)
plt.legend()
plt.xlabel(r"mean($q$)")
plt.ylabel(r"mean($h$)")
plt.title("Espectro de Hurst médio")
plt.show()
