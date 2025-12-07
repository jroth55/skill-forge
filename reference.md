# Skill Forge Reference

This file is the “why” and the edge cases. Keep `SKILL.md` short.

## The non-negotiables

A Skill is “good” when it is:

- **Discoverable**: description says *what + when* with concrete triggers.
- **Focused**: one workflow. No junk drawers.
- **Deterministic where it matters**: parsing, transforms, API calls, generation in code.
- **Token-efficient**: raw data to disk, summaries to stdout.
- **Safe**: least privilege tools, no secrets in files, confirmations for risky actions.
- **Tested**: smoke prompts + at least one runnable script path.

## The Filesystem Pattern (the whole point)

- Never dump huge JSON into chat.
- Save raw outputs to `workspace/`.
- Print:
  - what was done
  - where artifacts were saved
  - a tiny preview (strictly capped)

See: [docs/filesystem-pattern.md](docs/filesystem-pattern.md)

## MCP vs code (short rubric)

Default: **code-first wrappers**.

Use **MCP** when you need:
- secret isolation (credentials must never touch the model)
- network boundary (sandbox can’t reach, MCP server can)
- cross-client interoperability
- massive tool surface with standardized discovery/schemas

Even then: prefer **MCP Bridge** so orchestration stays in code.

See: [docs/decision-rubric.md](docs/decision-rubric.md)

