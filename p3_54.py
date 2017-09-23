from numpy import *
import scipy as Sci
import scipy.linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# exit()
import os

# g = 32.2*12
m1 = 0.5
m2 = 1
k1 = 1
k2 = 1
k3 = 0

# Set physical properties
M = mat([[m1, 0], [0, m2]])
K = mat([[k1+k2, -(k2)], [-(k2), k2+k3]])
print 'Mass:\n' + str(M) + '\n'
print 'Stiffness:\n' + str(K) + '\n'

# Set damping ratios (modal domain)
zeta = [0,0]

x_0 = mat([[0],[0.10]])
Dx_0 = mat([[0], [0]])

# Set forcing functions (physical domain)
# format: [quad,lin,const]
F1 = mat([[0,0,0]])
F2 = mat([[0,0,0]])
# F1 = mat([[0,0,1000]])
# F2 = mat([[0,0,]])

# Calculate Eigenvalues
a = M[0,0] * M[1,1] - M[1,0] * M[1,0]
b = 2 * M[0,1] * K[0,1] - K[0,0] * M[1,1] - K[1,1] * M[0,0]
c = K[0,0] * K[1,1] - K[0,1] * K[0,1]
lam1 = (-b - sqrt(b**2 - 4*a*c))/(2*a)
lam2 = (-b + sqrt(b**2 - 4*a*c))/(2*a)

print('Eigenvalues:\n%0.5f   %0.5f \n' % (lam1, lam2))

freq1 = sqrt(lam1)
dfreq1 = freq1 * sqrt(1 - zeta[0]**2)
freq2 = sqrt(lam2)
dfreq2 = freq2 * sqrt(1 - zeta[1]**2)
print('Natural Frequencies:\n%0.5f   %0.5f \n' % (freq1, freq2))
print('Damped  Frequencies:\n%0.5f   %0.5f \n' % (dfreq1, dfreq2))
print('sigma:\n %0.5f    %0.5f\n' % (zeta[0]*freq1, zeta[1]*freq2))
print('2* sigma:\n %0.5f    %0.5f\n' % (2*zeta[0]*freq1, 2*zeta[1]*freq2))

# Calculate eigenvectors
a21 = (M[0,0] * lam1 - K[0,0])/(K[0,1] - M[0,1] * lam1)
a22 = (M[0,0] * lam2 - K[0,0])/(K[0,1] - M[0,1] * lam2)
A = mat([[1, 1], [a21, a22]])
print 'Eigenvectors:\n' + str(A) + '\n'

# Normalize Eigenvectors\n
M_q = A.T * M * A
K_q = A.T * K * A
A_s1 = A[:,0]/sqrt(M_q[0,0])
A_s2 = A[:,1]/sqrt(M_q[1,1])
A_s = bmat('A_s1, A_s2');
print 'Modal Masses: \n' + str(M_q) + '\n'
print 'Normalized Eigenvectors:\n' + str(A_s) + '\n'
# print str(K_q)

M_m = A_s.T * M * A_s
K_m = A_s.T * K * A_s

q_0 = A_s.T * M * x_0
Dq_0 = A_s.T * M * Dx_0
print 'Modal Pos ICs:\n' + str(q_0) +'\n'
print 'Modal Vel ICs:\n' + str(Dq_0) +'\n'
			
Qf1 = A_s.T[0,0]*F1 + A_s.T[0,1]*F2
Qf2 = A_s.T[1,0]*F1 + A_s.T[1,1]*F2

print 'Modal forcing function Qf1:\n' + str(Qf1) + '\n'
print 'Modal forcing function Qf2:\n' + str(Qf2) + '\n'

if freq1 < 1e-5:
	qp1 = lambda t: 0
	Dqp1 = lambda t: 0
else:
	qp1 = lambda t: Qf1[0,0]/lam1*(t**2 - 4*zeta[0]*t/freq1 - 2/lam1*(1-4*zeta[0]**2)) + Qf1[0,1]/lam1*(t-2*zeta[0]/freq1) + Qf1[0,2]/lam1
	Dqp1 = lambda t: Qf1[0,0]/lam1*(2*t - 4*zeta[0]/freq1) + Qf1[0,1]/lam1

qp2 = lambda t: Qf2[0,0]/lam2*(t**2 - 4*zeta[1]*t/freq2 - 2/lam2*(1-4*zeta[1]**2)) + Qf2[0,1]/lam2*(t-2*zeta[1]/freq2) + Qf2[0,2]/lam2
Dqp2 = lambda t: Qf2[0,0]/lam2*(2*t - 4*zeta[1]/freq2) + Qf2[0,1]/lam2

# Find these constants!!
if freq1 < 1e-5:
	A1 = Dq_0[0,0]
	B1 = q_0[0,0]
	q1 = lambda t: A1 * t + B1
