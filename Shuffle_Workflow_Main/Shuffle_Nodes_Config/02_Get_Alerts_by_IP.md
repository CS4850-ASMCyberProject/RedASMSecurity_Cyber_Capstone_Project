# Get Alerts by IP Cache

## Purpose
Gets stored data cache of a list holding timestamps and user entries for a specified IP.

---

## Node Type
`Get Cache Value`

---

## Setup

**Name:**
```text
Get_Alerts_by_IP
```

**Action:**
```text
Get Cache Value
```

**Key:**
```text
alerts_by_ip_$exec.all_fields.data.srcip
```

**Category:**
```text
alerts_by_ip
```

---

## Workflow Path

```text
01_Get_Set_Thread_TS
    ↓
02_Get_Alerts_by_IP
    ↓
03_Normalize_User
(No Branch Conditional)
```
