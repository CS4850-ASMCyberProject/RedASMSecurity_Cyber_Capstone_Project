from zoneinfo import ZoneInfo
from datetime import datetime
import json, base64
import re
import time

#This function returns an integer between 0-3 which scores the wazuh alert level
#If the wazuh level is greater than 10, then it gets the highest score at 3 and so on
def getwazuhlvl(level):
	if level >= 10:
		return 3
	if level >= 7:
		return 2
	if level >= 4:
		return 1
	else:
		return 0

#This function returns an integer between 0-3 which scores the mitre tactic score 
#if the tactic is of high privilige, it gets the highest score at 3 and so on
def getmitrelvl(mitre_tactic):
    mitre_tactic = mitre_tactic.split(", ")
    score = []
    for tactic in mitre_tactic:
        
        Mitre_Tactic_Score = {

        "Reconnaissance": 0,
        "Resource Development": 0,

        "Initial Access": 1,
        "Discovery": 1,

        "Execution": 2,
        "Collection": 3,

        "Persistence": 3,
        "Privilege Escalation": 3,
        "Defense Evasion": 3,
        "Credential Access": 3,
        "Lateral Movement": 3,
        "Command and Control": 3,
        "Exfiltration": 3,
        "Impact": 3,
        }
        score.append(Mitre_Tactic_Score.get(tactic,0))

    maxscore = max(score)
    return maxscore


#This function returns an integer between 0-3 which determines if the CIA triad has been affected
# If the tactic score is a 3, this means that a tactic was used that affected confidentiality, and we add c to the set cia
# Since confidentiality mostly deals with web attacks, if the web_status_code is 200 or 304, meaning data was leaked or returned
# Then we capitalize the C and if it's capitalized, we return 3
#if a file has been changed and checksum or integrity is in the text of an event, add I to the set cia
#if denial or service is in text, add A to cia which affects availability
#a score is returned based on the length of the set cia
#If the length is greater than or equal to 2, return 3, else if it's 1, return 2, and if it's 0, return 0
def getimpactlvl(tactic_score, text, file_path, web_status_code):
    cia = set()
    
    if tactic_score == 3:
      cia.add("c")
      if web_status_code in ("200", "304"):
        cia = {c.upper() for c in cia}
    if "checksum" in text.lower() or "integrity" in text.lower() or file_path:
        cia.add("I")
    if "denial" in text.lower() or "dos" in text.lower():
        cia.add("A")
        
    if len(cia) >= 2:
        return 3
    if len(cia) == 1:
      if "C" in cia:
        return 3
      else:
        return 2
    else:
        return 0

#Returns a string that determines the severity of each alert based on the
#severity_score which is calculated by the sum of the impactscore, wazuhlvl, and mitrelvl
def getseveritylvl(severity_score):
	if severity_score >= 9:
		severity = "Critical"
	elif severity_score >= 6:
		severity = "High"
	else:
		severity = "Low"

	return severity	

#returns the file_path for an event if it was an integrity changing event
def parsefile(text: str):
    file_path = ""
    
    m = re.search(r"File\s+'([^']+)'", text or "")
    if m:
        file_path = m.group(1)
        
    return file_path

#Returns the changed attributes (SHA256) of an integrity changing event
def parseattr(text: str):
    changed_attributes = ""
    
    m = re.search(r"Changed attributes:\s*([^\r\n]+)", text or "")
    if m:
        changed_attributes = m.group(1).strip().split(",")

        cleaned = changed_attributes
		
        changed_attributes = ", ".join(cleaned)
        
    return changed_attributes

#Sets the severity emoji color based on the severity rating of the event 
def severityemoji(severity):
	if severity == "Critical":
		return "🔴"
	elif severity == "High": 	
		return "🟠"
	else:
		return "🟢"