else:
	A1 = q_0[0,0] - qp1(0)
	B1 = (Dq_0[0,0] + zeta[0]*freq1*A1 - Dqp1(0))/dfreq1
	q1 = lambda t: exp(-zeta[0]*freq1*t)*(A1*cos(dfreq1*t)+B1*sin(dfreq1*t)) + qp1(t)

A2 = q_0[1,0] - qp2(0)
B2 = (Dq_0[1,0] + zeta[1]*freq2*A2 - Dqp2(0))/dfreq2

print 'constants for first mode time response:\nA1 = %0.5f, B1 = %0.5f\n' % (A1, B1)
print 'constants for second modal time response:\nA2 = %0.5f, B2 = %0.5f\n' % (A2, B2)

print 'constants for physical_1 time response:\nA1*a_11 = %0.5f, B1*a_11 = %0.5f, A2*a_12 = %0.5f, B2*a_12 = %0.5f\n' % (A1*A_s[0,0], B1*A_s[0,0], A2*A_s[0,1], B2*A_s[0,1])
print 'constants for physical_2 time response:\nA1*a_21 = %0.5f, B1*a_21 = %0.5f, A2*a_22 = %0.5f, B2*a_22 = %0.5f\n' % (A1*A_s[1,0], B1*A_s[1,0], A2*A_s[1,1], B2*A_s[1,1])

q2 = lambda t: exp(-zeta[1]*freq2*t)*(A2*cos(dfreq2*t)+B2*sin(dfreq2*t)) + qp2(t)

x1 = lambda t: A_s[0,0]*q1(t) + A_s[0,1]*q2(t)
x2 = lambda t: A_s[1,0]*q1(t) + A_s[1,1]*q2(t)

q_unity = mat('%f; %f' % (qp1(0), qp2(0)))
q_quad = mat('%f; %f' % (((qp1(-1) + qp1(1))/2 - q_unity[0,0]), ((qp2(-1) + qp2(1))/2 - q_unity[1,0])))
q_lin = mat('%f; %f' % ((qp1(1) - q_unity[0,0] - q_quad[0,0]), (qp2(1) - q_unity[1,0] - q_quad[1,0])))

# print str(q_unity)
# print str(q_lin)
# print str(q_quad)

x_unity = A_s *q_unity
x_lin = A_s*q_lin
x_quad = A_s*q_quad

if freq1 < 1e-5:
	print 'q_1(t) = %0.5f t + %0.5f \n' % (A1, B1)
else:
	print 'q_1(t) = e^(-%0.5f t)*[%0.5f cos(%0.5f t) + %0.5f sin(%0.5f t)] + \n + %0.5f t^2 + %0.5f t + %0.5f\n' % ((zeta[0]*freq1), A1, dfreq1, B1, dfreq1, q_quad[0,0], q_lin[0,0], q_unity[0,0])

print 'q_2(t) = e^(-%0.5f t)*[%0.5f cos(%0.5f t) + %0.5f sin(%0.5f t)] + \n + %0.5f t^2 + %0.5f t + %0.5f\n' % ((zeta[1]*freq2), A2, dfreq2, B2, dfreq2, q_quad[1,0], q_lin[1,0], q_unity[1,0])

print 'x_1_ss(t) = %0.5f t^2 + %0.5f t + %0.5f' % (x_quad[0,0], x_lin[0,0], x_unity[0,0])
print 'x_2_ss(t) = %0.5f t^2 + %0.5f t + %0.5f' % (x_quad[1,0], x_lin[1,0], x_unity[1,0])

if freq1 < 1e-5:
	T_fin = 5
else:
	T_fin = 2* 2*pi/freq1

numFrames = 500
time = linspace(0,T_fin, num=numFrames)

Pos1 = list()
Pos2 = list()
modalPos1 = list()
modalPos2 = list()

for timestep in time:
	x1_now = x1(timestep)
	Pos1.append(x1_now)

	x2_now = x2(timestep)
	Pos2.append(x2_now)

	q1_now = q1(timestep)
	modalPos1.append(q1_now)

	q2_now = q2(timestep)
	modalPos2.append(q2_now)

# print str(Pos1)
plt.figure(1)
plt.subplot(211)
plt.subplots_adjust(hspace=0.5)
plt.plot(time,modalPos1, time, modalPos2)
plt.title('Modal Responses')
# plt.xlabel('Time (s)')
plt.ylabel('Displacement')
# plt.subplot(223)
plt.legend(('q_1','q_2'))
plt.xlabel('Time (s)')
# plt.plot(time,modalPos2)
plt.subplot(212)
plt.title('Physical Responses')
plt.ylabel('Displacement (m)')
# plt.xlabel('Time (s)')
plt.plot(time,Pos1, time, Pos2)
# plt.subplot(224)
# plt.ylabel('Second Mass')
plt.legend(('x_1','x_2'))
plt.xlabel('Time (s)')
# plt.plot(time,Pos2)
plt.savefig('motion.png')