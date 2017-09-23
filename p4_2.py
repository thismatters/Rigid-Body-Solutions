import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np

v_A = convertPolarToCartesian(10,degrees(180))  # ft/s
# v_B = convertPolarToCartesian(30.,degrees(120))  # ft/s

a_A = convertPolarToCartesian(2,degrees(50))  # ft/s^2
# a_B = convertPolarToCartesian(200., degrees(330))  # ft/s^2

r_A = sym.Matrix([15, -5, 0]) / 12.  # ft
r_B = sym.Matrix([8, 8, 0]) / 12.  # ft
r_P = sym.Matrix([-5, 8, 0]) / 12.  # ft

A = Point(position_x=r_A[0], position_y=r_A[1], velocity_x=v_A[0], velocity_y=v_A[1], acceleration_x=a_A[0], acceleration_y=a_A[1])

# B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])

P = Point(position_x=r_P[0], position_y=r_P[1])

body = RigidBody('potato', angularVelocity= rpm(600), angularAcceleration=-3)
body.addPoint('A', A)
# body.addPoint('B', B)
body.addPoint('P', P)

print str(A)
print str(P)

body.calculate()
body.verbosity = 5
print str(body)
# print str(B)
# print str(P)

