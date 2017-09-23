from sympy import * 
from mdof import *

M = 25
R = 0.050
m = 10
k_A = 1000
k_B = 2500
k_C = 1000

# Set physical properties
M = Matrix([[m, 0], [0, 3 * M * R ** 2 / 2]])
K = Matrix([[k_A + k_B , -k_B * R], [-k_B * R , (k_B + k_C) * R **2]])

this = MDOF_System(M=M, K=K, normalize=True)

M_t = symbols('M_E')

this.F = Matrix([0, M_t])

this.doEigenAnalysis()