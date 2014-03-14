import numpy as np
import cvxpy as cp
from cvxopt import solvers
import cvxopt as co
Q = co.matrix ([[1.0,-1/2],[-1/2,2]])
P = co.matrix([-1.0,0])
A = co.matrix([[1.0,2],[1,-4],[5,76]])
b = co.matrix([-2.0,-3,1])

x = cp.Variable(2,1)

objective = cp.Minimize(cp.quad_form(x,Q)+P.T*x)
constraints = [A.T*x<=b]
p = cp.Problem(objective,constraints)
result = p.solve()


print x.value
print result
print constraints[0].dual_value


