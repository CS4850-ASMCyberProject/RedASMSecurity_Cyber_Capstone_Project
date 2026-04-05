import json, base64

#Normalize the output of Slack Cases and Slack Alerts needed to set the thread timestamps of both channels in Slack 
#Each alert will only be posted to either Slack Alerts or Slack Cases, each of which has a single node in Slack for posting.
#Normalize Slack Thread TS Script simply gets the payload from each node and puts it into a varaible slack_alert or slack_case.
#We then normalize the output of both results by putting it into a variable called alert using a conditional because only 1 variable will have output.
#The other will be empty. 
slack_alert = json.loads(r'''{{$sp-108-redasm_cases.body | default({}) | tojson}}''')

slack_case = json.loads(r'''{{$sp-108-redasm_alerts.body | default({}) | tojson}}''')

alert = slack_alert if slack_alert else slack_case
  
print(json.dumps(alert, ensure_ascii=False))
