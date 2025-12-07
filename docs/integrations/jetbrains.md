# JetBrains AI Assistant

JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, etc.) support AI assistant rules.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.aiassistant/rules/*.md` |
| **Settings path** | Settings → Tools → AI Assistant → Rules |
| **Format** | Markdown |
| **Official docs** | [Configure Project Rules](https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html) |

## Rule Types

| Type | When Applied |
|------|--------------|
| Always | Applied to all chat sessions |
| Manually | Invoked with `@rule:` or `#rule:` |
| By model decision | Applied when the model considers it relevant |
| By file patterns | Matches globs like `*.py` or `src/**` |

## Setup

### 1. Create Rules Directory

```bash
mkdir -p .aiassistant/rules
```

### 2. Create Skill Forge Rules

Create `.aiassistant/rules/skillforge.md`:

```markdown
# Skill Forge Guidelines

## When to Apply

Apply these rules when creating skills, automations, or agent capabilities.

## Code-First Workflow

- Implement as Python scripts
- Save raw outputs to `workspace/`
- Summarize results in stdout

## Commands

- Scaffold: `python tools/skill-forge/scripts/forge.py --interactive`
- Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
- Scan: `python tools/skill-forge/scripts/security_scan.py <path>`

## Archetypes

- **basic**: Local processing (default)
- **api-wrapper**: External APIs
- **mcp-bridge**: MCP required only
```

### 3. Configure Rule Type

In your IDE:

1. Go to **Settings → Tools → AI Assistant → Rules**
2. Select the rule file
3. Choose the appropriate rule type (recommend: **Always** for Skill Forge guidelines)

## Custom Prompts (Optional)

For additional custom prompts:

1. Go to **Tools → AI Assistant → Prompt Library**
2. Create prompts that incorporate Skill Forge instructions
3. Use `$SELECTION` variable to insert selected code

## Notes

- Rules are version-controlled when stored in `.aiassistant/rules/`
- Multiple rule files can coexist
- Use "By file patterns" for language-specific rules
