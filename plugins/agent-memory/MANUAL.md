# Agent-Memory — Operating Manual

This project has a persistent **memory brain** at `memory/`, maintained automatically by the
Agent-Memory plugin's hooks. It exists so every chat session — planning or coding — starts with full
context, and so decisions, design and plan progress are never lost between sessions. Maintaining it is
part of working; the operator should not have to tell you to.

## Read this first every session
`memory/STATE.md` is the quick-context snapshot, injected at the start of every session. It holds the
problem statement, current status, next step, the active plan pointer, a rules digest, and a decision
index. **Treat it as given — do not ask the operator to re-explain the project.** Open the deeper files
only when the task needs them.

## The files
- `memory/STATE.md` — living snapshot (~1 screen). The entry point for every session.
- `memory/plans/` — implementation plans, one file per plan, steps as checkboxes, tracked across sessions.
- `memory/decisions.md` — append-only log of committed choices (what / why / what would reverse it).
- `memory/design.md` — architecture, data model, key interfaces, constraints.
- `memory/conventions.md` — coding rules, patterns, "never do" list.

## Two kinds of session

**Planning / design session (no code).** Discuss, decide, architect. When you produce an implementation
plan, write it with `/plan` to `memory/plans/NNNN-<slug>.md`, set it as the Active plan in STATE.md, and
record the decisions behind it in `decisions.md`.

**Coding session.** STATE.md names the Active plan. **Read that plan file and its linked decisions/design
BEFORE writing any code.** Execute the next unchecked step exactly as specified. When a step is done,
change its `- [ ]` to `- [x]` and append a dated line to the plan's `## Log`. Ship what the plan says —
if reality forces a deviation, **stop and flag it / note it in the Log; do not silently improvise.**

## Capture is automatic, not a command — hard rule
Whenever a decision is made, an approach is chosen, a constraint or gotcha is discovered, or a plan step
is completed — capture it in the right `memory/` file as part of your response. Do not wait to be asked.

## Session-end consolidation — enforced
When a session changed files, the **Stop hook blocks the turn from ending** until you consolidate:
refresh STATE.md, check off completed plan steps, append new decisions, and commit (if git). This runs on
every turn that did real work, so STATE stays current **even if the operator leaves mid-chat.** `/sync`
forces the same consolidation mid-session.

## Plan format — memory/plans/NNNN-<slug>.md
- **Frontmatter:** `id`, `title`, `status` (draft | active | done | abandoned), `design_refs`, `created`.
- `## Goal` — what shipping this achieves + the done-definition.
- `## Constraints / decisions it implements` — links to the ADRs and principles that bind it.
- `## Steps` — grouped under `### Phase N`. Each step: `- [ ] N.M <action> — _accept: <criterion>_`.
- `## Log` — append-only, dated progress lines.
- A very large plan becomes a folder `memory/plans/NNNN-<slug>/` with `00-overview.md` + per-phase files.

Make each step precise enough that a fresh session with only STATE.md + this plan + its `design_refs` can
execute it correctly. The plan is the contract coding sessions follow.

## Review panel
`/review` launches the software review subagents (architect, security, test-qa, simplicity,
devils-advocate) in parallel against the current diff, a plan, or a design, then synthesizes their
findings. Use it before committing a risky change or before locking a plan.

## What to capture vs skip
- **Capture:** decisions, design choices, chosen approaches, constraints, gotchas, plan progress, status.
- **Skip:** trivia, restating code, anything already recorded, one-off chatter.

Keep STATE.md to about one screen — summarize and point to the detail files.
