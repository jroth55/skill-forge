# Architecture Decision Rubric

## The Golden Rule
**Code execution is the default. MCP is the special case.**

## Decision flow

### 1) Can you access the system via a standard SDK/HTTP/CLI *from your execution environment*?
- **YES** → Use **API Wrapper** (code-first).
  - Save raw outputs to `workspace/`.
  - Print only summaries + artifact path.
- **NO** → go to step 2.

### 2) Is the system isolated (OAuth dance, enterprise proxy, local network boundary) such that scripts cannot reach it?
- **YES** → you probably need **MCP** → go to step 3.
- **NO** → Use **Basic Logic** (local processing, CLI tools, files).

### 3) Do you need loops/conditions/retries with this tool?
- **YES** → Use **MCP Bridge** (MCP-from-code orchestration).
- **NO** → Raw MCP can be acceptable for low-frequency interactive use, but it’s still worse for token costs.

## Summary
- Convert MCP → code-first when feasible: **API Wrapper**
- Must use MCP → orchestrate in code: **MCP Bridge**
- Pure local work: **Basic Logic**
