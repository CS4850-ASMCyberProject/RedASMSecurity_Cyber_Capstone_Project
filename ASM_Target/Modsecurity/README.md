# 🛡️ ModSecurity + Nginx + OWASP Juice Shop Setup

## Overview

This document outlines the complete setup process for integrating *ModSecurity (WAF)* with *Nginx* to protect an OWASP Juice Shop application.

---

## ⚙️ 1. Install Dependencies

```bash
sudo apt update
sudo apt install -y git build-essential libpcre2-dev libyajl-dev libssl-dev
