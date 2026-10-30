"""Tests for the CLI-compatible AlphaEvolve evaluator."""

import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import pytest

from evaluator import evaluate_program

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
INITIAL_CODE = (ROOT_DIR / "initial_program.py").read_text(encoding="utf-8")


def test_evaluate_program_returns_score_and_insights():
    """evaluate_program() returns a dict with finite float score and insights list."""
    result = evaluate_program(INITIAL_CODE)
    assert isinstance(result["score"], float)
    assert result["score"] > 50.0
    assert isinstance(result["insights"], list)
    labels = {item["label"] for item in result["insights"]}
    assert "campaign_kpis" in labels


def test_evaluate_program_returns_error_insights_on_syntax_failure():
    """evaluate_program() returns None score and error/traceback insights for bad syntax."""
    result = evaluate_program("def broken_syntax(!!!")
    assert result["score"] is None
    labels = {i["label"] for i in result["insights"]}
    assert "error" in labels
    assert "traceback" in labels


def test_evaluate_program_rejects_forbidden_imports():
    """AST validation tier rejects forbidden system imports."""
    bad_code = "import subprocess\ndef evaluate(ei): return {'fitness_score': 999.0}"
    result = evaluate_program(bad_code)
    assert result["score"] is None
    assert any("Forbidden import" in i["text"] for i in result["insights"])


def test_evaluate_program_captures_stdout():
    """stdout from the program is captured as an insight."""
    code = 'print("circana-diagnostic-trace")\ndef evaluate(ei): return {"fitness_score": 123.4}'
    result = evaluate_program(code)
    assert result["score"] == pytest.approx(123.4)
    stdout_items = [i for i in result["insights"] if i["label"] == "stdout"]
    assert len(stdout_items) == 1
    assert "circana-diagnostic-trace" in stdout_items[0]["text"]


def test_cli_main_writes_output_file():
    """Running evaluator.py as a CLI script writes a valid JSON output file."""
    tmpdir = tempfile.mkdtemp()
    try:
        shutil.copy(ROOT_DIR / "initial_program.py", os.path.join(tmpdir, "initial_program.py"))
        shutil.copy(ROOT_DIR / "evaluator.py", os.path.join(tmpdir, "evaluator.py"))
        output_file = os.path.join(tmpdir, "scores.json")

        cmd = [
            sys.executable,
            "evaluator.py",
            "--output-file",
            output_file,
            "--program-dir",
            tmpdir,
        ]
        proc = subprocess.run(
            cmd,
            cwd=tmpdir,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        assert proc.returncode == 0, f"stderr: {proc.stderr}"
        with open(output_file, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data["score"], (int, float))
        assert isinstance(data["insights"], list)
    finally:
        shutil.rmtree(tmpdir)


def test_all_eight_national_and_pdi_milestones_increase_monotonically():
    """All 8 candidate milestones (5 National + 3 PDI Geo-Temporal) evaluate cleanly and increase."""
    from webapp.server import AlphaEvolveGuiConfig, simulate_evolution

    res = simulate_evolution(AlphaEvolveGuiConfig())
    milestones = res["milestones"]
    assert len(milestones) == 8

    scores = [m["score"] for m in milestones]
    for i in range(1, len(scores)):
        assert scores[i] > scores[i - 1], f"Milestone {i} did not improve: {scores}"

    # Verify National Champion (Gen 5) vs PDI Geo-Temporal Champion (Gen 8)
    assert milestones[0]["score"] == pytest.approx(196.49, abs=0.1)
    assert milestones[4]["score"] == pytest.approx(522.33, abs=0.1)
    assert milestones[5]["score"] == pytest.approx(589.40, abs=0.2)
    assert milestones[6]["score"] == pytest.approx(641.25, abs=0.2)
    assert milestones[7]["score"] == pytest.approx(684.90, abs=0.2)
    assert milestones[7]["telemetry"]["pdi_enabled"] is True
    assert milestones[7]["telemetry"]["pdi_geo_dividend_musd"] > 4.0

