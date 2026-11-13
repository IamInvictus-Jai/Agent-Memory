#!/usr/bin/env python3
"""SessionStart hook: inject the Agent-Memory operating manual + the project's STATE.md.

The manual ships with the plugin (CLAUDE_PLUGIN_ROOT) so the user's CLAUDE.md is never touched.
Both are injected only when the memory brain is scaffolded in this project (memory/.memory-root).
"""
import json
import os
import sys
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}

    cwd = Path(data.get("cwd") or ".")
    if not (cwd / "memory" / ".memory-root").exists():
        # Plugin installed but brain not scaffolded here — stay silent.
        return

    parts = []

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if plugin_root:
        manual = Path(plugin_root) / "MANUAL.md"
        if manual.exists():
            try:
                parts.append(
                    "===== Agent-Memory — Operating Manual (how to use the brain) =====\n"
                    + manual.read_text(encoding="utf-8")
                )
            except Exception:
                pass

    state = cwd / "memory" / "STATE.md"
    if state.exists():
        try:
            parts.append(
                "The quick-context snapshot below is your starting context — do NOT ask the operator "
                "to re-explain the project; it is here. If STATE names an ACTIVE plan, read that plan "
                "file under memory/plans/ (and its linked decisions/design) BEFORE writing code.\n\n"
                "===== memory/STATE.md =====\n" + state.read_text(encoding="utf-8")
            )
        except Exception:
            pass

    if not parts:
        return

    out = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n\n".join(parts),
        }
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main()
