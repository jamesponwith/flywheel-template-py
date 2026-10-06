# flywheel-template-py

Python variant of [flywheel-template](https://github.com/jamesponwith/flywheel-template):
a template repo carrying the full personal agentic flywheel —
**Intent → Build → Validate → Release → Learn** — for Python (and JAX) projects.

## Use

1. "Use this template" on GitHub, then clone.
2. Edit `name` in `pyproject.toml`; replace `main.py` / `test_main.py`.
3. `uv sync` (tooling), then `bd init`, then `tools/flywheel/setup-beads.sh`, in that order. `bd init`
   points `core.hooksPath` at its own hooks and tracks its JSONL export. The script untracks the exports,
   pushes the beads database to `refs/dolt/data` on origin, and hands `.git/hooks` to lefthook
   (agentic-flywheel ADRs 0011 and 0012). Skipping it is how a merged branch's stale export reopened closed beads.
4. Fill in `SPEC.md`. Every feature starts as a `bd` issue.

## What's inside

- `CLAUDE.md` — agent conventions: intent sources, ponytail, uv-only tooling, test style
- `SPEC.md` + `docs/adr/` — where intent lives (Intent)
- `lefthook.yml` — pre-commit: ruff format, ruff check, pytest, <10s (Build);
  pre-push: local AI review (Validate)
- `.github/workflows/pr.yml` — ruff + pytest gate, no green no merge (Validate)
- `.github/workflows/release.yml` — semver tag → GitHub Release with notes (Release)
- `.github/workflows/learn.yml` — weekly DORA-lite snapshot to `docs/dora.json`,
  reusing flywheel-template's Go collector via `go run`; label incidents `incident` (Learn)
- `.claude/settings.json` — hooks: `bd prime` on session start, ruff on stop

Public metrics for all flywheel repos: [jamesponwith.github.io/dora.html](https://jamesponwith.github.io/dora.html).

