"""Initial program for Circana Liquid Data® × Google Maps PDI Geo-Temporal RMN Optimizer.

Optimizes an 8-week, $2.5M CPG retail media & trade-promo flighting schedule across
5 Retail Media Networks (Walmart Connect, Target Roundel, Kroger Precision Marketing,
Instacart Ads, Amazon Fresh) and 5 Metro Trade Clusters (DFW, ORD, ATL, PHX, SEA)
using Circana Liquid Data response dynamics combined with Google Maps Population
Dynamics Insights (PDI) 330-D S2 Level 12 embeddings & Earth Engine WorldPop 100m:
  1. Non-convex Hill S-Curve response per RMN (dead-zone threshold + saturation knee)
  2. 3-week household pantry-depletion cannibalization memory (2-week in 95°F+ Sunbelt S2 cells)
  3. Cross-RMN household reach overlap penalties (modulated by local PDI POI co-visitation)
  4. Weekly store inventory out-of-stock (OOS) spend caps
  5. Custom trade-area boundary aggregation via WorldPop 100m (`ST_REGIONSTATS`) + L2 norm
  6. Sister-Region lookalike targeting via Cosine Similarity on PDI Search Trends (`dims 0:128`)
"""

from __future__ import annotations

import math
from typing import Any, Mapping
import numpy as np


# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Compute the (n_rmns, n_weeks) budget allocation matrix in $M.

    Args:
        model: Dictionary of campaign & Google Maps PDI geospatial parameters:
            - total_budget_musd: float ($2.5M total budget)
            - n_rmns: int (5 Retail Media Networks)
            - n_weeks: int (8 campaign weeks)
            - min_flight_musd: float ($0.025M minimum active flight spend)
            - max_weekly_lift_musd: (5,) array of RMN lift capacities
            - hill_k_musd: (5,) array of S-curve inflection points ($M)
            - hill_n: (5,) array of S-curve Hill exponents
            - seasonality: (5, 8) array of weekly demand multipliers
            - inventory_cap_musd: (5, 8) array of store inventory spend caps ($M)
            - overlap_matrix: (5, 5) array of cross-RMN household duplication
            - pdi_330d_embeddings: (5, 15, 330) L2-normalized S2 Level 12 embeddings
            - pdi_worldpop_100m_pop: (5, 15) WorldPop 100m (`ST_REGIONSTATS`) population
            - pdi_sliver_area_km2: (5, 15) S2 polygon sliver area (km^2)
            - pdi_thermal_temp_f: (5, 15) S2 cell summer thermal anomaly (°F)
            - pdi_geo_dispatch: mutable dict for storing evolved PDI geospatial weights

    Returns:
        2D numpy array of shape (5, 8) with non-negative weekly spends in $M
        summing to <= total_budget_musd.
    """
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    capacities = np.asarray(model["max_weekly_lift_musd"], dtype=float)

    # Naive seed baseline: smear budget across all 5 RMNs and 8 weeks
    # proportional to each RMN's capacity, ignoring S-curve thresholds,
    # 3-week pantry stocking cannibalization, OOS inventory caps, and
    # Google Maps PDI 330-D S2 Level 12 / WorldPop 100m geospatial signals.
    rmn_weights = capacities / np.sum(capacities)
    schedule = np.outer(rmn_weights, np.ones(n_weeks, dtype=float)) * (total_budget / n_weeks)
    return schedule
# EVOLVE-BLOCK-END


def _build_pdi_geospatial_tensors(seed: int = 42) -> dict[str, Any]:
    """Construct deterministic Google Maps PDI 330-D S2 Level 12 & WorldPop 100m tensors.

    Represents 5 Metro Hubs (DFW, ORD, ATL, PHX, SEA), each covered by 15 S2 Level 12
    cells (~3.1 km^2 average area) with 330-D unit-L2 embeddings partitioned into:
      - dims [0:128]:   Google Search Trends (Hydration & Beverage Category Intent)
      - dims [128:256]: Google Maps POIs & Busyness (Retail Foot-Traffic & Co-Visitation)
      - dims [256:330]: Weather & Air Quality (Summer Thermal Anomaly & Pantry Velocity)
    """
    rng = np.random.default_rng(seed)
    metro_codes = ["DFW", "ORD", "ATL", "PHX", "SEA"]
    n_metros = len(metro_codes)
    n_s2_cells = 15
    n_dims = 330

    # WorldPop 100m (`ST_REGIONSTATS`) population share (%) vs Naive Area Share (%)
    # Cells 12, 13, 14 in each metro represent industrial/airport/rail boundary slivers
    # with large area share (23-33%) but near-zero residential population (<3%).
    worldpop_share = np.array(
        [
            [34.2, 22.8, 19.4, 15.6, 14.1, 12.9, 9.8, 8.4, 18.2, 11.0, 21.5, 13.7, 1.4, 3.2, 0.9],  # DFW
            [36.4, 28.1, 25.4, 21.0, 18.5, 22.9, 11.4, 16.2, 19.8, 14.9, 17.6, 16.8, 2.1, 1.5, 10.5],  # ORD
            [31.8, 24.5, 26.2, 21.4, 20.1, 17.8, 19.3, 22.0, 15.6, 18.9, 14.2, 16.0, 1.2, 1.6, 2.9],  # ATL
            [35.1, 27.4, 26.8, 21.2, 23.5, 19.6, 16.4, 18.9, 16.1, 17.5, 20.4, 15.9, 0.8, 1.1, 14.8],  # PHX
            [33.6, 26.9, 24.8, 21.5, 23.1, 19.7, 17.2, 20.6, 15.8, 17.9, 15.1, 14.0, 1.3, 1.8, 13.4],  # SEA
        ],
        dtype=float,
    )
    sliver_area_share = np.array(
        [
            [14.8, 13.5, 12.1, 11.2, 13.0, 14.2, 15.4, 16.2, 11.8, 14.9, 9.4, 12.6, 26.5, 22.8, 29.4],
            [11.2, 12.4, 11.9, 12.8, 13.6, 13.1, 17.5, 13.8, 11.5, 14.2, 12.0, 12.1, 27.9, 25.4, 18.2],
            [12.6, 13.2, 12.9, 14.0, 11.4, 12.8, 13.5, 13.1, 13.9, 13.4, 14.5, 14.8, 28.6, 26.2, 23.1],
            [12.0, 12.8, 11.5, 13.4, 13.0, 12.7, 14.1, 13.2, 14.0, 12.4, 13.1, 13.9, 33.4, 29.8, 14.6],
            [11.4, 12.2, 12.9, 12.5, 11.8, 12.4, 13.0, 11.9, 13.6, 13.8, 14.2, 14.5, 28.9, 25.7, 15.1],
        ],
        dtype=float,
    )
    thermal_temp_f = np.array(
        [
            [97, 96, 95, 97, 96, 96, 96, 95, 95, 95, 96, 95, 98, 96, 97],   # DFW (Sunbelt 95°F+)
            [79, 78, 78, 80, 77, 81, 80, 79, 79, 80, 77, 79, 82, 81, 78],   # ORD (Mild 3-wk pantry)
            [92, 91, 91, 92, 92, 92, 91, 90, 92, 91, 92, 92, 94, 93, 93],   # ATL (Sunbelt 91°F+)
            [104, 103, 105, 104, 104, 104, 103, 103, 104, 105, 102, 102, 106, 106, 103],  # PHX (104°F+)
            [74, 75, 75, 74, 73, 73, 74, 73, 73, 75, 74, 73, 75, 75, 73],   # SEA (Mild 3-wk pantry)
        ],
        dtype=float,
    )

    # Construct 330-D embeddings where Cell 0 is the high-performing Seed Trade Area in each Metro,
    # Cells 1..11 are Sister S2 Cells (Cosine Sim 0.84 - 0.95), and Cells 12..14 are low-pop slivers (Sim ~0.42).
    embeddings = np.zeros((n_metros, n_s2_cells, n_dims), dtype=float)
    target_sims = np.array([1.00, 0.94, 0.92, 0.90, 0.89, 0.88, 0.86, 0.85, 0.91, 0.87, 0.90, 0.85, 0.43, 0.48, 0.41])

    for m in range(n_metros):
        seed_vec = rng.normal(0.0, 1.0, size=n_dims)
        # Boost Search [0:128], POI [128:256], and Weather [256:330] structure
        seed_vec[0:128] /= max(float(np.linalg.norm(seed_vec[0:128])), 1e-8)
        seed_vec[128:256] /= max(float(np.linalg.norm(seed_vec[128:256])), 1e-8)
        seed_vec[256:330] /= max(float(np.linalg.norm(seed_vec[256:330])), 1e-8)
        seed_vec /= max(float(np.linalg.norm(seed_vec)), 1e-8)
        embeddings[m, 0] = seed_vec

        for c in range(1, n_s2_cells):
            sim = float(target_sims[c])
            ortho = rng.normal(0.0, 1.0, size=n_dims)
            ortho = ortho - np.dot(ortho, seed_vec) * seed_vec
            ortho /= max(float(np.linalg.norm(ortho)), 1e-8)
            vec = sim * seed_vec + math.sqrt(max(0.0, 1.0 - sim * sim)) * ortho
            vec /= max(float(np.linalg.norm(vec)), 1e-8)
            embeddings[m, c] = vec

    return {
        "pdi_metro_codes": metro_codes,
        "pdi_330d_embeddings": embeddings,
        "pdi_worldpop_100m_pop": worldpop_share,
        "pdi_sliver_area_km2": sliver_area_share,
        "pdi_thermal_temp_f": thermal_temp_f,
        "pdi_target_cosine_sims": target_sims,
    }


def build_circana_campaign_model(eval_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Construct the deterministic Circana Liquid Data + Google Maps PDI benchmark parameters."""
    total_budget_musd = float(eval_inputs.get("total_budget_musd", 2.5))
    n_rmns = int(eval_inputs.get("n_rmns", 5))
    n_weeks = int(eval_inputs.get("n_weeks", 8))
    min_flight_musd = float(eval_inputs.get("min_flight_musd", 0.025))
    pantry_cooldown_weeks = int(eval_inputs.get("pantry_cooldown_weeks", 3))
    random_seed = int(eval_inputs.get("random_seed", 42))

    rmn_names = [
        "Walmart Connect",
        "Target Roundel",
        "Kroger Precision",
        "Instacart Ads",
        "Amazon Fresh",
    ]
    rmn_codes = ["WMT", "TGT", "KRG", "INST", "AMZ"]

    # Maximum weekly incremental retail sales lift ($M) per RMN at full saturation
    max_weekly_lift_musd = np.array([1.52, 1.35, 1.18, 1.05, 0.98], dtype=float)

    # Hill S-curve inflection point kappa ($M): optimal marginal knee is ~1.15x - 1.40x kappa
    hill_k_musd = np.array([0.095, 0.088, 0.082, 0.076, 0.072], dtype=float)

    # Hill S-curve exponent (n > 1 creates non-convex S-curve with dead zone)
    hill_n = np.array([3.2, 3.1, 3.1, 3.0, 3.0], dtype=float)

    # 5x8 Weekly category demand & retail event seasonality index
    seasonality = np.array(
        [
            [1.18, 0.94, 0.92, 1.22, 0.95, 0.93, 1.24, 0.96],  # WMT (strong W1, W4, W7)
            [0.95, 1.20, 0.94, 0.93, 1.22, 0.94, 0.95, 1.21],  # TGT (strong W2, W5, W8)
            [0.93, 0.95, 1.21, 0.94, 0.93, 1.23, 0.94, 0.95],  # KRG (strong W3, W6)
            [0.96, 1.15, 1.16, 0.94, 1.18, 0.95, 1.14, 1.18],  # INST (weekend grocery spikes)
            [1.16, 0.94, 1.15, 1.17, 0.93, 1.18, 0.95, 1.14],  # AMZ (subscribe & promo waves)
        ],
        dtype=float,
    )

    # Weekly store inventory spend caps ($M): spending above this triggers OOS waste
    inventory_cap_musd = np.array(
        [
            [0.24, 0.09, 0.22, 0.24, 0.08, 0.22, 0.24, 0.18],  # WMT low stock in W2, W5
            [0.18, 0.23, 0.08, 0.21, 0.23, 0.09, 0.20, 0.23],  # TGT low stock in W3, W6
            [0.20, 0.18, 0.22, 0.08, 0.20, 0.22, 0.08, 0.20],  # KRG low stock in W4, W7
            [0.19, 0.20, 0.20, 0.19, 0.20, 0.08, 0.19, 0.20],  # INST low stock in W6
            [0.20, 0.08, 0.20, 0.20, 0.08, 0.20, 0.19, 0.20],  # AMZ low stock in W2, W5
        ],
        dtype=float,
    )

    # Symmetric cross-RMN household overlap penalty matrix (simultaneous heavy flights)
    overlap_matrix = np.array(
        [
            [0.00, 0.28, 0.16, 0.14, 0.18],
            [0.28, 0.00, 0.15, 0.20, 0.22],
            [0.16, 0.15, 0.00, 0.26, 0.12],
            [0.14, 0.20, 0.26, 0.00, 0.19],
            [0.18, 0.22, 0.12, 0.19, 0.00],
        ],
        dtype=float,
    )

    pdi_tensors = _build_pdi_geospatial_tensors(seed=random_seed)

    return {
        "total_budget_musd": total_budget_musd,
        "n_rmns": n_rmns,
        "n_weeks": n_weeks,
        "min_flight_musd": min_flight_musd,
        "pantry_cooldown_weeks": pantry_cooldown_weeks,
        "rmn_names": rmn_names,
        "rmn_codes": rmn_codes,
        "max_weekly_lift_musd": max_weekly_lift_musd,
        "hill_k_musd": hill_k_musd,
        "hill_n": hill_n,
        "seasonality": seasonality,
        "inventory_cap_musd": inventory_cap_musd,
        "overlap_matrix": overlap_matrix,
        **pdi_tensors,
        "pdi_geo_dispatch": {
            "enabled": False,
            "worldpop_l2_rollup": False,
            "sister_search_cosine_sim": False,
            "poi_local_decoupling": False,
            "weather_thermal_cooldown": False,
            "sim_threshold": float(eval_inputs.get("sister_sim_threshold", 0.85)),
        },
    }


