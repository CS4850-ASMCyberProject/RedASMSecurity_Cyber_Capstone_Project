# TheHive Case History Page

## Purpose
Sends an HTTP POST request to TheHive to append a page to the current case showing the scoring of the case and why it was promoted to a case.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Scoring_Page
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.17.0.1:9000/thehive/api/v1/case/$thehive_promote_to_case.body._id/page
```

**Body:**
```text
$thehive_scoring_page_script.message
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

---

## Workflow Path (No Conditional Branching)

```text
14_TheHive_Scoring_Page_Script
    ↓
15_TheHive_Scoring_Page
    ↓
16_Cyber_Archive_Payload
```
