# 01_Get_Set_Thread_TS

## Purpose
Gets stored data cache for each Slack thread set.

---

## Node Type
`Get Cache Value`

---

## Setup

**Name:**  
```text
Get_Set_Thread_TS
```

**Action:**  
```text
Get Cache Value
```

**Key:**
```text
slack_thread_$exec.all_fields.agent.id:$exec.rule_id
```

**Category:**  
```text
slack_threading
```

---

## Workflow Path

```text
00_Wazuh_Webhook
    ↓
01_Get_Set_Thread_TS
    ↓
02_Get_Alerts_by_IP
(No Branch Conditional)
```
