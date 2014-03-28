# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:44:22 2014

@author: admin
"""
import numpy as np
import matplotlib.pyplot as plt
#### The following is the implementation for gradient descent ###
### problem definition ###
m = 2000
n = 1000
plt.close('all')
ALPHA = 0.01 # parameters for 
BETA = 0.5
MAXITERS = 1000 # maximum iteration
NTTOL = 1e-9
GRADTOL = 1e-3

# generate random problem
A = np.random.rand(m,n)
######### Approximate 2##################################

vals = []
steps = []

x = np.zeros((n,1))

for iter in range(MAXITERS):
    
     val = -np.sum(np.log(1-np.dot(A,x)))-np.sum(np.log(1-x**2))
     vals.append(val)
     d = 1/(1-np.dot(A,x))
     grad = np.dot(A.transpose(),d)-1/(1+x)+1/(1-x)
     hess = np.dot(np.dot(A.transpose(),np.diag((d**2)[:,0])),A)+np.diag((1/(1+x)**2+1/(1-x)**2)[:,0])
     H = np.diag(np.diag(hess))
     print np.linalg.norm(grad)
     if np.linalg.norm(grad)<GRADTOL:
         print 'finish'         
         break     

     v = -np.dot(np.linalg.inv(H),grad)
     fprime =np.dot(grad.transpose(),v)
     if (fprime >0):
         print '>0'
     t = 1
     while(np.max(np.dot(A,(x+t*v)))>=1) or (np.max(np.abs(x+t*v))>=1):
    #feasibility condition: value of log should be large
         t = BETA*t
     while -np.sum(np.log(1-np.dot(A,x+t*v)))-np.sum(np.log(1-(x+t*v)**2))>val+ALPHA*t*fprime:
         t = BETA*t
    #print 'second t',t
     x = x+t*v
     steps.append(t)
print iter
optival = vals[len(vals)-1]
plt.figure(2)
plt.semilogy(range(len(vals)),vals-optival,'-',range(len(vals)),vals-optival,'o')
plt.text(len(vals)-1,vals[len(vals)-2]-optival,"Newton method")
