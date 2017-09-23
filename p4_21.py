from sympy import *
import os, sys
lib_path = os.path.abspath('/home/paul/Tutoring/libpy')
sys.path.append(lib_path)
from rigidbodies import *

t_star = 0

theta_ddot_init = 0  # rad / s^2
theta_dot_init = 3600 * (2 * pi) / 60.0 # rad / s
theta_init = 30 * pi / 180.0 # rad
# theta, theta_dot, theta_ddot = symbols('theta theta_dot theta_ddot')

theta_ddot = theta_ddot_init
theta_dot = theta_dot_init + theta_ddot * t_star
theta = theta_init + theta_dot_init * t_star + theta_ddot_init * t_star **2 / 2

t, phi, phi_dot, phi_ddot = symbols('t phi phi_dot phi_ddot')
x, x_dot, x_ddot = symbols('x x_dot x_ddot')

l_1 = 1.5  # m
l_2 = 6  # m
# a = 1.2  # m
# r, L, a = symbols('r L a')

th = theta + theta_dot * t + theta_ddot / 2 * t ** 2
ph = phi + phi_dot * t + phi_ddot / 2 * t ** 2
X = x + x_dot * t + x_ddot / 2 * t ** 2

x_traverse = l_1 * cos(th) + l_2 * cos(ph) - X 
y_traverse = l_1 * sin(th) - l_2 * sin(ph) 

solutions = {t: 0}

solns = solve([x_traverse.subs(solutions), y_traverse.subs(solutions)], dict=True)

solutions.update(solns[0])

x_traverse_dot = x_traverse.diff(t)
y_traverse_dot = y_traverse.diff(t)

solns = solve([x_traverse_dot.subs(solutions), y_traverse_dot.subs(solutions)], dict=True)

solutions.update(solns[0])

x_traverse_ddot = x_traverse_dot.diff(t)
y_traverse_ddot = y_traverse_dot.diff(t)

solns = solve([x_traverse_ddot.subs(solutions), y_traverse_ddot.subs(solutions)], dict=True)
solutions.update(solns[0])


print str(x_traverse_dot.subs({t: 0}))
print str(y_traverse_dot.subs({t: 0}))
print str(x_traverse_ddot.subs({t: 0}))
print str(y_traverse_ddot.subs({t: 0}))

print str(solutions)

zero = S(0)
O = Point(position_y=zero, position_x=zero, velocity_x=zero, velocity_y=zero, acceleration_x=zero, acceleration_y=zero)
A = Point(position_r=l_1, position_theta=theta)

body1 = RigidBody('OA', angularVelocity=theta_dot, angularAcceleration=theta_ddot, verbosity=0)
body1.addPoint('O', O)
body1.addPoint('A', A)
body1.calculate()

# B_prime = Point(duplicateOf=B)
# B_prime.position_x = 0
# B_prime.position_y = 0
G = Point(position_relative_to=A, position_r=l_2 / 2, position_theta=-solutions[phi])
B = Point(position_relative_to=A, position_r=l_2, position_theta=-solutions[phi])

# print str(solutions[phi_dot])

body2 = RigidBody('AB', angularVelocity=-solutions[phi_dot], angularAcceleration=-solutions[phi_ddot], verbosity=0)
body2.addPoint('A', A)
body2.addPoint('B', B)
body2.addPoint('G', G)

body2.calculate()
print str(A)
print str(B)
print str(G)