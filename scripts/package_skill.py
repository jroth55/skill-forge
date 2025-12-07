#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

EXCLUDE_DIRS = {"__pycache__", ".git", ".svn", ".hg", "workspace"}
EXCLUDE_SUFFIXES = {".zip", ".pyc"}

def main() -> None:
    ap = argparse.ArgumentParser(description="Package a Skill folder into a shareable zip (folder at zip root).")
    ap.add_argument("skill_dir", help="Path to the skill folder")
    ap.add_argument("--out", help="Output zip path (default: <skill-name>.zip next to folder)")
    args = ap.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.exists() or not skill_dir.is_dir():
        raise SystemExit(f"Not a directory: {skill_dir}")
    if not (skill_dir / "SKILL.md").exists():
        raise SystemExit("Missing SKILL.md in skill folder")

    out = Path(args.out).expanduser().resolve() if args.out else skill_dir.with_suffix(".zip")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in skill_dir.rglob("*"):
            if p.is_dir():
                continue
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            if p.suffix in EXCLUDE_SUFFIXES:
                continue
            arcname = str(Path(skill_dir.name) / p.relative_to(skill_dir))
            zf.write(p, arcname)

    print(f"✅ Packaged: {out}")
    print(f"   Zip root folder: {skill_dir.name}/")

if __name__ == "__main__":
    main()