#Correlate Alert uses two dictionaries that correlate alerts within the last hour based 
#on a specific ip or a specific user and determines whether each cached data meets the 
#threshold to be a regular attack or burst attack. If a source ip or user has 5 alerts 
#within the last hour, it is a regular attack, if there are 3 alerts within the last 3 minutes,
#then it is a burst attack. This function returns two booleans: reg_attack and burst
def correlate_alert(source_ip, source_user, alerts_by_ip, alerts_by_user, ts):
	#Check if source_ip or source_user is empty
    if source_ip == "None" and source_user == "None":
      return False, False
    now = time.time()
    ip_alerted = []
    user_alerted = []
    burst = False
    reg_attack = False
    burst_count = 0
    one_hour_ago = now - 3600
    three_minutes_ago = now - 180

	#If source_ip not empty and the timestamp in alerts_by_ip is within the last hour, add the ip_alerted for the source_ip
    if source_ip != "None":
      for entry in alerts_by_ip[source_ip]:
          if entry["timestamp"] >= one_hour_ago:
              ip_alerted.append(entry["timestamp"])

	  #If the length of ip_alerted is greater than or equal to 5, it is a regular attack 
      if len(ip_alerted) >= 5:
          reg_attack = True

	  # Check if it's a burst attack. If the timestamps in ip_alerted are within the last 3 minutes and there are three
	  # Then this is a burst attack
      for ts in ip_alerted:
          if ts >= three_minutes_ago:
              burst_count = burst_count + 1
      if burst_count >= 3:
          burst = True
  
      burst_count = 0

	#Do the same above for the user 
    if source_user != "None":
      for entry in alerts_by_user[source_user]:
          if entry["timestamp"] >= one_hour_ago:
              user_alerted.append(entry["timestamp"])
  
      if len(user_alerted) >= 5:
          reg_attack = True
  
      for ts in user_alerted:
          if ts >= sixty_seconds_ago:
              burst_count = burst_count + 1
      if burst_count >= 3:
          burst = True

    return reg_attack, burst

#Prune Sources keeps a cache limit in Shuffle on the data it stores for the
#dictionaries alerts_by_ip and alerts_by_user (used for correlate_alert). 
#It only holds alerts correlated to an ip or user within the last hour, and removes 
#older entries otherwise.
def prunesources(alerts_by_ip, alerts_by_user):
  now = time.time()
  one_hour_ago = now - 3600
  for ip in alerts_by_ip:
    alerts_by_ip[ip] = [e for e in alerts_by_ip[ip] if e["timestamp"] >= one_hour_ago]
  for user in alerts_by_user:
    alerts_by_user[user] = [e for e in alerts_by_user[user] if e["timestamp"] >= one_hour_ago]

#Function that adds the current alert to alerts_by_ip or alerts_by_user if they exist.
#Both are dictionaries with the key the specific ip or user and the value is a list 
#of dictionaries which hold the timestamp of that alert and the associated ip or user
def addalert(source_ip, ts, source_user):
    if source_ip == "None"and source_user == "None":
      return
    if source_ip not in alerts_by_ip and source_ip != "None":
        alerts_by_ip[source_ip] = []
        alerts_by_ip[source_ip].append({"timestamp": ts, "user": source_user})
    elif source_ip != "None":
        alerts_by_ip[source_ip].append({"timestamp": ts, "user": source_user})
    if source_user not in alerts_by_user and source_user != "None":
        alerts_by_user[source_user] = []
        alerts_by_user[source_user].append({"timestamp": ts, "ip": source_ip})
    elif source_user != "None":
        alerts_by_user[source_user].append({"timestamp": ts, "ip": source_ip})

    return alerts_by_ip, alerts_by_user

