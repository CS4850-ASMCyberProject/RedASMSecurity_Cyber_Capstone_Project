# TheHive Promote to Case

## Purpose
Sends an HTTP POST request to TheHive to create a new case.

---

## Node Type
`Http Node`

---

## Setup

**Name:**
```text
TheHive_Promote_to_Case
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.17.0.1:9000/thehive/api/v1/case
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

**Body:**
```json
{
  "title": "## 🟠 $python_slack_script.message.text",
  "description": "### Attacker Information\n- User: $exec.all_fields.data.srcuser\n- IP: $exec.all_fields.data.srcip\n- Port: $exec.all_fields.data.srcport\n\n### Host Information\n- Name: $exec.all_fields.agent.name\n- IP: $exec.all_fields.agent.ip\n- Rule ID: $exec.all_fields.rule.id\n- Level: $exec.all_fields.rule.level\n- Time: $python_slack_script.message.timestamp\n\n### MITRE ATT&CK\n- Technique ID: $python_slack_script.message.mitre_id\n- Tactic: $python_slack_script.message.mitre_tactic\n- Technique: $python_slack_script.message.mitre_technique\n",
  "severity": 2,
  "status": "${status}",
  "tags": [
    "$python_slack_script.message.corrkey"
  ]
}
```

---

## Workflow Path

```text
08_Set_Alerts_by_User
    ↓
10_TheHive_Promote_To_Case
    ↓
12_Get_TS
(No Conditional Branching)
```
