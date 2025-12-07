# ChatGPT and Custom GPTs

OpenAI's ChatGPT supports custom instructions and Custom GPTs for persistent context.

## Quick Reference

| Item | Value |
|------|-------|
| **Custom instructions** | Settings → Personalization → Custom Instructions |
| **Custom GPTs** | chatgpt.com/gpts |
| **Instruction limit** | ~1,500 characters |
| **Official docs** | [ChatGPT Custom Instructions](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions) |

## Option 1: Custom Instructions

In ChatGPT settings → Personalization → Custom Instructions:

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

Always validate before considering complete.
```

## Option 2: Custom GPT

### 1. Create the GPT

Go to chatgpt.com/gpts and create a new GPT.

### 2. Upload Knowledge Files

Upload these files as knowledge:
- `SKILL.md` (example)
- `skill.spec.json` (example)
- `README.md` from Skill Forge

### 3. Configure Instructions

```
You are Skill Forge, an assistant that creates AI agent skills.

Follow these principles:
- Code-first: implement as Python scripts
- Save raw data to workspace/, summarize in stdout
- Never print large JSON blobs

Use forge.py to scaffold, validate_skill.py to validate, security_scan.py to check security.

Default to basic archetype. Use api-wrapper for external APIs. Use mcp-bridge only when MCP is required.

When creating a skill:
1. Ask clarifying questions about what the skill should do
2. Propose an archetype with reasoning
3. Generate the required files
4. Explain how to validate and test
```

### 4. Add Prompt Starters

- "Create a skill that summarizes PDF documents"
- "Build an API wrapper skill for the GitHub API"
- "Help me validate my existing skill"

## Notes

- Custom instructions apply to all conversations
- Custom GPTs can have uploaded knowledge and specific capabilities
- GPTs can be shared publicly or kept private
- See [Key Guidelines for Writing Instructions](https://help.openai.com/en/articles/9358033-key-guidelines-for-writing-instructions-for-custom-gpts) for best practices
