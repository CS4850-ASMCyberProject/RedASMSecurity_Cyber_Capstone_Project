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
18_Slack_Case_Triage_Links
    ↓
19_SP-108-RedASM_Cases
    ↓
20_Normalize_Slack_Thread_TS
```
