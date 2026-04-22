# 🛡️ Red ASM Security Cyber Capstone Project  
## Attack Surface Management: The Blueprint to Cyber Attacks & Defensive Strategies  

> **Attack or Defend. Heads or Tails. ASM reveals the bet that will break the bank.**

---

## 🎯 Project Focus

This project demonstrates a full **Attack Surface Management (ASM)** pipeline integrating both offensive (Red Team) and defensive (Blue Team) strategies.

### Core Objectives
- 🔍 **Attack Surface Management (ASM)**  
  Tools that uncover the target scope for which attackers attack & defenders defend  

- 🚨 **Security Detection & Response**  
  Implementation of:
  - **SIEM** (Wazuh)
  - **SOAR** (Shuffle)
  - **Case Management** (TheHive)

- ⚔️ **Red vs Blue Team Simulation**  
  Demonstrating attacker pipelines and defender response workflows  

- 🛡️ **System Hardening**
  - ModSecurity WAF
  - Slack Action Buttons for automated response
  - Secure coding (parameterized queries)

- 💉 **SQL Injection Simulation**
  - Exploitation of vulnerable endpoints in OWASP Juice Shop
  - Detection and mitigation via SOC pipeline

- ☁️ **Cyber-Ready Infrastructure**
  - Public-facing vulnerable system
  - Hidden defensive management environment

---

## 🏗️ Architecture Overview

### 🔴 ASM Target (Vulnerable Environment)
- **Dockerized OWASP Juice Shop**
- **Nginx Reverse Proxy**
- **ModSecurity (WAF)**
- **Wazuh Agent** (log + alert forwarding)

#### Hosted Services:
- `shop.redasmsecurity.cloud`  
  → Vulnerable Juice Shop (protected by ModSecurity + Slack response actions)

- `secure-shop.redasmsecurity.cloud`  
  → Hardened Juice Shop (secure backend using parameterized queries)

---

### 🔵 ASM Manager (Defensive Environment)
- **Wazuh Manager (SIEM)**  
  → Detects threats from incoming logs  

- **Shuffle (SOAR)**  
  → Automates incident response workflows  

- **TheHive (Case Management)**  
  → Central hub for investigation & case tracking  

- **Python Automation Server**
  - Listens for Shuffle responses  
  - Executes automated actions:
    - Block IPs
    - Disable vulnerable endpoints

- **ASM Scanning Engine**
  - Daily automated scans
  - Detects new assets & vulnerabilities  

- **MySQL Database**
  - Stores:
    - Discovered assets
    - Vulnerabilities
    - Hardening results

---

### ⚙️ Supporting Infrastructure

- 🌐 **Domain**
  - `redasmsecurity.cloud`

- 💬 **Slack**
  - Alerts Channel → Low priority threats  
  - Cases Channel → High priority incidents  

- ☁️ **Cloudflare**
  - DNS + subdomain management  
  - Secure tunnel for private services  

- ⏱️ **Crontab**
  - Automates daily ASM scanning  

- 🐳 **Docker**
  - Containerized deployment of:
    - OWASP Juice Shop
    - Shuffle
    - TheHive  

---

## 🧩 Project Structure

```bash
ASM_Manager/
ASM_Target/
Infrastructure/
