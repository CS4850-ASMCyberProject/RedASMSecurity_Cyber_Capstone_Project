import json
import urllib.parse
import base64

# Pull Shuffle $exec into python safely (This r string which converts the raw wazuh alert to json to base64 is used  to ensure code handling in Shuffle
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''
data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

#Get the Raw Slack Payload (An encoded string)
raw = data.get("payload", "")

# Decode the string
decoded = urllib.parse.unquote(raw)

# Convert the decoded String to a Json String
payload = json.loads(decoded)

#Get the action_ID and source_ip from the Slack payload
action_id = payload.get("actions", [{}])[0].get("action_id", "")
source_ip = payload.get("actions", [{}])[0].get("value", "")

# Normalize source_ip to an empty string if None
# If source_ip == 10.0.0.48 (the target vm) or 10.0.0.97 (the manager vm) change to 49
# Protect from blocking important private ips and the network gateway 10.0.0.65
if not source_ip or source_ip == "None":
    source_ip = ""
if source_ip == "10.0.0.48" or source_ip == "10.0.0.97":
  source_ip = "10.0.0.49"
if source_ip.startswith("172.") or source_ip == "10.0.0.65" or source_ip.startswith("169.254") or source_ip.startswith("192.168"):
    print("Refusing to block internal IP.")
    exit()

# Build the payload
payload = {
  "source_ip": source_ip,
  "action_id": action_id
}

print(json.dumps(payload))
