# Tabnine

Tabnine supports guidelines stored in Markdown files (max 500 lines each).

## Quick Reference

| Item | Value |
|------|-------|
| **Guidelines** | `.tabnine/guidelines/*.md` |
| **MCP config** | `.tabnine/mcp_servers.json` |
| **Official docs** | [Tabnine Guidelines](https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines) |

## Setup

### 1. Create Guidelines Directory

```bash
mkdir -p .tabnine/guidelines
```

### 2. Create Skill Forge Guidelines

Create `.tabnine/guidelines/skillforge.md`:

```markdown
# Skill Forge Guidelines

## Code-First Approach

- Implement skills as Python scripts
- Call functions in the skill rather than reimplementing them
- Save raw data to `workspace/`

## Workspace Pattern

- Large data (CSV, JSON, PDFs) → save under `workspace/`
- Reference files in the answer, don't embed content
- Summaries only in stdout

## Example: Saving a CSV

path = write_workspace("results.csv", csv_data)
print(f"Saved {len(rows)} rows to {path}")
print(f"Columns: {', '.join(columns)}")

## Workflow

1. `python tools/skill-forge/scripts/forge.py --interactive`
2. Edit scripts/
3. `python tools/skill-forge/scripts/validate_skill.py <path>`
4. `python tools/skill-forge/scripts/security_scan.py <path>`
```

### 3. Configure MCP Servers (Optional)

If your skill wraps an MCP server, create `.tabnine/mcp_servers.json`:

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "python",
      "args": ["scripts/mcp_server.py"],
      "env": {}
    }
  }
}
```

## Notes

- Keep each guideline file under 500 lines
- Use multiple files to organize guidelines by topic
- Guidelines are automatically loaded when Tabnine starts
