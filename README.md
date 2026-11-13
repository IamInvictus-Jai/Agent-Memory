# Agent-Memory

A **Claude-Code-first persistent memory brain** for software projects, packaged as a single installable
plugin. Every chat session — planning or coding — starts with full context (what you're building, the
decisions, the design, the live implementation plan) without you re-explaining it. Capture is automatic,
enforced by hooks, not something you have to ask for.

Built for how many developers work: **one session to discuss / plan / design (no code), separate sessions
to build.** Builder sessions read exactly what the planning session decided, so they ship what you planned.

## Install (from GitHub)

```
/plugin marketplace add <your-username>/agent-memory
/plugin install agent-memory@agent-memory
```

Then, in any project you want memory for:

```
/memory-init
```

`/memory-init` scaffolds the `memory/` brain into the repo. The plugin's hooks are installed globally but
**stay dormant until a project has `memory/.memory-root`** — so they activate only where you've scaffolded.
Open a fresh session afterward so the brain is injected.

## What you get

- **Single quick-context file** — `memory/STATE.md`, injected at every session start. No re-explaining.
- **Tracked implementation plans** — `memory/plans/NNNN-*.md`, phases → checkbox steps with acceptance
  criteria. `/plan` writes them; coding sessions check steps off. The persistent plan *is* your build log.
- **Automatic capture** — decisions, design, and plan progress are written to `memory/` as you work.
- **Enforced consolidation** — the Stop hook blocks turn-end until the brain is updated + committed, so
  STATE stays current even if you leave mid-chat. PreCompact flushes before a long session compacts.
- **Parallel review panel** — `/review` runs five software reviewers (architect, security, test-qa,
  simplicity, devils-advocate) as subagents on a diff/plan/design and synthesizes their findings.

## Layout

```
agent-memory/                              ← marketplace repo
├── .claude-plugin/marketplace.json
└── plugins/agent-memory/                  ← the plugin
    ├── .claude-plugin/plugin.json
    ├── MANUAL.md                          ← operating rules, injected at SessionStart
    ├── hooks/
    │   ├── hooks.json                     ← wires the 4 hooks (CLAUDE_PLUGIN_ROOT)
    │   ├── session_start.py               ← injects MANUAL + STATE
    │   ├── track_activity.py              ← flags the session dirty on file changes
    │   ├── stop_consolidate.py            ← blocks turn-end until consolidated + committed
    │   └── pre_compact.py                 ← flush before context compacts
    ├── commands/{memory-init,plan,sync,review}.md
    ├── agents/{architect,security,test-qa,simplicity,devils-advocate}.md
    ├── skills/agent-memory/SKILL.md
    └── scaffold/memory/                   ← the brain template /memory-init copies in
        ├── .memory-root
        ├── STATE.md
        ├── decisions.md
        ├── design.md
        ├── conventions.md
        └── plans/0001-example.md
```

## The memory brain (in your project)

```
memory/
  STATE.md         ← quick-context, auto-loaded every session (read first)
  plans/           ← tracked implementation plans
  decisions.md     ← append-only decision log
  design.md        ← architecture & data model
  conventions.md   ← rules, patterns, never-do
```

## Requirements
- Claude Code with plugin support.
- `python3` on PATH (the hooks are Python, stdlib only — no dependencies).

## License
MIT
