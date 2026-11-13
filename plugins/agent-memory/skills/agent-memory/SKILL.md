---
name: agent-memory
description: Operate the Agent-Memory brain — a Claude-Code-first persistent memory for software projects. Read STATE.md first, capture decisions/design/plan-progress automatically, write tracked implementation plans, and run the review panel. Use when working in a project that has memory/.memory-root, or when the user asks how the memory brain works.
---

# Agent-Memory — operator skill

This project uses the Agent-Memory plugin. A persistent brain lives at `memory/` and the plugin's hooks
keep it current. The authoritative rules are in the plugin's `MANUAL.md` (injected into every session by
the SessionStart hook). This skill is the short operator reference.

## First, always
Read `memory/STATE.md`. It is the quick-context snapshot — the project's purpose, status, next step,
active plan, rules digest, and decision index. Do not ask the operator to re-explain the project.

## The files
- `memory/STATE.md` — living ~1-screen snapshot. The session entry point.
- `memory/plans/` — tracked implementation plans, steps as checkboxes.
- `memory/decisions.md` — append-only decisions (what / why / what would reverse it).
- `memory/design.md` — architecture & data model.
- `memory/conventions.md` — rules, patterns, never-do.

## Commands
- `/memory-init` — scaffold the brain into a project (first-time setup; activates the dormant hooks).
- `/plan` — write a tracked implementation plan and set it active in STATE.md.
- `/sync` — force consolidation into memory/ mid-session.
- `/review` — launch the parallel review panel (architect, security, test-qa, simplicity,
  devils-advocate) on a diff, plan, or design, then synthesize.

## Workflow
- **Planning session (no code):** discuss → `/plan` → decisions recorded → plan set active.
- **Coding session:** read the active plan + its `design_refs` → execute the next unchecked step →
  check it off → log it. If reality diverges from the plan, stop and flag it; don't silently improvise.
- **Capture is automatic:** record decisions/design/plan-progress as you work, not only when asked.
- **Session end:** the Stop hook enforces consolidation + commit on any turn that changed files.

## Reliability model
Three hooks make capture guaranteed, not advisory: SessionStart injects the manual + STATE; Stop blocks
turn-end until the brain is consolidated and committed; PreCompact flushes decisions before a long
session compacts. All hooks no-op in projects without `memory/.memory-root`.
