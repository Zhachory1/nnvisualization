#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import csv
import json
import sys
from urllib.parse import unquote

PORT_NUMBER = 8080
STATIC_ROOT = os.path.abspath(os.path.dirname(__file__))

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		if self.path == "/":
			self.path = "/index.html"

		try:
			# Decode URL-encoded characters and normalize path
			decoded_path = unquote(self.path)
			# Remove leading slash and normalize
			clean_path = os.path.normpath(decoded_path.lstrip('/'))
			# Build absolute path and resolve symlinks
			requested_path = os.path.realpath(os.path.join(STATIC_ROOT, clean_path))

			# Security check: ensure path stays within STATIC_ROOT
			if not requested_path.startswith(STATIC_ROOT):
				print(f"[SECURITY] Blocked path traversal attempt: {self.path}")
				self.send_error(403, 'Forbidden: Path traversal detected')
				return

			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if requested_path.endswith(".html"):
				mimetype = 'text/html'
				sendReply = True
			if requested_path.endswith(".jpg"):
				mimetype = 'image/jpg'
				sendReply = True
			if requested_path.endswith(".gif"):
				mimetype = 'image/gif'
				sendReply = True
			if requested_path.endswith(".js"):
				mimetype = 'application/javascript'
				sendReply = True
			if requested_path.endswith(".css"):
				mimetype = 'text/css'
				sendReply = True
			if requested_path.endswith(".csv"):
				mimetype = 'text/csv'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				if mimetype == 'text/csv':
					# CSV files: convert to JSON
					with open(requested_path, 'r') as f:
						data = read_csv(f)
						self.send_response(200)
						self.send_header('Content-type', mimetype)
						self.end_headers()
						self.wfile.write(data.encode('utf-8'))
				else:
					# Other files: serve as-is in binary mode
					with open(requested_path, 'rb') as f:
						self.send_response(200)
						self.send_header('Content-type', mimetype)
						self.end_headers()
						self.wfile.write(f.read())
			return

		except IOError:
			self.send_error(404, 'File Not Found: %s' % self.path)

#Read CSV File
def read_csv(file):
    csv_rows = []
    reader = csv.DictReader(file)
    title = reader.fieldnames
    for row in reader:
        csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
    return json.dumps(csv_rows)

def main(args=[]):
	try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('', PORT_NUMBER), myHandler)
		print(f'Started httpserver on port {PORT_NUMBER}')

		#Wait forever for incoming http requests
		server.serve_forever()

	except KeyboardInterrupt:
		print('^C received, shutting down the web server')
		server.socket.close()

if __name__ == "__main__":
	main(sys.argv[1:])