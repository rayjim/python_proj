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
        
def rotation_matrix(a):
    R = np.eye(4)
    R[:3,:3]= linalg.expm(np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]]))
    return R