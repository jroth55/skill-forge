from __future__ import annotations

from pathlib import Path
import shutil

def safe_rmtree(path: Path) -> None:
    # Best-effort delete. Never follow symlinks.
    if not path.exists():
        return
    if path.is_symlink():
        path.unlink()
        return
    shutil.rmtree(path)
