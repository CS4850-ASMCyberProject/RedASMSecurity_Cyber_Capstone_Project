import json

alert = $python_slack_script.message

promotescore = alert.get("promote_score", {})

total = promotescore.get("total", 0)

severitycore = promotescore.get("severity_score", 0)

unknownipscore = promotescore.get("unkown_ip_score", 0)

burstscore = promotescore.get("burstscore", 0)

regattackscore = promotescore.get("regular_attack_score", 0)

unknownregionscore = promotescore.get("unknown_region_score", 0)

hardpromote = promotescore.get("hard_promote", "")

if hardpromote == "true":
  hardpromote = True
else:
  hardpromote = False

severity = alert.get("observables", {}).get("severity", "")

severityscore = alert.get("observables", {}).get("severity_score", 0)

content = (
  f"### Severity Level\n- **{severity}**\n"
  "### Promote Score\n\n"
   "| Metric | Value |\n"
   "|--------|-------|\n"
  f"|🔢 *Total*: |{total}|\n"
  f"|⚠️ *Severity Score*: |{severityscore}|\n"
  f"|🌐 *Unknown IP Score*: |{unknownipscore}|\n"
  f"|⚡ *Burst Score*: |{burstscore}|\n"
  f"|🔁 *Regular Attack Score*: |{regattackscore}|\n"
  f"|🌍 *Unkown Region Score:* |{unknownregionscore}|\n"
  f"|🚨 *Hard Promote:* |{hardpromote}|\n"
)

payload = {
  "title": "Case Scoring:",
  "content": content,
  "category": "Investigation"
}


print(json.dumps(payload, ensure_ascii=False))
