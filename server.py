#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi

from recommender import recommend

PORT_NUMBER = 8080

# This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "index.html"

            try:
                #Check the file extension required and
                #set the right mime type
                sendReply = False
                if self.path.endswith(".html"):
                    mimetype = 'text/html'
                    sendReply = True
                if self.path.endswith(".jpg"):
                    mimetype = 'image/jpg'
                    sendReply = True
                if self.path.endswith(".gif"):
                    mimetype = 'image/gif'
                    sendReply = True
                if self.path.endswith(".js"):
                    mimetype = 'application/javascript'
                    sendReply = True
                if self.path.endswith(".css"):
                    mimetype = 'text/css'
                    sendReply = True

                if sendReply:
                    #Open the static file requested and send it
                    f = open(curdir + sep + self.path)
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(f.read().encode('utf-8'))
                    f.close()
                return


            except IOError:
                self.send_error(404, 'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        rate = []
        index = []
        index_range = 20
        for i in range(index_range):
            index.append(str(i + 1))
        if self.path == "/send":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                })

            # print(type(form.getvalue("1")))  #string
            for i in range(index_range):
                if form.getvalue(index[i]):
                    rate.append(int(form.getvalue(index[i])))
                else:
                    rate.append(0)
            while len(rate) < 1682:
                rate.append(0)

            recommended_movies = recommend(0, rate)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(recommended_movies.encode("utf-8"))
            return


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()