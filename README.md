# ASM_Manager SOC Workflow  
## Threat Detection & Response with Wazuh, Shuffle, Slack, TheHive & GitHub

**Branch:** `llado_shuffle_slack`  
**Author:** Adam Llado  

---

<p align="center">
  <img src="docs/images/Infinity_Lock.png" width="300">
</p>

## 📌 Overview

The `llado_shuffle_slack` branch implements a fully automated, open-source SOC workflow integrating:

- **Wazuh** – SIEM & threat detection  
- **Shuffle** – SOAR automation engine  
- **Slack** – Real-time analyst alerting  
- **TheHive** – Case management & incident tracking  
- **GitHub (Private Repo)** – Cyber event archival  

### 🎯 Objectives

This workflow is designed to:

- Detect security alerts from monitored endpoints  
- Automatically trigger response playbooks via Shuffle  
- Enrich and correlate alerts in real time  
- Notify analysts with contextual Slack alerts  
- Promote high-risk alerts into formal SOC cases  
- Archive full event JSON for forensic tracking  

The system leverages intelligent alert correlation, cached enrichment logic, and conditional branching to create a production-ready SOC automation pipeline suitable for professional environments.

---

## 🏗️ High-Level Architecture Flow

1. **Wazuh Agent (Target VM)** detects suspicious activity.  
2. **Wazuh Manager** processes the alert.  
3. Alert is forwarded via **Wazuh Webhook** to Shuffle.  
4. **Shuffle SOAR workflow**:
   - Enriches alert data  
   - Correlates similar events  
   - Determines threading vs. case promotion  
   - Sends alerts to Slack  
   - Creates/updates alerts or cases in TheHive  
   - Archives full JSON to GitHub  
5. **SOC Analysts investigate and respond.**

---

# 🔄 Alert Workflow Breakdown

---

## 1️⃣ Detection – Wazuh (SIEM Layer)

### 📂 Monitored Sources

- Endpoint logs  
- Syslog  
- Authentication logs  
- ASM project directory (File Integrity Monitoring)  
- Custom monitored directories  

### 🚨 Example Triggers

- SSH brute force attempts  
- Privilege escalation activity  
- Suspicious process execution  
- File tampering events  

### 📡 Alert Flow

When a rule triggers:

1. The Wazuh Agent sends data to the Wazuh Manager.  
2. The Wazuh Manager processes and stores the alert.  
3. A webhook forwards the alert to Shuffle for automation.

---

## 2️⃣ Automation – Shuffle (SOAR Engine)

Shuffle acts as the orchestration engine where all enrichment and decision logic occurs.

### 🔗 Webhook Trigger

A Wazuh webhook acts as the entry point for alert automation.

---

## 🧠 Core Enrichment Logic

A custom Python script (**"Main Slack SOC Enrichment"**) builds a structured alert payload containing:

### 🔎 Key Observables

- `source_ip`
- `user`
- `attack_group`
- `file_path`
- `severity`
- `threading` (Boolean)
- `promote_to_case` (Boolean)
- `thread_ts`
- `last_seen`
- `promotescore`
- Additional metadata fields

### 🧩 Enrichment Decisions

The logic determines:

- Whether to thread the alert in Slack  
- Whether to promote it to a SOC case  
- Which Slack channel to post to  
- Whether to create/update in TheHive  

---

## 🗂️ Cached Nodes (Correlation Engine)

Shuffle uses cache nodes to intelligently correlate alerts.

| Cache Node | Purpose |
|------------|----------|
| **Get Slack Threading** | Retrieves thread timestamp for similar alerts within 5 minutes |
| **Set Slack Threading** | Stores thread timestamp by `rule_id` |
| **Get Alerts_by_IP** | Tracks alerts from same IP within 1 hour |
| **Set Alerts_by_IP** | Updates IP-based alert history |
| **Get Alerts_by_User** | Tracks alerts by username within 1 hour |
| **Set Alerts_by_User** | Updates user-based alert history |

This enables frequency-based scoring and intelligent case promotion.

---

