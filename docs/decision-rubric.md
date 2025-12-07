# Architecture Decision Rubric

## The Golden Rule

**Code execution is the default. MCP is the special case.**

## Quick Decision Tree

```
Is this local processing (files, transforms, codegen)?
├── YES → basic (preferred default)
└── NO
    └── Can you reach the system via HTTP/SDK?
        ├── YES → api-wrapper
        └── NO (auth/network boundary)
            └── Do you need loops/retries/batching?
                ├── YES → mcp-bridge
                └── NO → raw MCP (acceptable but costly)
```

## Detailed Decision Flow

### Step 1: Is this purely local work?

**Examples:** Parse a file, transform data, generate code, run CLI tools

- **YES** → Use **basic** archetype
- **NO** → Continue to Step 2

### Step 2: Can you access the system via HTTP/SDK/CLI?

**Question:** From your execution environment, can a Python script directly call the API?

- **YES** → Use **api-wrapper** archetype
  - Save raw outputs to `workspace/`
  - Print only summaries + artifact paths
- **NO** → Continue to Step 3

### Step 3: Is the system isolated?

**Examples:** OAuth dance required, enterprise proxy, VPN-only access, localhost-only service

- **YES** → You probably need MCP → Continue to Step 4
- **NO** → Reconsider **basic** or **api-wrapper**

### Step 4: Do you need orchestration?

**Question:** Does your workflow need loops, conditions, retries, or batching?

- **YES** → Use **mcp-bridge** archetype
  - Spawn MCP server from code
  - Orchestrate via stdio JSON-RPC
  - Keep control flow in Python
- **NO** → Raw MCP calls may be acceptable
  - But still worse for token costs
  - Consider wrapping anyway

## Archetype Summary

| Archetype | When to Use | Entry Point |
|-----------|-------------|-------------|
| **basic** | Local transforms, file ops, codegen | `scripts/main.py` |
| **api-wrapper** | External HTTP/SDK APIs you can reach | `scripts/wrapper.py` |
| **mcp-bridge** | MCP required but need code orchestration | `scripts/bridge.py` |

## Examples

| Task | Archetype | Reasoning |
|------|-----------|-----------|
| Parse CSV and generate report | basic | Pure local processing |
| Fetch GitHub issues | api-wrapper | GitHub API is HTTP-accessible |
| Query internal wiki via MCP | mcp-bridge | MCP required, need pagination |
| Send Slack message | api-wrapper | Slack API is HTTP-accessible |
| Access enterprise system behind SSO | mcp-bridge | Auth boundary requires MCP |

## When NOT to Use Skill Forge

Not everything needs to be a skill:

- **Quick one-off transformations** — just write the code inline
- **Conversational Q&A** — no persistent artifacts needed
- **Simple chat interactions** — skill overhead not justified
- **Experimental/throwaway code** — don't formalize prematurely

## Migration Guide

### Converting MCP → api-wrapper

If you're currently using MCP for something HTTP-accessible:

1. Identify the underlying API
2. Scaffold with `--archetype api-wrapper`
3. Replace MCP calls with `requests`/`httpx`
4. Save outputs to `workspace/`
5. Test and validate

### Converting raw scripts → basic

If you have standalone scripts:

1. Scaffold with `--archetype basic`
2. Move script logic to `scripts/main.py`
3. Add `_fs.py` helpers for workspace pattern
4. Create `SKILL.md` and `skill.spec.json`
5. Validate with `validate_skill.py`
