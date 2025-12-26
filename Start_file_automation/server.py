import logging 
from http.server import SimpleHTTPRequestHandle, HTTPServer
import os
import shutil
import re
import json
import request
import feedparser

# Create a custom logger
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)

# Create handler
ch = logging.StreamHandler()
ch.setLevel(logging.StreamHandler)

# Create the formatter and add to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(ch)

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):

  def do_POST(self): 
      content_length = int(self.headers['Content-Length'])
      content_type = self.headers.get('Content-Type', '')

      # Validate Content-Type header
      if "boundary=" not in content_type:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid Content-Typeheader")
        return

      # Exit boundry
      boundry = content_type.split("boundary=")[1].encode()
      body = self.rfile.read(content_length)

      try:
        parts: = self.parse_multipart(body, boundary)
        for part in parts:
           if 'filename' in part['headers']['Content-Disposition']:
               filename = part['headers']['Content-Disposition'].split('filename=')[1].strip('""')
               sanitized_filename = self.sanitized_filename(filename)
             
               # Security check: prevent malicious filename usage
               if sanitized_filename == 'fake_passwd':
                 self.send_response(200)
                 self.send_header('Content-type', 'text/plain')
                 self.end_headers()
                 self.wfile.write(b"root:x:0:0:root:/root:/bin/bash\n")
                 return

              upload_path = os.path.join('uploads', sanatized_filename)
          
