---
name: skill-forge
description: Meta-skill that scaffolds, validates, and packages other Agent Skills. Enforces code-first (MCP is the special case) via archetypes and filesystem-based workflows.
allowed-tools: Read, Write, Grep, Glob, Bash
license: MIT
metadata:
  version: 2.0.0
---

# Skill Forge (Meta‑Skill)

Skill Forge creates **production-ready Skill folders** using opinionated **archetypes** that enforce:

- **Code execution is the default**
- **MCP is the special case**
- **Filesystem Pattern**: raw data to `workspace/`, stdout only for summaries

## Quickstart

Create a new Skill (interactive):
```bash
python scripts/forge.py --interactive
```

Validate a Skill:
```bash
python scripts/validate_skill.py .claude/skills/<skill-name>
```

Package a Skill zip (folder as zip root):
```bash
python scripts/package_skill.py .claude/skills/<skill-name>
```

Security scan (heuristic):
```bash
python scripts/security_scan.py .claude/skills/<skill-name>
```

## Archetypes

1) **API Wrapper (default)**  
For replacing HTTP/SDK-able MCP tools with code. Implements the Filesystem Pattern by default.

2) **Basic Logic**  
For local transforms, file processing, parsing, deterministic generation.

3) **MCP Bridge (special case)**  
For unavoidable MCP usage (auth/network boundary) while keeping orchestration in code via stdio JSON‑RPC.

## What “code-first” means here

- Skills should primarily run scripts rather than perform long chains of direct tool calls.
- Scripts save raw outputs to disk and print small summaries or previews.
- When MCP is required, wrap calls behind a script so loops, retries, and batching happen in code.

## References

- Architecture decision rubric: [docs/decision-rubric.md](docs/decision-rubric.md)  
- Filesystem Pattern: [docs/filesystem-pattern.md](docs/filesystem-pattern.md)  
- Security notes: [docs/security.md](docs/security.md)  
- Skill spec format: [docs/skill-spec.md](docs/skill-spec.md)
