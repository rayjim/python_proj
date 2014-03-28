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
m = 200
nn = 100
plt.close('all')
ALPHA = 0.01 # parameters for 
BETA = 0.5
MAXITERS = 1000 # maximum iteration
NTTOL = 1e-9
GRADTOL = 1e-3

# generate random problem
A = np.random.rand(m,nn)


######### Approximation 1 ##################################


steps = [1,15,20,30]
for elem in range(len(steps)):
    print "steps=",steps[elem]
    vals = []
    x = np.zeros((nn,1))
    flops =[]
    flop_cum = 0
    for iter in range(MAXITERS):
        val = -np.sum(np.log(1-np.dot(A,x)))-np.sum(np.log(1-x**2))
        vals.append(val)
        flops.append(flop_cum)
        d = 1/(1-np.dot(A,x))
        grad = np.dot(A.transpose(),d)-1/(1+x)+1/(1-x)
        if (iter%steps[elem]==0):
            hess = np.dot(np.dot(A.transpose(),np.diag((d**2)[:,0])),A)+np.diag((1/(1+x)**2+1/(1-x)**2)[:,0])
            L = np.linalg.cholesky(hess)
            flop_cum = nn**3/3
            print 'flop_cum for is',flop_cum
        else:
            flop_cum = 0
         
        v = -np.dot(np.linalg.inv(L.transpose()),np.dot(np.linalg.inv(L),grad))
        flop_cum = flop_cum+2*nn**2
        
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
    
     
    print iter
    optival = vals[len(vals)-1]
    cflops = np.cumsum(flops)
    plt.figure(1)
    plt.semilogy(cflops[0:len(vals)-1],vals[0:len(vals)-1]-optival,'-',cflops,vals-optival,'o',label="test")


