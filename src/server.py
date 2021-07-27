import http.server
import socketserver
from http import HTTPStatus
import urllib.parse as urlparse
import json

from account_manager import AccountManager

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        parsed = urlparse.urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        if path == '/createAccount':
            username = json.loads(post_data)['username']
            password = json.loads(post_data)['password']
            if manager.create_account(username, password):
                self.wfile.write("Created account\n".encode())
            else:
                self.wfile.write("Username taken\n".encode())

    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        path = parsed.path
        query = urlparse.parse_qs(parsed.query)

        if path == '/logIn':
            username = query['username'][0]
            password = query['password'][0]
            if manager.log_in(username, password):
                self.wfile.write("Login valid\n".encode())
            else:
                self.wfile.write("Invalid username or password\n".encode())

manager = AccountManager()
manager.initialize_tables()
httpd = socketserver.TCPServer(('', 8000), Handler)
try:
    httpd.serve_forever()
except:
    print('Shutting down')
    manager.close()
    httpd.shutdown()
