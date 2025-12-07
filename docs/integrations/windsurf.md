# Windsurf

Windsurf (Codeium) supports custom rules via a `.windsurfrules` file.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.windsurfrules` (project root) |
| **Format** | Markdown |
| **Official docs** | Community practice |

> **Note:** This configuration is based on community practice as of December 2025. Verify against the latest Windsurf documentation.

## Setup

Create `.windsurfrules` in your project root:

```markdown
# Skill Development Standards

## Creating New Skills

Use Skill Forge for all skill/automation creation:

### Scaffold

python tools/skill-forge/scripts/forge.py \
  --name <skill-name> \
  --title "<Human Title>" \
  --description "<what + when>" \
  --archetype <api-wrapper|basic|mcp-bridge>

### Validate

python tools/skill-forge/scripts/validate_skill.py skills/<name>

### Security Check

python tools/skill-forge/scripts/security_scan.py skills/<name>

## Architecture Rules

- Default to `basic` for local processing
- Use `api-wrapper` for external APIs
- Use `mcp-bridge` only when MCP is mandatory
- Always implement the filesystem pattern:
  - Raw data goes to `workspace/`
  - Only summaries go to stdout
```

## Notes

- Rules are automatically loaded when Windsurf starts in the project
- Keep rules concise and actionable
- Combine with workspace settings for tool paths if needed
