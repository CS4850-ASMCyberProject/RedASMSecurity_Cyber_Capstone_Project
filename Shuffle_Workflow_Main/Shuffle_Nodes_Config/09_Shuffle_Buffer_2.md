# Shuffle Buffer 2

## Purpose
Dummy node used to continue workflow when user-based cache updates are skipped.

---

## Node Type
`Check Cache Contains` <p><img src="../../doc/images/Check_Cache_Contains_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Shuffle_Buffer
```

**Action:**
```text
Check Cache Contains
```

**Key:**
```text
$get_alerts_by_user.key
```

**Value:**
```text
$exec.all_fields.agent.ip
```

**Append:**
```text
False
```
---

## Workflow Path

```text
06 Set_Alerts_By_IP | 07_Shuffle_Buffer
    ↓                     ↓
09_Shuffle_Buffer_2
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
