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
	Mitre_Tactic_Score = {

    "Reconnaissance": 0,
    "Resource Development": 0,

    "Initial Access": 1,
    "Discovery": 1,

    "Execution": 2,
    "Collection": 2,

    "Persistence": 3,
    "Privilege Escalation": 3,
    "Defense Evasion": 3,
    "Credential Access": 3,
    "Lateral Movement": 3,
    "Command and Control": 3,
    "Exfiltration": 3,
    "Impact": 3,
    }

	score = Mitre_Tactic_Score.get(mitre_tactic,0)

	return score


#This function returns an integer between 0-3 which determines if the CIA triad has been affected
#If the tactic score is a 3, this means that a tactic was used that affected confidentiality, and we add C to the set cia
#if a file has been changed and checksum or integrity is in the text of an event, add I to the set cia
#if denial or service is in text, add A to cia which affects availability
#a score is returned based on the length of the set cia
def getimpactscore(tactic_score, text, file_path):
    cia = set()
    
    if tactic_score == 3:
        cia.add("C")
    if "checksum" in text.lower() or "integrity" in text.lower() or file_path:
        cia.add("I")
    if "denial" in text.lower() or "service" in text.lower():
        cia.add("A")
        
    if len(cia) >= 2:
        return 3
    if len(cia) == 1:
        return 2
    else:
        return 0

#Returns a string that determines the severity of each alert based on the
#severity_score which is calculated by the sum of the impactscore, wazuhlvl, and mitrelvl
def getseverityscore(severity_score):
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
#within the last hour, it is a regular attack, if there are 3 alerts within the last minute,
#then it is a burst attack. This function returns two booleans: reg_attack and burst
def correlate_alert(source_ip, source_user, alerts_by_ip, alerts_by_user, ts):
    if source_ip == "None"and source_user == "None":
      return False, False
    now = time.time()
    ip_alerted = []
    user_alerted = []
    burst = False
    reg_attack = False
    burst_count = 0
    one_hour_ago = now - 3600
    sixty_seconds_ago = now - 60

    for entry in alerts_by_ip[source_ip]:
        if entry["timestamp"] >= one_hour_ago:
            ip_alerted.append(entry["timestamp"])

    if len(ip_alerted) >= 5:
        reg_attack = True

    for ts in ip_alerted:
        if ts >= sixty_seconds_ago:
            burst_count = burst_count + 1
    if burst_count >= 3:
        burst = True

    burst_count = 0

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
def getpromotescore(severity, source_ip, source_user, burst, reg_attack):
    hardpromote = False
    severityscore = 0
    unknownipscore = 0
    burstscore = 0
    reg_attackscore = 0
    unknowncountryscore = 0

    if severity == "Critical":
        hardpromote = True
        return hardpromote, promotescore
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

    totalscore = severityscore + unknownipscore + burstscore + reg_attackscore + unknowncountryscore

    promotescore = {
        "total": totalscore,
        "severity_score": severityscore,
        "unknown_ip_score": unknownipscore,
        "burst_score": burstscore,
        "regular_attack_score": reg_attackscore,
        "unknown_region_score": unknownregionscore,
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
    "10.0.0.48",
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

data = json.loads(base64.b64decode(exec_b64).decode("utf-8"))

#Get the level for the message (0-16)
level = data.get("all_fields", {}).get("rule", {}).get("level", 0)

#Filter Packets and show only alerts above level 7
if level < 7:

    #Must make print statement even for alerts less than 7
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

#Dictionary used to associate related alerts to an ip, assigning a list of timestamps and users to an ip
alerts_by_ip = json.loads('{{ $get_alerts_by_ip.value | default({}) | tojson }}')

#Dictionary used to associate related alerts to a user, assigning a list of timestamps and ips to a user
alerts_by_user = json.loads('{{ $get_alerts_by_user.value | default({}) | tojson }}')

#get the mitre dictionary
mitre = data.get("all_fields", {}).get("rule", {}).get("mitre", {})

#Get the mitre ID
mitre_id = ", ".join(mitre.get("id", ""))

#Get the mitre tactic
mitre_tactic = ", ".join(mitre.get("tactic", ""))

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

#Get the value (thread_ts & expiresat) for each get thread cache (returns dict)
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
mitrelvl = getmitrelvl(mitre_tactic)
#Get the impact score (score 0-3)
impactscore = getimpactscore(mitrelvl, text, file_path)
#Add the wazuhlvl, mitrelvl, and impactscore together to get severity score which categorizes each even as Low, High, Critical
severityscore = wazuhlvl + mitrelvl + impactscore
#Get the severity level for each event which is a string between Low, High, and Critical
severity = getseverityscore(severityscore)
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

#Call getpromotescore to determine if alert should be promoted to case
promotescore = getpromotescore(severity, source_ip, source_user, burst, reg_attack)

#Call attack_group to determine the category of attack based on the groups assocaited with the attack
attack_group = categorizeatt(groups_list)

#Fields holds information about the wazuh level of each event, the wazuh rule ID, and the time stamp
fields = [
	{ "type": "mrkdwn", "text": f"*Level*: {level or ''}" },
	{ "type": "mrkdwn", "text": f"*Rule ID*: {rule_id or ''}" },
	{ "type": "mrkdwn", "text": f"*Time*: {pretty_ts or ''}" },
]

#A list of triage links used for investigation into a recently promoted case
#Will include a call to ipinfo.com using source_ip to determine maliciousness
#A full event dump of the alert linked in GitHub
#A runbook for the type of attack based on the attack_group
triage_links = [

]

#Tells the soc analyst how to respond to cases to close them as benign or escalate to level 2
respond = [
  { "type": "mrkdwn", "text": f"Close As Benign: React with ✅ & reply in thread with reason."},  
  { "type": "mrkdwn", "text": f"Escalate to L2: React with 🚨 & reply in thread with reason."}
]

#If the agent_ip is collected, insert this field markdown as the first field
if agent_ip:
    fields.insert(0, { "type": "mrkdwn", "text": f"*Name & IP*: {agent_name or ''} - {agent_ip}" })
else:
    fields.insert(0, { "type": "mrkdwn", "text": f"*Name*: {agent_name or ''}" })
#If the mitre information is collected, add the Mitre ID, Tactic, and technique to the fields
if mitre:
	fields.append({ "type": "mrkdwn", "text": f"*MITRE ATT&CK* - *ID*: {mitre_id or ''} *Tactic*: {mitre_tactic or ''} *Technique*: {mitre_technique or ''}" })
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

#if source_ip exists, create a button linked to a query of the source_ip on ipinfo.com, a malicious i database
if source_ip:
  triage_links.append({ "type": "button", 
  "text": { "type": "plain_text", "text": "🌍 IPInfo"},
  "url": f"https://ipinfo.io/{source_ip}"})

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
    "observables": {
        "agent_ip": agent_ip,
        "source_ip": source_ip,
        "source_user": source_user,
        "attack_group": attack_group,
        "rule_id": rule_id,
        "file_path": file_path,
        "severity": severity,
        "severity_score": severityscore,
        "mitre": mitre
    }
}

