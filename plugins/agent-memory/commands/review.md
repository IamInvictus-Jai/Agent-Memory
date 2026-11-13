---
description: Run the software review panel (architect, security, test-qa, simplicity, devils-advocate) in parallel on a diff, plan, or design.
---

Run the Agent-Memory review panel in parallel and synthesize the findings.

### Step 1 — Determine the target
From `$ARGUMENTS`, pick what to review:
- a path to a `memory/plans/NNNN-*.md` file → review the **plan**;
- `design` → review `memory/design.md`;
- a file path or glob → review those **files**;
- nothing given → review the **uncommitted diff** (`git diff` + `git diff --cached`); if not a git repo
  or no diff, ask the operator what to review.
State clearly what you're reviewing before launching.

### Step 2 — Gather shared context
Read `memory/STATE.md`, `memory/design.md`, and `memory/conventions.md` so every reviewer is grounded in
the project's goals, architecture, and rules. You'll pass this context to each subagent.

### Step 3 — Launch the panel in parallel
Launch these subagents **in a single message (parallel)** via the Task tool, each with: the target
content, the shared context from Step 2, and any specific concern the operator flagged.
- `architect` — design fit, boundaries, failure modes, over/under-engineering.
- `security` — input trust, secrets, authz, injection, unsafe deps.
- `test-qa` — coverage gaps, untested edge cases, how this could break.
- `simplicity` — reuse, dead code, simpler equivalents, maintainability.
- `devils-advocate` — the pre-mortem: how this ships and then fails.

(If the operator has added or removed persona files, use whatever is actually installed — don't assume a
fixed roster.)

### Step 4 — Synthesize
Collect the five reviews and produce ONE prioritized summary:
- **Blockers** (must fix before merging) with the reviewer who raised each.
- **Concerns** (should address) grouped by theme.
- **Nits** (optional).
- **Agreements/conflicts** between reviewers worth the operator's judgment.

### Step 5 — Capture
If any finding is a durable decision or a new rule/gotcha, record it (`decisions.md` / `conventions.md`).
Do not auto-apply fixes — leave that to the operator unless they ask.
