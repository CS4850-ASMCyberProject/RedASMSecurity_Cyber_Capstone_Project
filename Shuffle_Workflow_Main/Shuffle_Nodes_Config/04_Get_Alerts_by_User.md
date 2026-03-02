# Get Alerts by User Cache

## Purpose
Gets stored data cache of a list holding timestamps and IP entries for a specified user.

---

## Node Type
`Get Cache Value` <p><img src="../../doc/images/Get_Cache_Icon.png" width="400"></p>

---

## Setup

**Name:**
```text
Get_Alerts_by_User
```

**Action:**
```text
Get Cache Value
```

**Key:**
```text
alerts_by_user_$normalize_user.message.source_user
```

**Category:**
```text
alerts_by_user
```

---

## Workflow Path

```text
03_Normalize_User
    ↓
04_Get_Alerts_by_User
    ↓
05_Python_Slack_Script
(No Branch Conditional)
```
