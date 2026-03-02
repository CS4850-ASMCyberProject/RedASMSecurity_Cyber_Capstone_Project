import json, base64

#The data passed into the script is raw $exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
decoded = r'''{{ $python_slack_script.message | tojson | base64_encode }}'''

alert = base64.b64decode(decoded).decode("utf-8")

alert = json.loads(alert)

corrkey = alert.get("corrkey", "")

update_corrkey = corrkey + ":" + "$set_new_thread_ts.value.Set_Thread_TS"

alert["corrkey"] = update_corrkey

#Print json.dumps with the alert 
print(json.dumps(alert))
