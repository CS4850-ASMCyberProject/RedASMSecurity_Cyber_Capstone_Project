# Set Alerts by IP Cache

## Purpose
Set stored data cache of a list holding timestamps and user entries for a specified IP.

---

## Node Type
`Set Cache Value` <p><img src="../../doc/images/Set_Cache_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Set_Alerts_by_IP
```

**Action:**
```text
Set Cache Value
```

**Key:**
```text
alerts_by_ip_$python_slack_script.message.observables.source_ip
```

**Value:**
```text
$python_slack_script.message.alerts_by_ip
```

**Category:**
```text
alerts_by_ip
```

---

## Workflow Path

```text
05_Python_Slack_Script
    ↓
06_Set_Alerts_by_IP
    ├── 07_Shuffle_Buffer
    └── 08_Set_Alerts_by_User
```

---

## Branch Condition → 07_Shuffle_Buffer

Left Value:
```text
"$python_slack_script.message.observables.source_user"
```

Operator:
> equals

Right Value:
```text
"None"
```

---

## Branch Condition → 08_Set_Alerts_by_User

Left Value:
```text
"$python_slack_script.message.observables.source_user"
```

Operator:
> does not equal

Right Value:
```text
"None"
```
