import cv2
import sys
import os
import subprocess
import threading
import time

import camera_queue2
import temp_humid_ini
import json_ini


def startMonitor():
	camera_queue2.startThread()
	temp_humid_ini.startThread()
	

def readWriteData(sec):
	while(True):
		(temperature, humidity) = temp_humid_ini.getTempHumid()
		(light_cond, motion) = camera_queue2.getMotionLightCond()
		try:
			json_ini.makeJSON(temp = temperature, humid = humidity, motion = motion, light = light_cond)
		except:
			print("Error occured during writting JSON")
		time.sleep(sec)
	
	
def startThread():
	startMonitor()
	threading.Thread(target = readWriteData, args = (5,)).start()
	
startThread()
 
