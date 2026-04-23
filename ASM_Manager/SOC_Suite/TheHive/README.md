# 🐝 TheHive Docker Setup (Ubuntu 22.04 ARM64 – Docker Compose Only)
## 📌 Overview

This setup follows the official StrangeBee Docker demo environment and is adapted for:

Ubuntu 22.04 Minimal (ARM64)
Docker + Docker Compose (NO swarm)
Testing / lab environment (Red ASM compatible)

## ⚙️ 1. Install Required Dependencies

The official docs require:

Docker Engine
Docker Compose plugin
jq

## ✅ Install everything (Ubuntu 22.04 ARM64)
```bash
sudo apt update
```

Base tools:

```bash
sudo apt install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release \
  git \
  jq
```

# Install Docker (official repo – ARM64 compatible)

```bash
sudo apt install -y docker.io docker-compose
```

# Enable Docker

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

# Allow current user to run docker

```bash
sudo usermod -aG docker $USER
newgrp docker
```

## ✅ Verify Installation

```bash
docker version
docker compose version
docker run hello-world
```

👉 These checks are required by the official docs to confirm Docker is working

## 📥 2. Download TheHive Docker Environment

```bash
git clone https://github.com/StrangeBeeCorp/docker.git
cd docker
```

👉 This is the official Docker repo used by the demo environment

## 📁 3. Navigate to Testing Profile

```bash
cd testing
```

👉 This is the demo / lab environment, not production.

### 🐳 4. REPLACE docker-compose.yml (IMPORTANT)

⚠️ DO NOT use the default compose file

👉 Use this file:

Replace command:
```bash
nano docker-compose.yml
```

