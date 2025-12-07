#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

def run(cmd: list[str]) -> int:
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(p.stdout.rstrip())
    return p.returncode

def main() -> None:
    ap = argparse.ArgumentParser(description="Validate + scan all skills under a directory.")
    ap.add_argument("--skills-dir", default=".claude/skills", help="Directory containing skill folders")
    args = ap.parse_args()

    skills_dir = Path(args.skills_dir).expanduser().resolve()
    if not skills_dir.exists():
        raise SystemExit(f"Not found: {skills_dir}")

    failures = 0
    for skill in sorted([p for p in skills_dir.iterdir() if p.is_dir()]):
        print(f"\n=== {skill.name} ===")
        rc1 = run([sys.executable, str(Path(__file__).parent / "validate_skill.py"), str(skill)])
        run([sys.executable, str(Path(__file__).parent / "security_scan.py"), str(skill)])
        if rc1 != 0:
            failures += 1

    if failures:
        raise SystemExit(f"\n❌ Audit finished with {failures} validation failure(s).")
    print("\n✅ Audit finished (no validation failures).")

if __name__ == "__main__":
    main()
