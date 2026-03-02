# START: Add Wazuh Webhook to Shuffle Workflow

## Node Type
`Webhook` <p><img src="../../doc/images/Wazuh_Webhook_Icon.png" width="100" width="100"></p>

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

## Workflow Path

```text
00_Wazuh_Webhook
    ↓
01_Get_Set_Thread_TS
(No Branch Conditional)
```
