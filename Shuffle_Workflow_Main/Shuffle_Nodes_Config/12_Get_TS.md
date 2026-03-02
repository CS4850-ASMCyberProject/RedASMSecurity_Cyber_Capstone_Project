# Get TS (GitHub Cyber Archive Prep)

## Purpose
Python script that defines a GitHub path and alters the original alert payload to post the full event archive to GitHub.

---

## Node Type
`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Get_TS
```

**Action:**
```text
Execute Python
```

**Code:**
```text
/Shuffle_Workflow_Main/Python_Scripts/GitHub_Cyber_Archive.py
```

(Optional: Replace the path above with a clickable GitHub link if stored in the repo.)

---

## Workflow Path

```text
10_Get_TheHive_Promote_to_Case
    ↓
12_Get_TS
    ↓
13_GitHub_Cyber_Event_Archive
(No Conditional Branching)
```
