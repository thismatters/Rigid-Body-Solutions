from sympy import * 
import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from mdof import *

g = 9.8
m_c = 5
m_p = 1
L = 0.5
k_theta = 3.5
k = 200

I_G = m_p * L ** 2 / 12

# Set physical properties
M = Matrix([[m_c + m_p, m_p * L / 2], [m_p * L / 2, I_G + m_p * L ** 2 / 4]])
K = Matrix([[k , 0], [0 , k_theta - m_p * g * L / 2]])

this = MDOF_System(M=M, K=K, normalize=True)

this.doEigenAnalysis()