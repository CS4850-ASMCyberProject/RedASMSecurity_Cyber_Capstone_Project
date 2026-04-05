# TheHive Query Alert

## Purpose
Sends an HTTP POST request to TheHive to retrieve the alert with the same thread timestamp of the current alert.

---

## Node Type
`Http Node` <p><img src="../../doc/images/Http_Icon.png" width="100" width="400"></p>

---

## Setup

**Name:**
```text
TheHive_Query_Alert
```

**Action:**
```text
POST
```

**URL:**
```text
http://172.17.0.1:9000/thehive/api/v1/query
```

**Body:**
```json
{
  "query": [
    {
      "_name": "listAlert"
    },
    {
      "_name": "filter",
      "_and": [
        {
          "_or": [
            {
              "_like": {
                "_field": "sourceRef",
                "_value": "wazuh-{$python_slack_script.message.corrkey}"
              }
            }
          ]
        }
      ]
    },
    {
      "_name": "page",
      "from": 0,
      "to": 2
    }
  ]
}
```

**Headers:**
```text
Content-Type: application/json
Authorization: Bearer YOUR_THEHIVE_TOKEN
```

---

## Workflow Path (No Conditional Branching)

```text
23_Set_Thread_TS_Updates
    ↓
24_TheHive_Query_Alert
    ↓
25_TheHive_Update_Alert
```
