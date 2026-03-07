# Normalize Slack Thread Timestamps

## Purpose
Python script that determines whether the current alert is an or a case and normalizes the output  
so that the set cache nodes can set the thread timestamp for both the slack alerts channel and cases channel.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Normalize_Slack_Thread_TS
```

**Action:**
```text
Execute Python
```

**Source Code:** [View Normalize_Slack_Thread_TS.py on GitHub](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Main/Python_Scripts/Normalize_Slack_Thread_TS.py)
```text
/Shuffle_Workflow_Main/Python_Scripts/Normalize_Slack_Thread_TS.py
```

---

## Workflow Path (No Conditional Branching)

```text
11_SP-108-RedASM_Alerts | 19_SP-108-RedASM_Cases
    ↓                        ↓
20_Normalize_Slack_Thread_TS
    ├── 21_Set_Thread_TS_Updates
    └── 22_Set_New_Thread_TS
```
---

## Branch Condition → 21_Set_Thread_TS_Updates

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

## Branch Condition → 22_Set_New_Thread_TS

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
