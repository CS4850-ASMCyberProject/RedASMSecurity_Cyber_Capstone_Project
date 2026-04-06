from datetime import datetime
from zoneinfo import ZoneInfo
import json

#Get the Custom Python Script Alert
alert = $python_slack_script.message

#Get Alerts_by_ip, which shows the alerts for an ip in the last hour
alerts_by_ip = alert.get("alerts_by_ip", {})

#Get source ip
source_ip = "$python_slack_script.message.observables.source_ip"

#Get source user
source_user = "$python_slack_script.message.observables.source_user"

#Convert the unix timestamps to human readable timestamps 
for entry in alerts_by_ip[source_ip]:
  pretty_ts = int(float(entry["timestamp"]))
  try:
    dt_utc = datetime.fromtimestamp(pretty_ts, tz=ZoneInfo("UTC"))
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
  except Exception:
    pass
  entry["timestamp"] = pretty_ts

# Get alerts by user dictionary list
alerts_by_user = alert.get("alerts_by_user", {})

#convert unix timestamps to human readable timestamps
for entry in alerts_by_user[source_user]:
  pretty_ts = int(float(entry["timestamp"]))
  try:
    dt_utc = datetime.fromtimestamp(pretty_ts, tz=ZoneInfo("UTC"))
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
  except Exception:
    pass
  entry["timestamp"] = pretty_ts

#Build the payload with alerts_by_ip and alerts_by_user and convert it to json string
alerts_history = json.dumps({
  "alerts_by_ip": alerts_by_ip,
  "alerts_by_user": alerts_by_user
}, indent=2)

#Format it for pretty json
content = (
  "```json\n"
  f"{alerts_history}\n"
  "```"
)

#Final Payload will include:
#Title of Page: Case History
#Content: The alerts by ip for a specific ip in the last hour | the alerts by user for a specific user in the last hour
#Category: The right sidebar tab that it will be organized under: Investigation 
payload = {
  "title": "Case History:",
  "content": content,
  "category": "Investigation"
}


print(json.dumps(payload, ensure_ascii=False))
