---
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
allowed-tools: {{ALLOWED_TOOLS}}
metadata:
  archetype: mcp-bridge
  risk_level: {{RISK_LEVEL}}
---

# {{SKILL_TITLE}} (MCP Bridge)

## Overview
This Skill uses an **MCP server**, but keeps the workflow **code-first**:
- MCP called from a script (stdio JSON‑RPC)
- artifacts saved to `workspace/`
- stdout is summaries only

## When to use it
Use when:
- the system requires MCP (auth isolation or network boundary)
- you still need orchestration (loops/retries/batching) in code

## Usage

List tools:
```bash
python scripts/bridge.py --server "uvx some-mcp-server@latest" --list-tools --tool dummy
```

Call a tool:
```bash
python scripts/bridge.py --server "uvx some-mcp-server@latest" --tool "tool_name" --args '{"k":"v"}'
```

## References
- Decision rubric: [../docs/decision-rubric.md](../docs/decision-rubric.md)
- Filesystem Pattern: [../docs/filesystem-pattern.md](../docs/filesystem-pattern.md)