#Get Promote Score is the main logic used to determine whether an alert should be promoted
#to a case that a soc analyst must investigate and determine a reasonable response. 
#It returns a dictionary that breaks down the total score of promotescore and scores each alert
#based on:
#severity_score - Scored based on whether it's severity is Low, High, or Critical
#unknown_ip_score - Scored on if the ip is known or unknown, compared against a list of friendly ips
#burstscore - Scored based on whether the attack has had 3 or more related alerts in the last minute
#regular_attack_score - Scored on whether the attack has had 5 or more related alerts in the last hour
#unknown_region_score - Scored based on wether the source ip is from a different region other than Georgia
#hardpromote - True or False based on whether the alert reaches a severity of Critical
#webattackscore - Checks if the attack group is in web_attack, and if the text includes SQL injection related words, add 1
def getpromotescore(severity, source_ip, source_user, burst, reg_attack, attack_group, text):
    hardpromote = False
    severityscore = 0
    unknownipscore = 0
    burstscore = 0
    reg_attackscore = 0
    unknownregionscore = 0
    webattackscore = 0
    database_leak_words = ["cards", "wallets", "sqlite_master", "addresses", "basketitems", "baskets", "captchas", "users"]

    if severity == "Critical":
        hardpromote = True
    elif severity == "High":
        severityscore += 3
    elif severity == "Low":
        severityscore += 1

    if source_ip in friendlyips:
        unknownipscore -= 3
    else:
        unknownipscore += 1
    if burst:
        burstscore += 3
    elif reg_attack:
        reg_attackscore += 2

    region = getregion(source_ip)
    if region and region != "Georgia":
        unknownregionscore += 2
        
    if attack_group == "web_attack": 
      if any(word in text.lower() for word in database_leak_words):
        webattackscore += 1

    totalscore = severityscore + unknownipscore + burstscore + reg_attackscore + unknownregionscore + webattackscore 

    promotescore = {
        "total": totalscore,
        "severity_score": severityscore,
        "unknown_ip_score": unknownipscore,
        "burst_score": burstscore,
        "regular_attack_score": reg_attackscore,
        "unknown_region_score": unknownregionscore,
        "web_attack_score": webattackscore,
        "hard_promote": hardpromote
    }

    return promotescore

#Function that gets the region (state) from which the ip came from
def getregion(source_ip):
    if source_ip == "None":
        return
    try:
        response = requests.get(f"https://ipinfo.io/{source_ip}/json")
    except requests.RequestException:
        return "Georgia"
    data = response.json()
    region = data.get("region", "")
    return region

#Categorize Attack uses the groups of the alert to assign a broader category of the type of attack it is.
#Authentication - ssh attacks, brute force, auth fail and success attacks
#File_Integrity - file integrity management attacks
#Web_Attack - Any server, HTTP, or web app attack
#Recon - Recon scanning
#Dos - denial of service attacks
def categorizeatt(groups_list):
    check_group = {
    "authentication": ["syslog", "sshd", "authentication failures", "authentication_failed"],
    "file_integrity": ["ossec", "syscheck", "syscheck_entry_modified", "syscheck_file"],
    "web_attack": ["web", "apache", "nginx", "sql_injection"],
    "recon": ["scan", "recon", "portscan"],
    "dos": ["dos"]
}

    for category in check_group:
        for entry in check_group[category]:
            if entry in groups_list:
                return category

    return "other"

def int_to_float(value: str):
  try:
    int(float(value))
  except (ValueError, TypeError):
    return 0
		
#CONSTANTS / Must add boolean variables because calling the cached datastores from shuffle use true and false which are invalid in Python
TTL_SECONDS = 300
true = True 
false = False
null = None

friendlyips = [
    "73.43.228.109",
    "100.70.35.63",
    "153.33.195.74",
    "104.185.200.147",
    "99.120.241.179",
    "174.49.72.16",
    "168.28.186.189"
]

#msg is used as a base dummy value to pass into json.dumps
#for messages with level lower than 7. Message is empty so
#alerts are not sent for these messsages
msg = {"success": True, "message": ""}

#The data passed into the script is raw $exec data, we
#convert it to json then to exec_b64 so that there aren't any
#formatting or type errors while passing the data in Shuffle.
#Also we use a r string so that the formatting is more legible.
exec_b64 = r'''{{ $exec | tojson | base64_encode }}'''

#Convert base64 to a Json String
data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

#Get the wazuh level for the message (0-16)
level = data.get("all_fields", {}).get("rule", {}).get("level", 0)

#Filter Packets and show only alerts above level 6
if level < 6:

    #Must make print statement even for alerts less than 6
    #because data passed in Shuffle is based on the previous alert
    #You don't run a print statement an error occurs
    print(json.dumps(msg))
    #exit the code/next alert
    raise SystemExit

#Get the severity (0-5)
severity = data.get("severity", "")

#Get the text (file-log)
text = data.get("text", "")

#Get the title (description)
title = data.get("title", "")

#Get the rule-id (wazuh alert code)
rule_id = data.get("rule_id", "unknown_rule")

#Get the web status code for web attacks 
web_status_code = data.get("all_fields", {}).get("data", {}).get("id", "")

