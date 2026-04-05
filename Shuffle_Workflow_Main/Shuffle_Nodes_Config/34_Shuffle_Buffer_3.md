# Shuffle Buffer 3

## Purpose
Dummy node used to pass `TheHive Attack Group Observable` when Attack Group is `other`.

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
32_TheHive_Attack_Group_Observable
    ↓
34_Shuffle_Buffer_3 
```

---

## Workflow Path Completed for New Alerts
