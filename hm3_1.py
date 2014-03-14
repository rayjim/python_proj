#solving problem of hw3_1 (extra question)
import cvxpy as cp
import cvxopt
A= cvxopt.matrix([1,2,0,1,0,0,3,1,0,3,1,1,2,1,2,5,1,0,3,2],(4,5)).T
c_max = cvxopt.matrix([100,100,100,100,100],(5,1))
p= cvxopt.matrix([3,2,7,6])
p_disc=cvxopt.matrix([2,1,4,2])
q=cvxopt.matrix([4,10,5,10])
u=cp.Variable(4,1)
x=cp.Variable(4,1)
objective = cp.Maximize(cp.sum(u))
constraints1 =[cp.min(p[i]*x[i],p[i]*q[i]+p_disc[i]*(x[i]-q[i]))>=u[i] for i in range(4)]
constraints =[x>=0, A*x<=c_max]
constraints1.extend(constraints)
prob = cp.Problem(objective,constraints1)
prob.solve()
print x.value
lamb = constraints1[2].dual_value

#############################################################
#original fomulation
#############################################################
print "equavlent form"
xx = cp.Variable(4,1)
objective1 = cp.Maximize(sum([cp.min(p[i]*xx[i],p[i]*q[i]+p_disc[i]*(xx[i]-q[i])) for i in range(4)]))
constraints2 = [xx>=0, A*xx<=c_max]
prob1 = cp.Problem(objective1, constraints2)
prob1.solve()
print xx.value
