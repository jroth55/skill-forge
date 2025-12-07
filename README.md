# Skill Forge

**A meta-skill for AI coding assistants to create, validate, and package production-ready Skills.**

Skill Forge enforces a "code-first" architecture where scripts handle the heavy lifting and MCP (Model Context Protocol) is used only when necessary. This results in token-efficient, secure, and maintainable AI agent skills.

---

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Quick Start](#quick-start)
- [The Three Archetypes](#the-three-archetypes)
- [The Filesystem Pattern](#the-filesystem-pattern)
- [Integration Guides](#integration-guides)
  - [Claude Code](#claude-code)
  - [Cursor AI](#cursor-ai)
  - [Windsurf](#windsurf)
  - [Cline (VS Code)](#cline-vs-code)
  - [Aider](#aider)
  - [Continue](#continue)
- [CLI Reference](#cli-reference)
- [Skill Anatomy](#skill-anatomy)
- [Security](#security)
- [License](#license)

---

## Core Philosophy

| Principle | What it means |
|-----------|---------------|
| **Code-first** | Scripts are the default. Long chains of tool calls are avoided. |
| **MCP is the special case** | Only use MCP when auth/network boundaries require it. |
| **Filesystem Pattern** | Raw data → `workspace/`. Stdout → summaries only. Never flood the context window. |
| **Least privilege** | Request only the tools you need. Confirm destructive actions. |

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

### 1. API Wrapper (Default)

Use when you can reach an external system via HTTP/SDK from your execution environment.

```
User: "Fetch my GitHub notifications"
→ Script calls GitHub API directly
→ Saves JSON to workspace/
→ Prints summary to stdout
```

### 2. Basic Logic

Use for local processing: file transforms, parsing, code generation, deterministic tasks.

```
User: "Generate a commit message from my staged diff"
→ Script runs `git diff --staged`
→ Saves preview to workspace/
→ Prints suggested message
```

### 3. MCP Bridge (Special Case)

Use only when MCP is unavoidable (OAuth, network isolation, cross-client interop) — but keep orchestration in code.

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

---

## Integration Guides

### Claude Code

Claude Code supports custom skills via the `.claude/skills/` directory.

#### Setup

1. **Copy Skill Forge to your project or a central location:**
   ```bash
   cp -r skill-forge ~/tools/skill-forge
   ```

2. **Create skills directory in your project:**
   ```bash
   mkdir -p .claude/skills
   ```

3. **Add Skill Forge as a skill itself** (meta-skill):
   
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

   Create a new skill:
   ```bash
   python ~/tools/skill-forge/scripts/forge.py --interactive
   ```

   Validate:
   ```bash
   python ~/tools/skill-forge/scripts/validate_skill.py .claude/skills/<name>
   ```

   Package:
   ```bash
   python ~/tools/skill-forge/scripts/package_skill.py .claude/skills/<name>
   ```
   ```

4. **Use it:**
   ```
   You: "Create a skill that summarizes Slack threads"
   Claude: [runs forge.py, edits template, validates, done]
   ```

#### Claude Code Project Configuration

Add to your `claude.config.json` or project instructions:

```json
{
  "skills_directory": ".claude/skills",
  "custom_instructions": "When creating new skills, always use Skill Forge (python ~/tools/skill-forge/scripts/forge.py). Follow the Filesystem Pattern: save raw data to workspace/, print only summaries."
}
```

---

### Cursor AI

Cursor uses `.cursorrules` and the composer for AI-assisted coding.

#### Setup

1. **Place Skill Forge in your workspace:**
   ```bash
   cp -r skill-forge ./tools/skill-forge
   ```

2. **Create `.cursorrules`** in your project root:
   ```markdown
   # Skill Creation Rules

   When asked to create a "skill", "agent capability", or "automation":

   1. Use Skill Forge to scaffold:
      ```bash
      python tools/skill-forge/scripts/forge.py --interactive
      ```

   2. Follow the Filesystem Pattern:
      - Save raw API responses to `workspace/`
      - Print only summaries and artifact paths to stdout
      - Never dump large JSON into the conversation

   3. Choose the right archetype:
      - **api-wrapper**: For HTTP/SDK-accessible systems (default)
      - **basic**: For local file processing, transforms, generation
      - **mcp-bridge**: Only when MCP is required (auth/network boundary)

   4. Always validate before considering done:
      ```bash
      python tools/skill-forge/scripts/validate_skill.py <skill-path>
      python tools/skill-forge/scripts/security_scan.py <skill-path>
      ```

   5. Skills go in: `.cursor/skills/` or `skills/`
   ```

3. **Add to Cursor Settings** (Preferences → Rules for AI):
   ```
   When building reusable automations, use the Skill Forge toolkit in tools/skill-forge/. 
   Always scaffold with forge.py, validate with validate_skill.py, and follow the Filesystem Pattern.
   ```

#### Usage in Cursor

```
Composer: "Build a skill that queries our Postgres database and generates reports"

Cursor will:
1. Run forge.py with archetype=api-wrapper
2. Edit wrapper.py to add psycopg2 logic
3. Update requirements.txt
4. Validate and scan
```

---

### Windsurf

Windsurf (Codeium) supports custom rules and tool configurations.

#### Setup

1. **Add Skill Forge to your workspace:**
   ```bash
   cp -r skill-forge ./tools/skill-forge
   ```

2. **Create `.windsurfrules`:**
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

   - Default to `api-wrapper` for external APIs
   - Use `basic` for local processing
   - Use `mcp-bridge` only when MCP is mandatory
   - Always implement Filesystem Pattern (workspace/ for data, stdout for summaries)
   ```

3. **Configure in Windsurf settings:**
   
   Add to your workspace configuration or AI instructions:
   ```
   Tool path: tools/skill-forge/
   Skills output: skills/
   Always validate skills before marking complete.
   ```

---

### Cline (VS Code)

Cline is a VS Code extension for AI-assisted development.

#### Setup

1. **Add Skill Forge to your project:**
   ```bash
   cp -r skill-forge ./tools/skill-forge
   ```

2. **Create `.clinerules`:**
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
      | Call external API | api-wrapper |
      | Process local files | basic |
      | Must use MCP server | mcp-bridge |

   4. **Validation Required:**
      ```bash
      python tools/skill-forge/scripts/validate_skill.py <path>
      python tools/skill-forge/scripts/security_scan.py <path>
      ```

   5. **Output Location:** `skills/` or `.cline/skills/`
   ```

3. **Add to Cline's custom instructions** (via VS Code settings):
   ```json
   {
     "cline.customInstructions": "Use Skill Forge (tools/skill-forge/) for creating any reusable skill or automation. Always scaffold, validate, and security scan."
   }
   ```

---

### Aider

Aider is a command-line AI pair programming tool.

#### Setup

1. **Add Skill Forge to your repo:**
   ```bash
   cp -r skill-forge ./tools/skill-forge
   ```

2. **Create `.aider.conf.yml`:**
   ```yaml
   # Aider configuration
   auto-commits: false
   
   # Custom conventions file
   conventions: .aider-conventions.md
   ```

3. **Create `.aider-conventions.md`:**
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
   - **api-wrapper**: HTTP APIs, SDKs, external services
   - **basic**: Local transforms, file ops, codegen
   - **mcp-bridge**: When MCP is unavoidable (rare)
   ```

4. **Usage:**
   ```bash
   aider
   > Create a skill that analyzes Python test coverage
   ```

---

### Continue

Continue is an open-source AI code assistant for VS Code and JetBrains.

#### Setup

1. **Add Skill Forge:**
   ```bash
   cp -r skill-forge ./tools/skill-forge
   ```

2. **Configure `.continue/config.json`:**
   ```json
   {
     "customCommands": [
       {
         "name": "skill",
         "description": "Create a new skill with Skill Forge",
         "prompt": "Create a new skill using Skill Forge. Scaffold with: python tools/skill-forge/scripts/forge.py --interactive. Follow the Filesystem Pattern (save raw data to workspace/, print only summaries). Validate with validate_skill.py and security_scan.py before finishing."
       }
     ],
     "systemMessage": "When creating skills or automations, use Skill Forge in tools/skill-forge/. Default to api-wrapper archetype. Always validate and security scan."
   }
   ```

3. **Create `.continue/rules.md`:**
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

4. **Usage:**
   ```
   /skill Create a skill that fetches Jira tickets
   ```

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

```yaml
---
name: my-skill-name
description: What this does + when to use it
allowed-tools: Read, Grep, Glob, Bash
metadata:
  archetype: api-wrapper
  risk_level: low
---
```

### skill.spec.json

```json
{
  "name": "my-skill-name",
  "title": "My Skill",
  "description": "What + when",
  "archetype": "api-wrapper",
  "risk_level": "low",
  "entry_point": "scripts/main.py",
  "triggers": ["fetch X", "get Y", "show Z"],
  "anti_triggers": ["delete everything", "unrelated task"],
  "acceptance_tests": ["handles empty input", "saves to workspace/"]
}
```

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
Can you reach the system via HTTP/SDK?
├── YES → api-wrapper (code-first)
└── NO
    └── Is it blocked by auth/network boundary?
        ├── YES → Do you need loops/retries?
        │   ├── YES → mcp-bridge
        │   └── NO → raw MCP (acceptable but costly)
        └── NO → basic (local processing)
```

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
