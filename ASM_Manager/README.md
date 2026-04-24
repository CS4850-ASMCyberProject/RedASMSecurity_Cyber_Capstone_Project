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
                            ASM Manager VM
                                   │
               ┌───────────────────┴───────────────────┐
               │                                       │
               ▼                                       │
      Wazuh Manager (SIEM)                             │
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
---

# 🧱 ASM_Manager Complete VM Package Installation Breakdown

## 🧾 Raw Commands (for reproducibility)

```bash
apt install -y docker.io git rsync curl
apt install -y nano
apt install -y software-properties-common build-essential git curl wget unzip zip tmux htop tree rsync python3 python3-pip python3-venv python3-tk net-tools iputils-ping dnsutils strace lsof chrony nano netcat-openbsd socat sysstat xfce4 xfce4-goodies xrdp dbus-x11 xorg xorgxrdp policykit-1 network-manager fonts-dejavu fonts-liberation adwaita-icon-theme gnome-icon-theme xfce4-clipman thunar-archive-plugin file-roller gvfs gvfs-backends nfs-common iptables-persistent
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt install -y firefox
apt install -y wazuh-indexer wazuh-manager wazuh-dashboard filebeat
apt install -y libxml2-utils
apt install -y wazuh-manager
apt install -y wazuh-indexer wazuh-dashboard
apt install -y mariadb-server mariadb-client
apt install -y golang-go
apt install -y ffuf
apt install -y jq
apt install -y dnsmasq
apt install -y cron
```

---

## 🧠 Categorized Breakdown

## 🔧 Core System & Development
```bash
software-properties-common
build-essential
git
curl
wget
nano
rsync
unzip, zip
tmux, tree
```

Used for:

Compiling (e.g., ModSecurity)
Repository management
System configuration

---

## 🐳 Containerization & Runtime
```bash
docker.io
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
```

Used for:

Shuffle
TheHive
Container orchestration

--- 

## 🐍 Python Environment
```bash
python3
python3-pip
python3-venv
python3-tk
```

Used for:

ASM scanning scripts
Python listener (Slack automation)
API services

---

## 🌐 Networking & Diagnostics
```bash
net-tools
iputils-ping
dnsutils
netcat-openbsd
socat
dnsmasq
```

Used for:

DNS resolution
Internal domain mapping
Service validation and debugging

---

## 🔍 Debugging & Monitoring
```bash
strace
lsof
htop
sysstat
```

Used for:

Process tracing
Performance monitoring
Debugging runtime issues

---

## ⏱️ Time & System Sync
```bash
chrony
```

Critical for:

Accurate timestamps (SIEM correlation)

---

## 🔐 Firewall & Security
```bash
iptables-persistent
```

Used for:

Persistent firewall rules
Automated blocking via Python listener

---

## 📡 File Systems / Services
```bash
nfs-common
gvfs, gvfs-backends
```

Enables:

File mounting
GUI file access

---

## 🖥️ GUI / Desktop Environment
```bash
xfce4
xfce4-goodies
xfce4-clipman
thunar-archive-plugin
file-roller
```

Provides:

Lightweight desktop interface

---

## 🖥️ Remote Desktop (RDP)
```bash
xrdp
xorg
xorgxrdp
dbus-x11
policykit-1
network-manager
```

Enables:

Remote GUI access via RDP

---

# ⚙️ XRDP Session Configuration (.xsession)

To properly initialize the XFCE desktop environment over XRDP, a .xsession file must be created in the user's home directory.

## 📁 File Location
```bash
/home/<your-user>/.xsession
```

## 📄 Configuration
```bash
xfce-4-session
```

🧠 Purpose
Ensures XFCE starts correctly when connecting via XRDP
Initializes required environment variables for GUI session stability
Prevents common XRDP issues such as:
blank screen after login
immediate session disconnect
missing desktop environment

Enables:

Remote GUI access via RDP  
Remote management of the VM

---

## 🎨 UI / Fonts / Themes
```bash
fonts-dejavu
fonts-liberation
adwaita-icon-theme
gnome-icon-theme
🌍 Browser / User Tools
firefox
```

Used for:

Accessing dashboards (Wazuh, Grafana, etc.)

---

## 🛡️ SIEM / Security Stack (Wazuh)
```bash
wazuh-manager
wazuh-indexer
wazuh-dashboard
filebeat
```

Core functionality:

Log ingestion
Indexing
Visualization

---

## 🗄️ Database Layer
```bash
mariadb-server
mariadb-client
```

Used for:

ASM scanning data storage

---

## ⚙️ Programming / Tooling
```bash
golang-go
```

Used for:

Tools like ffuf

---

## 🔎 Security / Scanning Tools
```bash
ffuf
```

Used for:

Directory fuzzing
Endpoint discovery

---

## 📊 Data Processing
```bash
jq
```

Used for:

Parsing JSON outputs (httpx, nuclei, etc.)

---

## 🧰 Utilities
```bash
libxml2-utils
```

Used for:

XML parsing / configuration handling

---

## ⏲️ Automation
```bash
cron
```

Used for:

Scheduled ASM scans
