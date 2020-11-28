#import tkinter
import SocketServer
import subprocess
#from tkinter import messagebox
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import shutil
import json
import datetime
import urlparse
import time

import monitor_ini
import camera_ini


FILEPATH = "./data.json"

def start_camera(self):
        monitor_ini.process_close()
        time.sleep(0.5)
        print ("Starting Camera")
        data = {}
        data['width'] = 320
        data['height'] = 400
        if "?" in self.path:
                for key, value in dict(urlparse.parse_qsl(self.path.split("?")[1], True)).items():
                        print(key+" = "+value)
                        data[key] = value                
        
        data['camera_status'] = "active"
        data['stream_address'] = "http:/ppdstream.serveo.net/?action=stream"
        data['time'] = str(datetime.datetime.now())
        json_data = json.dumps(data)
        self.wfile.write(json_data)
        
        with open('camera.json', 'w') as outfile:
                json.dump(data, outfile)
        
        camera_ini.process_close()
        camera_ini.process_camera_ini(data)

def stop_camera(self, web=True):
        print ("Closing Camera")
        
        data = {}
        data['camera_status'] = "inactive"
        data['stream_address'] = "http:/ppdstream.serveo.net/?action=stream"
        data['time'] = str(datetime.datetime.now())
        json_data = json.dumps(data)
        if(web==True):
                self.wfile.write(json_data)
        
        with open('camera.json', 'w') as outfile:
                json.dump(data, outfile)
                
        camera_ini.process_close()
        time.sleep(0.5)
        monitor_ini.process_close()
        monitor_ini.process_monitor()

def update_monitor(self):
        print ("Update monitor called!")
        with open(FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/json')
            #self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
            self.send_header("Content-Disposition", 'inline')
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)

def start_monitor(self):
        print ("Start monitor called!")
        stop_camera(self, web=False)
        
        with open(FILEPATH, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-Type", 'application/json')
            #self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
            self.send_header("Content-Disposition", 'inline')
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs.st_size))
            self.end_headers()
            shutil.copyfileobj(f, self.wfile)
        
def stop_monitor(self):
        print("Monitor system closed!")
        monitor_ini.process_close()
        time.sleep(0.5)
        data = {}
        data['camera_status'] = "inactive"
        data['monitor_status'] = "inactive"
        data['stream_address'] = "http:/ppdstream.serveo.net/?action=stream"
        data['time'] = str(datetime.datetime.now())
        json_data = json.dumps(data)
        self.wfile.write(json_data)

class MyHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
                self.send_response(200)
                self.send_header("Content-Type", 'application/json')
                self.send_header("Content-Disposition", 'inline')
                self.end_headers()

        def do_POST(self):
        # Doesn't do anything with posted data
                # print("Iam here!")
                content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
                # print(content_length)
                post_data = self.rfile.read(content_length) # <--- Gets the data itself
                print("\n")
                self._set_headers()
                # print(post_data) has to be decoded as when data is received it is recevied in bytes not in strings or anything readable
                dataString = post_data.decode("utf-8")
                dataStringArray = dataString.split(" ")
                print(dataString)

                print("\n")

        def do_GET(self):
                
                if '/startCamera' in self.path:
                        self._set_headers()
                        start_camera(self)
                        #self.wfile.write("Starting Camera")
                if '/stopCamera' in self.path:
                        self._set_headers()
                        stop_camera(self)
                        #self.wfile.write("Stoping Camera")
                if '/startMonitor' in self.path:
                        #self._set_headers()
                        start_monitor(self)
                        #self.wfile.write("Done Nothing")
                if '/updateMonitor' in self.path:
                        #self._set_headers()
                        update_monitor(self)
                if '/stopMonitor' in self.path:
                        stop_monitor(self)
                        
                
                        
                #self.send_response(200)
                

httpd = SocketServer.TCPServer(("", 3000), MyHandler)
httpd.serve_forever()

