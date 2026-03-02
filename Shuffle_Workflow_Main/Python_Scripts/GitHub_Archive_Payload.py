import json, base64

#The data passed into the script is raw $exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''

event = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

# Pick a stable event id (adjust if your schema differs)
event_id = event.get("id", "")

# Date-based folder structure (UTC)
now = datetime.datetime.utcnow()
path = f"events/{now.year}/{now.month:02}/{now.day:02}/{event_id}.json"

# Pretty JSON so GitHub renders it nicely
pretty = json.dumps(event, indent=2, ensure_ascii=False, sort_keys=True, default=str) + "\n"

# GitHub Contents API requires base64-encoded content
content_b64 = base64.b64encode(pretty.encode("utf-8")).decode("utf-8")

alert = $python_slack_script.message

alert["path"] = path
alert["github_event"] = content_b64
alert["commit_msg"] = f"Add Wazuh event dump {event_id}"
alert["event_id"] = event_id

print(json.dumps(alert, ensure_ascii=False))
