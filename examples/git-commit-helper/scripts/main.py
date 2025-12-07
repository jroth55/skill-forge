#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from _fs import write_text, safe_preview_text

def main() -> None:
    diff = subprocess.run(["git", "diff", "--staged"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
    if not diff.strip():
        print("No staged changes. Stage files first, then rerun.")
        return

    preview = "\n".join(diff.splitlines()[:120])
    path = write_text("staged_diff_preview.txt", preview)

    print(f"✅ Saved staged diff preview to: {path}")
    print("Preview (capped):")
    print(safe_preview_text(preview, max_bytes=768))
    print("\nNext: Use this preview to write a concise commit summary line (<50 chars) and a short body (what + why).")

if __name__ == "__main__":
    main()
