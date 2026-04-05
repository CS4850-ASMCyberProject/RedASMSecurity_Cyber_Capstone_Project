import json, base64

# Get the original wazuh alert
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''

# Convert to a Json string
data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

# Get the source user for certain alerts which is located in a different place than other alerts 
# Normalize the call. Most users are stored at srcuser, but some are at dstuser
# If it's an alert stored at dstuser, then normalize it as a variable called source_user
source_user = data.get("all_fields", {}).get("data", {}).get("srcuser", "") or data.get("all_fields", {}).get("data", {}).get("dstuser", "")

# If the source user is empty, meaning it's not an alert that stores the user at dstuser, then pass
# Else, add the source_user to a key source_user
if not source_user:
  pass
else:
  user = {"source_user": source_user}
  print(json.dumps(user))
