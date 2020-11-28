import cv2
import sys
import os
import subprocess
import threading
import time
import monitor_ini

continue_op = True

def process_check(delay):
	#delay = 10
	#print("inside1")
	while(continue_op):
		time.sleep(delay)  #delay in seconds
		res_ppdweb = subprocess.check_output("curl -Is https://ppdweb.serveo.net | head -1 |awk '{ print  $2}' ", shell=True)
		res_ppdstream = subprocess.check_output("curl -Is https://ppdstream.serveo.net | head -1 |awk '{ print  $2}' ", shell=True)
		#print("inside2")
		
		if(int(res_ppdweb)==502):
			print("res_ppdweb: "+"Not OK")
			res_ppdwebserver = subprocess.check_output("ps aux | awk '$11==\"ppdwebserver\" {print $11}'", shell=True)
			if(len(str(res_ppdwebserver))<3):
				process_webserver()
			res_ppdweb = subprocess.check_output("ps aux | awk '$11==\"ppdweb\" {print $11}'", shell=True)
			if(len(str(res_ppdweb))<3):
				process1()
		else:
			print("res_ppdweb: "+str(res_ppdweb))
		
		if(int(res_ppdstream)==502):
			print("res_ppdstream: "+"Not OK")
			res_ppdstream = subprocess.check_output("ps aux | awk '$11==\"ppdstream\" {print $11}'", shell=True)
			if(len(str(res_ppdstream))<3): 
				process2()
				print("res_ppdstream: activated")
		else:
			print("res_ppdstream: "+str(res_ppdstream))

		
def initiate_check():
	try:
		#thread.start_new_thread(process_check, (60,))
		check_th = threading.Thread(target = process_check, args = (60, ))
		check_th.start()
	except:
		print("Some error occured in process check!!")	
		

def process_webserver():	
	#subprocess.call('bash -c "exec -a ppdwebserver python -m SimpleHTTPServer 3000" &', shell=True)
	subprocess.call('bash -c "exec -a ppdwebserver python httpwebserver.py" &', shell=True)

def process_webserver_close():
	subprocess.call('pkill -f ppdwebserver &', shell=True)
		
def process2():
	res = subprocess.call('bash -c "exec -a ppdstream ssh -R ppdstream:80:localhost:9000 serveo.net" &', shell=True)
	#print res
def process2_close():
	subprocess.call('pkill -f ppdstream &', shell=True)
	
def process1():
	res = subprocess.call('bash -c "exec -a ppdweb ssh -R ppdweb:80:localhost:3000 serveo.net" &', shell=True)

def process1_close():
	subprocess.call('pkill -f ppdweb &', shell=True)	
	
def process3():
	res = subprocess.call('bash -c "exec -a ppdremote ssh -R ppdremote:80:localhost:7000 serveo.net" &', shell=True)
	
def process_lcd():
	res = subprocess.call('bash -c "exec -a ppdlcd python lcd_ini.py" &', shell=True)
	
def process_lcd_close():
	res = subprocess.call('pkill -f ppdlcd &', shell=True)
	

process_webserver_close()
process1_close()
process2_close()
process_lcd_close()
monitor_ini.process_close()

process_webserver()
process1()
process2()
monitor_ini.process_monitor()
process_lcd()


"""
try:
	#thread.start_new_thread(process1, ("1",))
except:
	print("Some error occured in port 3000!!!")

try:
	process2("ffs")
	#thread.start_new_thread(process2, ("2",))
except:
	print("Some error occured in port 9000!!!")
"""
initiate_check()

print("hello")

