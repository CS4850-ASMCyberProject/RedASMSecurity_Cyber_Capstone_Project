# 🖥️ ASM Manager VM Configuration (Oracle Cloud)

## 📌 Overview
This virtual machine serves as the *defensive management bunker* in the ASM cybersecurity project. It is a mini security operations center (SOC) & database suite (My SQL), tracking the attack surface (ASM scanning script),  responding to and investigating threats (Shuffle, Wazuh, TheHive), and storing vulnerabilities to preempt defensive prevention.

---

## 🧱 Basic Information

- *Instance Name:* ASM_Manager
- *Compartment:* CS4850_SeniorProject
- *Region:* US East (Ashburn)
- *Availability Domain:* AD-1

---

## 💻 Image Configuration

- *Operating System:* Ubuntu 22.04 Minimal (aarch64)
- *Image Build:* 2026.03.31-0
- *Architecture:* ARM (Ampere)
- *Security Mode:* Confidential Computing Enabled

---

## ⚙️ Compute Shape

- *Shape:* VM.Standard.A1.Flex
- *Tier:* Always Free Eligible
- *CPU:* 2 vCPUs
- *Memory:* 12 GB RAM
- *Network Bandwidth:* ~2 Gbps

---

# 🌐 ASM Manager VM Networking Configuration (Oracle Cloud)

## 📌 Overview
This section defines the *network connectivity, IP addressing, and access controls* for the ASM Manager VM. The configuration enables only *private communication (for internal security tools)* to enhance security.

---

## 🔌 Primary VNIC Configuration

- *VNIC Name:* ASM_Manager
- *Virtual Cloud Network (VCN):* Create a VCN before proceeding & give it a name
- *VCN Compartment:* Create a compartment
- *Subnet:* Create a private subnet

👉 The VM is deployed in a *private subnet*, ensuring that the security suite is hardened and secure to outside threats.

---

## 🧠 Network Design Purpose

- Restrict direct public access to the management infrastructure
- Host core security and orchestration services:
  - Wazuh Manager
  - Shuffle (SOAR)
  - TheHive (Case Management)
  - ASM_Scanning Script (24 Hour Scans)
  - MySQL Database (ASM Scanning Data)
  - Python Server (Automate Slack buttons)
  - Grafana (Database Visualization)
- Maintain secure internal communication with:
  - ASM Target VM (Wazuh Agent, logs, events)
  - Supporting backend services (databases, pipelines)

---

## 🔒 Access Model

- *No public IP exposure*
- Accessible only through:
  - ASM Target VM (Bastion Host)
- SSH & RDP flow:

```text
Local Machine
   ↓
ASM Target (Public VM / Bastion)
   ↓
ASM Manager (Private VM)
```

---

## 🔒 Private IPv4 Configuration

- *Assignment Type:* Automatically Assign Private IPv4 Address

## Create Instance

- All Configurations have been made, now hit Create!

## 🌐 Intended Role in Architecture

```text
ASM Manager VM
   ├── Wazuh Manager → Centralized Threat Detection & Alert Aggregation
   ├── Shuffle (SOAR) → Automated Incident Response & Workflow Orchestration
   ├── TheHive → Case Management & Incident Tracking
   ├── ASM Scanning Framework → Continuous Attack Surface Discovery
   ├── MySQL Database → Storage of Discovered Assets & Scan Results
   ├── Python Listener Server → Receives Shuffle Webhooks (Slack Actions)
   ├── Grafana → Visualization of ASM Data & Trends
```


## 🔁 Data Flow Architecture

```text
                      Wazuh Manager (ASM Manager VM)
                                   │
               ┌───────────────────┴───────────────────┐
               │                                       │
               ▼                                       ▼
        Shuffle (SOAR)                         ASM Scanning Script
               │                                       │
   ┌────────────────────┬───────────┐                  ▼
   │                    │           │            MySQL Database
   ▼                    ▼           ▼                  │
Slack (Primary)  Python Server   TheHive               ▼
 (Case Mgmt)    (Slack Buttons)  (Cases)     Grafana (Visualization)
                        │
                        ▼
     ASM Target VM (iptables + Nginx block rules)
```
   
