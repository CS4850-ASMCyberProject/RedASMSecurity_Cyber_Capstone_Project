import json


#Get the full Custom Python Script alert in Shuffle
alert = $python_slack_script.message

#Get the promote score dictionary which includes a list of values for each type of atack score
promotescore = alert.get("promote_score", {})

#Get the total promote score
total = promotescore.get("total", 0)

#Get the severity score 
severitycore = promotescore.get("severity_score", 0)

#Get the unknowwn ip score
unknownipscore = promotescore.get("unkown_ip_score", 0)

#Get the burst score
burstscore = promotescore.get("burstscore", 0)

#Get the regular attacks score 
regattackscore = promotescore.get("regular_attack_score", 0)

#Get the unknown region score 
unknownregionscore = promotescore.get("unknown_region_score", 0)

#Get the hard promote boolean value
hardpromote = promotescore.get("hard_promote", "")

webattackscore = promotescore.get("web_attack_score", 0)

#Set Shuffle lowercase "true" to Python Uppercase True for better legibility in theHive
#Same with False 
if hardpromote == "true":
  hardpromote = True
else:
  hardpromote = False

#Get the severity Critical High Low
severity = alert.get("observables", {}).get("severity", "")

#Get the severity score 
severityscore = alert.get("observables", {}).get("severity_score", 0)

#Get the severity emoji
severity_emoji = alert.get("severity_emoji", "")

#Build the content which is displayed in two charts: the severity level chart and promote score chart 
#Severity Level Chart:
#Include the severity emoji and severity as level
#Include the severity level as the value
#Promote Score Chart:
#Include the Severity Score which is the sum of wazuh level, mitre level, impact level
#Include the unknown ip score
#Include the burst score
#Include the regular attack score 
#Include the web attack score
#Include the unknown region score
#Include the hard promote score a boolean value 
#Include the total promote score 
content = (
  f"### Severity Level\n\n"
  "| Level | Value |\n"
  "|--------|-------|\n"
  f"**{severity_emoji} {severity}**| {severitylvl}\n\n\n"
  f"Scoring: Critical >= 9 | High >= 6 | Low < 6\n\n"
  "### Promote Score\n\n"
   "| Metric | Value |\n"
   "|--------|-------|\n"
  f"|⚠️ *Severity Score*: |{severityscore}|\n"
  f"|🌐 *Unknown IP Score*: |{unknownipscore}|\n"
  f"|⚡ *Burst Score*: |{burstscore}|\n"
  f"|🔁 *Regular Attack Score*: |{regattackscore}|\n"
  f"|💻 *Web Attack Score*: |{webattackscore}|\n"
  f"|🌍 *Unkown Region Score:* |{unknownregionscore}|\n"
  f"|🚨 *Hard Promote:* |{hardpromote}|\n"
  f"|🔢 *Total*: |{total}|\n\n\n"
  f"Scoring: Promote to Case if >= 5 or Hard Promote = True"
)

#Build the payload:
#Title: Case Scoring
#Content
#Category: Investigation which is the tab on the right to organize the alerts
payload = {
  "title": "Case Scoring:",
  "content": content,
  "category": "Investigation"
}


print(json.dumps(payload, ensure_ascii=False))