📌 Copy & Paste this config into Docker-Compose:
```bash
services:
  cassandra:
    image: "cassandra:${cassandra_image_version}"
    container_name: cassandra
    hostname: cassandra
    restart: unless-stopped
    user: ${UID}:${GID}
    environment:
      - CASSANDRA_CLUSTER_NAME=TheHive
      - CASSANDRA_AUTHENTICATOR=PasswordAuthenticator
      - CASSANDRA_NUM_TOKENS=4
      - HEAP_NEWSIZE=200M
      - MAX_HEAP_SIZE=1280M
    volumes:
      - ./cassandra/data:/var/lib/cassandra
      - ./cassandra/logs:/var/log/cassandra
    deploy:
      resources:
        limits:
          memory: 2G
    # Prevent swap https://docs.docker.com/engine/containers/resource_constraints/#prevent-a-container-from-using-swap
    memswap_limit: 2G
    networks:
      - thehive-cortex-network
    healthcheck:
      # Waiting for cqlsh command to succeed to make sure Cassandra is ready
      test: ["CMD-SHELL", "cqlsh -u cassandra -p cassandra -e 'describe keyspaces' || exit 1"]
      start_period: 180s
      interval: 30s
      timeout: 10s
      retries: 5
    labels:
      com.strangebee.stack: "thehive-cortex-stack"
      com.strangebee.service: "cassandra"
      com.strangebee.role: "database"
      com.strangebee.environment: "testing"
      com.strangebee.version: "${cassandra_image_version}"
      com.strangebee.dependency: "None"

  elasticsearch:
    image: "elasticsearch:${elasticsearch_image_version}"
    container_name: elasticsearch
    hostname: elasticsearch
    restart: unless-stopped
    user: ${UID}:0
    environment:
      - http.host=0.0.0.0
      - discovery.type=single-node
      - cluster.name=hive
      - thread_pool.search.queue_size=10000
      - thread_pool.write.queue_size=10000
      - bootstrap.memory_lock=true
      - xpack.security.enabled=true
      - ELASTIC_PASSWORD=${elasticsearch_password} # Password for "elastic" default user
      - ES_JAVA_OPTS=-Xms1G -Xmx1G
    volumes:
      - ./elasticsearch/data:/usr/share/elasticsearch/data
      - ./elasticsearch/logs:/usr/share/elasticsearch/logs
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    deploy:
      resources:
        limits:
          memory: 2G
    memswap_limit: 2G
    networks:
      - thehive-cortex-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f -s -u 'elastic:${elasticsearch_password}' http://elasticsearch:9200/_cat/health || exit 1"]
      start_period: 180s
      interval: 10s
      timeout: 5s
      retries: 10
    labels:
      com.strangebee.stack: "thehive-cortex-stack"
      com.strangebee.service: "elasticsearch"
      com.strangebee.role: "indexing"
      com.strangebee.environment: "testing"
      com.strangebee.version: "${elasticsearch_image_version}"
      com.strangebee.dependency: "None"

  thehive:
    image: "strangebee/thehive:${thehive_image_version}"
    container_name: thehive
    hostname: thehive
    restart: unless-stopped
    command: '--no-config --no-config-secret'
    user: ${UID}:${GID}
    environment:
      - |
        JAVA_OPTS=
          -Xms1280M
          -Xmx1280M
          -XX:MaxMetaspaceSize=400m
          -XX:ReservedCodeCacheSize=250m
    volumes:
      - ./thehive/config:/etc/thehive:ro
      - ./thehive/data/files:/opt/thp/thehive/files
      - ./thehive/logs:/var/log/thehive
    deploy:
      resources:
        limits:
          memory: 2G
    memswap_limit: 2G
    networks:
      - thehive-cortex-network
    ports:
      - '0.0.0.0:9000:9000'
    healthcheck:
      test: ["CMD-SHELL", "curl -s -f thehive:9000/thehive/api/status || exit 1"]
      start_period: 40s
      interval: 10s
      timeout: 1s
      retries: 5
    depends_on:
      elasticsearch:
        condition: service_healthy
      cassandra:
        condition: service_healthy
    labels:
      com.strangebee.stack: "thehive-cortex-stack"
      com.strangebee.service: "thehive"
      com.strangebee.role: "application"
      com.strangebee.environment: "testing"
      com.strangebee.version: "${thehive_image_version}"
      com.strangebee.dependency: "elasticsearch, cassandra"

  cortex:
    image: "thehiveproject/cortex:${cortex_image_version}"
    container_name: cortex
    hostname: cortex
    restart: unless-stopped
    environment:
      - |
        JAVA_OPTS=
          -Xms1000M
          -Xmx1000M
          -XX:MaxMetaspaceSize=400m
          -XX:ReservedCodeCacheSize=250m
      - es_uri=http://elasticsearch:9200
      - job_directory=/tmp/cortex-jobs
      - docker_job_directory=${cortex_docker_job_directory}
    volumes:
      # Mounting docker socket in the container so that cortex can run jobs as containers
      - /var/run/docker.sock:/var/run/docker.sock
      # Storing jobs under /tmp for now
      - ./cortex/cortex-jobs:/tmp/cortex-jobs
      - ./cortex/config:/etc/cortex:ro
      - ./cortex/logs:/var/log/cortex
      - ./cortex/neurons:/opt/cortexneurons
    deploy:
      resources:
        limits:
          memory: 2G
    memswap_limit: 2G
    networks:
      - thehive-cortex-network
    ports:
      - '0.0.0.0:9001:9001'
    healthcheck:
      test: ["CMD-SHELL", "curl -s -f cortex:9001/cortex/api/status || exit 1"]
      start_period: 40s
      interval: 10s
      timeout: 1s
      retries: 5
    depends_on:
      elasticsearch:
        condition: service_healthy
    labels:
      com.strangebee.stack: "thehive-cortex-stack"
      com.strangebee.service: "cortex"
      com.strangebee.role: "application"
      com.strangebee.environment: "testing"
      com.strangebee.version: "${cortex_image_version}"
      com.strangebee.dependency: "elasticsearch"

  nginx:
    image: "nginx:${nginx_image_version}"
    container_name: nginx
    hostname: nginx
    restart: unless-stopped
    environment:
      SERVER_NAME: "${nginx_server_name}"
      NGINX_SSL_TRUSTED_CERTIFICATE: "${nginx_ssl_trusted_certificate}"
    volumes:
      - ./nginx/templates:/etc/nginx/templates  # Custom Nginx configuration
      - ./nginx/certs:/etc/nginx/certs  # Directory for custom certificates
    ports:
      - '3443:443'
    networks:
      - thehive-cortex-network
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.000'
    depends_on:
      - thehive
      - cortex
    labels:
      com.strangebee.stack: "thehive-cortex-stack"
      com.strangebee.service: "nginx"
      com.strangebee.role: "reverse proxy"
      com.strangebee.environment: "testing"
      com.strangebee.version: "${nginx_image_version}"
      com.strangebee.dependency: "thehive, cortex"


networks:
  thehive-cortex-network:
```

## ▶️ 5. Start TheHive Stack
```bash
docker-compose up -d
```

## ✅ Verify Containers
```bash
docker ps
```

You should see:

thehive
cassandra
elasticsearch
cortex
nginx

## 🌐 6. Access TheHive
```bash
http://<SERVER-IP>:9000
```
or (if using nginx):
```bash
https://<SERVER-IP>:3443
```

## 🧪 7. Health Check
```bash
curl http://localhost:9000/thehive/api/status
```

 ## ⚠️ 8. IMPORTANT – Licensing Requirement

After initial deployment, TheHive runs in trial mode.

To continue using:

Case management
Alerts
Integrations (Shuffle, Wazuh, etc.)

👉 You MUST request a free community license

## 📧 Steps:
Go to: https://strangebee.com/thehive/
Contact support

Request:

TheHive Community License

Without this:

Features will be restricted after trial expiration
🧠 Notes for Your ASM Project
This stack includes:
Cassandra (DB)
Elasticsearch (indexing)
Cortex (SOAR-style analysis)
Nginx (reverse proxy)
Fully compatible with:
Wazuh alerts → TheHive cases
Shuffle → automation workflows
Recommended minimum (testing):
4 CPUs
8 GB RAM

## ✅ Summary

This setup gives you:

Full TheHive test environment
Docker Compose only (no swarm complexity)
Ready for SOC pipeline integration
