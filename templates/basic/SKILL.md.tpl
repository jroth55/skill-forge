---
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
allowed-tools: {{ALLOWED_TOOLS}}
metadata:
  archetype: basic
  risk_level: {{RISK_LEVEL}}
---

# {{SKILL_TITLE}} (Basic Logic)

## What this Skill does
- Runs a deterministic local script
- Writes artifacts under `workspace/`
- Prints only summaries/previews

## Usage
```bash
python scripts/main.py --help
```

## References
- Filesystem Pattern: [../docs/filesystem-pattern.md](../docs/filesystem-pattern.md)
