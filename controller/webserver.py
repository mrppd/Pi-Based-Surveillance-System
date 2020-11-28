import tkinter
import socketserver
import subprocess
from tkinter import messagebox
from http.server import BaseHTTPRequestHandler, HTTPServer
import BEuser as BE


def some_function():
        print ("some_function got called")
        # hide main window
        #root = tkinter.Tk()
        #root.withdraw()

        #result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
        stdoutput = subprocess.getoutput("ls")
        print("stdoutput: " + stdoutput)
        #messagebox.showinfo("HW!","Hello World!")
#def createDockerContainer(dataArray):
        #dataArray structure address:0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1 pass:gznaejin OS:CentOS leaseTime:50 storage:50 price:10
#       print("createDockerContainer method got called!")

class MyHandler(BaseHTTPRequestHandler):
        def _set_headers(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
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
                BE.createDockerContainer(dataStringArray)
                print("\n")

        def do_GET(self):
                if self.path == '/startPython':
                        some_function()

                self.send_response(200)

httpd = socketserver.TCPServer(("", 8547), MyHandler)
httpd.serve_forever()