#Get the source_ip
source_ip = data.get("all_fields", {}).get("data", {}).get("srcip", "")

#If source_ip does not exist, set it to a string "None"
if not source_ip:
  source_ip = "None"

#Get the source_user
source_user = data.get("all_fields", {}).get("data", {}).get("srcuser", "")

#If source_user does not exist, set it to a string "None"
if not source_user:
  source_user = "None"

#Get the current unix timestamp of the alert
id = data.get("id", "")

#set the id unix timestamp as a float used throughout functions to compare timestamps
ts = float(id)

#human readable timestamp used for alert cards in slack and converted to pretty_ts
timestamp = data.get("timestamp", "")

#make ts pretty use datetime & change utc to est
pretty_ts = timestamp
try:
    dt_utc = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
except Exception:
    pass

#Capture the group list
groups_list = data.get("all_fields", {}).get("rule", {}).get("groups", [])

#lower case the str for each group
groups_list = [str(g).lower() for g in groups_list]

# Get the alerts by ip dictionary
alerts_by_ip_raw =r'''{{$get_alerts_by_ip.value | default({}) | tojson}}'''

#Normalize  alerts_by_ip and convert it to an empty dictionary if no results
#Must do this because calling the shuffle variable $get_alerts_by_ip.value could be empty and it'll cause an error 
#If it's not handled and converted to an empty string 
if not alerts_by_ip_raw or alerts_by_ip_raw.strip() == "":
    alerts_by_ip = {}
else:
    try:
        alerts_by_ip = json.loads(alerts_by_ip_raw)
    except json.JSONDecodeError:
        alerts_by_ip = {}

#Do the same thing about but with alerts by user
alerts_by_user_raw =r'''{{$get_alerts_by_user.value | default({}) | tojson}}'''

if not alerts_by_user_raw or alerts_by_user_raw.strip() == "":
    alerts_by_user = {}
else:
    try:
        alerts_by_user = json.loads(alerts_by_user_raw)
    except json.JSONDecodeError:
        alerts_by_user = {}

#get the mitre dictionary
mitre = data.get("all_fields", {}).get("rule", {}).get("mitre", {})

#Get the mitre ID
mitre_id = ", ".join(mitre.get("id", ""))

#Get the mitre tactic
mitre_tactic = ", ".join(mitre.get("tactic", []))

#Get the mitre technique
mitre_technique = ", ".join(mitre.get("technique", "")) 

#Get the agent dictionary
agent = data.get("all_fields", {}).get("agent", {})

#Get the agent name
agent_name = agent.get("name", "")

#Get the agent IP
agent_ip = agent.get("ip", "")

#Get the agent ID
agent_id = agent.get("id", "unknown_agent")

#Correlation-key for threading slack events (agent_id + rule_id)
corrkey = agent_id + ":" + rule_id

#Get the file_path 
file_path = parsefile(text)

#Get the changed_attributes 
changed_attributes = parseattr(text)

#Variable that holds the current time
now = int(time.time())

#Found holds True or False if there is a stored thread in get_thread cache node
found = $get_set_thread_ts.found

#Get the value (thread timestamp, last seen, source_ip, corrkey) for each get thread cache (returns dict)
raw_thread = $get_set_thread_ts

#Initialize a string that will hold the thread_ts for slack threading
parent_ts = ""

#Initialize expired to True
expired = True

#Threading flag used in shuffle workflow to determine if current alert should be threaded
threading = False

#Initialize stored_thread to empty dict and will store raw_thread after checking
#it's parameters to ensure safe handling
stored_thread = {}

#Get the wazuhlvl (score 0-3)
wazuhlvl = getwazuhlvl(level)
#Get the mitrelvl (score 0-3)
if mitre_tactic:
  mitrelvl = getmitrelvl(mitre_tactic)
else:
  mitrelvl = 0
#Get the impact score (score 0-3)
impactlvl = getimpactlvl(mitrelvl, text, file_path, web_status_code)
#Add the wazuhlvl, mitrelvl, and impactscore together to get severity score which categorizes each even as Low, High, Critical
severitylvl = wazuhlvl + mitrelvl + impactlvl
#Get the severity level for each event which is a string between Low, High, and Critical
severity = getseveritylvl(severitylvl)
#Get the emoji severity color (Green, Orange, Red)
emoji = (severityemoji(severity))

