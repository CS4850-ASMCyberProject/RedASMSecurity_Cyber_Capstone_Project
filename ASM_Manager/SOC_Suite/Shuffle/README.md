# 🔀 Shuffle (SOAR) – Quick Setup (ASM Manager VM)

## 📌 Overview

This setup deploys **Shuffle (SOAR)** using a simple **Docker Compose configuration** (no Docker Swarm).

It includes:

- Shuffle Frontend (UI)
- Shuffle Backend (API)
- Orborus (worker/orchestrator)
- OpenSearch (data store)

---

## 📦 Prerequisites

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

---

## 📁 Step 1 – Clone Shuffle

```bash
cd /opt
git clone https://github.com/shuffle/shuffle.git Shuffle
cd Shuffle
```

---

## ⚙️ Step 2 – Configure .env file

Edit the .env file:
```bash
nano .env
```

🔑 Minimum Required Changes:
```bash
FRONTEND_PORT=3001
FRONTEND_PORT_HTTPS=8443
BACKEND_PORT=5001
BACKEND_HOSTNAME=shuffle-backend
OUTER_HOSTNAME=shuffle-backend

DB_LOCATION=./shuffle-database

SHUFFLE_OPENSEARCH_USERNAME=admin
SHUFFLE_OPENSEARCH_PASSWORD=StrongShufflePassword321!
OPENSEARCH_INITIAL_ADMIN_PASSWORD=StrongShufflePassword321!
```
