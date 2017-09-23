import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np
import sympy as sym

V_G, A_G, R_1, R_2, v_A_y, a_A_y, v_B_y, a_B_y  = sym.symbols('v_G a_G r R v_A a_A v_B a_B')

A = Point(position_x=-R_2, position_y=sym.S(0), velocity_x=sym.S(0), velocity_y=v_A_y, acceleration_y=a_A_y)
B = Point(position_x=R_1, position_y=sym.S(0), velocity_x=sym.S(0), velocity_y=v_B_y, acceleration_y=a_B_y)
O = Point(position_x=sym.S(0), position_y=sym.S(0), velocity_x=sym.S(0), acceleration_x=sym.S(0))
P = Point(position_x=sym.S(0), position_y=R_2)


body1 = RigidBody('Cly1')
body1.addPoint('A', A)
body1.addPoint('B', B)
body1.addPoint('O', O)
body1.addPoint('P', P)

print str(A)

body1.calculate()

print str(body1)
print str(P)