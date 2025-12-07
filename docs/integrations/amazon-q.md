# Amazon Q Developer

Amazon Q Developer (formerly AWS CodeWhisperer) supports project rules in Markdown files.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.amazonq/rules/*.md` |
| **Format** | Markdown |
| **Official docs** | [Amazon Q Developer Documentation](https://docs.aws.amazon.com/amazonq/) |

> **Note:** Path and format may change. Verify against the latest AWS documentation.

## Setup

### 1. Create Rules Directory

```bash
mkdir -p .amazonq/rules
```

### 2. Create Skill Forge Rules

Create `.amazonq/rules/skillforge.md`:

```markdown
# Skill Forge Guidelines

## Philosophy

- Code-first: implement skills as Python code
- Save large outputs under `workspace/`
- Summarize results in stdout, never dump raw data

## Workflow

1. Scaffold: `python tools/skill-forge/scripts/forge.py --interactive`
2. Implement the generated scripts
3. Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
4. Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`

## Archetypes

- **basic**: Local processing (preferred default)
- **api-wrapper**: External API access
- **mcp-bridge**: MCP required (rare)

## Filesystem Pattern

- Large data (CSV, JSON, PDFs) → save under `workspace/`
- Reference files in the answer, don't embed content
- Keep stdout summaries under 1KB
```

## Notes

- Rules are automatically loaded when you chat with Q in your IDE
- You can centralize common rules in a shared Git repository
- Multiple rule files can coexist in the `rules/` directory
