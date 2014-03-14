import cvxpy as cp
import numpy as np

P = np.matrix([[3.5000,1.11,1.11,1.04,1.01],[0.5,0.97,0.98,1.05,1.01],
               [0.5,0.99,0.99,0.99,1.01],[0.5,1.05,1.06,0.99,1.01],
               [0.5,1.16,0.99,1.07,1.01],[0.5000,0.990,0.9900,1.0600,1.0100],
               [0.5000,0.9200,1.0800,0.9900,1.0100],[0.5000,1.130,1.1000,0.9900,1.0100],
               [0.5000, 0.9300,0.9500, 1.0400, 1.0100],[3.5000,0.9900,0.9700,0.9800,1.0100]])

(m,n)=P.shape
x_unif = np.ones((n,1))/n

###################################################
## Insert the code
pi = np.ones((m,1))/m
y = cp.Variable(m)
x = cp.Variable(n)
constraints1 = [y == P*x]
constraints2 = [x>=0,np.ones((1,n))*x==1]
constraints = constraints1+constraints2
objective = cp.Minimize(-pi.T*cp.log(y))
pro = cp.Problem(objective, constraints)
pro.solve()
Rit = pi.T*np.log(P*x.value)
print x.value
print Rit
R_unif = pi.T*np.log(P*x_unif)
print x_unif
print R_unif

###################################################
N=10
T=200
w_opt=[]
w_unif=[]

for i in range(N):

    events  = np.ceil(np.random.rand(1,T)*m-1).astype(int)
    P_event = P[events,:]
   
    w_unif.extend((np.hstack((np.matrix(1),np.cumprod(P_event*x_unif)))).tolist())
    w_opt.extend((np.hstack((np.matrix(1),np.cumprod(P_event*x.value)))).tolist())
import matplotlib.pyplot as plt
plt.semilogy(matrix(w_unif).T,'r--')
plt.semilogy(matrix(w_opt).T,'g')
plt.grid()
plt.xlabel('time')
plt.ylabel('wealth')
