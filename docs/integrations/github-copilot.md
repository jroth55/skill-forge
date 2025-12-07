# GitHub Copilot (VS Code)

VS Code's Copilot Chat supports custom instructions files that are automatically prepended to every chat session.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.github/instructions/*.instructions.md` |
| **Custom agents** | `.github/agents/*.agent.md` |
| **Legacy location** | `.github/copilot-instructions.md` (pre-1.102) |
| **Official docs** | [VS Code Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) |

## Setup

### 1. Create Instructions File

Create `.github/instructions/skillforge.instructions.md`:

```markdown
---
applyTo: "**/*.py"
description: Skill Forge coding guidelines
---

# Skill Forge Instructions

- Always call the provided Python functions rather than reimplementing them
- Save large outputs to the `workspace/` directory and summarize results
- Avoid printing raw data; provide clear, concise summaries instead
- Use the basic archetype unless external API calls are required
- Run validation before considering any skill complete
```

### 2. Create Custom Agent (Optional)

For complex workflows, create `.github/agents/skillforge.agent.md`:

```markdown
---
description: Skill Forge agent for creating and validating skills
tools: [python, fetch, files.write]
---

# Skill Forge Agent

You create skills using Skill Forge. Follow the code-first, least-privilege guidelines.

## Workflow

1. Scaffold: `python tools/skill-forge/scripts/forge.py --interactive`
2. Edit the generated scripts
3. Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
4. Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`

## Rules

- Save raw data to `workspace/`
- Print only summaries to stdout
- Never dump large JSON into the conversation
```

## Usage

Copilot automatically applies instructions to relevant chat sessions. You can also manually attach via **Add Context → Instructions**.

## Notes

- VS Code 1.102+ recommends `.instructions.md` over the legacy single-file format
- Use `applyTo` globs to target specific file types
- Nested `.instructions.md` files in subdirectories apply to those folders
