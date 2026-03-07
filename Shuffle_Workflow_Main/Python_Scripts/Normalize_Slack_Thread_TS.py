import json, base64

#The data passed into the script is raw exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
slack_alert = json.loads(r'''{{$sp-108-redasm_cases.body | default({}) | tojson}}''')

slack_case = json.loads(r'''{{$sp-108-redasm_alerts.body | default({}) | tojson}}''')

alert = slack_alert if slack_alert else slack_case
  
print(json.dumps(alert, ensure_ascii=False))
