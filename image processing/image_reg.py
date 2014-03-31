# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 13:59:55 2014
image registration
@author: admin
"""

from xml.dom import minidom
import numpy as np
def read_points_from_xml(xmlFileName):
    """Read control points for face alignment."""
    
    xmldoc = minidom.parse(xmlFileName)
    facelist = xmldoc.getElementsByTagName('face')
    faces = {}
    for xmlFace in facelist:
        fileName = xmlFace.attributes['file'].value
        xf = int(xmlFace.attributes['xf'].value)
        yf = int(xmlFace.attributes['yf'].value)
        xs = int(xmlFace.attributes['xs'].value)
        ys = int(xmlFace.attributes['ys'].value)
        xm = int(xmlFace.attributes['xm'].value)
        ym = int(xmlFace.attributes['ym'].value)
        faces[fileName]= np.array([xf,yf,xs,ys,xm,ym])
    return faces
    
def compute_rigid_transform(refpoints, points):
    A = np.array([[points[0],-points[1],1,0],
                  [points[1],points[0],0,1],
                  [points[2],-points[3],1,0],
                  [points[3],points[2],0,1],
                  [points[4],-points[5],1,0],
                  [points[5],points[4],0,1]])
    y = np.array([refpoints[0],
                 refpoints[1],
                 refpoints[2],
                 refpoints[3],
                 refpoints[4],
                 refpoints[5]])
    #least sq solutions
    a,b,tx,ty = np.linalg.lstsq(A,y)[0]
    R = np.array([[a,-b],[b,a]])
    return R,tx,ty