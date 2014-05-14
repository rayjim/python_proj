# -*- coding: utf-8 -*-
"""
Created on Wed May 14 18:11:48 2014

@author: admin
"""

import pickle
import bayes
import imtools
import numpy as np

# load 2D example points using Pickle
with open('points_ring.pkl','r') as f:
    class_1 = pickle.load(f)
    class_2 = pickle.load(f)
    labels = pickle.load(f)
    
#train Bayes classifier
bc = bayes.BayesClassifier()
bc.train([class_1,class_2],[1,-1])

#with open('points_normal.pkl','r') as f:
#    class_1= pickle.load(f)
#    class_2= pickle.load(f)
#    labels = pickle(f)
    
    
#test on some points
print bc.classify(class_1[:10])[0]
def classify(x,y,bc=bc):
    points=np.vstack((x,y))
    return bc.classify(points.T)[0]
    
imtools.plot_2D_boundary([-6,6,-6,6],[class_1,class_2],classify,[1,-1])


