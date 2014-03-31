# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 15:03:25 2014

@author: admin
"""
import imregistration
xmlFileName ='jkfaces.xml'
points = imregistration.read_points_from_xml(xmlFileName)

imregistration.rigid_alignment(points,'jkfaces')