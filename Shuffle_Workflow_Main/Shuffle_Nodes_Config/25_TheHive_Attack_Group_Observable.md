# TheHive Attack Group Observable

## Purpose
Sends an HTTP POST request to TheHive to post the attack group as an observable for the current alert.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Attack_Group_Observable
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
  "data":"$python_slack_script.message.observables.attack_group","dataType":"other"
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
24_TheHive_Agent_Observable
    ↓ 
25_TheHive_Attack_Group_Observable
    ├── 26_TheHive_File_Path_Observable
    └── 27_Shuffle_Buffer_3
```

---

## Branch Condition → 26_TheHive_File_Path_Observable

Left Value:
```text
$python_slack_script.message.observables.file_path
```

Operator:
> contains_any_of

Right Value:
```text
/
```

---

## Branch Condition → 27_Shuffle_Buffer_3

Left Value:
```text
"$python_slack_script.message.observables.file_path"
```

Operator:
> ! contains_any_of

Right Value:
```text
/
```
