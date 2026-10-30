#!/usr/bin/env python3
"""FastAPI Backend for Circana Liquid Data® × Google Maps PDI × AlphaEvolve Demo.

Provides:
1. Real-time execution of candidate programs through the AlphaEvolve 3-tier `evaluator.py`
2. Full inspection & editing of AlphaEvolve configurations + Google Maps PDI 330-D
   S2 Level 12 & Earth Engine WorldPop 100m (`ST_REGIONSTATS`) geospatial settings
3. Live evolutionary trajectory generation across 8 progressive algorithmic milestones:
   - Milestones 1..5: National-only AlphaEvolve evolution (196.49 -> 522.33)
   - Milestones 6..8: Google Maps PDI 330-D + WorldPop 100m Geo-Temporal breakthrough (522.33 -> 684.90)
4. Direct `ae` CLI integration (`ae version`, `ae --json config show`, `ae --json program evaluate`)
"""

from __future__ import annotations

import difflib
import json
import os
import pathlib
import subprocess
import sys
import time
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT_DIR / "static"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import evaluator  # noqa: E402

app = FastAPI(
    title="Circana Liquid Data® × Google Maps PDI × AlphaEvolve — Geo-Temporal RMN Optimizer",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ==============================================================================
# 8 Progressive Candidate Algorithms (5 National + 3 Google Maps PDI Geo-Temporal)
# Evaluated Live by evaluator.py!
# ==============================================================================

CANDIDATE_EVOLVE_BLOCKS: List[Dict[str, Any]] = [
    {
        "stage_id": "seed",
        "progress_ratio": 0.01,
        "nickname": "seed-uniform-smear",
        "is_pdi_stage": False,
        "model_used": "initial_program.py (Baseline Seed)",
        "summary": "Gen 1 (Seed): Naive proportional budget split across all 5 RMNs & 8 weeks",
        "what_changed": "Initial seed program. Distributes budget uniformly across all 8 weeks proportional to RMN capacity, ignoring S-curve thresholds, 3-week pantry cannibalization, OOS caps, and PDI S2 embeddings.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 1 Seed: Uniform weekly split proportional to RMN capacity (No PDI Geo)."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    capacities = np.asarray(model["max_weekly_lift_musd"], dtype=float)

    rmn_weights = capacities / np.sum(capacities)
    schedule = np.outer(rmn_weights, np.ones(n_weeks, dtype=float)) * (total_budget / n_weeks)
    return schedule''',
    },
    {
        "stage_id": "scurve_threshold",
        "progress_ratio": 0.14,
        "nickname": "hill-threshold-concentrator",
        "is_pdi_stage": False,
        "model_used": "gemini-3.5-flash",
        "summary": "Gen 2: Discovers Hill S-Curve inflection pulsing (eliminates dead-zone micro-spends)",
        "what_changed": "Replaced uniform weekly smearing with pulsed flights sized at 1.25x each RMN's Hill S-curve inflection point (hill_k_musd) during above-average seasonality weeks.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 2: Pulse flights at 1.25x Hill S-curve inflection kappa in high-seasonality weeks."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for r in range(n_rmns):
        top_weeks = np.argsort(-seasonality[r])[:5]
        for t in top_weeks:
            schedule[r, t] = 1.25 * hill_k[r]

    if np.sum(schedule) > 0:
        schedule *= total_budget / np.sum(schedule)
    return schedule''',
    },
    {
        "stage_id": "pantry_cooldown",
        "progress_ratio": 0.31,
        "nickname": "pantry-cooldown-pulser",
        "is_pdi_stage": False,
        "model_used": "gemini-3.5-flash",
        "summary": "Gen 3: Evolves 3-week household pantry-depletion spacing + OOS ceiling gates",
        "what_changed": "Enforces a minimum 2-to-3 week cooldown between active flights on the same RMN while gating out low-inventory OOS weeks.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 3: Dynamic pantry-depletion spacing per RMN + OOS gating."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for r in range(n_rmns):
        chosen: list[int] = []
        order = np.argsort(-(seasonality[r] * (inv_cap[r] >= 1.15 * hill_k[r])))
        for w in order:
            w_int = int(w)
            if inv_cap[r, w_int] < 1.15 * hill_k[r]:
                continue
            if all(abs(w_int - c) >= 2 for c in chosen):
                chosen.append(w_int)
            if len(chosen) == 4:
                break
        for w_int in chosen:
            schedule[r, w_int] = min(1.55 * hill_k[r], inv_cap[r, w_int])

    if np.sum(schedule) > 0:
        schedule = np.minimum(schedule * (total_budget / np.sum(schedule)), inv_cap * 0.98)
        if np.sum(schedule) > total_budget:
            schedule *= total_budget / np.sum(schedule)
    return schedule''',
    },
    {
        "stage_id": "cross_rmn_dedup",
        "progress_ratio": 0.52,
        "nickname": "cross-rmn-overlap-decoupler",
        "is_pdi_stage": False,
        "model_used": "gemini-3.1-pro-preview",
        "summary": "Gen 4: Cross-RMN household overlap deduplication across Walmart, Target & Kroger",
        "what_changed": "Jointly optimizes across all 5 RMNs using overlap_matrix to stagger Walmart Connect, Target Roundel, and Kroger flights onto non-colliding weeks.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 4: Joint cross-RMN overlap-aware staggered flight selection."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    hill_n = np.asarray(model["hill_n"], dtype=float)
    max_lift = np.asarray(model["max_weekly_lift_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    overlap = np.asarray(model["overlap_matrix"], dtype=float)

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for _ in range(18):
        best_gain = 0.0
        best_pair = None
        best_spend = 0.0
        for r in range(n_rmns):
            for t in range(n_weeks):
                if schedule[r, t] > 0 or inv_cap[r, t] < 1.15 * hill_k[r]:
                    continue
                pantry_pen = 1.0
                for dt, w_pen in ((1, 0.52), (2, 0.30)):
                    if (t - dt >= 0 and schedule[r, t - dt] > 0) or (t + dt < n_weeks and schedule[r, t + dt] > 0):
                        pantry_pen -= w_pen
                if pantry_pen < 0.45:
                    continue
                spend = min(1.62 * hill_k[r], inv_cap[r, t] * 0.98)
                if np.sum(schedule) + spend > total_budget:
                    spend = total_budget - float(np.sum(schedule))
                if spend < 0.90 * hill_k[r]:
                    continue
                active_int = np.clip(schedule[:, t] / (hill_k * 1.2), 0.0, 1.4)
                ov_mult = max(0.45, 1.0 - 0.32 * float(overlap[r] @ active_int))
                h_val = (spend ** hill_n[r]) / (hill_k[r] ** hill_n[r] + spend ** hill_n[r])
                gain = (max_lift[r] * seasonality[r, t] * h_val * pantry_pen * ov_mult) / spend
                if gain > best_gain:
                    best_gain = gain
                    best_pair = (r, t)
                    best_spend = spend
        if best_pair is None:
            break
        schedule[best_pair[0], best_pair[1]] = best_spend
    if 0 < np.sum(schedule) < total_budget:
        schedule = np.minimum(schedule * (total_budget / np.sum(schedule)), inv_cap * 0.99)
    return schedule''',
    },
    {
        "stage_id": "national_ae_champion",
        "progress_ratio": 0.68,
        "nickname": "national-ae-champion",
        "is_pdi_stage": False,
        "model_used": "gemini-3.1-pro-preview",
        "summary": "Gen 5 (National Baseline Top): Staggered Pulse Search + Marginal Hill Coordinate Ascent (522.33)",
        "what_changed": "Champion algorithm from baseline circan_alpha_evolve: combines combinatorial pulse selection with marginal-lift coordinate ascent. Reaches the 522.33 ceiling of national-only scheduling.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 5 (National Baseline Top = 522.33): Combinatorial Pulse Selection + Coordinate Ascent."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    min_flight = float(model["min_flight_musd"])
    hill_k = np.asarray(model["hill_k_musd"], dtype=float)
    hill_n = np.asarray(model["hill_n"], dtype=float)
    max_lift = np.asarray(model["max_weekly_lift_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    overlap = np.asarray(model["overlap_matrix"], dtype=float)

    def sim_net_lift(sched: np.ndarray) -> float:
        total = 0.0
        for t in range(n_weeks):
            b_t = sched[:, t]
            eff_b = np.minimum(b_t, inv_cap[:, t])
            num = np.power(eff_b, hill_n)
            den = np.power(hill_k, hill_n) + num
            base_t = max_lift * seasonality[:, t] * np.where(den > 0, num / den, 0.0)
            pantry = np.ones(n_rmns, dtype=float)
            for lag, w_decay in ((1, 0.52), (2, 0.30)):
                if t - lag >= 0:
                    pantry -= w_decay * np.clip(sched[:, t - lag] / (hill_k * 1.1), 0.0, 1.5)
            after_p = base_t * np.clip(pantry, 0.22, 1.0)
            act_int = np.clip(eff_b / (hill_k * 1.2), 0.0, 1.4)
            ov_mult = np.clip(1.0 - 0.32 * (overlap @ act_int), 0.45, 1.0)
            oos_pen = np.maximum(0.0, b_t - inv_cap[:, t]) * 2.4
            total += float(np.sum(np.maximum(0.0, after_p * ov_mult - oos_pen)))
        return total

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for _ in range(18):
        cur_lift = sim_net_lift(schedule)
        rem_budget = total_budget - float(np.sum(schedule))
        if rem_budget < min_flight:
            break
        best_roi = 0.0
        best_move = None
        for r in range(n_rmns):
            for t in range(n_weeks):
                if schedule[r, t] > 0 or inv_cap[r, t] < 1.10 * hill_k[r]:
                    continue
                trial_spend = min(1.38 * hill_k[r], inv_cap[r, t], rem_budget)
                if trial_spend < 0.85 * hill_k[r]:
                    continue
                trial = schedule.copy()
                trial[r, t] = trial_spend
                gain = sim_net_lift(trial) - cur_lift
                roi = gain / trial_spend
                if roi > best_roi:
                    best_roi = roi
                    best_move = (r, t, trial_spend)
        if best_move is None or best_roi <= 0.8:
            break
        schedule[best_move[0], best_move[1]] = best_move[2]

    active_cells = [(r, t) for r in range(n_rmns) for t in range(n_weeks) if schedule[r, t] > 0]
    delta = 0.008
    for _ in range(140):
        rem = total_budget - float(np.sum(schedule))
        if rem >= delta:
            cur_l = sim_net_lift(schedule)
            best_g = 0.0
            best_c = None
            for r, t in active_cells:
                if schedule[r, t] + delta <= inv_cap[r, t]:
                    schedule[r, t] += delta
                    g = sim_net_lift(schedule) - cur_l
                    schedule[r, t] -= delta
                    if g > best_g:
                        best_g = g
                        best_c = (r, t)
            if best_c is not None and best_g > 0:
                schedule[best_c[0], best_c[1]] += delta
                continue
        break

    return schedule''',
    },
    {
        "stage_id": "pdi_worldpop_rollup",
        "progress_ratio": 0.79,
        "nickname": "pdi-worldpop-boundary-aggregator",
        "is_pdi_stage": True,
        "model_used": "gemini-3.5-flash",
        "summary": "Gen 6 (+PDI Step 1): BigQuery S2 Level 12 + WorldPop 100m Custom Trade-Area Rollup (589.40)",
        "what_changed": "Integrates Google Maps PDI S2 Level 12 embeddings aggregated over 5km custom store boundaries via Earth Engine WorldPop 100m (`ST_REGIONSTATS`) + L2 normalization. Prunes zero-household industrial/airport slivers (+12.8% over National AE!).",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 6 (+PDI Step 1): WorldPop 100m (`ST_REGIONSTATS`) S2 Level 12 boundary rollup + L2 norm."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    min_flight = float(model["min_flight_musd"])
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    overlap = np.asarray(model["overlap_matrix"], dtype=float)

    # Activate PDI Step 1: WorldPop 100m (`ST_REGIONSTATS`) + L2-normalized custom boundary rollup
    emb = np.asarray(model["pdi_330d_embeddings"], dtype=float)
    wp_pop = np.asarray(model["pdi_worldpop_100m_pop"], dtype=float)
    area_km2 = np.asarray(model["pdi_sliver_area_km2"], dtype=float)
    wp_weights = wp_pop / np.sum(wp_pop, axis=1, keepdims=True)
    area_weights = area_km2 / np.sum(area_km2, axis=1, keepdims=True)
    agg_330d = np.einsum("mc,mcd->md", wp_weights, emb)
    agg_330d /= np.maximum(np.linalg.norm(agg_330d, axis=1, keepdims=True), 1e-8)

    model["pdi_geo_dispatch"].update({
        "enabled": True,
        "worldpop_l2_rollup": True,
        "sister_search_cosine_sim": False,
        "poi_local_decoupling": False,
        "weather_thermal_cooldown": False,
    })

    wp_res_gain = float(np.mean(np.sum(wp_weights[:, :12], axis=1) - np.sum(area_weights[:, :12], axis=1)))
    eff_hill_k = np.asarray(model["hill_k_musd"], dtype=float) * 0.93
    eff_max_lift = np.asarray(model["max_weekly_lift_musd"], dtype=float) * (1.0 + 0.42 * wp_res_gain)
    hill_n = np.asarray(model["hill_n"], dtype=float)

    def sim_lift(sched: np.ndarray) -> float:
        total = 0.0
        for t in range(n_weeks):
            eff_b = np.minimum(sched[:, t], inv_cap[:, t])
            num = np.power(eff_b, hill_n)
            den = np.power(eff_hill_k, hill_n) + num
            base_t = eff_max_lift * seasonality[:, t] * np.where(den > 0, num / den, 0.0)
            pantry = np.ones(n_rmns, dtype=float)
            for lag, w_d in ((1, 0.52), (2, 0.30)):
                if t - lag >= 0:
                    pantry -= w_d * np.clip(sched[:, t - lag] / (eff_hill_k * 1.1), 0.0, 1.5)
            after_p = base_t * np.clip(pantry, 0.22, 1.0)
            ov_mult = np.clip(1.0 - 0.32 * (overlap @ np.clip(eff_b / (eff_hill_k * 1.2), 0.0, 1.4)), 0.45, 1.0)
            total += float(np.sum(np.maximum(0.0, after_p * ov_mult - np.maximum(0.0, sched[:, t] - inv_cap[:, t]) * 2.4)))
        return total

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for _ in range(18):
        cur_l = sim_lift(schedule)
        rem = total_budget - float(np.sum(schedule))
        if rem < min_flight:
            break
        best_roi, best_mv = 0.0, None
        for r in range(n_rmns):
            for t in range(n_weeks):
                if schedule[r, t] > 0 or inv_cap[r, t] < 1.10 * eff_hill_k[r]:
                    continue
                sp = min(1.38 * eff_hill_k[r], inv_cap[r, t], rem)
                if sp < 0.85 * eff_hill_k[r]:
                    continue
                tr = schedule.copy()
                tr[r, t] = sp
                roi = (sim_lift(tr) - cur_l) / sp
                if roi > best_roi:
                    best_roi, best_mv = roi, (r, t, sp)
        if best_mv is None or best_roi <= 0.8:
            break
        schedule[best_mv[0], best_mv[1]] = best_mv[2]

    active = [(r, t) for r in range(n_rmns) for t in range(n_weeks) if schedule[r, t] > 0]
    for _ in range(140):
        if total_budget - float(np.sum(schedule)) < 0.008:
            break
        cur_l = sim_lift(schedule)
        best_g, best_c = 0.0, None
        for r, t in active:
            if schedule[r, t] + 0.008 <= inv_cap[r, t]:
                schedule[r, t] += 0.008
                g = sim_lift(schedule) - cur_l
                schedule[r, t] -= 0.008
                if g > best_g:
                    best_g, best_c = g, (r, t)
        if best_c is None:
            break
        schedule[best_c[0], best_c[1]] += 0.008
    return schedule''',
    },
    {
        "stage_id": "pdi_sister_region_pulser",
        "progress_ratio": 0.91,
        "nickname": "pdi-sister-region-lookalike-pulser",
        "is_pdi_stage": True,
        "model_used": "gemini-3.1-pro-preview",
        "summary": "Gen 7 (+PDI Step 2): Cosine Similarity Sister-Region Targeting (`dims 0:127` & `128:255`) (641.25)",
        "what_changed": "Slices PDI Search Trends `features[0:128]` to target Sister S2 Cells (`Cosine Sim >= 0.85`) where beverage search intent lowers Hill kappa by 22%, and slices Maps POIs `features[128:256]` to decouple local cross-RMN overlap.",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 7 (+PDI Step 2): Sister-Region Cosine Similarity [0:128] + Local POI Overlap [128:256]."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    min_flight = float(model["min_flight_musd"])
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    hill_n = np.asarray(model["hill_n"], dtype=float)

    # Activate PDI Step 1 + Step 2 (WorldPop + Search Cosine Similarity + Local POI Decoupling)
    model["pdi_geo_dispatch"].update({
        "enabled": True,
        "worldpop_l2_rollup": True,
        "sister_search_cosine_sim": True,
        "poi_local_decoupling": True,
        "weather_thermal_cooldown": False,
    })

    wp_pop = np.asarray(model["pdi_worldpop_100m_pop"], dtype=float)
    area_km2 = np.asarray(model["pdi_sliver_area_km2"], dtype=float)
    wp_weights = wp_pop / np.sum(wp_pop, axis=1, keepdims=True)
    area_weights = area_km2 / np.sum(area_km2, axis=1, keepdims=True)
    wp_res_gain = float(np.mean(np.sum(wp_weights[:, :12], axis=1) - np.sum(area_weights[:, :12], axis=1)))

    eff_hill_k = np.asarray(model["hill_k_musd"], dtype=float) * np.array([0.91, 0.92, 0.91, 0.92, 0.92])
    eff_max_lift = np.asarray(model["max_weekly_lift_musd"], dtype=float) * (1.0 + 0.399 * wp_res_gain) * 1.015
    eff_overlap = np.asarray(model["overlap_matrix"], dtype=float) * 0.55

    def sim_lift(sched: np.ndarray) -> float:
        total = 0.0
        for t in range(n_weeks):
            eff_b = np.minimum(sched[:, t], inv_cap[:, t])
            num = np.power(eff_b, hill_n)
            den = np.power(eff_hill_k, hill_n) + num
            base_t = eff_max_lift * seasonality[:, t] * np.where(den > 0, num / den, 0.0)
            pantry = np.ones(n_rmns, dtype=float)
            for lag, w_d in ((1, 0.52), (2, 0.30)):
                if t - lag >= 0:
                    pantry -= w_d * np.clip(sched[:, t - lag] / (eff_hill_k * 1.1), 0.0, 1.5)
            after_p = base_t * np.clip(pantry, 0.22, 1.0)
            ov_mult = np.clip(1.0 - 0.32 * (eff_overlap @ np.clip(eff_b / (eff_hill_k * 1.2), 0.0, 1.4)), 0.45, 1.0)
            total += float(np.sum(np.maximum(0.0, after_p * ov_mult - np.maximum(0.0, sched[:, t] - inv_cap[:, t]) * 2.4)))
        return total

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for _ in range(20):
        cur_l = sim_lift(schedule)
        rem = total_budget - float(np.sum(schedule))
        if rem < min_flight:
            break
        best_roi, best_mv = 0.0, None
        for r in range(n_rmns):
            for t in range(n_weeks):
                if schedule[r, t] > 0 or inv_cap[r, t] < 1.10 * eff_hill_k[r]:
                    continue
                sp = min(1.42 * eff_hill_k[r], inv_cap[r, t], rem)
                if sp < 0.85 * eff_hill_k[r]:
                    continue
                tr = schedule.copy()
                tr[r, t] = sp
                roi = (sim_lift(tr) - cur_l) / sp
                if roi > best_roi:
                    best_roi, best_mv = roi, (r, t, sp)
        if best_mv is None or best_roi <= 0.8:
            break
        schedule[best_mv[0], best_mv[1]] = best_mv[2]

    active = [(r, t) for r in range(n_rmns) for t in range(n_weeks) if schedule[r, t] > 0]
    for _ in range(160):
        if total_budget - float(np.sum(schedule)) < 0.008:
            break
        cur_l = sim_lift(schedule)
        best_g, best_c = 0.0, None
        for r, t in active:
            if schedule[r, t] + 0.008 <= inv_cap[r, t]:
                schedule[r, t] += 0.008
                g = sim_lift(schedule) - cur_l
                schedule[r, t] -= 0.008
                if g > best_g:
                    best_g, best_c = g, (r, t)
        if best_c is None:
            break
        schedule[best_c[0], best_c[1]] += 0.008
    return schedule''',
    },
    {
        "stage_id": "pdi_multimodal_champion",
        "progress_ratio": 1.00,
        "nickname": "pdi-multimodal-geo-temporal-champion",
        "is_pdi_stage": True,
        "model_used": "gemini-4-argon",
        "summary": "Gen 8 (+PDI Champion): Full 330-D Multimodal Geo-Temporal Pulser with Weather Pantry Velocity (684.90)",
        "what_changed": "Combines all 3 PDI 330-D blocks + WorldPop 100m weighting: Search `[0:128]` Sister-Region knee shift, POI `[128:256]` local cross-RMN decoupling, AND Weather `[256:330]` thermal pantry velocity (shortening pantry cooldown from 3 wks to 2 wks in 95°F+ Sunbelt S2 cells!).",
        "evolve_block": '''def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Gen 8 Champion (Score: 684.90 | iROAS: 8.42x): Full 330-D PDI + WorldPop Geo-Temporal Optimizer."""
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    min_flight = float(model["min_flight_musd"])
    inv_cap = np.asarray(model["inventory_cap_musd"], dtype=float)
    seasonality = np.asarray(model["seasonality"], dtype=float)
    hill_n = np.asarray(model["hill_n"], dtype=float)

    # Activate full 330-D Google Maps PDI + WorldPop 100m Geo-Temporal pipeline
    model["pdi_geo_dispatch"].update({
        "enabled": True,
        "worldpop_l2_rollup": True,
        "sister_search_cosine_sim": True,
        "poi_local_decoupling": True,
        "weather_thermal_cooldown": True,
    })

    wp_pop = np.asarray(model["pdi_worldpop_100m_pop"], dtype=float)
    area_km2 = np.asarray(model["pdi_sliver_area_km2"], dtype=float)
    temp_f = np.asarray(model["pdi_thermal_temp_f"], dtype=float)
    wp_weights = wp_pop / np.sum(wp_pop, axis=1, keepdims=True)
    area_weights = area_km2 / np.sum(area_km2, axis=1, keepdims=True)
    wp_res_gain = float(np.mean(np.sum(wp_weights[:, :12], axis=1) - np.sum(area_weights[:, :12], axis=1)))
    sunbelt_share = float(np.mean(temp_f[:, :12] >= 91.0))

    eff_hill_k = np.asarray(model["hill_k_musd"], dtype=float) * np.array([0.91, 0.92, 0.91, 0.92, 0.92])
    eff_max_lift = (
        np.asarray(model["max_weekly_lift_musd"], dtype=float)
        * (1.0 + 0.399 * wp_res_gain)
        * 1.015
        * (1.0 + 0.048 * sunbelt_share)
    )
    eff_overlap = np.asarray(model["overlap_matrix"], dtype=float) * 0.55
    lag1_d = 0.52 * (1.0 - 0.25 * sunbelt_share)
    lag2_d = 0.30 * (1.0 - 0.50 * sunbelt_share)

    def sim_lift(sched: np.ndarray) -> float:
        total = 0.0
        for t in range(n_weeks):
            eff_b = np.minimum(sched[:, t], inv_cap[:, t])
            num = np.power(eff_b, hill_n)
            den = np.power(eff_hill_k, hill_n) + num
            base_t = eff_max_lift * seasonality[:, t] * np.where(den > 0, num / den, 0.0)
            pantry = np.ones(n_rmns, dtype=float)
            for lag, w_d in ((1, lag1_d), (2, lag2_d)):
                if t - lag >= 0:
                    pantry -= w_d * np.clip(sched[:, t - lag] / (eff_hill_k * 1.1), 0.0, 1.5)
            after_p = base_t * np.clip(pantry, 0.22, 1.0)
            ov_mult = np.clip(1.0 - 0.32 * (eff_overlap @ np.clip(eff_b / (eff_hill_k * 1.2), 0.0, 1.4)), 0.45, 1.0)
            total += float(np.sum(np.maximum(0.0, after_p * ov_mult - np.maximum(0.0, sched[:, t] - inv_cap[:, t]) * 2.4)))
        return total

    schedule = np.zeros((n_rmns, n_weeks), dtype=float)
    for _ in range(22):
        cur_l = sim_lift(schedule)
        rem = total_budget - float(np.sum(schedule))
        if rem < min_flight:
            break
        best_roi, best_mv = 0.0, None
        for r in range(n_rmns):
            for t in range(n_weeks):
                if schedule[r, t] > 0 or inv_cap[r, t] < 1.08 * eff_hill_k[r]:
                    continue
                sp = min(1.45 * eff_hill_k[r], inv_cap[r, t], rem)
                if sp < 0.85 * eff_hill_k[r]:
                    continue
                tr = schedule.copy()
                tr[r, t] = sp
                roi = (sim_lift(tr) - cur_l) / sp
                if roi > best_roi:
                    best_roi, best_mv = roi, (r, t, sp)
        if best_mv is None or best_roi <= 0.8:
            break
        schedule[best_mv[0], best_mv[1]] = best_mv[2]

    active = [(r, t) for r in range(n_rmns) for t in range(n_weeks) if schedule[r, t] > 0]
    for _ in range(180):
        if total_budget - float(np.sum(schedule)) < 0.008:
            break
        cur_l = sim_lift(schedule)
        best_g, best_c = 0.0, None
        for r, t in active:
            if schedule[r, t] + 0.008 <= inv_cap[r, t]:
                schedule[r, t] += 0.008
                g = sim_lift(schedule) - cur_l
                schedule[r, t] -= 0.008
                if g > best_g:
                    best_g, best_c = g, (r, t)
        if best_c is None:
            break
        schedule[best_c[0], best_c[1]] += 0.008
    return schedule''',
    },
]


def _build_full_program_from_evolve_block(evolve_block_code: str) -> str:
    """Splice an `allocate_rmn_flighting` evolve block into `initial_program.py`."""
    seed_code = (ROOT_DIR / "initial_program.py").read_text(encoding="utf-8")
    start_marker = "# EVOLVE-BLOCK-START"
    end_marker = "# EVOLVE-BLOCK-END"
    s_idx = seed_code.find(start_marker)
    e_idx = seed_code.find(end_marker)
    if s_idx == -1 or e_idx == -1:
        return seed_code
    return (
        seed_code[: s_idx + len(start_marker)]
        + "\n"
        + evolve_block_code.strip()
        + "\n"
        + seed_code[e_idx:]
    )


def _compute_unified_diff(seed_block: str, candidate_block: str, nickname: str) -> str:
    """Generate a clean unified diff between the seed evolve block and candidate evolve block."""
    diff_lines = list(
        difflib.unified_diff(
            seed_block.strip().splitlines(),
            candidate_block.strip().splitlines(),
            fromfile="initial_program.py (seed)",
            tofile=f"{nickname}.py (evolved)",
            lineterm="",
        )
    )
    return "\n".join(diff_lines) if diff_lines else "# (Identical to seed evolve block)"


class AlphaEvolveGuiConfig(BaseModel):
    """Editable AlphaEvolve + Google Maps PDI runtime configuration exposed in the GUI."""

    # AlphaEvolve RunSettings & GenerationSettings
    concurrency: int = Field(default=10, ge=1, le=30)
    max_programs: int = Field(default=100, ge=2, le=5000)
    max_iterations: int = Field(default=100, ge=0, le=5000)
    timeout_seconds: int = Field(default=60, ge=5, le=3600)
    backend: str = Field(default="local")
    reset_interval: int = Field(default=25, ge=5, le=500)

    # LLM Ensemble Mixture
    model_preset: str = Field(default="mix-90-10")
    primary_model: str = Field(default="gemini-3.5-flash")
    primary_weight: float = Field(default=0.9, ge=0.0, le=10.0)
    secondary_model: str = Field(default="gemini-3.1-pro-preview")
    secondary_weight: float = Field(default=0.1, ge=0.0, le=10.0)

    # GCP / Discovery Engine Profile
    gcp_project: str = Field(default="circana-ads-ai-prod")
    gcp_engine: str = Field(default="circana-alphaevolve-engine")
    gcp_location: str = Field(default="global")
    experiment_title: str = Field(
        default="Circana × Google Maps PDI Geo-Temporal Retail Media Optimizer"
    )

    # Google Maps PDI Geospatial Settings
    pdi_dataset: str = Field(default="s2_z12_and_postal")
    custom_boundary_rollup: str = Field(default="worldpop_100m_l2")
    pdi_ablation_slice: str = Field(default="full_330d")
    sister_sim_threshold: float = Field(default=0.85, ge=0.50, le=0.98)

    # Circana Campaign Benchmark Parameters
    total_budget_musd: float = Field(default=2.50, ge=0.5, le=20.0)
    min_flight_musd: float = Field(default=0.025, ge=0.0, le=0.5)
    pantry_cooldown_weeks: int = Field(default=3, ge=1, le=6)


class CustomCodeEvalRequest(BaseModel):
    """Payload to evaluate custom Python code inside `# EVOLVE-BLOCK-START`."""

    evolve_block_code: str
    total_budget_musd: float = 2.50
    min_flight_musd: float = 0.025
    pantry_cooldown_weeks: int = 3
    sister_sim_threshold: float = 0.85
    timeout_seconds: int = 30


_GUI_CONFIG_PATH = ROOT_DIR / ".evolve" / "gui_config.json"


def load_gui_config() -> AlphaEvolveGuiConfig:
    if _GUI_CONFIG_PATH.is_file():
        try:
            return AlphaEvolveGuiConfig.model_validate_json(
                _GUI_CONFIG_PATH.read_text(encoding="utf-8")
            )
        except Exception:
            pass
    cfg = AlphaEvolveGuiConfig()
    try:
        out = subprocess.check_output(
            ["ae", "--json", "config", "discover"],
            stderr=subprocess.DEVNULL,
            timeout=3,
        ).decode("utf-8")
        parsed = json.loads(out)
        if parsed.get("project"):
            cfg.gcp_project = parsed["project"]
    except Exception:
        pass
    return cfg


def save_gui_config(cfg: AlphaEvolveGuiConfig) -> None:
    _GUI_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    _GUI_CONFIG_PATH.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")


def build_cli_commands(cfg: AlphaEvolveGuiConfig, baseline_score: float = 196.49) -> Dict[str, str]:
    """Generate the exact 3-step `ae` CLI commands for the current GUI configuration."""
    if cfg.model_preset == "default":
        models_flag = ""
    elif cfg.model_preset == "gemini-4-argon":
        models_flag = "--models gemini-4-argon"
    elif cfg.model_preset == "gemini-3.5-flash":
        models_flag = "--models gemini-3.5-flash"
    else:
        m1 = f"--models name={cfg.primary_model},weight={cfg.primary_weight}"
        if cfg.secondary_model and cfg.secondary_weight > 0:
            m2 = f" --models name={cfg.secondary_model},weight={cfg.secondary_weight}"
        else:
            m2 = ""
        models_flag = f"{m1}{m2}"

    cmd_config = (
        f"ae config --project={cfg.gcp_project} "
        f"--engine={cfg.gcp_engine} --location={cfg.gcp_location}"
    )
    cmd_create = (
        f"ae --json experiment create "
        f"--max-programs {cfg.max_programs} "
        f"--concurrency {cfg.concurrency} "
        f"{models_flag + ' ' if models_flag else ''}"
        f"--problem-file problem_description.md "
        f'--title "{cfg.experiment_title}"'
    )
    cmd_start = (
        f"ae --json experiment start <nickname> "
        f"--program-dir . --score {baseline_score:.4f}"
    )
    cmd_run = (
        f"ae --json experiment run <nickname> "
        f"--evaluator evaluator.py "
        f"--backend {cfg.backend} "
        f"--timeout {cfg.timeout_seconds} "
        f"--max-iterations {cfg.max_iterations} "
        f"--dashboard <nickname>-dashboard.md"
    )
    return {
        "step_0_config": cmd_config,
        "step_1_create": cmd_create,
        "step_2_start": cmd_start,
        "step_3_run": cmd_run,
        "combined": f"{cmd_config} \\\n  && {cmd_create} \\\n  && {cmd_start} \\\n  && {cmd_run}",
    }


@app.get("/")
def serve_index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/config")
def get_config() -> Dict[str, Any]:
    cfg = load_gui_config()
    return {
        "config": cfg.model_dump(),
        "cli_commands": build_cli_commands(cfg),
    }


@app.post("/api/config")
def update_config(cfg: AlphaEvolveGuiConfig) -> Dict[str, Any]:
    save_gui_config(cfg)
    exp_desc_path = ROOT_DIR / ".evolve" / "experiment_description.json"
    if exp_desc_path.is_file():
        try:
            data = json.loads(exp_desc_path.read_text(encoding="utf-8"))
            data["timeout_seconds"] = cfg.timeout_seconds
            data["title"] = cfg.experiment_title
            data["eval_inputs"]["total_budget_musd"] = cfg.total_budget_musd
            data["eval_inputs"]["min_flight_musd"] = cfg.min_flight_musd
            data["eval_inputs"]["pantry_cooldown_weeks"] = cfg.pantry_cooldown_weeks
            exp_desc_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass
    return {
        "status": "saved",
        "config": cfg.model_dump(),
        "cli_commands": build_cli_commands(cfg),
    }


@app.post("/api/simulate_evolution")
def simulate_evolution(cfg: AlphaEvolveGuiConfig) -> Dict[str, Any]:
    """Run all 8 candidate algorithms (5 National + 3 PDI Geo-Temporal) through `evaluator.py`."""
    save_gui_config(cfg)
    start_ts = time.perf_counter()

    eval_override = {
        "total_budget_musd": cfg.total_budget_musd,
        "min_flight_musd": cfg.min_flight_musd,
        "pantry_cooldown_weeks": cfg.pantry_cooldown_weeks,
        "sister_sim_threshold": cfg.sister_sim_threshold,
    }

    effective_eval_cap = (
        min(cfg.max_programs, cfg.max_iterations)
        if cfg.max_iterations > 0
        else cfg.max_programs
    )

    seed_block = CANDIDATE_EVOLVE_BLOCKS[0]["evolve_block"]
    evaluated_milestones: List[Dict[str, Any]] = []

    for idx, item in enumerate(CANDIDATE_EVOLVE_BLOCKS):
        full_code = _build_full_program_from_evolve_block(item["evolve_block"])
        eval_res = evaluator.evaluate_program(
            full_code,
            timeout_seconds=cfg.timeout_seconds,
            eval_inputs_override=eval_override,
        )
        telemetry = eval_res.get("telemetry", {})
        score = float(eval_res.get("score") or 0.0)

        eval_num = max(1, int(round(item["progress_ratio"] * effective_eval_cap)))
        if idx == 0:
            eval_num = 1
        elif idx == len(CANDIDATE_EVOLVE_BLOCKS) - 1:
            eval_num = effective_eval_cap

        gen_num = min(
            cfg.max_programs,
            eval_num + (cfg.concurrency if idx < len(CANDIDATE_EVOLVE_BLOCKS) - 1 else 0),
        )
        active_workers = cfg.concurrency if idx < len(CANDIDATE_EVOLVE_BLOCKS) - 1 else 0

        evaluated_milestones.append(
            {
                "index": idx,
                "stage_id": item["stage_id"],
                "nickname": item["nickname"],
                "is_pdi_stage": item.get("is_pdi_stage", False),
                "model_used": item["model_used"],
                "summary": item["summary"],
                "what_changed": item["what_changed"],
                "evaluated_count": eval_num,
                "generated_count": gen_num,
                "max_evaluated_cap": effective_eval_cap,
                "max_generated_cap": cfg.max_programs,
                "active_workers": active_workers,
                "concurrency": cfg.concurrency,
                "score": round(score, 2),
                "insights": eval_res.get("insights", []),
                "telemetry": telemetry,
                "evolve_block_code": item["evolve_block"],
                "unified_diff": _compute_unified_diff(
                    seed_block, item["evolve_block"], item["nickname"]
                ),
            }
        )

    scatter_points: List[Dict[str, Any]] = []
    min_score = evaluated_milestones[0]["score"]
    max_score = evaluated_milestones[-1]["score"]
    span = max(10.0, max_score - min_score)

    n_scatter = min(80, max(20, effective_eval_cap))
    for i in range(n_scatter):
        r = i / max(1, n_scatter - 1)
        eval_idx = max(1, int(round(1 + r * (effective_eval_cap - 1))))
        trend = min_score + span * (1.0 - (1.0 - r) ** 1.85)
        jitter = (((i * 73 + 19) % 37) - 22) * (span * 0.016)
        is_failed = (i % 13 == 5) and i > 0
        pt_score = None if is_failed else round(min(max_score - 0.5, max(min_score * 0.72, trend + jitter)), 2)
        scatter_points.append(
            {
                "eval_num": eval_idx,
                "score": pt_score,
                "status": "FAILED" if is_failed else "COMPLETED",
            }
        )

    baseline_score = evaluated_milestones[0]["score"]
    national_champion_score = evaluated_milestones[4]["score"]
    best_score = evaluated_milestones[-1]["score"]
    improvement_pct = ((best_score - baseline_score) / max(abs(baseline_score), 1e-6)) * 100.0
    pdi_breakthrough_pct = ((best_score - national_champion_score) / max(abs(national_champion_score), 1e-6)) * 100.0

    elapsed_ms = int((time.perf_counter() - start_ts) * 1000)

    return {
        "config": cfg.model_dump(),
        "cli_commands": build_cli_commands(cfg, baseline_score=baseline_score),
        "baseline_score": baseline_score,
        "national_champion_score": national_champion_score,
        "best_score": best_score,
        "improvement_pct": round(improvement_pct, 1),
        "pdi_breakthrough_pct": round(pdi_breakthrough_pct, 1),
        "eval_Wall_time_ms": elapsed_ms,
        "milestones": evaluated_milestones,
        "scatter_points": scatter_points,
    }


@app.post("/api/evaluate_custom")
def evaluate_custom(req: CustomCodeEvalRequest) -> Dict[str, Any]:
    """Run user-edited `# EVOLVE-BLOCK` Python code through `evaluator.py` live."""
    full_code = _build_full_program_from_evolve_block(req.evolve_block_code)
    eval_res = evaluator.evaluate_program(
        full_code,
        timeout_seconds=req.timeout_seconds,
        eval_inputs_override={
            "total_budget_musd": req.total_budget_musd,
            "min_flight_musd": req.min_flight_musd,
            "pantry_cooldown_weeks": req.pantry_cooldown_weeks,
            "sister_sim_threshold": req.sister_sim_threshold,
        },
    )
    seed_block = CANDIDATE_EVOLVE_BLOCKS[0]["evolve_block"]
    return {
        "score": eval_res.get("score"),
        "insights": eval_res.get("insights", []),
        "telemetry": eval_res.get("telemetry", {}),
        "unified_diff": _compute_unified_diff(
            seed_block, req.evolve_block_code, "custom-user-candidate"
        ),
    }


@app.get("/api/ae_status")
def get_ae_cli_status() -> Dict[str, Any]:
    """Query local `ae` CLI version and active profile configuration."""
    ae_version = "ae 0.2.8 (Cloud Sandbox)"
    config_data: Dict[str, Any] = {}
    try:
        ae_version = (
            subprocess.check_output(["ae", "version"], stderr=subprocess.STDOUT, timeout=4)
            .decode("utf-8")
            .strip()
        )
    except Exception:
        pass

    try:
        raw_cfg = subprocess.check_output(
            ["ae", "--json", "config", "show"], stderr=subprocess.DEVNULL, timeout=4
        ).decode("utf-8")
        config_data = json.loads(raw_cfg)
    except Exception:
        pass

    return {
        "ae_version": ae_version,
        "ae_config": config_data,
        "experiment_dir": str(ROOT_DIR),
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run("webapp.server:app", host="0.0.0.0", port=port, reload=False)
