import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j0, j1, jn_zeros

## ----------------------------------------------------
## Eingaben
## ----------------------------------------------------
#dpdx = -0.008#-8.0e-3      # Druckgradient [Pa/m] (negativ => Flow in +x)
#rho  = 1000.0       # Dichte [kg/m^3]
#mu   = 1.0    # dyn. Viskosität [Pa·s]
#nu   = 1.0e-3      # kin. Viskosität [m^2/s]
#R    = 0.03       # Radius (halbe Breite) [m]
#t    = 3  # Transiente Zeit [s]

#dpdx = -0.1#-8.0e-3      # Druckgradient [Pa/m] (negativ => Flow in +x)
#rho  = 1000.0       # Dichte [kg/m^3]
#mu   = 1.0    # dyn. Viskosität [Pa·s]
#nu   = 1.0e-3     # kin. Viskosität [m^2/s]
#R    = 0.04       # Radius (halbe Breite) [m]
#t    = 1    # Transiente Zeit [s]
#

##Sergio
##19.12.25 - habe hier nu statt mu bei umax 
#dpdx = -1e-4#-8.0e-3      # Druckgradient [Pa/m] (negativ => Flow in +x)
#rho  = 1000.0       # Dichte [kg/m^3]
#mu   = 1e-1   # dyn. Viskosität [Pa·s]
#nu   = 1e-4    # kin. Viskosität [m^2/s]
#R    = 0.05      # Radius (halbe Breite) [m]
#t    = 1.2   # Transiente Zeit [s]
#
#
#BigExample
#19.12.25 - habe hier nu statt mu bei umax 
dpdx = -1e-4#-8.0e-3      # Druckgradient [Pa/m] (negativ => Flow in +x)
rho  = 1000.0       # Dichte [kg/m^3]
mu   = 1e-1   # dyn. Viskosität [Pa·s]
nu   = 1e-4    # kin. Viskosität [m^2/s]
R    = 0.05      # Radius (halbe Breite) [m]
t    = 1 # Transiente Zeit [s]

#BigExample
#Versuche mit Schallgeschwindigkeit c
dpdx = -6e-3#-8.0e-3      # Druckgradient [Pa/m] (negativ => Flow in +x)
rho  = 1000.0       # Dichte [kg/m^3]
mu   = 1e-1   # dyn. Viskosität [Pa·s]
nu   = 1e-4    # kin. Viskosität [m^2/s]
R    = 0.05      # Radius (halbe Breite) [m]
t    = 10 # Transiente Zeit [s]
# ----------------------------------------------------
# Hilfsgrößen
# ----------------------------------------------------
# maximale stationäre Geschwindigkeit (Poiseuille)
u_max = - (R**2 / (4.0 * nu)) * dpdx    # [m/s]

print(f"u_max (stationär) = {u_max:.6e} m/s")

# ----------------------------------------------------
# transiente Lösung als Funktion
# ----------------------------------------------------
def u_transient(r, t, dpdx, mu, rho, R, n_terms=50):
    """
    Transientes Poiseuille-Profil im Rohr:
    u(r,t) = u_max * [ (1 - (r/R)^2) - Sum_k 8/(λ_k^3 J1(λ_k)) J0(λ_k r/R) exp(-λ_k^2 nu t / R^2) ]
    λ_k ... Nullstellen von J0
    """
    nu = mu / rho
    u_max = - (R**2 / (4.0 * nu)) * dpdx

    # Nullstellen von J0: λ_k
    lambdas = jn_zeros(0, n_terms)  # 0. Ordnung, erste n_terms Nullstellen

    # Summe über Bessel-Moden
    r_over_R = r / R
    sum_terms = np.zeros_like(r, dtype=float)

    for lam in lambdas:
        coeff = 8.0 / (lam**3 * j1(lam))
        sum_terms += coeff * j0(lam * r_over_R) * np.exp(-lam**2 * nu * t / R**2)

    u = u_max * ((1.0 - r_over_R**2) - sum_terms)
    return u

# ----------------------------------------------------
# Profil für dein t = 0.1 s berechnen
# ----------------------------------------------------
r = np.linspace(-R, R, 200)                 # Radius von Zentrum bis Wand
u_t = u_transient(r, t, dpdx, mu, rho, R)    # transient
u_steady = u_max * (1.0 - (r/R)**2)          # stationär

# ----------------------------------------------------
# Plot
# ----------------------------------------------------
plt.figure()
plt.plot(r, u_steady, label="stationary", linestyle="--")
plt.plot(r, u_t, label=f"transient t={t} s")
plt.xlabel("r [m]")
plt.ylabel("u(r,t) [m/s]")
plt.title("Transient Poiseuille profile in the pipe")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------------------------------------
# ANALYTISCHE CSV ERZEUGEN IM EXACTEN MEASURETOOL-FORMAT
# ----------------------------------------------------

# Die 13 X-Werte exakt wie in deiner Datei:
x = np.array([0.13, 0.125, 0.12, 0.115, 0.11, 0.105,
              0.10, 0.095, 0.09, 0.085, 0.08, 0.075, 0.07])
x = np.array([0.13, 0.127273, 0.124545, 0.121818, 0.119091, 0.116364,
              0.113636, 0.110909, 0.108182, 0.105455, 0.102727, 0.100000, 0.097273, 0.094545, 0.091818, 0.089091, 0.086364, 0.083636, 0.080909, 0.078182, 0.075455, 0.072727, 0.070000])

x = np.array([-0.055,-0.05,-0.045,-0.04,-0.035,-0.03,-0.025,-0.02,-0.015,-0.01,-0.005,0,0.005,0.01,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055])

x = np.array([-0.05,-0.0454545,-0.0409091,-0.0363636,-0.0318182,-0.0272727,-0.0227273,-0.0181818,-0.0136364,-0.0090909,-0.0045455,0,0.0045455,0.0090909,0.0136364,0.0181818,0.0227273,0.0272727,0.0318182,0.0363636,0.0409091,0.0454545,0.05])

# Konstant:
y = np.full_like(x, 0.1)
z = np.full_like(x, 0.2)

# Radiale Entfernung r = |x - center|
# Wenn dein Rohrmittelpunkt bei 0 liegt:
r = np.abs(x - 0.10)  # <--- falls Mitte nicht 0 ist: bitte anpassen
r = np.abs(x)  # <--- falls Mitte nicht 0 ist: bitte anpassen

# Transiente Geschwindigkeiten:
u_t = u_transient(r, t, dpdx, mu, rho, R)

# ----------------------------------------------------
# Schreiben der Datei
# ----------------------------------------------------
with open(f"AnalyticalTransientProfile_t_{t}sekundeFinalRe<<_SmallerMessDPRes.csv", "w") as f:

    # 1) Position-Zeilen
    f.write(" ;PosX [m]:;" + ";".join(f"{v:.6f}" for v in x) + "\n")
    f.write(" ;PosY [m]:;" + ";".join(f"{v:.6f}" for v in y) + "\n")
    f.write(" ;PosZ [m]:;" + ";".join(f"{v:.6f}" for v in z) + "\n")

    # 2) Header für die Zeitreihe
    header = "Part;Time [s];" + ";".join([f"Vel.z_{i}" for i in range(len(x))])
    f.write(header + "\n")

    # 3) Datenzeile (Part = 0, Time = t)
    row = f"{int(t*100)};{t};" + ";".join(f"{v:.16e}" for v in u_t)
    f.write(row + "\n")
