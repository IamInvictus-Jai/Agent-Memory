#!/usr/bin/env python3
"""Stop hook: before the turn ends, consolidate the session into the memory brain.

If the session changed files (dirty flag set), block the stop once and instruct the agent to update
STATE.md, check off plan steps, append decisions, and commit. On the follow-up stop (stop_hook_active),
allow the turn to end and clear the flag. Keeps STATE current even if the operator leaves mid-chat.
"""
import json
import sys
from pathlib import Path

INSTRUCTIONS = (
    "SESSION CONSOLIDATION (Agent-Memory brain). This session changed files, so before you stop, "
    "update `memory/` so the next session has full context. Do this autonomously — no need to ask:\n"
    "1. memory/STATE.md — refresh 'Where we are now' and 'Next up', and the one-line decision index. "
    "Keep it ~1 screen; it is the single quick-context file.\n"
    "2. If an implementation plan advanced, open its file in memory/plans/, check off completed steps "
    "(`- [ ]` -> `- [x]`), and append a dated line to that plan's ## Log. If reality diverged from the "
    "plan, note the deviation — do not silently rewrite it.\n"
    "3. memory/decisions.md — append any new committed decision (what, why, what would reverse it).\n"
    "4. memory/design.md / memory/conventions.md — record durable design choices, rules or gotchas.\n"
    "Capture only durable items; skip trivia and anything already recorded. If this is a git repo, "
    "commit the memory/ changes with a short message. Then stop."
)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return

    cwd = Path(data.get("cwd") or ".")
    sid = data.get("session_id") or "default"
    dirty = cwd / ".claude" / ".agent-memory" / f"{sid}.dirty"

    # Already triggered consolidation this cycle -> let the turn end and reset.
    if data.get("stop_hook_active"):
        try:
            dirty.unlink()
        except FileNotFoundError:
            pass
        except Exception:
            pass
        return

    if not dirty.exists():
        return

    print(json.dumps({"decision": "block", "reason": INSTRUCTIONS}))


if __name__ == "__main__":
    main()
