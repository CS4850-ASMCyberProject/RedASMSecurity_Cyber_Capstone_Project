# TheHive IP Observable

## Purpose
Sends an HTTP POST request to TheHive to post the source user as an observable for the current alert.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_User_Observable
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
  "data":"$python_slack_script.message.observables.source_user","dataType":"other"
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
22_TheHive_IP_Observable
    ↓ 
23_TheHive_User_Observable
    ├── 24_TheHive_Agent_Observable
    └── 25_TheHive_Attack_Group_Observable
```

---

## Branch Condition → 24_TheHive_Agent_Observable

Left Value:
```text
"$python_slack_script.message.observables.agent_ip"
```

Operator:
> does not equals

Right Value:
```text
"None"
```

---

## Branch Condition → 24_TheHive_Attack_Group_Observable

Left Value:
```text
"$python_slack_script.message.observables.agent_ip"
```

Operator:
> equals

Right Value:
```text
"None"
```
