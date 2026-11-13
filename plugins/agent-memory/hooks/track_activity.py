#!/usr/bin/env python3
"""PostToolUse hook: flag the session 'dirty' when files change, so the Stop hook consolidates."""
import json
import sys
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    cwd = Path(data.get("cwd") or ".")
    if not (cwd / "memory" / ".memory-root").exists():
        return

    sid = data.get("session_id") or "default"
    flagdir = cwd / ".claude" / ".agent-memory"
    try:
        flagdir.mkdir(parents=True, exist_ok=True)
        (flagdir / f"{sid}.dirty").write_text("1", encoding="utf-8")
    except Exception:
        pass


if __name__ == "__main__":
    main()
