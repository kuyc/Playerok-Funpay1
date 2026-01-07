from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_web():
    threading.Thread(
        target=HTTPServer(("0.0.0.0", 8080), Handler).serve_forever,
        daemon=True
    ).start()

