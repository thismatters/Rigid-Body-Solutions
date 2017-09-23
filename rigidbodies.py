# import numpy as np
import sympy as sym


class Point:
	def __init__(self,  
				 position_x=None, 
				 position_y=None,
				 position_r=None,
				 position_theta=None, 
				 position_relative_to=None,
				 velocity_x=None, 
				 velocity_y=None, 
				 velocity_r=None,
				 velocity_theta=None, 
				 acceleration_x=None, 
				 acceleration_y=None,
				 fixed=False,
				 duplicateOf=None):
		self.name = None
		if duplicateOf is not None:
			self.position_x = duplicateOf.position_x
			self.position_y = duplicateOf.position_y
			self.velocity_x = duplicateOf.velocity_x
			self.velocity_y = duplicateOf.velocity_y
			self.acceleration_x = duplicateOf.acceleration_x
			self.acceleration_y = duplicateOf.acceleration_y
			self.solved = duplicateOf.solved
		else:
			self.position_x = sym.S(position_x)
			self.position_y = sym.S(position_y)

			if position_r is not None and position_theta is not None:
				self.position_x = sym.S(position_r) * sym.cos(position_theta)
				self.position_y = sym.S(position_r) * sym.sin(position_theta)
			if position_relative_to is not None:
				self.position_x += position_relative_to.position_x
				self.position_y += position_relative_to.position_y
			if fixed:
				self.velocity_x = 0
				self.velocity_y = 0
				self.acceleration_x = 0
				self.acceleration_y = 0
			else:
				self.velocity_x = sym.S(velocity_x)
				self.velocity_y = sym.S(velocity_y)
				if velocity_r is not None and velocity_theta is not None:
					self.velocity_x = sym.S(velocity_r) * sym.cos(velocity_theta)
					self.velocity_y = sym.S(velocity_r) * sym.sin(velocity_theta)

				self.acceleration_x = sym.S(acceleration_x)
				self.acceleration_y = sym.S(acceleration_y)
			self.solved = False
			self.status

	def __str__(self):
		returnString = "\n"
		if self.name is not None:
			returnString += "Point: %s \n " % str(self.name)

		returnString += '\t{:>4} {:>9}\n'.format('Pos-x:', self.position_x.evalf(4) if self.position_x is not None else "None") 
		returnString += '\t{:>4} {:>9}\n'.format('Pos-y:', self.position_y.evalf(4) if self.position_y is not None else "None") 
		returnString += '\t{:>4} {:>9}\n'.format('Vel-x:', self.velocity_x.evalf(4) if self.velocity_x is not None else "None")
		returnString += '\t{:>4} {:>9}\n'.format('Vel-y:', self.velocity_y.evalf(4) if self.velocity_y is not None else "None")
		returnString += '\t{:>4} {:>9}\n'.format('Acc-x:', self.acceleration_x.evalf(4) if self.acceleration_x is not None else "None")
		returnString += '\t{:>4} {:>9}\n'.format('Acc-y:', self.acceleration_y.evalf(4) if self.acceleration_y is not None else "None")
		return returnString

	def pointData(self):
		data = {'p{}x'.format(self.name): self.position_x.evalf(4),
				'p{}y'.format(self.name): self.position_y.evalf(4),
				'v{}x'.format(self.name): self.velocity_x.evalf(4),
				'v{}y'.format(self.name): self.velocity_y.evalf(4),
				'a{}x'.format(self.name): self.acceleration_x.evalf(4),
				'a{}y'.format(self.name): self.acceleration_y.evalf(4),}
		return data

	def status(self):
		"""The status code tells (in binary) what data are known about the point"""
		if self.solved:
			return 63
		status = 0

		if self.position_x is not None:
			status += 1
		if self.position_y is not None:
			status += 1 << 1
		if self.velocity_x is not None:
			status += 1 << 2
		if self.velocity_y is not None:
			status += 1 << 3
		if self.acceleration_x is not None:
			status += 1 << 4
		if self.acceleration_y is not None:
			status += 1 << 5

		if status == 63:
			self.solved = True
		return status



