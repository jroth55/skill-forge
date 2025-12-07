---
name: git-commit-helper
description: Generate concise git commit messages from staged diffs. Use when the user asks for a commit message or wants help summarizing staged changes.
allowed-tools: Read, Grep, Glob, Bash
metadata:
  archetype: basic
  risk_level: low
---

# Git Commit Helper

## What this Skill does
- Reads the staged diff (via git)
- Saves a short diff preview to workspace/
- Produces a suggested commit message (human-reviewed)

## Usage
```bash
python scripts/main.py
```
