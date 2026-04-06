# START: Add Webhook to Shuffle Workflow



## Purpose

The webhook is the entrypoint for alerts stored in the Wazuh Manager. This data is sent via the webhook where Shuffle can start alert automation.



---



## Node Type

`Webhook` <p><img src="../../doc/images/Wazuh_Webhook_Icon.png" width="100" width="400"></p>



---



## Wazuh Configuration



Edit:



```bash

sudo nano /var/ossec/etc/ossec.conf

```



Add inside `<ossec_config>` (last entry):



```xml

<integration>

  <name>shuffle</name>

  <hook_url>YOUR_WEBHOOK_URL</hook_url>

  <level>3</level>

  <alert_format>json</alert_format>

</integration>

```



---



## Workflow Path (No Conditional Branching)



```text

00_Slack_Webhook

    ↓

01_Slack_Source_IP

```
