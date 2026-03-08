import json
import urllib.parse

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

if action_id != "block_ip":
  print(json.dumps({"status": "ignored", "reason": "not block_ip button"}))
  raise SystemExit
    
source_ip = "$slack_source_ip.message"

thread_ts = payload.get("message", {}).get("ts", "")
channel = payload.get("channel", {}).get("id", "")

slack_blocked_reply = {
  "thread_ts": thread_ts,
  "channel": channel,
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ""
      }
    }
  ]
}

blocked_string = "$http_block_ip.body"

if blocked_string.startswith("Blocked"):
  message = f"🚫 *IP {source_ip} has been blocked.*\nFirewall rule deployed."
else:
  message = f"🛡 *No Action Needed — IP {source_ip} is already blocked.*"
  
slack_blocked_reply["blocks"][0]["text"]["text"] = message
  
print(json.dumps(slack_blocked_reply, ensure_ascii=False))
