# Skill Anatomy

A valid Skill Forge skill is a self-contained folder with a specific structure.

## Directory Structure

```
my-skill/
├── SKILL.md              # Frontmatter + documentation (required)
├── skill.spec.json       # Machine-readable contract (required)
├── requirements.txt      # Python dependencies (if needed)
├── scripts/
│   ├── main.py           # Entry point
│   └── _fs.py            # Filesystem helpers
├── tests/
│   └── smoke_prompts.md  # Test prompts
└── workspace/            # Runtime artifacts (gitignored)
```

## Required Files

### SKILL.md

The primary documentation file with YAML frontmatter:

```yaml
---
name: my-skill-name
description: What this does + when to use it
allowed-tools: Read, Grep, Glob, Bash
metadata:
  archetype: basic
  risk_level: low
---

# My Skill Name

## What This Skill Does

- Description of functionality
- When to use it
- When NOT to use it

## Usage

\`\`\`bash
python scripts/main.py --help
\`\`\`
```

#### Required Frontmatter Fields

| Field | Description | Constraints |
|-------|-------------|-------------|
| `name` | Skill identifier | Lowercase hyphenated, 1-64 chars, no reserved words |
| `description` | What + when | Max 1024 chars, no XML tags |
| `allowed-tools` | MCP tools needed | Comma-separated list |

#### Optional Frontmatter Fields

| Field | Description |
|-------|-------------|
| `license` | License identifier (e.g., `MIT`) |
| `metadata` | Nested object for archetype, risk_level, etc. |

### skill.spec.json

Machine-readable contract for the skill:

```json
{
  "name": "my-skill-name",
  "title": "My Skill Name",
  "description": "What this does + when to use it",
  "archetype": "basic",
  "risk_level": "low",
  "entry_point": "scripts/main.py",
  "triggers": [
    "When the user asks to do X",
    "When the user wants Y",
    "When working with Z"
  ],
  "anti_triggers": [
    "When the user wants something unrelated",
    "When destructive operations are needed"
  ],
  "acceptance_tests": [
    "Handles empty input gracefully",
    "Saves output to workspace/",
    "Prints summary under 1KB"
  ]
}
```

#### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Must match SKILL.md frontmatter |
| `title` | Yes | Human-readable title |
| `description` | Yes | Must match SKILL.md frontmatter |
| `archetype` | Yes | `basic` \| `api-wrapper` \| `mcp-bridge` |
| `risk_level` | Yes | `low` \| `medium` \| `high` |
| `entry_point` | Yes | Path to main script |
| `triggers` | Yes | When to activate this skill |
| `anti_triggers` | Yes | When NOT to use this skill |
| `acceptance_tests` | Yes | Criteria for correct behavior |

## The workspace/ Directory

Each skill owns a `workspace/` directory at its root for runtime artifacts.

### Rules

1. **All raw data goes here** — API responses, downloaded files, generated outputs
2. **Must be gitignored** — Add to `.gitignore`
3. **Scripts should create it** — Use the `_fs.py` helper
4. **Never read/write outside** — Unless explicitly required by the skill

### Example .gitignore

```gitignore
workspace/
__pycache__/
*.pyc
```

## Scripts Directory

### Entry Point

The main script (usually `main.py` or `wrapper.py` or `bridge.py` depending on archetype):

```python
#!/usr/bin/env python3
from _fs import write_json, safe_preview_json

def main():
    # Do work
    result = {"items": [...]}
    
    # Save to workspace
    path = write_json("result.json", result)
    
    # Print summary only
    print(f"✅ Saved {len(result['items'])} items to {path}")
    print(f"Preview: {safe_preview_json(result, max_bytes=512)}")

if __name__ == "__main__":
    main()
```

### Filesystem Helpers (_fs.py)

Standard helper for the filesystem pattern:

```python
import json
from pathlib import Path

WORKSPACE = Path(__file__).parent.parent / "workspace"

def ensure_workspace():
    WORKSPACE.mkdir(exist_ok=True)
    return WORKSPACE

def write_json(filename: str, data: dict) -> Path:
    ensure_workspace()
    path = WORKSPACE / filename
    path.write_text(json.dumps(data, indent=2))
    return path

def write_text(filename: str, text: str) -> Path:
    ensure_workspace()
    path = WORKSPACE / filename
    path.write_text(text)
    return path

def safe_preview_json(data, max_bytes: int = 512) -> str:
    text = json.dumps(data, indent=2)
    if len(text) <= max_bytes:
        return text
    return text[:max_bytes] + "\n... (truncated)"

def safe_preview_text(text: str, max_bytes: int = 512) -> str:
    if len(text) <= max_bytes:
        return text
    return text[:max_bytes] + "\n... (truncated)"
```

## Tests Directory

### smoke_prompts.md

Example prompts for testing the skill:

```markdown
# Smoke Test Prompts

## Happy Path

> "Run the skill with typical input"

Expected: Saves output to workspace/, prints summary

## Empty Input

> "Run the skill with no input"

Expected: Helpful error message, no crash

## Large Input

> "Run the skill with very large input"

Expected: Handles gracefully, doesn't flood stdout
```

## Archetypes

The archetype determines which template is used:

| Archetype | Entry Point | Use Case |
|-----------|-------------|----------|
| `basic` | `scripts/main.py` | Local processing, transforms, codegen |
| `api-wrapper` | `scripts/wrapper.py` | External HTTP/SDK APIs |
| `mcp-bridge` | `scripts/bridge.py` | MCP server orchestration |

See [Decision Rubric](../docs/decision-rubric.md) for how to choose.
