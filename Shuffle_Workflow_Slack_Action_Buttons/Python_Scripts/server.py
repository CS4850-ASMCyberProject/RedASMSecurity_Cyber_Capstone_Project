from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess

#The Server is bound to the docker IP gateway 172.18.0.1. and listens on port 8787. The server basicaly becomes the docker gateway IP and listens for when the user clicks the contain path or block ip action buttons in Slack.
BIND = "172.18.0.1"
PORT = 8787

#The server can only handle post requests, which corresponds to the two http post request nodes in Shuffle after the action buttons have been pushed.
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        #Get the raw input from Shuffle 
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode(errors="ignore").strip()

        #Convert the raw data to a Json string.
        try:
            data = json.loads(raw)
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        #Get the ip and action ID
        ip = data.get("source_ip", "")
        action_id = data.get("action_id", "")

        try:
            #If action Id is Block IP, use the Block Ip automated script
            if action_id == "block_ip":
                out = subprocess.check_output(
                    ["/srv/asm_project/Shuffle_Workflow_Block_IP/Python_Scripts/slack_ssh_blockip", ip],
                    stderr=subprocess.STDOUT,
                    text=True
                )
            #If action Id is Block SQL, use the Block SQL automated script
            elif action_id == "block_sql":
                out = subprocess.check_output(
                    ["/srv/asm_project/Shuffle_Workflow_Block_IP/Python_Scripts/slack_ssh_blocksql"],
                    stderr=subprocess.STDOUT,
                    text=True
                )
            # Else send a 400 response error
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
