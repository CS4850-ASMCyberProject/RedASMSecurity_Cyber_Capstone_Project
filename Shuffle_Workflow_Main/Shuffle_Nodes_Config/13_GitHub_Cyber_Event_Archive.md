# GitHub Cyber Event Archive

## Purpose
Sends an HTTP PUT request to GitHub to upload the full event archive of a SOC case for investigation and reference.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
GitHub_Cyber_Event_Archive
```

**Action:**
```text
PUT
```

**URL:**
```text
https://api.github.com/repos/CS4850-ASMCyberProject/cyber_event_archive/contents/$cyber_archive_payload.message.path
```

**Headers:**
```text
Authorization: Bearer YOUR_GITHUB_TOKEN
Accept: application/vnd.github+json
Content-Type: application/json
```

**Body:**
```json
{
  "message": "$cyber_archive_payload.message.commit_msg",
  "content": "$cyber_archive_payload.message.github_event",
  "branch": "main"
}
```

---

## Workflow Path (No Conditional Branching)

```text
12_Cyber_Archive_Payload
    ↓
13_GitHub_Cyber_Event_Archive
    ↓
14_Get_TS_Copy
```
