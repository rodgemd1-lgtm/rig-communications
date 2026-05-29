"""
RIG Communication Protocol V10 — CLI
Deterministic local commands for scoring, gate checks, and smoke tests.

Usage:
    python3 src/cli.py smoke
    python3 src/cli.py score  --text "Your message here"
    python3 src/cli.py gates  --text "Your message here"
    python3 src/cli.py idp
    python3 src/cli.py swarm
"""

from __future__ import annotations

import argparse
import json
import sys
import os

# Allow running from repo root or from src/
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from scoring import CommunicationScore, GateEngine
from formulas import (
    comm_raw_score,
    email_voltage_score,
    bdf30,
    compute_idp,
    idp_classify,
    IDPScoreInput,
    formula_registry,
)
from gates import GateEngine as FullGateEngine, compute_entropy_ratio, compute_reactance_risk
from swarm import example_swarm


# ============================================================================
# Shared fixtures
# ============================================================================

def _sarah_chen_score() -> CommunicationScore:
    """Return the canonical Sarah Chen cold-email score fixture."""
    return CommunicationScore(
        wound_precision=0.85,
        mirror_accuracy=0.90,
        autonomy_preservation=0.85,
        qualification_tension=0.80,
        specificity_density=0.88,
        open_loop_residue=0.88,
        rpe_strength=0.85,
        reality_anchor=0.90,
        anti_generic_force=0.88,
        tone_precision=0.82,
        memory_residue=0.80,
        ethical_restraint=0.92,
        stakes_clarity=0.90,
        desire_activation=0.82,
        tension_release=0.78,
        relief_clarity=0.85,
        identity_resonance=0.85,
        peak_end_memory=0.88,
        wound_identification=0.88,
        specificity=0.85,
        restraint=0.80,
        mirror_accuracy_reply=0.90,
        qualification_frame=0.82,
        open_loop_strength=0.85,
        close_quality=0.78,
        semantic_inversion=0.92,
        proof_density=0.88,
        enemy_specificity=0.90,
        catchphrase_voltage=0.85,
        structural_novelty=0.82,
        negative_space_weight=0.75,
        identity_force=0.90,
        eminem_density=0.88,
        hemingway_compression=0.85,
        didion_cadence=0.82,
        mccarthy_rhythm=0.80,
        wallace_recursion=0.86,
        catchphrase_score=0.85,
        evidence=0.90,
        rig_signature=0.88,
        artifact_completeness=0.85,
        emotional_voltage=0.82,
        mechanism_clarity=0.80,
        memory_compounding=0.78,
    )


_SARAH_CHEN_TEXT = (
    "Sarah —\n\n"
    "Your team is spending 40% of engineering hours on architecture maintenance.\n"
    "At 200 engineers, that's 80 full-time equivalents not shipping product.\n\n"
    "The real number is probably worse. Architecture tax scales nonlinearly with "
    "service count. Every new endpoint requires coordination across 4-7 services. "
    "That's not maintenance. That's an architecture actively hostile to velocity.\n\n"
    "If this is intentional — if you're betting the next round makes it manageable — "
    "ignore this. But if the 40% is creeping toward 50%, the math gets nonlinear fast.\n\n"
    "I have a hypothesis about which 3 services are causing 80% of the coupling. "
    "I'd need 15 minutes with the dependency graph to confirm it.\n\n"
    "— Mike"
)


# ============================================================================
# Commands
# ============================================================================

def cmd_smoke(_args: argparse.Namespace) -> int:
    """
    Deterministic smoke test — runs all four engines against the canonical
    Sarah Chen cold-email fixture and prints a pass/fail summary.

    Exit code: 0 if all pass, 1 if any fail.
    """
    print("=" * 60)
    print("  RIG Communications V10 — Smoke Test")
    print("=" * 60)

    failures: list[str] = []
    score = _sarah_chen_score()

    # --- Engine 1: CommRawScore ---
    crs = comm_raw_score(score)
    status = "PASS" if crs >= 0.65 else "FAIL"
    if status == "FAIL":
        failures.append(f"CommRawScore {crs:.4f} < 0.65")
    print(f"\n[scoring]  CommRawScore       {crs:.4f}  →  {status}")

    # --- Engine 2: GateEngine (full) ---
    report = FullGateEngine.check_gates(score, _SARAH_CHEN_TEXT)
    gate_status = "PASS" if report.can_ship else "FAIL"
    if not report.can_ship:
        for b in report.blocks:
            failures.append(f"Gate BLOCK: {b.name} — {b.message}")
    print(f"[gates]    can_ship           {report.can_ship!s:5}  →  {gate_status}")
    if report.blocks:
        for b in report.blocks:
            print(f"           BLOCK: {b.name} — {b.message}")

    # --- Engine 3: IDP ---
    idp_inp = IDPScoreInput(
        orthodoxy_strength=0.80, destruction_quality=0.75,
        replacement_clarity=0.70, audience_impact=0.85,
        named_entity_precision=0.90, profit_transparency=0.80,
        accountability_surface=0.85, memetic_contagion=0.78,
        measurability=0.85, stake_magnitude=0.75,
        timeline_specificity=0.70, counter_consensus=0.80,
        prior_term_familiarity=0.90, inversion_distance=0.85,
        cognitive_stickiness=0.82, domain_originality=0.88,
        pain_frequency=0.85, emotional_charge=0.80,
        invisibility=0.78, cost_quantifiability=0.72,
        copy_count_inverse=0.80, structural_originality=0.75,
        attention_advantage=0.82, phonetic_memorability=0.85,
        compression_density=0.80, cross_channel_viability=0.78,
        visual_logo_potential=0.70, academic_evidence=0.75,
        industry_data=0.70, primary_research_potential=0.68,
        anecdotal_strength=0.80, doctrine_thread_cont=0.85,
        optimal_spacing=0.78, catchphrase_recurrence=0.80,
        villain_consistency=0.88,
    )
    idp_val = compute_idp(idp_inp)
    idp_status = "PASS" if idp_val >= 0.70 else "FAIL"
    if idp_status == "FAIL":
        failures.append(f"IDP {idp_val:.4f} < 0.70")
    print(f"[formulas] IDP                 {idp_val:.4f}  →  {idp_status}  ({idp_classify(idp_val).split('—')[0].strip()})")

    # --- Engine 4: PredictionSwarm ---
    swarm = example_swarm()
    ps = swarm.predicted_success()
    sc = swarm.swarm_consensus()
    swarm_status = "PASS" if sc >= 0.65 else "FAIL"
    if swarm_status == "FAIL":
        failures.append(f"SwarmConsensus {sc:.4f} < 0.65")
    print(f"[swarm]    SwarmConsensus     {sc:.4f}  →  {swarm_status}")
    print(f"[swarm]    PredictedSuccess   {ps:.4f}")

    # --- Summary ---
    print("\n" + "=" * 60)
    if not failures:
        print("  SMOKE: ALL PASS  ✓")
        print("=" * 60)
        return 0
    else:
        print(f"  SMOKE: FAILED — {len(failures)} failure(s)")
        for f in failures:
            print(f"    • {f}")
        print("=" * 60)
        return 1


