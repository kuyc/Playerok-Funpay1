from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"OK")

def start_web():
    threading.Thread(
        target=HTTPServer(("0.0.0.0",8080),H).serve_forever,
        daemon=True
    ).start()
