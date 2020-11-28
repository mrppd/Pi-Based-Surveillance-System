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
import pandas as pd
import pickle
from scipy.signal import savgol_filter
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib 
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

url = "G:\Work\Educational info\Gottingen\WSN lab\ProjectWork"

class MyFrameQueue:
    def __init__(self, length):
        self.length = length
        self.frameList = []
        self.normList = []
        self.newNormList = []
        self.diffList = []
        self.meanDiffList = 0
        self.medianDiffList = 0
        self.isRunning = False
        self.smoothNormsActivated = False
        self.status = "None"
        
    def ini(self, length=-1):
        if(length>=0):
            self.length = length
        self.frameList = []
        self.normList = []
        self.newNormList = []
        self.diffList = []
        self.meanDiffList = 0
        self.medianDiffList = 0
        self.isRunning = True
        self.smoothNormsActivated =False
    
    def finish(self):
        self.isRunning = False
    
    def framePush(self, frame):
        if(len(self.frameList)<self.length):
            #self.frameList.append(frame)
            frameNorm = np.linalg.norm(frame)
            self.normList.append(frameNorm)
    
        if(len(self.normList)==self.length):
            #del self.frameList[0]
            del self.normList[0]
            
    def smoothNorms(self):
        self.smoothNormsActivated = True
        self.newNormList = savgol_filter( self.normList, 11, 3)
        
    def rateOfChange(self, showPlot=False):
        # Way 2: find the difference between the values of position i and i+1
        # Then, Take the average of these consecutive differences with a window size of interval. 
        # here interval is 2 * frames per seconds (FPS)
        if(self.smoothNormsActivated):
            newNormList = self.newNormList
        else:
            newNormList = self.normList
            
        self.diffList = []
        #interval = int(FPS)*2
        interval = int(self.length/3)
        for i in range(interval, len(newNormList)):
            diff = 0
            for j in range(i-(interval-1), i):
                diff = diff + abs(newNormList[j]-newNormList[j-1])

            diff = diff/ len(range(i-(interval-1), i))
            self.diffList.append(diff)  
        
        self.meanDiffList = st.mean(self.diffList)
        self.medianDiffList = st.median(self.diffList)
        #print(int(self.medianDiffList), end=" ")
        self.getStatus()
        #print(self.diffList, end=" ")
        if(showPlot==True):
            #print("Diff List Length: "+ str(len(self.diffList)))
            plt.plot(self.diffList)
            plt.show()
     
        
    def getStatus(self):
        if(self.medianDiffList<4):
            self.status = "None"
        elif(self.medianDiffList>=4 and self.medianDiffList<40):
            self.status = "Low"
        elif(self.medianDiffList>=40 and self.medianDiffList<90):
            self.status = "Medium"
        elif(self.medianDiffList>=90 and self.medianDiffList<300):
            self.status = "High"
        else:
            self.status = "Extream"
            
        
    def showStatus(self):
        #print(self.status)
        return self.status;


        

FQ = MyFrameQueue(60)
globFrame = []

def captureFrame():
    global globFrame
    cap = cv2.VideoCapture(0)
    cap.set(3, 320);
    cap.set(4, 240);
    cap.set(15, 0.1);
    cap.set(5, 20);
    FQ.ini()
    
    while(True):
        ret, frame = cap.read()
        cv2.imshow("image", frame)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY);
        FQ.framePush(frame)
        globFrame = frame
        
        if cv2.waitKey(1) & 0xFF == ord('e'):
            cv2.destroyAllWindows() 
            FQ.finish()
            break

 
def plot(sec):
    cv2.waitKey(5000)
    i=0
    while(FQ.isRunning):
        #print("\n")
        #print(st.mean(FQ.frameList))
        #print(frameList)
        FQ.smoothNorms()
        FQ.rateOfChange(showPlot = False)
        #plt.plot(FQ.diffList)
        print(FQ.showStatus(), end = " ")
        
        cv2.waitKey(1000*sec)
        i = i+2
        

X_test = []
def daylight_aprox(sec):
    global X_test
    histList = []
    cv2.waitKey(7000)
    condition = {1: "Dark", 2: 'Dim', 3: "Visible", 4: "Bright"}
    
    i=0
    #load scaler and mlp model
    scalerLight = joblib.load(url+'\scalerLight.pkl') 
    mlpLight = joblib.load(url+'\mlpLight.pkl') 
    
    while(FQ.isRunning):
        hist = cv2.calcHist([globFrame],[0],None,[5],[0,200])  
        #plt.plot(hist)
        #plt.show()
    

        histList.append(hist.transpose().tolist()[0])
        #print(histList)
        X_test = pd.DataFrame(histList)
        #print(X_test)
        #Normalization
        X_test = scalerLight.transform(X_test)
        # Prediction
        Y_pred =  mlpLight.predict(X_test)
        
        print(condition[Y_pred[0]])
        
        histList = []
        cv2.waitKey(1000*sec)
        i = i + 1
        
    #with open(url + '\histListVisibleN', 'wb') as fp:
        #pickle.dump(histList, fp)
    #with open (url + '\histListVisible', 'rb') as fp:
        #histList = pickle.load(fp)

  
    
def test_list(sec):
    i = 0
    while(i<20*sec):
        print(i, end=' ')
        rval = random.randint(0,1000)
        FQ.framePush(rval)
        cv2.waitKey(50)
        i = i+1
        

threading.Thread(target=captureFrame, args = ()).start()
threading.Thread(target=plot, args = (5,)).start()
threading.Thread(target=daylight_aprox, args = (5, )).start()
    

#threading.Thread(target=test_list, args = (60,)).start()

