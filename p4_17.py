import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np
import sympy as sym

V_G, A_G, R_1, R_2, A_O, v, psi, omega, b = sym.symbols('v_G a_G r R a_O v psi omega_1 b')

zero = sym.S(0)
a_A_x = sym.S(0)

BO = Point(position_x= zero, position_y = zero, fixed=True)
BC = Point(position_x=zero, position_y=-b)
body0 = RigidBody('roller', angularVelocity=omega, angularAcceleration=zero)
body0.addPoint('BO',BO)
body0.addPoint('BC',BC)
body0.calculate()

C = Point(position_y=-R_2, position_x=zero, velocity_y=zero, velocity_x=BC.velocity_x, acceleration_x=BC.acceleration_x)
E = Point(position_r=R_1, position_theta=-psi, velocity_r=v, velocity_theta=sym.pi/2 -psi)
O = Point(position_x=zero, position_y=zero, velocity_y=zero, acceleration_y=zero)
B = Point(position_r=R_2, position_theta=-psi)

body1 = RigidBody('Cly1')
body1.addPoint('C', C)
body1.addPoint('E', E)
body1.addPoint('O', O)
body1.addPoint('B', B)

body1.calculate()

print str(body1)
print str(B)
print str(E)
print str(O)
print str(C)
