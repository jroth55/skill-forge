# Continue

Continue is an open-source AI code assistant for VS Code and JetBrains.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.continue/config.json` |
| **Rules file** | `.continue/rules.md` |
| **Format** | JSON config, Markdown rules |
| **Official docs** | [Continue Documentation](https://continue.dev/docs) |

## Setup

### 1. Configure Custom Commands

Create or edit `.continue/config.json`:

```json
{
  "customCommands": [
    {
      "name": "skill",
      "description": "Create a new skill with Skill Forge",
      "prompt": "Create a new skill using Skill Forge. Scaffold with: python tools/skill-forge/scripts/forge.py --interactive. Follow the filesystem pattern (save raw data to workspace/, print only summaries). Validate with validate_skill.py and security_scan.py before finishing."
    }
  ],
  "systemMessage": "When creating skills or automations, use Skill Forge. Default to basic archetype. Always validate and security scan. Save raw data to workspace/, print only summaries."
}
```

### 2. Create Rules File

Create `.continue/rules.md`:

```markdown
# Continue Rules

## Skill Creation

Always use Skill Forge for skills:

1. `python tools/skill-forge/scripts/forge.py --interactive`
2. Edit generated scripts
3. `python tools/skill-forge/scripts/validate_skill.py <path>`
4. `python tools/skill-forge/scripts/security_scan.py <path>`

## Filesystem Pattern

- Raw data → `workspace/`
- Stdout → summaries only
- Max preview: 512 bytes
```

## Usage

```
/skill Create a skill that fetches Jira tickets
```

## Notes

- Custom commands are invoked with `/commandname`
- The system message applies to all conversations
- Rules are loaded automatically and apply globally
