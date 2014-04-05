# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 20:05:55 2014

@author: ray
"""

from scipy import linalg
import numpy as np
class Camera(object):
    """ Class for represeting pin-hole cameras"""
    
    def __init__(self,P):
        """ Initialize P = K[R|t] camera model"""
        self.P = P
        self.K = None
        self.R = None
        self.t = None
        self.c = None
    def project(self,X):
        x = np.dot(self.P,X)
        for i in range(3):
            x[i]/=x[2]
        return x
    def factor(self):
        """Factorize the camera matrix into K, R, t as P=K[P|t]"""
        K,R = linalg.rq(self.P[:,:3])
        #make diagonal of K positive
        T = np.diag(np.sign(np.diag(K)))
        if linalg.det(T)<0:
            T[1,1]*=-1
            
        self.K = np.dot(K,T)
        self.R = np.dot(T,R)
        self.t = np.dot(linalg.inv(self.K),self.P[:,3])
        
        return self.K, self.R, self.t
    def center(self):
        """ compute and return the camera center."""
        if self.c is not None:
           return self.c
        else:
            # compute c by factoring
           self.factor()
           self.c=-np.dot(self.R.T,self.t)
           return self.c
    
        
def rotation_matrix(a):
    R = np.eye(4)
    R[:3,:3]= linalg.expm(np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]]))
    return R
    


