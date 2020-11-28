# -*- coding: utf-8 -*-
"""
Created on Sat May  4 23:12:40 2019

@author: Pronaya
"""

import numpy as np 
import cv2 
import requests 
import time 
import argparse 
import matplotlib.pyplot as plt
import random
import threading
import pandas as pd
import pickle
from scipy.signal import savgol_filter
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib 
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix


url = "."

with open (url + '/histListDarkN', 'rb') as fp:
    histListDark = pickle.load(fp)
#with open(url + '/histListDarkN', 'wb') as fp:
        #pickle.dump(histListDark, fp, protocol=0)

with open (url + '/histListDimN', 'rb') as fp:
    histListDim = pickle.load(fp)
#with open(url + '/histListDimN', 'wb') as fp:
    #pickle.dump(histListDim, fp, protocol=0)
        
with open (url + '/histListVisibleN', 'rb') as fp:
    histListVisible = pickle.load(fp)
#with open(url + '/histListVisibleN', 'wb') as fp:
    #pickle.dump(histListVisible, fp, protocol=0)  
    
with open (url + '/histListVisibleExtN', 'rb') as fp:
    histListVisibleExt = pickle.load(fp)
#with open(url + '/histListVisibleExtN', 'wb') as fp:
    #pickle.dump(histListVisibleExt, fp, protocol=0)  
    
with open (url + '/histListBrightN', 'rb') as fp:
    histListBright = pickle.load(fp)
#with open(url + '/histListBrightN', 'wb') as fp:
    #pickle.dump(histListBright, fp, protocol=0)  
    
histListAll = histListDark + histListDim + histListVisible + histListVisibleExt + histListBright

histAllDF = pd.DataFrame(histListAll)

X = histAllDF.drop([5, 6],axis=1)
Y = histAllDF[6]

scaler = StandardScaler()
# Fit only to the training data
scaler.fit(X)

# Save the scaler for future use
# then just 'dump' your file
joblib.dump(scaler, url+'/scalerLight.pkl') 

# And now to load...
#scaler = joblib.load(url+'\scaler.pkl') 

# Now apply the transformations to the data:
X_train = scaler.transform(X)

# Train the model
mlp = MLPClassifier(hidden_layer_sizes=(5,10, 5), max_iter=2000)

mlp.fit(X_train, Y)

# Save the trained model
joblib.dump(mlp, url+'/mlpLight.pkl') 

# Prediction
predictions = mlp.predict(X_train)
print(confusion_matrix(Y,predictions))















    
