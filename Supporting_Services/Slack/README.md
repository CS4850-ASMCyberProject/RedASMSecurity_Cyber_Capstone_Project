# 💬 Slack Setup – Shuffle SOC Output

## 📌 Overview

Slack was used as the real-time SOC interface for the Red ASM Security project.

Shuffle sends alerts into Slack, and Slack interactive buttons send actions back into Shuffle.

🔗 Slack Channels Used
#redasm-alerts  
#redasm-cases  

Channel	Purpose
#redasm-alerts	General alert output from Wazuh → Shuffle  
#redasm-cases	Higher-risk alerts promoted for case triage  

## ⚙️ 1. Create Slack App
Go to Slack API Apps
Create a new app
Choose From Manifest
Select the workspace
Paste/import your Slack app manifest
Create the app

## 🔐 2. Required Bot Permissions

Minimum OAuth bot scopes:
```bash
oauth_config:
  scopes:
    bot:
      - chat:write
      - chat:write.public
      - channels:read
      - groups:read
```

For interactive buttons / workflows, also include:
      - commands
      - incoming-webhook
      
## 📲 3. Install App to Workspace
Go to OAuth & Permissions
Click Install to Workspace
Approve permissions
Copy the Bot User OAuth Token

Example:
```bash
xoxb-xxxxxxxxxxxxxxxx
```

## 📢 4. Add App to Slack Channels

Inside each channel, invite the bot:
```bash
/invite @your-slack-app-name
```

Add it to:

#redasm-alerts
#redasm-cases

## 🔄 5. Shuffle Slack Output

In Shuffle, configure Slack output nodes to post into:

redasm-alerts
redasm-cases

Basic routing:
```bash
Wazuh Alert
    ↓
Shuffle Webhook
    ↓
Alert Enrichment / Decision Logic
    ↓
Slack Output
    ├── #redasm-alerts
    └── #redasm-cases
```

## 🧩 6. Enable Slack Interactivity

Slack interactivity is required for:

Buttons  
Shortcuts  
Modals  
Select menus  
Action-based workflows  

In the Slack app settings:  

Go to Interactivity & Shortcuts  
Turn Interactivity ON  

Set the Request URL to: 
```bash
https://slack_blockip.redasmsecurity.cloud/api/v1/hooks/webhook_ddec6399-cd24-4c2c-bf09-abfd4a2d14db
```

Save changes

Slack will send an HTTP POST request to this URL whenever a user clicks an interactive component.

## 🚨 7. Interactive Button Workflow

Example Slack actions:

Block IP
Contain Path

Workflow:
```bash
Analyst clicks Slack button
    ↓
Slack sends POST request to Shuffle interactivity webhook
    ↓
Shuffle parses button payload
    ↓
Shuffle runs response logic
    ↓
Shuffle sends HTTP request to Python Server to Run Remote Automated script
    ↓
Block Action is executed against target infrastructure
```

## 🧱 8. Example Use Case: Block / Contain Response

For the Red ASM project, interactive buttons can trigger Shuffle workflows that:

Receive Slack button click
Parse the selected action
Identify the target IP, path, or alert
SSH into the target VM
Write temporary Nginx block rules
Test Nginx config
Reload Nginx

Example response flow:
```bash
Slack Button Click
    ↓
Shuffle Webhook
    ↓
SSH to Target VM
    ↓
Write Nginx Rule
    ↓
nginx -t
    ↓
systemctl reload nginx
    ↓
Slack Confirmation
```