class RigidBody:
	"""A class for storing and calculating the kinematic properties of a rigid body expressing planar motion"""
	def __init__(self, name=None, angularVelocity=None, angularAcceleration=None, duplicateOf=None, verbosity=5, precision=8):
		if duplicateOf is not None:
			self.angularAcceleration = duplicateOf.angularAcceleration
			self.angularVelocity = duplicateOf.angularVelocity
			self.name = duplicateOf.name + "_c"
			self.calculationHistory = duplicateOf.calculationHistory[:]
			self._pointnames = list()
			self._points = list()
			self.verbosity = duplicateOf.verbosity
			for origPoint in duplicateOf._points:
				self.addPoint(origPoint.name + "_c", Point(duplicateOf=origPoint))
			print("Body {} duplicated".format(duplicateOf.name))
		else:
			self._points = list()
			self._pointnames = list()
			self.calculationHistory = list()
			self.name = name
			self.angularVelocity = sym.S(angularVelocity)
			self.angularAcceleration = sym.S(angularAcceleration)
			self.verbosity = verbosity
		self.precision = precision


	def addPoint(self, _name, point=Point()):
		# check for collisions with name
		if _name in self._pointnames:
			raise Exception("Duplicate point name added to body")
			return
		point.name = _name
		self._pointnames.append(_name)
		self._points.append(point)
		# print "Point added, there are now %d points \n" % len(self._points)


	def __str__(self):
		returnString = "\n"
		if self.name is not None:
			returnString += "Body: %s \n " % str(self.name)
		if self.verbosity > 0:
			returnString += "\tAngularVelocity: " 
			if self.angularVelocity is not None:
				returnString += "{:>9} [rad/sec] \n".format(self.angularVelocity.evalf(7) if self.angularVelocity is not None else "None")
			else:
				returnString += "unknown\n" 
			returnString += "\tAngularAcceleration: " 
			if self.angularAcceleration is not None:
				returnString += "{:>9} [rad/sec^2] \n".format(self.angularAcceleration.evalf(7) if self.angularAcceleration is not None else "None")
			else:
				returnString += "unknown\n"
		if self.verbosity > 1: 
			returnString += "Has points:"
			for point in self._points:
				returnString += str(point)
		return returnString


	def runCalculation(self, calculation):
		pointA, pointB, maskA, maskB = calculation
		if self.verbosity > 2:
			print("Doing calculation: ({}, {}) on body: {}".format(maskA, maskB, self.name))
		try:
			if maskA == maskB:
				if maskA == 6:
					self.angularVelocity = (pointB.velocity_x - pointA.velocity_x) / (pointA.position_y - pointB.position_y)
					if self.angularVelocity.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
						self.angularVelocity = None
						raise ZeroDivisionError
				elif maskA == 9:
					self.angularVelocity = (pointB.velocity_y - pointA.velocity_y) / (pointB.position_x - pointA.position_x)
					if self.angularVelocity.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
						self.angularVelocity = None
						raise ZeroDivisionError
				elif maskA == 19:
					if self.angularVelocity is None:
						self.angularVelocity = sym.sqrt(((pointB.acceleration_x - pointA.acceleration_x) + (
												pointB.position_y - pointA.position_y) * self.angularAcceleration) / (pointA.position_x - pointB.position_x))
						if self.angularVelocity.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							self.angularVelocity = None
							raise ZeroDivisionError
					else:
						self.angularAcceleration = ((pointB.acceleration_x - pointA.acceleration_x) + (pointB.position_x - pointA.position_x) * self.angularVelocity ** 2)/(pointA.position_y - pointB.position_y)
						if self.angularAcceleration.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							self.angularAcceleration = None
							raise ZeroDivisionError
				elif maskA == 35:
					if self.angularVelocity is None:
						self.angularVelocity = sym.sqrt(((pointB.acceleration_y - pointA.acceleration_y) - (
												pointB.position_x - pointA.position_x) * self.angularAcceleration) / (pointA.position_y - pointB.position_y))
						if self.angularVelocity.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							self.angularVelocity = None
							raise ZeroDivisionError
					else:
						self.angularAcceleration = ((pointB.acceleration_y - pointA.acceleration_y) + (pointB.position_y - pointA.position_y) * self.angularVelocity ** 2)/(pointB.position_x - pointA.position_x)
						if self.angularAcceleration.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							self.angularAcceleration = None
							raise ZeroDivisionError
			else:
				if maskA == 6:
					if maskB == 2:
						pointB.velocity_x = self.angularVelocity * (pointA.position_y - pointB.position_y) + pointA.velocity_x
						if pointB.velocity_x.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.velocity_x = None
							raise ZeroDivisionError
					elif maskB == 4:
						pointB.position_y = (pointA.velocity_x - pointB.velocity_x) / self.angularVelocity + pointA.position_y 
						if pointB.position_y.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_y = None
							raise ZeroDivisionError
				elif maskA == 9:
					if maskB == 1:
						pointB.velocity_y = self.angularVelocity * (pointB.position_x - pointA.position_x) + pointA.velocity_y
						if pointB.velocity_y.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.velocity_y = None
							raise ZeroDivisionError
					elif maskB == 8:
						pointB.position_x = (pointB.velocity_y - pointA.velocity_y) / self.angularVelocity + pointA.position_x
						if pointB.position_x.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_x = None
							raise ZeroDivisionError
				elif maskA == 19:
					if maskB == 3:
						pointB.acceleration_x = pointA.acceleration_x + (pointA.position_y - pointB.position_y) * self.angularAcceleration + (pointA.position_x - pointB.position_x) * self.angularVelocity ** 2
						if pointB.acceleration_x.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.acceleration_x = None
							raise ZeroDivisionError
					elif maskB == 17:
						pointB.position_y = ((pointA.acceleration_x - pointB.acceleration_x) + (pointA.position_x - pointB.position_x) * self.angularVelocity ** 2) / self.angularAcceleration + pointA.position_y
						if pointB.position_y.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_y = None
							raise ZeroDivisionError
					elif maskB == 18:
						pointB.position_x = ((pointA.acceleration_x - pointB.acceleration_x) + (pointA.position_y - pointB.position_y) * self.angularAcceleration) / (self.angularVelocity ** 2) + pointA.position_x
						if pointB.position_x.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_x = None
							raise ZeroDivisionError
				elif maskA == 35:
					if maskB == 3:
						pointB.acceleration_y = pointA.acceleration_y + (pointB.position_x - pointA.position_x) * self.angularAcceleration + (pointA.position_y - pointB.position_y) * self.angularVelocity ** 2
						if pointB.acceleration_y.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.acceleration_y = None
							raise ZeroDivisionError
					elif maskB == 33:
						pointB.position_y = ((pointA.acceleration_y - pointB.acceleration_y) + (pointB.position_x - pointA.position_x) * self.angularAcceleration) / (self.angularVelocity ** 2) + pointA.position_y
						if pointB.position_y.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_y = None
							raise ZeroDivisionError
					elif maskB == 34:
						pointB.position_x = ((pointB.acceleration_y - pointA.acceleration_y) + (pointB.position_y - pointA.position_y) * self.angularVelocity ** 2) / self.angularAcceleration + pointA.position_x
						if pointB.position_x.has(sym.oo, -sym.oo, sym.zoo, sym.nan):
							pointB.position_x = None
							raise ZeroDivisionError
			self.calculationHistory.append((pointA.name, pointB.name, maskA, maskB))
		except ZeroDivisionError:
			print("Division by zero happened, no data stored for this calculation")
			return


	def possibleCalculations(self, limitResultsToOmegaAffectors=False):
		result = list()
		for pointA in iter(self._points):
				pointA_status = pointA.status()
				pointA_statuses = list()
				for x in [6, 9, 19, 35]:
					if pointA_status & x == x:
						pointA_statuses.append(x)
				for i in range(len(self._points)): #pointB in iter(self._points):
					pointB = self._points[i]
					if pointB.solved and self.angularAcceleration is not None and self.angularVelocity is not None:
						continue
					if pointB.name is pointA.name:
						if self.verbosity > 2:
							print("checking point {} (as A) against point {} (as B) [collides]".format(pointA.name, pointB.name))
						continue
					else:
						print("checking point {} (as A) against point {} (as B)".format(pointA.name, pointB.name))
					pointB_status = pointB.status()
					for x in pointA_statuses:
						y = pointB_status & x
						calculation = (pointA, pointB, x, y)
						if x < 10:
							if y == x:
								if self.angularVelocity is None:
									result.append(calculation)
									if self.verbosity > 2:
										print("calculation possible: ({}, {}, {}, {})".format(calculation[0].name, calculation[1].name, calculation[2], calculation[3]))
									# showsImprovement = True
							elif y in statusMasks[x] and not limitResultsToOmegaAffectors:
								if self.angularVelocity is not None:
									result.append(calculation)
									if self.verbosity > 2:
										print("calculation possible: ({}, {}, {}, {})".format(calculation[0].name, calculation[1].name, calculation[2], calculation[3]))
									# showsImprovement = True
						else:
							if y == x:
								if (self.angularVelocity is not None) ^ (self.angularAcceleration is not None):
									result.append(calculation)
									if self.verbosity > 2:
										print("calculation possible: ({}, {}, {}, {})".format(calculation[0].name, calculation[1].name, calculation[2], calculation[3]))
									# showsImprovement = True
							elif y in statusMasks[x] and not limitResultsToOmegaAffectors:
								if (self.angularVelocity is not None) and (self.angularAcceleration is not None):
									result.append(calculation)
									if self.verbosity > 2:
										print("calculation possible: ({}, {}, {}, {})".format(calculation[0].name, calculation[1].name, calculation[2], calculation[3]))
									# showsImprovement = True
		# if printable
		# 	for calculation in result:

		return self.cullDuplicateCalculations(result)

	def cullDuplicateCalculations(self, calculations):
		culledOne = True
		while culledOne:
			culledOne = False
			numCalcs = len(calculations)
			for i in range(0, numCalcs):
				for j in range(0, numCalcs):
					if i == j:
						continue
					if calculations[i][2] == calculations[j][2] and calculations[i][3] == calculations[j][3]:
						if calculations[i][0] == calculations[j][1] and calculations[i][1] == calculations[j][0]:
							calculations.pop(j)
							culledOne=True
							break;
				if culledOne:
					break
		return(calculations)

	def calculate(self):
		# This algorithm is x-cheuvanistic, meaning that when calculating it always defaults 
		#   to the x values for velocity, acceleration as the most accurate value, this may 
		#   lead to some uncertainty propogation, which I will address in a later version.
		showsImprovement = True
		runs = 0
		statusMasks = {6: [2, 4], 9: [1, 8], 19: [3, 17, 18], 35: [3, 33, 34]}
		# print str(self._points)
		while showsImprovement and runs < 5:
			if self.verbosity > 2:
				print("Iterating through 'calculate'")
			showsImprovement = False
			for pointA in iter(self._points):
				pointA_status = pointA.status()
				pointA_statuses = list()
				for x in [6, 9, 19, 35]:
					if pointA_status & x == x:
						pointA_statuses.append(x)
				for i in range(len(self._points)): #pointB in iter(self._points):
					pointB = self._points[i]
					if pointB.solved:
						continue
					if pointB.name is pointA.name:
						if self.verbosity > 2:
							print("checking point {} (as A) against point {} (as B) [collides]".format(pointA.name, pointB.name))
						continue
					else:
						if self.verbosity > 2:
							print("checking point {} (as A) against point {} (as B)".format(pointA.name, pointB.name))
					pointB_status = pointB.status()
					for x in pointA_statuses:
						y = pointB_status & x
						if x < 10:
							if y == x:
								if self.angularVelocity is None:
									self.runCalculation((pointA, pointB, x, x))
									showsImprovement = True
							elif y in statusMasks[x]:
								if self.angularVelocity is not None:
									self.runCalculation((pointA, pointB, x, y))
									showsImprovement = True
						else:
							if y == x:
								if (self.angularVelocity is not None) ^ (self.angularAcceleration is not None):
									self.runCalculation((pointA, pointB, x, x))
									showsImprovement = True
							elif y in statusMasks[x]:
								if (self.angularVelocity is not None) and (self.angularAcceleration is not None):
									self.runCalculation((pointA, pointB, x, y))
									showsImprovement = True		
			runs += 1		
								

def convertPolarToCartesian(r,theta):
	"""Accepts theta in radians"""
	return r * sym.Matrix([sym.cos(theta), sym.sin(theta), 0])


def percentDifference(x1, x2):
	return float(x2 - x1) / x1

degrees = lambda x: x * sym.pi / 180.  # convert degrees to standard radians
rpm = lambda x: x * 2 * sym.pi / 60.  # convert rpm to rad/sec
hz = lambda x: x * 2 * sym.pi  # convert hz to rad/sec