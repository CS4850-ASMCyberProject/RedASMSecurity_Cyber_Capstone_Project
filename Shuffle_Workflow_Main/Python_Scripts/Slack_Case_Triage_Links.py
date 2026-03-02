import json

null = None
alert = $python_slack_script.message
blocks = alert.get("blocks", [])
github_url = "$github_cyber_event_archive.body.content.html_url"

if alert.get("observables", {}).get("attack_group", "") == "authentication":
  runbook_url = "https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/austin-runbooks/runbooks/auth-bruteforce-linux.md"
elif alert.get("observables", {}).get("attack_group", "") == "file_integrity":
  runbook_url = "https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/austin-runbooks/runbooks/fim-linux.md"

# Find the first actions block and append button
for b in blocks:
    if b.get("type") == "actions":
        b.get("elements", []).append({
            "type": "button",
            "text": {"type": "plain_text", "text": "📄 Full Event (GitHub)"},
            "url": github_url
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
