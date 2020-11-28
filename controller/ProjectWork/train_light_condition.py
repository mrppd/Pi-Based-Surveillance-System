# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:12:40 2019

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

with open (url + '\histListDark', 'rb') as fp:
    histListDark = pickle.load(fp)

with open (url + '\histListDim', 'rb') as fp:
    histListDim = pickle.load(fp)
        
with open (url + '\histListVisible', 'rb') as fp:
    histListVisible = pickle.load(fp)

with open (url + '\histListBright', 'rb') as fp:
    histListBright = pickle.load(fp)
    
histListAll = histListDark + histListDim + histListVisible + histListBright

histAllDF = pd.DataFrame(histListAll)

X = histAllDF.drop([5, 6],axis=1)
Y = histAllDF[6]

scaler = StandardScaler()
# Fit only to the training data
scaler.fit(X)

# Save the scaler for future use
# then just 'dump' your file
joblib.dump(scaler, url+'\scalerLight.pkl') 

# And now to load...
#scaler = joblib.load(url+'\scaler.pkl') 

# Now apply the transformations to the data:
X_train = scaler.transform(X)

# Train the model
mlp = MLPClassifier(hidden_layer_sizes=(5,5,5), max_iter=1000)

mlp.fit(X_train, Y)

# Save the trained model
joblib.dump(mlp, url+'\mlpLight.pkl') 

# Prediction
predictions = mlp.predict(X_train)
print(confusion_matrix(Y,predictions))















    