# Claude Code

Anthropic's Claude Code uses a persistent instruction file called `CLAUDE.md`.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `CLAUDE.md` (project root) |
| **Skills directory** | `.claude/skills/` |
| **Official docs** | [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) |

## Setup

### 1. Create CLAUDE.md

Create `CLAUDE.md` in your project root:

```markdown
# Skill Forge Guidelines

## Code-First Workflow

- Call Python functions in the skill rather than reimplementing them
- Use `forge.py` to generate new skills
- Do not call external services unless the skill wrapper permits it

## Filesystem Pattern

- Store raw outputs in `workspace/`
- Summarize results in stdout
- Never print data > 1KB directly

## Commands

- Create skill: `python tools/skill-forge/scripts/forge.py --interactive`
- Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
- Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`
- Package: `python tools/skill-forge/scripts/package_skill.py <path>`

## Archetype Selection

- **basic**: Local transforms, file ops, codegen (preferred default)
- **api-wrapper**: HTTP APIs, SDKs, external services
- **mcp-bridge**: Only when MCP is unavoidable
```

### 2. Add Skill Forge as a Skill (Optional)

Create `.claude/skills/skill-forge/SKILL.md`:

```markdown
---
name: skill-forge
description: Create, validate, and package new Skills. Use when the user wants to build a new skill, scaffold a skill template, or audit existing skills.
allowed-tools: Read, Write, Grep, Glob, Bash
metadata:
  archetype: basic
  risk_level: low
---

# Skill Forge

## Usage

- Create: `python tools/skill-forge/scripts/forge.py --interactive`
- Validate: `python tools/skill-forge/scripts/validate_skill.py .claude/skills/<name>`
- Package: `python tools/skill-forge/scripts/package_skill.py .claude/skills/<name>`
```

## Notes

- Claude searches for `CLAUDE.md` in parent and child directories and merges multiple files
- Subdirectories can have additional `CLAUDE.md` files with more specific guidelines
- Use the `/permissions` command to restrict Claude to safe operations
