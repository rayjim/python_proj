# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 18:06:52 2014
speed up computation for solving linear equation
@author: ray
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy as sci
import time
import scipy.sparse.linalg as splin

n = 2000
k = 100
delta = 1
eta = 1

data_mat=loadmat('data_sol.mat')
A = data_mat['A']
b = data_mat['b']

e = np.ones((n,1))
D = sci.sparse.spdiags(np.hstack((-e,2*e,-e)).T,np.array([-1,0,1]),n,n)
D.data[1,0]=1
D.data[1,n-1]=1
#I = np.eye(n)
I = sci.sparse.eye(n)
#I = sci.sparse.spdiags(np.hstack((e)).T,np.array([0]),n,n)
F = np.dot(A.T,A)+eta*I++delta*D
P = delta*D.data
P[1,:] = eta*I.data + delta*D.data[1,:]
#P = D+I
#P=sci.sparse.csr_matrix(P)
g = np.dot(A.T,b)

# Directly computing optimal solution
print ''
print 'Directly computing solution'
print ''
s1 = time.time()
#x_gen = np.dot(np.linalg.inv(F),g)
x_gen = sci.linalg.solve(F,g)
s2 = time.time()
print 'Done in',s2-s1,'sec'
print ''
print 'Computing solution using efficient method'
print ''

t1 = time.time()
#Z_0 = np.dot(sci.linalg.inv(P),np.hstack((g,A.T)))
#Z_0 = np.linalg.solve(P,np.hstack((g,A.T)))
Z_0 = sci.linalg.solve_banded((1,1),P,np.hstack((g,A.T)))
z_1 = Z_0[:,0]
Z_2 = Z_0[:,1:k+1]
#z_1 = sci.linalg.solve_banded((1,1),P,g)
#Z_2 = sci.linalg.solve_banded((1,1),P,A.T)
z_3 = np.linalg.solve(np.eye(k)+np.dot(A,Z_2),np.dot(A,z_1))
x_eff = z_1-np.dot(Z_2,z_3)
t2 = time.time()
print "Done in ", t2-t1,"sec"
print 'error is', np.linalg.norm(x_eff-x_gen.flatten())/np.linalg.norm(x_gen)


from scipy import optimize
print "Using optimazatin tools"
def f(x):
#    e = np.ones((n,1))
#    D = sci.sparse.spdiags(np.hstack((-e,2*e,-e)).T,np.array([-1,0,1]),n,n)
#    D.data[1,0]=1
#    D.data[1,n-1]=1
    return np.linalg.norm(np.dot(A,x)-b)+np.linalg.norm(np.dot(D.todense(),x))+np.linalg.norm(x)
t1 = time.time()
x_0 = np.zeros((2000,1))
optimize.fmin_bfgs(f,x_0)
t2 = time.time()
print "using ", t2-t1,"sec"