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

INITIAL_CODE = pathlib.Path(__file__).with_name("initial_program.py").read_text(encoding="utf-8")


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
        base_dir = pathlib.Path(__file__).resolve().parent
        shutil.copy(base_dir / "initial_program.py", os.path.join(tmpdir, "initial_program.py"))
        shutil.copy(base_dir / "evaluator.py", os.path.join(tmpdir, "evaluator.py"))
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

