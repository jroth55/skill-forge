# Cursor

Cursor is a VS Code fork with integrated AI assistance that supports multiple rule types.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.cursor/rules/*.mdc` |
| **Alternative** | `AGENTS.md` (legacy, still supported) |
| **User rules** | Cursor Settings → Rules |
| **Official docs** | [Cursor Rules](https://cursor.com/docs/context/rules) |

## Rule Types

| Type | When Applied |
|------|--------------|
| Always Apply | Every chat session |
| Apply Intelligently | Agent decides based on description |
| Apply to Specific Files | Matches glob patterns |
| Apply Manually | Invoked with `@rule:` or `#rule:` |

## Setup

### 1. Create Project Rules

Create `.cursor/rules/skillforge.mdc`:

```markdown
---
description: Guidelines for using Skill Forge
alwaysApply: true
---

# Skill Forge Rules

When asked to create a "skill", "agent capability", or "automation":

## Workflow

1. Scaffold: `python tools/skill-forge/scripts/forge.py --interactive`
2. Implement the generated scripts following the filesystem pattern
3. Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
4. Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`

## Filesystem Pattern

- Save raw API responses to `workspace/`
- Print only summaries and artifact paths to stdout
- Never dump large JSON into the conversation

## Archetype Selection

- **basic**: Local processing, transforms, generation (preferred)
- **api-wrapper**: HTTP/SDK-accessible systems
- **mcp-bridge**: Only when MCP is required (auth/network boundary)
```

### 2. Add Language-Specific Rules (Optional)

Create `.cursor/rules/python-skills.mdc`:

```markdown
---
description: Python skill guidelines
globs: ["**/*.py"]
---

# Python Skill Rules

- Use type hints for all function signatures
- Follow PEP 8 style guidelines
- Save outputs to `workspace/`
- Include docstrings for public functions
```

## Alternative: AGENTS.md

You can also use a simple `AGENTS.md` file at the project root with similar content. This is a legacy approach but still supported.

## Notes

- Project rules in `.cursor/rules/` are version-controlled
- User rules (Settings → Rules) are global preferences
- Team rules are managed via the Cursor web dashboard
