"""Filesystem Pattern helpers.

Rules:
- write raw artifacts under workspace/
- print only small summaries/previews (never dump huge payloads to stdout)
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Tuple

WORKSPACE_DIR = Path("workspace")

def ensure_workspace() -> Path:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    return WORKSPACE_DIR

def write_text(filename: str, text: str) -> Path:
    ensure_workspace()
    path = WORKSPACE_DIR / filename
    path.write_text(text, encoding="utf-8")
    return path

def write_json(filename: str, obj: Any) -> Path:
    ensure_workspace()
    path = WORKSPACE_DIR / filename
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return path

def safe_preview_text(text: str, max_bytes: int = 512) -> str:
    b = text.encode("utf-8", errors="replace")
    if len(b) <= max_bytes:
        return text
    cut = b[:max_bytes]
    return cut.decode("utf-8", errors="ignore") + "…"

def safe_preview_json(obj: Any, max_bytes: int = 512) -> str:
    s = json.dumps(obj, ensure_ascii=False, indent=2)
    return safe_preview_text(s, max_bytes=max_bytes)
