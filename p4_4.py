from rigidbodies import *
import numpy as np
import sympy as sym

R_1, R_2, V_O, A_O, psi = sym.symbols('r R v_O a_O psi')

O = Point(position_x=0., position_y=0., velocity_x=V_O, velocity_y=0., acceleration_x=A_O, acceleration_y=0.)
C = Point(position_x=0., position_y=-R_1, velocity_x=0., velocity_y=0., acceleration_x=0.)
E = Point(position_r=R_2, position_theta=sym.pi - psi)


body = RigidBody('Wheel')
body.addPoint('O', O)
# body.addPoint('B', B)
body.addPoint('C', C)
body.addPoint('E', E)

body.calculate()

print str(body)
print str(E)

