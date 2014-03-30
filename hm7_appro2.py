# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:44:22 2014
approximate hessian with its diagnol
@author: admin
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import scipy as sci
import time
#### The following is the implementation for gradient descent ###
### problem definition ###
m = 200
n = 100
plt.close('all')
ALPHA = 0.01 # parameters for 
BETA = 0.5
MAXITERS = 1000 # maximum iteration
NTTOL = 1e-9
GRADTOL = 1e-3

# generate random problem
np.random.seed(1)
x=loadmat('data.mat')
A = x['A']
#A= np.random.rand(1,n)

######### Approximate 2##################################

vals = []


x = np.zeros((n,1))
t1 = time.time()
for iter in range(MAXITERS):
    
     val = -np.sum(np.log(1-np.dot(A,x)))-np.sum(np.log(1+x))-np.sum(np.log(1-x))
     vals.append(val)
     d = 1/(1-np.dot(A,x))
     grad = np.dot(A.transpose(),d)-1/(1+x)+1/(1-x)
     hess = np.dot(np.dot(A.transpose(),np.diag((d**2)[:,0])),A)+\
     np.diag((1/(1+x)**2+1/(1-x)**2)[:,0])
     #H = hess
     H = np.diag(np.diag(hess))
     print "cond = ",np.linalg.cond(hess)
     print "grad = ",np.linalg.norm(grad)
     
     if np.linalg.norm(grad)<GRADTOL:
         print 'Decent finished after ',iter,' iteration'         
         break     

     #v = -np.dot(np.linalg.inv(H),grad)
     #v = -np.dot(np.linalg.inv(H),grad)
     v = -np.linalg.solve(H,grad)
     fprime =np.dot(grad.transpose(),v)
    # print "decre = ",np.abs(fprime)
     if (fprime >0):
         print '>0'
     t = 1
     while(np.max(np.dot(A,(x+t*v)))>=1) or (np.max(np.abs(x+t*v))>=1):
    #feasibility condition: value of log should be large
         t = BETA*t
     while -np.sum(np.log(1-np.dot(A,x+t*v)))-np.sum(np.log(1-(x+t*v)**2))>\
     val+ALPHA*t*fprime:
         t = BETA*t
    
    # print 'second t',t
    
     x = x+t*v
#############################################################
t2 = time.time()
print t2-t1,'sec'

optival = vals[len(vals)-1]
plt.figure(2)
plt.semilogy(range(len(vals)),vals-optival,'-')
plt.text(len(vals)-1,vals[len(vals)-2]-optival,"Newton method")
