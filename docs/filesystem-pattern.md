# The Filesystem Pattern

## The problem
Tools and MCP servers can return huge payloads. If you dump that into the conversation, you:
- burn tokens
- drown the model
- recreate the worst version of “tool use”

## The solution
Treat the filesystem as **long-term memory** and the context window as **working memory**.

### Rules for scripts
1) **Never print data > 1KB to stdout.**
2) **Always save raw data to `workspace/`.**
3) **Print only summaries + artifact paths + tiny previews.**

### Bad
```python
print(big_json_blob)
```

### Good
```python
raw = fetch()
path = write_workspace("data.json", raw)
print(f"Saved {len(raw)} bytes to {path}")
print("Summary: ...")
```

## Mechanical enforcement
The archetype templates ship helper utilities that:
- always create `workspace/`
- write artifacts to disk
- cap previews to small byte limits
