# Slack Case Triage Links

## Purpose
Python script that retrieves the GitHub Cyber Event Archive URL and appends it to the alert payload.  
The enriched payload is then posted to the Slack Case card along with additional triage links to assist investigation.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Slack_Case_Triage_Links
```

**Action:**
```text
Execute Python
```

**Source Code:** [View Slack_Case_Triage_Links.py on GitHub](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Main/Python_Scripts/Slack_Case_Triage_Links.py)
```text
/Shuffle_Workflow_Main/Python_Scripts/Slack_Case_Triage_Links.py
```

---

## Workflow Path (No Conditional Branching)

```text
17_GitHub_Cyber_Event_Archive
    ↓
18_Slack_Case_Triage_Links
    ↓
19_SP-108-RedASM_Cases
```
