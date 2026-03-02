# Slack Cases Channel

## Purpose
Posts alerts to the SOC Cases Slack channel with optional threading support.

---

## Node Type
`Slack Node` <p><img src="../../doc/images/Slack_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
SP-108-RedASM_Cases
```

**Authentication:**
```text
OAuth2 (chat:write, channels:read)
```

**Action:**
```text
Chat postmessage
```

**Body:**
```text
{{$slack_case_triage_links.message}}
```

**Headers:**
```text
None
```

---

## Workflow Path

```text
14_Slack_Case_Triage_Links
    ↓
15_SP-108-RedASM_Cases
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

## Branch Condition → 17_Set_Thread_TS_Alerts

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
