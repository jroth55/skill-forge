# Sourcegraph Cody

Sourcegraph's Cody integrates with VS Code and supports custom commands.

## Quick Reference

| Item | Value |
|------|-------|
| **Commands** | `.vscode/cody.json` |
| **Global commands** | `~/.vscode/cody.json` |
| **Official docs** | [Sourcegraph Cody](https://sourcegraph.com/docs/cody) |

## Setup

### 1. Create Custom Commands

Create `.vscode/cody.json`:

```json
{
  "commands": {
    "skillforge": {
      "description": "Run Skill Forge pipeline to create and validate a skill",
      "command": "python3 tools/skill-forge/scripts/forge.py --interactive",
      "prompt": "You are using Skill Forge. Follow the code-first workflow: save raw outputs to workspace/ and summarize results. After scaffolding, validate with validate_skill.py and security_scan.py."
    },
    "validate-skill": {
      "description": "Validate an existing skill",
      "command": "python3 tools/skill-forge/scripts/validate_skill.py",
      "prompt": "Validate the skill and report any issues found."
    },
    "scan-skill": {
      "description": "Security scan a skill",
      "command": "python3 tools/skill-forge/scripts/security_scan.py",
      "prompt": "Run a security scan and report any findings."
    }
  }
}
```

### 2. Add Instructions File (Optional)

Since Cody runs in VS Code, you can also use `.github/instructions/skillforge.instructions.md` to apply code-first guidelines to all Cody Chat sessions.

## Usage

1. Open the Cody command menu: **Alt + C**
2. Type the command name: `/skillforge`
3. Cody will run the command and use the prompt context

## Notes

- Commands can run scripts, open files, or call CLI programs
- Global commands in `~/.vscode/cody.json` are available across all projects
- Install the **Cody++** extension for a graphical interface to edit commands
