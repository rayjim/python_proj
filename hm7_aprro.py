# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 07:19:23 2014
Newton method approximation
@author: admin
"""
# -*- coding: utf-8 -*-

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
NTTOL = 1e-8
GRADTOL = 1e-3

# generate random problem
A = np.random.rand(m,n)


######### Newton method ##################################
vals = []
steps = []

x = np.zeros((n,1))

for iter in range(MAXITERS):
     val = -np.sum(np.log(1-np.dot(A,x)))-np.sum(np.log(1-x**2))
     vals.append(val)
     d = 1/(1-np.dot(A,x))
     grad = np.dot(A.transpose(),d)-1/(1+x)+1/(1-x)
     hess = np.dot(np.dot(A.transpose(),np.diag((d**2)[:,0])),A)+np.diag((1/(1+x)**2+1/(1-x)**2)[:,0])
     v = -np.dot(np.linalg.inv(hess),grad)
     fprime =np.dot(grad.transpose(),v)
     if np.abs(fprime)<NTTOL:
         print 'finish'         
         break
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
plt.figure(1)
plt.semilogy(range(len(vals)),vals-optival,'-',range(len(vals)),vals-optival,'o')
plt.text(len(vals),vals[len(vals)-2]-optival,"N = 1")

#plt.text(len(vals)-1,vals[len(vals)-1]-optival,'test')
plt.figure(2)
plt.plot(range(len(steps)),steps,'-',range(len(steps)),steps,'o')


######### Approximation 1 ##################################


N = [10,15,20,30]
for nn in range(len(N)):
    print "N=",N[nn]
    vals = []
    steps = []
    x = np.zeros((n,1))
    for iter in range(MAXITERS):
        val = -np.sum(np.log(1-np.dot(A,x)))-np.sum(np.log(1-x**2))
        vals.append(val)
        d = 1/(1-np.dot(A,x))
        grad = np.dot(A.transpose(),d)-1/(1+x)+1/(1-x)
        if (iter%N[nn]==0):
            hess = np.dot(np.dot(A.transpose(),np.diag((d**2)[:,0])),A)+np.diag((1/(1+x)**2+1/(1-x)**2)[:,0])
        v = -np.dot(np.linalg.inv(hess),grad)
        fprime =np.dot(grad.transpose(),v)
        if np.abs(fprime)<NTTOL:
            print 'finish'         
            break
        t = 1
        while(np.max(np.dot(A,(x+t*v)))>=1) or (np.max(np.abs(x+t*v))>=1):
         #feasibility condition: value of log should be large
            t = BETA*t
        while -np.sum(np.log(1-np.dot(A,x+t*v)))-np.sum(np.log(1-(x+t*v)**2))>val+ALPHA*t*fprime:
            t = BETA*t
        #   print 'second t',t
        x = x+t*v
        steps.append(t)
     
    print iter
    optival = vals[len(vals)-1]
    plt.figure(1)
    plt.semilogy(range(len(vals)),vals-optival,'-',range(len(vals)),vals-optival,'o',label="test")
    plt.text(len(vals),vals[len(vals)-2]-optival,"N = "+map(str,N)[nn])    
    plt.figure(2)
    plt.plot(range(len(steps)),steps,'-',range(len(steps)),steps,'o')


