# Google Gemini Code Assist

Google's Gemini Code Assist reads project instructions from a `.gemini/` directory.

## Quick Reference

| Item | Value |
|------|-------|
| **Instructions** | `.gemini/instructions.md` |
| **Style guide** | `.gemini/styleguide.md` |
| **Config** | `.gemini/config.yaml` |
| **Official docs** | [Gemini Code Assist Customization](https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github) |

## Setup

### 1. Create Instructions File

Create `.gemini/instructions.md`:

```markdown
# Project Context

This project uses Skill Forge for creating AI agent skills.

# Coding Standards

- Follow PEP 8 for Python
- Use type hints
- Require docstrings

# Architecture

- Code-first: prefer Python scripts over tool chains
- Save raw outputs to `workspace/`
- Print only summaries to stdout (< 1KB)

# Skill Creation Workflow

1. Scaffold: `python tools/skill-forge/scripts/forge.py --interactive`
2. Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
3. Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`

# Important Notes

- Never print large JSON blobs
- Use basic archetype unless external API is required
- MCP bridge is the last resort
```

### 2. Create Style Guide (Optional)

Create `.gemini/styleguide.md` for code review rules:

```markdown
# Style Guide

- Maximum line length: 100
- Indentation: 4 spaces
- Imports: stdlib, third-party, local (separated by blank lines)
- Naming: snake_case for functions/variables, PascalCase for classes
- Type hints required for function signatures
```

### 3. Create Config (Optional)

Create `.gemini/config.yaml` to configure indexing:

```yaml
# Exclude large data files from context
exclude:
  - workspace/**
  - "*.json"
```

## Notes

- Gemini merges project instructions with enterprise-level style guides
- Project-level settings take precedence over global settings
- Commit your `.gemini/` folder to version control for team consistency
