import cvxpy as cp
import numpy as np
A = np.matrix([[1,0,1,0,0],[1,0,0,1,0],[0,0,0,0,1],[0,1,1,0,0],[0,0,1,1,0]])
p = np.matrix([0.5,0.6,0.6,0.6,0.2])
q = np.matrix([10,5,5,20,10])
n=5
m=5
x = cp.Variable(5)
t = cp.Variable(1)
objective = cp.Maximize(p*x-t)
constraints1 = [A*x<=np.ones((5,1))*t]
constraints2 = [x>=0,x<=q.T]
constraints = constraints1+constraints2
pro = cp.Problem(objective, constraints)
pro.solve()
print x.value
r_opt = p*x.value-np.max(A*x.value)
print r_opt
r_comp = p*q.T-np.max(A*q.T)
print r_comp
