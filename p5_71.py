from sympy import * 
from mdof import *

M = 50
R = 0.150
m = 150
k_A = 5500
k_B = 2000

# Set physical properties
M = Matrix([[3 * M * R ** 2 / 2, M * R], [M * R, m + M]])
K = Matrix([[k_A * R ** 2 , k_A * R], [k_A * R , k_B + k_A]])

this = MDOF_System(M=M, K=K, normalize=True)

M_t = symbols('M_E')

this.F = Matrix([M_t, 0])

this.doEigenAnalysis()