import SimpleHTTPServer
import SocketServer
import socket
import os
import webbrowser

PORT = 8000 # Desired web server port

# Start the server and open the web page
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
httpd = SocketServer.TCPServer(("", PORT), Handler)
print("Web server started: http://%s:%s" % (socket.gethostname(),PORT))
webbrowser.open_new("http://%s:%s" % (socket.gethostname(),PORT))
httpd.serve_forever()