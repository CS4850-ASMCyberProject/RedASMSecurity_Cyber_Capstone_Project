# Shuffle Buffer

## Purpose
Dummy node used to pass `Set_Alerts_by_IP` when IP is `None`.

---

## Node Type
`Repeat back to me`

---

## Setup

**Name:**
```text
Shuffle_Buffer
```

**Action:**
```text
Repeat back to me
```

**Call:**
```text
Nothing
```

---

## Workflow Path

```text
06_Set_Alerts_by_IP
    ↓
07_Shuffle_Buffer
    ├── 08_Set_Alerts_by_User
    └── 09_Shuffle_Buffer_2
```

---

## Branch Condition → 08_Set_Alerts_by_User

Left Value:
```text
$python_slack_script.message.observables.source_user
```

Operator:
> does not equal

Right Value:
```text
None
```

---

## Branch Condition → 09_Shuffle_Buffer_2

Left Value:
```text
$python_slack_script.message.observables.source_user
```

Operator:
> equals

Right Value:
```text
None
```
