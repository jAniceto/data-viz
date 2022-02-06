# Imports
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


# Configuration
plt.style.use(['science','no-latex'])


# Load data
T_Pvap = np.loadtxt('propane-vapor-pressure.txt')
temp = T_Pvap[:,0]  # ºF
pvap = T_Pvap[:,1]  # psia

# Unit conversion
temp = (temp-32)/1.8  # ºC
pvap = pvap/14.69595*760  # mmHg

# Plot experimental data
fig1, ax1 = plt.subplots()
ax1.plot(temp, pvap, 'bo', label='Experimental')
plt.xlabel('Temperature (ºC)')
plt.ylabel('Vapor Pressure (mmHg)')
plt.savefig('opt-data.png', dpi=300, bbox_inches='tight')

# Define the system of 3 equations and solve it using scipy.optimize.fsolve
def equations(p):
    A, B, C = p
    eq1 = np.log10(pvap[0])+B/(C+temp[0])-A
    eq2 = (A-np.log10(pvap[1]))*(C+temp[1])-B
    eq3 = B/(A-np.log10(pvap[2]))-temp[2]-C
    return eq1, eq2, eq3

A, B, C = optimize.fsolve(equations, (5, 600, 200))

ABC0 = np.array([A, B, C])

# Define the objective function
def fobj(ABC):
    pvap_calc = 10**(ABC[0]-ABC[1]/(ABC[2]+temp))
    f = np.sum((pvap_calc-pvap)**2)
    return f

# Run optimization to determine parameters A, B and C
ABC = optimize.fmin(fobj, ABC0)
pvap_final = 10**(ABC[0]-ABC[1]/(ABC[2]+temp))

print('\nOptimized Antoine Constants:\nA = %.3f\nB = %.3f\nC = %.3f' % (ABC[0], ABC[1], ABC[2]))

# Display results graphicaly
fig2, ax2 = plt.subplots()
ax2.plot(temp, pvap, 'bo', label='Experimental')
ax2.plot(temp, pvap_final, 'r-', label='Calculated')
plt.xlabel('Temperature (ºC)')
plt.ylabel('Vapor Pressure (mmHg)')
legend = ax2.legend(loc='upper left')
plt.savefig('opt-fitting.png', dpi=300, bbox_inches='tight')
