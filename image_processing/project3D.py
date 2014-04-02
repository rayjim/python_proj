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