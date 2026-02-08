from zoneinfo import ZoneInfo
from datetime import datetime
import json, base64
import re


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
    
    m = re.search(r"Changed attributes:\s*([^r\n]+)", text or "")
    if m:
        changed_attributes = m.group(1).strip().split(",")

        cleaned = changed_attributes
		
        changed_attributes = ", ".join(cleaned)
        
    return changed_attributes

#Sets the severity emoji color based on the severity rating of the event 
def severityemoji(severity):
	if severity == "Critical":
		return "??"
	elif severity == "High": 	
		return "??"
	else:
		return "??"
		

#group_list is used to capture the list of groups in the metadata
group_list = []

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
rule_id = data.get("rule_id", "")

#Get the timestamp
ts = data.get("timestamp", "")

#make ts pretty use datetime & change utc to est
pretty_ts = ts
try:
    dt_utc = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z")
    dt_est = dt_utc.astimezone(ZoneInfo("America/New_York"))
    pretty_ts = dt_est.strftime("%b %d %Y, %I:%M:%S %p %Z")
except Exception:
    pass

#Capture the group list
groups_list = data.get("all_fields", {}).get("rule", {}).get("groups", [])

#lower case the str for each group
for g in groups_list:
    str(g).lower()

#make a groups string and join the list into a string delimited by space
groups = " ".join(groups_list)

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

#Get the file_path 
file_path = parsefile(text)

#Get the changed_attributes 
changed_attributes = parseattr(text)

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

#Fields holds information about the wazuh level of each event, the wazuh rule ID, and the time stamp
fields = [
	{ "type": "mrkdwn", "text": f"*Level*: {level or ''}" },
	{ "type": "mrkdwn", "text": f"*Rule ID*: {rule_id or ''}" },
	{ "type": "mrkdwn", "text": f"*Time*: {pretty_ts or ''}" },
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

#Alert is the final payload dictionary that specifies the Slack channel, the header, and the blocks 
alert = {
    "channel": "C0AB651MRFE",
    "blocks": blocks
}

#Print json.dumps with the alert 
print(json.dumps(alert))