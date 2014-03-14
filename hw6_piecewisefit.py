import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt

npzfile=np.load("plw_data.npz")
x = np.matrix(npzfile['x'])
y = np.matrix(npzfile['y'])
plt.plot(x.T,y.T,'+k')
A=np.hstack((x.T,np.ones((x.T.size,1))))
a_0,a_1 =np.linalg.lstsq(A,y.T)[0]
plt.plot(x.T,A*np.vstack((a_0,a_1)),'b')
mse = np.linalg.norm(A*np.vstack((a_0,a_1))-y.T)**2
print mse
for K in range (1,4):
    #print K
    a = np.linspace(0,1,K+2)  
    F=np.hstack(((a[1]-x.T)/(a[1]-a[0]),np.zeros((x.size,1))))
    F = np.max(F,1) #f_0
    #print F.shape
    for k in range(1,K+1):
        a_1 = a[k-1]
        a_2 = a[k]
        a_3 = a[k+1]
        f = np.hstack(((x.T-a_1)/(a_2-a_1),(a_3-x.T)/(a_3-a_2)))
        f = np.min(f,1)
        f = np.hstack((f,np.zeros((x.size,1))))
        f = np.max(f,1)
        F = np.hstack((F,f))
    #print F.shape
    f = np.hstack(((x.T-a[K])/(a[K+1]-a[K]),np.zeros((x.size,1))))
    f = np.max(f,1)
    F = np.hstack((F,f))
    #print F.shape
    #print F.shape
    #F_para = cp.Parameter(F)
    z = cp.Variable(K+2)
    objective = cp.Minimize(cp.norm(F*z-y.T,2))
    constraints =[(z[i+1]-z[i])*(1/(a[i+1]-a[i]))>=(z[i]-z[i-1])*(1/(a[i]-a[i-1])) for i in range(1,K+1)]
    p = cp.Problem(objective, constraints)
    p.solve()
    y2 = F*z.value
    mse = np.linalg.norm(y2-y.T)
    print mse**2
    if (K == 1):
        plt.plot(x.T,y2,'r')
    elif (K==2):
        plt.plot(x.T,y2,'g')
    else:
        plt.plot(x.T,y2,'m')
plt.xlabel('x')
plt.ylabel('y')
     
