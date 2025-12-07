# Skill Forge 2.0

**A meta-skill for AI coding assistants to create, validate, and package production-ready Skills.**

Skill Forge is a scaffold generator for building "skills" — modular pieces of functionality that can be used by AI agents or editors such as VS Code. It enforces a "code-first" architecture where Python scripts handle the heavy lifting and MCP (Model Context Protocol) is used only when necessary.

## Who This Is For

- **Developers** building AI "skills" or MCP tools for coding assistants
- **Team leads** standardizing AI-assisted workflows across a codebase
- **Anyone** maintaining a repo and wanting consistent, safe AI behavior

This repo is **meta tooling** — it helps you create skills, not run them.

## Quick Start

### Prerequisites

- Python >= 3.10
- Git

### Installation

```bash
git clone https://github.com/jroth55/skill-forge.git
cd skill-forge
```

No dependencies required (stdlib only).

### Create Your First Skill

```bash
# Interactive mode (recommended)
python scripts/forge.py --interactive

# Or non-interactive
python scripts/forge.py \
  --name my-skill \
  --title "My Skill" \
  --description "Does X when user asks for Y" \
  --archetype basic
```

### Validate and Scan

```bash
python scripts/validate_skill.py .claude/skills/my-skill
python scripts/security_scan.py .claude/skills/my-skill
```

### Package for Distribution

```bash
python scripts/package_skill.py .claude/skills/my-skill
```

## Core Philosophy

The core idea is to **save intermediate data to disk**, **let code handle heavy lifting**, and **summarize results**. This protects the model's context window and reduces the risk of leaking raw data.

| Principle | What It Means |
|-----------|---------------|
| **Code-first** | Implement skills as Python scripts. Avoid long chains of tool calls. |
| **Filesystem pattern** | Raw data → `workspace/`. Stdout → summaries only (< 1KB). |
| **Least privilege** | Request only the tools you need. Confirm destructive actions. |

## Archetypes & Decision Rubric

Choose the right template based on your use case:

```
Is this local processing (files, transforms, codegen)?
├── YES → basic (preferred default)
└── NO
    └── Can you reach the system via HTTP/SDK?
        ├── YES → api-wrapper
        └── NO (auth/network boundary)
            └── mcp-bridge (last resort)
```

| Archetype | Use Case | Entry Point |
|-----------|----------|-------------|
| **basic** | Local transforms, file ops, codegen | `scripts/main.py` |
| **api-wrapper** | External HTTP/SDK APIs | `scripts/wrapper.py` |
| **mcp-bridge** | MCP server orchestration | `scripts/bridge.py` |

**When NOT to use Skill Forge:**
- Quick one-off transformations
- Conversational Q&A with no persistent artifacts
- Simple chat interactions

## Integrations

Skill Forge works with 13+ AI coding assistants. Each has a dedicated setup guide:

| Assistant | Config Location | Guide |
|-----------|-----------------|-------|
| GitHub Copilot | `.github/instructions/*.instructions.md` | [Setup](docs/integrations/github-copilot.md) |
| Claude Code | `CLAUDE.md` | [Setup](docs/integrations/claude-code.md) |
| Cursor | `.cursor/rules/*.mdc` | [Setup](docs/integrations/cursor.md) |
| Windsurf | `.windsurfrules` | [Setup](docs/integrations/windsurf.md) |
| Cline | `.clinerules` | [Setup](docs/integrations/cline.md) |
| Aider | `.aider-conventions.md` | [Setup](docs/integrations/aider.md) |
| Continue | `.continue/config.json` | [Setup](docs/integrations/continue.md) |
| Amazon Q | `.amazonq/rules/*.md` | [Setup](docs/integrations/amazon-q.md) |
| Gemini | `.gemini/instructions.md` | [Setup](docs/integrations/gemini.md) |
| Tabnine | `.tabnine/guidelines/*.md` | [Setup](docs/integrations/tabnine.md) |
| JetBrains AI | `.aiassistant/rules/*.md` | [Setup](docs/integrations/jetbrains.md) |
| Sourcegraph Cody | `.vscode/cody.json` | [Setup](docs/integrations/cody.md) |
| ChatGPT | Custom Instructions / GPTs | [Setup](docs/integrations/chatgpt.md) |

See [docs/integrations/](docs/integrations/) for the full index.

## Documentation

| Document | Description |
|----------|-------------|
| [CLI Reference](docs/cli.md) | All commands, options, and exit codes |
| [Skill Anatomy](docs/skill-anatomy.md) | File structure, SKILL.md, skill.spec.json |
| [Filesystem Pattern](docs/filesystem-pattern.md) | Why and how to use `workspace/` |
| [Decision Rubric](docs/decision-rubric.md) | When to use each archetype |
| [Security](docs/security.md) | Security principles and scanner details |
| [Integrations](docs/integrations/) | Per-assistant setup guides |

## Example

The `examples/git-commit-helper/` directory contains a complete skill:

```bash
# Validate the example
python scripts/validate_skill.py examples/git-commit-helper

# Run it (from a git repo with staged changes)
python examples/git-commit-helper/scripts/main.py
```

## Project Structure

```
skill-forge/
├── scripts/           # CLI tools (forge, validate, scan, package)
├── templates/         # Archetype templates (basic, api-wrapper, mcp-bridge)
├── docs/              # Documentation
│   └── integrations/  # Per-assistant setup guides
├── examples/          # Example skills
├── SKILL.md           # This repo's own skill definition
└── README.md          # You are here
```

## Security

The security scanner is **heuristic** — it catches common issues but has limitations:

- **False positives**: Documentation mentioning dangerous patterns
- **False negatives**: Obfuscated or novel attack patterns

**Manual review is still required.**

See [docs/security.md](docs/security.md) for details.

## Contributing

1. Fork and clone
2. Create a skill using Skill Forge (dogfood it!)
3. Run `python scripts/validate_skill.py` and `python scripts/security_scan.py`
4. Submit PR

## License

MIT License — see [LICENSE.txt](LICENSE.txt)

---

*Built for AI assistants that build things.*
