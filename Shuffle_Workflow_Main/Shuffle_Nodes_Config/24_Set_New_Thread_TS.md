# Set New Slack Alert Threads Timestamp Cache

## Purpose
Set stored data cache for a Slack alert thread timestamp following the creation of a Slack alert.

---

## Node Type
`Set Cache Value` <p><img src="../../doc/images/Set_Cache_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Set_New_Thread_TS
```

**Action:**
```text
Set Cache Value
```

**Key:**
```text
slack_thread_$exec.all_fields.agent.id:$exec.rule_id
```

**Value:**
```json
{
"Set_Thread_TS":"$get_set_thread_ts.value.Set_Thread_TS",
"last_seen":"$python_slack_script.message.last_seen",
"corrkey":"$get_set_thread_ts.value.corrkey",
"source_ip":"$python_slack_script.message.observables.source_ip"
}
```

**Category:**
```text
slack_threading
```

---

## Workflow Path (No Conditional Branching)

```text
19_SP-108-RedASM_Cases
    ↓
24_Set_New_Thread_TS
    ↓
25_Update_Corrkey
```
