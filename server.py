#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, chdir
import cgi

from config.route import *
from recommender import recommend


PORT_NUMBER = 8080


# This class will handles any incoming request from the browser
class Handler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        self.path = Routes.checkUrl(self.path)

        try:
            # Check the file extension required and
            # set the right mime type
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                chdir("../../front/view")
                mimetype = 'image/jpg'
                img = open(curdir + sep + self.path, 'rb').read()
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(img)
                chdir("../../data/dataset")

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
                # Open the static file requested and send it
                chdir("../../front/view")
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
                f.close()
                chdir("../../data/dataset")
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        rate = []
        index_range = 20
        if self.path == "/recommend":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                })

            for i in range(index_range):
                if form.getvalue(str(i)):
                    rate.append(int(form.getvalue(str(i))))
                else:
                    rate.append(0)
            while len(rate) < 1682:
                rate.append(0)

            recommended_movies = recommend(rate)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(recommended_movies.encode("utf-8"))
            return


try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), Handler)
    print(".......beetle developers.......")
    print('Started httpserver on port ', PORT_NUMBER)

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()