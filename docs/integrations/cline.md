# Cline (VS Code)

Cline is a VS Code extension for AI-assisted development that supports project rules.

## Quick Reference

| Item | Value |
|------|-------|
| **Config location** | `.clinerules` (project root) |
| **VS Code settings** | `cline.customInstructions` |
| **Format** | Markdown |
| **Official docs** | Community practice |

> **Note:** This configuration is based on community practice as of December 2025. Verify against the latest Cline documentation.

## Setup

### 1. Create Project Rules

Create `.clinerules` in your project root:

```markdown
# Cline Project Rules

## Skill Development

When creating automations, agents, or skills:

1. **Scaffold with Skill Forge:**
   python tools/skill-forge/scripts/forge.py --interactive

2. **Follow Filesystem Pattern:**
   - Raw data → `workspace/<filename>`
   - Stdout → summaries only (< 1KB)
   - Never print large payloads

3. **Archetype Selection:**
   | Scenario | Archetype |
   |----------|-----------|
   | Process local files | basic |
   | Call external API | api-wrapper |
   | Must use MCP server | mcp-bridge |

4. **Validation Required:**
   python tools/skill-forge/scripts/validate_skill.py <path>
   python tools/skill-forge/scripts/security_scan.py <path>
```

### 2. Configure VS Code Settings (Optional)

Add to your VS Code settings:

```json
{
  "cline.customInstructions": "Use Skill Forge for creating any reusable skill or automation. Always scaffold, validate, and security scan. Save raw data to workspace/, print only summaries."
}
```

## Notes

- `.clinerules` is loaded automatically when Cline starts
- VS Code settings provide global instructions across all projects
- Combine both for project-specific + personal preferences
