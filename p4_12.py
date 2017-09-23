import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np

R_1 = 0.425 / 2
# R_2 = 10. / 12

r_B = convertPolarToCartesian(R_1,degrees(-90))

O = Point(position_x=0., position_y=0., velocity_x=0., acceleration_y=5., acceleration_x=0)
C = Point(position_x=R_1, position_y=0, velocity_x=0., velocity_y=0., acceleration_y=0.)
A = Point(position_y=0., position_x=-R_1, velocity_x=0, velocity_y=2.1)
B = Point(position_x=r_B[0], position_y=r_B[1])

# D = Point(position_x=0., position_y=0., velocity_y=0., acceleration_y=0.)
# C2 = Point(position_y=-R_2, position_x=0, velocity_x=0., velocity_y=0., acceleration_x=0.)
# B = Point(position_x=0., position_y=R_2, velocity_x=-2, velocity_y=0, acceleration_x=2. / 5)
# D = Point(position_x=0., position_y=R_2)

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body1 = RigidBody('Cly1')
body1.addPoint('O', O)
body1.addPoint('C', C)
body1.addPoint('A', A)
body1.addPoint('B', B)
print str(body1)
print str(O)
print str(C)
print str(A)
print str(B)


# body2 = RigidBody('Cyl2')
# body2.addPoint('B', B)
# body2.addPoint('C2', C2)
# body2.addPoint('D', D)

# print str(A)
# print str(P)

body1.calculate()
# body2.calculate()

print str(body1)
print str(B)
# print str(B)
# print str(D)

