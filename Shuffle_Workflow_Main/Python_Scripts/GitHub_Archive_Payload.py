import json, base64

#Get the data and encode it to base64 for safe Shuffle handling.
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''

#Convert the base64 to a Json String. 
event = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

# event_id will be the name of the file the alert event is stored
event_id = event.get("id", "")

# Get the year, month, and day. Each event will be stored in the path events/year/month/day/event_id
now = datetime.datetime.utcnow()
path = f"events/{now.year}/{now.month:02}/{now.day:02}/{event_id}.json"

# Convert to Pretty Json
pretty = json.dumps(event, indent=2, ensure_ascii=False, sort_keys=True, default=str) + "\n"

# GitHub Contents API requires base64-encoded content
content_b64 = base64.b64encode(pretty.encode("utf-8")).decode("utf-8")

# Get the payload alert to add more info
alert = $python_slack_script.message

# Add the event path to which the event will be stored in GitHub.
# Add the event content.
# Add the commit msg to commit to GitHub.
# Add the event_id
alert["path"] = path
alert["github_event"] = content_b64
alert["commit_msg"] = f"Add Wazuh event dump {event_id}"
alert["event_id"] = event_id

print(json.dumps(alert, ensure_ascii=False))
