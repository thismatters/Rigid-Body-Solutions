from sympy import * 
import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
init_printing()
from mdof import *

# g = 32.2*12
m1 = 200
m2 = 200
r1 = 0.2 
r2 = 0.2
L = 3
G = 90E6
d = 0.075

I_1 = 0.5 * m1 * r1 ** 2
I_2 = 0.5 * m2 * r2 ** 2

k = pi * d ** 4 * G / (32 * L)

# Set physical properties
M = Matrix([[I_1, 0], [0, I_2]])
K = Matrix([[k, -k], [-k, k]])

this = MDOF_System(M=M, K=K, normalize=True)

this.doEigenAnalysis()