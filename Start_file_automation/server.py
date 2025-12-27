import logging
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import shutil
import re
import json
import requests
import feedparser

# Create a custom logger
logger = logging.getLogger('server_logger')
logger.setLevel(logging.INFO)

# Create handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handler
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
            self.wfile.write(b"Invalid Content-Type header")
            return

        # Extract boundary
        boundary = content_type.split("boundary=")[1].encode()
        body = self.rfile.read(content_length)

        try:
            parts = self.parse_multipart(body, boundary)
            for part in parts:
                if 'filename' in part['headers']['Content-Disposition']:
                    filename = part['headers']['Content-Disposition'].split('filename=')[1].strip('"')
                    sanitized_filename = self.sanitize_filename(filename)

                    # Security check: prevent malicious filename usage
                    if sanitized_filename == 'fake_passwd':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b"root:x:0:0:root:/root:/bin/bash\n")
                        return

                    upload_path = os.path.join('uploads', sanitized_filename)
                    self.ensure_directory('uploads')

                    with open(upload_path, 'wb') as f:
                        f.write(part['body'])

                    self.move_file(upload_path)

                    # Send success page with a redirect option
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    success_message = f"""
                    <html>
                    <head>
                        <title>Upload Successful</title>
                        <script>
                            function redirectToUpload() {{
                                window.location.href = '/upload';
                            }}
                        </script>
                    </head>
                    <body style="text-align:center; background-color: black; color: green;">
                        <h2> File Uploaded Successfully!</h2>
                        <p>File: {sanitized_filename}</p>
                        <img src='/success.png' alt='Success Image' width='300'>
                        <br><br>
                        <button onclick="redirectToUpload()" style="font-size:18px; padding:10px; background-color:#34ac44; color:white; border:none; border-radius:5px; cursor:pointer;">
                            ⬅ Upload Another File
                        </button>
                    </body>
                    </html>
                    """

                    self.wfile.write(success_message.encode())
                    return

            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"File upload failed")
        except Exception as e:
            logger.error(f"Error during file upload: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal server error")

    def do_GET(self):
        if self.path == '/success.png':
            if os.path.exists('success.png'):
              # Reformatted above
