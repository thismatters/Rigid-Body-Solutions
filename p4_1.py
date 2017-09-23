import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *
import numpy as np

# use 46.642215 for more accurate numbers
v_A = convertPolarToCartesian(46.64,degrees(68.31))  # m/s
v_B = convertPolarToCartesian(30.,degrees(120))  # m/s

a_A = convertPolarToCartesian(8909.5,degrees(118))  # m/s
a_B = convertPolarToCartesian(200., degrees(330))  # m/s

r_A = sym.Matrix([0.15, -0.05, 0])  # m
r_B = sym.Matrix([0.08, 0.08, 0])  # m
r_P = sym.Matrix([-0.05, 0.08, 0])  # m

A = Point(position_x=r_A[0], position_y=r_A[1], velocity_x=v_A[0], velocity_y=v_A[1], acceleration_x=a_A[0], acceleration_y=a_A[1])

B = Point(position_x=r_B[0], position_y=r_B[1], velocity_x=v_B[0], velocity_y=v_B[1], acceleration_x=a_B[0], acceleration_y=a_B[1])

P = Point(position_x=r_P[0], position_y=r_P[1])

body = RigidBody('potato')
body.addPoint('A', A)
body.addPoint('B', B)
body.addPoint('P', P)

print str(A)
print str(P)

body.calculate()
body.verbosity = 5
print str(body)
# print str(A)
# print str(B)
# print str(P)

print str(body.calculationHistory)
