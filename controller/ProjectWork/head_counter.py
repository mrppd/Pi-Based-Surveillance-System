# -*- coding: utf-8 -*-
"""
Created on Thu May  2 00:25:15 2019

@author: Pronaya
"""

import argparse
import imutils
import time
import cv2
import numpy as np
import sys
from skimage import img_as_ubyte


shift=-30

pplsizemin = 50
pplsizemax = 2000
history = 20
ppl = 0
lastppl = 0
cX = 0
cY = 0

pX = 320
pY = 240
gate = 40


lineB=int(pY/2-gate+shift)
lineR=int(pY/2+gate+shift)

enter = " "
sumppl = 0
abreast = 10

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)) 
	
c_in    = [0 for i in range(abreast)]
c_out   = [0 for i in range(abreast)]
cY_temp  = [0 for i in range(abreast)]
getpplno =0
getpplflag =0

######

hairLower = (63, 90, 0)
hairUpper = (87, 255, 255)


cap = cv2.VideoCapture(0)

cap.set(3, pX);
cap.set(4, pY);
cap.set(15, 0.1);
cap.set(5, 30);

i = 0
ret, firstFrame  = cap.read()

cv2.line(firstFrame,(0,lineB),(pX,lineB),(255,0,0),3)
cv2.line(firstFrame,(0,lineR),(pX,lineR),(0,0,255),3)

while 10*i<pY:
	cv2.line(firstFrame,(0,10*i),(pX,10*i),(0,255,0),1)
	i = i+1
cv2.imshow("firstFrame", firstFrame)


#camera =  cv2.imread("temp.bmp")
#firstFrame = camera
#firstFrame = cv2.equalizeHist(firstFrame)
fgbg = cv2.createBackgroundSubtractorMOG2()

while(True):
    ret, image = cap.read()
    #init = time.time()
    #image = np.array(image, dtype=np.int8)
	#####src_hsv = cv2.cvtColor(image,cv2.CV_BGR2HSV)
    cv2.line(image,(0,lineB),(pX,lineB),(255,0,0),3)
    cv2.line(image,(0,lineR),(pX,lineR),(0,0,255),3)
	
    ppl = 0
    getpplflag = 0
    temppl  = [0 for i in range(abreast)]
    
    image_crop = image[lineB:lineR, 0:pX]
    hsv = cv2.cvtColor(image_crop, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, hairLower, hairUpper)
    image_mask = cv2.erode(mask, kernel, iterations=5)
    image_mask = cv2.dilate(mask,kernel, iterations=5)
	
    gray = cv2.GaussianBlur(image_mask, (9, 9), 0)
    im_bw = fgbg.apply(gray, learningRate=1.0/history)
	
    (cnts, _) = cv2.findContours(im_bw.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    center = None
	
    for c in cnts:
		#print cv2.contourArea(c)
		#print ppl
        if (cv2.contourArea(c) < pplsizemin or cv2.contourArea(c) > pplsizemax):
            continue
			
        ((x, y), radius) = cv2.minEnclosingCircle(c)
		#print radius
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center = (cX,cY+pY/2-gate+shift)
        if radius > 6 and radius<30:
            ppl = ppl+1
            cv2.circle(image, (int(x), int(y)+pY/2-gate+shift), int(radius),(0, 255, 255), 2)
            cv2.circle(image, center, 5, (0, 0, 255), -1)
        
        
        
        
        if(c_in[ppl]!=0 and c_out[ppl]!=0 ):
            c_in = [0 for i in range(abreast)]
            c_out = [0 for i in range(abreast)]
            
        if (c_in[ppl]==0 and cY!=0):
            if (cY<gate and cY_temp[ppl]<cY):
                c_in[ppl] = -1
				#print ("in -1")
            if (cY>gate and cY_temp[ppl]>cY):
                c_in[ppl] = 1
				#print ("in 1")
        if (c_in[ppl]!=0 and cY!=0):
            if(c_in[ppl] ==-1 and cY>gate):
                c_out[ppl] = -1
                #print ("out -1")
                sumppl = sumppl -1
                enter = "--"
                getpplflag = 1
            if(c_in[ppl] ==1 and cY<gate):
                c_out[ppl] = 1
				#print ("out 1")
                sumppl = sumppl +1
                enter = "++"	
                getpplflag = 1				
        lastppl = ppl
        cY_temp[ppl] = cY
		


    pc = "PPL"+str(ppl)
		
    cv2.putText(image, pc, (30, 60),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(image, "X:"+str(cX), (10, image.shape[0] - 50),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(image, "Y:"+str(cY), (10, image.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(image, "Enter:"+enter, (pX-80, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(image, "Sum:"+str(sumppl), (pX-80, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    if getpplflag ==1:
        cv2.imwrite('getppl'+str(getpplno)+'.jpg',image)
        getpplno = getpplno + 1
	
    #rawCapture.truncate(0)
	#cv2.imshow("firstFrame", firstFrame)
    cv2.imshow("image_mask", image_mask)
    cv2.imshow("image", image)
    cv2.imshow("dilate", im_bw)
    cv2.waitKey (50)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()   






















