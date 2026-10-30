"""CLI-compatible Three-Tier Evaluator for Circana Omni-Channel RMN Flighting Optimizer.

Invoked by the AlphaEvolve `ae` CLI as:
    python evaluator.py --output-file <path> --program-dir <workspace>
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import json
import math
import os
import signal
import sys
import traceback
from typing import Any, Mapping
import numpy as np

EVALUATION_METRIC = "fitness_score"
EVALUATION_INPUTS: dict[str, Any] = {
    "total_budget_musd": 2.5,
    "n_rmns": 5,
    "n_weeks": 8,
    "min_flight_musd": 0.025,
    "pantry_cooldown_weeks": 3,
    "random_seed": 42,
}

FORBIDDEN_MODULES = {"os", "sys", "subprocess", "socket", "shutil", "inspect", "ctypes"}


class EvaluationTimeout(Exception):
    """Raised when candidate program execution exceeds timeout_seconds."""


def _timeout_handler(signum: int, frame: Any) -> None:
    raise EvaluationTimeout("Evaluation timed out")


if hasattr(signal, "alarm"):
    signal.signal(signal.SIGALRM, _timeout_handler)


def _check_ast_security(code: str) -> str | None:
    """Tier 1 AST validation: check syntax and reject forbidden imports/primitives."""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_mod = alias.name.split(".")[0]
                if root_mod in FORBIDDEN_MODULES:
                    return f"Forbidden import '{alias.name}' is not allowed."
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_mod = node.module.split(".")[0]
                if root_mod in FORBIDDEN_MODULES:
                    return f"Forbidden import from '{node.module}' is not allowed."
    return None


def _failure(
    error: str,
    tb: str | None = None,
    stdout: str = "",
    stderr: str = "",
) -> dict[str, Any]:
    """Construct a standardized AlphaEvolve failure payload."""
    insights: list[dict[str, str]] = [{"label": "error", "text": error}]
    if tb:
        insights.append({"label": "traceback", "text": tb[-2000:]})
    if stdout:
        insights.append({"label": "stdout", "text": stdout[-2000:]})
    if stderr:
        insights.append({"label": "stderr", "text": stderr[-2000:]})
    return {"score": None, "insights": insights}


def evaluate_program(
    code: str,
    timeout_seconds: int = 30,
    eval_inputs_override: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute candidate Python code and return AlphaEvolve score + diagnostic insights."""
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()

    # === TIER 1: VALIDATION (Syntax & AST Security Check) ===
    try:
        security_err = _check_ast_security(code)
        if security_err:
            return _failure(security_err)
    except SyntaxError as exc:
        return _failure(f"SyntaxError: {exc}", tb=traceback.format_exc())

    inputs = dict(EVALUATION_INPUTS)
    if eval_inputs_override:
        inputs.update(eval_inputs_override)

    # === TIER 2 & 3: VERIFICATION & EVALUATION ===
    try:
        if hasattr(signal, "alarm"):
            signal.alarm(timeout_seconds)

        exec_namespace: dict[str, Any] = {
            "__builtins__": __builtins__,
            "np": np,
            "math": math,
            "Any": Any,
            "Mapping": Mapping,
        }

        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            exec(compile(code, "initial_program.py", "exec"), exec_namespace)
            eval_fn = exec_namespace.get("evaluate")
            if not callable(eval_fn):
                return _failure(
                    "Program missing callable 'evaluate(eval_inputs)' function",
                    stdout=stdout_capture.getvalue(),
                    stderr=stderr_capture.getvalue(),
                )
            result = eval_fn(inputs)

        stdout_str = stdout_capture.getvalue()
        stderr_str = stderr_capture.getvalue()

        if not isinstance(result, Mapping):
            return _failure(
                f"evaluate() must return a dict, got {type(result).__name__}",
                stdout=stdout_str,
                stderr=stderr_str,
            )

        raw_score = result.get(EVALUATION_METRIC)
        if raw_score is None:
            return _failure("No 'fitness_score' returned by evaluate()", stdout=stdout_str, stderr=stderr_str)

        score_val = float(raw_score)
        if math.isnan(score_val) or math.isinf(score_val) or score_val <= -1e11:
            return _failure(
                f"Invalid or non-finite score: {raw_score}",
                stdout=stdout_str,
                stderr=stderr_str,
            )

        insights: list[dict[str, str]] = []
        if stdout_str:
            insights.append({"label": "stdout", "text": stdout_str[-2000:]})
        if stderr_str:
            insights.append({"label": "stderr", "text": stderr_str[-2000:]})

        if "incremental_lift_musd" in result:
            insights.append(
                {
                    "label": "campaign_kpis",
                    "text": (
                        f"Incremental Sales Lift: +${result.get('incremental_lift_musd', 0):.2f}M | "
                        f"iROAS: {result.get('iroas', 0):.2f}x | "
                        f"Spend: ${result.get('total_spend_musd', 0):.2f}M | "
                        f"Ad/OOS Waste: {result.get('waste_pct', 0):.1f}%"
                    ),
                }
            )
            insights.append(
                {
                    "label": "loss_breakdown",
                    "text": (
                        f"Pantry Cannibalization Loss: ${result.get('pantry_loss_musd', 0):.2f}M | "
                        f"Cross-RMN Overlap Loss: ${result.get('overlap_loss_musd', 0):.2f}M | "
                        f"Out-of-Stock Penalty: ${result.get('oos_loss_musd', 0):.2f}M"
                    ),
                }
            )
            if "pdi_cosine_sim_match" in result:
                insights.append(
                    {
                        "label": "pdi_geospatial_insights",
                        "text": (
                            f"PDI Active: {result.get('pdi_enabled', False)} | "
                            f"Sister-Region Cosine Match: {result.get('pdi_cosine_sim_match', 0):.2f} | "
                            f"PDI Geo Dividend: +${result.get('pdi_geo_dividend_musd', 0):.2f}M | "
                            f"WorldPop Capture: {result.get('worldpop_residential_capture_pct', 0):.1f}%"
                        ),
                    }
                )

        return {
            "score": round(score_val, 4),
            "insights": insights,
            "telemetry": dict(result),
        }

    except EvaluationTimeout:
        return _failure(
            f"Timed out after {timeout_seconds}s",
            tb=traceback.format_exc(),
            stdout=stdout_capture.getvalue(),
            stderr=stderr_capture.getvalue(),
        )
    except Exception as exc:
        return _failure(
            f"Evaluation failed: {exc}",
            tb=traceback.format_exc(),
            stdout=stdout_capture.getvalue(),
            stderr=stderr_capture.getvalue(),
        )
    finally:
        if hasattr(signal, "alarm"):
            signal.alarm(0)


def main() -> None:
    """CLI entry point invoked by `ae` CLI."""
    parser = argparse.ArgumentParser(description="Circana RMN Flighting Evaluator")
    parser.add_argument("--output-file", required=True, help="Path to write JSON score output")
    parser.add_argument("--program-dir", required=True, help="Directory containing initial_program.py")
    args = parser.parse_args()

    sys.path.insert(0, args.program_dir)
    program_path = os.path.join(args.program_dir, "initial_program.py")
    with open(program_path, encoding="utf-8") as f:
        code = f.read()

    eval_out = evaluate_program(code)
    # Strip extra local UI telemetry key when writing strict ae CLI JSON output
    cli_payload = {
        "score": eval_out["score"],
        "insights": eval_out["insights"],
    }
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(cli_payload, f, indent=2)


if __name__ == "__main__":
    main()