def cmd_score(args: argparse.Namespace) -> int:
    """
    Score a text against all formula registry entries.
    Uses the Sarah Chen fixture scores; pass --text for the text to gate-check.
    """
    score = _sarah_chen_score()
    print(json.dumps(
        {name: round(func(score), 4) for name, func in formula_registry.items()},
        indent=2,
    ))
    return 0


def cmd_gates(args: argparse.Namespace) -> int:
    """Run all gates against --text (or the canonical example) and print results."""
    text = args.text if args.text else _SARAH_CHEN_TEXT
    score = _sarah_chen_score()
    report = FullGateEngine.check_gates(score, text)

    out: dict = {
        "can_ship": report.can_ship,
        "blocks": [{"name": b.name, "message": b.message} for b in report.blocks],
        "warnings": [{"name": w.name, "message": w.message} for w in report.warnings],
        "category_summary": report.summary,
        "entropy_ratio": round(compute_entropy_ratio(text, "professional email regarding business services"), 4),
        "reactance_risk": round(compute_reactance_risk(text), 4),
    }
    print(json.dumps(out, indent=2))
    return 0 if report.can_ship else 1


def cmd_idp(_args: argparse.Namespace) -> int:
    """Run IDP scoring with the canonical example fixture."""
    idp_inp = IDPScoreInput(
        orthodoxy_strength=0.80, destruction_quality=0.75,
        replacement_clarity=0.70, audience_impact=0.85,
        named_entity_precision=0.90, profit_transparency=0.80,
        accountability_surface=0.85, memetic_contagion=0.78,
        measurability=0.85, stake_magnitude=0.75,
        timeline_specificity=0.70, counter_consensus=0.80,
        prior_term_familiarity=0.90, inversion_distance=0.85,
        cognitive_stickiness=0.82, domain_originality=0.88,
        pain_frequency=0.85, emotional_charge=0.80,
        invisibility=0.78, cost_quantifiability=0.72,
        copy_count_inverse=0.80, structural_originality=0.75,
        attention_advantage=0.82, phonetic_memorability=0.85,
        compression_density=0.80, cross_channel_viability=0.78,
        visual_logo_potential=0.70, academic_evidence=0.75,
        industry_data=0.70, primary_research_potential=0.68,
        anecdotal_strength=0.80, doctrine_thread_cont=0.85,
        optimal_spacing=0.78, catchphrase_recurrence=0.80,
        villain_consistency=0.88,
    )
    idp_val = compute_idp(idp_inp)
    print(json.dumps({
        "idp": round(idp_val, 4),
        "classification": idp_classify(idp_val),
        "gate_pass": idp_val >= 0.70,
    }, indent=2))
    return 0 if idp_val >= 0.70 else 1


def cmd_swarm(_args: argparse.Namespace) -> int:
    """Run the 8-persona prediction swarm on the canonical example."""
    swarm = example_swarm()
    ps = swarm.predicted_success()
    sc = swarm.swarm_consensus()
    td = swarm.has_trust_decay()
    print(json.dumps({
        "predicted_success": round(ps, 4),
        "swarm_consensus": round(sc, 4),
        "trust_decay": td,
        "gate_pass": sc >= 0.65,
    }, indent=2))
    return 0 if sc >= 0.65 else 1


# ============================================================================
# Argument parser
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="rig",
        description="RIG Communication Protocol V10 — CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("smoke", help="Run all-engine deterministic smoke test (exit 0 = all pass)")

    score_p = sub.add_parser("score", help="Score a communication artifact")
    score_p.add_argument("--text", default="", help="Text to score (optional)")

    gates_p = sub.add_parser("gates", help="Run gate checks on text")
    gates_p.add_argument("--text", default="", help="Text to check (defaults to canonical example)")

    sub.add_parser("idp", help="Run IDP (IdeaDeviationPotential) on canonical fixture")
    sub.add_parser("swarm", help="Run 8-persona prediction swarm on canonical fixture")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    commands = {
        "smoke": cmd_smoke,
        "score": cmd_score,
        "gates": cmd_gates,
        "idp": cmd_idp,
        "swarm": cmd_swarm,
    }
    handler = commands.get(args.command)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
