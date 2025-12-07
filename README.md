# Skill Forge 2.0

**A meta-skill for AI coding assistants to create, validate, and package production-ready Skills.**

Skill Forge is a scaffold generator for building "skills" — modular pieces of functionality that can be used by AI agents or editors such as VS Code. It enforces a "code-first" architecture where Python scripts handle the heavy lifting and MCP (Model Context Protocol) is used only when necessary. This results in token-efficient, secure, and maintainable AI agent skills.

---

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Quick Start](#quick-start)
- [The Three Archetypes](#the-three-archetypes)
- [The Filesystem Pattern](#the-filesystem-pattern)
- [General Integration Guidelines](#general-integration-guidelines)
- [Integration Guides](#integration-guides)
  - [GitHub Copilot (VS Code)](#github-copilot-vs-code)
  - [Claude Code](#claude-code)
  - [Cursor](#cursor)
  - [Windsurf](#windsurf)
  - [Cline (VS Code)](#cline-vs-code)
  - [Aider](#aider)
  - [Continue](#continue)
  - [Amazon Q Developer](#amazon-q-developer)
  - [Google Gemini Code Assist](#google-gemini-code-assist)
  - [Tabnine](#tabnine)
  - [JetBrains AI Assistant](#jetbrains-ai-assistant)
  - [Sourcegraph Cody](#sourcegraph-cody)
  - [ChatGPT and Custom GPTs](#chatgpt-and-custom-gpts)
- [CLI Reference](#cli-reference)
- [Skill Anatomy](#skill-anatomy)
- [Security](#security)
- [License](#license)

---

## Core Philosophy

Understanding the Skill Forge philosophy helps you write precise instructions for AI assistants. The core idea is to save intermediate data to disk, let code handle heavy lifting and summarise results, which protects memory and avoids leaks of raw data.

| Principle | What it means |
|-----------|---------------|
| **Code-first** | Skills should be implemented as Python code. Only use an API wrapper when there is a compelling external API, and prefer the basic or bridge templates when possible. Scripts are the default; long chains of tool calls are avoided. |
| **Least privilege & safety** | Agents should use the `workspace/` folder to store raw outputs, print only concise summaries to stdout, and avoid leaking credentials. Skills must document which MCP servers they need and request only necessary read/write access. |
| **Filesystem Pattern** | Large outputs or downloaded files must be saved under `workspace/` and referenced in the summary instead of being printed directly. Raw data → `workspace/`. Stdout → summaries only. Never flood the context window. |

---

## Quick Start

```bash
# 1. Create a new skill (interactive)
python scripts/forge.py --interactive

# 2. Validate the skill
python scripts/validate_skill.py .claude/skills/<skill-name>

# 3. Security scan (heuristic)
python scripts/security_scan.py .claude/skills/<skill-name>

# 4. Package for distribution
python scripts/package_skill.py .claude/skills/<skill-name>
```

---

## The Three Archetypes

### 1. Basic Logic (Preferred Default)

Use for local processing: file transforms, parsing, code generation, deterministic tasks. **Start here unless you need external APIs.**

```
User: "Generate a commit message from my staged diff"
→ Script runs `git diff --staged`
→ Saves preview to workspace/
→ Prints suggested message
```

### 2. API Wrapper

Use when you need to reach an external system via HTTP/SDK from your execution environment.

```
User: "Fetch my GitHub notifications"
→ Script calls GitHub API directly
→ Saves JSON to workspace/
→ Prints summary to stdout
```

### 3. MCP Bridge (Special Case)

Use **only** when MCP is unavoidable (OAuth, network isolation, cross-client interop) — but keep orchestration in code.

```
User: "Search my company's internal wiki"
→ Script spawns MCP server via stdio
→ Calls tool with JSON-RPC
→ Saves result to workspace/
→ Prints summary
```

---

## The Filesystem Pattern

**Problem**: Tools can return huge payloads. Dumping them into the conversation burns tokens and drowns the model.

**Solution**: Treat the filesystem as long-term memory; the context window as working memory.

```python
# ❌ Bad
print(huge_json_blob)

# ✅ Good
path = write_workspace("data.json", huge_json_blob)
print(f"Saved {len(huge_json_blob)} bytes to {path}")
print(f"Summary: {len(results)} items found")
print(f"Preview: {results[:3]}")
```

### Rules for Scripts

1. **Never print data > 1KB to stdout.**
2. **Always save raw data to `workspace/`.**
3. **Print only summaries + artifact paths + tiny previews.**

---

## General Integration Guidelines

When integrating Skill Forge skills with any AI coding assistant:

1. **Explain the code-first workflow.** Tell the assistant to call Python functions in the skill rather than reimplementing them. Emphasise that the skill will save raw data to `workspace/` and that the assistant should summarise results.

2. **Describe the workspace pattern.** Instruct the assistant that any time it handles large data (CSV, JSON, PDFs) it should save the file under the `workspace/` directory, then refer to it in the final answer rather than embedding large content directly.

3. **Mention the required tools and privileges.** Each skill declares which MCP tools it needs in `skill.spec.json`. Remind the assistant to request only those tools (read vs. write, search, etc.) and not to call external APIs unless the skill wrapper provides it.

4. **Encourage safe output.** Ask the assistant to summarise findings, cite relevant lines or file names, and avoid exposing sensitive information. The summary should be clear but concise.

When an assistant supports persistent instructions (rules, guidelines, style guides or prompt files), create a file in the specified location and include the Skill Forge principles. When the assistant supports multiple rule types (always apply, pattern-specific, etc.), choose **Always/Always Apply** rules for the general Skill Forge philosophy and additional pattern rules for specific languages or directories.

---

## Integration Guides

### GitHub Copilot (VS Code)

VS Code's Copilot Chat supports custom instructions files which are automatically prepended to every chat session.

#### Instructions Files

Create Markdown files with the `.instructions.md` extension in `.github/instructions/`. They can include optional YAML frontmatter:

```yaml
---
applyTo: "**/*.py"
description: Skill Forge coding guidelines
---
```

#### Setup

1. **Create the instructions file:**
   
   Open Chat in VS Code → Configure Chat → Chat Instructions → New instruction file. Choose `.github/instructions/skillforge.instructions.md`:

   ```markdown
   ---
   applyTo: "**/*.py"
   description: Skill Forge coding guidelines
   ---
   
   # Skill Forge Instructions
   
   - Always call the provided Python functions rather than reimplementing them.
   - Save large outputs to the `workspace/` directory and summarise results.
   - Avoid printing raw data; provide clear, concise summaries instead.
   - Use the code-first template unless API calls are unavoidable.
   - Place large outputs in workspace/ and always summarise rather than dump raw data.
   ```

2. **For complex workflows, create custom agents:**
   
   Create `.github/agents/skillforge.agent.md`:

   ```markdown
   ---
   description: Skill Forge agent for creating and validating skills
   tools: [python, fetch, files.write]
   ---
   
   # Skill Forge Agent
   
   You create skills using Skill Forge. Follow the code-first, least-privilege guidelines.
   
   ## Workflow
   1. Scaffold with `python scripts/forge.py --interactive`
   2. Edit the generated scripts
   3. Validate with `python scripts/validate_skill.py <path>`
   4. Security scan with `python scripts/security_scan.py <path>`
   
   ## Rules
   - Save raw data to `workspace/`
   - Print only summaries to stdout
   - Never dump large JSON into the conversation
   ```

3. **Copilot will automatically apply instructions** to relevant chat sessions. You can also manually attach via Add Context → Instructions.

> **Note:** Older versions used `.github/copilot-instructions.md`. VS Code 1.102+ recommends `.instructions.md` or custom agents.

---

### Claude Code

Anthropic's Claude Code uses a persistent instruction file called `CLAUDE.md`.

#### Setup

1. **Create `CLAUDE.md`** in your project root:

   ```markdown
   # Skill Forge Guidelines
   
   ## Code-First Workflow
   - Call Python functions in the skill rather than reimplementing them
   - Use `forge.py` to generate new skills
   - Do not call external services unless the skill wrapper permits it
   
   ## Filesystem Pattern
   - Store raw outputs in `workspace/`
   - Summarise results in stdout
   - Never print data > 1KB directly
   
   ## Commands
   - Create skill: `python scripts/forge.py --interactive`
   - Validate: `python scripts/validate_skill.py <path>`
   - Security scan: `python scripts/security_scan.py <path>`
   - Package: `python scripts/package_skill.py <path>`
   
   ## Archetype Selection
   - **basic**: Local transforms, file ops, codegen (preferred default)
   - **api-wrapper**: HTTP APIs, SDKs, external services
   - **mcp-bridge**: Only when MCP is unavoidable
   ```

2. **Add as a skill itself** (optional):
   
   Create `.claude/skills/skill-forge/SKILL.md`:

   ```markdown
   ---
   name: skill-forge
   description: Create, validate, and package new Skills. Use when the user wants to build a new skill, scaffold a skill template, or audit existing skills.
   allowed-tools: Read, Write, Grep, Glob, Bash
   metadata:
     archetype: basic
     risk_level: low
   ---
   
   # Skill Forge
   
   ## Usage
   - Create: `python scripts/forge.py --interactive`
   - Validate: `python scripts/validate_skill.py .claude/skills/<name>`
   - Package: `python scripts/package_skill.py .claude/skills/<name>`
   ```

3. **Claude searches for `CLAUDE.md`** in parent and child directories and merges multiple files, so subdirectories can have additional guidelines.

---

### Cursor

Cursor is a VS Code fork with integrated AI assistance. It supports four types of rules:

- **Project rules**: Stored in `.cursor/rules/` (one `.mdc` file per rule), version-controlled
- **User rules**: Global preferences in Cursor Settings → Rules
- **Team rules**: Managed via web dashboard
- **AGENTS.md**: Simple Markdown alternative (deprecated but supported)

#### Setup

1. **Create `.cursor/rules/skillforge.mdc`:**

   ```markdown
   ---
   description: Guidelines for using Skill Forge
   alwaysApply: true
   ---
   
   # Skill Forge Rules
   
   When asked to create a "skill", "agent capability", or "automation":
   
   ## Workflow
   1. Scaffold with `python tools/skill-forge/scripts/forge.py --interactive`
   2. Follow the Filesystem Pattern:
      - Save raw API responses to `workspace/`
      - Print only summaries and artifact paths to stdout
      - Never dump large JSON into the conversation
   3. Validate: `python tools/skill-forge/scripts/validate_skill.py <path>`
   4. Security scan: `python tools/skill-forge/scripts/security_scan.py <path>`
   
   ## Archetype Selection
   - **basic**: Local processing, transforms, generation (preferred)
   - **api-wrapper**: HTTP/SDK-accessible systems
   - **mcp-bridge**: Only when MCP is required (auth/network boundary)
   ```

2. **For language-specific rules**, create additional files with globs:

   ```markdown
   ---
   description: Python skill guidelines
   globs: ["**/*.py"]
   ---
   
   # Python Skill Rules
   - Use type hints
   - Follow PEP 8
   - Save outputs to workspace/
   ```

3. **Alternative: Use `AGENTS.md`** at the project root with similar content.

4. **Or define User Rules** via Cursor Settings → Rules for global preferences.

#### Rule Types

| Type | When Applied |
|------|--------------|
| Always Apply | Every chat session |
| Apply Intelligently | Agent decides based on description |
| Apply to Specific Files | Matches glob patterns |
| Apply Manually | Invoked with `@rule:` or `#rule:` |

---

### Windsurf

Windsurf (Codeium) supports custom rules and tool configurations.

#### Setup

1. **Create `.windsurfrules`:**

   ```markdown
   # Skill Development Standards
   
   ## Creating New Skills
   
   Use Skill Forge for all skill/automation creation:
   
   ```bash
   # Scaffold
   python tools/skill-forge/scripts/forge.py \
     --name <skill-name> \
     --title "<Human Title>" \
     --description "<what + when>" \
     --archetype <api-wrapper|basic|mcp-bridge>
   
   # Validate
   python tools/skill-forge/scripts/validate_skill.py skills/<name>
   
   # Security check
   python tools/skill-forge/scripts/security_scan.py skills/<name>
   ```
   
   ## Architecture Rules
   
   - Default to `basic` for local processing
   - Use `api-wrapper` for external APIs
   - Use `mcp-bridge` only when MCP is mandatory
   - Always implement Filesystem Pattern (workspace/ for data, stdout for summaries)
   ```

---

### Cline (VS Code)

Cline is a VS Code extension for AI-assisted development.

#### Setup

1. **Create `.clinerules`:**

   ```markdown
   # Cline Project Rules
   
   ## Skill Development
   
   When creating automations, agents, or skills:
   
   1. **Scaffold with Skill Forge:**
      ```bash
      python tools/skill-forge/scripts/forge.py --interactive
      ```
   
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
      ```bash
      python tools/skill-forge/scripts/validate_skill.py <path>
      python tools/skill-forge/scripts/security_scan.py <path>
      ```
   ```

2. **Add to VS Code settings:**

   ```json
   {
     "cline.customInstructions": "Use Skill Forge for creating any reusable skill or automation. Always scaffold, validate, and security scan. Save raw data to workspace/, print only summaries."
   }
   ```

---

### Aider

Aider is a command-line AI pair programming tool.

#### Setup

1. **Create `.aider.conf.yml`:**

   ```yaml
   auto-commits: false
   conventions: .aider-conventions.md
   ```

2. **Create `.aider-conventions.md`:**

   ```markdown
   # Project Conventions
   
   ## Skill Development
   
   When asked to create a skill, automation, or agent capability:
   
   ### Step 1: Scaffold
   ```bash
   python tools/skill-forge/scripts/forge.py \
     --name <lowercase-hyphenated> \
     --title "<Human Readable>" \
     --description "<what it does + when to use>" \
     --archetype <api-wrapper|basic|mcp-bridge> \
     --output-dir skills/
   ```
   
   ### Step 2: Implement
   Edit the generated `scripts/` files. Follow Filesystem Pattern:
   - Save data to `workspace/`
   - Print summaries to stdout
   - Cap previews to 512 bytes
   
   ### Step 3: Validate
   ```bash
   python tools/skill-forge/scripts/validate_skill.py skills/<name>
   python tools/skill-forge/scripts/security_scan.py skills/<name>
   ```
   
   ### Archetype Guide
   - **basic**: Local transforms, file ops, codegen (preferred)
   - **api-wrapper**: HTTP APIs, SDKs, external services
   - **mcp-bridge**: When MCP is unavoidable (rare)
   ```

---

### Continue

Continue is an open-source AI code assistant for VS Code and JetBrains.

#### Setup

1. **Configure `.continue/config.json`:**

   ```json
   {
     "customCommands": [
       {
         "name": "skill",
         "description": "Create a new skill with Skill Forge",
         "prompt": "Create a new skill using Skill Forge. Scaffold with: python tools/skill-forge/scripts/forge.py --interactive. Follow the Filesystem Pattern (save raw data to workspace/, print only summaries). Validate with validate_skill.py and security_scan.py before finishing."
       }
     ],
     "systemMessage": "When creating skills or automations, use Skill Forge. Default to basic archetype. Always validate and security scan. Save raw data to workspace/, print only summaries."
   }
   ```

2. **Create `.continue/rules.md`:**

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

3. **Usage:** `/skill Create a skill that fetches Jira tickets`

---

### Amazon Q Developer

Amazon Q Developer (formerly AWS CodeWhisperer) allows project rules in Markdown files under `.amazonq/rules/`.

#### Setup

1. **Create `.amazonq/rules/skillforge.md`:**

   ```markdown
   # Skill Forge Guidelines
   
   ## Philosophy
   - Code-first: implement skills as Python code
   - Save large outputs under `workspace/`
   - Summarise results in stdout, never dump raw data
   
   ## Workflow
   1. Scaffold: `python scripts/forge.py --interactive`
   2. Implement the generated scripts
   3. Validate: `python scripts/validate_skill.py <path>`
   4. Security scan: `python scripts/security_scan.py <path>`
   
   ## Archetypes
   - **basic**: Local processing (preferred default)
   - **api-wrapper**: External API access
   - **mcp-bridge**: MCP required (rare)
   ```

2. **Rules are automatically loaded** when you chat with Q in your IDE.

3. **Optionally centralise rules** in a shared Git repository and reference them across projects.

---

### Google Gemini Code Assist

Google's Gemini Code Assist reads project instructions from a `.gemini/` directory.

#### Setup

1. **Create `.gemini/instructions.md`:**

   ```markdown
   # Project Context
   
   This project uses Skill Forge for creating AI agent skills.
   
   # Coding Standards
   
   - Follow PEP 8 for Python
   - Use type hints
   - Require docstrings
   
   # Architecture
   
   - Code-first: prefer Python scripts over tool chains
   - Save raw outputs to `workspace/`
   - Print only summaries to stdout (< 1KB)
   
   # Skill Creation Workflow
   
   1. Scaffold: `python scripts/forge.py --interactive`
   2. Validate: `python scripts/validate_skill.py <path>`
   3. Security scan: `python scripts/security_scan.py <path>`
   
   # Important Notes
   
   - Never print large JSON blobs
   - Use basic archetype unless external API is required
   - MCP bridge is the last resort
   ```

2. **Create `.gemini/styleguide.md`** for code review rules:

   ```markdown
   # Style Guide
   
   - Maximum line length: 100
   - Indentation: 4 spaces
   - Imports: stdlib, third-party, local (separated by blank lines)
   - Naming: snake_case for functions/variables, PascalCase for classes
   - Type hints required for function signatures
   ```

3. **Create `.gemini/config.yaml`** to configure indexing:

   ```yaml
   # Exclude large data files from context
   exclude:
     - workspace/**
     - "*.json"
   ```

---

### Tabnine

Tabnine supports guidelines stored in `.tabnine/guidelines/` (one or more Markdown files, max 500 lines each).

#### Setup

1. **Create `.tabnine/guidelines/skillforge-guidelines.md`:**

   ```markdown
   # Skill Forge Guidelines
   
   ## Code-First Approach
   - Implement skills as Python scripts
   - Call functions in the skill rather than reimplementing them
   - Save raw data to `workspace/`
   
   ## Workspace Pattern
   - Large data (CSV, JSON, PDFs) → save under `workspace/`
   - Refer to files in the answer, don't embed content
   - Summaries only in stdout
   
   ## Example: Saving a CSV
   ```python
   path = write_workspace("results.csv", csv_data)
   print(f"Saved {len(rows)} rows to {path}")
   print(f"Columns: {', '.join(columns)}")
   ```
   
   ## Workflow
   1. `python scripts/forge.py --interactive`
   2. Edit scripts/
   3. `python scripts/validate_skill.py <path>`
   4. `python scripts/security_scan.py <path>`
   ```

2. **For MCP server configuration**, create `.tabnine/mcp_servers.json`:

   ```json
   {
     "servers": {
       "skill-server": {
         "command": "python",
         "args": ["scripts/mcp_server.py"],
         "env": {}
       }
     }
   }
   ```

---

### JetBrains AI Assistant

JetBrains IDEs offer an AI assistant that can be customised via project rules in `.aiassistant/rules/`.

#### Setup

1. **Create `.aiassistant/rules/skillforge-guidelines.md`:**

   ```markdown
   # Skill Forge Guidelines
   
   ## When to Apply
   Apply these rules when creating skills, automations, or agent capabilities.
   
   ## Code-First Workflow
   - Implement as Python scripts
   - Save raw outputs to `workspace/`
   - Summarise results in stdout
   
   ## Commands
   - Scaffold: `python scripts/forge.py --interactive`
   - Validate: `python scripts/validate_skill.py <path>`
   - Scan: `python scripts/security_scan.py <path>`
   
   ## Archetypes
   - basic: Local processing (default)
   - api-wrapper: External APIs
   - mcp-bridge: MCP required only
   ```

2. **Configure rule type** in Settings → Tools → AI Assistant → Rules:
   - **Always**: Applied to all chat sessions
   - **Manually**: Invoked with `@rule:` or `#rule:`
   - **By model decision**: Applied when relevant
   - **By file patterns**: Matches globs like `*.py` or `src/**`

3. **For custom prompts**, go to Tools → AI Assistant → Prompt Library and create prompts that incorporate Skill Forge instructions.

---

### Sourcegraph Cody

Sourcegraph's Cody integrates with VS Code and supports custom commands via `.vscode/cody.json`.

#### Setup

1. **Create `.vscode/cody.json`:**

   ```json
   {
     "commands": {
       "skillforge": {
         "description": "Run Skill Forge pipeline to create and validate a skill",
         "command": "python3 scripts/forge.py --interactive",
         "prompt": "You are using Skill Forge. Follow the code-first workflow: save raw outputs to workspace/ and summarise results. After scaffolding, validate with validate_skill.py and security_scan.py."
       },
       "validate-skill": {
         "description": "Validate an existing skill",
         "command": "python3 scripts/validate_skill.py",
         "prompt": "Validate the skill and report any issues found."
       }
     }
   }
   ```

2. **Usage:** Open Cody command menu (Alt + C) and type `/skillforge`.

3. **Combine with instructions files:** Create a `skillforge.instructions.md` to apply code-first guidelines to all Cody Chat sessions.

4. **Optional:** Install the Cody++ extension for a graphical interface to edit commands.

---

### ChatGPT and Custom GPTs

OpenAI's ChatGPT allows custom instructions (up to 1,500 characters) and Custom GPTs.

#### Custom Instructions

In ChatGPT settings → Personalisation → Custom Instructions:

```
When I ask you to create a "skill" or "automation":

1. Use a code-first approach - implement as Python scripts
2. Save large outputs to a workspace/ directory, not inline
3. Print only summaries (< 1KB) to stdout
4. Follow this workflow:
   - Scaffold structure with required files
   - Create SKILL.md with frontmatter (name, description, allowed-tools)
   - Create skill.spec.json with triggers and anti-triggers
   - Implement main script in scripts/

Archetypes:
- basic: Local processing (default)
- api-wrapper: External API access
- mcp-bridge: MCP required only
```

#### Custom GPT

1. **Create a Custom GPT** at chatgpt.com/gpts
2. **Upload knowledge files:** SKILL.md, skill.spec.json examples, and this README
3. **Configure instructions:**

   ```
   You are Skill Forge, an assistant that creates AI agent skills.
   
   Follow these principles:
   - Code-first: implement as Python scripts
   - Save raw data to workspace/, summarise in stdout
   - Never print large JSON blobs
   
   Use forge.py to scaffold, validate_skill.py to validate, security_scan.py to check security.
   
   Default to basic archetype. Use api-wrapper for external APIs. Use mcp-bridge only when MCP is required.
   ```

4. **Add prompt starters:**
   - "Create a skill that summarises PDF documents"
   - "Build an API wrapper skill for the GitHub API"
   - "Help me validate my existing skill"

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `python scripts/forge.py --interactive` | Scaffold a new skill interactively |
| `python scripts/forge.py --name X --title Y --description Z --archetype A` | Scaffold non-interactively |
| `python scripts/validate_skill.py <path>` | Validate structure, frontmatter, syntax |
| `python scripts/security_scan.py <path>` | Heuristic scan for credentials, dangerous patterns |
| `python scripts/package_skill.py <path>` | Create distributable zip |
| `python scripts/audit_skills.py --skills-dir <dir>` | Validate + scan all skills in directory |

### Forge Options

```
--name          Skill name (lowercase-hyphen, e.g., github-issue-fetcher)
--title         Human-readable title
--description   What + when (appears in skill discovery)
--archetype     api-wrapper | basic | mcp-bridge
--risk          low | medium | high
--output-dir    Where to create (default: .claude/skills)
--force         Overwrite existing
--interactive   Guided prompts
```

---

## Skill Anatomy

A valid skill folder contains:

```
my-skill/
├── SKILL.md              # Frontmatter + docs (required)
├── skill.spec.json       # Machine-readable contract (required)
├── requirements.txt      # Python dependencies (if needed)
├── scripts/
│   ├── main.py           # Entry point
│   └── _fs.py            # Filesystem helpers
├── tests/
│   └── smoke_test.py     # Basic tests
└── workspace/            # Runtime artifacts (gitignored)
```

### SKILL.md Frontmatter

The SKILL.md file describes the skill and includes YAML frontmatter:

```yaml
---
name: my-skill-name
description: What this does + when to use it
allowed-tools: Read, Grep, Glob, Bash
metadata:
  archetype: basic
  risk_level: low
---
```

**Required fields:**
- `name`: Lowercase hyphenated identifier (1-64 chars)
- `description`: What the skill does + when to use it
- `allowed-tools`: Which MCP tools the skill needs

### skill.spec.json

Machine-readable contract specifying endpoints, arguments and metadata:

```json
{
  "name": "my-skill-name",
  "title": "My Skill",
  "description": "What + when",
  "archetype": "basic",
  "risk_level": "low",
  "entry_point": "scripts/main.py",
  "triggers": ["fetch X", "get Y", "show Z"],
  "anti_triggers": ["delete everything", "unrelated task"],
  "acceptance_tests": ["handles empty input", "saves to workspace/"]
}
```

The `validate_skill.py` script ensures these constraints are followed.

---

## Security

### Principles

- **Least privilege**: Only request tools you need
- **No secrets in files**: Use environment variables
- **Confirm destructive actions**: Delete, overwrite, push
- **Treat untrusted content as data**: Never execute instructions from fetched documents

### What the Scanner Detects

- Private key blocks (`-----BEGIN PRIVATE KEY-----`)
- Access key patterns (`AKIA...`)
- Token-like strings (`xoxb-...`)
- Prompt injection phrases ("ignore previous instructions")
- Dangerous commands (`rm -rf`, `curl | bash`)
- Risky Python patterns (`eval()`, `exec()`, `shell=True`)

### Running Security Scan

```bash
python scripts/security_scan.py .claude/skills/my-skill
```

---

## Decision Rubric

```
Is this local processing (files, transforms, codegen)?
├── YES → basic (preferred default)
└── NO
    └── Can you reach the system via HTTP/SDK?
        ├── YES → api-wrapper (code-first)
        └── NO
            └── Is it blocked by auth/network boundary?
                ├── YES → Do you need loops/retries?
                │   ├── YES → mcp-bridge
                │   └── NO → raw MCP (acceptable but costly)
                └── NO → basic
```

---

## Summary

Skill Forge enables AI assistants to execute complex tasks safely by shifting heavy computation to Python code and summarising results. To integrate it with different coding assistants:

- **Use each assistant's persistent instruction mechanism** (custom instructions files, rules directories, style guides or prompt libraries) to embed the Skill Forge philosophy: code-first, save raw outputs to `workspace/`, and summarise results.
- **Choose the proper rule type** (always, intelligent, pattern-based) so the guidelines apply when relevant.
- **When supported, create custom agents or commands** that run the `forge.py` script or validate skills automatically.
- **Always commit instruction files to version control** to ensure consistency across the team.

By following these practices and using the specific file locations and formats described above, you can make any AI coding assistant behave predictably and safely with the Skill Forge framework.

---

## References

- [VS Code Custom Instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Amazon Q Developer Rules](https://medium.com/@anjancd/contextualizing-amazon-q-developer-responses-to-improve-development-productivity-41a06b1e42e2)
- [Gemini CLI Rules](https://dev.to/yigit-konur/complete-guide-how-to-set-ai-coding-rules-for-gemini-cli-4k70)
- [Gemini Code Assist Customization](https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github)
- [Tabnine Guidelines](https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Cursor Rules](https://cursor.com/docs/context/rules)
- [JetBrains AI Assistant Rules](https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html)
- [Sourcegraph Cody](https://sourcegraph.com/blog/cody-vscode-0-10-release)
- [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions)

---

## License

MIT License — see [LICENSE.txt](LICENSE.txt)

---

## Contributing

1. Fork and clone
2. Create a skill using Skill Forge (dogfood it!)
3. Validate and scan
4. Submit PR

---

*Built for AI assistants that build things.*
