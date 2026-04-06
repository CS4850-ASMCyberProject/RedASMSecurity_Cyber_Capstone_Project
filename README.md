# 🔍 ASM Scanning Database & Automation Framework  
## Attack Surface Management (ASM) Pipeline with Discovery, Enumeration & Vulnerability Scanning

**Author:** Adam Llado, Kimani Gordon
**Project:** ASM_Scanning_Database_Llado_Upgrades  

---

## 📌 Overview

This project implements a **modular Attack Surface Management (ASM) pipeline** designed to:

- Discover external-facing assets  
- Enumerate subdomains and services  
- Perform content and endpoint discovery  
- Run automated vulnerability scanning  
- Aggregate results into structured datasets  

The system is built using **Python automation scripts + industry-standard security tools** such as:

- **Subfinder** – passive subdomain enumeration  
- **DNSX** – active brute-force subdomain resolution
- **HTTPX** – service probing    
- **Nuclei** – vulnerability scanning
- **FFUF** – content discovery

---

## 🎯 Objectives

This framework is designed to:

- Automate external attack surface discovery  
- Identify exposed services and endpoints  
- Detect vulnerabilities across discovered assets  
- Normalize and store results for analysis  
- Enable repeatable scanning workflows  

---

## 🏗️ High-Level Architecture

### 🔄 Workflow Pipeline

1. **Discovery Phase**
   - Passive subdomain enumeration (**Subfinder**)  
   - Active brute-force enumeration (**DNSX**)  

2. **Validation Phase**
   - HTTP probing (**HTTPX**)  
   - Live host filtering  

3. **Vulnerability Scanning**
   - **Nuclei** template-based scanning  
   - CVE & misconfiguration detection

4. **Enumeration Phase**
   - Directory and endpoint discovery (**FFUF**)  
   - Path enumeration  

5. **Data Processing**
   - Python scripts aggregate results  
   - Output stored in structured files  

---

## 📂 Project Structure

