# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:32:16 2014

@author: admin
"""
import pickle
import knn
import imtools
from numpy import *
#definefunctionforplotting

#load2DpointsusingPickle
with open('points_normal.pkl','r') as f:
    class_1=pickle.load(f)
    class_2=pickle.load(f)
    labels=pickle.load(f)
model=knn.KnnClassifier(labels,vstack((class_1,class_2)))



#definefunctionforplotting
def classify(x,y,model=model):
    return array([model.classify([xx,yy]) for(xx,yy) in zip(x,y)])

#plottheclassificationboundary
imtools.plot_2D_boundary([-6,6,-6,6],[class_1,class_2],classify,[1,-1])
show()
figure()
#loadtestdatausingPickle
with open('points_ring.pkl','r') as f:
    class_1=pickle.load(f)
    class_2=pickle.load(f)
    labels=pickle.load(f)
model=knn.KnnClassifier(labels,vstack((class_1,class_2)))
#testonthefirstpoint
    #definefunctionforplotting


#plottheclassificationboundary
imtools.plot_2D_boundary([-6,6,-6,6],[class_1,class_2],classify,[1,-1])

show()