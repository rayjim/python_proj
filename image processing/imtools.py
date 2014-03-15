"""
This file containing examples taken from computer vision with python
author(implement): ray
"""
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

from scipy.ndimage import filters

def compute_harris_response(im,sigma = 3):
    """
    compute harris corner detector response function for each pixel    
    return the Harris corner detector response function
    """
    
    #derivatives
    imx = zeros(im.shape)
    filters.gaussian_filter(im,(sigma,sigma),(0,1),imx)
    imy = zeros(im.shape)
    filters.gaussian_filter(im,(sigma,sigma),(1,0),imy)
    
    # compute components of the Harris corner
    Wxx = filters.gaussian_filter(imx*imx,sigma)
    Wxy = filters.gaussian_filter(imx*imy,sigma)
    Wyy = filters.gaussian_filter(imy*imy,sigma)
    
    #determinant and trace
    Wdet = Wxx*Wyy - Wxy**2
    Wtr =  Wxx+ Wyy
    return Wdet/Wtr

def get_harris_points(harrisim, min_dist=10,threshold=0.1):
     """ Return corners form a Harris response image
        min_dist is the minimum number of pixels seperate corners and 
        image bondary        
     """
    # find top corner candidates above a threshold
     corner_threshold = harrisim.max()*threshold
     harrisim_t = (harrisim>corner_threshold)*1
     
     # get coordinates of the candidates
     coords = array(harrisim_t.nonzero()).T
     
     #... and their values
     candidate_values =[harrisim[c[0],c[1]] for c in coords]
     
     # sort candidates
     index = argsort(candidate_values)
     
     # store allowed point locations in array
     allowed_locations = zeros(harrisim.shape)
     allowed_locations[min_dist:-min_dist,min_dist:-min_dist] = 1
     
     # select the best points taking min_distance into account
     filtered_coords = []
     for i in index:
         if allowed_locations[coords[i,0],coords[i,1]]==1:
             filtered_coords.append(coords[i])
             allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                               (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0
     return filtered_coords
    
def plot_harris_points(image,filtered_coords):
    """"Plots corners found in image."""
    
    figure()
    gray()
    imshow(image)
    plot([p[1] for p in filtered_coords],[p[0] for p in filtered_coords], '*')
    axis('off')
    show()
















