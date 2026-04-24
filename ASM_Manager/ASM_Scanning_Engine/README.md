# 🌐 ASM Scanning Engine - Llado_ASM_Scanning_Database_Upgrades

By: Adam Llado, Kimani Gordon, Alec Sundby

## 🔗 Branch Link:
https://github.com/CS4850-ASMCyberProject/RedASMSecurity_Cyber_Capstone_Project/tree/Llado_ASM_Scanning_Database_Upgrades

## 📌 Overview

The ASM Scanning Engine branch implements a fully automated Attack Surface Management (ASM) discovery and analysis pipeline designed to identify, validate, and analyze exposed assets in real time.

This workflow integrates:

🔍 Subfinder – Subdomain discovery  
🌐 DNSX – DNS validation & brute forcing  
🌍 HTTPX – Live service detection & metadata extraction  
🚨 Nuclei – Vulnerability scanning engine  
🔎 FFUF – Path and endpoint discovery  
🐍 Python Engine – Orchestration, parsing, and enrichment logic  
🎯 Purpose  

This system is designed to:

Continuously discover exposed assets and subdomains
Validate live hosts and services
Identify vulnerable endpoints and misconfigurations
Build a structured database of attack surface data
Feed results into downstream SOC systems (Wazuh, Shuffle, TheHive)
Simulate real-world attacker reconnaissance techniques

## 🔄 High-Level Workflow
Subdomain Discovery
Subfinder enumerates subdomains for target domain
DNS Validation
DNSX filters valid/resolvable domains
Optional brute-force expansion
Service Discovery
HTTPX identifies active web services
Extracts metadata (IP, status, tech stack)
Vulnerability Scanning
Nuclei scans endpoints using templates
Detects known vulnerabilities and exposures
Endpoint / Path Discovery
FFUF brute-forces directories and API paths
Identifies hidden or sensitive endpoints
Data Processing Pipeline
Python scripts normalize JSON outputs
Extract IP ↔ domain relationships
Generate structured datasets
Output Storage

Results stored in:
results/ (timestamped runs)
logs/ (execution logs)
latest/ (symlink to most recent scan)

# 🧠 Key Features

## 🔍 Automated Asset Discovery

Continuous subdomain enumeration
Expands attack surface dynamically

## 🌐 Intelligent Service Mapping
Maps domains → IPs → live services
Handles inconsistent tool output formats
⚡ Rate-Limited Scanning Engine
Tuned for low-resource environments
Prevents VM overload (critical for your manager VM)

## 🧩 Modular Scan Pipeline
Each stage (discovery → validation → scanning) is independent
Easy to extend or replace tools

## 🧠 JSON Normalization Engine
Handles varying tool outputs (HTTPX versions, DNSX formats)
Ensures consistent downstream processing

## 📊 Structured Data Output

Produces clean datasets for:
Wazuh ingestion
Shuffle automation
Database storage

## 🧩 ASM Workflow Components
Discovery: Subfinder
Validation: DNSX
Service Detection: HTTPX
Vulnerability Scanning: Nuclei
Path Discovery: FFUF
Processing Engine: Python scripts
Storage: Local filesystem (results + logs)

## ⚙️ What This Branch Demonstrates

This branch represents the offensive reconnaissance layer of the ASM project:

Real-world attacker discovery techniques
Automated attack surface mapping
Vulnerability identification at scale
Data pipeline feeding defensive systems

## 📁 Project Structure (Simplified)
```bash
ASM_Scanning_Database_Llado_Upgrades/
│
├── scanner.py
├── terminal_run.py
├── vulnerability_scan.py
├── url_paths_scan.py
├── frontend_paths_scan.py
│
├── results/
│   └── <timestamped_scan_runs>/
│
├── logs/
│   └── scan.log
│
├── latest -> symlink to most recent scan
│
├── discovery.txt
├── verified_discovery.txt
├── httpx.json
├── nuclei.json
```

## 🧠 Notes
Designed to run on the ASM Manager VM
Targets services hosted on the ASM Target VM
Integrates directly with:
Wazuh (alert generation)
Shuffle (automation workflows)
Uses /etc/hosts manipulation for internal resolution during scanning

## 🚀 Summary

The ASM Scanning Engine showcases a fully automated reconnaissance pipeline that:

Discovers attack surface assets
Validates and maps live infrastructure
Identifies vulnerabilities and exposed endpoints
Structures data for downstream SOC processing
Simulates real-world attacker behavior

All while maintaining a modular, scalable, and production-style ASM workflow that feeds directly into your SOC automation pipeline.
