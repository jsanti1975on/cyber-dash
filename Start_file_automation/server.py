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
        
        



