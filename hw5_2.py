import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
m = 30
n = 100
A_re = np.random.rand(m,n)
A_im = np.random.rand(m,n)
A_1 = np.hstack([A_re, -A_im])
A_2 = np.hstack([A_im, A_re]);
A = np.vstack([A_1, A_2])
b_re = np.random.rand(m,1)
b_im = np.random.rand(m,1)
b = np.vstack([b_re,b_im])
###############################################33
#norm2
x_2 = cp.Variable(2*n)
objective_2 = cp.Minimize (cp.norm(x_2,2))
constraints_2 = [A*x_2==b]
prob_2 = cp.Problem(objective_2,constraints_2)
prob_2.solve()

###################################################
#norminf not correct

x_inf = cp.Variable(2*n)
objective_inf = cp.Minimize(cp.norm(x_inf,"inf"))
constraints_inf =[A*x_inf==b]
prob_inf = cp.Problem(objective_inf,constraints_inf)
prob_inf.solve()

##################################################
#plot

plt.scatter(x_2.value[0:n-1],x_2.value[n:2*n-1],marker='^')
plt.scatter(x_inf.value[0:n-1],x_inf.value[n:2*n-1],marker='o')