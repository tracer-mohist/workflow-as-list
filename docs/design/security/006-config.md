<!-- docs/design/security/006-config.md -->
# Configuration

Date: 2026-03-09
Status: Accepted
Authors: sha_dow, Tracer

---

## Purpose

Define configuration format and structure.

---

## File Format

INI format. Simple, practical.

Location: ~/.config/wf/config.ini

---

## Structure

```ini
[security]
blacklist_file = ~/.config/wf/blacklist.txt

[audit]
network_whitelist_file = ~/.config/wf/network-whitelist.txt
command_whitelist_file = ~/.config/wf/command-whitelist.txt
requires_human_review = base64,url,ip_address,command_keyword

[executor]
context_max = 128000
bytes_per_token = 4

[paths]
registry_file = ~/.config/wf/registry.jsonl
audit_log_file = ~/.config/wf/audit.log
```

NOTE: Token limits calculated, not configured.

---

## Blacklist Format

```ini
# ~/.config/wf/blacklist.txt
# One keyword per line
# Matching: Substring match

rm -rf
eval(
exec(
/etc/passwd
base64 -d
curl | bash
```

---

## Whitelist Format

### Network

```ini
# ~/.config/wf/network-whitelist.txt
# One domain or IP per line

github.com
api.github.com
127.0.0.1
```

### Command

```ini
# ~/.config/wf/command-whitelist.txt
# One command pattern per line

git status
git add
npm install
```

---

## Loading Order

1. Load global config (~/.config/wf/config.ini)
2. Load project config (.wf/config.ini, if exists)
3. Use defaults for missing values

---

## Defaults

| Setting | Default |
|---------|---------|
| context_max | 128000 |
| bytes_per_token | 4 |
| registry_file | ~/.config/wf/registry.jsonl |
| blacklist_file | ~/.config/wf/blacklist.txt |
| whitelist files | Empty (opt-in) |

---

## Design Decisions

DECISION: 2026-03-09 — INI format.

WHY: Simple, practical, widely supported.

---

DECISION: 2026-03-09 — Token limits not configured.

WHY: Calculated from context_max. Formula-based.

---

## Related Documents

REFERENCE: 005-layers.md — Security layers
REFERENCE: ../../../research/encoding/002-ascii.md — Encoding rationale

---

Last Updated: 2026-03-09
