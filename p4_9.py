import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np
import sympy as sym

V_G, A_G = sym.symbols('v_G a_G')
R_1 = sym.S(4) / 12
R_2 = sym.S(10) / 12

r_E = convertPolarToCartesian(R_1,degrees(sym.S(0)))

C1 = Point(position_y=-R_1, position_x=sym.S(0), velocity_x=sym.S(0), velocity_y=sym.S(0), acceleration_x=sym.S(0))
A = Point(position_x=sym.S(0), position_y=R_1, velocity_x=V_G, velocity_y=sym.S(0), acceleration_x=A_G)
O = Point(position_x=sym.S(0), position_y=sym.S(0), velocity_y=sym.S(0), acceleration_y=sym.S(0))
E = Point(position_x=r_E[0], position_y=r_E[1])

D = Point(position_x=sym.S(0), position_y=sym.S(0), velocity_y=sym.S(0), acceleration_y=sym.S(0))
C2 = Point(position_y=-R_2, position_x=sym.S(0), velocity_x=sym.S(0), velocity_y=sym.S(0), acceleration_x=sym.S(0))
B = Point(position_x=sym.S(0), position_y=R_2, velocity_x=V_G, velocity_y=sym.S(0), acceleration_x=A_G)
# D = Point(position_x=0., position_y=R_2)

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body1 = RigidBody('Cly1')
body1.addPoint('O', O)
body1.addPoint('C1', C1)
body1.addPoint('A', A)
body1.addPoint('E', E)
print str(C1)
print str(A)


body2 = RigidBody('Cyl2')
body2.addPoint('B', B)
body2.addPoint('C2', C2)
body2.addPoint('D', D)

# print str(A)
# print str(P)

body1.calculate()
body2.calculate()

print str(body1)
print str(body2)
print str(E)
# print str(B)
# print str(D)

print "Velocity of point E is %0.4f I + %0.4f J ft/sec" % (E.velocity_x.subs(V_G, sym.S(2)).evalf(4), E.velocity_y.subs(V_G, sym.S(2)).evalf(4))
print "Angular acceleration of Large Cylinder: " + str(body2.angularAcceleration.subs([(V_G, sym.S(2)), (A_G, sym.S(2) / 5)]).evalf(4))
