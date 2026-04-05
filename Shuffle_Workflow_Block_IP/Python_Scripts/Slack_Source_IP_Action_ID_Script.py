import json
import urllib.parse
import base64

# Pull Shuffle $exec into python safely
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''
data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

raw = data.get("payload", "")

# Slack interactive requests come in as a form body:
# payload=<urlencoded json>
 # adjust if your webhook stores it under another key
decoded = urllib.parse.unquote(raw)

payload = json.loads(decoded)

action_id = payload.get("actions", [{}])[0].get("action_id", "")
source_ip = payload.get("actions", [{}])[0].get("value", "")
# optionally normalize:
if not source_ip or source_ip == "None":
    source_ip = ""
if source_ip == "10.0.0.48" or source_ip == "10.0.0.97":
  source_ip = "10.0.0.49"
if source_ip.startswith("172.") or source_ip == "10.0.0.65" or source_ip.startswith("169.254") or source_ip.startswith("192.168"):
    print("Refusing to block internal IP.")
    exit()
    
payload = {
  "source_ip": source_ip,
  "action_id": action_id
}

print(json.dumps(payload))
