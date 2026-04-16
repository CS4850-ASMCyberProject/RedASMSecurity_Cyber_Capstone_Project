# Runbook: SQL Injection Detection (Web Application)

**Applies to:**
- Wazuh alerts related to web attacks
- Alerts from ModSecurity or custom detection rules
- Alert severity: High or Critical
- MITRE ATT&CK: T1190

---

## Purpose
This runbook explains how to respond to SQL injection attempts detected on web applications.

---

## Trigger Conditions
Use this runbook when:
- A Wazuh alert indicates possible SQL injection activity
- The alert contains suspicious SQL patterns or payloads
- The alert severity is high or critical

Common indicators:
- ' OR 1=1 --
- UNION SELECT
- SELECT * FROM
- sqlite_master
- Unexpected SQL errors in logs

---

## Initial Triage (0–10 minutes)

1. Identify the source of the request
    - IP address of the attacker
    - Geolocation (if available)

2. Review the request details
    - URL and endpoint targeted
    - Payload used in the request
    - HTTP method (GET, POST)

3. Check the response from the server
    - Did the request succeed or fail?
    - Any database errors returned?

4. Look for related activity
    - Multiple requests from same IP?
    - Other attack patterns (XSS, scanning, etc.)

---

## Decision Guide

- If the request is blocked and no impact occurred
  → Log the event and monitor for repeated attempts

- If the request shows probing behavior (multiple payloads)
  → Flag as active attack and monitor closely

- If the request appears successful or returns data
  → Escalate immediately as potential data breach

---

## Response Actions
- Block the source IP (firewall or WAF)
- Enable or tighten ModSecurity rules
- Validate and sanitize user inputs in the application
- Review database logs for unauthorized queries
- Patch vulnerable endpoints

---

## Escalation Criteria
Escalate immediately if:
- Sensitive data is returned in the response
- Repeated SQL injection attempts from the same source
- Multiple endpoints are targeted
- Database errors indicate possible exploitation

---

## References
- MITRE ATT&CK: T1190
- OWASP SQL Injection Guide
- Wazuh Web Attack Detection documentation