# TheHive Agent Observable

## Purpose
Sends an HTTP POST request to TheHive to post the agent ip as an observable for the current alert.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Agent_Observable
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.17.0.1:9000/thehive/api/v1/alert/$thehive_create_alert.body._id/observable
```

**Body:**
```json
{
  "data":"$python_slack_script.message.observables.agent_ip","dataType":"ip"
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
30_TheHive_User_Observable
    ↓ 
31_TheHive_Agent_Observable
    ├── 32_TheHive_Attack_Group_Observable
    └── 33_TheHive_File_Path_Observable
```

---

## Branch Condition → 32_TheHive_Attack_Group_Observable

Left Value:
```text
"$python_slack_script.message.observables.attack_group"
```

Operator:
> does not equal

Right Value:
```text
"other"
```

---

## Branch Condition → 33_TheHive_File_Path_Observable

Left Value:
```text
"$python_slack_script.message.observables.attack_group"
```

Operator:
> equals

Right Value:
```text
"other"
```
