# AI Coding Assistant Integrations

This directory contains setup guides for integrating Skill Forge with various AI coding assistants.

> **Note:** File paths and configuration formats are based on documentation and community practice as of December 2025. Verify against the latest tool documentation for your specific version.

## Quick Reference

| Assistant | Config Location | Docs |
|-----------|-----------------|------|
| [GitHub Copilot](./github-copilot.md) | `.github/instructions/*.instructions.md` | [Official](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) |
| [Claude Code](./claude-code.md) | `CLAUDE.md` | [Official](https://www.anthropic.com/engineering/claude-code-best-practices) |
| [Cursor](./cursor.md) | `.cursor/rules/*.mdc` | [Official](https://cursor.com/docs/context/rules) |
| [Windsurf](./windsurf.md) | `.windsurfrules` | Community practice |
| [Cline](./cline.md) | `.clinerules` | Community practice |
| [Aider](./aider.md) | `.aider-conventions.md` | [Official](https://aider.chat/docs/config.html) |
| [Continue](./continue.md) | `.continue/config.json` | [Official](https://continue.dev/docs) |
| [Amazon Q Developer](./amazon-q.md) | `.amazonq/rules/*.md` | [Official](https://docs.aws.amazon.com/amazonq/) |
| [Google Gemini](./gemini.md) | `.gemini/instructions.md` | [Official](https://developers.google.com/gemini-code-assist/docs/customize-gemini-behavior-github) |
| [Tabnine](./tabnine.md) | `.tabnine/guidelines/*.md` | [Official](https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines) |
| [JetBrains AI](./jetbrains.md) | `.aiassistant/rules/*.md` | [Official](https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html) |
| [Sourcegraph Cody](./cody.md) | `.vscode/cody.json` | [Official](https://sourcegraph.com/docs/cody) |
| [ChatGPT](./chatgpt.md) | Custom Instructions / GPTs | [Official](https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions) |

## General Integration Pattern

All integrations follow the same core pattern:

1. **Tell the assistant about Skill Forge** — what it is and when to use it
2. **Embed the workflow** — scaffold → implement → validate → scan
3. **Enforce the filesystem pattern** — raw data to `workspace/`, summaries to stdout
4. **Specify archetype selection** — basic (default) → api-wrapper → mcp-bridge

See the [main README](../../README.md) for the full philosophy and decision rubric.
