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
    
def compute_P(x,X):
    """Computecameramatrixfrompairsof
    2D-3Dcorrespondences(inhomog.coordinates)."""
    n=x.shape[1]
    if X.shape[1]!=n:
        raiseValueError("Numberofpointsdon'tmatch.")
    #creatematrixforDLTsolution
    M=zeros((3*n,12+n))
    for i in range(n):
        M[3*i,0:4]=X[:,i]
        M[3*i+1,4:8]=X[:,i]
        M[3*i+2,8:12]=X[:,i]
        M[3*i:3*i+3,i+12]=-x[:,i]
    U,S,V=linalg.svd(M)
    return V[-1,:12].reshape((3,4))
def compute_P_from_fundamental(F):
    """Computesthesecondcameramatrix(assumingP1=[I0])
    fromafundamentalmatrix."""
    e=compute_epipole(F.T)#leftepipole
    Te=skew(e)
    return vstack((dot(Te,F.T).T,e)).T
def skew(a):
    """SkewmatrixAsuchthataxv=Avforanyv."""
    return array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    
def compute_P_from_essential(E):
    """Computesthesecondcameramatrix(assumingP1=[I0])
    from anessentialmatrix.Outputisalistoffour
    possiblecameramatrices."""
    #makesureEisrank2
    U,S,V=svd(E)
    if det(dot(U,V))<0:
        V=-V
    E=dot(U,dot(diag([1,1,0]),V))
    #creatematrices(Hartleyp258)
    Z=skew([0,0,-1])
    W=array([[0,-1,0],[1,0,0],[0,0,1]])
    #returnallfoursolutions
    P2=[vstack((dot(U,dot(W,V)).T,U[:,2])).T,
        vstack((dot(U,dot(W,V)).T,-U[:,2])).T,
        vstack((dot(U,dot(W.T,V)).T,U[:,2])).T,
        vstack((dot(U,dot(W.T,V)).T,-U[:,2])).T]
        
    return P2
class RansacModel(object):
    """Classforfundmentalmatrixfitwithransac.pyfrom
    http://www.scipy.org/Cookbook/RANSAC"""
    def __init__(self,debug=False):
        self.debug=debug
    def fit(self,data):
        """Estimatefundamentalmatrixusingeight
        selectedcorrespondences."""
        #transposeandsplitdataintothetwopointsets
        data=data.T
        x1=data[:3,:8]
        x2=data[3:,:8]
        #estimatefundamentalmatrixandreturn
        F=compute_fundamental_normalized(x1,x2)
        return F
    def get_error(self,data,F):
        """Computex^TFxforallcorrespondences,
        returnerrorforeachtransformedpoint."""
        #transposeandsplitdataintothetwopoint
        data=data.T
        x1=data[:3]
        x2=data[3:]
        #Sampsondistanceaserrormeasure
        Fx1=dot(F,x1)
        Fx2=dot(F,x2)
        denom=Fx1[0]**2+Fx1[1]**2+Fx2[0]**2+Fx2[1]**2
        err=(diag(dot(x1.T,dot(F,x2))) )**2/denom
        #returnerrorperpoint
        return err        
def compute_fundamental_normalized(x1,x2):
    """Computesthefundamentalmatrixfromcorrespondingpoints
    (x1,x23*narrays)usingthenormalized8pointalgorithm."""
    n=x1.shape[1]
    if x2.shape[1]!=n:
        raise ValueError("Numberofpointsdon’tmatch.")
    #normalizeimagecoordinates
    x1=x1/x1[2]
    mean_1=mean(x1[:2],axis=1)
    S1=sqrt(2)/std(x1[:2])
    T1=array([[S1,0,-S1*mean_1[0]],[0,S1,-S1*mean_1[1]],[0,0,1]])
    x1=dot(T1,x1)
    x2=x2/x2[2]
    mean_2=mean(x2[:2],axis=1)
    S2=sqrt(2)/std(x2[:2])
    T2=array([[S2,0,-S2*mean_2[0]],[0,S2,-S2*mean_2[1]],[0,0,1]])
    x2=dot(T2,x2)
    #computeFwiththenormalizedcoordinates
    F=compute_fundamental(x1,x2)
    #reversenormalization
    F=dot(T1.T,dot(F,T2))
    return F/F[2,2]
def F_from_ransac(x1,x2,model,maxiter=5000,match_theshold=1e-6):
    """RobustestimationofafundamentalmatrixFfrompoint
    correspondencesusingRANSAC(ransac.pyfrom
    http://www.scipy.org/Cookbook/RANSAC).
    input:x1,x2(3*narrays)pointsinhom.coordinates."""
    import ransac
    data=vstack((x1,x2))
    #computeFandreturnwithinlierindex
    F,ransac_data=ransac.ransac(data.T,model,8,maxiter,match_theshold,20,return_all=True)
    return F, ransac_data['inliers']