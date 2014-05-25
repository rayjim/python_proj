# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:11:17 2014

@author: admin
"""
from numpy.random import randn
import pickle
from numpy import *

n=200
#twonormaldistributions
class_1=0.6*randn(n,2)
class_2=1.2*randn(n,2)+array([5,1])
labels=hstack((ones(n),-ones(n)))
#savewithPickle
with open('points_normal_test.pkl','w') as f:
    pickle.dump(class_1,f)
    pickle.dump(class_2,f)
    pickle.dump(labels,f)
    
#normaldistributionandringaroundit
class_1=0.6*randn(n,2)
r=0.8*randn(n,1)+5
angle=2*pi*randn(n,1)
class_2=hstack((r*cos(angle),r*sin(angle)))
labels=hstack((ones(n),-ones(n)))
#savewithPickle
with open('points_ring_test.pkl','w') as f:
    pickle.dump(class_1,f)
    pickle.dump(class_2,f)
    pickle.dump(labels,f)
    
    
