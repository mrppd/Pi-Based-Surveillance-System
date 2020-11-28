import cv2
import sys
import os
import subprocess
import threading
import time

continue_op = True

def process_check(delay):
	#delay = 10
	print("inside1\n")
	while(continue_op):
		time.sleep(delay)  #delay in seconds
		res_ppdweb = subprocess.check_output("curl -Is https://ppdweb.serveo.net | head -1 |awk '{ print  $2}' ", shell=True)
		res_ppdstream = subprocess.check_output("curl -Is https://ppdstream.serveo.net | head -1 |awk '{ print  $2}' ", shell=True)
		print("inside2\n")
		
		if(int(res_ppdweb)==502):
			print("Not OK\n")
		else:
			print("res_ppdweb: "+str(res_ppdweb)+"\n")
		
		if(int(res_ppdstream)==502):
			print("Not OK\n")
		else:
			print("res_ppdstream: "+str(res_ppdstream)+"\n")
		
		
		
def initiate_check():
	try:
		#thread.start_new_thread(process_check, (10,))
		check_th = threading.Thread(target = process_check, args = (10, ))
		check_th.start()
	except:
		print("Some error occured in process check!!")	


initiate_check()
#print("program started")
