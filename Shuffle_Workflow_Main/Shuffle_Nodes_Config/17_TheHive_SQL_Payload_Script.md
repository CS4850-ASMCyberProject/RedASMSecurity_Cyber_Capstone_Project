# TheHive SQL Payload Page

## Purpose
Sends
---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_SQL_Payload_Page
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
$thehive_sql_payload_script.message
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

---

## Workflow Path (No Conditional Branching)

```text
16_TheHive_SQL_Payload_Page
    ↓
17_TheHive_SQL_Payload_Script
    ↓
18_Cyber_Archive_Payload
```
