# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 15:28:58 2014
This is the convex optimazation example for 3way classifcation
@author: ray
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import cvxpy as cp

np.random.seed(1)
data_mat=loadmat('data_sep.mat')
X = data_mat['X']
Y = data_mat['Y']
Z = data_mat['Z']



#######################
#example values
#
#a1 = np.array([1,1]).T
#a2 = np.array([1,-5]).T
#a3 = np.array([-1,-1]).T
#b1 = 0
#b2 = 0
#b3 = 0
#######################

a1 = cp.Variable(2,1)
a2 = cp.Variable(2,1)
a3 = cp.Variable(2,1)
b1 = cp.Variable(1)
b2 = cp.Variable(1)
b3 = cp.Variable(1)
obj = cp.Minimize(0)
constraints1 = [a1.T*X-b1>=cp.max(a2.T*X-b2,a3.T*X-b3)+1]
constraints2 = [a2.T*Y-b2>=cp.max(a1.T*Y-b1,a3.T*Y-b3)+1]
constraints3 = [a3.T*Z-b3>=cp.max(a1.T*Z-b1,a2.T*Z-b2)+1]
constraints4 =[a1+a2+a3==0]
constraints5 =[b1+b2+b3==0]
constraints = constraints1+constraints2+constraints3#+constraints4+constraints5
pro = cp.Problem(obj,constraints)
pro.solve(solver=cp.CVXOPT)
a1 = np.array(a1.value.T).flatten()
a2 = np.array(a2.value.T).flatten()
a3 = np.array(a3.value.T).flatten()
b1 = b1.value
b2 = b2.value
b3 = b3.value

######################
#find maximally confusing point
# [(a1-a2);(a1-a3)]/[(b1-b2);(b1-b3)]
p = np.dot(np.linalg.inv(np.vstack(((a1-a2),(a1-a3)))),
np.vstack(((b1-a2),(b1-a3))))
#plot
t = np.arange(-7,7,0.01)
u1 = a1-a2
u2 = a2-a3
u3 = a3-a1
v1 = b1-b2
v2 = b2-b3
v3 = b3-b1
line1 = (-t*u1[0]+v1)/u1[1]
idx1 = np.nonzero(np.dot(u2,np.vstack((t,line1)))-v2>0)
line2 = (-t*u2[0]+v2)/u2[1]
idx2 = np.nonzero(np.dot(u3,np.vstack((t,line2)))-v3>0)
line3 = (-t*u3[0]+v3)/u3[1]
idx3 = np.nonzero(np.dot(u1,np.vstack((t,line3)))-v1>0)
plt.plot(X[0,:],X[1,:],'*',Y[0,:],Y[1,:],'ro',Z[0,:],Z[1,:],'g+',
         t[idx1],line1[idx1],'k',t[idx2],line2[idx2],'k',t[idx3],line3[idx3],'k')
plt.axis([-7, 7, -7, 7])