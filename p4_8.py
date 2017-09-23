import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np

R_1 = 1.5
R_2 = 3.

r_B = convertPolarToCartesian(R_2,degrees(-45))

G = Point(position_x=0., position_y=0., velocity_y=0., acceleration_y=0.)
C = Point(position_y=-R_2, position_x=0, velocity_x=0., velocity_y=0., acceleration_x=0.)
A = Point(position_x=0., position_y=R_1, velocity_x=15, velocity_y=0, acceleration_x=0.5)
B = Point(position_x=r_B[0], position_y=r_B[1])
# D = Point(position_x=0., position_y=R_2)

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body = RigidBody('potato')
body.addPoint('G', G)
body.addPoint('C', C)
body.addPoint('A', A)
body.addPoint('B', B)
# body.addPoint('B', B)
# body.addPoint('D', D)

# print str(A)
# print str(P)

body.calculate()

print str(body)
print str(G)
print str(B)
# print str(D)

