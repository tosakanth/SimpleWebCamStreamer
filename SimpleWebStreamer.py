import cv2
import Image
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
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
               #capture a picture from web camera
               rc,img  = camera.read()
               img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
               
               #encode it to jpeg format
               jpg_img =  Image.fromarray(img_rgb)
               
               #create in-memory temp file to store jpeg image
               mem_file = StringIO()
               
               #save jpeg on in-memory file
               jpg_img.save(mem_file,'JPEG')
               
               #write boundary string to web page
               self.wfile.write("--BOUNDARYSTRING")
               
               #set content type as image type
               self.send_header("Content-type","image/jpeg")
               
               #tell browser to know size of data
               self.send_header("Content-length",str(mem_file.len))
               self.end_headers()
               
               #write image content to web browser
               self.wfile.write(mem_file.getvalue()+"\r\n")
               
            except KeyboardInterrupt:
               break
            
      elif self.path=="/" or not self.path :
         self.send_response(200)
         self.send_header("Content-type","text/html")
         self.end_headers()
         self.wfile.write(
"""
<html>
<head>
<style type=text/css>
 body { background-image: url(/stream); background-repeat:no-repeat; background-position:center top; background-attachment:fixed; height:100% }
</style>
</head>
<body>
</body>
</html>
"""
         )
         
camera = None
cam_index=0 #/dev/video0
port = 8080

def main():
   global camera
   global cam_index
   global port   
   camera = cv2.VideoCapture(cam_index)
   camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320)      
   camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240)      
   try:
      webserver = HTTPServer(('0.0.0.0',port),WebHandler)
      print "Server Started"
      webserver.serve_forever()
   except:
      camera.release()
      webserver.socket.close()
      
if __name__ == "__main__":
   main()

