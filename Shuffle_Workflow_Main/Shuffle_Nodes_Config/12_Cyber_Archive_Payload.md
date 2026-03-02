# Cyber Archive Payload (GitHub Upload Prep)

## Purpose
Python script that defines a GitHub path and alters the original alert payload to post the full event archive to GitHub.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Cyber_Archive_Payload
```

**Action:**
```text
Execute Python
```

**Source Code:** [View GitHub_Cyber_Payload.py on GitHub](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Main/Python_Scripts/GitHub_Cyber_Payload.py))
```text
/Shuffle_Workflow_Main/Python_Scripts/GitHub_Cyber_Archive.py
```

---

## Workflow Path (No Conditional Branching)

```text
10_Get_TheHive_Promote_to_Case
    ↓
12_Cyber_Archive_Payload
    ↓
13_GitHub_Cyber_Event_Archive
```
