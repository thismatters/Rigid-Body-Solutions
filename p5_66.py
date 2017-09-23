from sympy import * 
from mdof import *

I_1 = 1.5E5 / 1000 **2
I_2 = 0.5E3 / 1000 **2
L = 1.25
G = 79E9
d = 0.05
D_2 = 0.175
M = 75
k_a = 2E3 * 1E3
k_b = 1.5E3 * 1E3

k_theta = pi * d ** 4 * G / (32.0 * L)

# Set physical properties
M = Matrix([[I_1, 0], [0, (I_2 + M * D_2 **2 / 4)]])
K = Matrix([[k_theta, -k_theta], [-k_theta, k_theta + (k_a + k_b) * D_2 **2 / 4]])

this = MDOF_System(M=M, K=K, normalize=True)

M_t = symbols('M(t)')

this.F = Matrix([M_t, 0])
this.doEigenAnalysis()