# HTTP Block SQL

## Purpose
Sends an HTTP POST request to Slack to contain a path using the contain path button.
It sends the request to the docker container gateway 172.18.0.1 which contains the path from sql injection.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Http_Block_SQL
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.18.0.1:8787
```

**Body:**
```text
$slack_source_ip_action_id.message
```

**Headers:**
```text
Content-Type: application/json
```

---

## Workflow Path (No Conditional Branching)

```text
01_Slack_Source_IP_Script
    ↓
03_HTTP_Block_SQL
    ↓
04_Blocked_IP_Reply_Slack
```
