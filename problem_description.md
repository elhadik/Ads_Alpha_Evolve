# Circana Omni-Channel Retail Media Flighting & iROAS Optimizer

## Problem Statement

A national CPG brand tracked in **Circana Liquid Data®** has a **$2.50M** promotional and retail media budget (`total_budget_musd = 2.5`) to allocate across **5 Retail Media Networks (RMNs)** (`Walmart Connect`, `Target Roundel`, `Kroger Precision Marketing`, `Instacart Ads`, `Amazon Fresh`) over an **8-week campaign horizon** (`n_weeks = 8`).

Your task is to evolve the body of `allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray`, which returns a `(5, 8)` numpy array of weekly ad spends (in `$M`) that maximizes net incremental retail sales lift (`fitness_score`).

## Formal Specification

For each RMN $r \in \{0, \dots, 4\}$ and week $t \in \{0, \dots, 7\}$, let $b_{r,t} \ge 0$ be the allocated spend in `$M`.

1. **Store Inventory Out-of-Stock (OOS) Cap**:
   Effective spend is capped by weekly store inventory availability $C_{r,t} = \text{inventory\_cap\_musd}[r, t]$:
   $$b^{\text{eff}}_{r,t} = \min(b_{r,t}, C_{r,t}), \quad \text{OOS}_{r,t} = \max(0, b_{r,t} - C_{r,t})$$

2. **Non-Convex Hill S-Curve Response**:
   Each RMN follows a non-convex Hill response with inflection $\kappa_r = \text{hill\_k\_musd}[r]$ and exponent $n_r = \text{hill\_n}[r] > 3$:
   $$\text{BaseLift}_{r,t} = L_{\max, r} \cdot S_{r,t} \cdot \frac{(b^{\text{eff}}_{r,t})^{n_r}}{\kappa_r^{n_r} + (b^{\text{eff}}_{r,t})^{n_r}}$$
   Spending below $0.75 \kappa_r$ falls into the flat dead-zone; spending near $1.15\kappa_r \text{–} 1.45\kappa_r$ achieves maximum marginal iROAS.

3. **3-Week Household Pantry-Depletion Cannibalization**:
   Heavy spend on RMN $r$ in weeks $t-1$ and $t-2$ stocks household pantries, suppressing week-$t$ responsiveness:
   $$P_{r,t} = \text{clip}\left(1 - 0.52 \cdot \text{clip}\left(\frac{b_{r,t-1}}{1.1 \kappa_r}, 0, 1.5\right) - 0.30 \cdot \text{clip}\left(\frac{b_{r,t-2}}{1.1 \kappa_r}, 0, 1.5\right), 0.22, 1.0\right)$$

4. **Cross-RMN Household Duplication Penalty**:
   Simultaneous flights across overlapping retailers in the same week $t$ incur reach duplication according to `overlap_matrix` $\Omega$:
   $$D_{r,t} = \text{clip}\left(1 - 0.32 \sum_{r' \neq r} \Omega_{r, r'} \cdot \text{clip}\left(\frac{b^{\text{eff}}_{r',t}}{1.2 \kappa_{r'}}, 0, 1.4\right), 0.45, 1.0\right)$$

5. **Net Weekly Incremental Lift**:
   $$\text{NetLift}_{r,t} = \max\left(0, \text{BaseLift}_{r,t} \cdot P_{r,t} \cdot D_{r,t} - 2.4 \cdot \text{OOS}_{r,t}\right)$$

## Evaluation

- **Metric:** `fitness_score` (`maximize`)
- **Strategy:** `COMPOSITE_MULTI_OBJECTIVE` — combines total incremental retail sales lift (`incremental_lift_musd`) minus waste percentage (`waste_pct`) and soft constraint penalties for budget overspend or sub-minimum flight tiers (`min_flight_musd = 0.025`).

## Solution Guidance

- **Pulse, don't smear:** Concentrating budget into discrete, high-seasonality flights at the Hill S-curve knee ($\approx 1.25 \kappa_r \text{ to } 1.45 \kappa_r$) strictly dominates uniform weekly spending.
- **Respect the 3-week pantry cycle:** Space active flights on the same RMN by at least 2–3 weeks so `P_{r,t} = 1.0`.
- **Stagger overlapping RMNs across weeks:** Avoid pulsing high-overlap pairs (e.g., Walmart Connect and Target Roundel) in the same week.
- **Never exceed `inventory_cap_musd[r, t]`:** Weeks with low inventory caps ($0.08M\text{–}0.09M$) should be skipped (`0.0`).

