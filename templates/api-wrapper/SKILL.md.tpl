---
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
allowed-tools: {{ALLOWED_TOOLS}}
metadata:
  archetype: api-wrapper
  risk_level: {{RISK_LEVEL}}
---

# {{SKILL_TITLE}} (API Wrapper)

## Overview
This Skill wraps an external system using code-first API calls and the **Filesystem Pattern**:
- raw data saved to `workspace/`
- only summaries printed to stdout

## When to use it
Use when:
- the user needs data from an HTTP API / SDK
- you want token-efficient processing (filter in code, summarize for the model)

Do not use when:
- the system is behind an auth/network boundary your code cannot reach (use **MCP Bridge**)

## Usage
```bash
python scripts/wrapper.py "search query"
```

## Setup
- Install optional deps:
  ```bash
  pip install -r requirements.txt
  ```
- Put secrets in env vars (never in repo files).

## References
- Filesystem Pattern: [../docs/filesystem-pattern.md](../docs/filesystem-pattern.md)
