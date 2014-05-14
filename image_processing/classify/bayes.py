# -*- coding: utf-8 -*-
"""
Created on Wed May 14 17:54:49 2014

@author: admin
"""
import numpy as np
class BayesClassifier(object):
    
    def __init__(self):
        """Initializing classifier with training data"""
        self.labels=[]
        self.mean=[]
        self.var =[]
        self.n = 0
        
    def train(self,data,labels=None):
        """Train on data(List of arrays n*dim)
        Labels are optional, default is 0...n-1"""
        if labels == None:
            labels = range(len(data))
        self.labels = labels
        self.n = len(labels)
        
        for c in data:
            self.mean.append(np.mean(c,axis=0))
            self.var.append(np.var(c,axis=0))
            
    def classify(self,points):
        """classify the points by computing probabilities for 
        each class and return most probable label"""
        #compute probabilities for each class
        est_prob = np.array([gauss(m,v,points)for m,v in zip(self.mean,self.var)])
        #get index of highest probability, this gives class label
        ndx = est_prob.argmax(axis=0)
        est_labels= np.array([self.labels[n] for n in ndx])
        
        return est_labels,est_prob
def gauss(m,v,x):
    """Evaluate Gaussian in d-dimensions with independent mean m an dvariance v"""
    if len(x.shape)==1:
        n,d=1,x.shape[0]
    else:
        n,d = x.shape
        
    S = np.diag(1/v)
    x = x-m
    y = np.exp(-0.5*np.diag(np.dot(x,np.dot(S,x.T))))
    return y*(2*np.pi)**(-d/2.0)/(np.sqrt(np.prod(v))+1e-6)        
    