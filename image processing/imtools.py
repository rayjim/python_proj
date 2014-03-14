#from PIL import Image
from pylab import *
from numpy import *
import os
def get_imlist(path):
    """Returns a list of filenames for
    all jpg images in a directory"""
    return[os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]
def histeq(im, nbr_bins=256):
    """ Histogram equalization of a grayscale image"""
    
    # get image histogram
    imhist,bins = histogram(im.flatten(),nbr_bins,normed=True)
    cdf = imhist.cumsum()
    cdf = 255*cdf/cdf[-1]
    
    im2 = interp(im.flatten(),bins[:-1],cdf)
    return im2.reshape(im.shape),cdf

def pca(X):
    
    num_data,dim = X.shape
    
    mean_X = X.mean(axis = 0)
    X = X - mean_X
    
    if dim > num_data:
        #PCA - compact trick used
        M= dot(X, X.T)
        e,EV= linalg.eigh(M)
        tmp = dot(X.T,EV).T
        V = tmp[::-1]
        S = sqrt(e)[::-1]
        for i in range(V.shape[1]):
            V[:,i] /= S
    else:
        U,S,V = linalg.svd(X)
        V = V[:num_data]
        # return the projection matrix, the variance and the mean 
    return V,S, mean_X

def denoise (im, U_init, tolerance=0.1, tau=0.125,tv_weight=100):
        """An implementation of the Rudin-Osher-Fatemi(ROF)
        """
        m,n = im.shape 
        # initialize
        U = U_init
        Px = im
        Py = im
        error = 1
        
        while(error>tolerance):
            Uold = U
            GradUx = roll(U, -1, axis = 1)-U
            GradUy = roll(U, -1, axis = 0)-U
            
            PxNew = Px + (tau/tv_weight)*GradUx
            PyNew = Py + (tau/tv_weight)*GradUy
            NormNew = maximum(1, sqrt(PxNew**2+PyNew**2))
            
            Px = PxNew/NormNew
            Py = PyNew/NormNew
            
            RxPx = roll(Px,1,axis = 1)
            RyPy = roll(Py,1,axis = 0)
            
            DivP = (Px-RxPx)+(Py-RyPy)
            U = im +tv_weight*DivP
            
            error = linalg.norm(U-Uold)/sqrt(n*m)
      
        return U, im-U