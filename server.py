#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
from recommender import recommend

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        user_list = recommend(1)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str(user_list).encode("utf-8"))
        return

    #Handler for the POST requests
    # def do_POST(self):
    #     if self.path == "/send":
    #         form = cgi.FieldStorage(
    #             fp=self.rfile,
    #             headers=self.headers,
    #             environ={'REQUEST_METHOD': 'POST',
    #                      'CONTENT_TYPE': self.headers['Content-Type'],
    #             })
    #
    #         ############
    #         user_list = main()
    #         ############
    #         self.send_response(200)
    #         self.end_headers()
    #         #self.wfile.write("Thanks %s !" % form["your_name"].value)
    #         #########
    #         self.wfile.write(user_list)
    #         #########
    #         return


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