#qp example
from cvxopt import matrix, solvers
from cvxopt.solvers import qp
from cvxpy import Variable
Q = matrix([[1.0,-1/2], [-1/2,2]])
f = matrix([-1.0,0])
A = matrix([[1.0,2],[1,-4],[5,76]])
b = matrix([-2.0,-3,1])

sol = qp(Q,f,A.T,b,None,None)
print sol['x']

from cvxpy import Minimize, Problem,norm2
#cholesky
L = matrix(np.linalg.cholesky(Q))
x = Variable(2,1)
objective = Minimize(norm2(L*x)+f.T*x)
constraints = [A.T*x <= b]
pro1 = Problem(objective, constraints)
print pro1.solve()
print x.value 


#purtube version of QP

