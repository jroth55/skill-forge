# CLI Reference

Skill Forge provides Python scripts for scaffolding, validating, scanning, and packaging skills.

## Prerequisites

- Python >= 3.10
- No external dependencies (stdlib only)

## Commands

### forge.py — Scaffold a New Skill

```bash
# Interactive mode (recommended)
python scripts/forge.py --interactive

# Non-interactive mode
python scripts/forge.py \
  --name github-issue-fetcher \
  --title "GitHub Issue Fetcher" \
  --description "Fetch and summarize GitHub issues" \
  --archetype api-wrapper \
  --risk low
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--name` | Skill name (lowercase-hyphen, 1-64 chars) | — |
| `--title` | Human-readable title | Auto-generated from name |
| `--description` | What + when (appears in skill discovery) | — |
| `--archetype` | `basic` \| `api-wrapper` \| `mcp-bridge` | `api-wrapper` |
| `--risk` | `low` \| `medium` \| `high` | `low` |
| `--output-dir` | Where to create the skill folder | `.claude/skills` |
| `--force` | Overwrite existing skill folder | `false` |
| `--interactive` | Guided prompts | `false` |

### validate_skill.py — Validate a Skill

Checks structure, frontmatter, syntax, and dependencies.

```bash
python scripts/validate_skill.py <skill-path>

# Example
python scripts/validate_skill.py skills/github-issue-fetcher
```

#### What It Checks

- `SKILL.md` exists with valid YAML frontmatter
- Required fields: `name`, `description`, `allowed-tools`
- `skill.spec.json` exists and matches frontmatter
- Entry point script exists
- Python syntax (AST parse) for all `scripts/*.py`
- Import hints vs `requirements.txt`
- Internal link targets exist

#### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Validation passed |
| 1 | Validation failed |

### security_scan.py — Security Scan

Heuristic scan for credentials, dangerous patterns, and prompt injection phrases.

```bash
python scripts/security_scan.py <skill-path>

# Example
python scripts/security_scan.py skills/github-issue-fetcher
```

#### What It Detects

| Pattern | Risk |
|---------|------|
| `-----BEGIN PRIVATE KEY-----` | Private key material |
| `AKIA[0-9A-Z]{16}` | AWS access key |
| `xoxb-*`, `xoxp-*` | Slack tokens |
| "ignore previous instructions" | Prompt injection |
| `rm -rf`, `mkfs` | Destructive commands |
| `curl \| bash` | Pipe-to-shell |
| `eval()`, `exec()` | Dangerous Python |
| `shell=True` | Injection risk |

#### Limitations

This scanner is **heuristic**. It will:
- Produce false positives (e.g., documentation mentioning these patterns)
- Miss obfuscated or novel attack patterns

**Manual review is still required.**

#### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No findings (or findings are informational) |
| Non-zero | Findings require review |

### package_skill.py — Package for Distribution

Creates a distributable zip file with the skill folder at the root.

```bash
python scripts/package_skill.py <skill-path>

# With custom output path
python scripts/package_skill.py skills/my-skill --out my-skill-v1.0.zip
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--out` | Output zip path | `<skill-name>.zip` next to folder |

#### Excluded Files

- `__pycache__/`
- `.git/`, `.svn/`, `.hg/`
- `workspace/` (runtime artifacts)
- `*.zip`, `*.pyc`

### audit_skills.py — Batch Audit

Validates and scans all skills in a directory.

```bash
python scripts/audit_skills.py --skills-dir .claude/skills
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skills-dir` | Directory containing skill folders | `.claude/skills` |

#### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All skills passed validation |
| Non-zero | One or more skills failed |

## Running from Different Locations

When Skill Forge is vendored into your project (e.g., at `tools/skill-forge/`):

```bash
# From project root
python tools/skill-forge/scripts/forge.py --interactive

# Output skills to project's skills directory
python tools/skill-forge/scripts/forge.py \
  --name my-skill \
  --output-dir ./skills
```

When running from within the Skill Forge repository:

```bash
# From skill-forge root
python scripts/forge.py --interactive
```
