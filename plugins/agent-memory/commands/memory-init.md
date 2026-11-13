---
description: Scaffold the Agent-Memory brain into this project so the hooks activate here.
---

Scaffold the Agent-Memory brain into the current project. The plugin's hooks are already installed but
stay dormant until `memory/.memory-root` exists — this command creates it.

1. **Preflight.**
   - Confirm `python3` is on PATH.
   - Confirm you're at the project root (a `.git/`, or a package manifest). If unsure, ask.
   - If `memory/.memory-root` already exists, STOP — the brain is already scaffolded. Offer to *update*
     STATE.md instead of overwriting anything.
2. **Infer the project.** Read README, package manifest, and a sample of the source to infer the
   project's purpose, primary language, and structure. Use this to pre-fill STATE.md rather than leaving
   it blank.
3. **Copy the brain.** Copy `${CLAUDE_PLUGIN_ROOT}/scaffold/memory/` → `./memory/` (`.memory-root`,
   `STATE.md`, `decisions.md`, `design.md`, `conventions.md`, `plans/0001-example.md`). Never overwrite
   files that already exist.
4. **Fill STATE.md.** Write the inferred purpose and current status into `memory/STATE.md`; ask the
   operator to confirm the few things you couldn't infer (rules, phase). Leave the example plan for them
   to replace via `/plan`.
5. **Gitignore the flags.** Add `.claude/.agent-memory/` to `.gitignore`.
6. **Self-test — required.** Prove the hooks fire before declaring success:
   - `echo '{"cwd":"<project-root>"}' | python3 "${CLAUDE_PLUGIN_ROOT}/hooks/session_start.py"` → must
     emit JSON whose `additionalContext` contains the manual and STATE.md.
   - `mkdir -p .claude/.agent-memory && echo 1 > .claude/.agent-memory/selftest.dirty`, then
     `echo '{"cwd":"<project-root>","session_id":"selftest"}' | python3 "${CLAUDE_PLUGIN_ROOT}/hooks/stop_consolidate.py"`
     → must emit `{"decision": "block", ...}`. Remove the flag afterward.
   Report pass/fail. Do NOT claim success unless the Stop block fires.
7. **Finish.** Tell the operator the brain is live, and to **open a fresh session** so SessionStart
   injects STATE.md. Then: `/plan` to write the first plan, `/review` to run the review panel.
