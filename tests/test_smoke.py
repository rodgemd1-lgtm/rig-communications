"""
RIG Communication Protocol V10 — Smoke Tests
Deterministic pytest suite for all four engines + CLI.

Run with:
    pytest tests/ -v
or via CLI smoke command:
    python3 src/cli.py smoke
"""

import sys
import os
import json

import pytest

# Ensure src/ is importable when running from repo root
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_src = os.path.join(_root, "src")
if _src not in sys.path:
    sys.path.insert(0, _src)

from scoring import CommunicationScore, GateEngine as ScoringGateEngine
from formulas import (
    comm_raw_score,
    email_voltage_score,
    email_reply_score,
    bdf30,
    craft_coefficient,
    catchphrase_score,
    customer_facing_artifact_score,
    rpe,
    compute_idp,
    idp_classify,
    IDPScoreInput,
    formula_registry,
)
from gates import GateEngine, compute_entropy_ratio, compute_reactance_risk
from swarm import PredictionSwarm, PersonaPrediction, example_swarm
from cli import main as cli_main, _sarah_chen_score, _SARAH_CHEN_TEXT


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture()
def sarah_score() -> CommunicationScore:
    """Canonical Sarah Chen cold-email score fixture."""
    return _sarah_chen_score()


@pytest.fixture()
def sarah_text() -> str:
    return _SARAH_CHEN_TEXT