#Conditional statement that checks if found and raw_thread are true
#If so, checks if raw_thread is a dictionary or str, if empty str, stroed_thread
#stays empty dict, otherwise stored_thread becomes raw_thread
if found and raw_thread:
  if isinstance(raw_thread, str):
    try:
      stored_thread = json.loads(raw_thread)
    except Exception:
      stored_thread = {}
  elif isinstance(raw_thread, dict):
    stored_thread = raw_thread
  
#Get the stored parameters from stored_thread cached in get_thread node which will be used to 
#check how alerts should be posted to Slack. If the stored corrkey mateches the corrkey for 
#the current alert, and there is a timestamp (parent_ts) and expiresat, then set expired

#If all three return true, set newexpiresat to the current expiresat
#and check if expired is true or false based on the get_thread expiresat
#The Threading process has a 5min sliding window and persists as long 
#as there are alerts from that correlation key coming in.
parent_ts = stored_thread.get("value", {}).get("Set_Thread_TS", "")
get_last_seen = stored_thread.get("value", {}).get("last_seen", "")
get_corrkey = stored_thread.get("value", {}).get("corrkey", "")

if parent_ts and get_last_seen and corrkey == get_corrkey:
  get_last_seen = int(float(get_last_seen))
  expired = (now - get_last_seen) > 300

#Check if the stored  expires at time is less than current time
#If it is, expired becomes true and fails
#If it is not, expired becomes false and passes. Then add parent_ts and newexpiresat
#Otherwise, remove thread_ts from alert to ensure a new parent mesasge is posted
if not expired:
  alert["threading"] = "true"
  alert["thread_ts"] = str(parent_ts)
else:
  alert.pop("thread_ts", None)
  alert["threading"] = "false"

#If promote score is true, add triage links and respond to slack case for investigation and soc analyst response
if promotescore.get("total", 0) >= 5 or promotescore.get("hard_promote", False):
    alert["promote_to_case"] = "true"
    blocks.append({ "type": "section", "text": { "type": "mrkdwn", "text": "Investigate:" }})
    blocks.append({ "type": "divider"})
    blocks.append({ "type": "actions", "elements": triage_links })
    blocks.append({ "type": "section", "text": { "type": "mrkdwn", "text": "Respond:" }})
    blocks.append({ "type": "divider"})
    blocks.append({ "type": "section", "fields": respond })

#Print json.dumps with the alert 
print(json.dumps(alert))
