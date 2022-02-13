# Imports
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


# Configuration
plt.style.use(['science','no-latex'])


# Data
k1 = k2 = k3 = 1  # min-1, kinetic constants
k1_ = k3_ = 2  # min-1, kinetic constants
CA0 = CD0 = 1  # mol/dm3, initial concentrations
CB0 = CC0 = 0  # mol/dm3, initial concentrations
tfinal = 20  # min, final integration time

# Define the system of ordinary differential equations (sode)
def sode(t, y):
    return [
        -k1*y[0] + k1_*y[1],
        k1*y[0] - k1_*y[1] - k2*y[1],
        k2*y[1] - k3*y[2] + k3_*y[3],
        k3*y[2] - k3_*y[3]
    ]

# Solve the sedo using scipy.integrate.solve_ivp
tspan = [0, tfinal]  # integration interval
y0 = [CA0, CB0, CC0, CD0]  # initial state (initial concentrations)
sol = integrate.solve_ivp(sode, tspan, y0, dense_output=True)

t = np.linspace(0, tfinal, 1000)
C = sol.sol(t)

# Display results graphically
fig1, ax1 = plt.subplots()
ax1.plot(t, C.T)
plt.ylim(bottom=0)
plt.xlim(left=0)
plt.xlabel('$t$ ($\mathrm{min}$)')
plt.ylabel('$C_i$ ($\mathrm{mol \ dm^{-3}}$)')
plt.legend(['$C_A$', '$C_B$', '$C_C$', '$C_D$']);
plt.savefig('de-system-odes.png', dpi=300, bbox_inches='tight')
