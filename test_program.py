"""Tests for the initial program (Circana Omni-Channel RMN Flighting Optimizer)."""

import math
import numpy as np
import pytest

from initial_program import allocate_rmn_flighting, build_circana_campaign_model, evaluate

EVAL_INPUTS = {
    "total_budget_musd": 2.5,
    "n_rmns": 5,
    "n_weeks": 8,
    "min_flight_musd": 0.025,
    "pantry_cooldown_weeks": 3,
    "random_seed": 42,
}


def test_allocate_rmn_flighting_returns_valid_matrix():
    """allocate_rmn_flighting() returns a (5, 8) non-negative numpy array within budget."""
    model = build_circana_campaign_model(EVAL_INPUTS)
    schedule = allocate_rmn_flighting(model)
    assert isinstance(schedule, np.ndarray)
    assert schedule.shape == (5, 8)
    assert np.all(np.isfinite(schedule))
    assert np.all(schedule >= 0.0)
    assert float(np.sum(schedule)) <= EVAL_INPUTS["total_budget_musd"] + 1e-6


def test_evaluate_returns_dict_with_metric():
    """evaluate() returns a dict containing 'fitness_score' and diagnostic telemetry."""
    result = evaluate(EVAL_INPUTS)
    assert isinstance(result, dict)
    assert "fitness_score" in result
    assert "incremental_lift_musd" in result
    assert "iroas" in result
    assert "waste_pct" in result


def test_evaluate_returns_finite_score():
    """evaluate() returns a finite positive baseline score for the seed program."""
    result = evaluate(EVAL_INPUTS)
    score = result["fitness_score"]
    assert isinstance(score, (int, float))
    assert math.isfinite(score)
    assert score > 50.0


def test_evaluate_is_deterministic():
    """Calling evaluate() twice with identical inputs yields the exact same score."""
    r1 = evaluate(EVAL_INPUTS)
    r2 = evaluate(EVAL_INPUTS)
    assert r1["fitness_score"] == pytest.approx(r2["fitness_score"], abs=1e-9)

