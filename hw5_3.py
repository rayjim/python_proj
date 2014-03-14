from cvxpy import Minimize, Variable, Problem,max,abs,sum
import numpy as np
n = 3
N = 30
A = np.matrix([[-1,0.4,0.8],[1,0,0],[0,1,0]])
b = np.matrix ([1,0,0.3]).T
x0 = zeros((n,1))
xdes = np.matrix([7,2,-6]).T
x = Variable(n,N+1)
u = Variable(1,N)
objective = Minimize(sum(max(abs(u),2*abs(u)-1)))
constraints1 = [x[:,1:N+1]== A*x[:,0:N]+b*u]
constraints2 = [x[:,0]==x0]
constraints3 = [x[:,N]== xdes]
constraints = constraints1 + constraints2 + constraints3
prob1 = Problem(objective, constraints)
prob1.solve()
print u.value
step(range(30),u.value.T)