## 🛡️ Wazuh Agent Setup (Target VM)

From your Wazuh Manager, get:

Manager IP → Determine your manager private IP

⚙️ 1. Add Wazuh repository
```bash
curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | sudo apt-key add -

echo "deb https://packages.wazuh.com/4.x/apt/ stable main" | \
sudo tee /etc/apt/sources.list.d/wazuh.list

sudo apt update
```

📦 2. Install Wazuh agent
```bash
sudo apt install wazuh-agent -y
```

🧾 3. Configure agent

Edit config:
```bash
sudo nano /var/ossec/etc/ossec.conf
```
Find:
```bash
<client>
  <server>
    <address>MANAGER_IP</address>
    <port>1514</port>
    <protocol>tcp</protocol>
  </server>
</client>
```
Replace:
```bash
<address>10.0.0.97</address>
🔑 4. Register the agent
Option A (modern, easiest — recommended)
sudo /var/ossec/bin/agent-auth -m 10.0.0.97
```

🚀 5. Start the agent
```bash
sudo systemctl daemon-reexec
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

🔍 6. Verify it’s running
```bash
sudo systemctl status wazuh-agent
```

🧪 7. Verify from Manager
```bash
sudo /var/ossec/bin/agent_control -l
```
You should see:
```bash
ID: 001  Name: asm-target  IP: 10.0.0.48  Active
```
