import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters
# -----------------------------
L   = 0.01        # m
TL  = 363.0       # K  left wall
TR  = 363.0       # K  right wall (set different if you want)
T0  = 293.0       # K  initial fluid

k   = 0.6         # W/(m K)
rho = 1000.0      # kg/m^3
cp  = 4182.0      # J/(kg K)
alpha = k/(rho*cp)

N_terms = 300

def T_two_walls(x, t):
    """Heat equation with T(0,t)=TL, T(L,t)=TR, and uniform initial T0."""
    # steady linear profile
    Ts = TL + (TR - TL) * (x / L)

    if t == 0:
        return T0 * np.ones_like(x)

    s = 0.0
    for n in range(1, N_terms + 1):
        # closed-form coefficient for uniform initial T0
        Bn = (2.0/(n*np.pi)) * (
            (T0 - TL) * (1.0 - (-1.0)**n) + (TR - TL) * ((-1.0)**n)
        )
        lam = n * np.pi / L
        s += Bn * np.sin(lam * x) * np.exp(-alpha * lam**2 * t)

    return Ts + s

# grid + times
x = np.linspace(0, L, 400)
times = [0, 2.5, 3, 5, 7.5, 10]  # seconds

plt.figure()
for t in times:
    T = T_two_walls(x, t)
    plt.plot(x, T,  label=f"t={t}s")

plt.xlabel("x [m]")
plt.ylabel("T [K]")
plt.title("Transient temperature (two hot walls)")
plt.grid(True)
plt.legend()
plt.show()
