# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 21:07:43 2014

@author: ray
"""

from scipy.cluster.vq import *
close('all')
class1 = 1.5 * randn(100,2)
class2 = randn(100,2) + array([5,5])
features = vstack((class1,class2))
centroids,variance = kmeans(features,3)
code,distance = vq(features,centroids)
figure()
ndx = where(code==0)[0] 
plot(features[ndx,0],features[ndx,1],'*') 
ndx = where(code==1)[0] 
plot(features[ndx,0],features[ndx,1],'r.') 
plot(centroids[:,0],centroids[:,1],'go') 
axis('off')
show()

import imtools
from PIL import Image 
import pca

# get list of images
imlist = imtools.get_imlist('../data/a_selected_thumbs/') 
imnbr = len(imlist)
# load model file
#with open('../a_pca_modes.pkl','rb') as f:
#  immean = pickle.load(f)
#  V = pickle.load(f)
# create matrix to store all flattened images
immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')
V,S,immean = pca.pca(immatrix)
#project on the 40 first PCs
immean = immean.flatten()
projected = array([dot(V[:40],immatrix[i]-immean) for i in range(imnbr)])
# k-means
projected = whiten(projected)
centroids,distortion = kmeans(projected,4)
code,distance = vq(projected,centroids)
# plot clusters
for k in range(4):
    ind = where(code==k)[0]
    figure()
    gray()
    for i in range(minimum(len(ind),40)):
        subplot(4,10,i+1) 
        imshow(immatrix[ind[i]].reshape((25,25))) 
        axis('off')
show()

from PIL import Image, ImageDraw # height and width
h,w = 1200,1200
# create a new image with a white background
img = Image.new('RGB',(w,h),(255,255,255))
draw = ImageDraw.Draw(img)
# draw axis
draw.line((0,h/2,w,h/2),fill=(255,0,0))
draw.line((w/2,0,w/2,h),fill=(255,0,0))
# scale coordinates to fit
scale = abs(projected).max(0)
scaled = floor(array([(p[0]/scale)*(w/2-20,h/2-20) + (w/2,h/2) for p in projected])) 
# paste thumbnail of each image
for i in range(imnbr):
    nodeim = Image.open(imlist[i]) 
    nodeim.thumbnail((25,25))
    ns = nodeim.size 
    img.paste(nodeim,(scaled[i][0]-ns[0]//2,scaled[i][1]-
    ns[1]//2,scaled[i][0]+ns[0]//2+1,scaled[i][1]+ns[1]//2+1)) 

img.save('pca_font.jpg')