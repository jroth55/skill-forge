#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

TEXT_EXTS = {".md", ".txt", ".py", ".js", ".ts", ".sh", ".json", ".yaml", ".yml"}

PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "Private key material"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "Access key pattern"),
    (re.compile(r"\b(?:xoxb|xoxp|xoxa|xapp)-[0-9A-Za-z-]{10,}\b"), "Token-like string"),
    (re.compile(r"ignore (all|any) (previous|prior) instructions", re.I), "Prompt injection phrase"),
    (re.compile(r"system prompt", re.I), "Prompt injection phrase"),
    (re.compile(r"exfiltrat(e|ion)", re.I), "Suspicious exfiltration wording"),
    (re.compile(r"\brm\s+-rf\b"), "Destructive shell command"),
    (re.compile(r"\bmkfs\b"), "Destructive shell command"),
    (re.compile(r"\bcurl\b\s+.*\|\s*(sh|bash)\b"), "Pipe-to-shell pattern"),
    (re.compile(r"\beval\s*\(", re.I), "Dangerous eval()"),
    (re.compile(r"\bexec\s*\(", re.I), "Dangerous exec()"),
    (re.compile(r"subprocess\..*shell\s*=\s*True", re.I), "shell=True (injection risk)"),
    (re.compile(r"os\.system\(", re.I), "os.system (injection risk)"),
]

def scan_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return [f"Could not read file: {e}"]
    for pat, label in PATTERNS:
        if pat.search(text):
            issues.append(label)
    return issues

def main() -> None:
    ap = argparse.ArgumentParser(description="Heuristic security scan for a Skill folder.")
    ap.add_argument("skill_dir", help="Path to the skill folder")
    args = ap.parse_args()

    root = Path(args.skill_dir).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    findings: list[str] = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix.lower() not in TEXT_EXTS and p.name != "SKILL.md":
            continue
        for issue in scan_file(p):
            findings.append(f"{p.relative_to(root)}: {issue}")

    if not findings:
        print("✅ Security scan passed (heuristic).")
        return

    print("⚠️  Security scan findings (review required):\n")
    for f in findings:
        print(f"- {f}")
    print("\nNote: heuristic scanner. Manual review still matters.")

if __name__ == "__main__":
    main()
