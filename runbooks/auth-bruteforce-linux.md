# Runbook: SSH Authentication / Brute Force (Linux)

**Applies to:**
- Wazuh SSH authentication alerts
- Alert severity: High or Critical
- MITRE ATT&CK: T1110

---

## Purpose
This runbook explains how to respond to SSH brute force and excessive authentication attempts detected by Wazuh on Linux systems.

---

## Trigger Conditions
Use this runbook when:
- A Wazuh SSH alert is generated
- The alert indicates repeated login failures or brute force attempts
- The alert severity is high or critical

Common examples:
- sshd brute force attempts
- Maximum authentication attempts exceeded
- Invalid or non-existent user login attempts

---

## Initial Triage (5-10 minutes)

1. Identify the source of the login attempts
    - What IP address initiated the attempts?
    - Is the source internal or external?

2. Check the targeted account
    - Is the user valid or non-existent?
    - Is the account privileged?

3. Review timing and frequency
    - How many attempts occurred?
    - Did they happen rapidly?

4. Look for related alerts
    - Successful logins after failures?
    - New processes or suspicious activity?
    - Additional alerts from the same IP?

---

## Decision Guide

- If activity is expected testing or ASM scanning
  → Close the alert as benign and document the reason

- If repeated attempts originate from an unknown external IP
  → Investigate further and consider blocking

- If login success occurs after brute force attempts
  → Escalate immediately

---

## Response Actions
- Review SSH authentication logs
- Block or rate-limit the attacking IP if malicious
- Disable targeted accounts if compromise is suspected
- Enforce key-based authentication where possible
- Monitor for additional suspicious activity

---

## Escalation Criteria
Escalate immediately if:
- A privileged account is targeted
- Successful authentication occurs after repeated failures
- Multiple hosts receive similar brute force attempts

---

## References
- MITRE ATT&CK: T1110
- Linux SSH Hardening Guidelines
- Wazuh SSH Monitoring Documentation