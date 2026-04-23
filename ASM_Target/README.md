# 🖥️ ASM Target VM Configuration (Oracle Cloud)

## 📌 Overview
This virtual machine serves as the **attack surface target** in the ASM cybersecurity project. It hosts vulnerable services (OWASP Juice Shop) and security controls (Nginx, ModSecurity, Wazuh Agent).

---

## 🧱 Basic Information

- **Instance Name:** `Asm_Target`
- **Compartment:** `CS4850_SeniorProject`
- **Region:** `US East (Ashburn)`
- **Availability Domain:** `AD-1`

---

## 💻 Image Configuration

- **Operating System:** Ubuntu 22.04 Minimal (aarch64)
- **Image Build:** `2026.03.31-0`
- **Architecture:** ARM (Ampere)
- **Security Mode:** Confidential Computing Enabled

---

## ⚙️ Compute Shape

- **Shape:** `VM.Standard.A1.Flex`
- **Tier:** Always Free Eligible
- **CPU:** 2 vCPUs
- **Memory:** 12 GB RAM
- **Network Bandwidth:** ~2 Gbps

---

# 🌐 ASM Target VM Networking Configuration (Oracle Cloud)

## 📌 Overview
This section defines the **network connectivity, IP addressing, and access controls** for the ASM Target VM. The configuration enables both **public access (for testing/attacks)** and **private communication (for internal security tools)**.

---

## 🔌 Primary VNIC Configuration

- **VNIC Name:** `ASM_Target`
- **Virtual Cloud Network (VCN):** Create a VCN before proceeding & give it a name
- **VCN Compartment:** Create a compartment
- **Subnet:** Create a public subnet

👉 The VM is deployed in a **public subnet**, allowing internet-facing services.

---

## 🧠 Network Design Purpose

- Allow **external attackers / scanners** to reach the target (Juice Shop)
- Enable **Cloudflare + DNS routing**
- Maintain **internal communication** with:
  - Wazuh Manager
  - ASM Manager VM
  - Shuffle / SIEM components

---

## 🔒 Private IPv4 Configuration

- **Assignment Type:** Automatically Assign Private IPv4 Address

## 🔒 Public IPv4 Configuration

- **Assignment Type:** Automatically Assign Public IPv4 Address

## Create Instance

- All Configurations have been made, now hit Create!

## 🌐 Intended Role in Architecture

```text
ASM Target VM
   ├── OWASP Juice Shop (Docker) → Vulnerable Web App
   ├── Patched Juice Shop (Docker) → Secure Version
   ├── Nginx → Reverse Proxy (Ports 80/443)
   ├── ModSecurity → Web Application Firewall (WAF)
   ├── Wazuh Agent → Endpoint Monitoring

# 🧱 ASM Target VM Package Installation Breakdown

## 🧾 Raw Commands (for reproducibility)

```bash
apt install -y software-properties-common
apt install -y xfce4 xfce4-goodies
apt install -y ssl-cert
apt install -y xrdp
apt install -y dbus-x11 xorg xorgxrdp policykit-1 network-manager
apt install -y fonts-dejavu fonts-liberation adwaita-icon-theme gnome-icon-theme
apt install -y xfce4-clipman thunar-archive-plugin file-roller gvfs gvfs-backends
apt install -y build-essential git curl wget unzip zip tmux htop tree rsync
apt install -y python3 python3-pip python3-venv
apt install -y net-tools iputils-ping dnsutils strace lsof
apt install -y chrony
apt install -y nano
apt install -y firefox
apt install -y remmina
apt install -y netcat-openbsd
apt install -y golang-go
apt install -y telnet
apt install -y tcpdump
apt install -y certbot
apt install -y nginx
apt install -y python3-certbot-nginx
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt install -y libmodsecurity3 libmodsecurity-dev git build-essential
apt install -y apt-utils autoconf automake build-essential git libcurl4-openssl-dev libgeoip-dev liblmdb-dev libpcre++-dev libtool libxml2-dev libyajl-dev pkgconf wget zlib1g-dev
apt install -y libpcre2-dev
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

🐳 Containerization & Runtime
```bash
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
```

Used for:

OWASP Juice Shop (vulnerable + patched)
Containerized service deployment

---

## 🐍 Python Environment
```bash
python3
python3-pip
python3-venv
```

Used for:

Python listener (Slack automation endpoint)
System scripting and automation

---

## 🌐 Networking & Diagnostics
```bash
net-tools
iputils-ping
dnsutils
netcat-openbsd
telnet
tcpdump
```

Used for:

DNS resolution
Service validation and debugging
Network traffic inspection

---

## 🔍 Debugging & Monitoring
```bash
strace
lsof
htop
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

Accurate timestamps (Wazuh alert correlation)

---

## 🔐 Firewall & Security
```bash
ssl-cert
```

Used for:

TLS certificate support for Nginx

## 🛡️ Web Server Stack
```bash
nginx
certbot
python3-certbot-nginx
```

Used for:

Reverse proxy (ports 80/443)
TLS termination (HTTPS)
Routing traffic to Docker services

---

## 🛡️ Web Application Firewall (ModSecurity)
```bash
libmodsecurity3
libmodsecurity-dev
libxml2-dev
libyajl-dev
libpcre2-dev
libpcre++-dev
libgeoip-dev
liblmdb-dev
libcurl4-openssl-dev
zlib1g-dev
autoconf
automake
libtool
pkgconf
```

Used for:

Compiling ModSecurity
Integrating WAF with Nginx
Applying OWASP Core Rule Set (CRS)

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
Remote management of the VM

## 🎨 UI / Fonts / Themes
```bash
fonts-dejavu
fonts-liberation
adwaita-icon-theme
gnome-icon-theme
🌍 Browser / User Tools
firefox
remmina
```

Used for:

Accessing web services and dashboards
RDP access into ASM Manager VM

## ⚙️ Programming / Tooling
```bash
golang-go
```

Used for:

Supporting tools (optional utilities)

## 🧰 Utilities
```bash
libxml2-utils
```

Used for:

XML parsing / configuration handling
