# ☁️ Cloudflare Setup – ASM Infrastructure

## 🔗 Domain: 
```bash
redasmsecurity.cloud
```

## 📌 Overview

Cloudflare was used to provide:  

🌐 Public DNS management for ASM assets  
🔍 Subdomain mapping for attack surface discovery  
🔒 Secure exposure of internal services via tunnels  
⚡ Simplified access to private infrastructure  
  
This setup connects your:  
  
ASM Manager VM  
ASM Target VM  
SOC tooling (Wazuh, Shuffle, TheHive, Grafana)  

## 🎯 Purpose  

This configuration enables:  

Public-facing subdomains for scanning and testing  
Internal services to be safely exposed without public IPs  
Easy access to SOC tools during development and investigation  
Realistic attack surface simulation  

## 🌐 1. Domain Setup

Purchase domain:
```bash
redasmsecurity.cloud
```

Add it to Cloudflare and update nameservers to:  
```bash
malavika.ns.cloudflare.com  
peter.ns.cloudflare.com
```

## 📡 2. DNS Records (Attack Surface Setup)

Navigate to:  

Cloudflare → DNS → Records  

Create multiple A records for subdomain enumeration:  
```bash
admin.redasmsecurity.cloud
api.redasmsecurity.cloud
dev.redasmsecurity.cloud
files.redasmsecurity.cloud
git.redasmsecurity.cloud
jenkins.redasmsecurity.cloud
project.redasmsecurity.cloud
root.redasmsecurity.cloud
shop.redasmsecurity.cloud
vpn.redasmsecurity.cloud
target.redasmsecurity.cloud
```

Example record:
```bash
Type: A
Name: shop
IP: 129.213.96.223
Proxy: DNS Only
```

## 🧠 Why This Matters

These subdomains simulate:

A realistic enterprise attack surface  
Targets for ASM scanning tools (Subfinder, DNSX, HTTPX, FFUF)  
Multiple entry points for vulnerability discovery  

## 🚇 3. Cloudflare Tunnel (ASM_Manager)
Create Tunnel  

Go to:  
```bash
Cloudflare → Zero Trust → Access → Tunnels  
```
Create tunnel:  
```bash
ASM_Manager
```

Install Connector (on ASM Manager VM)
```bash
sudo apt install cloudflared
```

Login:
```bash
cloudflared tunnel login
```
Create tunnel:
```bash
cloudflared tunnel create ASM_Manager
```

## 🌍 4. Publish Internal Services

Map internal services to public subdomains:  

Subdomain	Internal Service  
```bash
wazuh.redasmsecurity.cloud	https://10.0.0.97  
shuffle.redasmsecurity.cloud	https://10.0.0.97:8443  
slack_blockip.redasmsecurity.cloud	https://10.0.0.97:8443  
thehive.redasmsecurity.cloud	https://10.0.0.97:3443  
grafana.redasmsecurity.cloud	http://10.0.0.97:3000  
```

Example Route Config:
```bash
wazuh.redasmsecurity.cloud → https://10.0.0.97
```

Tunnel Routing Behavior:
```bash
Public Request
    ↓
Cloudflare DNS
    ↓
Cloudflare Tunnel (ASM_Manager)
    ↓
Private Service (10.0.0.97)
```

## 🔐 5. Proxy vs DNS Only
DNS Only (Grey Cloud)

Used for:

ASM scanning targets  
Raw IP resolution  

Example:
```bash
shop.redasmsecurity.cloud → DNS Only
```

Proxied (Orange Cloud)

Used for:

Internal services via tunnel
SOC tooling access

Example:
```bash
wazuh.redasmsecurity.cloud → Proxied
```

## 🧩 6. Tunnel + DNS Integration

Cloudflare automatically creates:

Type: Tunnel  
Name: wazuh / shuffle / thehive / grafana  
Target: ASM_Manager  

This links:

Subdomain → Tunnel → Internal Service


## 🧠 Key Features
🌐 Attack Surface Simulation
Multiple exposed subdomains
Realistic recon targets

## 🔒 Secure Internal Access
No need for public IP exposure
Uses outbound-only connections

## ⚡ Centralized Routing
All services routed through one tunnel
Easy to manage and scale

## 🧪 Development Friendly
Quickly expose services for testing
Works with Slack, Shuffle, Wazuh integrations

## 🔗 Integration in ASM Pipeline

Cloudflare connects:
```bash
Internet
    ↓
Cloudflare DNS
    ↓
ASM Target (public services)
    ↓
ASM Manager Tunnel
    ↓
SOC Tools (Wazuh, Shuffle, TheHive, Grafana)
```

## 🚀 Summary

This Cloudflare setup enables:

Public attack surface simulation via DNS records
Secure exposure of internal SOC infrastructure
Seamless integration between scanning and detection systems
A realistic hybrid red/blue team environment
