# -*- coding: utf-8 -*-
"""
Created on Sat May  4 01:42:01 2019

@author: Pronaya
"""

from imutils.object_detection import non_max_suppression 
import numpy as np 
import imutils 
import cv2 
import requests 
import time 
import argparse 
import matplotlib.pyplot as plt
import random
import threading
import statistics as st

class MyFrameQueue:
    def __init__(self, length):
        self.length = length
        self.frameList = []
        self.normList = []
    
    def framePush(self, frame):
        if(len(self.frameList)<self.length):
            self.frameList.append(frame)
            frameNorm = np.linalg.norm(frame)
            self.normList.append(frameNorm)
    
        if(len(self.frameList)==self.length):
            del self.frameList[0]
            del self.normList[0]
    
        

FQ = MyFrameQueue(50)



def test_list(sec):
    i = 0
    while(i<20*sec):
        print(i, end=' ')
        rval = random.randint(0,1000)
        FQ.framePush(rval)
        cv2.waitKey(50)
        i = i+1

 
def plot(sec):
    i=0
    while(i<60):
        print("\n")
        print(st.mean(FQ.frameList))
        #print(frameList)
        plt.plot(FQ.frameList)
        plt.show()
        cv2.waitKey(1000*sec)
        i = i+2

    
threading.Thread(target=test_list, args = (60,)).start()

threading.Thread(target=plot, args = (2,)).start()