# -*- coding: utf-8 -*-
"""
Created on Fri May 16 16:22:48 2014

@author: admin
"""

import cv2

cap=cv2.VideoCapture(0)
while True:
    ret,im=cap.read()
    cv2.imshow('videotest',im)
    key=cv2.waitKey(10)
    if key==27:
        break
    if key==ord(' '):
        cv2.imwrite('vid_result.jpg',im)