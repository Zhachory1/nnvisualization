#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import csv
import json
import sys

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".csv"):
				mimetype='text/csv'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path, 'r') 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				if mimetype == 'text/csv':
					data = read_csv(f)
					self.wfile.write(data)
				else:
					self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

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
		print 'Started httpserver on port ' , PORT_NUMBER
		
		#Wait forever for incoming htto requests
		server.serve_forever()

	except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()

if __name__ == "__main__":
	main(sys.argv[1:])