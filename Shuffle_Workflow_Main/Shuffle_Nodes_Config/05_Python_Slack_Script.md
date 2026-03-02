# Python Slack SOC Enrichment

## Purpose
Main Python script for building alert payload, Slack threading, promote score handling, triage links, and enrichment logic.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Main/Python_Scripts/Slack_Soc_Enrichment_Main.py

---

## Setup

**Name:**
```text
Python_Slack_Script
```

**Action:**
```text
Execute Python
```

**Code:**
```text
/Shuffle_Workflow_Main/Python_Scripts/Slack_Soc_Enrichment_Main.py
```

(Optional: Replace with a clickable GitHub link if stored in the repo.)

---

## Workflow Path (Fork & Conditional Branching)

```text
04_Get_Alerts_by_User
    ↓
05_Python_Slack_Script
    ├── 06_Set_Alerts_by_IP
    └── 07_Shuffle_Buffer
```

---

## Branch Conditions

**Branch → 06_Set_Alerts_by_IP**
```text
$python_slack_script.message.observables.source_ip != "None"
```

**Branch → 07_Shuffle_Buffer**
```text
$python_slack_script.message.observables.source_ip == "None"
```
