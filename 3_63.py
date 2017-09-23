from numpy import *
import numpy
from scipy.optimize import fsolve
import scipy as Sci
import scipy.linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

g = 32.2  # ft / sec^2

w_c = 5  # lb
w_b = 0.229 / 16  # oz -> lb


v_0 = 2820  # ft/sec

w_t = w_c + w_b
v_1 = v_0 * w_b / w_t

omega_n = v_1 * 12

m_t = w_t / g

k =  m_t * omega_n ** 2  # lb/ft

print 'Part c) Required stiffness k = %f [lb / ft]' % k

pos = lambda t: 1/12.0 * sin(omega_n *t) 

t_crit = 2 * pi / omega_n * (1 / 4.0)

print str(t_crit)

vel_withdamping = lambda z: v_1 * exp((-1.0) * z * omega_n * t_crit * 0.85)  * ( cos(omega_n * sqrt(1 - z**2) * t_crit * 0.85) - z / sqrt(1 - z**2) * sin(omega_n * sqrt(1 - z**2) * t_crit * 0.85))

zetavals = linspace(0,1,50, False)

times = linspace(0,0.5,100)

plt.plot(zetavals, vel_withdamping(zetavals))
# plt.plot(times, pos(times))
plt.savefig('temp.png')

zetaval = fsolve(vel_withdamping, 0.5)

print 'Part d) Required damping ratio: %f, and associated damping coefficient c = %f [lb . s / ft]' % (zetaval, (2 * zetaval * omega_n * m_t))