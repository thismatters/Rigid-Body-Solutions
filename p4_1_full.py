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

potato = RigidBody('potato', verbosity=1, precision=3)
potato.addPoint('A', A)
potato.addPoint('B', B)
# potato.addPoint('P', P)

# potato.angularVelocity = sym.S(3)
# print str(A)
# print str(B)

possibleOutcomes = list()

def explore(_body, depth=0):
	calculations = _body.possibleCalculations(limitResultsToOmegaAffectors=True)
	first = True
	numCalcs = len(calculations)
	# print str(numCalcs)
	for i in range(0,numCalcs):
		_bodyToExplore = _body
		if i + 1 != numCalcs:
			_bodyCopy = RigidBody(duplicateOf=_body)
			_bodyCopy.name += str(depth)
			possibleOutcomes.append(_bodyCopy)
			_bodyToExplore = _bodyCopy
		# print "about to run " + str(calculations[i]) + " on body " + str(_body.name)
		
		_bodyToExplore.runCalculation(calculations[i])
		explore(_bodyToExplore, depth=depth+1)
	if numCalcs == 0:
		secondPass = _body.possibleCalculations(limitResultsToOmegaAffectors=False)
		for calculation in secondPass:
			_body.runCalculation(calculation)


possibleOutcomes.append(potato)
# for body in possibleOutcomes:
explore(potato)

angularVelocities = list()
angularAccelerations = list()
for body in possibleOutcomes:
	angularVelocities.append(body.angularVelocity.evalf(6))
	angularAccelerations.append(body.angularAcceleration.evalf(6))

print "Possible Angular Velocities: " + str(angularVelocities)
print "Possible Angular Accelerations: " + str(angularAccelerations)
# body.calculate()

# print str(body)
# print str(A)
# print str(B)
# print str(P)

# print str(body.calculationHistory)
