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

##############################################################################
#The following is used for Harris 
##############################################################################
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

def get_descriptors(image, filtered_coords, wid=5):
    """ For each point return pixel values around the point
    using a neibourhood of width 2*wid+1
    """
    desc = []
    for coords in filtered_coords:
        patch = image[coords[0]-wid:coords[0]+wid+1,
                      coords[1]-wid:coords[1]+wid+1].flatten()
        desc.append(patch)
        
    return desc
    
def match(desc1, desc2, threshold=0.5):
    """ For each corner point descriptor in the first image,
    select its match to second image using 
    normalized cross correlation."""
    
    n = len(desc1[0])
    #pair-wise distance
    d = -ones((len(desc1),len(desc2)))
    for i in range(len(desc1)):
        for j in range(len(desc2)):
            d1 = (desc1[i]-mean(desc1[i]))/std(desc1[i])
            d2 = (desc2[j]-mean(desc2[j]))/std(desc2[j])
            ncc_value = sum(d1*d2)/(n-1)
            if ncc_value > threshold:
                d[i,j]= ncc_value
            
    ndx = argsort(-d)
    matchscores = ndx[:,0]
    
    return matchscores
    
 
def match_twosided(desc1,desc2,threshold=0.5):
    """ Two-sided symmetric version of match()."""
    matches_12 = match(desc1,desc2,threshold)
    matches_21 = match(desc2,desc1,threshold)
    ndx_12 = where(matches_12>=0)[0]
    
    # remove matches that are not symmetric
    for n in ndx_12:
        if matches_21[matches_12[n]] !=n:
            matches_12[n] = -1
            
    return matches_12
    
    
def appendimages(im1,im2):
    """"Return a new image that appeds the two images side by side."""
    
    # select the image with the fewest rows and fill in enough empty rows
    rows1 = im1.shape[0]
    rows2 = im2.shape[0]
    
    if rows1 <rows2:
        im1 = concatenate((im1,zeros((rows2-rows1,im1.shape[1]))), axis = 0)
    elif rows1 >rows2:
        im2 = concatenate((im2,zeros((rows1-rows2,im2.shape[1]))), axis = 0)
        
    return concatenate((im1,im2),axis = 1)

def plot_matches(im1,im2,locs1,locs2,matchscores,show_below=True)   :
    """ Show a figure with lines joining the accepted matches
    input: im1, im2(image as arrays), locs1, locs2(feature location)
    """
    
    im3 = appendimages(im1, im2)
    imshow(im3)
    
    cols1 = im1.shape[1]
    for i,m in enumerate(matchscores):
        if m>0:
            plot([locs1[i][1],locs2[m][1]+cols1],[locs1[i][0],locs2[m][0]],'c')
            
    
    
    
    
    
    
    
    
    
    
    














