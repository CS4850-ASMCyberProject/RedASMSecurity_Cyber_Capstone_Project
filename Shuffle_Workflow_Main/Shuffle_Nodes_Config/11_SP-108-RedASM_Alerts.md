# Slack Alerts Channel

## Purpose
Posts alerts to the SOC Alerts Slack channel with optional threading support.

---

## Node Type
`Slack Node` <p><img src="../../doc/images/Slack_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
SP-108-RedASM_Alerts
```

**Authentication:**
```text
OAuth2 (chat:write, channels:read)
```

**Body:**
```text
{{$python_slack_script.message}}
```

**Headers:**
```text
None
```

---

## Workflow Path

```text
08_Set_Alerts_by_User | 09_Shuffle_Buffer_2
    ↓                       ↓
11_SP-108-RedASM_Alerts
    ├── 16_Set_Thread_TS_Cases
    └── 17_Set_Thread_TS_Alerts
```

---

## Branch Condition → 16_Set_Thread_TS_Cases

Left Value:
```text
$python_slack_script.message.threading
```

Operator:
> equals

Right Value:
```text
true
```

---

## Branch Condition → 19_Set_Thread_TS_Alerts

Left Value:
```text
$python_slack_script.message.threading
```

Operator:
> equals

Right Value:
```text
false
```
