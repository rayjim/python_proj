from scipy import linalg, matrix
from numpy import *






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
        
#solution 1
nopts = 1000
p=logspace(-3,0,nopts)
f=zeros(p.size)
for k in range(nopts):
    f[k] = np.max(np.abs(log(A*matrix((p[k]*ones((m,1)))))))


print np.min(f)
print p[argmin(f)]


#solution 2 least square
b = ones((n,1))
p_ls_sat = np.linalg.lstsq(A, b)[0]
p_ls_sat = np.minimum(p_ls_sat,ones((m,1)))
p_ls_sat = np.maximum(p_ls_sat,zeros((m,1)))
print p_ls_sat
val_ls_sat = np.max(np.abs(log(A*matrix(p_ls_sat))))
print val_ls_sat


#solution 3 regularizepd least squares




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




#solution 4 chebyshev approximation
from cvxpy import Minimize, normInf,Variable,Problem,inv_pos
x=Variable (m,1)
objective = Minimize(normInf(matrix(A)*x-ones((n,1))))
constraints =[x>=0,x<=1]
pro = Problem(objective, constraints) 
result = pro.solve()
print x.value
val_ls_chev = np.max(np.abs(log(A*matrix(x.value))))
print val_ls_chev


#solution 5 cvxpy


from cvxpy import max
y=Variable (m,1)
Am = matrix(A)
qq = [max(Am[i,:]*y,inv_pos(Am[i,:]*y)) for i in range(n)]
objective1 = Minimize(max(*qq))
constraints1 =[y>=0,y<=1]
pro1 = Problem(objective1, constraints1) 
result1 = pro1.solve()
print y.value
val_ls_cvx = np.max(np.abs(log(A*matrix(y.value))))
print val_ls_cvx


#solution 6 cvxpy equvelent


z=Variable (m,1)
u = Variable(1)
qq = [(max(Am[i,:]*z,inv_pos(Am[i,:]*z))<=u) for i in range(n)]
objective2 = Minimize(u)
pp =[z>=0,z<=1]
constraints2 = pp+qq
pro2 = Problem(objective2, constraints2) 
result1 = pro2.solve()
print z.value
val_ls_cvx = np.max(np.abs(log(A*matrix(z.value))))
print val_ls_cvx

