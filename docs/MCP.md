# RIG Communications V10 — MCP Surface Design

## Status: DESIGNED (not yet implemented)

MCP (Model Context Protocol) implementation is deferred until V11 agent orchestration is complete. This document defines the intended surface so the design is locked and implementation can proceed without architecture debate.

---

## Why MCP?

The RIG scoring engines are deterministic and composable. They are ideal MCP tools because:
- Every tool call has a stable schema (in: text + score fields → out: float or report)
- No secrets or deployment required to run locally
- Tools can be used by any MCP-compatible agent client (Claude, Copilot, etc.)
- The gate engine is a natural pre-ship gate in any agent workflow

---

## Transport Decision

| Option | Decision |
|--------|----------|
| stdio (local) | **Default** — zero infrastructure, deterministic, safe |
| HTTP/SSE | Deferred to V12 (requires server + auth layer) |
| WebSocket | Out of scope for V10 |

The V10 MCP server runs as a local stdio server:
```bash
python3 src/mcp_server.py
```

---

## Tool Surface (5 tools)

### Tool 1: `score_communication`

Score a communication artifact against all 8 formula registry entries.

**Input schema:**
```json
{
  "text": "string — the communication text",
  "wound_precision": "float 0.0–1.0",
  "mirror_accuracy": "float 0.0–1.0",
  "autonomy_preservation": "float 0.0–1.0",
  "specificity_density": "float 0.0–1.0",
  "open_loop_residue": "float 0.0–1.0",
  "rpe_strength": "float 0.0–1.0",
  "reality_anchor": "float 0.0–1.0",
  "anti_generic_force": "float 0.0–1.0",
  "qualification_tension": "float 0.0–1.0",
  "tone_precision": "float 0.0–1.0",
  "memory_residue": "float 0.0–1.0",
  "ethical_restraint": "float 0.0–1.0"
}
```

**Output schema:**
```json
{
  "comm_raw_score": "float",
  "email_voltage_score": "float",
  "email_reply_score": "float",
  "bdf30": "float",
  "rpe": "float",
  "gate_pass": "boolean"
}
```

---

### Tool 2: `check_gates`

Run all 24 universal hard gates against a text and score object.

**Input schema:**
```json
{
  "text": "string",
  "score": "CommunicationScore fields (same as score_communication)",
  "is_linkedin": "boolean (optional, default false)",
  "swarm_consensus": "float (optional, required if is_linkedin=true)",
  "hook_rupture": "float (optional, required if is_linkedin=true)"
}
```

**Output schema:**
```json
{
  "can_ship": "boolean",
  "blocks": [{"name": "string", "message": "string"}],
  "warnings": [{"name": "string", "message": "string"}],
  "category_summary": {"sequence": "bool", "quality": "bool", ...},
  "entropy_ratio": "float",
  "reactance_risk": "float"
}
```

---

### Tool 3: `compute_idp`

Compute IdeaDeviationPotential for an angle or post concept before drafting.

**Input schema:**
```json
{
  "orthodoxy_strength": "float 0.0–1.0",
  "destruction_quality": "float 0.0–1.0",
  "replacement_clarity": "float 0.0–1.0",
  "audience_impact": "float 0.0–1.0",
  "named_entity_precision": "float 0.0–1.0",
  "proof_availability_score": "float 0.0–1.0"
}
```

**Output schema:**
```json
{
  "idp": "float",
  "classification": "string",
  "gate_pass": "boolean (idp >= 0.70)",
  "sub_scores": {"orthodoxy_destruction_depth": "float", ...}
}
```

---

### Tool 4: `run_prediction_swarm`

Run the 8-persona prediction swarm to forecast trust delta, reply probability, and consensus.

**Input schema:**
```json
{
  "artifact_summary": "string — 1–3 sentence description of the communication",
  "channel": "string — cold-email | linkedin-post | reply | proposal | dm"
}
```

**Output schema:**
```json
{
  "predicted_success": "float",
  "swarm_consensus": "float",
  "trust_decay": "boolean",
  "gate_pass": "boolean (consensus >= 0.65)",
  "persona_predictions": [{"persona": "string", "trust_delta": "float", ...}]
}
```

---

### Tool 5: `scan_banned_phrases`

Scan text for banned phrases. Safe to call at any stage.

**Input schema:**
```json
{
  "text": "string"
}
```

**Output schema:**
```json
{
  "found": ["string"],
  "clean": "boolean"
}
```

---

## Resource Surface (3 resources)

| URI | Description |
|-----|-------------|
| `rig://protocol` | Full V10 doctrine (docs/PROTOCOL.md) |
| `rig://formulas` | All 8 scoring formulas with weights |
| `rig://gates` | 24 universal hard gates with thresholds |

---

## Prompt Surface (3 prompts)

| Prompt name | Description |
|-------------|-------------|
| `score-and-gate` | Score a communication artifact and run all gates |
| `idp-tournament` | Evaluate an idea angle before drafting |
| `weekly-self-review` | Weekly quality check prompt for repo improvement loop |

---

## Intentional Deferrals

| Feature | Reason deferred |
|---------|----------------|
| HTTP transport | Requires auth layer; out of scope for V10 |
| Real swarm calls | Requires LLM API keys; V11 feature |
| Brier recalibration | Requires outcome tracking database; V14 feature |
| Ensemble writer tools | Requires 5 LLM agents; V13 feature |

---

## Implementation Path (V11)

1. Add `mcp` to `requirements.txt` (the official `mcp` Python SDK)
2. Create `src/mcp_server.py` wrapping the 5 tools above
3. Add `stdio` transport via `mcp.server.stdio`
4. Document in README: `python3 src/mcp_server.py` usage
5. Test: run MCP inspector against local server before merging

---

## Proof Command (when implemented)

```bash
# Install MCP inspector (no secrets required)
npx @modelcontextprotocol/inspector python3 src/mcp_server.py

# Verify 5 tools are listed
# Verify scan_banned_phrases returns clean: true for clean text
```
