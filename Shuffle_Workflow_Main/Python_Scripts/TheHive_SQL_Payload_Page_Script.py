import json, base64
import random
import urllib.parse

#The data passed into the script is raw $exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
status_code = $exec.all_fields.data.id
protocol = "$exec.all_fields.data.protocol"
base_url = "http://shop.redasmsecurity.cloud"
url_path = "$exec.all_fields.data.url"
full_url = f"{base_url}{url_path}"

url = urllib.parse.quote(full_url, safe=":/?&=%")

content = (
  f"{url}\n\n"
  f"### SQL Injection Path\n\n"
  f"| Metric | Value |\n"
  f"|--------|-------|\n"
  f"|💉SQLi|*{url_path}*|\n"
  f"|📬HTTP Protocol|{protocol}\n"
  f"|📊Status Code|{status_code}\n\n"
)

payload = {
  "title": "Data Leaked:",
  "content": content,
  "category": "Investigation"
}

print(json.dumps(payload, ensure_ascii=False))
