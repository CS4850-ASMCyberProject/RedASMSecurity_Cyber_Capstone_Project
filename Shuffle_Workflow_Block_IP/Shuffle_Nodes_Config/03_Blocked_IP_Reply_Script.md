# Slack Reply Payload



## Purpose

Python Script that constructs the Slack Block IP Reply to tell the user the IP has been blocked or that there is no action needed because the IP was already blocked. 



---



## Node Type

`Execute Python` <p><img src="../../doc/images/Execute_Python_Icon.png" width="100" width="400"></p>



---



## Setup



**Name:**

```text

Blocked_IP_Reply_Slack

```



**Action:**

```text

Execute Python

```



**Code Source:** [View Blocked_IP_Reply_Script.py on GitHub](https://github.com/CS4850-ASMCyberProject/CS4850_Red_ASMCyberProject/blob/Llado_shuffle_slack/Shuffle_Workflow_Block_IP/Python_Scripts/Blocked_IP_Reply_Slack.py)

```text

/Shuffle_Workflow_Block_IP/Python_Scripts/Blocked_IP_Reply_Script.py

```

---



## Workflow Path (No Conditional Branching)



```text

02_HTTP_Block_IP

    ↓

03_Blocked_IP_Reply_Script

    ↓

04_Slack_Blocked_Reply

```
