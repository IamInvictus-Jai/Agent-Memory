---
description: Turn the current discussion into a tracked implementation plan under memory/plans/
---

Create a structured, trackable implementation plan from what we've discussed (and `$ARGUMENTS` if given).

1. **Pick the id.** Next plan id = highest `NNNN` in `memory/plans/` + 1, zero-padded to 4.
2. **Write `memory/plans/NNNN-<slug>.md`:**
   - Frontmatter: `id`, `title`, `status: active`, `design_refs` (links into decisions.md / design.md),
     `created` (today).
   - `## Goal` — what shipping this achieves + the done-definition.
   - `## Constraints / decisions it implements` — link the ADRs and principles that bind it.
   - `## Steps` — grouped under `### Phase N`. Each step is
     `- [ ] N.M <action> — _accept: <criterion>_`. Keep steps small and independently verifiable.
   - `## Log` — empty, append-only.
   - If the plan is very large, make a folder `memory/plans/NNNN-<slug>/` with `00-overview.md` +
     one file per phase instead of a single file.
3. **Set it active:** update `memory/STATE.md` — point "Active plan" at the new file and refresh "Next up".
4. **Record the decisions** behind the plan in `memory/decisions.md`.
5. If this is a git repo, commit.

Make each step precise enough that a fresh coding session with only STATE.md + this plan + its
`design_refs` can execute it correctly. The plan is the contract coding sessions follow.
