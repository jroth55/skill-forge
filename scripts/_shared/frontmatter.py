from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

FRONTMATTER_DELIM = re.compile(r"^---\s*$")

ALLOWED_TOP_LEVEL_KEYS = {"name", "description", "allowed-tools", "license", "metadata"}

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
RESERVED = {"anthropic", "claude"}
XML_TAG_RE = re.compile(r"<[^>]+>")

@dataclass
class Frontmatter:
    data: Dict[str, str]
    start_line: int
    end_line: int

def _strip_quotes(s: str) -> str:
    s = s.strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return s[1:-1]
    return s

def extract_frontmatter(md_text: str) -> Optional[Frontmatter]:
    lines = md_text.splitlines()
    if not lines or not FRONTMATTER_DELIM.match(lines[0]):
        return None

    end = None
    for i in range(1, len(lines)):
        if FRONTMATTER_DELIM.match(lines[i]):
            end = i
            break
    if end is None:
        return None

    fm_lines = lines[1:end]
    data: Dict[str, str] = {}

    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        raw = line.rstrip("\n")
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue

        # Top-level key line must not be indented
        if raw.startswith((" ", "\t")):
            i += 1
            continue

        m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", raw)
        if not m:
            i += 1
            continue

        key = m.group(1)
        rest = m.group(2) or ""
        rest_stripped = rest.strip()

        # Multiline scalar indicators: |, >, with optional modifiers
        if rest_stripped.startswith("|") or rest_stripped.startswith(">"):
            indicator = rest_stripped  # e.g., "|", ">-"
            block: List[str] = []
            i += 1
            while i < len(fm_lines):
                nxt = fm_lines[i]
                if nxt.startswith((" ", "\t")):
                    # Remove one indentation level (1+ spaces) but preserve relative indentation
                    block.append(nxt.lstrip(" \t"))
                    i += 1
                    continue
                # Next top-level key or end
                break

            if indicator.startswith("|"):
                value = "\n".join(block).rstrip("\n")
            else:
                # Folded: join non-empty lines with spaces; preserve blank lines as newlines.
                out_parts: List[str] = []
                pending_blank = False
                for b in block:
                    if not b.strip():
                        out_parts.append("\n")
                        pending_blank = True
                        continue
                    if out_parts and not out_parts[-1].endswith("\n"):
                        out_parts.append(" ")
                    out_parts.append(b.strip())
                    pending_blank = False
                value = "".join(out_parts).strip()
            data[key] = value
            continue

        # Normal scalar (single line)
        data[key] = _strip_quotes(rest_stripped)
        i += 1

    return Frontmatter(data=data, start_line=0, end_line=end)

def validate_frontmatter(data: Dict[str, str]) -> List[str]:
    errors: List[str] = []

    unknown = set(data.keys()) - ALLOWED_TOP_LEVEL_KEYS
    if unknown:
        errors.append(f"Unknown frontmatter keys: {sorted(unknown)}. Allowed: {sorted(ALLOWED_TOP_LEVEL_KEYS)}")

    name = (data.get("name") or "").strip()
    if not name:
        errors.append("Missing required frontmatter field: name")
    else:
        if not NAME_RE.match(name):
            errors.append("Invalid name. Must match ^[a-z0-9-]{1,64}$")
        if XML_TAG_RE.search(name):
            errors.append("Invalid name: must not contain XML tags")
        lowered = name.lower()
        if any(r in lowered for r in RESERVED):
            errors.append('Invalid name: must not contain reserved words "anthropic" or "claude"')

    desc = (data.get("description") or "").strip()
    if not desc:
        errors.append("Missing required frontmatter field: description")
    else:
        if len(desc) > 1024:
            errors.append("Description too long (>1024 characters)")
        if XML_TAG_RE.search(desc):
            errors.append("Invalid description: must not contain XML tags")

    return errors

def parse_allowed_tools(value: str) -> List[str]:
    raw = (value or "").strip()
    if not raw:
        return []
    raw = raw.strip("[]")
    return [p.strip() for p in raw.split(",") if p.strip()]
