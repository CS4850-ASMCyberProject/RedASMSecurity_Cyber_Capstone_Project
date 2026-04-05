# Slack Source IP & Action ID Script



## Purpose

Python Script used to retrieve the source_ip and action ID from the Slack Webhook for the block ip & block sql CLI command. 



---



## Node Type

`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>



---



## Setup



**Name:**

```text

Slack_Source_IP_Action_ID

```



**Action:**

```text

Execute Python

```



**Code Source:** [View Slack_Source_IP_Action_ID_Script.py on GitHub](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Block_IP/Python_Scripts/Slack_Source_IP_Action_ID_Script.py)

```text

/Shuffle_Workflow_Block_IP/Python_Scripts/Slack_Source_IP_Script.py

```

---



## Workflow Path

```text
00 Slack_Webhook
    ↓ 
01_Slack_Source_IP_Script
    ├── 02_HTTP_Block_IP
    └── 03_HTTP_Block_SQL
```

---

## Branch Condition → 02_HTTP_Block_IP

Left Value:
```text
"$slack_source_ip_action_id.message.action_id"
```

Operator:
> equals

Right Value:
```text
"block_ip"
```

---

## Branch Condition → 03_HTTP_Block_SQL

Left Value:
```text
"$slack_source_ip_action_id.message.action_id"
```

Operator:
> equals

Right Value:
```text
"block_sql"
```

