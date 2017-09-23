from sympy import * 
from mdof import *

g = 9.8
m_1 = 0.75
m_2 = 2 * m_1
L_1 = 0.5
L_2 = 2 * L_1
k_1 = 20
k_2 = 4 * k_1
k_3 = k_1
d_1 = L_1 
d_2 = 2 * L_2 / 3.0
d_3 = L_2

I_O1 = m_1 * L_1 **2 / 3
I_O2 = m_2 * L_2 **2 / 3

# k_theta = pi * d ** 4 * G / (32.0 * L)

# Set physical properties
M = Matrix([[I_O1, 0], [0, I_O2]])
K = Matrix([[m_1 * g * L_1 / 2 + (k_1 + k_2) * d_1 **2, -k_2 * d_1 * d_2], [-k_2 * d_1 * d_2, k_3 * d_3 ** 2 + m_2 * g * L_2 / 2 + d_2 **2 * k_2]])

this = MDOF_System(M=M, K=K, normalize=True)

this.doEigenAnalysis()