# CLAUDE.md

Python project built inside the personal agentic flywheel: Intent → Build → Validate → Release →
Operate → Learn.

## Before writing code (Intent)

- Read SPEC.md and the open `bd` issue for the task. No bead, no build — create one first (`bd q "..."`).
- Any feature bigger than one session gets a SPEC.md section before code.
- Decisions that would take >5 minutes to re-derive get an ADR: `docs/adr/`, ~20 lines, copy `template.md`.

## Conventions (Build)

- Ponytail active: the laziest solution that works. stdlib first.
- Tooling is `uv`: `uv run pytest`, `uv run ruff check .` — no bare pip, no manual venvs.
- No new dependency without an ADR justifying it.
- Test-first; parametrized tests (`pytest.mark.parametrize` — see `test_main.py` for the shape).
- Deliberate shortcuts get a `# ponytail:` comment naming the ceiling and the upgrade path.
- Pre-commit (lefthook) runs ruff format, ruff check, pytest — keep the whole hook under 10s.

## Commit protocol

- Small commits, imperative subject, reference the bead ID: `bd-12: add retry backoff`.
- Never bypass a failing pre-commit hook. If a gate gets skipped twice, delete it or automate it.
- Pre-push runs a local AI review (ponytail-review) — advisory findings, read them before opening the PR.
- PRs merge only on a green Validate pipeline; the human is the final approver.

## Running in production (Operate)

- `docs/slo.yml` is the contract: probe url, latency budget, and how long a
  breach must persist before it is an incident. Point `url` at the real
  deployment before enabling `.github/workflows/operate.yml`.
- Keep `healthz.py` when you replace `main.py`, and wire `healthz_response`
  into your server — it is framework-agnostic on purpose. The version it
  reports is how Learn attributes an incident to a release; set it via
  `FLYWHEEL_VERSION` at deploy time.
- Incidents are filed and closed by the shared Go prober, never by hand. If you
  find yourself opening an `incident` issue manually, the prober is
  misconfigured — fix that instead, or the DORA numbers go back to measuring
  your memory.

## Agents

- Unattended agents are bound by autonomy boundaries (agentic-flywheel ADR
  0003): branch, commit, gate, PR, comment, reserve territory — never merge,
  tag, deploy, force-push, or read secrets.
- `tools/flywheel/guard.sh check` is the kill switch. Check it before acting;
  a non-zero exit means stop immediately and silently.
- `/flywheel-next` is the unit of autonomous work: one bead, one worktree, one
  PR, then stop. "Could not finish" is a correct outcome — leave the bead open
  with a comment rather than papering over a red gate.
- `/flywheel-review` runs the three-lens panel at pre-push and records every
  finding, including rejected ones, in `.flywheel/review.jsonl`.
- Anything expected to take more than one session gets a design note in the
  bead's `--design` field first: signatures and boundaries, no prose (ADR 0008).
