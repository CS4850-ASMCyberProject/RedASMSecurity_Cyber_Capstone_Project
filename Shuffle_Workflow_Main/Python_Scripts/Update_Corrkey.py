import json, base64

#Get the custom python script alert in Shuffle. Use this encoding convert to base 64 for safe handling in Shuffle
decoded = r'''{{ $python_slack_script.message | tojson | base64_encode }}'''
alert = base64.b64decode(decoded).decode("utf-8")

#Convert to Json String 
alert = json.loads(alert)

#Get the Corrkey
corrkey = alert.get("corrkey", "")

#Add the thread timestamp to the corrkey for thehive 
#This is similar to Slack Threading, where alerts are threaded together if it's a related alert set off within the last 5 minutes
#Else the Corrkey adds a new parent timestamp to create a new alert in thehive
update_corrkey = corrkey + ":" + "$set_new_thread_ts.value.Set_Thread_TS"

#Update Corrkey in the alert payload
alert["corrkey"] = update_corrkey

#Print json.dumps with the alert 
print(json.dumps(alert))
