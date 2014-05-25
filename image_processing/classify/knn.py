# -*- coding: utf-8 -*-
"""
Created on Mon May 12 10:06:58 2014

@author: admin
"""
import numpy as np

class KnnClassifier(object):
    def __init__(self,labels,samples):
        """Initialize classifier with training data."""
        self.labels=labels
        self.samples=samples
    def classify(self,point,k=3):
        """Classify a point against knearest
        in the training data,return label."""
        #computedistancetoalltrainingpoints
        point = np.array(point)
        dist=np.array([L2dist(point,s) for s in self.samples])
        #sortthem
        ndx=dist.argsort()
        #usedictionarytostoretheknearest
        votes={}
        for i in range(k):
            label=self.labels[ndx[i]]
            votes.setdefault(label,0)
            votes[label]+=1
        return max(votes)
        
def L2dist(p1,p2):
    return np.sqrt(sum((p1-p2)**2))
    


