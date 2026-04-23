# 🛡️ ModSecurity + Nginx + OWASP Juice Shop Setup

## Overview

This document outlines the complete setup process for integrating *ModSecurity (WAF)* with *Nginx* to protect an OWASP Juice Shop application.

---

## ⚙️ 1. Install Dependencies

```bash
sudo apt update
sudo apt install -y git build-essential libpcre2-dev libyajl-dev libssl-dev
```

## 📦 2. Build ModSecurity (libmodsecurity)

```bash
cd /opt
git clone --depth 1 https://github.com/owasp-modsecurity/ModSecurity
cd ModSecurity

git submodule update --init --recursive
./build.sh
./configure
make
sudo make install
```

## 🔗 3. Register ModSecurity Library

```bash
echo '/usr/local/modsecurity/lib' | sudo tee /etc/ld.so.conf.d/modsecurity.conf
sudo ldconfig
ldconfig -p | grep modsecurity
```

## 🧩 4. Build Nginx ModSecurity Module

```bash
cd /opt
git clone --depth 1 https://github.com/owasp-modsecurity/ModSecurity-nginx.git

wget http://nginx.org/download/nginx-1.18.0.tar.gz
tar zxvf nginx-1.18.0.tar.gz

cd nginx-1.18.0
./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx
make modules

sudo cp objs/ngx_http_modsecurity_module.so /usr/lib/nginx/modules/
```

## 🧠 5. Load Module in Nginx

Edit:
```bash
sudo nano /etc/nginx/nginx.conf
```
Add At the top of the file:
```bash
load_module /usr/lib/nginx/modules/ngx_http_modsecurity_module.so;
```

## 📁 6. Create ModSecurity Config Directory

```bash
sudo mkdir /etc/nginx/modsec
```

## 🧱 7. Install OWASP Core Rule Set (CRS)

```bash
cd /etc/nginx
sudo git clone --depth 1 https://github.com/coreruleset/coreruleset.git modsec-crs

cd modsec-crs
sudo cp crs-setup.conf.example crs-setup.conf
```
## 🔗 8. Create Main ModSecurity Rules File

```bash
sudo nano /etc/nginx/modsec/juice_shop_modsec_main.conf
```
Add:
```bash
# Enable ModSecurity
SecRuleEngine On

# Log everything (important for Wazuh later)
SecAuditEngine RelevantOnly
SecAuditLog /var/log/modsec_audit.log

# Request body access (needed for POST attacks)
SecRequestBodyAccess On

# Include CRS
Include /etc/nginx/modsec-crs/crs-setup.conf
Include /etc/nginx/modsec-crs/rules/*.conf
```

## 🌐 9. Enable ModSecurity in Nginx Site

```bash
sudo nano /etc/nginx/sites-enabled/juice-shop
```
Include in the server {} part of the config under the server name
```bash
modsecurity on;
modsecurity_rules_file /etc/nginx/modsec/juice_shop_modsec_main.conf;
```

## 🚀 10. Test & Reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```
