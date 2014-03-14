import numpy as np
import cvxpy as cp
k = 2000
t = [-3.0+6.0*(i)/(k-1) for i in range(k) ] #range start from zero
y = np.exp(t)
T_powers = np.matrix(np.hstack((np.ones((k,1)),np.matrix(t).T,np.power(np.matrix(t).T,2))))
u = np.exp(3)
l = 0
bisection_tol = 1e-3
gamma1 = cp.Parameter(sign='positive')
a = cp.Variable(3)
b = cp.Variable(2)
objective = 0
#constraints = [cp.abs(T_powers[i]*a-y[i]*(T_powers[i]*cp.vstack(1,b)))<=gamma1*(T_powers[i]*cp.vstack(1,b)) for i in range(100)]
#constraints = [T_powers*a-np.diag(y)*(T_powers*cp.vstack(1,b))<=gamma1*(T_powers*cp.vstack(1,b)),
 #              T_powers*a-np.diag(y)*(T_powers*cp.vstack(1,b))>=-gamma1*(T_powers*cp.vstack(1,b))]
constraints = [cp.abs(T_powers*a-np.diag(y)*(T_powers*cp.vstack(1,b)))<=gamma1*(T_powers*cp.vstack(1,b))]
objective = cp.Minimize(np.ones((1,3))*a)
p = cp.Problem(objective,constraints)
gamma1.value = (l+u)/2.0
a_opt = 0
b_opt = 0
gamma1.value = (u+l)/2
while (u-l)>=bisection_tol:
    print p.is_dcp()
   # p.solve(solver=cp.CVXOPT)
    p.solve()
   # p.solve(verbose=True)
    if p.status is 'optimal':
        u = gamma1.value
        a_opt = a.value
        b_opt = b.value
        #print a_opt
        #print b_opt
        objval_opt = gamma1.value
        #print 'here'
        
    else:
        l = gamma1.value
    gamma1.value = (l+u)/2
    #print gamma1.value
    print p.status
    
#y_fit = T_powers*a_opt
print a_opt
print b_opt
print gamma1.value
plot(t,y,'b')
f_fit = np.divide(T_powers*a_opt,T_powers*np.vstack((1,b_opt)))
plot(t,f_fit,'r+')