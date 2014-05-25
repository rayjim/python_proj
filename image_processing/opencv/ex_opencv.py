import cv2
#read image


#readimage
im=cv2.imread('empire.jpg')
#downsample
#im_lowres=cv2.pyrDown(im)
im_Lowers=im
#converttograyscale
gray=cv2.cvtColor(im_lowres,cv2.COLOR_RGB2GRAY)
#detectfeaturepoints
s=cv2.SURF()
mask=uint8(ones(gray.shape))
keypoints=s.detect(gray,mask)
#showimageandpoints
vis=cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
for k in keypoints[::10]:
    cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),2,(0,255,0),-1)
    cv2.circle(vis,(int(k.pt[0]),int(k.pt[1])),int(k.size),(0,255,0),2)
cv2.imshow('localdescriptors',vis)
cv2.waitKey()


