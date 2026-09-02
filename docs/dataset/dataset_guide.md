# Dataset Guide — CERT Insider Threat r4.2

## Overview

The CERT Insider Threat dataset (release 4.2) contains synthetic enterprise data
simulating 1,000 employees over 18 months with two embedded insider threat scenarios.

## Files

| File | Size | Records | Description |
|------|------|---------|-------------|
| `logon.csv` | ~56 MB | ~500K | Logon/logoff events |
| `device.csv` | ~28 MB | ~200K | USB device connect/disconnect |
| `email.csv` | ~1.3 GB | ~2M | Email messages with content |
| `http.csv` | ~14.5 GB | ~28M | Web browsing with URLs |
| `file.csv` | ~184 MB | ~400K | File copies to removable media |
| `psychometric.csv` | ~44 KB | 1,000 | Big Five personality scores |
| `LDAP/` | ~2.5 MB | 18 files | Monthly employee directory |

## Key Threat Indicators

- After-hours logins and device usage
- Logins to other users' machines
- Increased removable device usage
- Changes in email patterns
- Unusual web browsing topics
- Employee termination events

See `dataset/metadata/schema.yaml` for complete column definitions.
