# 🌐 ASM Web Interface – austin-website

By: Austin Abeln

## 🔗 Branch Link:
https://github.com/CS4850-ASMCyberProject/RedASMSecurity_Cyber_Capstone_Project/tree/austin-website

## 📌 Overview

The austin-website branch implements a web-based interface for the Red ASM Security project, providing a centralized dashboard to visualize and interact with the system’s attack surface, scan data, and security insights.

This interface acts as the presentation layer of the ASM pipeline, connecting backend data with a user-friendly frontend.  

This workflow integrates:

🌐 React Frontend – User interface and visualization layer  
⚙️ FastAPI Backend – API service for data retrieval and logic  
🗄️ MySQL / MariaDB – ASM database storage  
🔍 ASM Scanning Engine – Data source for assets, paths, and vulnerabilities  

## 🎯 Purpose

This system is designed to:

Provide a centralized dashboard for ASM data  
Visualize discovered assets and attack surface  
Display URL paths and endpoints found during scanning  
Surface vulnerability data in a readable format  
Allow users to interact with and explore scan results  
Bridge backend security data with frontend usability  

## 🔄 High-Level Workflow
```bash
ASM Scanner
    ↓
Database (Assets, Paths, Vulnerabilities)
    ↓
FastAPI Backend
    ↓
React Frontend
    ↓
User Dashboard / Visualization
```

## 🧠 Key Features
📊 Attack Surface Visualization
Displays discovered subdomains and services
Shows asset metadata (IP, status, tech stack)

## 🌐 URL Path Exploration
Lists endpoints discovered via FFUF
Provides metadata such as status codes and response size

## 🚨 Vulnerability Display
Surfaces vulnerabilities detected by Nuclei
Includes severity, type, and extracted results

## ⚙️ API-Driven Architecture
Frontend communicates with FastAPI backend
Backend queries database and formats responses

## 🧩 Modular Design
Clean separation between:
frontend (React)
backend (FastAPI)
data layer (MySQL)

## 🧩 Web Interface Components
Frontend: React (dashboard UI)
Backend: FastAPI (API endpoints)
Database: MySQL / MariaDB (ASM data)
Data Sources: ASM Scanning Engine outputs

## ⚙️ What This Branch Demonstrates

This branch represents the user-facing layer of the ASM project:

Visualization of attack surface data  
Integration between backend and frontend systems  
Transformation of raw scan data into actionable insights  
Usable interface for analysts and developers  

## 📁 Notes
Designed to run alongside the ASM Manager infrastructure
Pulls data directly from the ASM database
Complements SOC pipeline (Wazuh + Shuffle + TheHive)
Intended for demonstration, analysis, and reporting

## 🚀 Summary

The austin-website branch showcases a web-based interface that:

Visualizes attack surface data
Displays scan results and vulnerabilities
Connects backend systems to a user-friendly dashboard
Enhances usability of the ASM pipeline
