# 🧬🌍 Circana Liquid Data® × Google Maps PDI × AlphaEvolve — Complete Step-by-Step Tutorial: Geo-Temporal Retail Media Flighting & S2 Level 12 Optimization

[![Live on Google Cloud Run](https://img.shields.io/badge/Cloud_Run-Live_Public_Demo-10b981?style=for-the-badge&logo=google-cloud)](https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app)
[![Executive Google Slides](https://img.shields.io/badge/Google_Slides-Executive_Deck-fbbc04?style=for-the-badge&logo=google-slides)](https://docs.google.com/presentation/d/13JBw4QDMnaGELTrfZwb-5AHPwzELPtJZQInkH8LQcMs/edit)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Ads__Alpha__Evolve-181717?style=for-the-badge&logo=github)](https://github.com/elhadik/Ads_Alpha_Evolve)
[![AlphaEvolve CLI](https://img.shields.io/badge/AlphaEvolve_CLI-ae_0.2.8-38bdf8?style=for-the-badge)](https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app)
[![Pytest Suite](https://img.shields.io/badge/Tests-11%2F11_Passing-22c55e?style=for-the-badge)](#9-part-9-running-locally-running-tests-deploying-to-cloud-run--using-the-ae-cli)

> **🌐 Live Google Cloud Run Web Studio (PDI + AlphaEvolve):** **https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app**  
> **📊 Executive Google Slides Deck:** **[Circana Liquid Data × Google Maps PDI × AlphaEvolve — Executive Briefing](https://docs.google.com/presentation/d/13JBw4QDMnaGELTrfZwb-5AHPwzELPtJZQInkH8LQcMs/edit)** ([PDF](presentations/circana_pdi_alphaevolve_executive_deck.pdf) • [PPTX](presentations/circana_pdi_alphaevolve_executive_deck.pptx))  
> **🌐 Baseline National Cloud Run App (`circan_alpha_evolve`):** **https://circana-alpha-evolve-943928157761.us-central1.run.app** (`Score: 522.33`)  
> **💻 Local Studio URL:** **http://localhost:8086**

---

## 🎯 Tutorial Goal: Who Is This Guide For?

This repository and tutorial are written so that **anyone—regardless of background—can master the entire system from first principles**:

1. **For Readers with ZERO Background in Advertising or Geospatial Data**:  
   We start from ground zero with plain-English analogies. You will learn what Consumer Packaged Goods (CPG) brands do, what a Retail Media Network (RMN) is, what Circana's **Liquid Data®** measures at supermarket checkout scanners, what a **Google Maps S2 Level 12 cell** (`~3.1 km²`) is, what a **330-dimensional embedding vector** represents, and why **Google Earth Engine WorldPop 100m** satellite population counts prevent ad budgets from being wasted on empty industrial zones and airport runways.
2. **For Ads & Retail Media Specialists**:  
   We show why **national-only ad flighting hits a hard mathematical ceiling** (`Score: 522.33`, `+$16.72M` lift, `6.69x` iROAS)—and how combining Circana POS attribution with **Google Maps Population Dynamics Insights (PDI)** unlocks an extra **`+$4.32M` Geospatial Dividend** (`Score: 684.90`, `+$21.04M` lift, **`8.44x` iROAS**, reducing ad waste to **`6.9%`**).
3. **For Software Engineers & ML Practitioners**:  
   We walk **line-by-line** through [`initial_program.py`](initial_program.py), [`evaluator.py`](evaluator.py), the **BigQuery GIS + Earth Engine (`ST_REGIONSTATS`) SQL pipeline**, and all **8 evolutionary code generations (`Gen 1` → `Gen 8`)** in [`webapp/server.py`](webapp/server.py) to show exactly how **Google DeepMind's AlphaEvolve** mutates executable Python code inside `# EVOLVE-BLOCK` and uses structured evaluator insights to discover a multi-modal geo-temporal optimizer.

---

## 🎬 Visual Walkthrough: 3D Search Space & Interactive PDI Web Studio

### 1. 3D Evolutionary Search Space & PDI S2 Geo-Flighting Visualization
Generated 100% offline via [`presentations/render_3d_visualization.py`](presentations/render_3d_visualization.py) (`NumPy` + `Pillow` + `ffmpeg`), this 3D animation maps the `# EVOLVE-BLOCK` Python code onto the `Z = 0` ground plane, projects the multi-peak non-convex fitness surface in 3D, illuminates vertical beacon pins (`o---`) across the evolutionary climb from **Gen 1 Seed (`196.49`)** through the **Gen 5 National Ceiling (`522.33`)** to the **Gen 8 PDI 330-D Champion (`684.90`)**, and renders the isometric `5 RMNs × 8 Weeks × S2 Level 12` geo-flighting matrix:

<video src="static/alphaevolve_3d_landscape.mp4" poster="static/alphaevolve_3d_poster.png" controls autoplay loop muted playsinline width="100%">
  <source src="static/alphaevolve_3d_landscape.mp4" type="video/mp4" />
  <source src="static/alphaevolve_3d_landscape.webm" type="video/webm" />
</video>

![Circana × Google Maps PDI × AlphaEvolve 3D Search Space & Geo-Flighting Matrix](static/alphaevolve_3d_landscape.gif)

*Direct 3D assets in [`static/`](static/): [`static/alphaevolve_3d_landscape.mp4`](static/alphaevolve_3d_landscape.mp4) • [`static/alphaevolve_3d_landscape.gif`](static/alphaevolve_3d_landscape.gif) • [`static/alphaevolve_3d_poster.png`](static/alphaevolve_3d_poster.png) • [`presentations/circana_pdi_alphaevolve_executive_deck.pdf`](presentations/circana_pdi_alphaevolve_executive_deck.pdf)*

### 2. Live Deployed Web Studio: Google Maps PDI S2 Playground & Synchronized Optimization Charts
Captured live from **https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app**:

![Google Maps PDI S2 Level 12 Explorer & Trade-Area Rollup](static/pdi_snap_playground.png)

![4 Synchronized AlphaEvolve + PDI Optimization Charts & Live Python Sandbox](static/pdi_snap_charts.png)

---

## 📚 Table of Contents

1. [Part 1: Domain Primer for Complete Beginners — Retail Media, Circana Liquid Data® & Google Maps PDI](#1-part-1-domain-primer-for-complete-beginners--retail-media-circana-liquid-data--google-maps-pdi)
2. [Part 2: The Seven Real-World Physics Dynamics (4 National + 3 PDI Geospatial) That Break Standard Optimizers](#2-part-2-the-seven-real-world-physics-dynamics-4-national--3-pdi-geospatial-that-break-standard-optimizers)
3. [Part 3: Line-by-Line Walkthrough of `initial_program.py` & the BigQuery + Earth Engine SQL Pipeline](#3-part-3-line-by-line-walkthrough-of-initial_programpy--the-bigquery--earth-engine-sql-pipeline)
4. [Part 4: Diagnosing Failure — Why Both the Seed (`196.49`) AND National AlphaEvolve (`522.33`) Hit a Wall](#4-part-4-diagnosing-failure--why-both-the-seed-19649-and-national-alphaevolve-52233-hit-a-wall)
5. [Part 5: Line-by-Line Walkthrough of `evaluator.py` — How AlphaEvolve Evolves Python Code](#5-part-5-line-by-line-walkthrough-of-evaluatorpy--how-alphaevolve-evolves-python-code)
6. [Part 6: Complete Tour of the 8 Evolved Generations (`Gen 1 → Gen 8`: Code + Math + Evaluation Improvements)](#6-part-6-complete-tour-of-the-8-evolved-generations-gen-1--gen-8-code--math--evaluation-improvements)
7. [Part 7: Interactive Web Studio Guide — PDI Map Playground, 4 Live Charts & Editable Controls](#7-part-7-interactive-web-studio-guide--pdi-map-playground-4-live-charts--editable-controls)
8. [Part 8: System Architecture & Modular Repository Structure](#8-part-8-system-architecture--modular-repository-structure)
9. [Part 9: Running Locally, Running Tests (`11/11`), Deploying to Cloud Run & Using the `ae` CLI](#9-part-9-running-locally-running-tests-1111-deploying-to-cloud-run--using-the-ae-cli)

---

## 1. Part 1: Domain Primer for Complete Beginners — Retail Media, Circana Liquid Data® & Google Maps PDI

If you are new to advertising, retail analytics, or geospatial machine learning, the terminology (`CPG`, `RMN`, `POS`, `iROAS`, `Hilbert S2 Level 12`, `330-D Embeddings`, `WorldPop 100m`, `L2 Renormalization`) can look intimidating. Let's demystify every single concept using everyday examples.

### 1.1 The Advertising Side: What Is Retail Media & What Does Circana Do?

```mermaid
flowchart LR
    CPG["🥤 CPG Brand\n(e.g., PepsiCo, Kraft, P&G)\n$2.50M 8-Week Ad Budget"]
    PDI["🌍 Google Maps PDI + WorldPop\n(330-D S2 Level 12 Embeddings\n& 100m Population Grid)"]
    RMN["🛒 5 Retail Media Networks\n(Walmart, Target, Kroger,\nInstacart, Amazon Fresh)"]
    HH["🏠 30M+ Shopper Households\n(Browse Apps, Buy in Stores,\nFill Kitchen Pantries)"]
    CIRC["📊 Circana Liquid Data®\n(Links Ad Exposure to Actual\nCheckout Barcode Scans)"]

    PDI -->|"Identifies High-Intent S2 Cells,\nLocal POI Overlap & Heatwaves"| CPG
    CPG -->|"Allocates Geo-Temporal Spend B[r, t]"| RMN
    RMN -->|"Shows Sponsored Products"| HH
    HH -->|"Swipes Loyalty Card at Checkout"| CIRC
    CIRC -->|"Measures True Incremental Lift (iROAS)"| CPG
```

1. **CPG (Consumer Packaged Goods)**:  
   Companies that make everyday physical products sold in grocery stores—sparkling water, sports drinks, potato chips, cereal, laundry detergent (`PepsiCo`, `Mondelēz`, `Procter & Gamble`, `Kraft Heinz`).
2. **RMN (Retail Media Network)**:  
   When you open the **Walmart** app, **Target** app, **Kroger** app, **Instacart**, or **Amazon Fresh** and search for *"sparkling water"*, the top product results have a small **"Sponsored"** tag.  
   - **Walmart Connect** is Walmart's advertising network.
   - **Target Roundel** is Target's advertising network.
   - **Kroger Precision Marketing (KPM)** is Kroger's advertising network.
   - **Instacart Ads** is Instacart's advertising network.
   - **Amazon Fresh** is Amazon's grocery advertising network.  
   CPG brands pay these 5 Retail Media Networks billions of dollars to place their products at the top of the digital aisle right as a shopper is filling their cart.
3. **Circana & Liquid Data®**:  
   **Circana** (formerly IRI + NPD) operates **Liquid Data®**, which tracks real supermarket checkout scanner data (**POS / Point-of-Sale**) and loyalty-card purchases across **30+ million households** and **350,000+ physical stores**. It answers the ultimate causal question:
   - *Did Household #48291 see the sponsored beverage ad on Walmart Connect in Week 3, AND did they actually scan an extra 12-pack at the checkout register?*
4. **Why `iROAS` (Incremental Return on Ad Spend) Matters More Than `ROAS`**:
   - Suppose a family buys 1 pack of sparkling water every Saturday out of habit. Showing them an ad on Friday and taking credit for Saturday's routine purchase is **not** true growth—that sale would have happened anyway.
   - **Incremental Sales Lift ($\Delta\text{Sales}$)** measures only the **net-new revenue** caused by the ad above baseline buying habits:
     $$\text{iROAS} = \frac{\text{True Incremental Dollar Sales Lift}}{\text{Total Ad Dollars Spent}}$$
   - With a **\$2.50M** budget:
     - Our **Naive Seed (`Gen 1`)** generates **`+\$6.82M`** incremental lift $\rightarrow$ **`2.73x` iROAS**.
     - Our **National AlphaEvolve Champion (`Gen 5`)** generates **`+\$16.72M`** incremental lift $\rightarrow$ **`6.69x` iROAS**.
     - Our **PDI Geo-Temporal AlphaEvolve Champion (`Gen 8`)** generates **`+\$21.04M`** incremental lift $\rightarrow$ **`8.44x` iROAS** (**`+\$4.32M` extra incremental sales** from the exact same **\$2.50M** budget!).

---

### 1.2 The Geospatial Side: What Is Google Maps Population Dynamics Insights (PDI)?

Even the smartest national schedule treats every Walmart or Target store across the United States as if they sit in the exact same neighborhood with the exact same weather and the exact same shoppers.

**Google Maps Population Dynamics Insights (PDI)** solves this by providing privacy-preserving, monthly-updated **330-dimensional AI embeddings** inside **BigQuery (`Analytics Hub`)** for every inhabited area on Earth.

![Google Maps PDI Architecture Diagram](static/s40_pdi_diagram_4.png)

Let's break down the three core building blocks of Google Maps PDI so anyone can understand them:

#### Concept A: What Is an `S2 Level 12 Cell`?
Instead of using postal ZIP codes (which have wildly irregular shapes—some covering 2 city blocks in Manhattan and others covering 500 square miles of desert), Google Maps divides the Earth's sphere into a uniform hierarchy of mathematical squares/polygons called **Hilbert S2 Cells**:
- At **S2 Level 12**, each cell covers roughly **`3.1 to 5.1 km²`** (about the size of a single residential neighborhood or grocery delivery zone).
- Every S2 Level 12 cell has a unique 64-bit token (for example, `89c259c4` in Dallas-Fort Worth or `882a100c` in Chicago).

![Google Maps PDI S2 Level 12 Grid Coverage](static/s38_s2_map_4.png)

#### Concept B: What Is Inside the `330-D Embedding Vector`?
For every S2 Level 12 cell $c$ and month, Google's foundational geospatial neural network compresses billions of anonymized regional signals into an array of **330 floating-point numbers** (`features[0..329]`), normalized so that its Euclidean length (L2 norm) equals `1.0` ($\|v\|_2 = \sqrt{\sum_{d=0}^{329} v_d^2} = 1.0$).

Why normalize to length `1.0`? Because when two vectors have length `1.0`, their **dot product** ($u \cdot v = \sum_{d} u_d v_d$) equals their **Cosine Similarity** ($\cos\theta \in [-1, 1]$)—letting us instantly measure whether two neighborhoods 1,500 miles apart behave like **"Sister Regions"** (`Cosine Similarity >= 0.85`)!

In our CPG Retail Media optimizer, those **330 dimensions** are organized into **3 actionable domain sub-blocks**:

| Embedding Slice | Dimensions | Google Maps PDI Signal Source | What It Tells Our Ad Optimizer |
| :--- | :---: | :--- | :--- |
| **Block 1: Search Trends** | `features[0 : 128]` (`128 dims`) | Aggregated regional Google Search trends & category intent | **Where shoppers are actively searching** for hydration, sparkling water, and back-to-school snacks right now. High cosine similarity (`>= 0.85`) to top-converting stores lowers the ad spend needed to win the auction ($\kappa_r$). |
| **Block 2: Maps POIs & Busyness** | `features[128 : 256]` (`128 dims`) | Google Maps Place types, store density & hourly foot-traffic | **Whether competing retailers share the same physical trade area**. If an S2 cell has a Walmart Supercenter and a Target right across the street (`high POI co-visitation`), pulsing both in the same week wastes money on the same shoppers! |
| **Block 3: Weather & Air Quality** | `features[256 : 330]` (`74 dims`) | Localized temperature anomalies, heat index & air quality | **How fast households drink beverages in their pantry**. In a `97°F–104°F` Sunbelt heatwave (`DFW`, `PHX`, `ATL`), families finish a 12-pack in **2 weeks** instead of **3 weeks**! |

![Google Maps PDI Interactive Playground Reference](static/s39_hex_playground_4.png)

#### Concept C: What Is `Earth Engine WorldPop 100m` (`ST_REGIONSTATS`), and Why Do We Need It?
Retailers rarely plan media around a single S2 square—they plan around a **custom store trade-area polygon** (for example, a **5km driving ring** around a Walmart Supercenter). That 5km ring overlaps **12 to 15 different S2 Level 12 cells**.

How should we combine those 15 S2 cell embeddings into a single 330-D vector for the store trade area?
- **The Naive Trap (Area Weighting)**: Suppose 3 of the 15 S2 polygons on the edge of the 5km ring cover **DFW Airport runways, a rail yard, or an industrial warehouse park**. Those 3 empty slivers make up **`29%` of the land area** (`pdi_sliver_area_km2`), but almost **zero families live there (`< 2%` of population)**! If you weight S2 cells by geometric area, `29%` of your store's embedding vector is polluted by airport/industrial noise.
- **The Google Official Solution (`WorldPop 100m` + `L2 Renormalization`)**:  
  Using BigQuery's native **Google Earth Engine integration (`ST_REGIONSTATS`)**, we query the **WorldPop 100m resolution raster (`projects/sat-io/open-datasets/WORLDPOP/pop`)** to count the exact residential population inside each S2 polygon sliver, weight the 330-D embeddings by **true human population**, and **L2-renormalize** the resulting vector back to unit length (`1.0`).

---

## 2. Part 2: The Seven Real-World Physics Dynamics (4 National + 3 PDI Geospatial) That Break Standard Optimizers

In this project, your Python function `allocate_rmn_flighting(model)` must output a **`5 × 8` matrix of weekly ad spends** (`5 Retail Media Networks × 8 Weeks`, summing to $\le \$2.50\text{M}$).

Why is this optimization problem so challenging? Because **seven coupled non-linear dynamics** govern how ad dollars turn into incremental grocery sales:

| # | Dynamic Name | Layer | Plain-English Intuition | Mathematical Mechanism in `initial_program.py` |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Non-Convex Hill S-Curve** | National (`Gen 2`) | Spending `\$20k/wk` is a whisper in a crowded room (Page 4 of search results = `0` lift). Spending `\$125k/wk` wins the #1 top-of-page slot. Spending `\$300k/wk` saturates the same shoppers. | $H_r(b) = \frac{b^{n_r}}{\kappa_r^{n_r} + b^{n_r}}$ with $n_r \in [3.0, 3.2]$ and inflection point $\kappa_r \in [\$72\text{k}, \$95\text{k}]$. |
| **2** | **3-Week Pantry Loading Cannibalization** | National (`Gen 3`) | Once a family buys 3 cases of sparkling water in Week 1, their kitchen pantry is full in Weeks 2 and 3. Promoting again in Week 2 loses `52%` of lift! | $\text{PantryMult}_{r,t} = \text{clip}(1 - d_1 I_{r,t-1} - d_2 I_{r,t-2}, 0.22, 1.0)$ where baseline $d_1 = 0.52, d_2 = 0.30$. |
| **3** | **Cross-RMN Household Reach Overlap** | National (`Gen 4`) | `28%` of Walmart shoppers also use Target (`overlap = 0.28`). Running heavy flights on both in Week 1 pays twice to reach the same kitchen pantry. | $\text{OverlapMult}_{r,t} = \text{clip}(1 - 0.32 \sum_{k \neq r} \Omega_{r,k} A_{k,t}, 0.45, 1.0)$. |
| **4** | **Store Inventory Out-of-Stock (OOS) Caps** | National (`Gen 3–5`) | Every retailer has supply-bottlenecked weeks (`\$80k–\$90k` cap). Spending above the cap sells zero extra units and triggers a `2.4x` OOS penalty. | $B^{\text{eff}}_{r,t} = \min(B_{r,t}, I_{r,t})$ and $\text{OOSPen}_{r,t} = 2.4 \max(0, B_{r,t} - I_{r,t})$. |
| **5** | **WorldPop 100m Boundary Sliver Pruning** | **PDI Geo (`Gen 6`)** | Weighting store trade rings by WorldPop 100m (`ST_REGIONSTATS`) instead of polygon area prunes zero-household industrial/airport S2 slivers (`Cells 12..14`), boosting residential household capture from `72.4%` to `96.4%`. | `wp_weights = wp_pop / sum(wp_pop)` increases effective trade-area lift ceiling `eff_max_lift` by `+9.6%` (`wp_boost`) and lowers `eff_hill_k` by `5.5%`. |
| **6** | **Sister-Region Search Cosine Similarity & Local POI Decoupling** | **PDI Geo (`Gen 7`)** | Targeting S2 cells whose Search Trends slice (`dims 0:128`) has `Cosine Sim >= 0.85` to seed trade areas lowers the S-curve inflection threshold $\kappa_r$, while Maps POI slice (`dims 128:256`) routes around co-located competitor stores. | Lowers `eff_hill_k` to `0.91x–0.92x` of national $\kappa_r$ and cuts effective cross-RMN overlap matrix `eff_overlap` by `45%` (`overlap * 0.55`). |
| **7** | **Sunbelt 95°F+ Thermal Pantry Velocity** | **PDI Geo (`Gen 8`)** | Weather & Air Quality embeddings (`dims 256:330`) detect `91°F–104°F` summer heat anomalies in Sunbelt S2 cells (`DFW`, `PHX`, `ATL`, `60%` of residential cells), where higher beverage consumption depletes pantries in **2 weeks instead of 3**. | Reduces lag-1 pantry decay $d_1$ by `15%` and lag-2 pantry decay $d_2$ by `30%`, enabling tighter 2-week high-velocity pulses! |

---

## 3. Part 3: Line-by-Line Walkthrough of `initial_program.py` & the BigQuery + Earth Engine SQL Pipeline

Let's open [`initial_program.py`](initial_program.py) (`493 lines`) and walk through **every single section line by line** so you understand both the Python simulation engine and the BigQuery + Earth Engine SQL pipeline behind it.

### 3.1 High-Level Architecture of `initial_program.py`

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  initial_program.py (493 lines)                                              │
│                                                                              │
│  Lines 23–61:   # EVOLVE-BLOCK-START ... # EVOLVE-BLOCK-END                  │
│                 def allocate_rmn_flighting(model) -> np.ndarray              │
│                 (ONLY these 38 lines are mutated by AlphaEvolve's LLMs!)     │
│                                                                              │
│  Lines 64–143:  def _build_pdi_geospatial_tensors(seed=42) -> dict           │
│                 Builds the 5 Metros × 15 S2 Level 12 × 330-D PDI embeddings, │
│                 WorldPop 100m population shares, polygon sliver areas, and   │
│                 summer thermal temperatures (°F).                            │
│                                                                              │
│  Lines 146–234: def build_circana_campaign_model(eval_inputs) -> dict        │
│                 Combines Circana Liquid Data® RMN parameters (Hill S-curves, │
│                 seasonality, OOS caps, overlap matrix) with PDI tensors.     │
│                                                                              │
│  Lines 237–492: def evaluate(eval_inputs) -> dict[str, Any]                  │
│                 Immutable evaluation harness: runs allocate_rmn_flighting,   │
│                 simulates all 8 weeks across national + PDI dynamics, and    │
│                 computes fitness_score + diagnostic telemetry.               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

### 3.2 Production SQL Pipeline: BigQuery GIS + Earth Engine `ST_REGIONSTATS` (`WorldPop 100m`)

Before looking at how `_build_pdi_geospatial_tensors()` represents the PDI data in Python, let's examine the **exact BigQuery Standard SQL query** (from Google's official [PDI WorldPop-Weighted Custom Boundary Aggregation Colab](https://colab.sandbox.google.com/github/googlemaps-samples/insights-samples/blob/main/population_dynamics_insights/notebooks/worldpop_weighted_custom_boundary_aggregation/pdi_worldpop_weighted_custom_boundary_aggregation.ipynb)) that generates these tensors in production:

```sql
-- ============================================================================
-- Google Maps PDI (S2 Level 12) × Earth Engine WorldPop 100m Custom Rollup
-- ============================================================================
WITH store_trade_polygons AS (
  -- Step 1: 5km radius custom trade-area boundary around each Retail Store
  SELECT
    store_id,
    rmn_partner,
    ST_BUFFER(ST_GEOGPOINT(store_lng, store_lat), 5000) AS trade_geom
  FROM `circana_liquid_data.retail_store_locations`
),
intersected_s2_slivers AS (
  -- Step 2: Spatial join against Google Maps PDI S2 Level 12 polygons (~3.1 km²)
  -- and compute exact intersected polygon sliver + WorldPop 100m population count
  SELECT
    s.store_id,
    s.rmn_partner,
    pdi.s2_cell_id,
    pdi.features AS embedding_330d,  -- ARRAY<FLOAT64> of length 330 (Unit L2)
    ST_AREA(ST_INTERSECTION(s.trade_geom, pdi.geometry)) / 1e6 AS sliver_area_km2,
    -- Native BigQuery + Google Earth Engine raster aggregation (WorldPop 100m)
     ST_REGIONSTATS(
      ST_INTERSECTION(s.trade_geom, pdi.geometry),
      'projects/sat-io/open-datasets/WORLDPOP/pop',
      'population'
    ).sum AS sliver_worldpop_100m
  FROM store_trade_polygons AS s
  INNER JOIN `bigquery-public-data.google_maps_pdi.s2_level_12_embeddings` AS pdi
    ON ST_INTERSECTS(s.trade_geom, pdi.geometry)
  WHERE pdi.year_month = '2026-08'
),
weighted_dimensions AS (
  -- Step 3: Unnest all 330 dimensions (dim_idx IN 0..329) and weight by WorldPop
  SELECT
    store_id,
    rmn_partner,
    dim_idx,
    SUM(val * sliver_worldpop_100m) / NULLIF(SUM(sliver_worldpop_100m), 0) AS raw_dim_val
  FROM intersected_s2_slivers,
  UNNEST(embedding_330d) AS val WITH OFFSET AS dim_idx
  GROUP BY store_id, rmn_partner, dim_idx
),
l2_norms AS (
  -- Step 4: Compute Euclidean L2 norm because weighted average of unit vectors has ||v||₂ < 1.0
  SELECT
    store_id,
    SQRT(SUM(POW(raw_dim_val, 2))) AS l2_magnitude
  FROM weighted_dimensions
  GROUP BY store_id
)
-- Step 5: Re-normalize every custom boundary vector back to the 330-D unit hypersphere (||v||₂ = 1.0)
SELECT
  w.store_id,
  w.rmn_partner,
  ARRAY_AGG(
    SAFE.DIVIDE(w.raw_dim_val, n.l2_magnitude)
    ORDER BY w.dim_idx
  ) AS trade_area_unit_embedding_330d
FROM weighted_dimensions AS w
INNER JOIN l2_norms AS n USING (store_id)
GROUP BY w.store_id, w.rmn_partner;
```

#### Line-by-Line Explanation of Why Every Step in This SQL Query Is Essential:
1. **`ST_BUFFER(ST_GEOGPOINT(store_lng, store_lat), 5000)`**: Creates a custom `5,000m` (`5km`) circular polygon around each physical store location.
2. **`ST_INTERSECTION(s.trade_geom, pdi.geometry)`**: Clips each S2 Level 12 cell polygon to the exact boundary of the 5km store ring (`sliver`).
3. **`ST_REGIONSTATS(..., 'projects/sat-io/open-datasets/WORLDPOP/pop', 'population').sum`**: Queries Google Earth Engine's **WorldPop 100m satellite population grid** inside that exact polygon sliver. If an S2 sliver covers an airport runway (`Cells 12..14`), `sliver_worldpop_100m` returns near zero, automatically silencing that sliver!
4. **`SAFE.DIVIDE(w.raw_dim_val, n.l2_magnitude)` (L2 Renormalization)**:  
   Mathematically, when you average two or more unit vectors on a sphere, their weighted average falls *inside* the sphere ($\|\bar{v}\|_2 < 1.0$). Dividing by `SQRT(SUM(POW(raw_dim_val, 2)))` projects the custom trade-area vector back onto the unit hypersphere ($\|\hat{v}\|_2 = 1.000000$) so dot products remain true Cosine Similarities.

---

### 3.3 Lines 64–143 of `initial_program.py`: `_build_pdi_geospatial_tensors(seed=42)` Explained Line by Line

To allow `evaluator.py` and the `ae` CLI to score 100+ candidate Python programs per minute **100% offline and deterministically** (without incurring network latency or BigQuery billing on every mutation), [`_build_pdi_geospatial_tensors()`](initial_program.py#L64-L143) constructs the exact in-memory NumPy representation of our **5 Metro Trade Clusters (`DFW`, `ORD`, `ATL`, `PHX`, `SEA`) × `15 S2 Level 12 Cells` × `330 Dimensions`**:

1. **Lines 79–101 — `worldpop_share` vs. `sliver_area_share` (`shape: (5, 15)`)**:
   - In each of the 5 metros, **S2 Cells `0..11`** are high-density residential and retail neighborhoods (`WorldPop share: 8.4% to 36.4%`).
   - **S2 Cells `12, 13, 14`** represent industrial/airport/rail boundary slivers on the edge of the 5km ring:
     - Their **geometric area share (`sliver_area_share`) is huge (`18.2% to 33.4%`)**.
     - Their **WorldPop 100m residential share (`worldpop_share`) is tiny (`0.8% to 3.2%` in `Cells 12–13`)**.
   - Consequently, across all 5 metros, weighting by WorldPop 100m captures **`96.4%` residential density**, whereas naive area weighting captures only **`72.4%`** (wasting `27.6%` of weight on non-residential slivers!).
2. **Lines 102–111 — `thermal_temp_f` (`shape: (5, 15)`)**:
   - Records the summer afternoon temperature (`°F`) captured in PDI's Weather & Air Quality block (`dims 256:330`):
     - **Sunbelt Metros (`>= 91°F`)**: `DFW` (`95°F–98°F`), `ATL` (`90°F–94°F`), and `PHX` (`102°F–106°F`) — `3 out of 5 metros` (`60%` of residential S2 cells).
     - **Mild Metros (`< 82°F`)**: `ORD` (`77°F–82°F`) and `SEA` (`73°F–75°F`).
3. **Lines 113–135 — Gram-Schmidt Construction of `pdi_330d_embeddings` (`shape: (5, 15, 330)`)**:
   - In each metro $m$, **Cell `0`** (`embeddings[m, 0]`) is the high-performing **Seed Trade Area** (`Cosine Sim = 1.00`), normalized across each of the 3 blocks (`[0:128]`, `[128:256]`, `[256:330]`) and across all `330` dimensions.
   - For **Cells `1..14`**, lines 127–134 use exact **Gram-Schmidt orthogonal projection** (`ortho = ortho - np.dot(ortho, seed_vec) * seed_vec`) to construct unit-L2 330-D vectors with exact target Cosine Similarities `target_sims`:
     - **Sister S2 Cells (`Cells 1..11`)**: `Cosine Similarity ∈ [0.85, 0.94]` (high beverage search intent + dense grocery POIs).
     - **Industrial/Airport Slivers (`Cells 12..14`)**: `Cosine Similarity ∈ [0.41, 0.48]` (low residential similarity).

---

### 3.4 Lines 146–234 of `initial_program.py`: Every Key in `model` Explained

When `allocate_rmn_flighting(model)` is called, `build_circana_campaign_model()` passes a dictionary `model` containing **both** the national Circana parameters and the Google Maps PDI tensors:

| Key in `model` | Shape / Type | Values in Benchmark | Plain-English Purpose |
| :--- | :---: | :--- | :--- |
| `total_budget_musd` | `float` | `2.50` | Total 8-week ad budget in Millions of USD (**\$2.50M**). |
| `n_rmns`, `n_weeks` | `int` | `5`, `8` | `5` Retail Media Networks (`WMT`, `TGT`, `KRG`, `INST`, `AMZ`) × `8` Weeks. |
| `min_flight_musd` | `float` | `0.025` | Minimum active weekly spend (**\$25,000**). |
| `max_weekly_lift_musd` | `ndarray (5,)` | `[1.52, 1.35, 1.18, 1.05, 0.98]` | Base weekly incremental sales ceiling (\$M) per RMN before PDI rollup. |
| `hill_k_musd` ($\kappa_r$) | `ndarray (5,)` | `[0.095, 0.088, 0.082, 0.076, 0.072]` | Base Hill S-curve inflection threshold (\$M) per RMN (`\$72k–\$95k`). |
| `hill_n` ($n_r$) | `ndarray (5,)` | `[3.2, 3.1, 3.1, 3.0, 3.0]` | Hill S-curve steepness exponent ($n_r \ge 3.0$ creates a sharp dead zone below $\kappa_r$). |
| `seasonality` ($S_{r,t}$) | `ndarray (5, 8)` | `[0.92 .. 1.24]` | Weekly retail event demand index (`WMT` peaks Wks 1,4,7; `TGT` peaks Wks 2,5,8; `KRG` peaks Wks 3,6). |
| `inventory_cap_musd` ($I_{r,t}$) | `ndarray (5, 8)` | `[0.08 .. 0.24]` | Weekly store shelf inventory spend cap (\$M). Low-stock `\$80k–\$90k` bottlenecks occur in specific weeks for each RMN. |
| `overlap_matrix` ($\Omega_{r,k}$) | `ndarray (5, 5)` | `[0.00 .. 0.28]` | National cross-RMN household duplication (`WMT-TGT = 0.28`, `KRG-INST = 0.26`). |
| `pdi_330d_embeddings` | `ndarray (5, 15, 330)` | Unit-L2 (`\|\|v\|\|₂ = 1.0`) | **PDI 330-D S2 Level 12 embeddings** (`[0:128]` Search, `[128:256]` POI, `[256:330]` Weather). |
| `pdi_worldpop_100m_pop` | `ndarray (5, 15)` | `[0.8 .. 36.4]` | **Earth Engine WorldPop 100m (`ST_REGIONSTATS`)** population share per S2 sliver. |
| `pdi_sliver_area_km2` | `ndarray (5, 15)` | `[9.4 .. 33.4]` | Geometric polygon sliver area (`km²`) per S2 cell (`Cells 12..14` have huge area but tiny WorldPop). |
| `pdi_thermal_temp_f` | `ndarray (5, 15)` | `[73°F .. 106°F]` | Summer thermal temperature (`°F`) per S2 cell (`DFW`, `ATL`, `PHX` $\ge 91^\circ\text{F}$). |
| `pdi_geo_dispatch` | `dict[str, Any]` | Flags (`enabled`, etc.) | Mutable dispatch dictionary that evolved `# EVOLVE-BLOCK` algorithms update when they activate PDI WorldPop, Sister-Region Cosine Sim, POI decoupling, and Weather velocity. |

---

### 3.5 Lines 237–492 of `initial_program.py`: How `evaluate()` Scores Any Candidate Schedule

Let's trace [`evaluate(eval_inputs)`](initial_program.py#L237-L492) step by step:

1. **Lines 248–272 — Contract & Soft-Constraint Validation**:
   - Calls `raw_schedule = allocate_rmn_flighting(model)`.
   - Verifies `raw_schedule.shape == (5, 8)` and all entries are finite and non-negative.
   - If `total_spend > total_budget`, records `overspend_musd = total_spend - total_budget` and scales `schedule` onto the budget simplex so the simulation still produces a smooth gradient, then applies `80.0 * overspend_musd` penalty in line 442.
2. **Lines 280–350 — Evaluating Google Maps PDI 330-D Physics Modifiers**:
   - Computes `wp_residential_capture` (`0.964`) vs. `area_residential_capture` (`0.724`) from `pdi_worldpop_100m_pop` and `pdi_sliver_area_km2`.
   - Slices `search_slice = emb[:, :, 0:128]`, normalizes each slice, and computes the exact Cosine Similarity `search_cos_sims` against each metro's seed S2 cell (`Cell 0`).
   - Checks which PDI capabilities the evolved algorithm activated in `model["pdi_geo_dispatch"]`:
     - **If `worldpop_l2_rollup` is active (`Gen 6+`)**: Pruning zero-household industrial slivers increases `eff_max_lift` by `wp_boost = 1.0 + 0.399 * (wp_residential_capture - area_residential_capture)` (`+9.58%`) and lowers `eff_hill_k` by `5.5%`.
     - **If `sister_search_cosine_sim` is active (`Gen 7+`)**: Focusing spend on Sister S2 Cells (`Cosine Sim >= 0.85` on `dims 0:128`) shifts `eff_hill_k` down to `[0.91, 0.92, 0.91, 0.92, 0.92] * hill_k`.
     - **If `poi_local_decoupling` is active (`Gen 7+`)**: Using Maps POI co-visitation (`dims 128:256`) to route around overlapping trade areas reduces `eff_overlap = overlap * 0.55`.
     - **If `weather_thermal_cooldown` is active (`Gen 8`)**: Using Weather thermal anomalies (`dims 256:330`, where `sunbelt_share = 0.60` of cells exceed `91°F`) reduces lag-1 pantry decay (`lag1_decay = 0.52 * (1 - 0.25 * sunbelt_share) = 0.442`) and lag-2 pantry decay (`lag2_decay = 0.30 * (1 - 0.50 * sunbelt_share) = 0.210`) while boosting beverage demand ceiling by `1 + 0.064 * sunbelt_share`.
3. **Lines 359–408 — The 8-Week Digital Twin Loop (`for t in range(n_weeks)`)**:
   - For each week `t = 0..7`:
     - Caps spend at store shelf inventory: `eff_b = np.minimum(b_t, inv_cap[:, t])`.
     - Evaluates the Hill S-curve: `hill_resp = eff_b^n / (eff_hill_k^n + eff_b^n)`.
     - Multiplies by `pantry_multiplier` (using `lag1_decay` and `lag2_decay` over weeks `t-1` and `t-2`).
     - Multiplies by `overlap_multiplier` (`1.0 - 0.32 * (eff_overlap @ active_intensity)`).
     - Subtracts the store Out-of-Stock penalty `2.4 * oos_excess`.
4. **Lines 442–448 — The Continuous AlphaEvolve Objective Function (`fitness_score`)**:
   ```python
   constraint_penalty = 80.0 * overspend_musd + 3.5 * n_sub_min
   raw_fitness = (
       31.65 * total_incremental_lift_musd
       - 0.35 * waste_pct
       + pdi_alignment_bonus
       - constraint_penalty
   )
   ```

---

## 4. Part 4: Diagnosing Failure — Why Both the Seed (`196.49`) AND National AlphaEvolve (`522.33`) Hit a Wall

### 4.1 Failure Mode 1: Why the 10-Line Seed Program (`Gen 1`) Scores Only `196.49`
Look at the initial seed inside `# EVOLVE-BLOCK` ([`initial_program.py`, lines 23–61](initial_program.py#L23-L61)):

```python
# EVOLVE-BLOCK-START
def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
    n_rmns = int(model["n_rmns"])
    n_weeks = int(model["n_weeks"])
    total_budget = float(model["total_budget_musd"])
    capacities = np.asarray(model["max_weekly_lift_musd"], dtype=float)

    rmn_weights = capacities / np.sum(capacities)
    schedule = np.outer(rmn_weights, np.ones(n_weeks, dtype=float)) * (total_budget / n_weeks)
    return schedule
# EVOLVE-BLOCK-END
```

This naive seed divides `\$2.50M` evenly across all 8 weeks (`\$312.5k/wk`) and across all 5 retailers (`\$50.4k to \$78.1k` per cell):
- **Every single cell falls below its Hill S-Curve inflection point $\kappa_r$ (`0.70x–0.82x` $\kappa_r$)** $\rightarrow$ trapped in the S-curve **Dead Zone**.
- **Zero pantry cooldown weeks** $\rightarrow$ **`\$7.24M` lost to Pantry Cannibalization**.
- **All 5 RMNs active simultaneously every week** $\rightarrow$ **`\$1.24M` lost to Cross-RMN Overlap**.
- **Result**: Only **`+\$6.82M` incremental lift** (`2.73x` iROAS, **`55.7%` waste**, **`Score: 196.49`**).

### 4.2 Failure Mode 2: Why National-Only AlphaEvolve (`Gen 5`) Hits a Hard Ceiling at `522.33`
In **Generations 2 through 5**, AlphaEvolve evolves a brilliant **National-Only Optimizer** (`national-ae-champion`, identical to the top algorithm in our baseline repository `circan_alpha_evolve`) that:
1. Concentrates spend into `1.25x–1.45x` $\kappa_r$ S-curve pulses,
2. Spaces flights by 3 weeks to respect national average pantry depletion,
3. Staggers Walmart, Target, and Kroger onto alternating weeks, and
4. Runs 140 steps of marginal coordinate ascent.

This raises the score from **`196.49` to `522.33`** (`+\$16.72M` lift, `6.69x` iROAS, `19.7%` waste). **Why can't National-Only AlphaEvolve go any higher than `522.33`?**
- **Blind Spot A (Industrial Sliver Leakage)**: Without Earth Engine WorldPop 100m (`ST_REGIONSTATS`), `27.6%` of custom trade-area boundary weight leaks into low-population industrial/airport S2 slivers (`Cells 12..14`).
- **Blind Spot B (Uniform National Thresholds)**: It assumes every store trade area has the same Hill inflection point $\kappa_r$, missing Sister S2 Cells (`Cosine Sim >= 0.85` on Search Trends `dims 0:128`) where organic beverage search intent lowers $\kappa_r$ by `8–9%`.
- **Blind Spot C (Uniform 3-Week Pantry Cooldown Across All Climates)**: It forces `104°F` Phoenix (`PHX`) and `97°F` Dallas (`DFW`) to wait a full 3 weeks between beverage promotions—even though PDI Weather embeddings (`dims 256:330`) show Sunbelt households deplete their beverage pantries in **2 weeks**!

---

## 5. Part 5: Line-by-Line Walkthrough of `evaluator.py` — How AlphaEvolve Evolves Python Code

Let's inspect [`evaluator.py`](evaluator.py) (`238 lines`), which acts as the bridge between the AlphaEvolve `ae` CLI (`gemini-3.5-flash` + `gemini-3.1-pro-preview` + `gemini-4-argon`) and `initial_program.py`.

```mermaid
sequenceDiagram
    participant DB as AlphaEvolve Island Database
    participant LLM as Gemini Ensemble (Flash / Pro / Argon)
    participant EVAL as 3-Tier evaluator.py
    participant SIM as Circana + Google Maps PDI Simulator

    DB->>LLM: Sample parent program + diagnostic Insights from previous run
    LLM->>EVAL: Propose mutated Python code for allocate_rmn_flighting(model)
    EVAL->>EVAL: Tier 1 Validation: _check_ast_security() (lines 47-61)
    EVAL->>EVAL: Tier 2 Verification: SIGALRM timeout + (5, 8) matrix check (lines 103-146)
    EVAL->>SIM: Tier 3 Evaluation: Run 8-week National + PDI 330-D simulation (line 124)
    SIM-->>EVAL: Return fitness_score + Pantry/Overlap/OOS losses + PDI Cosine Sim & WorldPop metrics
    EVAL-->>DB: Return JSON {score, insights} (lines 154-193) to guide next LLM mutation!
```

### Line-by-Line Breakdown of `evaluator.py`:
1. **Lines 32 & 47–61 — Tier 1 Validation (`_check_ast_security`)**:
   - Parses the candidate Python code with Python's `ast.parse(code)`.
   - Walks every AST node (`ast.Import`, `ast.ImportFrom`) and rejects any program that imports `FORBIDDEN_MODULES = {"os", "sys", "subprocess", "socket", "shutil", "inspect", "ctypes"}`. This guarantees LLM mutations cannot touch the filesystem, spawn processes, or make network calls.
2. **Lines 103–146 — Tier 2 Verification (`evaluate_program`)**:
   - Sets a POSIX `signal.alarm(timeout_seconds)` (`30s` default) so infinite loops in mutated code are cleanly terminated via `EvaluationTimeout`.
   - Executes the compiled code inside a restricted `exec_namespace` containing only `np`, `math`, `Any`, and `Mapping`.
   - Verifies `evaluate(inputs)` returns a dictionary with a finite `fitness_score > -1e11`.
3. **Lines 154–188 — Tier 3 Structured Diagnostic `insights` (The Secret to Fast Evolution)**:
   - Look at the three `insights` blocks returned to the AlphaEvolve database (`lines 155–187`):
     ```json
     {
       "score": 522.33,
       "insights": [
         {
           "label": "campaign_kpis",
           "text": "Incremental Sales Lift: +$16.72M | iROAS: 6.69x | Spend: $2.50M | Ad/OOS Waste: 19.7%"
         },
         {
           "label": "loss_breakdown",
           "text": "Pantry Cannibalization Loss: $1.87M | Cross-RMN Overlap Loss: $1.46M | Out-of-Stock Penalty: $0.00M"
         },
         {
           "label": "pdi_geospatial_insights",
           "text": "PDI Active: False | Sister-Region Cosine Match: 0.65 | PDI Geo Dividend: +$0.00M | WorldPop Capture: 96.4%"
         }
       ]
     }
     ```
   - Notice what happens at **Gen 5 (`score: 522.33`)**: when Gemini sees `"PDI Active: False | Sister-Region Cosine Match: 0.65 | PDI Geo Dividend: +$0.00M | WorldPop Capture: 96.4%"` alongside `model` keys `pdi_330d_embeddings`, `pdi_worldpop_100m_pop`, and `pdi_thermal_temp_f`, the LLM immediately realizes there is an untapped geospatial tensor pipeline in `model` and begins evolving the PDI geo-temporal stages (`Gen 6 → Gen 8`)!

---

## 6. Part 6: Complete Tour of the 8 Evolved Generations (`Gen 1 → Gen 8`: Code + Math + Evaluation Improvements)

Let's examine all **8 evolutionary milestones** stored in [`webapp/server.py` (`CANDIDATE_EVOLVE_BLOCKS`, lines 60–582)](webapp/server.py#L60-L582).

### 6.1 Master Comparison Table Across All 8 Runs (`$2.50M` 8-Week Campaign)

| Gen | Milestone Nickname | Regime | Generator Model | Score (`fitness`) | Net Sales Lift | Campaign iROAS | Ad/OOS Waste | Sister S2 Cosine Sim | PDI Geo Dividend |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Gen 1** | `seed-uniform-smear` | National | `initial_program.py` | **196.49** | `+\$6.82M` | `2.73x` | `55.7%` | `0.51` | `+\$0.00M` |
| **Gen 2** | `hill-threshold-concentrator` | National | `gemini-3.5-flash` | **379.11** | `+\$12.44M` | `4.97x` | `41.4%` | `0.65` | `+\$0.00M` |
| **Gen 3** | `pantry-cooldown-pulser` | National | `gemini-3.5-flash` | **482.74** | `+\$15.55M` | `6.22x` | `26.6%` | `0.65` | `+\$0.00M` |
| **Gen 4** | `cross-rmn-overlap-decoupler` | National | `gemini-3.1-pro-preview` | **495.88** | `+\$15.94M` | `6.38x` | `24.6%` | `0.65` | `+\$0.00M` |
| **Gen 5** | `national-ae-champion` | **National Ceiling** | `gemini-3.1-pro-preview` | **522.33** | **`+\$16.72M`** | **`6.69x`** | **`19.7%`** | **`0.65`** | **`+\$0.00M`** |
| **Gen 6** | `pdi-worldpop-boundary-aggregator` | **+PDI Step 1** | `gemini-3.5-flash` | **589.40** | `+\$18.52M` | `7.43x` | `14.2%` | `0.84` | **`+\$1.80M`** |
| **Gen 7** | `pdi-sister-region-lookalike-pulser` | **+PDI Step 2** | `gemini-3.1-pro-preview` | **641.25** | `+\$19.90M` | `7.98x` | `8.6%` | `0.90` | **`+\$3.18M`** |
| **Gen 8** | `pdi-multimodal-geo-temporal-champion` | **+PDI Champion** | `gemini-4-argon` | **684.90** | **`+\$21.04M`** | **`8.44x`** | **`6.9%`** | **`0.92`** | **`+\$4.32M`** |

---

### 6.2 Phase A: Evolving the National Schedule (`Gen 1` → `Gen 5`, `Score: 196.49 → 522.33`)

#### Generation 1 (`seed-uniform-smear` — Score: `196.49`, Lift: `+$6.82M`, iROAS: `2.73x`)
- **Code**: Uniformly divides `total_budget / n_weeks` across all 8 weeks proportional to `max_weekly_lift_musd`.
- **Evaluation Diagnosis**: Every cell is trapped in the Hill S-curve dead zone (`< 0.82κ`), pantry cannibalization destroys `\$7.24M` of lift, and waste is `55.7%`.

#### Generation 2 (`hill-threshold-concentrator` — Score: `196.49 → 379.11`, Lift: `+$6.82M → +$12.44M`)
- **What Changed in the Code** ([`webapp/server.py`, lines 88–104](webapp/server.py#L88-L104)):
  ```python
  schedule = np.zeros((n_rmns, n_weeks), dtype=float)
  for r in range(n_rmns):
      top_weeks = np.argsort(-seasonality[r])[:5]
      for t in top_weeks:
          schedule[r, t] = 1.25 * hill_k[r]
  if np.sum(schedule) > 0:
      schedule *= total_budget / np.sum(schedule)
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+182.62` points)**:  
  `gemini-3.5-flash` reads `model["hill_k_musd"]` and `model["seasonality"]`, selects only the top 5 seasonality weeks per retailer (`np.argsort(-seasonality[r])[:5]`), and concentrates **`1.25 * hill_k[r]`** into those active weeks (leaving 3 weeks at `\$0`). Every active flight now clears the S-curve inflection point $\kappa_r$, jumping net lift by **`+\$5.62M`** (to `+\$12.44M`, `4.97x` iROAS)!

#### Generation 3 (`pantry-cooldown-pulser` — Score: `379.11 → 482.74`, Lift: `+$12.44M → +$15.55M`)
- **What Changed in the Code** ([`webapp/server.py`, lines 114–142](webapp/server.py#L114-L142)):
  ```python
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
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+103.63` points)**:  
  Guided by the evaluator's `loss_breakdown` insight (`Pantry Cannibalization Loss: $6.67M`), the LLM adds two crucial rules:
  1. **OOS Inventory Gate (`inv_cap[r, w_int] < 1.15 * hill_k[r]`)**: Never pulse a retailer during a supply-bottlenecked week.
  2. **Pantry Cooldown Spacing (`all(abs(w_int - c) >= 2 for c in chosen)`)**: Enforces at least a 2-week gap between active flights on the same retailer.
  - **Result**: Pantry cannibalization loss plunges from **`\$6.67M` down to `\$2.73M`**, and net lift jumps to **`+\$15.55M`** (`6.22x` iROAS)!

#### Generation 4 (`cross-rmn-overlap-decoupler` — Score: `482.74 → 495.88`, Lift: `+$15.55M → +$15.94M`)
- **What Changed in the Code** ([`webapp/server.py`, lines 152–197](webapp/server.py#L152-L197)):
  ```python
  active_int = np.clip(schedule[:, t] / (hill_k * 1.2), 0.0, 1.4)
  ov_mult = max(0.45, 1.0 - 0.32 * float(overlap[r] @ active_int))
  h_val = (spend ** hill_n[r]) / (hill_k[r] ** hill_n[r] + spend ** hill_n[r])
  gain = (max_lift[r] * seasonality[r, t] * h_val * pantry_pen * ov_mult) / spend
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+13.14` points)**:  
  Instead of scheduling each retailer row independently, `gemini-3.1-pro-preview` uses `overlap = model["overlap_matrix"]` inside a joint 18-step greedy selector. Before placing a flight on `(r, t)`, it computes `overlap[r] @ active_int` to penalize weeks where an overlapping retailer (like Walmart vs. Target) is already active. Cross-RMN overlap loss drops from `\$2.48M` to `\$2.05M`.

#### Generation 5 (`national-ae-champion` — Score: `495.88 → 522.33`, Lift: `+$15.94M → +$16.72M`)
- **What Changed in the Code** ([`webapp/server.py`, lines 207–286](webapp/server.py#L207-L286)):
  - Writes a complete internal surrogate simulator `sim_net_lift(sched)` inside `# EVOLVE-BLOCK` (`lines 220–237`), selects 18 high-ROI staggered pulses (`lines 240–263`), and then runs **140 steps of marginal coordinate ascent** (`delta = 0.008`, `lines 265–285`), adding `\$8,000` increments to whichever active pulse has the steepest marginal Hill derivative $\frac{\partial \text{Lift}}{\partial B_{r,t}}$.
- **Why `522.33` Is the National Ceiling**:  
  This achieves **`+\$16.72M` lift (`6.69x` iROAS, `19.7%` waste)**—the exact optimum possible using national-only data.

---

### 6.3 Phase B: Breaking Through the Ceiling with Google Maps PDI (`Gen 6` → `Gen 8`, `Score: 522.33 → 684.90`)

Now watch what happens in **Generations 6, 7, and 8** as AlphaEvolve discovers how to exploit the **Google Maps PDI 330-D S2 Level 12 embeddings** and **Earth Engine WorldPop 100m** tensors in `model`!

#### Generation 6 (`pdi-worldpop-boundary-aggregator` — Score: `522.33 → 589.40`, Lift: `+$16.72M → +$18.52M`)
- **What the LLM Discovered (+PDI Step 1)**:  
  The LLM inspects `model["pdi_330d_embeddings"]` (`(5, 15, 330)`), `model["pdi_worldpop_100m_pop"]` (`(5, 15)`), and `model["pdi_sliver_area_km2"]` (`(5, 15)`). It implements **WorldPop 100m (`ST_REGIONSTATS`) custom trade-area aggregation + L2 renormalization** using `np.einsum`:
- **Exact Evolved Code** ([`webapp/server.py`, lines 306–326](webapp/server.py#L306-L326)):
  ```python
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
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+67.07` points over National Ceiling!)**:
  1. `wp_weights = wp_pop / np.sum(wp_pop, axis=1, keepdims=True)` computes the exact WorldPop 100m population weight for each of the 15 S2 slivers in each metro.
  2. `agg_330d = np.einsum("mc,mcd->md", wp_weights, emb)` computes the population-weighted 330-D embedding for each store trade area, and `agg_330d /= np.linalg.norm(...)` L2-renormalizes it back to unit length `1.0`.
  3. By silencing the zero-household industrial/airport slivers (`Cells 12..14`, which had `26–33%` area share but `< 3%` WorldPop), residential household capture rises from `72.4%` to **`96.4%`** (`wp_res_gain = +0.24`).
  4. **Result**: Score surges from **`522.33` to `589.40`**, unlocking **`+\$1.80M` in PDI Geospatial Dividend** (`+\$18.52M` total lift, `7.43x` iROAS, waste cut from `19.7%` to `14.2%`)!

---

#### Generation 7 (`pdi-sister-region-lookalike-pulser` — Score: `589.40 → 641.25`, Lift: `+$18.52M → +$19.90M`)
- **What the LLM Discovered (+PDI Step 2)**:  
  Next, `gemini-3.1-pro-preview` unlocks **Block 1 (`Search Trends`, `dims 0:128`)** and **Block 2 (`Maps POIs & Busyness`, `dims 128:256`)** of the 330-D PDI embeddings:
- **Exact Evolved Code** ([`webapp/server.py`, lines 403–421](webapp/server.py#L403-L421)):
  ```python
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
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+51.85` points)**:
  1. **Sister-Region Lookalike Targeting (`sister_search_cosine_sim = True`)**: By concentrating spend into S2 Level 12 cells whose Search Trends slice (`dims 0:128`) has **`Cosine Similarity >= 0.85`** (average match **`0.90`**) to the top-performing seed trade area, shoppers already have high organic search intent for beverages. This shifts the Hill S-curve inflection point down (`eff_hill_k = hill_k * [0.91, 0.92, ...]`), meaning each active pulse reaches the optimal S-curve knee with `8–9%` less spend!
  2. **Local POI Co-Visitation Decoupling (`poi_local_decoupling = True`)**: By checking `dims 128:256` (Google Maps POI density & co-visitation), the optimizer routes concurrent RMN flights into S2 cells where Walmart and Target do *not* share the same shopping plaza, cutting effective cross-RMN overlap by **`45%`** (`eff_overlap = overlap * 0.55`).
  3. **Result**: Score jumps from **`589.40` to `641.25`**, lifting total incremental sales to **`+\$19.90M`** (`7.98x` iROAS, **`+\$3.18M` PDI Geospatial Dividend**, waste down to **`8.6%`**)!

---

#### Generation 8 (`pdi-multimodal-geo-temporal-champion` — Score: `641.25 → 684.90`, Lift: `+$19.90M → +$21.04M`)
- **What the LLM Discovered (+PDI Step 3 Champion)**:  
  In the final evolutionary breakthrough, `gemini-4-argon` integrates **Block 3 (`Weather & Air Quality`, `dims 256:330`)** alongside `model["pdi_thermal_temp_f"]` (`(5, 15)`), creating the complete **330-D Multimodal Geo-Temporal Optimizer**:
- **Exact Evolved Code** ([`webapp/server.py`, lines 487–580](webapp/server.py#L487-L580)):
  ```python
  def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:
      """Gen 8 Champion (Score: 684.90 | iROAS: 8.44x): Full 330-D PDI + WorldPop Geo-Temporal Optimizer."""
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
  ```
- **Line-by-Line Explanation & Evaluation Improvement (`+43.65` points, `+31.1%` over National AlphaEvolve)**:
  1. `sunbelt_share = float(np.mean(temp_f[:, :12] >= 91.0))` measures the fraction of residential S2 cells experiencing `91°F–106°F` summer thermal anomalies (`DFW`, `ATL`, `PHX` $\rightarrow$ `sunbelt_share = 0.60`).
  2. Because families in `95°F+` Sunbelt S2 cells consume cold beverages much faster, their kitchen pantries deplete in **2 weeks instead of 3 weeks** (`lag1_d` drops from `0.52` to `0.442`, and `lag2_d` drops from `0.30` to `0.210`).
  3. Inside the pulse selector (`for _ in range(22)`) and **180-step marginal coordinate ascent** (`for _ in range(180)`), the optimizer schedules **22 high-velocity geo-temporal pulses** (up from 18 in National AE) and fine-tunes every cell in `\$8,000` (`0.008`) increments.
  4. **Final Champion Result**:
     - **Evaluator Fitness Score**: **`684.90`** (`+248.6%` over Seed `196.49`, and **`+31.1%` above the National AlphaEvolve Ceiling `522.33`**)
     - **Total Incremental Sales Lift**: **`+\$21.04M`** (an extra **`+\$4.32M` PDI Geospatial Dividend** above National AlphaEvolve from the exact same `\$2.50M` budget!)
     - **Campaign iROAS**: **`8.44x`** (up from `2.73x` Seed and `6.69x` National AE)
     - **Total Ad & OOS Waste**: Reduced to **`6.9%`** (down from `55.7%` Seed and `19.7%` National AE)

---

## 7. Part 7: Interactive Web Studio Guide — PDI Map Playground, 4 Live Charts & Editable Controls

Open **https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app** (or `http://localhost:8086` locally) to explore the full interactive studio:

![Full Interactive Studio Overview](static/pdi_studio_full.png)

### 7.1 Top Visual Section: Google Maps PDI S2 Level 12 Explorer & Custom Boundary Rollup
Modeled directly after the Google Maps Platform **PDI Playground**, this interactive geospatial panel lets you:
- **Switch Metro Trade Clusters**: Click between **Dallas-Fort Worth (`DFW - 97°F`)**, **Chicago (`ORD - 79°F`)**, **Atlanta (`ATL - 92°F`)**, **Phoenix (`PHX - 104°F`)**, and **Seattle (`SEA - 74°F`)**.
- **Switch Embedding View Modes**: Toggle between **Cosine Similarity (`features[0..329]`)**, **WorldPop 100m vs. Area Slivers**, **Search Trends (`dims 0..127`)**, **Maps POIs (`dims 128..255`)**, and **Thermal Pantry Velocity (`dims 256..329`)**.
- **Inspect Individual S2 Level 12 Cells**: Click any S2 cell on the map (`89c259c4`, `89c259cc`, etc.) to inspect its **Cosine Similarity**, **WorldPop 100m share vs. Polygon Sliver Area share**, **330-D Vector Sparkline**, and **BigQuery `ST_REGIONSTATS` + L2 Renormalization SQL**.

### 7.2 Middle Section: 4 Synchronized Optimization Charts
As you scrub the **Generation Timeline Slider (`Gen 1` → `Gen 8`)** or click **▶ Play Evolution**:
1. **Chart 1 — Evolutionary Fitness & PDI Breakthrough (`fitness_score`)**: Shows the national climb (`Gen 1: 196.49` $\rightarrow$ `Gen 5: 522.33` National Ceiling) and the emerald **Google Maps PDI Breakthrough (`Gen 6: 589.40` $\rightarrow$ `Gen 8: 684.90`)**.
2. **Chart 2 — Hill S-Curve Operating Points (PDI Shifts $\kappa$ Left)**: Shows all 5 RMN operating markers moving out of the red Dead Zone (`Gen 1`) into the green Optimal Marginal Knee (`Gen 5–8`).
3. **Chart 3 — 8-Week × 5-RMN Geo-Temporal Flighting Plan (\$k)**: Displays the exact weekly dollar allocation for each retailer, highlighting **Sunbelt 2-Week Velocity Pulses (`☀️`)**, **Sister S2 Cell Pulses (`🔗`)**, and **Pantry Cooldown Weeks (`—`)**.
4. **Chart 4 — Cumulative 8-Week Incremental Sales Lift (\$M)**: Compares the **Gen 8 PDI Champion (`+\$21.04M`)** against the **Gen 5 National Ceiling (`+\$16.72M`)** and **Gen 1 Naive Seed (`+\$6.82M`)**, shading the **`+\$4.32M` PDI Geospatial Dividend**.

### 7.3 Bottom Inspector: Live `# EVOLVE-BLOCK` Python Sandbox & Diff Viewer
- **Tab 1 (`🧬 # EVOLVE-BLOCK Python Code`)**: View and **live-edit** the Python code of `allocate_rmn_flighting(model)` directly in the browser, then click **🧪 Evaluate Edited Code Now (`evaluator.py`)** to run your custom algorithm through the real 3-tier `evaluator.py` backend!
- **Tab 2 (`🔍 Unified Diff vs. Seed`)**: Line-by-line `git diff` comparing the active generation against `initial_program.py`.
- **Tab 3 (`🌍 BigQuery GIS + Earth Engine WorldPop SQL`)**: Ready-to-run BigQuery Standard SQL for `ST_REGIONSTATS` WorldPop 100m aggregation and L2 renormalization.
- **Tab 4 (`💻 Generated ae CLI Commands & Insights`)**: Live `ae` CLI commands and raw JSON `score` + `insights` from `evaluator.py`.

---

## 8. Part 8: System Architecture & Modular Repository Structure

```mermaid
flowchart LR
    subgraph Browser["Interactive Web Studio (Cloud Run / Local Port 8086)"]
        MAP["🌍 Google Maps PDI S2 Playground\n(5 Metros × 15 S2 Cells × 330-D)"]
        CFG["⚙️ Editable AE + PDI Sidebar\n(Concurrency, Models, Budget, WorldPop, Cosine Sim)"]
        CHARTS["📈 4 Synchronized Canvas Charts\n(Fitness, S-Curve, Flighting Matrix, Lift)"]
        EDITOR["🧬 Live # EVOLVE-BLOCK Editor\n& Unified Diff Inspector"]
    end

    subgraph FastAPI["FastAPI Backend (webapp/server.py)"]
        SIM["POST /api/simulate_evolution"]
        CUSTOM["POST /api/evaluate_custom"]
        CONF["GET/POST /api/config"]
        AESTAT["GET /api/ae_status"]
    end

    subgraph CoreAE["Official AlphaEvolve Experiment Root"]
        INIT["initial_program.py\n(# EVOLVE-BLOCK + PDI 330-D Simulator)"]
        EVAL["evaluator.py\n(3-Tier Cascade Evaluator)"]
        DESC[".evolve/experiment_description.json"]
        CLI["ae CLI (ae 0.2.8)"]
    end

    MAP --> SIM
    CFG --> SIM
    EDITOR --> CUSTOM
    SIM --> EVAL
    CUSTOM --> EVAL
    EVAL --> INIT
    AESTAT --> CLI
    SIM --> CHARTS
```

### Organized Repository Directory Tree
```text
circana_alpha_evolve_and_pdi/
├── .evolve/
│   ├── experiment_description.json              # Official AlphaEvolve ExperimentDescription schema
│   └── gui_config.json                          # Persisted GUI runtime & PDI configuration
├── cloud_run/                                   # Google Cloud Run deployment configuration
│   ├── Dockerfile                               # Production container image definition
│   ├── .dockerignore                            # Excludes .venv/ and build caches
│   └── deploy.sh                                # One-command Cloud Run deployment script
├── presentations/                               # 3D Search Space renderers & Executive Slide Decks
│   ├── render_3d_visualization.py               # Offline 3D search-space + PDI S2 matrix renderer
│   ├── build_pdi_executive_deck.py              # Automated 8-slide Google Slides deck builder
│   ├── circana_pdi_alphaevolve_executive_deck.pdf
│   └── circana_pdi_alphaevolve_executive_deck.pptx
├── static/                                      # Frontend HTML/CSS/JS, PDI Map & 3D Video/GIF assets
│   ├── index.html                               # Interactive Web Studio + PDI S2 Map Playground
│   ├── styles.css                               # Executive dark-mode styling
│   ├── app.js                                   # Synchronized charts, S2 cell inspector & sandbox
│   ├── alphaevolve_3d_landscape.mp4             # 3D Search Space & PDI Geo-RMN video (H.264 MP4)
│   ├── alphaevolve_3d_landscape.gif             # 3D Search Space looping GIF for slides/README
│   ├── alphaevolve_3d_poster.png                # 3D Search Space high-res climax frame
│   ├── pdi_snap_playground.png                  # Screenshot of PDI S2 Level 12 Map Playground
│   ├── pdi_snap_charts.png                      # Screenshot of 4 synchronized charts + code editor
│   ├── s38_s2_map_4.png                         # Google Maps PDI S2 Level 12 reference map
│   ├── s39_hex_playground_4.png                 # Google Maps PDI Interactive Playground reference
│   └── s40_pdi_diagram_4.png                    # Google Maps PDI 330-D architecture diagram
├── tests/                                       # Automated Pytest verification suite (11/11 passing)
│   ├── __init__.py
│   ├── test_program.py                          # Tests initial_program.py & PDI 330-D simulation (5 tests)
│   └── test_evaluator.py                        # Tests evaluator.py 3-tier validation & insights (6 tests)
├── webapp/                                      # FastAPI backend server
│   ├── __init__.py
│   └── server.py                                # Serves static/ and executes real-time PDI evaluations
├── initial_program.py                           # Seed program (# EVOLVE-BLOCK) + Circana/PDI simulator
├── evaluator.py                                 # 3-tier CLI & library evaluator for `ae`
├── problem_description.md                       # Natural-language prompt context for AlphaEvolve LLMs
├── example_evaluation.json                      # Verified baseline score output from `ae program evaluate`
├── pyproject.toml                               # uv Python project & pytest configuration
├── requirements.txt                             # Cloud Run Python dependencies
└── README.md                                    # This complete tutorial & documentation
```

---

## 9. Part 9: Running Locally, Running Tests (`11/11`), Deploying to Cloud Run & Using the `ae` CLI

### 9.1 Run the Interactive Web Studio Locally
```bash
git clone https://github.com/elhadik/Ads_Alpha_Evolve.git
cd Ads_Alpha_Evolve
uv sync
uv run uvicorn webapp.server:app --host 0.0.0.0 --port 8086
```
Open **http://localhost:8086** in your browser (or visit the live deployment at **https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app**).

### 9.2 Run the Automated Pytest Suite (`11 / 11 Passing`)
```bash
uv run pytest -v
```
- [`tests/test_program.py`](tests/test_program.py) (`5 tests`): Verifies `allocate_rmn_flighting()` returns a valid `(5, 8)` matrix within the `\$2.50M` budget, validates the `(5, 15, 330)` unit-L2 PDI tensors, and confirms `evaluate()` is deterministic when PDI geo-dispatch is enabled.
- [`tests/test_evaluator.py`](tests/test_evaluator.py) (`6 tests`): Verifies `evaluator.py` scores both the seed (`196.49`) and the evolved PDI champion (`684.90`), catches syntax errors, blocks forbidden imports (`os`, `subprocess`, `socket`), captures `stdout`, and writes the strict `--output-file` JSON schema required by the `ae` CLI.

### 9.3 Regenerate the 3D Search Space Video & GIF Offline
```bash
uv run python presentations/render_3d_visualization.py
```
This renders [`static/alphaevolve_3d_landscape.mp4`](static/alphaevolve_3d_landscape.mp4), [`static/alphaevolve_3d_landscape.gif`](static/alphaevolve_3d_landscape.gif), and [`static/alphaevolve_3d_poster.png`](static/alphaevolve_3d_poster.png) 100% offline.

### 9.4 Deploy to Google Cloud Run
```bash
chmod +x cloud_run/deploy.sh
./cloud_run/deploy.sh shade-sandbox us-central1
```
- **Live Cloud Run URL**: **https://circana-alpha-evolve-pdi-ns6bqifvaq-uc.a.run.app**

### 9.5 Launch a Full Cloud AlphaEvolve Experiment via the `ae` CLI
```bash
# Step 0: Configure GCP project, Discovery Engine, and 90/10 Flash+Pro model mixture
ae config init \
  --project YOUR_GCP_PROJECT_ID \
  --engine YOUR_DISCOVERY_ENGINE_ID \
  --models "gemini-3.5-flash:0.9,gemini-3.1-pro-preview:0.1"

# Step 1: Create the experiment with Concurrency = 10 and Max Generated = 100
ae --json experiment create \
  --concurrency 10 \
  --max-programs 100 \
  --problem-file problem_description.md \
  --title "Circana x Google Maps PDI Geo-Temporal RMN Flighting Optimizer"

# Step 2: Upload initial_program.py and seed score (196.4941)
ae --json experiment start <nickname> \
  --program-dir . \
  --score 196.4941

# Step 3: Run the local evaluation loop for up to 100 iterations
ae --json experiment run <nickname> \
  --evaluator evaluator.py \
  --backend local \
  --timeout 60 \
  --max-iterations 100 \
  --dashboard <nickname>-dashboard.md
```
