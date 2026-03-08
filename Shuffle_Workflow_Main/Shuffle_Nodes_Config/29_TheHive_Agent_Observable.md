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
28_TheHive_User_Observable
    ↓ 
29_TheHive_Agent_Observable
    ├── 30_TheHive_Attack_Group_Observable
    └── 31_TheHive_File_Path_Observable
```

---

## Branch Condition → 30_TheHive_Attack_Group_Observable

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

## Branch Condition → 31_TheHive_File_Path_Observable

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
