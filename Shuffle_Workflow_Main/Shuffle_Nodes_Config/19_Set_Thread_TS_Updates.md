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
new_slack_thread_$python_slack_script.message.corrkey
```

**Value:**
```json
{
"Set_Thread_TS":"$get_set_thread_ts.value.Set_Thread_TS",
"last_seen":"$python_slack_script.message.last_seen",
"corrkey":"$get_set_thread_ts.value.corrkey"
}
```

**Category:**
```text
slack_threading_new
```

---

## Workflow Path (No Conditional Branching)

```text
15_SP-108-RedASM_Cases
    ↓
16_Set_New_Thread_TS
    ↓
18_TheHive_Query_Alert
```
