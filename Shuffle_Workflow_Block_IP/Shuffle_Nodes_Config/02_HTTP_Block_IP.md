# HTTP Block IP 

## Purpose
Sends an HTTP POST request to Slack to block an ip using the block IP button. 

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Http_Block_IP
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.19.0.1:8787
```

**Body:**
```text
$slack_source_ip.message
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
02_HTTP_Block_IP
    ↓
03_Blocked_IP_Reply_Slack
```
