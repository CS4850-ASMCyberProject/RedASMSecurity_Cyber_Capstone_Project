import json, base64
import random
import urllib.parse

#Page Used to showcase the data leaked for custom SQL injection alerts 
#get the status code, Http protocol, base url for OWASP juice shop, the url path that the attacker used
#Build the full url from base url and url path
status_code = $exec.all_fields.data.id
protocol = "$exec.all_fields.data.protocol"
base_url = "http://shop.redasmsecurity.cloud"
url_path = "$exec.all_fields.data.url"
full_url = f"{base_url}{url_path}"

#there were errors trying to post the url in shuffle, so we have to tell shuffle certain characters are safe 
url = urllib.parse.quote(full_url, safe=":/?&=%")

#Build the content:
#Include the SQL Injection attack URL at the top
#Build a chart that includes:
#SQL Injection path
#Http Protocol
#Web Status Code
content = (
  f"{url}\n\n"
  f"### SQL Injection Path\n\n"
  f"| Metric | Value |\n"
  f"|--------|-------|\n"
  f"|💉SQLi|*{url_path}*|\n"
  f"|📬HTTP Protocol|{protocol}\n"
  f"|📊Status Code|{status_code}\n\n"
)

#Build the final payload:
#Title of page is Data Leaked
#Content
#Category: Investigation which is the left hand side tab to organize the pages
payload = {
  "title": "Data Leaked:",
  "content": content,
  "category": "Investigation"
}

print(json.dumps(payload, ensure_ascii=False))
