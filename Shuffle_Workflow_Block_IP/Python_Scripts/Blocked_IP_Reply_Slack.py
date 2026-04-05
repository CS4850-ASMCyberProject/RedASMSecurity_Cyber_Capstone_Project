import json
import urllib.parse

# Pull Shuffle $exec into python safely (This r string which converts the raw wazuh alert to json to base64 is used  to ensure code handling in Shuffle
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''
data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

#Get the Raw Slack Payload (An encoded string)
raw = data.get("payload", "")

# Decode the string
decoded = urllib.parse.unquote(raw)

# Convert the decoded String to a Json String
payload = json.loads(decoded)

# Get the Action ID 
action_id = payload.get("actions", [{}])[0].get("action_id", "")

# If Action ID not blocksql or blockip, output a reason and exit
if action_id not in ["block_ip", "block_sql"]:
  print(json.dumps({"status": "ignored", "reason": "not block_ip button"}))
  raise SystemExit

#Get Source IP
source_ip = "$slack_source_ip_action_id.message.source_ip"

#Get Thread_TS and Channel for Slack
thread_ts = payload.get("message", {}).get("ts", "")
channel = payload.get("channel", {}).get("id", "")

#Build Payload
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

#Get the output of the http_block_ip and http_Block_sql script response
blocked_ip = "$http_block_ip.body"
blocked_sql = "$http_block_sql.body"

#Normalize the string responses above into a single string 
blocked_string = blocked_ip if blocked_ip else blocked_sql

# Conditional Block that determines the reply message for Slack based on the messages given from the automated scripts
# If blocked string starts with Blocked, this means it used the block IP automated script was used
# Elif blocked string starts with IP, this means the block IP automated script was used but the IP was already blocked
# Elif blocked string starts with IP, this means the block SQL automated script was used
# Else an unknown error occured, check Shuffle for error details
if blocked_string.startswith("Blocked"):
  message = f"🚫 *IP {source_ip} has been blocked.*\nFirewall rule deployed."
elif blocked_string.startswith("IP"):
  message = f"🛡 *No Action Needed — IP {source_ip} is already blocked.*"
elif blocked_string.startswith("/rest"):
  message = "*🚧 shop.redasmsecurity.cloud/rest/products/search has temporarily blocked malicious cyber attacks while the service is fixed*."
else:
  message = "Unknown Error Occured. Check the Internal system to determine the cause."

#Set the message
slack_blocked_reply["blocks"][0]["text"]["text"] = message

#Print the message
print(json.dumps(slack_blocked_reply, ensure_ascii=False))