@pytest.fixture()
def canonical_idp() -> IDPScoreInput:
    return IDPScoreInput(
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


# ============================================================================
# Engine 1: Scoring
# ============================================================================

class TestScoringEngine:
    def test_comm_raw_score_above_gate(self, sarah_score):
        crs = comm_raw_score(sarah_score)
        assert crs >= 0.65, f"CommRawScore {crs:.4f} must be >= 0.65"

    def test_comm_raw_score_known_value(self, sarah_score):
        crs = comm_raw_score(sarah_score)
        assert abs(crs - 0.8601) < 0.001, f"Expected ~0.860, got {crs:.4f}"

    def test_email_voltage_score(self, sarah_score):
        evs = email_voltage_score(sarah_score)
        assert 0.0 <= evs <= 1.0

    def test_all_formula_registry_callable(self, sarah_score):
        for name, func in formula_registry.items():
            result = func(sarah_score)
            assert isinstance(result, float), f"{name} must return float"

    def test_score_to_dict_structure(self, sarah_score):
        d = sarah_score.to_dict()
        assert "formulas" in d
        assert "comm_raw_score" in d["formulas"]
        assert "banned_phrases" in d

    def test_banned_phrase_scanner(self):
        engine = ScoringGateEngine
        found = engine.scan_banned_phrases("hope this finds you well and just checking in")
        assert "hope this finds you well" in found
        assert "just checking in" in found

    def test_clean_text_no_banned_phrases(self, sarah_text):
        engine = ScoringGateEngine
        found = engine.scan_banned_phrases(sarah_text)
        assert found == [], f"Clean text should have no banned phrases, got: {found}"


# ============================================================================
# Engine 2: Gate Engine
# ============================================================================

class TestGateEngine:
    def test_clean_communication_passes_all_gates(self, sarah_score, sarah_text):
        report = GateEngine.check_gates(sarah_score, sarah_text)
        assert report.can_ship is True, (
            f"Gate check failed. Blocks: {[b.name for b in report.blocks]}"
        )
        assert len(report.blocks) == 0

    def test_banned_phrase_blocks_shipment(self, sarah_score):
        bad_text = "Hope this finds you well. Would love to chat about your needs!"
        report = GateEngine.check_gates(sarah_score, bad_text)
        block_names = [b.name for b in report.blocks]
        assert "BANNED_PHRASES" in block_names

    def test_all_seven_categories_pass_on_clean_text(self, sarah_score, sarah_text):
        report = GateEngine.check_gates(sarah_score, sarah_text)
        for category, passed in report.summary.items():
            assert passed, f"Category '{category}' should pass, but failed"

    def test_entropy_ratio_above_threshold(self, sarah_text):
        baseline = "professional email regarding business services"
        ratio = compute_entropy_ratio(sarah_text, baseline)
        assert ratio >= 1.2, f"Entropy ratio {ratio:.3f} must be >= 1.2"

    def test_reactance_risk_below_threshold_for_clean_text(self, sarah_text):
        risk = compute_reactance_risk(sarah_text)
        assert risk <= 0.20, f"ReactanceRisk {risk:.3f} must be <= 0.20"

    def test_reactance_risk_high_for_pushy_text(self):
        pushy = "You must act now! This is urgent and you need to respond immediately."
        risk = compute_reactance_risk(pushy)
        assert risk > 0.20, f"Pushy text should have ReactanceRisk > 0.20, got {risk:.3f}"

    def test_low_autonomy_score_blocks(self):
        low_autonomy = CommunicationScore(
            wound_precision=0.85,
            mirror_accuracy=0.90,
            autonomy_preservation=0.30,  # Below 0.70 gate
            specificity_density=0.88,
            anti_generic_force=0.88,
            identity_force=0.90,
            rig_signature=0.88,
            ethical_restraint=0.92,
            semantic_inversion=0.92,
            proof_density=0.88,
            enemy_specificity=0.90,
            catchphrase_voltage=0.85,
            structural_novelty=0.82,
            negative_space_weight=0.75,
        )
        report = GateEngine.check_gates(low_autonomy, "Some text without banned phrases.")
        block_names = [b.name for b in report.blocks]
        assert "AUTONOMY" in block_names


# ============================================================================
# Engine 3: Formula Registry / IDP
# ============================================================================

class TestFormulaRegistry:
    def test_idp_above_strong_threshold(self, canonical_idp):
        idp_val = compute_idp(canonical_idp)
        assert idp_val >= 0.70, f"IDP {idp_val:.4f} must be >= 0.70 (Strong)"

    def test_idp_known_value(self, canonical_idp):
        idp_val = compute_idp(canonical_idp)
        assert abs(idp_val - 0.798) < 0.005, f"Expected ~0.798, got {idp_val:.4f}"

    def test_idp_classify_strong(self, canonical_idp):
        idp_val = compute_idp(canonical_idp)
        label = idp_classify(idp_val)
        assert "Strong" in label

    def test_idp_classify_labels(self):
        assert "Elite" in idp_classify(0.95)
        assert "Exceptional" in idp_classify(0.85)
        assert "Strong" in idp_classify(0.75)
        assert "Marginal" in idp_classify(0.67)
        assert "Insufficient" in idp_classify(0.55)
        assert "Generic" in idp_classify(0.40)

    def test_bdf30_on_sarah_score(self, sarah_score):
        val = bdf30(sarah_score)
        assert 0.0 <= val <= 1.0

    def test_rpe_positive_for_strong_email(self, sarah_score):
        val = rpe(sarah_score)
        assert val > 0, f"RPE must be > 0 for strong email, got {val:.4f}"

    def test_craft_coefficient_max_of_archetypes(self, sarah_score):
        cc = craft_coefficient(sarah_score)
        expected = max(
            sarah_score.eminem_density,
            sarah_score.hemingway_compression,
            sarah_score.didion_cadence,
            sarah_score.mccarthy_rhythm,
            sarah_score.wallace_recursion,
        )
        assert abs(cc - expected) < 1e-9


# ============================================================================
# Engine 4: Prediction Swarm
# ============================================================================

class TestPredictionSwarm:
    def test_swarm_consensus_above_gate(self):
        swarm = example_swarm()
        sc = swarm.swarm_consensus()
        assert sc >= 0.65, f"SwarmConsensus {sc:.4f} must be >= 0.65"

    def test_brier_score_computation(self):
        swarm = PredictionSwarm()
        predictions = {"reply": 0.8, "forward": 0.3}
        outcomes = {"reply": 1.0, "forward": 0.0}
        bs = swarm.brier_score(predictions, outcomes)
        expected = ((0.8 - 1.0) ** 2 + (0.3 - 0.0) ** 2) / 2
        assert abs(bs - expected) < 1e-9

    def test_trust_decay_detection(self):
        swarm = PredictionSwarm()
        swarm.add_prediction(PersonaPrediction(
            persona="Skeptic", read_past_line_2=True,
            trust_delta=-0.5, reply_probability=0.1,
            share_probability=0.0, comment_probability=0.0,
            forward_probability=0.0, meeting_probability=0.0,
        ))
        assert swarm.has_trust_decay() is True

    def test_no_trust_decay_all_positive(self):
        swarm = PredictionSwarm()
        swarm.add_prediction(PersonaPrediction(
            persona="Fan", read_past_line_2=True,
            trust_delta=0.5, reply_probability=0.9,
            share_probability=0.5, comment_probability=0.4,
            forward_probability=0.3, meeting_probability=0.6,
        ))
        assert swarm.has_trust_decay() is False

    def test_empty_swarm_returns_zeros(self):
        swarm = PredictionSwarm()
        assert swarm.predicted_success() == 0.0
        assert swarm.swarm_consensus() == 0.0


# ============================================================================
# CLI
# ============================================================================

class TestCLI:
    def test_smoke_exits_zero(self):
        exit_code = cli_main(["smoke"])
        assert exit_code == 0

    def test_score_exits_zero(self):
        exit_code = cli_main(["score"])
        assert exit_code == 0

    def test_gates_exits_zero_on_clean_text(self):
        exit_code = cli_main(["gates"])
        assert exit_code == 0

    def test_gates_exits_nonzero_on_banned_text(self, capsys):
        exit_code = cli_main(["gates", "--text", "Hope this finds you well, touching base!"])
        assert exit_code != 0

    def test_idp_exits_zero(self):
        exit_code = cli_main(["idp"])
        assert exit_code == 0

    def test_swarm_exits_zero(self):
        exit_code = cli_main(["swarm"])
        assert exit_code == 0

    def test_smoke_output_contains_pass(self, capsys):
        cli_main(["smoke"])
        captured = capsys.readouterr()
        assert "SMOKE: ALL PASS" in captured.out

    def test_score_output_is_valid_json(self, capsys):
        cli_main(["score"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "comm_raw_score" in data
