# -*- coding: utf-8 -*-
"""
Created on Tue May  8 15:43:14 2018

@author: 565637
"""

from PIL import Image
from PIL import ImageStat
import cv2
import numpy as np
from scipy.stats import kurtosis, skew

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()

def get_stats(fileName):
  image_file = fileName
  size = Image.open(image_file).size
  
  im = Image.open(image_file).convert('L')
  stat = ImageStat.Stat(im)
  brightness = stat.mean[0]
  
  image = cv2.imread(image_file)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  sharpness = variance_of_laplacian(gray)
  
  img = cv2.imread(image_file,0)
  hist,bins = np.histogram(img.flatten(),256,[0,256])
  kurt_contrast = kurtosis(hist)
  print (size,brightness,sharpness,kurt_contrast)
  if (all(i >= 64 for i in size))and(brightness>50) and (sharpness>25) and (abs(kurt_contrast)<25):
    return "Good"
  else:
    return "Bad"
  
  


#def pixel_size(fileName):
#    image_file = fileName
#    im = Image.open(image_file)
#    
#    return im.size
#
#def brightness( im_file ):
#   im = Image.open(im_file).convert('L')
#   stat = ImageStat.Stat(im)
#   return stat.mean[0]
#
#
#
#def blur_detection(imagePath):
#    image = cv2.imread(imagePath)
#    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#    fm = variance_of_laplacian(gray)
#    return fm
#
#def contrast_hist(image):
#    img = cv2.imread(image,0)
#    hist,bins = np.histogram(img.flatten(),256,[0,256])
#
#    print( 'excess kurtosis of normal distribution (should be 0): {}'.format( kurtosis(hist) ))
#    print( 'skewness of normal distribution (should be 0): {}'.format( skew(hist) ))
#
#import glob
#for filename in glob.glob("./statsimages/*")[0:2]:
#
#
##filename = "./images/grainy.jpg"  
#    pixel = pixel_size(filename)
#    print ("pixels for file : ",filename ,pixel )
#    
#    avg_pixel_brightness = brightness(filename)
#    print ("!!! avg_pixel_brightness : ", avg_pixel_brightness)
#    
#    sharpness = blur_detection(filename)
#    print ("### sharpness : ", sharpness)
#    
#    contrast_hist(filename)
#    print("_________________________________ xx _________________________________")
#    