# Update Slack Threads Timestamp Cache

## Purpose
Update stored data cache for a Slack thread timestamp following the creation of a Slack case or alert.

---

## Node Type
`Set Cache Value` <p><img src="../../doc/images/Set_Cache_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Set_Thread_TS_Updates
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
slack_threading_cases
```

---

## Workflow Path (No Conditional Branching)

```text
20_Normalize_Slack_Thread_TS
    ↓
21_Set_Thread_TS_Updates.md
    ↓
22_TheHive_Query_Alert
```
