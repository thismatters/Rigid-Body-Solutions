from sympy import * 
init_printing()

class MDOF_System:
	def __init__(self, M=None, K=None, F=None, zeta_q=None, posIC=None, velIC=None, normalize=True, verbose=True):
		self.M = M
		self.K = K
		if self.M is None or self.K is None:
			return returnVal

		dimen = self.M.shape
		if dimen[0] != dimen[1]:
			raise Exception("Mass matrix shape inconsistent (must be n by n)")
		if dimen != self.K.shape:
			raise Exception("Mass and stiffness matricies of different shape")

		self.n = dimen[0]

		self.F = F
		self.zeta_q = zeta_q
		self.posIC = posIC
		self.velIC = velIC
		self.shouldNormalize = normalize
		self.didNormalize = False
		self.A = None
		self.Lam = None
		self.Astar = None
		self.verbose = verbose
		self.time = symbols('t')

			
	def doEigenAnalysis(self):
		"""Find Eigen Values, Eigen Vectors, and normalize (if appropriate) for the MDOF_System"""
		returnVal = False
		charMatrix = None
		
		if self.verbose:
			print "M = "
			print pretty(self.M.evalf(7)) + "\n"
			print "K = "
			print pretty(self.K.evalf(7)) + "\n"

		lamda = symbols('lamda')
		charMatrix = self.K - lamda * self.M
		eigvals = solve(charMatrix.det(), lamda)
		self.Lam = zeros(self.n, self.n)
		self.Omega_n = zeros(1, self.n)
		# if self.verbose:
		# 	print "eigvals = " + str(eigvals)
		
		A_i = MatrixSymbol('A_i', self.n-1, 1)
		A = Matrix(A_i)  # .subs(A_i[0,0], 1)
		
		# print str(charMatrix)

		eigvecs = None
		for i in range(0,self.n):
			eigval = re(eigvals[i])
			try:
				if eigval < 1E-9:
					# this breaks for symbols %%%%
					eigval = 0
			except TypeError:
				pass
			self.Omega_n[0,i] = sqrt(eigval)
			self.Lam[i,i] = eigval

			thisCharMatrix = charMatrix.subs(lamda, eigval).evalf(15)
			thisCharMatrix.row_del(0)
			# remove col from front, negate it, and append it to the back
			frontCol = thisCharMatrix.col(0) * -1
			thisCharMatrix.col_del(0)
			thisCharMatrix = thisCharMatrix.col_insert(self.n-1, frontCol)
			sols = solve_linear_system_LU(thisCharMatrix, A)
			
			eigvec = sols.values()
			eigvec.insert(0,1)
			# if self.verbose:
			# 	print str(eigvec)
			
			eigvec = Matrix(eigvec)
			if i == 0:
				eigvecs = eigvec
			else:
				eigvecs = eigvecs.col_insert(i,eigvec)
		self.A = eigvecs
		if self.verbose:
			print "Lambda = " 
			print pretty(self.Lam.evalf(10)) + "\n" 
			print "Omega_n = " 
			print pretty(self.Omega_n.evalf(5)) + " [rad/sec]; " + pretty(self.Omega_n.evalf(5) / (2 * pi.evalf(5))) + " [Hz] \n"
			print "A = " 
			print pretty(self.A.evalf(5))  + "\n"
		
		self.Mq = self.A.T * self.M * self.A
		self.Kq = self.A.T * self.K * self.A
		
		if self.verbose:
			print "Mq = " 
			print pretty(self.Mq.evalf(5)) + "\n"
			print "Kq = " 
			print pretty(self.Kq.evalf(5))  + "\n"
		
		# Normalize
		if self.shouldNormalize:
			self.normalize()

		# Deal with RHS
		if self.F is not None:
			if self.didNormalize:
				Qf = self.Astar.T * self.F
			else:
				Qf = self.A.T * self.F
		else:
			Qf = zeros(self.n,1)

		DQf = zeros(self.n,1)
		for i in range(0, self.n):
			DQf[i] = diff(Qf[i],self.time)
		

		# if self.verbose:
		# 	print "Q_f = "
		# 	print pretty(Qf.evalf(5)) + "\n"
		# 	print "DQ_f = "
		# 	print pretty(DQf.evalf(5)) + "\n"

		# State modal diff eq. 
		#  this only works for normalized=true
		for i in range(0,self.n):
			x = "q_" + str(i+1)
			deqString = ""
			if self.didNormalize:
				deqString += "\\ddot " + x 
				if self.Lam[i,i] != 0:
					deqString += " + {:} * {:}".format(self.Lam[i,i].evalf(7), x)
			else:
				deqString += " {:} \\ddot {:}".format(self.Mq[i,i].evalf(7), x)
				if self.Kq[i,i] > 1E-7:
					deqString += " + {:} * {:}".format(self.Kq[i,i].evalf(7), x)

			deqString += " = {:}".format(Qf[i].evalf(4)) 
			print deqString

		# # Find modal ICs
		# if self.posIC is not None and self.velIC is not None:
		# 	premult = None
		# 	if self.didNormalize:
		# 		premult = self.Astar.T * self.M
		# 	else:
		# 		premult = self.A ** -1
		# 	Q_posIC = premult * self.posIC
		# 	Q_velIC = premult * self.velIC

		# # deal with proportional damping

		# # Solve modal diff eq.
		# Q = Matrix([0])
		# for i in range(0,self.n):
		# 	if self.zeta_q is not None:
		# 		zeta = self.zeta_q[i]
		# 	else:
		# 		zeta = 0
		# 	expr = None
		# 	if self.Lam[i,i] != 0:
		# 		omega_n = sqrt(self.Lam[i,i])
		# 		omega_d = omega_n * sqrt(1 - zeta ** 2)
		#  define Qp
		# 		constA = self.posIC[i] - Qp[i].subs(self.time, 0)
		# 		constB = (DQp[i].subs(self.time, 0) + zeta * omega_n * constA) / omega_d

		# 		Qp = 0  # for now

		# 		expr = exp(-zeta * omega_n * self.time) * (constA * cos(omega_d * self.time) + constB * sin(omega_d * self.time)) + Qp
		# 	Q = Q.row_insert(i, Matrix([expr]))
		return returnVal


	def normalize(self):
		Astar = zeros(self.n,1)
		for i in range(0,self.n):
			Astar = Astar.col_insert(i, self.A.col(i) / sqrt(self.Mq[i,i]))
		Astar.col_del(self.n)
		self.Astar = Astar
		self.didNormalize = True

		if self.verbose:
			print "A^star = "
			print pretty(self.Astar.evalf(5)) + "\n"
			print "A^star^T * M * A^star = "
			I_test = self.Astar.T * self.M * self.Astar
			print pretty(I_test.evalf(5)) + "\n"
			print "A^star^T * K * A^star = "
			Lam_test = self.Astar.T * self.K * self.Astar
			print pretty(Lam_test.evalf(5)) + "\n"

	# def modalF(self):
	# 	"""Return the modal forcing function, or False"""
	# 	returnVal = False
	# 	if self.F is not None:
	# 		A = None
	# 		if self.didNormalize:
	# 			A = self.As 
	# 		else:
	# 			A = self.A

	# 		if A is not None:
	# 			returnVal = A.T * self.F
	# 	return returnVal


	# def modalPosIC(self):
	# 	"""Return the modal position initial conditions, or False"""
	# 	returnVal = False
	# 	if self.posIC is not None:
	# 		A = None
	# 		if self.didNormalize:
	# 			A = self.As 
	# 		else:
	# 			A = self.A

	# 		if A is not None:
	# 			returnVal = A * M * self.posIC
	# 	return returnVal


	# def modalVelIC(self):
	# 	"""Return the modal velocity initial conditions, or False"""
	# 	returnVal = False
	# 	if self.velIC is not None:
	# 		A = None
	# 		if self.didNormalize:
	# 			A = self.As 
	# 		else:
	# 			A = self.A

	# 		if A is not None:
	# 			returnVal = A * M * self.velIC
	# 	return returnVal

