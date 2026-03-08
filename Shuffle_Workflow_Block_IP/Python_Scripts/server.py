from http.server import BaseHTTPRequestHandler, HTTPServer

import subprocess

BIND = "172.19.0.1"
PORT = 8787

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        ip = self.rfile.read(length).decode(errors="ignore").strip()
        try:
            out = subprocess.check_output(
                ["/srv/asm_project/remote_block", ip],
                stderr=subprocess.STDOUT,
                text=True
            )
            body = out.strip()
            self.send_response(200)
        except subprocess.CalledProcessError as e:
            body = (e.output or "failed").strip()
            self.send_response(500)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body.encode())))
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        return  # quiet

HTTPServer((BIND, PORT), Handler).serve_forever()
