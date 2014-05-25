# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
D:\bao\WinPython-64bit-2.7.5.3\settings\.spyder2\.temp.py
"""

import pickle
from svmutil import *
import imtools
import numpy as np

# load 2D example points using Pickle
with open('points_normal.pkl','r') as f:
    class_1 = pickle.load(f)
    class_2 = pickle.load(f)
    labels = pickle.load(f)
    
#convert to lists for libsvm

class_1 = map(list,class_1)
class_2 = map(list,class_2)
labels = list(labels)
samples = class_1+class_2

#create SVM
prob = svm_problem(labels,samples)
param = svm_parameter('-t 2')
# train SVM on data
m = svm_train(prob,param)

res = svm_predict(labels,samples,m)

with open('points_normal_test.pkl','r') as f:
    class_1 = pickle.load(f)
    class_2 = pickle.load(f)
    labels = pickle.load(f)
    
#convert to lists for libsvm
class_1 = map(list,class_1)
class_2 = map(list,class_2)
#definefunctionforplotting
def predict(x,y,model=m):
    return np.array(svm_predict([0]*len(x),zip(x,y),model)[0])
#plottheclassificationboundary
imtools.plot_2D_boundary([-6,6,-6,6],[np.array(class_1),np.array(class_2)],predict,[-1,1])
show()