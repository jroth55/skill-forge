# The Filesystem Pattern

## The Problem

Tools and MCP servers can return huge payloads. If you dump that into the conversation, you:

- **Burn tokens** — large responses consume context window budget
- **Drown the model** — too much data degrades reasoning quality
- **Create poor UX** — users see walls of JSON instead of useful summaries

## The Solution

Treat the filesystem as **long-term memory** and the context window as **working memory**.

```
┌─────────────────┐     ┌─────────────────┐
│   Raw Data      │     │   Summary       │
│   (workspace/)  │     │   (stdout)      │
│                 │     │                 │
│  - Full JSON    │     │  - Item count   │
│  - Downloaded   │     │  - File path    │
│    files        │     │  - Preview      │
│  - Large blobs  │     │    (< 512 bytes)│
└─────────────────┘     └─────────────────┘
     Long-term              Working
     Memory                 Memory
```

## Rules for Scripts

1. **Never print data > 1KB to stdout**
2. **Always save raw data to `workspace/`**
3. **Print only: summaries + artifact paths + tiny previews**

## Examples

### ❌ Bad

```python
response = api.fetch_all_items()
print(json.dumps(response, indent=2))  # Could be megabytes!
```

### ✅ Good

```python
from _fs import write_json, safe_preview_json

response = api.fetch_all_items()
path = write_json("items.json", response)

print(f"✅ Saved {len(response['items'])} items to {path}")
print(f"Preview: {safe_preview_json(response['items'][:2], max_bytes=512)}")
```

## The workspace/ Directory

Each skill owns a `workspace/` directory at its root:

```
my-skill/
├── scripts/
├── workspace/          ← Runtime artifacts go here
│   ├── items.json
│   ├── report.csv
│   └── downloaded.pdf
└── ...
```

### Rules

| Rule | Rationale |
|------|-----------|
| **Must be gitignored** | Contains runtime data, not source code |
| **Scripts should create it** | Use the `_fs.py` helper or `mkdir -p` |
| **Never read/write outside** | Keeps skills self-contained |
| **Clean up old files** | Implement retention policy if needed |

## Helper Utilities

The archetype templates include `_fs.py` with these helpers:

```python
from _fs import (
    write_json,         # Save dict/list as JSON
    write_text,         # Save string as text file
    safe_preview_json,  # JSON preview capped to N bytes
    safe_preview_text,  # Text preview capped to N bytes
)
```

### Usage

```python
# Save and summarize
path = write_json("results.json", data)
print(f"Saved to {path}")
print(safe_preview_json(data, max_bytes=512))
```

## Why This Matters

| Without Filesystem Pattern | With Filesystem Pattern |
|---------------------------|------------------------|
| 50KB JSON in context | 200 bytes summary |
| Model struggles to reason | Model focuses on task |
| User scrolls through data | User sees actionable info |
| Repeated fetches | Data persisted for reuse |

## Integration with AI Assistants

When configuring AI assistants (Copilot, Cursor, Claude, etc.), always include:

> "Save raw data to `workspace/`. Print only summaries to stdout. Never dump large JSON into the conversation."

This single instruction dramatically improves skill behavior.
