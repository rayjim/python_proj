from PIL import Image
import os
from pylab import *
import imtools

close("all")
gray()
pil_im = array(Image.open('lena.png'))
pil_img = array(Image.open('lena.png').convert('L'))
figure (1)

subplot(121)
imshow(pil_im)
subplot(122)
imshow(pil_img,cmap=cm.Greys_r)
figure(2)
hist(pil_img.flatten(),128)
show()
figure(3)
im2 = 255 - pil_img
im3=(100/255.0)*pil_img+100
im4 = 255.0*(pil_img/255.0)**2
subplot(221)
imshow(pil_img,cmap=cm.Greys_r)
subplot(222)
imshow(im2,cmap=cm.Greys_r)
subplot(223)
imshow(im3,cmap=cm.Greys_r)
subplot(224)
imshow(im4,cmap=cm.Greys_r)
figure(4)
im5,cdf = imtools.histeq(pil_img)
subplot(221)
imshow(pil_img,cmap=cm.Greys_r)
subplot(222)
imshow(im5,cmap=cm.Greys_r)
subplot(223)
plot(cdf)
###########################################################
close("all")
# pca
imlist = imtools.get_imlist('gwb_cropped')
im = array(Image.open(imlist[0]))
m,n = im.shape[0:2]
imnbr = len(imlist)

immatrix = array([array(Image.open(im)).flatten() for im in imlist],'f')
# perform PCA
V,S,immean= imtools.pca(immatrix)


figure()

subplot(2,4,1)
imshow(immean.reshape(m,n))
for i in range(7):
    subplot(2,4,i+2)
    imshow(V[i].reshape(m,n))

show()

############################################################
#bluring image test
from scipy.ndimage import filters
#close("all")
figure()
subplot(1,4,1)
imshow(pil_img)
for i in range(4):
    im2 = filters.gaussian_filter(pil_img,1+i*3)
    a= subplot(1,4,i+1)
    a.set_title('variance 1+i*3')
    imshow(im2)
    
############################################################
# sobel derivative filters
    
imx = zeros(pil_img.shape)
filters.sobel(pil_img,0,imx)

imy = zeros(pil_img.shape)
filters.sobel(pil_img,1,imy)
maginitude = sqrt(imx**2+imy**2)
##Gaussian filter

close('all')
figure()
a=subplot(221)
imshow(pil_img)
a.set_title('original')
a=subplot(222)
a.set_title('sobel')
imshow(maginitude)
figure()
sigma = array([2,5,10])
for i in range(3):
    imx = zeros(pil_img.shape)
    filters.gaussian_filter(pil_img,(sigma[i],sigma[i]),(0,1),imx)
    imy = zeros(pil_img.shape)
    filters.gaussian_filter(pil_img,(sigma[i],sigma[i]),(1,0),imy)
    maginitude = zeros(pil_img.shape)
    maginitude = sqrt(imx**2+imy**2)
    subplot(3,4,i*4+1)
    imshow(pil_img)
    subplot(3,4,i*4+2)
    imshow(imx)
    subplot(3,4,i*4+3)
    imshow(imy)
    subplot(3,4,i*4+4)
    imshow(maginitude)

########################################################################
#morphology-counting objects
from scipy.ndimage import measurements, morphology

im = 1*(pil_img<128)

labels,nbr_bojects = measurements.label(im)
im_open = morphology.binary_opening(im,ones((9,5)),iterations=2)
labels_open,nbr_bojects_open = measurements.label(im_open)
figure()
subplot(121)
imshow(im)
subplot(122)
im_open = 1*im_open
show(im_open)
print "Number of objects:", nbr_bojects
print "Number of objects:", nbr_bojects_open






















