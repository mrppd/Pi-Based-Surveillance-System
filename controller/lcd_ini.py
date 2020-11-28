
from RPi import GPIO
from RPLCD.gpio import CharLCD
import time
import threading
import json


lcd = CharLCD(cols=16, rows=2, pin_rs=6, pin_e=16, pins_data=[21, 22, 27, 26], numbering_mode=GPIO.BCM, compat_mode=True)

temp = 33
humid = 50
light_cond = "Visible"
motion = "Extream"
camera_feed = True

monitor_str_th = u""
monitor_str_mov = u""
monitor_str_light = u""
monitor_str_camera = u""

camera_feed_text_ac = u"  Camera Feed     Activated!!"
camera_feed_text_dac = u"  Camera Feed     Deactivated!"
lcd.clear()
#lcd.cursor_mode = "hide"

#Will be defined in a seperate thread
def getData():
	global monitor_str_th, monitor_str_mov, monitor_str_light, monitor_str_camera
	global temp, humid, motion, light_cond, camera_feed_text_ac, camera_feed_text_dac, camera_feed
	
	while(True):
		data = {}
		camera = {}
		with open('data.json') as json_file:
			data = json.load(json_file)
		with open('camera.json') as json_file:
			camera = json.load(json_file)
		
		monitor_str_th = u"T:"+str(data['temp'])+"C-H:"+str(data['humid'])+"% "
		monitor_str_mov = u"Motion: "+str(data['video_state'])
		monitor_str_light = u"Light: "+str(data['light_condition'])
	
		if(camera['camera_status']=="active"):
			monitor_str_camera = camera_feed_text_ac
			camera_feed = True
		else:
			monitor_str_camera = camera_feed_text_dac
			camera_feed = False
		time.sleep(4)
###############################################

#Another Thread##############################


def lcdDisplay():
	global monitor_str_camera, monitor_str_th, monitor_str_mov, monitor_str_light
	
	lcd.write_string(u" Device Started ")
	time.sleep(5)
	lcd.clear()
	time.sleep(1)
	lcd.write_string(u" Welcome to the  WSN Project")
	time.sleep(3)
	lcd.clear()
	time.sleep(1)	
	lcd.cursor_pos = (0, 0)
	lcd.write_string(u"piMonitor System")
	time.sleep(3)
	lcd.clear()
	time.sleep(1)
	
	i=0
	camera_flag = True
	while(True):
		if(camera_feed==True):
			lcd.cursor_pos = (0, 0)
			lcd.write_string(monitor_str_camera)
			time.sleep(2)
			lcd.clear()
			time.sleep(1)
			camera_flag = False
		else:
			if(camera_flag == False):
				lcd.cursor_pos = (0, 0)
				lcd.write_string(monitor_str_camera)
				time.sleep(3)
				lcd.clear()
				time.sleep(2)
				camera_flag = True
				
			lcd.cursor_pos = (0, 0)
			lcd.write_string(monitor_str_th)
			
			time.sleep(1)
		
			lcd.cursor_pos = (1, 0)
			lcd.write_string(monitor_str_mov)

			time.sleep(3)
			lcd.clear()

			lcd.cursor_pos = (0, 0)
			lcd.write_string(monitor_str_th)
			
			time.sleep(1)

			lcd.cursor_pos = (1, 0)
			lcd.write_string(monitor_str_light)
	
			time.sleep(3)
			lcd.clear()

		i = i+1
		
	lcd.clear()
	lcd.close()


threading.Thread(target = getData, args = ()).start()
threading.Thread(target = lcdDisplay, args = ()).start()

