import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
n=100
m=300
A=np.matrix(np.random.rand(m,n))
b= A*np.ones((n,1))/2
c=-np.matrix(np.random.rand(n,1))

##################################3
x=cp.Variable(n)
objective = cp.Minimize(c.T*x)
constraints1 = [A*x<=b]
constraints2 = [x>=0,x<=1]
constraints = constraints1+constraints2
pro = cp.Problem(objective, constraints)
pro.solve()
#print x.value
t = np.linspace(0,1,100)
obj =[]
cond=[]
for i in range(t.size):
    x_new = np.copy(x.value)
    x_new[np.where(x_new<t[i])[0]]=0
    x_new[np.where(x_new>=t[i])[0]]=1
    temp =(np.max(A*x_new-b)).tolist()
    cond.append(temp)
    obj.extend((c.T*x_new).tolist())
obj=np.array(obj)
i_feas = np.where(np.array(cond)<=0)[0] #Find good point
U = np.min(obj[i_feas])
print U
tt = np.min(i_feas)

plt.subplot(2,1,1)
plt.plot(t[0:tt-1],cond[0:tt-1],'r',t[tt:],cond[tt:],'b')
plt.ylabel("Ax-b")
plt.subplot(2,1,2)
plt.plot(t[0:tt-1],obj[0:tt-1],'r',t[tt:],obj[tt:],'b')
plt.xlabel("t")
plt.ylabel("objective")