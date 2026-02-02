from zoneinfo import ZoneInfo

from datetime import datetime

import json, base64





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

#Get the agent ID

agent_ip = agent.get("ip", "")



#Generate the output for the alert

#** are for bold

#```{text}``` is for code block (put the file log in a code block)

alert = (



    f"*Wazuh Alert*\n"



    f"*Title*: {title}\n"



    f"*Name & IP*: {agent_name} - {agent_ip}\n"



    f"*Level*: {level}\n"



    f"*Rule ID*: {rule_id}\n"



    f"*Time*: {pretty_ts}\n"

    

    f"*MITRE ATT&CK -*\n"

    f"*ID:* {mitre_id}\n"

    f"*Tactic:* {mitre_tactic}\n"

    f"*Technique:* {mitre_technique}\n"



    f"```{text}```"



)



#Print json.dumps with the alert as the message/payload

print(json.dumps({"success": True, "message": alert}))
