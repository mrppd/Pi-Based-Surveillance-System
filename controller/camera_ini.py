import cv2
import sys
import os
import subprocess
import threading
import time

def process_camera_ini(data):
	subprocess.call('modprobe bcm2835-v4l2', shell=True)
	res = subprocess.call('../../mjpg-streamer/mjpg_streamer '+
						'-i "../../mjpg-streamer/input_uvc.so -f 15 -r '
						+data["width"]+'x'+data["height"]+' -n -y" '+
						'-o "../../mjpg-streamer/output_http.so '+
						'-w ../../mjpg-streamer/www -p 9000" &', shell=True)

def process_close():
	res = subprocess.call('killall mjpg_streamer &', shell=True)


if(len(sys.argv)==2):
	condition = sys.argv[1]
	if(condition=="start"):
		camera_ini = threading.Thread(target = process_camera_ini, args = ( ))
		camera_ini.start()
		print("hello camera")

		#time.sleep(30)
	if(condition=="stop"):	
		camera_close = threading.Thread(target = process_close, args = ( ))
		camera_close.start()
		print("bye-bye camera")




