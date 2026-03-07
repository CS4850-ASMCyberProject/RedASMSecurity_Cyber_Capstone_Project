from datetime import datetime
from zoneinfo import ZoneInfo
import json

alert = $python_slack_script.message

alerts_by_ip = alert.get("alerts_by_ip", {})

source_ip = "$python_slack_script.message.observables.source_ip"

source_user = "$python_slack_script.message.observables.source_user"

for entry in alerts_by_ip[source_ip]:
  pretty_ts = int(float(entry["timestamp"]))
  try:
    dt_utc = datetime.fromtimestamp(pretty_ts, tz=ZoneInfo("UTC"))
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
  except Exception:
    pass
  entry["timestamp"] = pretty_ts

alerts_by_user = alert.get("alerts_by_user", {})

for entry in alerts_by_user[source_user]:
  pretty_ts = int(float(entry["timestamp"]))
  try:
    dt_utc = datetime.fromtimestamp(pretty_ts, tz=ZoneInfo("UTC"))
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
  except Exception:
    pass
  entry["timestamp"] = pretty_ts

alerts_history = json.dumps({
  "alerts_by_ip": alerts_by_ip,
  "alerts_by_user": alerts_by_user
}, indent=2)

content = (
  "```json\n"
  f"{alerts_history}\n"
  "```"
)

payload = {
  "title": "Case History:",
  "content": content,
  "category": "Investigation"
}


print(json.dumps(payload, ensure_ascii=False))
