#!/usr/bin/env python3
"""Build the 8-Slide Executive Presentation for Circana × Google Maps PDI × AlphaEvolve."""

from __future__ import annotations

import json
import pathlib
import subprocess
from typing import Any, Dict, List

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
STATIC_DIR = ROOT_DIR / "static"
PRES_DIR = ROOT_DIR / "presentations"


def run_gslides(args: List[str]) -> str:
    cmd = ["gslides"] + args
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"gslides failed ({res.returncode}): {res.stdout}\n{res.stderr}")
    return (res.stdout + "\n" + res.stderr).strip()


def main() -> None:
    pres_id = "13JBw4QDMnaGELTrfZwb-5AHPwzELPtJZQInkH8LQcMs"
    print(f"[1/5] Using Presentation ID: {pres_id}")

    table_rows = [
        ["Stage / Nickname", "Gemini Model", "Key Algorithmic & PDI Innovation", "Lift / iROAS", "Fitness Score"],
        ["Gen 1: seed-uniform-smear", "Baseline Seed", "Uniform $62.5k smear; dead-zone & sliver waste", "+$6.82M (2.73x)", "196.49"],
        ["Gen 2: hill-threshold", "gemini-3.5-flash", "Pulses at 1.25x Hill κ; escapes S-curve dead zone", "+$12.44M (4.97x)", "379.11"],
        ["Gen 3: pantry-cooldown", "gemini-3.5-flash", "3-week household pantry spacing + OOS cap gates", "+$15.55M (6.22x)", "482.74"],
        ["Gen 4: cross-rmn-dedup", "gemini-3.1-pro", "Staggers Walmart/Target & Kroger/Instacart overlap", "+$15.94M (6.38x)", "495.88"],
        ["Gen 5: national-ae-top", "gemini-3.1-pro", "National Coordinate Ascent Ceiling (No PDI Geo)", "+$16.72M (6.69x)", "522.33"],
        ["Gen 6: +pdi-worldpop", "gemini-3.5-flash", "ST_REGIONSTATS WorldPop 100m + L2 boundary rollup", "+$18.52M (7.43x)", "589.40 (+12.8%)"],
        ["Gen 7: +pdi-sister-s2", "gemini-3.1-pro", "Search [0:127] Cosine Sim ≥ 0.85 + POI [128:255]", "+$19.90M (7.98x)", "641.25 (+22.8%)"],
        ["Gen 8: +pdi-330d-champ", "gemini-4-argon", "Full 330-D + Weather [256:329] 2-wk Sunbelt cycle", "+$21.05M (8.42x)", "684.90 (+31.1%)"],
    ]

    ops: List[Dict[str, Any]] = [
        # Remove default placeholders on Slide 1 ('p')
        {"op": "delete-element", "element": "i0"},
        {"op": "delete-element", "element": "i1"},
        {"op": "set-background", "slide": "p", "color": "#0B1120"},
        # Add Slides 2..8
        {"op": "add-slide", "id": "SLIDE_PROBLEM", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_PROBLEM", "color": "#F8FAFC"},
        {"op": "add-slide", "id": "SLIDE_SOLUTION", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_SOLUTION", "color": "#0F172A"},
        {"op": "add-slide", "id": "SLIDE_3D_VIS", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_3D_VIS", "color": "#04060C"},
        {"op": "add-slide", "id": "SLIDE_PDI_MAP", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_PDI_MAP", "color": "#F8FAFC"},
        {"op": "add-slide", "id": "SLIDE_CHARTS", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_CHARTS", "color": "#0F172A"},
        {"op": "add-slide", "id": "SLIDE_TABLE", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_TABLE", "color": "#F8FAFC"},
        {"op": "add-slide", "id": "SLIDE_CLOSING", "layout": "BLANK"},
        {"op": "set-background", "slide": "SLIDE_CLOSING", "color": "#0B1120"},
        # ================= SLIDE 1: HERO TITLE & 3 KPI STAT CARDS =================
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 36,
            "y": 24,
            "width": 380,
            "height": 26,
            "background_color": "#064E3B",
            "text": "GOOGLE CLOUD ALPHAEVOLVE × CIRCANA® × GOOGLE MAPS PDI",
            "font_size": 9,
            "bold": True,
            "color": "#6EE7B7",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 36,
            "y": 58,
            "width": 648,
            "height": 84,
            "text": "Geo-Temporal Retail Media Flighting\nwith 330-D Google Maps PDI Embeddings",
            "font_size": 28,
            "bold": True,
            "color": "#FFFFFF",
        },
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 36,
            "y": 148,
            "width": 648,
            "height": 48,
            "text": "Breaking through the National RMN Optimization Ceiling (+31.1%) by fusing Circana Liquid Data® POS response curves with BigQuery S2 Level 12 PDI embeddings & Earth Engine WorldPop 100m rasters.",
            "font_size": 12,
            "color": "#94A3B8",
        },
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 36,
            "y": 216,
            "width": 204,
            "height": 148,
            "background_color": "#1E293B",
            "text": "684.90\nEvaluator Fitness Score\n\n+248.6% vs Naive Seed (196.5)\n+31.1% over National AE (522.3)",
            "font_size": 12,
            "bold": True,
            "color": "#6EE7B7",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 258,
            "y": 216,
            "width": 204,
            "height": 148,
            "background_color": "#1E293B",
            "text": "+$21.05M\nIncremental Retail Lift\n\n+$4.33M PDI Geo Dividend\non $2.50M Total Ad Budget",
            "font_size": 12,
            "bold": True,
            "color": "#7DD3FC",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": "p",
            "x": 480,
            "y": 216,
            "width": 204,
            "height": 148,
            "background_color": "#1E293B",
            "text": "8.42x iROAS\nCampaign Return on Spend\n\nAd/Sliver Waste Cut to 7.2%\n(0.92 Cosine Sister Match)",
            "font_size": 12,
            "bold": True,
            "color": "#FCD34D",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        # ================= SLIDE 2: PROBLEM STATEMENT (2x2 GRID) =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 36,
            "y": 14,
            "width": 648,
            "height": 34,
            "text": "The Problem: Why National-Only RMN Flighting Plateaus at 522.3",
            "font_size": 18,
            "bold": True,
            "color": "#0F172A",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 36,
            "y": 50,
            "width": 648,
            "height": 26,
            "text": "Allocating $2.50M across 5 RMNs & 8 Weeks using national averages ignores 4 critical local geospatial dynamics:",
            "font_size": 11,
            "color": "#475569",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 36,
            "y": 86,
            "width": 314,
            "height": 142,
            "background_color": "#FFFFFF",
            "text": "1. Boundary Sliver Waste (Area vs. WorldPop)\n• Custom 5km store trade rings clip huge S2 cells covering airports, rail yards & industrial parks.\n• Naive area-weighted rollups waste 18%+ of ad spend on zero-household slivers instead of dense residential cores.",
            "font_size": 11,
            "color": "#1E293B",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 370,
            "y": 86,
            "width": 314,
            "height": 142,
            "background_color": "#FFFFFF",
            "text": "2. Local Hill S-Curve Inflection Variance\n• National Hill inflection (κ = $72k–$95k) assumes uniform category intent across all zip codes.\n• High-similarity Sister S2 cells (PDI Search dims 0:127) reach their S-curve knee at 22% lower ad spend.",
            "font_size": 11,
            "color": "#1E293B",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 36,
            "y": 242,
            "width": 314,
            "height": 142,
            "background_color": "#FFFFFF",
            "text": "3. Heterogeneous Cross-RMN POI Overlap\n• National averages assume 28% Walmart–Target household duplication everywhere.\n• PDI Maps POIs & Busyness (dims 128:255) reveal local trade hubs with only 14% overlap where simultaneous pulses win.",
            "font_size": 11,
            "color": "#1E293B",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PROBLEM",
            "x": 370,
            "y": 242,
            "width": 314,
            "height": 142,
            "background_color": "#FFFFFF",
            "text": "4. Sunbelt Thermal Pantry-Depletion Velocity\n• Fixed 3-week pantry cooldown leaves money on the table during 95°F+ Sunbelt heatwaves (DFW, PHX, ATL).\n• PDI Weather & AQI (dims 256:329) captures 2-week beverage replenishment cycles for an extra pulse wave.",
            "font_size": 11,
            "color": "#1E293B",
        },
        # ================= SLIDE 3: SOLUTION ARCHITECTURE =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 36,
            "y": 14,
            "width": 648,
            "height": 34,
            "text": "The Solution: PDI 330-D + WorldPop 100m + AlphaEvolve",
            "font_size": 22,
            "bold": True,
            "color": "#FFFFFF",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 36,
            "y": 50,
            "width": 648,
            "height": 24,
            "text": "Three-stage geospatial & evolutionary pipeline linking BigQuery GIS, Earth Engine, and Gemini code evolution:",
            "font_size": 11,
            "color": "#94A3B8",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 36,
            "y": 84,
            "width": 204,
            "height": 220,
            "background_color": "#1E293B",
            "text": "① BigQuery GIS + WorldPop\n\n• S2_COVERINGCELLIDS at Level 12 (~3.1 km²) over 5km store polygons\n• Earth Engine WorldPop 100m via ST_REGIONSTATS\n• Population-weighted average + unit L2 sphere normalization\n• Captures 96.9% residential HHs vs 74.1% naive area",
            "font_size": 10.5,
            "color": "#E2E8F0",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 258,
            "y": 84,
            "width": 204,
            "height": 220,
            "background_color": "#1E293B",
            "text": "② 330-D PDI GNN Embeddings\n\n• dims [0:127] Search Trends: ML.DISTANCE Cosine Sim ≥ 0.85 Sister S2 cells\n• dims [128:255] Maps POIs: Local RMN co-visitation overlap matrix\n• dims [256:329] Weather/AQI: 2-wk vs 3-wk thermal pantry velocity",
            "font_size": 10.5,
            "color": "#E2E8F0",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 480,
            "y": 84,
            "width": 204,
            "height": 220,
            "background_color": "#1E293B",
            "text": "③ AlphaEvolve Code Search\n\n• Evolves allocate_rmn_flighting inside # EVOLVE-BLOCK\n• 90/10 Gemini 3.5 Flash & 3.1 Pro + Gemini 4 Argon\n• Evaluates 100 candidates across 8 milestones\n• Breakthrough: 522.33 -> 684.90 (+31.1% Geo Lift)",
            "font_size": 10.5,
            "color": "#E2E8F0",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_SOLUTION",
            "x": 36,
            "y": 316,
            "width": 648,
            "height": 68,
            "background_color": "#064E3B",
            "text": "KEY DISCOVERY: Combining WorldPop 100m S2 boundary pruning (+12.8%), Sister-Region Search Cosine Similarity (+9.9%), and Sunbelt 2-Week Thermal Pantry Cycling (+8.4%) unlocks +$4.33M in net-new CPG sales on the exact same $2.50M budget.",
            "font_size": 11,
            "bold": True,
            "color": "#ECFDF5",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        # ================= SLIDE 5: GOOGLE MAPS PDI PLAYGROUND & 330-D GNN =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_PDI_MAP",
            "x": 36,
            "y": 12,
            "width": 648,
            "height": 30,
            "text": "Interactive Studio: Google Maps PDI Playground & 330-D GNN",
            "font_size": 21,
            "bold": True,
            "color": "#0F172A",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_PDI_MAP",
            "x": 36,
            "y": 42,
            "width": 648,
            "height": 22,
            "text": "Left: Full web studio with H3/S2 Playground Card & Per-Cell Breakdown Chart | Right: Multimodal PDFM 330-D GNN",
            "font_size": 10.5,
            "color": "#475569",
        },
        # ================= SLIDE 6: 6 DYNAMIC CHARTS & BIGQUERY WORLDPOP SQL =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_CHARTS",
            "x": 36,
            "y": 12,
            "width": 648,
            "height": 30,
            "text": "Dynamic Optimization Charts & BigQuery WorldPop 100m SQL",
            "font_size": 21,
            "bold": True,
            "color": "#FFFFFF",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_CHARTS",
            "x": 36,
            "y": 42,
            "width": 648,
            "height": 22,
            "text": "6 synchronized real-time charts tracking the +31.1% PDI leap over National AE + live Python & BigQuery GIS sandbox",
            "font_size": 10.5,
            "color": "#94A3B8",
        },
        # ================= SLIDE 7: 8-MILESTONE PROGRESSION TABLE =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_TABLE",
            "x": 36,
            "y": 12,
            "width": 648,
            "height": 30,
            "text": "Evolutionary Trajectory: 5 National Stages + 3 PDI Breakthroughs",
            "font_size": 20,
            "bold": True,
            "color": "#0F172A",
        },
        {
            "op": "add-table",
            "id": "S7_TBL",
            "slide": "SLIDE_TABLE",
            "x": 28,
            "y": 48,
            "width": 664,
            "height": 334,
            "rows": 9,
            "cols": 5,
        },
        # ================= SLIDE 8: CLOSING IMPACT & DELIVERABLES =================
        {
            "op": "add-textbox",
            "slide": "SLIDE_CLOSING",
            "x": 36,
            "y": 24,
            "width": 648,
            "height": 40,
            "text": "Executive Summary: The +$4.33M Geospatial Dividend",
            "font_size": 20,
            "bold": True,
            "color": "#FFFFFF",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_CLOSING",
            "x": 36,
            "y": 76,
            "width": 648,
            "height": 126,
            "background_color": "#064E3B",
            "text": "196.49 (Seed)  ➔  522.33 (National AE Ceiling)  ➔  684.90 (PDI 330-D Champion)\n\n• +$21.05M Total Incremental Sales Lift (+$14.23M vs Seed, +$4.33M over National AE)\n• 8.42x Campaign iROAS across Walmart Connect, Target Roundel, Kroger, Instacart & Amazon Fresh\n• 96.9% Residential Population Capture via Earth Engine WorldPop 100m (ST_REGIONSTATS) + L2 Norm",
            "font_size": 12,
            "bold": True,
            "color": "#ECFDF5",
            "alignment": "center",
            "content_alignment": "MIDDLE",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_CLOSING",
            "x": 36,
            "y": 218,
            "width": 314,
            "height": 152,
            "background_color": "#1E293B",
            "text": "Organized Project Workspace\n\n• Folder: circana_alpha_evolve_and_pdi/\n• Subfolders: cloud_run/, presentations/, static/, tests/, webapp/\n• Baseline preserved in: circan_alpha_evolve/\n• 11/11 Pytest Suite Passing (330-D L2 & WorldPop verified)",
            "font_size": 11,
            "color": "#E2E8F0",
        },
        {
            "op": "add-textbox",
            "slide": "SLIDE_CLOSING",
            "x": 370,
            "y": 218,
            "width": 314,
            "height": 152,
            "background_color": "#1E293B",
            "text": "Interactive Web Studio & 3D Assets\n\n• Google Maps PDI Playground (H3 Hex + S2 Level 12 Heatmap + Per-Cell Breakdown Chart)\n• Offline 3D Search-Space Video & GIF (alphaevolve_3d_landscape.mp4 / .gif)\n• BigQuery GIS + WorldPop 100m SQL Pipeline",
            "font_size": 11,
            "color": "#E2E8F0",
        },
    ]

    # Add set-table-cell ops for Slide 7 table
    for r_idx, row in enumerate(table_rows):
        for c_idx, val in enumerate(row):
            is_hdr = r_idx == 0
            is_pdi_row = r_idx >= 6
            bg = "#0F172A" if is_hdr else ("#ECFDF5" if is_pdi_row else ("#F8FAFC" if r_idx % 2 == 1 else "#FFFFFF"))
            fg = "#FFFFFF" if is_hdr else ("#065F46" if is_pdi_row else "#1E293B")
            ops.append(
                {
                    "op": "set-table-cell",
                    "table": "S7_TBL",
                    "row": r_idx,
                    "col": c_idx,
                    "text": val,
                    "font_size": 9,
                    "bold": is_hdr or is_pdi_row or c_idx in (0, 4),
                    "color": fg,
                    "background_color": bg,
                }
            )

    batch_path = pathlib.Path("/tmp/pdi_exec_deck_batch.json")
    batch_path.write_text(json.dumps(ops, indent=2), encoding="utf-8")

    print("[2/5] Applying 8-slide batch layout & typography...")
    batch_out = run_gslides(["mutate", "batch", pres_id, "--file", str(batch_path), "--json"])
    # Parse resolved_ids from batch JSON response
    json_line = [ln for ln in batch_out.splitlines() if ln.strip().startswith("{")][-1]
    resolved = json.loads(json_line).get("resolved_ids", {})
    print("      Resolved Slide IDs:", resolved)

    s_3d = resolved.get("SLIDE_3D_VIS", "SLIDE_3D_VIS")
    s_map = resolved.get("SLIDE_PDI_MAP", "SLIDE_PDI_MAP")
    s_charts = resolved.get("SLIDE_CHARTS", "SLIDE_CHARTS")

    print("[3/5] Inserting animated 3D GIF and PDI Web Studio snapshots...")
    # Slide 4: Full-bleed animated 3D GIF
    run_gslides(
        [
            "mutate",
            "insert-image-from-file",
            pres_id,
            "--slide",
            s_3d,
            "--file",
            str(STATIC_DIR / "alphaevolve_3d_landscape.gif"),
            "--x",
            "0",
            "--y",
            "0",
            "--width",
            "720",
            "--height",
            "405",
        ]
    )

    # Slide 5: Left = PDI Playground Web Studio snapshot, Right = Multimodal 330-D GNN diagram
    run_gslides(
        [
            "mutate",
            "insert-image-from-file",
            pres_id,
            "--slide",
            s_map,
            "--file",
            "/tmp/pdi_snap_playground.png",
            "--x",
            "28",
            "--y",
            "70",
            "--width",
            "445",
            "--height",
            "296",
        ]
    )
    run_gslides(
        [
            "mutate",
            "insert-image-from-file",
            pres_id,
            "--slide",
            s_map,
            "--file",
            str(STATIC_DIR / "s40_pdi_diagram_4.png"),
            "--x",
            "482",
            "--y",
            "96",
            "--width",
            "212",
            "--height",
            "240",
        ]
    )

    # Slide 6: 6 Dynamic Optimization Charts + BigQuery WorldPop SQL snapshot
    run_gslides(
        [
            "mutate",
            "insert-image-from-file",
            pres_id,
            "--slide",
            s_charts,
            "--file",
            "/tmp/pdi_snap_charts.png",
            "--x",
            "64",
            "--y",
            "68",
            "--width",
            "592",
            "--height",
            "325",
        ]
    )

    print("[4/5] Exporting PDF to presentations/circana_pdi_alphaevolve_executive_deck.pdf...")
    pdf_out = PRES_DIR / "circana_pdi_alphaevolve_executive_deck.pdf"
    run_gslides(["readonly", "export", pres_id, str(pdf_out), "--format", "pdf"])

    print(f"[5/5] Done! Presentation URL: https://docs.google.com/presentation/d/{pres_id}/edit")


if __name__ == "__main__":
    main()

