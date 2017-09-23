import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np

R_A = 8
R_B = 8
R_1 = 9
R_2 = 18

# r_B = convertPolarToCartesian(R_1,degrees(-90))

CA = Point(position_x=0., position_y=0., velocity_y=0., velocity_x=0., acceleration_y=0., acceleration_x=0.)
AA = Point(position_x=R_A, position_y=0, velocity_x=0)

bodyA = RigidBody('PulleyA', angularVelocity=6, angularAcceleration=-4.5)
bodyA.addPoint('CA', CA)
bodyA.addPoint('AA', AA)

CB = Point(position_x=0., position_y=0., velocity_y=0., velocity_x=0., acceleration_y=0., acceleration_x=0.)
BB = Point(position_x=-R_B, position_y=0, velocity_x=0)
bodyB = RigidBody('PulleyB', angularVelocity=-5, angularAcceleration=-1.75)
bodyB.addPoint('CB', CB)
bodyB.addPoint('BB', BB)

bodyA.calculate()
bodyB.calculate()

B = Point(position_y=0., position_x=R_1, velocity_x=0., velocity_y=BB.velocity_y, acceleration_y=BB.acceleration_y)
A = Point(position_y=0., position_x=-R_2, velocity_x=0., velocity_y=AA.velocity_y, acceleration_y=AA.acceleration_y)
D = Point(position_y=R_2, position_x=0.)
O = Point(position_x=0., position_y=0., velocity_x=0., acceleration_x=0.)
C = Point(position_x=R_2, position_y=0.)

# D = Point(position_x=0., position_y=0., velocity_y=0., acceleration_y=0.)
# C2 = Point(position_y=-R_2, position_x=0, velocity_x=0., velocity_y=0., acceleration_x=0.)
# B = Point(position_x=0., position_y=R_2, velocity_x=-2, velocity_y=0, acceleration_x=2. / 5)
# D = Point(position_x=0., position_y=R_2)

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body1 = RigidBody('Cly1')
body1.addPoint('O', O)
body1.addPoint('B', B)
body1.addPoint('A', A)
body1.addPoint('D', D)
body1.addPoint('C', C)
# print str(body1)
# print str(O)
# print str(C)
# print str(A)
# print str(B)


# body2 = RigidBody('Cyl2')
# body2.addPoint('C2', C2)
# body2.addPoint('D', D)

# print str(A)
# print str(P)

body1.calculate()
# body2.calculate()

print str(body1)
print str(C)
print str(D)
print str(O)

# print str(B)

