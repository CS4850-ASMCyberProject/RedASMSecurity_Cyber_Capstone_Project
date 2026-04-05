from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

BIND = "172.18.0.1"
PORT = 8787

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode(errors="ignore").strip()

        try:
            data = json.loads(raw)
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        ip = data.get("source_ip", "")
        action_id = data.get("action_id", "")

        try:
            if action_id == "block_ip":
                out = subprocess.check_output(
                    ["/srv/asm_project/Shuffle_Workflow_Block_IP/Python_Scripts/slack_ssh_blockip", ip],
                    stderr=subprocess.STDOUT,
                    text=True
                )
            elif action_id == "block_sql":
                out = subprocess.check_output(
                    ["/srv/asm_project/Shuffle_Workflow_Block_IP/Python_Scripts/slack_ssh_blocksql"],
                    stderr=subprocess.STDOUT,
                    text=True
                )
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid action_id")
                return

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
        return

HTTPServer((BIND, PORT), Handler).serve_forever()
