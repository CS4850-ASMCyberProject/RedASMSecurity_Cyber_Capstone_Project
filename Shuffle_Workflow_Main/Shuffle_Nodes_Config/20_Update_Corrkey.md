# Update Alert Payload Corrkey

## Purpose
Update the correlation key (Corrkey) of the alert payload with the slack thread timestamp.  
Do this so that alerts in TheHive don't explode and threading is possible.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Update_Corrkey
```

**Action:**
```text
Execute Python
```

**Code Source:** [View Update_Corrkey.py on GitHub]([https://github.com/CS4850-ASMCyberProjck/Shuff](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Main/Python_Scripts/Update_Corrkey.py))
```text
/Shuffle_Workflow_Main/Python_Scripts/Update_Corrkey.py
```
---

## Workflow Path (No Conditional Branching)

```text
19_Set_New_Thread_TS
    ↓
20_Update_Corrkey
    ↓
21_TheHive_Create_Alert
```
