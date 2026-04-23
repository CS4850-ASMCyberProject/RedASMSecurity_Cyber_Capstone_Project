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

## 🌐 Intended Role in Architecture

```text
ASM Target VM
   ├── OWASP Juice Shop (Docker) → Vulnerable Web App
   ├── Patched Juice Shop (Docker) → Secure Version
   ├── Nginx → Reverse Proxy (Ports 80/443)
   ├── ModSecurity → Web Application Firewall (WAF)
   ├── Wazuh Agent → Endpoint Monitoring
