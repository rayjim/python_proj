# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:57:20 2014

@author: admin
"""

from svmutil import *
from ocr import *
import imtools
import numpy as np
from PIL import *

#Training data
features,labels = load_ocr_data('data/ocr_data/training/')

#Testing data
test_features,test_labels = load_ocr_data('data/ocr_data/testing/')

#train a linear SVM classifier

features=map(list,features)
test_features=map(list,test_features)

prob = svm_problem(labels,features)
param = svm_parameter('-t 0')

m = svm_train(prob,param)

#how did the training do?
res = svm_predict(labels,features,m)
#
##how dose it perform on the test set
#res = svm_predict(test_labels,test_features,m)

#imname = 'data/sudokus/sudoku21.jpg'
#vername = 'data/sudokus/sudoku21.sud'
#
#im=np.array(Image.open(imname).convert('L'))
#
#x = find_sudoku_edges(im,axis=0)
#y = find_sudoku_edges(im,axis=1)
#
##cropcellsandclassify
#crops=[]
#for col in range(9):
#    for row in range(9):
#        crop=im[y[col]:y[col+1],x[row]:x[row+1]]
#        crops.append(compute_feature(crop))
#res=svm_predict(loadtxt(vername),map(list,crops),m)[0]
#res_im=np.array(res).reshape(9,9)
#print 'Result:'
#print res_im


import homography
from scipy import ndimage

imname='data/sudokus/sudoku8.jpg'
vername='data/sudokus/sudoku8.sud'
im=np.array(Image.open(imname).convert('L'))
#markcorners
figure()
imshow(im)
gray()
x=ginput(4)
fp=array([np.array([p[1],p[0],1]) for p in x]).T
tp=array([[0,0,1],[0,1000,1],[1000,1000,1],[1000,0,1]]).T
#estimatethehomographyim
H=homography.H_from_points(tp,fp)
#helperfunctionforgeometric_transform
def warpfcn(x):
    x=array([x[0],x[1],1])
    xt=dot(H,x)
    xt=xt/xt[2]
    return xt[0],xt[1]
#warpimagewithfullperspectivetransform
im_g=ndimage.geometric_transform(im,warpfcn,(1000,1000))
x = find_sudoku_edges(im_g,axis=0)
y = find_sudoku_edges(im_g,axis=1)
#cropcellsandclassify\
#cropcellsandclassify
crops=[]
for col in range(9):
    for row in range(9):
        crop=im[y[col]:y[col+1],x[row]:x[row+1]]
        crops.append(compute_feature(crop))
res=svm_predict(loadtxt(vername),map(list,crops),m)[0]
res_im=np.array(res).reshape(9,9)
print 'Result:'
print res_im