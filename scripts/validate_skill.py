#!/usr/bin/env python3
"""Validate a Skill folder.

Checks:
1) SKILL.md frontmatter (required keys + allowed keys)
2) skill.spec.json exists and basic fields match frontmatter
3) Entry point exists
4) requirements.txt present when archetype usually needs deps (warn)
5) Python syntax checks (AST parse) for scripts/*.py
6) Basic dependency hints (warn if imports suggest missing requirements)

This is intentionally conservative and stdlib-only.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path
from typing import List, Set

from _shared.frontmatter import extract_frontmatter, validate_frontmatter, parse_allowed_tools
from _shared.imports import imported_top_levels

VALID_TOOL_NAMES = {"Read", "Write", "Grep", "Glob", "Bash"}
ARCHETYPES_REQUIRING_REQS = {"api-wrapper", "mcp-bridge"}

COMMON_THIRD_PARTY = {
    "requests": "requests>=2.31.0",
    "httpx": "httpx",
    "numpy": "numpy",
    "pandas": "pandas",
    "mcp": "mcp",
}

def check_links(skill_dir: Path, skill_md_text: str) -> List[str]:
    import re
    errors: List[str] = []
    for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", skill_md_text):
        target = m.group(1).strip()
        if "://" in target or target.startswith("#"):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        p = (skill_dir / target).resolve()
        if not p.exists():
            errors.append(f"Broken link target: {target}")
    return errors

def check_python_syntax(file_path: Path) -> List[str]:
    try:
        ast.parse(file_path.read_text(encoding="utf-8"))
        return []
    except SyntaxError as e:
        return [f"Python syntax error in {file_path.name}: {e.msg} (line {e.lineno})"]
    except Exception as e:
        return [f"Could not parse {file_path.name}: {e}"]

def load_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def read_requirements(req_path: Path) -> str:
    try:
        return req_path.read_text(encoding="utf-8")
    except Exception:
        return ""

def main() -> None:
    ap = argparse.ArgumentParser(description="Validate a Skill folder.")
    ap.add_argument("skill_dir", help="Path to the skill folder")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        raise SystemExit(f"Not a directory: {skill_dir}")

    errors: List[str] = []
    warnings: List[str] = []

    # 1) Frontmatter
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
        raise SystemExit("\n".join(errors))

    skill_text = skill_md.read_text(encoding="utf-8")
    fm = extract_frontmatter(skill_text)
    if fm is None:
        errors.append("SKILL.md must start with YAML frontmatter delimited by --- lines")
    else:
        errors.extend(validate_frontmatter(fm.data))
        allowed_raw = (fm.data.get("allowed-tools") or "").strip()
        if allowed_raw:
            tools = parse_allowed_tools(allowed_raw)
            unknown = [t for t in tools if t not in VALID_TOOL_NAMES]
            if unknown:
                errors.append(f"Unknown tool(s) in allowed-tools: {unknown}. Known: {sorted(VALID_TOOL_NAMES)}")

    errors.extend(check_links(skill_dir, skill_text))

    # 2) Spec
    spec_path = skill_dir / "skill.spec.json"
    spec = {}
    if not spec_path.exists():
        errors.append("Missing skill.spec.json")
    else:
        try:
            spec = load_spec(spec_path)
        except Exception as e:
            errors.append(f"Invalid skill.spec.json: {e}")

    # 3) Cross-check name/description where possible
    if fm and spec:
        fm_name = (fm.data.get("name") or "").strip()
        if spec.get("name") and spec["name"] != fm_name:
            warnings.append(f"skill.spec.json name '{spec['name']}' does not match SKILL.md name '{fm_name}'")
        fm_desc = (fm.data.get("description") or "").strip()
        if spec.get("description") and spec["description"] != fm_desc:
            warnings.append("skill.spec.json description differs from SKILL.md description")

    # 4) Entry point exists
    entry = (spec.get("entry_point") or "").strip()
    if entry:
        ep = (skill_dir / entry)
        if not ep.exists():
            errors.append(f"Entry point not found: {entry}")
    else:
        warnings.append("skill.spec.json missing entry_point")

    # 5) requirements.txt expectations
    archetype = (spec.get("archetype") or "").strip()
    reqs_path = skill_dir / "requirements.txt"
    if archetype in ARCHETYPES_REQUIRING_REQS and not reqs_path.exists():
        warnings.append(f"Archetype '{archetype}' typically needs requirements.txt (deps). Missing.")

    req_text = read_requirements(reqs_path) if reqs_path.exists() else ""

    # 6) Python syntax + import hints
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        imports: Set[str] = set()
        for py_file in scripts_dir.glob("*.py"):
            errors.extend(check_python_syntax(py_file))
            try:
                imports |= imported_top_levels(py_file)
            except Exception as e:
                warnings.append(f"Could not analyze imports in {py_file.name}: {e}")

        # Dependency hints (warn only)
        for mod, hint in COMMON_THIRD_PARTY.items():
            if mod in imports and hint not in req_text:
                warnings.append(f"Script imports '{mod}' but requirements.txt does not mention it (expected like: {hint})")
    else:
        warnings.append("Missing scripts/ directory")

    if errors:
        print("❌ Validation failed:\n")
        for e in errors:
            print(f"- {e}")
        if warnings:
            print("\nWarnings:")
            for w in warnings:
                print(f"- {w}")
        raise SystemExit(1)

    print("✅ Validation passed.")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"- {w}")

if __name__ == "__main__":
    main()
