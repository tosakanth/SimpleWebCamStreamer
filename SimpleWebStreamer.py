import cv2
import Image
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
try
   from cStringIO import StringIO
except
   from StringIO import StringIO
   
   
class WebHandler(BaseHTTPRequestHandler):
   def do_GET(self):
      global camera
      if self.path=='/stream':
         self.send_response(200)
         self.send_header("Connection","close")
         self.send_header("Server","TKEyes")
         self.send_header("Expires","Mon, 3 Jan 2000 12:34:56 GMT")       
         self.send_header("Pragma","no-cache")
         
         #to send image string to browser, you have to send content type as multipart
         self.send_header("Content-Type","multipart/x-mixed-replace;boundary=--BOUNDARYSTRING\r\n")
         self.end_headers()
         while True :
            try :
               rc,img  = camera
            except :
            
