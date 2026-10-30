"""Initial program for Circana Omni-Channel Retail Media Flighting & iROAS Optimizer.

Optimizes an 8-week, $2.5M CPG retail media & trade-promo flighting schedule across
5 Retail Media Networks (Walmart Connect, Target Roundel, Kroger Precision Marketing,
Instacart Ads, Amazon Fresh) using Circana Liquid Data response dynamics:
  1. Non-convex Hill S-Curve response per RMN (dead-zone threshold + saturation knee)
  2. 3-week household pantry-depletion cannibalization memory
  3. Cross-RMN household reach overlap penalties (simultaneous heavy flights)
  4. Weekly store inventory out-of-stock (OOS) spend caps
  5. Discrete minimum flight spend floor ($25k per active RMN-week)
"""

from __future__ import annotations

import math
from typing import Any, Mapping
import numpy as np


# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    """Compute the (n_rmns, n_weeks) budget allocation matrix in $M.

    Args:
        model: Dictionary of campaign parameters:
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
    # 3-week pantry stocking cannibalization, and OOS inventory caps.
    rmn_weights = capacities / np.sum(capacities)
    schedule = np.outer(rmn_weights, np.ones(n_weeks, dtype=float)) * (total_budget / n_weeks)
    return schedule
# EVOLVE-BLOCK-END


def build_circana_campaign_model(eval_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Construct the deterministic Circana Liquid Data CPG benchmark parameters."""
    total_budget_musd = float(eval_inputs.get("total_budget_musd", 2.5))
    n_rmns = int(eval_inputs.get("n_rmns", 5))
    n_weeks = int(eval_inputs.get("n_weeks", 8))
    min_flight_musd = float(eval_inputs.get("min_flight_musd", 0.025))
    pantry_cooldown_weeks = int(eval_inputs.get("pantry_cooldown_weeks", 3))

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
    }


def evaluate(eval_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Score the candidate RMN flighting schedule.

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

    max_lift = model["max_weekly_lift_musd"]
    hill_k = model["hill_k_musd"]
    hill_n = model["hill_n"]
    seasonality = model["seasonality"]
    inv_cap = model["inventory_cap_musd"]
    overlap = model["overlap_matrix"]

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
        den = np.power(hill_k, hill_n) + num
        hill_resp = np.where(den > 0, num / den, 0.0)

        base_lift_t = max_lift * seasonality[:, t] * hill_resp
        potential_unconstrained_lift += float(np.sum(base_lift_t))

        # Track dead-zone & saturation inefficiency
        for r in range(n_rmns):
            if b_t[r] > 1e-5:
                # Optimal marginal knee on Hill curve is around 1.15 * hill_k[r]
                ratio = b_t[r] / hill_k[r]
                if ratio < 0.75:
                    total_deadzone_waste += float(b_t[r] * (0.75 - ratio))
                elif ratio > 1.55:
                    total_deadzone_waste += float((b_t[r] - 1.55 * hill_k[r]) * 0.85)

        # 2. 3-week household pantry-depletion cannibalization memory
        pantry_Withholding = np.ones(n_rmns, dtype=float)
        for lag, decay_weight in ((1, 0.52), (2, 0.30)):
            if t - lag >= 0:
                prev_b = schedule[:, t - lag]
                prev_intensity = np.clip(prev_b / (hill_k * 1.1), 0.0, 1.5)
                pantry_Withholding -= decay_weight * prev_intensity
        pantry_multiplier = np.clip(pantry_Withholding, 0.22, 1.0)
        after_pantry = base_lift_t * pantry_multiplier
        total_pantry_loss += float(np.sum(base_lift_t - after_pantry))

        # 3. Cross-RMN household reach duplication penalty in week t
        active_intensity = np.clip(eff_b / (hill_k * 1.2), 0.0, 1.4)
        overlap_load = overlap @ active_intensity
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
    total_loss_equiv = (
        total_pantry_loss
        + total_overlap_loss
        + total_oos_loss
        + total_deadzone_waste * 2.2
    )
    denom_lift = max(total_incremental_lift_musd + total_loss_equiv, 1e-6)
    waste_pct = float(np.clip((total_loss_equiv / denom_lift) * 100.0, 1.5, 95.0))

    # Monotonic additive hill-climbing score calibrated so naive seed ~ 100.0
    # and near-optimal staggered dynamic programming ~ 285-300
    constraint_penalty = 80.0 * overspend_musd + 3.5 * n_sub_min
    raw_fitness = (
        31.65 * total_incremental_lift_musd
        - 0.35 * waste_pct
        - constraint_penalty
    )

    # Normalized S-curve operating points (x in [0, 1] where 0.46-0.66 is optimal knee)
    active_spends = schedule[schedule > 0.01]
    if active_spends.size == 0:
        scurve_pts = [0.05] * 8
    else:
        ratios = (schedule / (hill_k[:, None] * 2.65)).flatten()
        nonzero_ratios = [float(np.clip(x, 0.04, 0.96)) for x in ratios if x > 0.03]
        if len(nonzero_ratios) >= 8:
            idxs = np.linspace(0, len(nonzero_ratios) - 1, 8).astype(int)
            scurve_pts = [round(nonzero_ratios[i], 3) for i in idxs]
        else:
            scurve_pts = (nonzero_ratios + [0.08] * 8)[:8]

    # Normalized matrix in [0, 1] for heatmap visualization
    norm_matrix = np.clip(schedule / (hill_k[:, None] * 2.15), 0.0, 0.98)

    return {
        "fitness_score": round(float(raw_fitness), 4),
        "incremental_lift_musd": round(total_incremental_lift_musd, 4),
        "iroas": round(float(iroas), 4),
        "waste_pct": round(waste_pct, 2),
        "total_spend_musd": round(total_spend, 4),
        "pantry_loss_musd": round(total_pantry_loss, 4),
        "overlap_loss_musd": round(total_overlap_loss, 4),
        "oos_loss_musd": round(total_oos_loss, 4),
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
