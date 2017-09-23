from rigidbodies import *
import numpy as np

R_1 = 0.5
R_2 = 1.

# r_A = convertPolarToCartesian(R,degrees(135))

O = Point(position_x=0., position_y=0., velocity_y=0., acceleration_y=0.)
C = Point(position_x=0., position_y=-R_1, velocity_x=0., velocity_y=0., acceleration_x=0.)
A = Point(position_x=0., position_y=-R_2)
B = Point(position_x=R_2, position_y=0.)
D = Point(position_x=0., position_y=R_2)

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body = RigidBody('potato', angularVelocity= -3.13, angularAcceleration= 9.81)
body.addPoint('O', O)
body.addPoint('C', C)
body.addPoint('A', A)
# body.addPoint('B', B)
# body.addPoint('D', D)

# print str(A)
# print str(P)

body.calculate()

print str(body)
print str(O)
print str(A)
# print str(D)

