import sys
import os
import subprocess
import threading
import time

def process_monitor():	
	subprocess.call('bash -c "exec -a ppdmonitor python monitor.py" &', shell=True)

def process_close():
	subprocess.call('pkill -f ppdmonitor &', shell=True)
