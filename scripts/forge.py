#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict

from _shared.templating import copy_template_tree
from _shared.safe_delete import safe_rmtree

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")

ARCHETYPES = {
    "api-wrapper": {
        "title": "API Wrapper (default)",
        "entry_point": "scripts/wrapper.py",
        "default_requires": True,
    },
    "basic": {
        "title": "Basic Logic",
        "entry_point": "scripts/main.py",
        "default_requires": False,
    },
    "mcp-bridge": {
        "title": "MCP Bridge (special case)",
        "entry_point": "scripts/bridge.py",
        "default_requires": True,
    },
}

def ask(prompt: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or (default or "")

def slugify(title: str) -> str:
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    return s[:64] if s else s

def pick_archetype() -> str:
    print("\nSelect archetype:")
    opts = list(ARCHETYPES.keys())
    for idx, k in enumerate(opts, start=1):
        print(f"  {idx}) {ARCHETYPES[k]['title']}  ({k})")
    choice = ask("Choice [1-3]", "1")
    try:
        i = int(choice)
        if 1 <= i <= len(opts):
            return opts[i - 1]
    except Exception:
        pass
    if choice in ARCHETYPES:
        return choice
    return "api-wrapper"

def pick_risk() -> str:
    risk = ask("Risk level (low/medium/high)", "low").lower().strip()
    return risk if risk in {"low","medium","high"} else "low"

def allowed_tools_for(risk: str) -> str:
    # "Least privilege" is limited by reality: if Bash is allowed, files can be changed.
    # Still, we avoid advertising unnecessary tools.
    base = ["Read", "Grep", "Glob", "Bash"]
    if risk in {"medium", "high"}:
        base.append("Write")
    return ", ".join(base)

def main() -> None:
    ap = argparse.ArgumentParser(description="Skill Forge: scaffold a new Skill folder using archetypes.")
    ap.add_argument("--name", help="Skill name (lowercase-hyphen). If omitted, interactive mode will ask.")
    ap.add_argument("--title", help="Human-friendly title (used in docs).")
    ap.add_argument("--description", help="Description (what + when).")
    ap.add_argument("--archetype", choices=list(ARCHETYPES.keys()), help="Which archetype to generate.")
    ap.add_argument("--risk", choices=["low","medium","high"], help="Risk level.")
    ap.add_argument("--output-dir", default=".claude/skills", help="Where to create the skill folder")
    ap.add_argument("--force", action="store_true", help="Overwrite if the folder already exists")
    ap.add_argument("--interactive", action="store_true", help="Interactive mode (recommended)")
    args = ap.parse_args()

    interactive = args.interactive or (not args.title and not args.name)

    title = args.title or ""
    name = args.name or ""
    description = args.description or ""
    archetype = args.archetype or ""
    risk = args.risk or ""

    if interactive:
        print("⚔️  Skill Forge: Create New Skill\n")
        title = ask("Skill Title (human)", title or "My New Skill")
        name = ask("Skill Name (lowercase-hyphen). Leave blank to auto-slugify", name or "")
        if not name:
            name = slugify(title)
        description = ask("Description (What + When)", description or "Do X when the user asks for Y")
        archetype = pick_archetype()
        risk = pick_risk()
    else:
        if not name:
            if not title:
                raise SystemExit("Provide --name or --title (or use --interactive).")
            name = slugify(title)
        if not title:
            title = name.replace("-", " ").title()
        if not description:
            raise SystemExit("Provide --description (or use --interactive).")
        if not archetype:
            archetype = "api-wrapper"
        if not risk:
            risk = "low"

    if not NAME_RE.match(name):
        raise SystemExit("Invalid name. Must match ^[a-z0-9-]{1,64}$")

    out_root = Path(args.output_dir).expanduser()
    skill_dir = out_root / name

    if skill_dir.exists():
        if not args.force and not (interactive and ask(f"Directory {skill_dir} exists. Overwrite? (y/n)", "n").lower() == "y"):
            print("Aborted.")
            return
        safe_rmtree(skill_dir)

    skill_dir.mkdir(parents=True, exist_ok=True)

    variables: Dict[str, str] = {
        "SKILL_NAME": name,
        "SKILL_TITLE": title,
        "DESCRIPTION": description,
        "RISK_LEVEL": risk,
        "ALLOWED_TOOLS": allowed_tools_for(risk),
        "ARCHETYPE": archetype,
        "ENTRY_POINT": ARCHETYPES[archetype]["entry_point"],
    }

    template_dir = Path(__file__).parent.parent / "templates" / archetype
    copy_template_tree(template_dir, skill_dir, variables)

    spec = {
        "name": name,
        "title": title,
        "description": description,
        "archetype": archetype,
        "risk_level": risk,
        "entry_point": ARCHETYPES[archetype]["entry_point"],
        "triggers": ["TODO: add trigger 1", "TODO: add trigger 2", "TODO: add trigger 3"],
        "anti_triggers": ["TODO: add anti-trigger 1", "TODO: add anti-trigger 2"],
        "acceptance_tests": ["TODO: add acceptance test 1", "TODO: add acceptance test 2", "TODO: add acceptance test 3"],
    }
    (skill_dir / "skill.spec.json").write_text(json.dumps(spec, indent=2), encoding="utf-8")

    print(f"\n✅ Created skill '{name}' at: {skill_dir}")
    print("Next:")
    print(f"  - edit:      {skill_dir/'SKILL.md'}")
    print(f"  - validate:  python scripts/validate_skill.py {skill_dir}")
    print(f"  - package:   python scripts/package_skill.py {skill_dir}")

if __name__ == "__main__":
    main()
