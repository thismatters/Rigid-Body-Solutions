from rigidbodies import *
import numpy as np

R = 0.04

r_A = convertPolarToCartesian(R,degrees(135))

O = Point(position_x=0., position_y=0., velocity_x=3., velocity_y=0., acceleration_x=-5., acceleration_y=0.)
C = Point(position_x=0., position_y=-R, velocity_x=0., velocity_y=0., acceleration_x=0.)
B = Point(position_x=R/2., position_y=0.)
A = Point(position_x=r_A[0], position_y=r_A[1])

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])


body = RigidBody('potato')
body.addPoint('O', O)
# body.addPoint('B', B)
body.addPoint('C', C)
body.addPoint('B', B)
body.addPoint('A', A)

# print str(A)
# print str(P)

body.calculate()

print str(body)
# print str(B)
# print str(B)

