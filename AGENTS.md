# RIG Communications V10 — Agent Notes

Load the full protocol before any communication work:
```bash
cat docs/PROTOCOL.md docs/FORMULAS.md docs/GATES.md
```

## Core Protocol Rules

- Every communication follows Wound → Mirror → Autonomy → Qualification → Open Loop.
- Score every artifact against CommRawScore before shipping.
- Banned phrases trigger automatic BLOCK: "just checking in", "following up", "touching base", "would love to chat", "let me know your thoughts", "happy to help", "hope this finds you well", "I wanted to reach out", "quick question", exclamation marks.
- For LinkedIn posts, run 8-persona prediction swarm (consensus > 0.65).
- For flagship content, use 5-agent ensemble: EminemDensity, HemingwayCompression, DidionCadence, McCarthyRhythm, WallaceRecursion.
- Ship max BDF30 draft. Only swarm the winner.
- Track Brier accuracy per persona. Recalibrate weights quarterly.
- Never ship without passing all universal hard gates.
- Never commit secrets, tokens, cookies, browser state, or private credential files.
- Evidence-cite all claims. If the claim can't be backed by Consensus-level research, don't make it.

---

## Agent Roles

Four agent roles apply to all work in this repo. All roles are advisory unless a sealed DoneContract authorizes implementation.

### Planner
- **Model**: Claude Sonnet or GPT-4o
- **Responsibility**: Break issue into atomic tasks. Write DoneContracts. Identify blockers.
- **Must not**: Implement features or ship communications without DoneContract.

### Drafter
- **Model**: Claude Sonnet or GPT-4.1
- **Responsibility**: Generate communication artifacts (emails, LinkedIn posts, replies). Generate code for new engines.
- **Must not**: Score its own output (use Reviewer). Commit without gate check.

### Reviewer
- **Model**: Claude Opus or GPT-4o
- **Responsibility**: Score artifacts with `python3 src/cli.py score`. Run gate checks with `python3 src/cli.py gates`. Block shipment if any gate fails.
- **Must not**: Override a gate block without human approval.

### QA
- **Model**: Claude Haiku or GPT-4.1-mini
- **Responsibility**: Run `python3 -m pytest tests/ -v`. Run `python3 src/cli.py smoke`. Report exit codes.
- **Must not**: Modify tests to make them pass. Modify gate thresholds.

---

## First Smoke Command (deterministic proof)

```bash
python3 src/cli.py smoke
# Expected output: SMOKE: ALL PASS ✓ (exit 0)
```

All agents must verify this passes before claiming work is complete.

---

## Quality Gates (hard gates — no exceptions)

| Gate | Threshold | Engine |
|------|-----------|--------|
| CommRawScore | >= 0.65 | `src/scoring.py` |
| AutonomyPreservation | >= 0.70 | `src/gates.py` |
| AntiGenericForce | >= 0.80 | `src/gates.py` |
| No banned phrases | 0 found | `src/gates.py` |
| EthicalRestraint | >= 0.70 | `src/gates.py` |
| ReactanceRisk | <= 0.20 | `src/gates.py` |
| EntropyRatio | >= 1.2 | `src/gates.py` |
| SwarmConsensus (LinkedIn) | >= 0.65 | `src/swarm.py` |
| All pytest tests | 34/34 pass | `tests/test_smoke.py` |

---

## Weekly Improvement Loop

**Runs automatically (no human approval needed):**
- `pytest tests/` on every PR
- `python3 src/cli.py smoke` on every PR

**Never runs without human approval:**
- Sending any real communication
- Changing gate thresholds (requires evidence + DoneContract)
- Recalibrating Brier weights (V14 feature)
- Deploying, publishing, or activating any new schedule
- Opening new issues or PRs on behalf of a human

**Weekly review (human-gated):**
1. CI runs on schedule: check `scores/examples.json` for formula drift
2. Human reviews weekly summary
3. Human approves any threshold change via DoneContract
4. Agent implements → human merges

---

## MCP Surface

Designed. Not yet implemented. See `docs/MCP.md` for the full surface.

5 tools: `score_communication`, `check_gates`, `compute_idp`, `run_prediction_swarm`, `scan_banned_phrases`

---

## Design Reference

See `docs/V10_DESIGN.md` for the complete 10-lens design including proof paths,
blocker list, and KPI scorecard.
