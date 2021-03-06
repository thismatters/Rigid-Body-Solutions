from rigidbodies import *
import numpy as np
import sympy as sym

V_G, A_G, R_1, R_2, v_A_x, a_A_x, v_E_x, psi  = sym.symbols('v_G a_G r R v_A a_A v psi')

C = Point(position_y=-R_2, position_x=sym.S(0), velocity_y=sym.S(0), velocity_x=v_A_x, acceleration_x=-a_A_x)
E = Point(position_y=R_1, position_x=sym.S(0), velocity_y=sym.S(0), velocity_x=v_E_x, acceleration_x=sym.S(0))
O = Point(position_x=sym.S(0), position_y=sym.S(0), velocity_y=sym.S(0), acceleration_y=sym.S(0))
B = Point(position_r=R_2, position_theta=-psi)

body1 = RigidBody('Cly1')
body1.addPoint('C', C)
body1.addPoint('E', E)
body1.addPoint('O', O)
body1.addPoint('B', B)

# print str(A)

body1.calculate()

print str(body1)
print str(O)
print str(B)
print str(C)
print str(E)