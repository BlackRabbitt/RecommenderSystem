#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, chdir
import cgi

from config.route import *
from recommender import recommend
from config import PORT_NUMBER


VIEW_PATH = "front/view"
ROOT_FROM_VIEW = "../../"


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
                # Open the static file requested and send it
                chdir(VIEW_PATH)
                f = open(curdir + sep + self.path, 'rb').read()
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f)
                chdir(ROOT_FROM_VIEW)
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