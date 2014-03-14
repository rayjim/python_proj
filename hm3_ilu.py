import cvxopt
from scipy import linalg, matrix
import numpy as np
import cvxpy as cp
###################################################################################
## preprocessing
####################################################################################
def nullspace(A, atol=1e-13, rtol=0):
     A = np.atleast_2d(A)
     u, s, vh = svd(A)
     tol = max(atol, rtol * s[0])
     nnz = (s >= tol).sum()
     ns = vh[nnz:].conj().T
     return ns


a1= matrix(linspace(0,1,10))
a2 = matrix([1.9, 1.8, 1.0, 1.1, 1.9, 1.8, 1.9, 1.7, 1.5, 1.5])
L=vstack([a1,a2])
m=L.shape[1]
V11 = [0.0, 0.1, 0.15, 0.2, 0.1, 0.2, 0.3, 0.0, 0.0, 0.0,0.1, 0.2,
      0.2, 0.0, 0.1, 0.05, 0.1, 0.1, 0.0, 0.2, 0.1]
V2 = matrix(map(lambda x: x*0.4,V11))
V1 = matrix(linspace(0,1,21))
V = vstack([V1,V2])
n = V.shape[1]-1
plot(array(a1.T),array(a2.T),'o',array(V1.T),array(V2.T),"-")


dV = V[:,1:n+1]-V[:,0:n]
VI=V[:,0:n]+0.5*dV
A=zeros((n,m))
#A[20,:] = 0.001*ones((1,10))
for i in range(n):
    for j in range(m):
        dVI=L[:,j]-VI[:,i]
        dVperp = nullspace(dV[:,i].T)
        if dVperp[1]<0:
            dVperp=-dVperp
        A[i,j]=np.max([0,dVI.T*dVperp/(norm(dVI)*norm(dVperp))])/(norm(dVI)*norm(dVI))
        
b = ones((20,1))
        
########################################################################################
#solution 1
#average
p1=np.logspace(-3,0,1000)   
f_0 = [np.max(np.abs(np.log(A*np.matrix((ones((m,1))*p1[ii]))))) for ii in range(p1.size)]
print min(f_0)
print p1[argmin(f_0)]

########################################################################################       
#solution 2 
# Least square
p2 = np.linalg.lstsq(A,b)[0]
p2[np.where(p2>1)[0]]=1
p2[np.where(p2<0)[0]]=0
val2 = np.max(np.abs(log(A*matrix(p2))))
print p2
print val2
#######################################################################################
#solution3 
# regulized least square
nopts=1000
rohs = linspace(1e-3,1,nopts)
crit = []


for i in range(nopts):
    A2 = vstack([A,sqrt(rohs[i])*identity(m)])
    b2  = vstack([ones((n,1)),sqrt(rohs[i])*0.5*ones((m,1))])
    p1 = np.linalg.lstsq(A2, b2)[0]
    crit.append(norm(p1-0.5*ones((m,1)),inf))
crit=array(crit)
idx = find(crit<=0.500)
#rohs = rohs[idx[0]]
rohs = rohs[idx[0]]
A3 = vstack([A,identity(m)*sqrt(rohs)])
b3  = vstack([ones((n,1)),sqrt(rohs)*0.5*ones((m,1))])
p_ls_reg = np.linalg.lstsq(A3, b3)[0]
val_ls_reg = np.max(np.abs(log(A*matrix(p_ls_reg))))
print p_ls_reg
print val_ls_reg

###########################################################################################
#solution 4
#chebshev approximation
p_chev = cp.Variable(m)
objective = cp.Minimize(cp.norm(A*p_chev-ones((n,1)),"inf"))
constraints =[p_chev<=1,p_chev>=0]
p4=cp.Problem(objective, constraints)
result = p4.solve()
f_4 = np.max(np.abs(log(A*matrix(p_chev.value))))
print p_chev.value
print f_4


###########################################################################################
#solution 5
#cvxpy
u = cp.Variable(1)
p_cp = cp.Variable(m)
objective = cp.Minimize(u)
constraints = [cp.max(matrix(A[i,:])*p_cp,cp.inv_pos(matrix(A[i,:])*p_cp))<=u for i in range(n)]
constraints.extend([p_cp<=1, p_cp>=0])
p5 = cp.Problem(objective, constraints)
result = p5.solve();
f_5 = np.max(np.abs(log(A*matrix(p_cp.value))))
print p_cp.value
print f_5














