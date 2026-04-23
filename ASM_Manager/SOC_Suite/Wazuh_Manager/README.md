# 🛡️ Wazuh Manager Setup (Quick & Dirty)
Ubuntu 22.04 Minimal (ARM64 Friendly)
##📌 Overview

This is a lightweight Wazuh manager setup for:

Ubuntu 22.04 Minimal
ARM64 / AARCH64 compatible
Docker / non-Docker environments
Lab / capstone use (not production hardened)

Perfect for:

🔍 Log ingestion
🚨 Alert generation
🔗 Integration with Shuffle / TheHive

## ⚙️ 1. Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
  curl \
  apt-transport-https \
  unzip \
  wget \
  gnupg
```

## 📥 2. Download Wazuh Install Script
```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
curl -sO https://packages.wazuh.com/4.14/config.yml
```

## 🚀 3. Install Wazuh Manager (Single Node)
```bash
sudo bash wazuh-install.sh --wazuh-server wazuh-1
```

This installs:

🛡️ Wazuh Manager
📦 Filebeat
📊 Indexer connection

## ✅ 4. Verify Installation
```bash
sudo systemctl status wazuh-manager
sudo systemctl status filebeat
```

Check listening ports:
```bash
sudo ss -tulpn | grep -E '1514|1515'
```

Expected:

🔌 1514 → agent communication
🔐 1515 → agent enrollment

## ⚙️ 5. Configure /var/ossec/etc/ossec.conf
```bash
sudo nano /var/ossec/etc/ossec.conf
```

## 🧠 Minimum Required Config - Change log alert, ports, & add Shuffle Integration
```bash
<ossec_config>

  <!-- 🌐 Global Settings -->
  <global>
    <jsonout_output>yes</jsonout_output>
    <alerts_log>yes</alerts_log>
    <logall>no</logall>
    <logall_json>no</logall_json>
    <email_notification>no</email_notification>
  </global>

  <!-- 🚨 Alert Levels -->
  <alerts>
    <log_alert_level>6</log_alert_level>
    <email_alert_level>12</email_alert_level>
  </alerts>

  <!-- 🔌 Agent Communication -->
  <remote>
    <connection>secure</connection>
    <port>1514</port>
    <protocol>tcp</protocol>
    <queue_size>131072</queue_size>
  </remote>

  <!-- 🔐 Agent Enrollment -->
  <auth>
    <disabled>no</disabled>
    <port>1515</port>
    <use_source_ip>no</use_source_ip>
    <purge>yes</purge>
    <use_password>no</use_password>
    <ssl_verify_host>no</ssl_verify_host>
    <ssl_manager_cert>etc/sslmanager.cert</ssl_manager_cert>
    <ssl_manager_key>etc/sslmanager.key</ssl_manager_key>
    <ssl_auto_negotiate>no</ssl_auto_negotiate>
  </auth>

  <!-- 📜 Log Sources -->
  <localfile>
    <log_format>journald</log_format>
    <location>journald</location>
  </localfile>

  <localfile>
    <log_format>syslog</log_format>
    <location>/var/ossec/logs/active-responses.log</location>
  </localfile>

  <localfile>
    <log_format>syslog</log_format>
    <location>/var/log/dpkg.log</location>
  </localfile>

  <!-- 🔗 Shuffle Integration -->
  <integration>
    <name>shuffle</name>
    <hook_url>https://shuffle.redasmsecurity.cloud/api/v1/hooks/webhook_XXXXXXXX</hook_url>
    <level>3</level>
    <alert_format>json</alert_format>
  </integration>

</ossec_config>
```

## 🔧 Ignore Nuclei Noisy Scans

📁 Ignore noisy scan directories:
```bash
<ignore>/srv/asm_project/nuclei-templates</ignore>
```

🧠 Enabled modules:
syscheck
rootcheck
vulnerability detection
syscollector

👉 These are optional but useful for full detection coverage.

## 🔄 6. Restart Wazuh
```bash
sudo systemctl restart wazuh-manager
sudo systemctl restart filebeat
```

## 🧪 7. Test Config Before Restart (IMPORTANT)
```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

This setup gives you:

🛡️ Wazuh Manager running
🔌 Agent communication (1514)
🔐 Agent enrollment (1515)
📜 Log ingestion (journald + syslog)
🚨 JSON alert output
🔗 Shuffle webhook integration
🧠 Capstone Fit

Perfect for your stack:

Wazuh → detects attacks
Shuffle → automates response
TheHive → manages cases