#pruncesources of alerts more than an hour ago
prunesources(alerts_by_ip, alerts_by_user)

#add current alert if it has source_ip or source_user
addalert(source_ip, ts, source_user)

#Call correlate_alert and determine if the current source_ip or source_user if involved in a regular_attack or burst attack
reg_attack, burst = correlate_alert(source_ip, source_user, alerts_by_ip, alerts_by_user, ts)

#initialize promotescore dictionary
promotescore = {}

#Call attack_group to determine the category of attack based on the groups assocaited with the attack
attack_group = categorizeatt(groups_list)

#Call getpromotescore to determine if alert should be promoted to case
promotescore = getpromotescore(severity, source_ip, source_user, burst, reg_attack, attack_group, text)

#Fields holds information about the wazuh level of each event, the wazuh rule ID, and the time stamp
fields = [
	{ "type": "mrkdwn", "text": f"*Level*: {level or ''}" },
	{ "type": "mrkdwn", "text": f"*Rule ID*: {rule_id or ''}" },
	{ "type": "mrkdwn", "text": f"*Time*: {pretty_ts or ''}" },
]

#A list of triage links used for investigation into a recently promoted case
#Will include a call to ipinfo.com using source_ip to determine maliciousness
#A full event dump of the alert linked in GitHub
#A case link to TheHive case 
#A wazuh in the last 24 hours for a specific ip if alert has a source_ip
#A runbook for the type of attack based on the attack_group
triage_links = [

]

#Tells the soc analyst how to respond to cases to close them as benign or escalate to level 2
respond = [
  { "type": "mrkdwn", "text": f"Close As Benign: React with ✅ & reply in thread with reason."},  
  { "type": "mrkdwn", "text": f"Escalate to L2: React with 🚨 & reply in thread with reason."}
]

#A List of Action buttons if an alert gets promoted to a case
#Contain Path to contain path from SQL Injection 
#Block IP for any attack with a source_ip
action_buttons = [
  
]


#If the agent_ip is collected, insert this field markdown as the first field
if agent_ip:
    fields.insert(0, { "type": "mrkdwn", "text": f"*Name & IP*: {agent_name or ''} - {agent_ip}" })
else:
    fields.insert(0, { "type": "mrkdwn", "text": f"*Name*: {agent_name or ''}" })
#If the mitre information is collected, add the Mitre ID, Tactic, and technique to the fields
if mitre:
	fields.append({ "type": "mrkdwn", "text": f"*MITRE ATT&CK - ID*: {mitre_id or ''} *Tactic*: {mitre_tactic or ''} *Technique*: {mitre_technique or ''}" })
#If the file_path is collected, add the field_path to the fields
if file_path:
	fields.append({ "type": "mrkdwn", "text": f"*File Path*: {file_path or ''}" })
#If changed_attributes is collected, add it to fields 
if changed_attributes:
	fields.append({ "type": "mrkdwn", "text": f"*Changed Attributes*: {changed_attributes or ''}" })
 
#blocks is a list which holds the header and fields of each alert card
blocks = [
	{ "type": "header", "text": { "type": "plain_text", "text": f"{emoji} [{severity}] - {title}"}},
	{ "type": "section", "fields": fields }
]

#if source_ip exists, create a button linked to a query of the source_ip on ipinfo.com, a malicious ip database
if source_ip and source_ip != "None":
  triage_links.append({ "type": "button", 
  "text": { "type": "plain_text", "text": "🌍 IPInfo"},
  "url": f"https://ipinfo.io/{source_ip}"})
  action_buttons.append({ "type": "button", 
  "text": { "type": "plain_text", "text": "🚫 Block IP"},
  "style": "danger",
  "action_id": "block_ip",
  "value": source_ip})

#If any of the alerts comes from the custom alerts made for SQL injection, then add a button used to contain 
#the path /rest/products/search in the exposed service OWASP juice shop from shop.redasmsecurity.cloud
if rule_id in ["100313", "100314", "100316"]:
  action_buttons.insert(0, {"type": "button",
  "text": { "type": "plain_text", "text": "🔐 Contain Path"},
  "style": "danger",
  "action_id": "block_sql"
  })