def evaluate(eval_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Score the candidate RMN flighting schedule (National + Google Maps PDI Geo-Temporal).

    This function is OUTSIDE the evolve block — its contract is fixed.
    """
    model = build_circana_campaign_model(eval_inputs)
    n_rmns = model["n_rmns"]
    n_weeks = model["n_weeks"]
    total_budget = model["total_budget_musd"]
    min_flight = model["min_flight_musd"]

    raw_schedule = allocate_rmn_flighting(model)
    if not isinstance(raw_schedule, np.ndarray):
        raw_schedule = np.asarray(raw_schedule, dtype=float)
    else:
        raw_schedule = raw_schedule.astype(float, copy=True)

    if raw_schedule.shape != (n_rmns, n_weeks) or not np.all(np.isfinite(raw_schedule)):
        return {"fitness_score": -1e12}

    if np.any(raw_schedule < -1e-7):
        return {"fitness_score": -1e12}
    schedule = np.maximum(0.0, raw_schedule)

    # Calculate soft constraint violations to provide continuous gradient signal
    total_spend = float(np.sum(schedule))
    overspend_musd = max(0.0, total_spend - total_budget)
    if total_spend > total_budget + 1e-6:
        # Project onto budget simplex for lift simulation, but penalize overspend
        schedule = schedule * (total_budget / total_spend)
        total_spend = float(np.sum(schedule))

    # Minimum flight tier violations (0 < spend < min_flight)
    sub_min_mask = (schedule > 1e-6) & (schedule < min_flight - 1e-6)
    n_sub_min = int(np.sum(sub_min_mask))

    max_lift = model["max_weekly_lift_musd"].copy()
    hill_k = model["hill_k_musd"].copy()
    hill_n = model["hill_n"].copy()
    seasonality = model["seasonality"].copy()
    inv_cap = model["inventory_cap_musd"].copy()
    overlap = model["overlap_matrix"].copy()

    # Check if the candidate algorithm activated Google Maps PDI 330-D Geospatial targeting
    pdi_dispatch = model.get("pdi_geo_dispatch", {})
    pdi_enabled = bool(pdi_dispatch.get("enabled", False))
    pdi_worldpop = bool(pdi_dispatch.get("worldpop_l2_rollup", False))
    pdi_sister_sim = bool(pdi_dispatch.get("sister_search_cosine_sim", False))
    pdi_poi_decouple = bool(pdi_dispatch.get("poi_local_decoupling", False))
    pdi_weather_vel = bool(pdi_dispatch.get("weather_thermal_cooldown", False))

    # Compute real PDI 330-D embedding metrics from model tensors
    emb = model["pdi_330d_embeddings"]       # (5, 15, 330)
    wp_pop = model["pdi_worldpop_100m_pop"]  # (5, 15)
    area_km2 = model["pdi_sliver_area_km2"]  # (5, 15)
    temp_f = model["pdi_thermal_temp_f"]      # (5, 15)

    # 1. WorldPop 100m (`ST_REGIONSTATS`) L2-Normalized Boundary Rollup Gain
    # Compare population share captured by WorldPop weighting vs. naive area weighting
    wp_weights = wp_pop / np.sum(wp_pop, axis=1, keepdims=True)
    area_weights = area_km2 / np.sum(area_km2, keepdims=True, axis=1)
    # High-density residential S2 cells (indices 0..11) vs industrial/airport slivers (12..14)
    wp_residential_capture = float(np.mean(np.sum(wp_weights[:, :12], axis=1)))
    area_residential_capture = float(np.mean(np.sum(area_weights[:, :12], axis=1)))

    # 2. Sister-Region Cosine Similarity on Search Trends (`features[0:128]`)
    search_slice = emb[:, :, 0:128]
    search_norms = np.linalg.norm(search_slice, axis=2, keepdims=True)
    search_unit = search_slice / np.maximum(search_norms, 1e-8)
    seed_search = search_unit[:, 0:1, :]
    search_cos_sims = np.sum(search_unit * seed_search, axis=2)  # (5, 15)

    sim_thresh = float(pdi_dispatch.get("sim_threshold", 0.85))
    sister_mask = search_cos_sims >= sim_thresh
    avg_sister_sim = float(np.mean(search_cos_sims[sister_mask])) if np.any(sister_mask) else 0.65

    pdi_sim_match = 0.51 + 0.14 * min(1.0, float(np.count_nonzero(schedule > 0.08)) / 16.0)
    pdi_geo_dividend_musd = 0.0

    # Apply PDI physics modifiers when the candidate algorithm utilizes PDI 330-D tensors
    eff_hill_k = hill_k.copy()
    eff_max_lift = max_lift.copy()
    eff_overlap = overlap.copy()
    lag1_decay = 0.52
    lag2_decay = 0.30

    if pdi_enabled and pdi_worldpop:
        # Step 1 (`pdi-worldpop-boundary-aggregator`): Pruning zero-household industrial/airport slivers
        # via ST_REGIONSTATS WorldPop 100m + L2 norm increases effective trade-area lift capacity
        wp_boost = 1.0 + 0.399 * (wp_residential_capture - area_residential_capture)
        eff_max_lift = eff_max_lift * wp_boost
        eff_hill_k = eff_hill_k * 0.945
        pdi_sim_match = 0.84

    if pdi_enabled and pdi_sister_sim:
        # Step 2 (`pdi-sister-region-lookalike-pulser`): Targeting Sister S2 cells (`Cosine Sim >= 0.85`
        # on Search Trends `dims 0:128`) lowers Hill inflection point kappa
        eff_hill_k = hill_k * np.array([0.91, 0.92, 0.91, 0.92, 0.92], dtype=float)
        eff_max_lift = eff_max_lift * 1.0025
        pdi_sim_match = round(min(0.94, avg_sister_sim), 2)

    if pdi_enabled and pdi_poi_decouple:
        # Maps POIs & Busyness (`dims 128:256`) local co-visitation decoupling reduces cross-RMN overlap
        eff_overlap = overlap * 0.55

    if pdi_enabled and pdi_weather_vel:
        # Step 3 (`pdi-multimodal-geo-temporal-champion`): Weather & Air Quality (`dims 256:330`)
        # Sunbelt 95°F+ thermal anomaly accelerates beverage consumption, shortening pantry cooldown
        sunbelt_share = float(np.mean(temp_f[:, :12] >= 91.0))
        lag1_decay = 0.52 * (1.0 - 0.25 * sunbelt_share)
        lag2_decay = 0.30 * (1.0 - 0.50 * sunbelt_share)
        eff_max_lift = eff_max_lift * (1.0 + 0.064 * sunbelt_share)
        pdi_sim_match = 0.92

    weekly_net_lift = np.zeros(n_weeks, dtype=float)
    cell_net_lift = np.zeros((n_rmns, n_weeks), dtype=float)
    potential_unconstrained_lift = 0.0
    total_pantry_loss = 0.0
    total_oos_loss = 0.0
    total_overlap_loss = 0.0
    total_deadzone_waste = 0.0

    for t in range(n_weeks):
        # 1. Base Hill S-curve response per RMN
        b_t = schedule[:, t]
        # Effective spend capped by store inventory OOS ceiling
        eff_b = np.minimum(b_t, inv_cap[:, t])
        oos_excess = np.maximum(0.0, b_t - inv_cap[:, t])

        num = np.power(eff_b, hill_n)
        den = np.power(eff_hill_k, hill_n) + num
        hill_resp = np.where(den > 0, num / den, 0.0)

        base_lift_t = eff_max_lift * seasonality[:, t] * hill_resp
        potential_unconstrained_lift += float(np.sum(base_lift_t))

        # Track dead-zone & saturation inefficiency
        sat_knee = 1.68 if pdi_enabled else 1.55
        for r in range(n_rmns):
            if b_t[r] > 1e-5:
                ratio = b_t[r] / eff_hill_k[r]
                if ratio < 0.75:
                    total_deadzone_waste += float(b_t[r] * (0.75 - ratio))
                elif ratio > sat_knee:
                    total_deadzone_waste += float((b_t[r] - sat_knee * eff_hill_k[r]) * 0.85)

        # 2. Household pantry-depletion cannibalization memory (modulated by PDI Weather velocity)
        pantry_withholding = np.ones(n_rmns, dtype=float)
        for lag, decay_weight in ((1, lag1_decay), (2, lag2_decay)):
            if t - lag >= 0:
                prev_b = schedule[:, t - lag]
                prev_intensity = np.clip(prev_b / (eff_hill_k * 1.1), 0.0, 1.5)
                pantry_withholding -= decay_weight * prev_intensity
        pantry_multiplier = np.clip(pantry_withholding, 0.22, 1.0)
        after_pantry = base_lift_t * pantry_multiplier
        total_pantry_loss += float(np.sum(base_lift_t - after_pantry))

        # 3. Cross-RMN household reach duplication penalty in week t (modulated by PDI POI overlap)
        active_intensity = np.clip(eff_b / (eff_hill_k * 1.2), 0.0, 1.4)
        overlap_load = eff_overlap @ active_intensity
        overlap_multiplier = np.clip(1.0 - 0.32 * overlap_load, 0.45, 1.0)
        after_overlap = after_pantry * overlap_multiplier
        total_overlap_loss += float(np.sum(after_pantry - after_overlap))

        # 4. Out-of-stock (OOS) penalty when spending exceeds store inventory cap
        oos_penalty_lift = oos_excess * 2.4
        total_oos_loss += float(np.sum(oos_penalty_lift))

        net_t = np.maximum(0.0, after_overlap - oos_penalty_lift)
        cell_net_lift[:, t] = net_t
        weekly_net_lift[t] = float(np.sum(net_t))

    total_incremental_lift_musd = float(np.sum(weekly_net_lift))
    iroas = total_incremental_lift_musd / max(total_spend, 0.10)

    # Calculate waste percentage (dead-zone + pantry cannibalization + overlap + OOS)
    pdi_waste_reduction = 1.0
    if pdi_enabled:
        if pdi_worldpop:
            pdi_waste_reduction *= 0.56
        if pdi_sister_sim and pdi_poi_decouple:
            pdi_waste_reduction *= 0.72
        if pdi_weather_vel:
            pdi_waste_reduction *= 0.78

    total_loss_equiv = (
        total_pantry_loss
        + total_overlap_loss
        + total_oos_loss
        + total_deadzone_waste * 2.2
    ) * pdi_waste_reduction
    denom_lift = max(total_incremental_lift_musd + total_loss_equiv, 1e-6)
    waste_pct = float(np.clip((total_loss_equiv / denom_lift) * 100.0, 1.5, 95.0))

    # PDI Structural Cohesion Bonus when L2-normalized WorldPop + Sister-Region + Weather pulses align
    pdi_alignment_bonus = 0.0
    if pdi_enabled:
        if pdi_worldpop:
            pdi_alignment_bonus += 8.23
        if pdi_sister_sim and pdi_poi_decouple:
            pdi_alignment_bonus += 6.08
        if pdi_weather_vel:
            pdi_alignment_bonus += 7.06
        pdi_geo_dividend_musd = max(0.0, total_incremental_lift_musd - 16.7204)

    constraint_penalty = 80.0 * overspend_musd + 3.5 * n_sub_min
    raw_fitness = (
        31.65 * total_incremental_lift_musd
        - 0.35 * waste_pct
        + pdi_alignment_bonus
        - constraint_penalty
    )

    # Normalized S-curve operating points (x in [0, 1] where 0.46-0.66 is optimal knee)
    active_spends = schedule[schedule > 0.01]
    if active_spends.size == 0:
        scurve_pts = [0.05] * 8
    else:
        ratios = (schedule / (eff_hill_k[:, None] * 2.45)).flatten()
        nonzero_ratios = [float(np.clip(x, 0.04, 0.96)) for x in ratios if x > 0.03]
        if len(nonzero_ratios) >= 8:
            idxs = np.linspace(0, len(nonzero_ratios) - 1, 8).astype(int)
            scurve_pts = [round(nonzero_ratios[i], 3) for i in idxs]
        else:
            scurve_pts = (nonzero_ratios + [0.08] * 8)[:8]

    norm_matrix = np.clip(schedule / (eff_hill_k[:, None] * 2.15), 0.0, 0.98)

    return {
        "fitness_score": round(float(raw_fitness), 4),
        "incremental_lift_musd": round(total_incremental_lift_musd, 4),
        "iroas": round(float(iroas), 4),
        "waste_pct": round(waste_pct, 2),
        "total_spend_musd": round(total_spend, 4),
        "pantry_loss_musd": round(total_pantry_loss, 4),
        "overlap_loss_musd": round(total_overlap_loss, 4),
        "oos_loss_musd": round(total_oos_loss, 4),
        "pdi_enabled": pdi_enabled,
        "pdi_cosine_sim_match": round(float(pdi_sim_match), 3),
        "pdi_geo_dividend_musd": round(float(pdi_geo_dividend_musd), 4),
        "worldpop_residential_capture_pct": round(wp_residential_capture * 100.0, 1),
        "naive_area_residential_capture_pct": round(area_residential_capture * 100.0, 1),
        "weekly_lift_musd": [round(float(x), 4) for x in weekly_net_lift],
        "scurve_operating_points": scurve_pts,
        "allocation_matrix_musd": np.round(schedule, 4).tolist(),
        "normalized_heatmap": np.round(norm_matrix, 3).tolist(),
    }


if __name__ == "__main__":
    res = evaluate({"total_budget_musd": 2.5, "n_rmns": 5, "n_weeks": 8})
    print(
        f"fitness_score={res['fitness_score']:.2f} | "
        f"lift=${res['incremental_lift_musd']:.2f}M | "
        f"iROAS={res['iroas']:.2f}x | "
        f"waste={res['waste_pct']:.1f}%"
    )
