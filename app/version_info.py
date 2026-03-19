"""Single source for displayed app version (repo VERSION file or bundled copy)."""

from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path


def _repo_root_dev() -> Path:
    # app/version_info.py -> app -> repo root
    return Path(__file__).resolve().parent.parent


@lru_cache
def get_app_version() -> str:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
        for rel in ("VERSION", "_internal/VERSION"):
            p = base / rel
            if p.is_file():
                return p.read_text(encoding="utf-8").strip()
        return "0.0.0"

    vf = _repo_root_dev() / "VERSION"
    if vf.is_file():
        return vf.read_text(encoding="utf-8").strip()
    return "0.0.0-dev"
