# Circana Liquid Data® × Google Maps PDI Geo-Temporal Retail Media Flighting & iROAS Optimizer

## Problem Statement

A national CPG brand tracked in **Circana Liquid Data®** has a **$2.50M** promotional and retail media budget (`total_budget_musd = 2.5`) to allocate across **5 Retail Media Networks (RMNs)** (`Walmart Connect`, `Target Roundel`, `Kroger Precision Marketing`, `Instacart Ads`, `Amazon Fresh`) and **5 Metro Trade Clusters** (`DFW`, `ORD`, `ATL`, `PHX`, `SEA`) over an **8-week campaign horizon** (`n_weeks = 8`).

In addition to Circana POS response dynamics, `model` provides **Google Maps Population Dynamics Insights (PDI)** 330-D S2 Level 12 (`v1_s2_z12`) & Postal Code (`v1_postal_codes`) embeddings alongside **Google Earth Engine WorldPop 100m** (`ST_REGIONSTATS`) population rasters.

Your task is to evolve the body of `allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray`, which returns a `(5, 8)` numpy array of weekly ad spends (in `$M`) and activates `model["pdi_geo_dispatch"]` to maximize net incremental retail sales lift (`fitness_score`).

## Formal Specification

For each RMN $r \in \{0, \dots, 4\}$ and week $t \in \{0, \dots, 7\}$, let $b_{r,t} \ge 0$ be the allocated spend in `$M`.

1. **Store Inventory Out-of-Stock (OOS) Cap**:
   Effective spend is capped by weekly store inventory availability $C_{r,t} = \text{inventory\_cap\_musd}[r, t]$:
   $$b^{\text{eff}}_{r,t} = \min(b_{r,t}, C_{r,t}), \quad \text{OOS}_{r,t} = \max(0, b_{r,t} - C_{r,t})$$

2. **Google Maps PDI 330-D & WorldPop 100m Geospatial Dynamics**:
   - **Custom Boundary Aggregation (`WorldPop 100m + L2 Norm`)**: Weighting S2 Level 12 slivers by `pdi_worldpop_100m_pop` (`ST_REGIONSTATS`) instead of naive `pdi_sliver_area_km2` prunes zero-household airport/industrial slivers and boosts residential trade-area lift capacity.
   - **Sister-Region Cosine Similarity (`dims [0:128]` Search Trends)**: Targeting Sister S2 cells with $\text{CosSim}(e^{\text{search}}_c, e^{\text{search}}_{\text{seed}}) \ge 0.85$ lowers the local Hill inflection point $\kappa_r$.
   - **Local POI Co-Visitation (`dims [128:256]` Maps POIs & Busyness)**: Decouples cross-RMN household reach overlap $\Omega_{r,r'}$ in trade areas with low co-visitation.
   - **Thermal Pantry Velocity (`dims [256:330]` Weather & Air Quality)**: In `95°F+` Sunbelt S2 cells (`DFW`, `PHX`, `ATL`), beverage pantry depletion accelerates from 3 weeks to 2 weeks.

3. **Non-Convex Hill S-Curve Response**:
   Each RMN follows a non-convex Hill response with effective inflection $\kappa^{\text{eff}}_r$ and exponent $n_r = \text{hill\_n}[r] > 3$:
   $$\text{BaseLift}_{r,t} = L^{\text{eff}}_{\max, r} \cdot S_{r,t} \cdot \frac{(b^{\text{eff}}_{r,t})^{n_r}}{(\kappa^{\text{eff}}_r)^{n_r} + (b^{\text{eff}}_{r,t})^{n_r}}$$

4. **Household Pantry-Depletion Cannibalization & Cross-RMN Duplication**:
   $$\text{NetLift}_{r,t} = \max\left(0, \text{BaseLift}_{r,t} \cdot P_{r,t} \cdot D_{r,t} - 2.4 \cdot \text{OOS}_{r,t}\right)$$

## Evaluation

- **Metric:** `fitness_score` (`maximize`)
- **Benchmarks:**
  - `Gen 1 Seed (Uniform Smear)`: `196.49` (`+$6.82M` Lift, `2.73x` iROAS, `55.7%` Waste)
  - `Gen 5 National AlphaEvolve Champion (No PDI)`: `522.33` (`+$16.72M` Lift, `6.69x` iROAS)
  - `Gen 8 PDI Multimodal Geo-Temporal Champion`: `684.90` (`+$21.05M` Lift, `8.42x` iROAS, `+31.1%` over National AE)
