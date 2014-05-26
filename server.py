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
        index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        if self.path == "/send":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                })

            print(type(form.getvalue("1")))  #string
            for i in range(10):
                if form.getvalue(index[i]):
                    rate.append(int(form.getvalue(index[i])))
                else:
                    rate.append(0)
            while len(rate) < 1682:
                rate.append(0)

            print("rate:", rate)
            print("length of rate", len(rate))

            recommended_movies = recommend(rate)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(str(recommended_movies).encode("utf-8"))
            # print(type(form["your_name"].value))
            # self.wfile.write(form["your_name"].value.encode('utf-8'))
            # self.wfile.write(form.getvalue("your_name"))
            #########
            # self.wfile.write()
            #########
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