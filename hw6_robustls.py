import numpy as np
import cvxpy as cp

A_bar = np.matrix([[60,45,-8],[90,30,-30],[0,-8,-4],[30,10,-10]])
d = 0.05
R = d* np.ones((4,3))
b = np.matrix([-6,-3,18,-9]).T
t1 = cp.Variable(1)
t2 = cp.Variable(1)
x =  cp.Variable(3)
objective = cp.Minimize(cp.norm(cp.abs(A_bar*x-b)+R*cp.abs(x),2))
#constraints1 = [cp.norm1(A_bar*x-b)==t1]
#constraints2 = [cp.norm1(R*x)==t2]
#constraints = constraints1+constraints2
constraints=[]
p = cp.Problem(objective,constraints)
p.solve()
nom_res_rls = np.linalg.norm(A_bar*x.value-b)
print nom_res_rls