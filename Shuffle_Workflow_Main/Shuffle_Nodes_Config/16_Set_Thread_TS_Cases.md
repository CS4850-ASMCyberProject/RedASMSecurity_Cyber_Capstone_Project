# Set Slack Case Threads Timestamp Cache

## Purpose
Set stored data cache of the Slack case thread timestamp following the creation of a Slack case.

---

## Node Type
`Set Cache Value` <p><img src="../../doc/images/Set_Cache_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Set_Thread_TS_Cases
```

**Action:**
```text
Set Cache Value
```

**Key:**
```text
slack_thread_cases_$python_slack_script.message.corrkey
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
slack_threading_cases
```

---

## Workflow Path (No Conditional Branching)

```text
15_SP-108-RedASM_Cases
    ↓
16_Set_Thread_TS_Cases
    ↓
18_TheHive_Query_Alert
```
