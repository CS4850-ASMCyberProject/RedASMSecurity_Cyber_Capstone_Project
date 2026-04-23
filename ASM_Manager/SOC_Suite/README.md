# 🛡️ SOC Automation Workflow – llado_shuffle_slack

🔗 *Branch Link:*  
https://github.com/CS4850-ASMCyberProject/RedASMSecurity_Cyber_Capstone_Project/tree/Llado_shuffle_slack

---

## 📌 Overview

The llado_shuffle_slack branch implements a fully automated *Security Operations Center (SOC) pipeline* using open-source tools to detect, analyze, and respond to security threats in real time.

This workflow integrates:

- *Wazuh* – SIEM detection engine  
- *Shuffle* – SOAR automation platform  
- *Slack* – Real-time alerting & triage interface  
- *TheHive* – Case management system  
- *GitHub (Private Repo)* – Long-term event archive  

---

## 🎯 Purpose

This system is designed to:

- Automatically ingest and process security alerts  
- Enrich and correlate events using custom logic  
- Notify analysts with structured Slack alerts  
- Promote high-risk alerts into formal SOC cases  
- Enable rapid response via action-driven workflows  
- Archive full event data for forensic tracking  

---

## 🔄 High-Level Workflow

1. *Wazuh Agent (Target VM)* detects suspicious activity  
2. Alert is processed by the *Wazuh Manager*  
3. Alert is sent via webhook to *Shuffle (SOAR)*  
4. Shuffle performs:
   - Alert enrichment (Python logic)
   - Correlation (IP, user, frequency, timing)
   - Conditional decision making (thread vs case)
5. Outputs are sent to:
   - *Slack* → Alerts + case triage
   - *TheHive* → Alert/case creation
   - *GitHub* → Full JSON event archive  
6. Analysts review and respond in real time  

---

## 🧠 Key Features

- *Intelligent Alert Correlation*
  - Groups repeated alerts (IP, user, rule)
  - Reduces alert noise

- *Slack Threading & Case Promotion*
  - Low-risk alerts → threaded messages  
  - High-risk alerts → SOC case channel  

- *Automated Case Management*
  - Create/update alerts in TheHive  
  - Promote alerts to cases dynamically  

- *Python-Based Enrichment Engine*
  - Builds structured alert payloads  
  - Drives decision logic inside Shuffle  

- *Event Archival*
  - Full alert JSON stored in GitHub  
  - Enables long-term forensic analysis  

---

## 🧩 SOC Workflow Components

- *Detection:* Wazuh SIEM  
- *Automation:* Shuffle SOAR  
- *Alerting:* Slack (Alerts + Cases channels)  
- *Case Management:* TheHive  
- *Storage:* GitHub (event archive)  

---

## ⚙️ What This Branch Demonstrates

This branch represents the *core SOC layer* of the ASM project:

- Real-time threat detection and response  
- Automated security orchestration  
- Analyst-friendly alerting workflows  
- Scalable, production-style SOC pipeline  

---

## 📁 Notes

- This workflow runs on the *ASM Manager VM*
- Integrates with the *ASM Target VM (Wazuh Agent)*
- Designed to simulate a *real-world blue team environment*

---

## 🚀 Summary

The llado_shuffle_slack branch showcases a *fully automated SOC pipeline* that:

- Detects threats  
- Correlates and enriches alerts  
- Notifies analysts  
- Automates case management  
- Enables rapid defensive response  

All while maintaining a structured, scalable, and professional security operations workflow.
