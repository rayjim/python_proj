# -*- coding: utf-8 -*-
"""
Created on Tue Apr 08 10:55:52 2014
sfm
@author: admin
"""
from numpy import *
from pylab import *
def compute_fundamental(x1,x2):
    """Computesthefundamentalmatrixfromcorrespondingpoints
    (x1,x23*narrays)usingthenormalized8pointalgorithm.
    eachrowisconstructedas
    [x’*x,x’*y,x’,y’*x,y’*y,y’,x,y,1]"""
    n=x1.shape[1]
    if x2.shape[1]!=n:
       raise ValueError("Number of points don’t match.")
    #build matrix forequations
    A=zeros((n,9))
    for i in range(n):
        A[i]=[x1[0,i]*x2[0,i],x1[0,i]*x2[1,i],x1[0,i]*x2[2,i],
        x1[1,i]*x2[0,i],x1[1,i]*x2[1,i],x1[1,i]*x2[2,i],
        x1[2,i]*x2[0,i],x1[2,i]*x2[1,i],x1[2,i]*x2[2,i]]
    #compute linear least square solution
    U,S,V=linalg.svd(A)
    F=V[-1].reshape(3,3)
    #constrainF
    #make rank2 by zeroing outlastsingularvalue
    U,S,V=linalg.svd(F)
    S[2]=0
    F=dot(U,dot(diag(S),V))
    return F
    
def compute_epipole(F):
    """Computesthe(right)epipolefroma
    fundamentalmatrixF.
    (UsewithF.Tforleftepipole.)"""
    #returnnullspaceofF(Fx=0)
    U,S,V=linalg.svd(F)
    e=V[-1]
    return e/e[2]
    
def plot_epipolar_line(im,F,x,epipole=None,show_epipole=True):
    """PlottheepipoleandepipolarlineF*x=0
    inanimage.Fisthefundamentalmatrix
    andxapointintheotherimage."""
    m,n=im.shape[:2]
    line=dot(F,x)
    #epipolarlineparameterandvalues
    t=linspace(-50000,n,1000)
    lt=array([(line[2]+line[0]*tt)/(-line[1])for tt in t])
    #takeonlylinepointsinsidetheimage
    ndx=(lt>=0)&(lt<m)
    plot(t[ndx],lt[ndx],linewidth=2)
    if show_epipole:
        if epipoleisNone:
            epipole=compute_epipole(F)
    plot(epipole[0]/epipole[2],epipole[1]/epipole[2],'r*')
    
def triangulate_point(x1,x2,P1,P2):
    """Pointpairtriangulationfrom
    leastsquaressolution."""
    M=zeros((6,6))
    M[:3,:4]=P1
    M[3:,:4]=P2
    M[:3,4]=-x1
    M[3:,5]=-x2
    U,S,V=linalg.svd(M)
    X=V[-1,:4]
    return X/X[3]

def triangulate(x1,x2,P1,P2):
    """Two-viewtriangulationofpointsin
    x1,x2(3*nhomog.coordinates)."""
    n=x1.shape[1]
    if x2.shape[1]!=n:
        raise ValueError("Numberofpointsdon’tmatch.")
    X=[triangulate_point(x1[:,i],x2[:,i],P1,P2) for i in range(n)]
    return array(X).T