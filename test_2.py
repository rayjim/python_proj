import cvxpy as cp
import numpy as np
import cvxopt
import matplotlib.pyplot as plt

n = 10
m = 5
A = cvxopt.normal(n,m)
b = cvxopt.normal(n)
gamma = cp.Parameter(sign="Positive")

x = cp.Variable(m)
objective = cp.Minimize(cp.norm(A*x-b,2)+gamma*cp.norm(x,2))
p = cp.Problem(objective)

def get_x(gamma_value):
    gamma.value = gamma_value
    result = p.solve()
    f1 = (A*x.value-b).T*(A*x.value-b)
    f2 = (x.value).T*(x.value)
    return (f1,f2)
gammas = np.linspace(0,5,200)
x_values = [get_x(value) for value in gammas]
f1_values, f2_values = zip(*x_values)
plt.scatter(f1_values,f2_values,color='blue',marker='.')
plt.figure
#plt.plot(f1_values,f2_values)
plt.xlabel("|Ax-b|")
plt.ylabel("|x|")