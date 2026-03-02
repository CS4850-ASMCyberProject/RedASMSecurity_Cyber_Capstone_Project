# Set Alerts by User Cache

## Purpose
Set stored data cache of a list holding timestamps and IP entries for a specified user.

---

## Node Type
`Set Cache Value` <p><img src="../../doc/images/Set_Cache_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Set_Alerts_by_User
```

**Action:**
```text
Set Cache Value
```

**Key:**
```text
alerts_by_ip_$python_slack_script.message.observables.source_user
```

**Value:**
```text
$python_slack_script.message.alerts_by_user
```

**Category:**
```text
alerts_by_user
```

---

## Workflow Path

```text
07_Shuffle_Buffer
    ↓
08_Set_Alerts_by_User
    ├── 10_TheHive_Promote_to_Case
    └── 11_SP-108-RedASM_Alerts
```

---

## Branch Condition → 10_TheHive_Promote_to_Case

Left Value:
```text
$python_slack_script.message.promote_to_case
```

Operator:
> equals

Right Value:
```text
true
```

---

## Branch Condition → 11_SP-108-RedASM_Alerts

Left Value:
```text
$python_slack_script.message.promote_to_case
```

Operator:
> equals

Right Value:
```text
false
```
