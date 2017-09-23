from sympy import * 
import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
init_printing()
from mdof import *

# g = 32.2*12
m = 2
E = 210E3 * 1000 ** 2
I_o = 22
L = 2.5
d = 0.025
k = 2000 * 1000
k_theta = 55

I = pi* d ** 4 / 64.0

# Set physical properties
M = Matrix([[m, 0], [0, I_o]])
K = Matrix([[k + 12 * I * E / L **3, -6 * E * I / L **2], [-6 * E * I / L **2, k_theta + 4 * E * I / L]])

this = MDOF_System(M=M, K=K, normalize=True)

this.doEigenAnalysis()