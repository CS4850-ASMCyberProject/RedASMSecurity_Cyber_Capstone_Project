import json

# Convert null to None as Json alerts have null which Python does not recognize 
null = None

# Get the custom slack script full message
alert = $python_slack_script.message

#Get the blocks from the alert
blocks = alert.get("blocks", [])

#Get the output from the github cyber event http node for the github event triage button
github_url = "$github_cyber_event_archive.body.content.html_url"

#Get the source ip 
source_ip = alert.get("observables", {}).get("source_ip", "")

#Define the base wazuh URL
wazuh_base_url = "https://wazuh.redasmsecurity.cloud"

# Build the Wazuh Triage Link which includes the base wazuh url, and the path which shows the alerts in the 
# last 24 hours for the source ip tied to the case
wazuh_url = (
    f"{wazuh_base_url}/app/threat-hunting#/overview/"
    f"?tab=general&tabView=events"
    f"&_a=(filters:!(),query:(language:kuery,query:'data.srcip:{source_ip}'))"
    f"&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-24h,to:now))"
)

#Get thehive case id
thehive_case_id = "$thehive_promote_to_case.body._id"

# Build the base thehive case
thehive_base_url = "https://thehive.redasmsecurity.cloud"

# Build the thehive case triage link which icludes thehive base url and the case id
thehive_url = (
  f"{thehive_base_url}/thehive/cases/{thehive_case_id}/details"
)

# Determine which runbook should be added to the case 
# If the case is from the attack group authentication (ssh attacks), add the brute force runbook
# If the case if from the attack group file integrity, add the File Integrity Monitoring runbook
if alert.get("observables", {}).get("attack_group", "") == "authentication":
  runbook_url = "https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/austin-runbooks/runbooks/auth-bruteforce-linux.md"
elif alert.get("observables", {}).get("attack_group", "") == "file_integrity":
  runbook_url = "https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/austin-runbooks/runbooks/fim-linux.md"


# Build the Triage Buttons and add each button to a case depending on the type of case or attack it is
# Every case will include the GitHub Full Event link which is the original Wazuh Alert using Pretty Json
# Every case will include TheHive case link which will include certain internal python logic pages depening on the case
# If the case has a source_ip, Add the wazuh 24 hour link 
# Add the Runbook Triage Buttons depending on if the attack is from the authentication group (ssh attacks) or file integrity group
for b in blocks:
    if b.get("type") == "actions":
        b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "📄 Full Event (GitHub)"},
            "url": github_url
        })
        if source_ip and source_ip != "None":
          b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "🕒 Wazuh – Last 24h"},
            "url": wazuh_url
        })
        b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "🐝 TheHive Case"},
            "url": thehive_url
        })
        if alert.get("observables", {}).get("attack_group", "") == "authentication":
          b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "📘 Runbook – SSH Brute Force"},
            "url": runbook_url
        })
        elif alert.get("observables", {}).get("attack_group", "") == "file_integrity":
          b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "📘 Runbook – File Integrity"},
            "url": runbook_url
        })
        break

alert["blocks"] = blocks

print(json.dumps(alert, ensure_ascii=False))
