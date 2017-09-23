from sympy import * 
from mdof import *


M_1 = 100  # kg
M_2 = 50
M_3 = 25
M_4 = 250

# r_1 = R_1  # meter
r_1 = 0.2  # meter
r_2 = 0.15
r_3 = 0.075
r_4 = 0.2

L_1 = 3  # meter
L_2 = 1.5

d_1 = 0.05  # meter
d_2 = 0.075

G = 80E9
G_1 = G
G_2 = G

k_theta1 = pi * d_1 ** 4 * G_1 / (32.0 * L_1)
k_theta2 = pi * d_2 ** 4 * G_2 / (32.0 * L_2)

I_1 = M_1 * r_1 ** 2 / 2
I_2 = M_2 * r_2 ** 2 / 2
I_3 = M_3 * r_3 ** 2 / 2
I_4 = M_4 * r_4 ** 2 / 2

M = Matrix([[I_1, 0, 0], [0, I_2 * (r_3 / r_2) ** 2 + I_3, 0], [0, 0, I_4]])
K = Matrix([[k_theta1, -k_theta1 * (r_3 / r_2), 0], [-k_theta1 * (r_3 / r_2), k_theta2 + k_theta1 * (r_3 / r_2) **2, -k_theta2], [0, -k_theta2, k_theta2]])

# # problem 3.52
# M = Matrix([[2, 0, 0], [0, 3, 0], [0, 0, 2]])
# K = Matrix([[100, -100, 0], [-100, 250, -150], [0, -150, 150]])

# # problem 3.53
# M = Matrix([[2, 0], [0, 4]])
# K = Matrix([[2000, -2000], [-2000, 4000]])



# t = symbols('t')

this = MDOF_System(M=M, K=K, normalize=True)

this.F = Matrix([cos(3*this.time), 0, 5 * this.time])

this.doEigenAnalysis()