import json, base64

#The data passed into the script is raw $exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''

data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

source_user = data.get("all_fields", {}).get("data", {}).get("srcuser", "") or data.get("all_fields", {}).get("data", {}).get("dstuser", "")

if not source_user:
  pass
else:
  user = {"source_user": source_user}
  print(json.dumps(user))
