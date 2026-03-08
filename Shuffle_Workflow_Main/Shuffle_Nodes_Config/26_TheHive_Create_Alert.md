# TheHive Create Alert

## Purpose
Sends an HTTP POST request to TheHive to create a new alert.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Create_Alert
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.17.0.1:9000/thehive/api/v1/alert
```

**Body:**
```json
{
  "title": "$python_slack_script.message.text",
  "description": "$python_slack_script.message.description",
  "source_ip": "$python_slack_script.message.observables.source_ip",
  "type": "$python_slack_script.message.observables.attack_group",
  "source": "Wazuh",
  "sourceRef": "wazuh-{$update_corrkey.message.corrkey}",
  "tags": [
    "$update_corrkey.message.corrkey"
  ]
} 
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

---

## Workflow Path

```text
25_Update_Corrkey
    ↓ 
26_TheHive_Create_Alert
    ├── 27_Set_TheHive_IP_Observable
    └── 28_Set_TheHive_User_Observable
```

---

## Branch Condition → 27_TheHive_IP_Observable

Left Value:
```text
"$update_corrkey.message.observables.source_ip"
```

Operator:
> does not equals

Right Value:
```text
"None"
```

---

## Branch Condition → 28_TheHive_User_Observable

Left Value:
```text
"$update_corrkey.message.observables.source_ip"
```

Operator:
> equals

Right Value:
```text
"None"
```
