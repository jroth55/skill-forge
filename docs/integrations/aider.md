# Aider

Aider is a command-line AI pair programming tool that supports conventions files.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.aider.conf.yml` + `.aider-conventions.md` |
| **Format** | YAML config, Markdown conventions |
| **Official docs** | [Aider Configuration](https://aider.chat/docs/config.html) |

## Setup

### 1. Create Aider Config

Create `.aider.conf.yml`:

```yaml
auto-commits: false
conventions: .aider-conventions.md
```

### 2. Create Conventions File

Create `.aider-conventions.md`:

```markdown
# Project Conventions

## Skill Development

When asked to create a skill, automation, or agent capability:

### Step 1: Scaffold

python tools/skill-forge/scripts/forge.py \
  --name <lowercase-hyphenated> \
  --title "<Human Readable>" \
  --description "<what it does + when to use>" \
  --archetype <basic|api-wrapper|mcp-bridge> \
  --output-dir skills/

### Step 2: Implement

Edit the generated `scripts/` files. Follow the filesystem pattern:
- Save data to `workspace/`
- Print summaries to stdout
- Cap previews to 512 bytes

### Step 3: Validate

python tools/skill-forge/scripts/validate_skill.py skills/<name>
python tools/skill-forge/scripts/security_scan.py skills/<name>

### Archetype Guide

- **basic**: Local transforms, file ops, codegen (preferred default)
- **api-wrapper**: HTTP APIs, SDKs, external services
- **mcp-bridge**: When MCP is unavoidable (rare)
```

## Usage

```bash
aider
> Create a skill that analyzes Python test coverage
```

## Notes

- Conventions are loaded automatically when Aider starts
- Use `auto-commits: false` to review changes before committing
- Aider supports multiple convention files via the config
