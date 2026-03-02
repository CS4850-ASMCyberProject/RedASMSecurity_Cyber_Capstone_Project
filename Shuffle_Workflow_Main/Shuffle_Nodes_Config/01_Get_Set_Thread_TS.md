# Get Slack Thread Cache

## Purpose
Gets stored data cache for each Slack thread, holding the Slack thread timsetamp, the correlation key, and last seen.

---

## Node Type
`Get Cache Value` <p><img src="../../doc/images/Get_Cache_Icon.png" width="100" width="400"></p>

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

## Workflow Path (No Conditional Branching)

```text
00_Wazuh_Webhook
    ↓
01_Get_Set_Thread_TS
    ↓
02_Get_Alerts_by_IP
```
