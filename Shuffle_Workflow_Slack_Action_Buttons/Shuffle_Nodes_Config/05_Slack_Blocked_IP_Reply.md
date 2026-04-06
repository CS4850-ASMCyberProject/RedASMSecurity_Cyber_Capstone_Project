# Slack Blocked IP Reply

## Purpose
Posts the block ip reply that states the ip was successfully blocked or was already blocked and that no action is required. 

---

## Node Type
`Slack Node` <p><img src="../../doc/images/Slack_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
Slack_Blocked_IP_Reply
```

**Authentication:**
```text
OAuth2 (chat:write, channels:read)
```

**Body:**
```text
{{$blocked_ip_reply_slack.message}}
```

**Headers:**
```text
Content-Type=application/json
Accept=application/json
```

---

## Workflow Path

```text
04_Blocked_IP_Reply_Script
    ↓
05_Slack_Blocked_IP_Reply
```