#Alert is the final payload dictionary that specifies the Slack channel, the header, and the blocks 
alert = {
    "text": f"[{severity}] - {title}",
    "description": f"Wazuh Alert: Target - {agent_ip} Attack: {title}",
    "channel": "C0AB0J5V9QE" if promotescore.get("total", 0) >= 5 or promotescore.get("hard_promote", False) else "C0AB651MRFE",
    "blocks": blocks,
    "corrkey": corrkey,
    "last_seen": now,
    "timestamp": pretty_ts,
    "promote_to_case": "false",
    "threading": "false",
    "mitre_id": mitre_id,
    "mitre_tactic": mitre_tactic,
    "mitre_technique": mitre_technique,
    "alerts_by_ip": alerts_by_ip,
    "alerts_by_user": alerts_by_user,
    "severity_emoji": emoji,
    "observables": {
        "agent_ip": agent_ip,
        "source_ip": source_ip,
        "source_user": source_user,
        "attack_group": attack_group,
        "rule_id": rule_id,
        "file_path": file_path,
        "severity": severity,
        "severity_level": severitylvl,
        "mitre": mitre
    }
}

#Conditional statement that checks if found and raw_thread are true
#If so, checks if raw_thread is a dictionary or str, if empty str, stored_thread
#stays empty dict, otherwise stored_thread becomes raw_thread
if found and raw_thread:
  if isinstance(raw_thread, str):
    try:
      stored_thread = json.loads(raw_thread)
    except Exception:
      stored_thread = {}
  elif isinstance(raw_thread, dict):
    stored_thread = raw_thread
  
#Check to see if stored thread holds the information needed from the get cache node to determine if the current alert 
#needs to be threaded or not.
#There must be a parent timestamp, a last seen value, and a corrkey
parent_ts = stored_thread.get("value", {}).get("Set_Thread_TS", "")
get_last_seen = stored_thread.get("value", {}).get("last_seen", "")
get_corrkey = stored_thread.get("value", {}).get("corrkey", "")

#If there is all three of these, then set expired, a boolean which determines if the last related alert was within 5 minutes
#If it is, then set expired to False.
#If it is not, then set expired to True
if parent_ts and get_last_seen and corrkey == get_corrkey:
  get_last_seen = int(float(get_last_seen))
  expired = (now - get_last_seen) > 300

#If the last related alert has not expired, then set threading to true
#Add the parent thread timestamp to the current alert to be threaded 
#Else remove the thread timestamp value from the current alert and set threading to false 
if not expired:
  alert["threading"] = "true"
  alert["thread_ts"] = str(parent_ts)
else:
  alert.pop("thread_ts", None)
  alert["threading"] = "false"

#If promote score is true, add triage links dictionary list, action buttons dictionary list, and respond list
#If hard promote is True, set it to "true" because of Shuffle handling which uses lowercase true not uppercase Python True
#Same thing with false
if promotescore.get("total", 0) >= 5 or promotescore.get("hard_promote", False):
  alert["promote_score"] = promotescore
  if promotescore.get("hard_promote", False):
    alert["promote_score"]["hard_promote"] = "true"
  else:
    alert["promote_score"]["hard_promote"] = "false"
  alert["promote_to_case"] = "true"
  get_source_ip = stored_thread.get("source_ip", "")
  if source_ip == "None" or source_ip != get_source_ip:
    alert["threading"] = "false"
  blocks.append({ "type": "section", "text": { "type": "mrkdwn", "text": "Investigate:" }})
  blocks.append({ "type": "divider"})
  blocks.append({ "type": "actions", "elements": triage_links })
  if not source_ip or source_ip != "None":
    blocks.append({ "type": "section", "text": { "type": "mrkdwn", "text": "Take Action:" }})
    blocks.append({ "type": "divider"})
    blocks.append({ "type": "actions", "elements": action_buttons })
  blocks.append({ "type": "section", "text": { "type": "mrkdwn", "text": "Respond:" }})
  blocks.append({ "type": "divider"})
  blocks.append({ "type": "section", "fields": respond })

#Print json.dumps with the alert 
print(json.dumps(alert))
