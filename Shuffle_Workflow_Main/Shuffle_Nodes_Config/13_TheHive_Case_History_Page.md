# TheHive Case History Page

## Purpose
Sends an HTTP POST request to TheHive to append a page to the current case showing related alerts by source_ip and source_user.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Case_History_Page
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
$thehive_case_history_page_script.message
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

---

## Workflow Path (No Conditional Branching)

```text
12_TheHive_Case_History_Page_Script
    ↓
13_TheHive_Case_History_Page
    ↓
14_TheHive_Scoring_Page_Script
```