## 🔀 Directed Arrow Conditionals

Conditional workflow routing determines:

- Thread vs. new Slack parent message  
- Alert vs. Case channel  
- TheHive alert vs. TheHive case creation  
- Alert update vs. new object creation  

Decision logic is based on:

- `threading`
- `promote_to_case`
- Correlation score
- Cached alert history

---

## 3️⃣ Notification – Slack

Two Slack channels are used:

### 🟢 SOC Alerts Channel

- General internet noise  
- Threaded alerts within a 5-minute window  
- Used for baseline monitoring  

### 🔴 SOC Cases Channel

- High-confidence or high-frequency alerts  
- Includes:
  - Triage links  
  - Response guidance  
  - GitHub archive link  
  - TheHive case link  

### 📢 Slack Messages Include

- Severity  
- Hostname  
- IP address  
- Attack type  
- Case promotion status  
- Thread correlation  
- Structured formatting for professional readability  

---

## 4️⃣ Case Management – TheHive

Shuffle integrates with TheHive using chained HTTP nodes.

### 🔧 Capabilities

- Create alert  
- Promote alert to case  
- Add observables  
- Update existing alerts  
- Tag cases  
- Query and update alerts dynamically  

Promotion logic mirrors Slack promotion decisions.

Observables are individually posted via chained nodes to ensure full enrichment inside TheHive.

---

## 5️⃣ Cyber Event Archive – GitHub (Private Repository)

When triggered, Shuffle:

- Posts full JSON event object to a private GitHub repository  
- Archives detailed metadata for forensic and investigative use  
- Provides a secure link accessible only to authorized users  
- Adds a Slack button for easy case access  

This creates a long-term, immutable audit trail of SOC events.

---

# ⚙️ Basic Setup & Configuration

## ✅ Prerequisites

- Wazuh Server  
- Shuffle instance  
- Slack workspace + bot token  
- TheHive instance + API key  
- GitHub account (private repo)  

---

## Step 1 – Configure Wazuh Webhook

```xml
<integration>
  <name>shuffle-webhook</name>
  <hook_url>http://SHUFFLE_URL/api/v1/hooks/...</hook_url>
  <level>5</level>
</integration>
```

---

## Step 2 – Build Shuffle Workflow

- Create webhook trigger  
- Add Python enrichment script  
- Implement cache nodes (IP, User, Threading)  
- Add Slack alert node  
- Duplicate Slack node for Case channel  
- Add conditional branches  
- Add TheHive HTTP nodes:
  - Create alert  
  - Promote to case  
  - Update alert  
  - Add observables  
- Add GitHub archive HTTP node  
- Test with sample payload  

---

## Step 3 – Configure Slack Bot

- Create Slack App  
- Enable Incoming Webhooks  
- Add bot to SOC channels  
- Insert webhook URL into Shuffle  

---

## Step 4 – Configure TheHive

- Generate API key  
- Configure organization  
- Create case template (optional)  
- Insert API key into Shuffle HTTP nodes  

---

## Step 5 – Host Configuration

- Modify `docker-compose.yml` if port conflicts exist  
- Change Shuffle frontend port if needed  
- Adjust Java heap sizes for TheHive  
- Add swap file if running on limited resources  
- Monitor RAM utilization (TheHive is resource-intensive)  

---

# 🔐 Security Considerations

- Store API keys securely  
- Restrict webhook endpoints  
- Use TLS for communications  
- Apply RBAC policies  
- Limit Slack bot permissions  
- Restrict GitHub repository access  

---

# 🧪 Testing & Validation

### Simulate:

- Failed SSH logins  
- File tampering events  
- Custom Wazuh rule triggers  

### Verify:

- Slack alert formatting  
- Threading behavior  
- Case promotion logic  
- TheHive case creation  
- GitHub JSON archive  

---

# 📊 Benefits

- Intelligent alert correlation  
- Automated case escalation  
- Reduced manual triage workload  
- Centralized incident tracking  
- Professional Slack alert presentation  
- Secure forensic archive  
- Scalable open-source SOC framework  

---
