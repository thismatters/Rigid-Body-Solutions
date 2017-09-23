from sympy import *
from rigidbodies import *

t_star = 0

theta_ddot_init = 0.25  # rad / s^2
theta_dot_init = 180 * (2 * pi) / 60.0 # rad / s
theta_init = 130 * pi / 180.0 # rad
# theta, theta_dot, theta_ddot = symbols('theta theta_dot theta_ddot')

theta_ddot = theta_ddot_init
theta_dot = theta_dot_init + theta_ddot * t_star
theta = theta_init + theta_dot_init * t_star + theta_ddot_init * t_star **2 / 2

t, phi, phi_dot, phi_ddot = symbols('t phi phi_dot phi_ddot')
s, s_dot, s_ddot = symbols('s s_dot s_ddot')

r = 0.2  # m
L = 1.5  # m
a = 1.2  # m
# r, L, a = symbols('r L a')

th = theta + theta_dot * t + theta_ddot / 2 * t ** 2
ph = phi + phi_dot * t + phi_ddot / 2 * t ** 2
S_BD = s + s_dot * t + s_ddot / 2 * t ** 2

x_traverse = r * cos(th) + S_BD * cos(ph) - a 
y_traverse = r * sin(th) - S_BD * sin(ph) 

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
A = Point(position_y=zero, position_x=zero, velocity_x=zero, velocity_y=zero, acceleration_x=zero, acceleration_y=zero)
B = Point(position_r=r, position_theta=theta)

body1 = RigidBody('AB', angularVelocity=theta_dot, angularAcceleration=theta_ddot, verbosity=0)
body1.addPoint('A', A)
body1.addPoint('B', B)
body1.calculate()

# B_prime = Point(duplicateOf=B)
# B_prime.position_x = 0
# B_prime.position_y = 0
C = Point(position_relative_to=B, position_r=L, position_theta=-solutions[phi])
D = Point(position_relative_to=B, position_r=solutions[s], position_theta=-solutions[phi])

# print str(solutions[phi_dot])

body2 = RigidBody('BD', angularVelocity=-solutions[phi_dot], angularAcceleration=-solutions[phi_ddot], verbosity=0)
body2.addPoint('B', B)
body2.addPoint('C', C)
body2.addPoint('D', D)

body2.calculate()
print str(B)
print str(D)
print str(C)