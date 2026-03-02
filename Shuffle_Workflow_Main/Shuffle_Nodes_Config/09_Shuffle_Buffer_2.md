# Shuffle Buffer 2

## Purpose
Dummy node used to continue workflow when user-based cache updates are skipped.

---

## Node Type
`Repeat back to me` <p><img src="../../doc/images/Repeat_Back_to_Me_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Shuffle_Buffer_2
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
07_Shuffle_Buffer
    ↓
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
