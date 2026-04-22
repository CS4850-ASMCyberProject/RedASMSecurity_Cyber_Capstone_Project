# Attack Surface Management: The Blueprint to Cyber Attacks & Defensive Strategies 
# Red ASM Security Cyber Capstone Project

Attack or Defend, Heads or Tails, ASM reveals the bet that will break the bank

The Focus of this project:
- Attack Surface Management (ASM) - Tools that uncover the target scope for which attackers attack & defenders defend
- Security Detection & Response with Security Information and Event Management (SIEM) & Security Orchestration, Automation, and Response (SOAR) Tools
- Implementation of ASM for Defender & Attacker Pipelines, showcasing Red/Blue team tactics for infiltration and Defense
- Secure System Hardening using action buttons, Modsecurity, & code correction
- Simulate SQL Injection on OWASP cyber security training website
- Cyber ready infrastructure that demonstrates a weak, attack endpoint alongside an invisible, defensive management bunker

## Structure
- ASM_Target
-   Docker service OWASP Juice Shop
-   ModSecurity
-   Nginx Server
-     OWASP Juice Shop hardened by Modsecurity & Slack Action Buttons (shop.redasmsecurity.cloud)
-     OWASP Juice Shop with fixed backend code, implementing parameterized queries (secure-shop.redasmsecurity.cloud)
-   Wazuh Agent collects alerts 
- ASM_Manager
-   Wazuh Manager SIEM tool automates threat detection (receives alerts from Wazuh Agent)
-   Shuffle SOAR tool automates threat response (receives alerts from Wazuh Manager)
-   TheHive Case Management Tool (Threat Response Hub for investigation)
-   Python server listening for Shuffle response to perform remote automated scripts to block ips and contain juice shop URL path
-   ASM scanning script - daily scans for updated attack surface monitoring & vulnerability prevention
-   MySQL Database stores ASM scan records which displays attack surface assets, vulnerabilities, & hardening updates.
- Supporting Services
-   Bought A Domain (redasmsecurity.cloud)
-   Slack - Main Threat Response Hub with alerts channel for low priority threats and cases channel for high priority threats
-   Cloudflare - Subdomain creation & tunnel to access private ASM_Manager services via Internet
-   Crontab - automates daily ASM scans
-   Docker - Manages Shuffle, TheHive, & OWASP Juice Shop with greater efficiency 

## Contributors
- Adam Llado
- Kimani Gordon
- Alec Sundby
- Austin Abeln
