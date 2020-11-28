#!/usr/bin/python
import sys
import Adafruit_DHT
import time
import threading

humidity = 0
temperature = 0

def startReadingTempHumid():
	global humidity
	global temperature
	while(True):
		humidity, temperature = Adafruit_DHT.read_retry(11, 4)
		print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
		time.sleep(3)

def startThread():
	threading.Thread(target=startReadingTempHumid, args = ()).start()


def getTempHumid():
	global humidity
	global temperature
	return (temperature, humidity)
