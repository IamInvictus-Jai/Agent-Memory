#!/usr/bin/env python3
"""PreCompact hook: flush un-captured decisions into the memory brain before context is compacted."""
import json
import sys
from pathlib import Path

MSG = (
    "CONTEXT IS ABOUT TO COMPACT. Before older turns are summarized away, write any un-captured "
    "decisions, design choices, plan progress (check off completed steps in memory/plans/) and key "
    "facts from this session into the `memory/` files now, so nothing important is lost."
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    cwd = Path(data.get("cwd") or ".")
    if not (cwd / "memory" / ".memory-root").exists():
        return

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreCompact",
            "additionalContext": MSG,
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
