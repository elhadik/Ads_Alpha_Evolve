#!/usr/bin/env python3
"""Offline 3D Visualization Video & GIF Generator for Circana × AlphaEvolve.

Reproduces the Google Cloud 'AlphaEvolve Live' (Slide 12 / Slide 15) 3D aesthetic
100% offline using NumPy + Pillow + FFmpeg:
  1. Perspective 3D multi-peak wireframe/ridgeline fitness landscape (amber -> coral/magenta -> cyan/blue)
  2. Glowing # EVOLVE-BLOCK Python code lines projected in 3D perspective onto the Z=0 ground plane
  3. Vertical dotted candidate beacon pins ('o---') rising from local & global optima across generations
  4. Isometric 3D 5-RMN x 8-Week ad-flighting bar matrix morphing from Seed (196.49) -> Best Evolved (522.33)
  5. Frame 0 is rendered at the climax state so Google Slides PDF exports show the full 3D visual,
     while Google Slides live mode and PPTX exports play the full looping 3D camera & evolution animation.
"""

from __future__ import annotations

import math
import pathlib
import subprocess
import sys
from typing import Any, Dict, List, Tuple

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import evaluator  # noqa: E402
from webapp.server import CANDIDATE_EVOLVE_BLOCKS  # noqa: E402

OUT_DIR = ROOT_DIR / "webapp" / "static"
MP4_PATH = OUT_DIR / "alphaevolve_3d_landscape.mp4"
WEBM_PATH = OUT_DIR / "alphaevolve_3d_landscape.webm"
GIF_PATH = OUT_DIR / "alphaevolve_3d_landscape.gif"
POSTER_PATH = OUT_DIR / "alphaevolve_3d_poster.png"

WIDTH = 1600
HEIGHT = 900
FPS = 20
N_FRAMES = 72  # 3.6s seamless loop


def load_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if mono:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    for path in candidates:
        if pathlib.Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def evaluate_milestones() -> List[Dict[str, Any]]:
    """Evaluate all 6 progressive Circana AlphaEvolve milestones via evaluator.py."""
    base_code = (ROOT_DIR / "initial_program.py").read_text(encoding="utf-8")
    start_marker = "# EVOLVE-BLOCK-START"
    end_marker = "# EVOLVE-BLOCK-END"
    s_idx = base_code.index(start_marker)
    e_idx = base_code.index(end_marker) + len(end_marker)

    results = []
    for idx, item in enumerate(CANDIDATE_EVOLVE_BLOCKS):
        replaced = (
            base_code[:s_idx]
            + f"{start_marker}\n{item['evolve_block']}\n{end_marker}"
            + base_code[e_idx:]
        )
        eval_res = evaluator.evaluate_program(replaced)
        tel = eval_res["telemetry"]
        results.append(
            {
                "index": idx,
                "stage_id": item["stage_id"],
                "nickname": item["nickname"],
                "model_used": item["model_used"],
                "summary": item["summary"],
                "evolve_block": item["evolve_block"],
                "score": float(eval_res["score"]),
                "lift_musd": float(tel["incremental_lift_musd"]),
                "iroas": float(tel["iroas"]),
                "schedule": np.asarray(tel["allocation_matrix_musd"], dtype=float),
            }
        )
    return results


def build_fitness_landscape(nx: int = 116, ny: int = 76) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Construct the multi-peak 3D algorithmic fitness surface Z(X, Y)."""
    x = np.linspace(-3.4, 3.4, nx)
    y = np.linspace(-2.3, 2.3, ny)
    xx, yy = np.meshgrid(x, y)

    # Multi-modal optimization peaks matching Slide 12 / Slide 15 topography
    peaks = [
        # (cx, cy, amp, sx, sy)
        (-2.15, -0.55, 0.52, 0.72, 0.62),  # Seed / dead-zone foothills (amber)
        (-1.25, 0.65, 0.76, 0.65, 0.58),   # M1 S-curve threshold ridge (amber-orange)
        (-0.45, -0.22, 1.18, 0.62, 0.52),  # M2 OOS cap peak (orange-coral)
        (0.22, -0.10, 1.48, 0.58, 0.50),   # M3 Pantry cooldown massif (magenta-coral)
        (1.12, 0.42, 1.72, 0.56, 0.52),    # M4 Cross-RMN dedup peak (teal-cyan)
        (2.05, 0.82, 2.02, 0.62, 0.55),    # M5 Global Optimum Nova-Phoenix peak (emerald-cyan)
        (1.55, -0.78, 0.96, 0.60, 0.50),   # Secondary blue ridge
    ]
    zz = np.zeros_like(xx)
    for cx, cy, amp, sx, sy in peaks:
        zz += amp * np.exp(-(((xx - cx) / sx) ** 2 + ((yy - cy) / sy) ** 2))

    # Add fine high-frequency algorithmic ruggedness / local optima ripples
    ripples = (
        0.13 * np.sin(5.2 * xx + 1.7 * yy) * np.cos(4.6 * yy - 1.3 * xx)
        + 0.08 * np.sin(11.0 * xx - 3.5 * yy) * np.sin(8.5 * yy + 2.0 * xx)
        + 0.05 * np.cos(16.0 * xx + 9.0 * yy)
    )
    envelope = np.clip(zz / 0.45, 0.08, 1.0)
    zz = np.maximum(0.0, zz + ripples * envelope)
    return xx, yy, zz


def terrain_color(x_val: float, y_val: float, z_val: float) -> Tuple[int, int, int]:
    """Map (x, y, z) to the Slide 12 gradient: Amber -> Coral/Magenta -> Cyan/Teal -> Deep Blue."""
    t = np.clip((x_val + 2.8) / 5.4, 0.0, 1.0)
    if t < 0.33:
        u = t / 0.33
        r = int(235 * (1 - u) + 242 * u)
        g = int(145 * (1 - u) + 92 * u)
        b = int(38 * (1 - u) + 115 * u)
    elif t < 0.64:
        u = (t - 0.33) / 0.31
        r = int(242 * (1 - u) + 45 * u)
        g = int(92 * (1 - u) + 212 * u)
        b = int(115 * (1 - u) + 191 * u)
    else:
        u = (t - 0.64) / 0.36
        r = int(45 * (1 - u) + 38 * u)
        g = int(212 * (1 - u) + 165 * u)
        b = int(191 * (1 - u) + 245 * u)

    if y_val < -0.35 and x_val > 0.7:
        # Deep cobalt/indigo foreground-right flank like Slide 12
        r = int(r * 0.55 + 35)
        g = int(g * 0.68 + 45)
        b = min(255, int(b * 1.05 + 45))

    bright = float(np.clip(0.48 + 0.78 * (z_val / 1.35), 0.34, 1.35))
    return (
        int(np.clip(r * bright, 24, 255)),
        int(np.clip(g * bright, 24, 255)),
        int(np.clip(b * bright, 32, 255)),
    )


def project_3d(
    pts: np.ndarray,
    yaw: float,
    pitch: float = 0.40,
    cam_dist: float = 8.4,
    focal: float = 1180.0,
    cx: float = WIDTH * 0.47,
    cy: float = HEIGHT * 0.59,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Project (N, 3) world coordinates (x, y, z) to screen (sx, sy, depth)."""
    c_y, s_y = math.cos(yaw), math.sin(yaw)
    c_p, s_p = math.cos(pitch), math.sin(pitch)

    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    # Rotate around Z (yaw)
    xr = x * c_y - y * s_y
    yr = x * s_y + y * c_y
    zr = z

    # Tilt camera (pitch around X)
    yc = yr * c_p + zr * s_p
    zc = -yr * s_p + zr * c_p

    depth = cam_dist + yc
    depth = np.maximum(depth, 0.5)
    sx = cx + (xr / depth) * focal
    sy = cy - (zc / depth) * focal
    return sx, sy, depth


CODE_GROUND_LINES = [
    "def allocate_rmn_flighting(model: Mapping[str, Any]) -> np.ndarray:",
    "    hill_k = np.asarray(model['hill_k_musd'], dtype=float)",
    "    inv_cap = np.asarray(model['inventory_cap_musd'], dtype=float)",
    "    overlap = np.asarray(model['overlap_matrix'], dtype=float)",
    "    # Cosine annealing & marginal Hill-elasticity coordinate ascent",
    "    h_val = (spend ** hill_n[r]) / (hill_k[r] ** hill_n[r] + spend ** hill_n[r])",
    "    ov_mult = max(0.45, 1.0 - 0.32 * float(overlap[r] @ active_int))",
    "    gain = (max_lift[r] * seasonality[r, t] * h_val * pantry_pen * ov_mult) / spend",
    "    schedule[best_pair[0], best_pair[1]] = min(1.62 * hill_k[r], inv_cap[r, t])",
    "    return schedule  # EVOLVE-BLOCK-END",
]


def draw_code_ground_plane(draw: ImageDraw.ImageDraw, yaw: float) -> None:
    """Draw the glowing perspective code lines & grid on the Z=0 base plane (like Slide 12 & 15)."""
    # 1. Perspective grid lines on Z = -0.02
    for gx in np.linspace(-3.5, 3.5, 29):
        pts = np.array([[gx, -2.4, -0.02], [gx, 2.4, -0.02]])
        sx, sy, _ = project_3d(pts, yaw)
        draw.line([(sx[0], sy[0]), (sx[1], sy[1])], fill=(38, 48, 68, 95), width=1)

    for gy in np.linspace(-2.4, 2.4, 21):
        pts = np.array([[-3.5, gy, -0.02], [3.5, gy, -0.02]])
        sx, sy, _ = project_3d(pts, yaw)
        draw.line([(sx[0], sy[0]), (sx[1], sy[1])], fill=(45, 58, 82, 95), width=1)

    # 2. Glowing tokenized code rows across the foreground Z=0 plane
    rng = np.random.default_rng(42)
    for row_idx in range(36):
        gy = -2.35 + row_idx * 0.085
        line_str = CODE_GROUND_LINES[row_idx % len(CODE_GROUND_LINES)]
        for col_block in range(3):
            x_start = -3.35 + col_block * 2.28 + (row_idx % 3) * 0.12
            cursor = x_start
            for ch_idx, ch in enumerate(line_str[:46]):
                if ch == " ":
                    cursor += 0.042
                    continue
                seg_len = 0.028 if ch not in ("_", "=", "(") else 0.04
                pts = np.array([[cursor, gy, -0.01], [cursor + seg_len, gy, -0.01]])
                sx, sy, depth = project_3d(pts, yaw)
                fade = float(np.clip((8.8 - depth[0]) / 3.4, 0.18, 1.0))
                if "#" in line_str and ch_idx > line_str.index("#"):
                    col = (int(95 * fade), int(185 * fade), int(155 * fade), int(175 * fade))
                else:
                    col = (int(155 * fade), int(168 * fade), int(198 * fade), int(165 * fade))
                draw.line([(sx[0], sy[0]), (sx[1], sy[1])], fill=col, width=1)
                cursor += 0.042 + (rng.random() * 0.004)


def draw_rmn_3d_inset(
    draw: ImageDraw.ImageDraw,
    schedule: np.ndarray,
    stage_idx: int,
    pulse_phase: float,
) -> None:
    """Draw an isometric 3D 5-RMN x 8-Week ad flighting bar matrix on the top-right."""
    panel_x, panel_y, panel_w, panel_h = 1135, 92, 430, 255
    draw.rounded_rectangle(
        [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
        radius=14,
        fill=(9, 14, 26, 215),
        outline=(56, 189, 248, 110),
        width=1,
    )
    font_sm = load_font(12, bold=True)
    font_xs = load_font(10, mono=True)
    draw.text(
        (panel_x + 16, panel_y + 12),
        "3D RMN FLIGHTING MATRIX (5 RETAILERS × 8 WEEKS)",
        fill=(148, 163, 184, 255),
        font=font_sm,
    )

    rmn_colors = [
        (245, 158, 11),  # Walmart
        (244, 63, 94),   # Target
        (168, 85, 247),  # Kroger
        (16, 185, 129),  # Instacart
        (56, 189, 248),  # Amazon Fresh
    ]
    rmn_short = ["WMT", "TGT", "KRG", "INS", "AMZ"]

    origin_x = panel_x + 165
    origin_y = panel_y + 188
    dx_w, dy_w = 24.0, -7.5
    dx_r, dy_r = -19.0, 11.0

    # Back-to-front isometric painter's order
    for r in range(5):
        # RMN label
        lx = origin_x + r * dx_r - 36
        ly = origin_y + r * dy_r - 4
        draw.text((lx, ly), rmn_short[r], fill=rmn_colors[r] + (230,), font=font_xs)
        for w in range(7, -1, -1):
            bx = origin_x + w * dx_w + r * dx_r
            by = origin_y + w * dy_w + r * dy_r
            spend = float(schedule[r, w])
            bar_h = max(3.0, min(82.0, spend * 410.0))
            base_c = rmn_colors[r]

            # Draw floor tile
            tile = [
                (bx, by),
                (bx + 15, by - 5),
                (bx + 5, by + 5),
                (bx - 10, by + 10),
            ]
            draw.polygon(tile, fill=(22, 32, 52, 160), outline=(51, 65, 85, 140))

            if spend > 0.015:
                # 3D isometric prism for active ad flight
                top_face = [
                    (bx, by - bar_h),
                    (bx + 14, by - 4 - bar_h),
                    (bx + 5, by + 4 - bar_h),
                    (bx - 9, by + 8 - bar_h),
                ]
                left_face = [
                    (bx - 9, by + 8 - bar_h),
                    (bx + 5, by + 4 - bar_h),
                    (bx + 5, by + 4),
                    (bx - 9, by + 8),
                ]
                right_face = [
                    (bx + 5, by + 4 - bar_h),
                    (bx + 14, by - 4 - bar_h),
                    (bx + 14, by - 4),
                    (bx + 5, by + 4),
                ]
                draw.polygon(
                    left_face,
                    fill=(int(base_c[0] * 0.72), int(base_c[1] * 0.72), int(base_c[2] * 0.72), 235),
                )
                draw.polygon(
                    right_face,
                    fill=(int(base_c[0] * 0.50), int(base_c[1] * 0.50), int(base_c[2] * 0.50), 235),
                )
                draw.polygon(
                    top_face,
                    fill=(min(255, int(base_c[0] * 1.15)), min(255, int(base_c[1] * 1.15)), min(255, int(base_c[2] * 1.15)), 255),
                )


def render_frame(
    frame_idx: int,
    xx: np.ndarray,
    yy: np.ndarray,
    zz: np.ndarray,
    milestones: List[Dict[str, Any]],
) -> Image.Image:
    """Render a single 1600x900 Slide-12-style 3D frame."""
    # Frame 0 is the climax frame (progress=1.0) so static PDF export shows the full 3D state!
    if frame_idx == 0:
        progress = 1.0
        yaw = -0.24
    else:
        t_norm = (frame_idx - 1) / float(N_FRAMES - 1)
        progress = min(1.0, t_norm * 1.18)
        yaw = -0.44 + 0.36 * math.sin(t_norm * math.pi * 1.0)

    # Active milestone index based on progress
    active_m_idx = min(len(milestones) - 1, int(progress * len(milestones)))
    if progress >= 0.96:
        active_m_idx = len(milestones) - 1
    active_m = milestones[active_m_idx]

    # Smoothly interpolate schedule between milestones
    exact_pos = progress * (len(milestones) - 1)
    m_lo = int(math.floor(exact_pos))
    m_hi = min(len(milestones) - 1, m_lo + 1)
    frac = exact_pos - m_lo
    interp_sched = (1.0 - frac) * milestones[m_lo]["schedule"] + frac * milestones[m_hi]["schedule"]
    interp_score = (1.0 - frac) * milestones[m_lo]["score"] + frac * milestones[m_hi]["score"]
    interp_lift = (1.0 - frac) * milestones[m_lo]["lift_musd"] + frac * milestones[m_hi]["lift_musd"]
    interp_iroas = (1.0 - frac) * milestones[m_lo]["iroas"] + frac * milestones[m_hi]["iroas"]

    base = Image.new("RGBA", (WIDTH, HEIGHT), (4, 6, 12, 255))
    glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_base = ImageDraw.Draw(base, "RGBA")
    draw_glow = ImageDraw.Draw(glow_layer, "RGBA")

    # 1. Draw glowing # EVOLVE-BLOCK code ground plane at Z=0
    draw_code_ground_plane(draw_base, yaw)

    # 2. Project 3D fitness surface mesh
    ny, nx = zz.shape
    z_scale = 0.55 + 0.82 * min(1.0, 0.30 + progress * 0.85)
    pts = np.stack([xx.ravel(), yy.ravel(), (zz * z_scale).ravel()], axis=1)
    sx, sy, depth = project_3d(pts, yaw)
    sx = sx.reshape(ny, nx)
    sy = sy.reshape(ny, nx)
    depth = depth.reshape(ny, nx)

    # Sort grid cells back-to-front by depth (painter's algorithm)
    cell_depths = 0.25 * (depth[:-1, :-1] + depth[1:, :-1] + depth[:-1, 1:] + depth[1:, 1:])
    order = np.argsort(-cell_depths.ravel())
    ys, xs = np.unravel_index(order, cell_depths.shape)

    for j, i in zip(ys, xs):
        z_val = float(zz[j, i] * z_scale)
        x_val = float(xx[j, i])
        y_val = float(yy[j, i])
        r, g, b = terrain_color(x_val, y_val, z_val)

        poly = [
            (float(sx[j, i]), float(sy[j, i])),
            (float(sx[j, i + 1]), float(sy[j, i + 1])),
            (float(sx[j + 1, i + 1]), float(sy[j + 1, i + 1])),
            (float(sx[j + 1, i]), float(sy[j + 1, i])),
        ]
        # Dark occluded fill so ridgelines hide background lines cleanly
        fill_col = (int(r * 0.14), int(g * 0.14), int(b * 0.18), 238)
        line_alpha = int(np.clip(135 + z_val * 75, 110, 255))
        line_col = (r, g, b, line_alpha)
        draw_base.polygon(poly, fill=fill_col)
        draw_base.line([poly[0], poly[1], poly[2]], fill=line_col, width=1)
        if z_val > 0.28 and (i + j) % 2 == 0:
            draw_glow.line([poly[0], poly[1], poly[2]], fill=(r, g, b, int(min(210, 70 + z_val * 65))), width=2)

    # 3. Draw vertical dotted candidate beacon pins ('o---') like Slide 12!
    beacon_defs = [
        # (x, y, pin_h, milestone_idx, label, is_major)
        (-2.20, -0.58, 0.58, 0, f"Gen 1 Seed: {milestones[0]['score']:.1f}", True),
        (-1.72, -0.15, 0.42, 0, "", False),
        (-1.32, 0.62, 0.66, 1, f"M1 S-Curve: {milestones[1]['score']:.1f}", True),
        (-0.92, 0.12, 0.45, 1, "", False),
        (-0.55, -0.25, 0.72, 2, f"M2 OOS Gate: {milestones[2]['score']:.1f}", True),
        (-0.12, 0.38, 0.48, 2, "", False),
        (0.12, 0.12, 0.92, 3, f"M3 Pantry: {milestones[3]['score']:.1f}", True),
        (0.58, -0.45, 0.52, 3, "", False),
        (0.78, 0.18, 0.50, 4, "", False),
        (1.05, -0.18, 0.68, 4, f"M4 Dedup: {milestones[4]['score']:.1f}", True),
        (1.52, 0.58, 0.62, 5, "", False),
        (2.08, 0.82, 1.08, 5, f"★ Best: {milestones[5]['score']:.1f} (+165.8%)", True),
    ]

    font_pin = load_font(12, bold=True)
    for bx, by, bh, m_idx, label, is_major in beacon_defs:
        if m_idx > active_m_idx:
            continue
        # Find nearest surface height
        ix = int(np.argmin(np.abs(xx[0] - bx)))
        iy = int(np.argmin(np.abs(yy[:, 0] - by)))
        bz = float(zz[iy, ix] * z_scale)

        pin_pts = np.array([[bx, by, bz], [bx, by, bz + bh]])
        psx, psy, _ = project_3d(pin_pts, yaw)
        x0, y0 = float(psx[0]), float(psy[0])
        x1, y1 = float(psx[1]), float(psy[1])

        r, g, b = terrain_color(bx, by, bz + 0.4)
        pin_col = (min(255, r + 45), min(255, g + 45), min(255, b + 45), 245)

        # Dotted vertical stalk
        n_dots = 14 if is_major else 9
        for d_i in range(n_dots):
            u = d_i / float(n_dots)
            dx = x0 + (x1 - x0) * u
            dy = y0 + (y1 - y0) * u
            rad = 1.6 if is_major else 1.2
            draw_base.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=pin_col)

        # Top ring ('o') like Slide 12
        ring_r = 5.5 if is_major else 4.0
        draw_base.ellipse(
            [x1 - ring_r, y1 - ring_r, x1 + ring_r, y1 + ring_r],
            outline=(255, 255, 255, 245),
            width=2,
        )
        draw_glow.ellipse(
            [x1 - ring_r * 2.2, y1 - ring_r * 2.2, x1 + ring_r * 2.2, y1 + ring_r * 2.2],
            fill=(r, g, b, 150),
        )

        if is_major and label:
            is_curr = m_idx == active_m_idx
            tw = len(label) * 7 + 16
            tx = x1 - tw // 2
            ty = y1 - 30
            bg_c = (16, 185, 129, 230) if m_idx == 5 else ((30, 41, 59, 215) if not is_curr else (59, 130, 246, 230))
            draw_base.rounded_rectangle(
                [tx, ty, tx + tw, ty + 20],
                radius=6,
                fill=bg_c,
                outline=(255, 255, 255, 180 if is_curr else 90),
                width=1,
            )
            draw_base.text((tx + 8, ty + 3), label, fill=(255, 255, 255, 255), font=font_pin)

    # 5. Apply multi-pass Gaussian bloom for the neon Slide 12 glow
    bloom_wide = glow_layer.filter(ImageFilter.GaussianBlur(radius=22))
    bloom_tight = glow_layer.filter(ImageFilter.GaussianBlur(radius=6))
    base = Image.alpha_composite(base, bloom_wide)
    base = Image.alpha_composite(base, bloom_tight)
    draw_hud = ImageDraw.Draw(base, "RGBA")

    # 6. Top Bar: Google Cloud | AlphaEvolve Live (matching Slide 12)
    font_brand = load_font(20, bold=True)
    font_subbrand = load_font(20, bold=False)
    font_title = load_font(30, bold=True)
    font_subtitle = load_font(15, bold=False)
    font_kpi_lbl = load_font(11, bold=True)
    font_kpi_val = load_font(22, bold=True)
    font_code = load_font(12, mono=True)

    draw_hud.text((42, 32), "Google Cloud", fill=(248, 250, 252, 255), font=font_brand)
    draw_hud.line([(186, 32), (186, 56)], fill=(100, 116, 139, 200), width=1)
    draw_hud.text((200, 32), "AlphaEvolve Live × Circana Liquid Data®", fill=(203, 213, 225, 255), font=font_subbrand)

    # Top-right "Live Demo" blue pill button from Slide 12
    draw_hud.rounded_rectangle(
        [1355, 24, 1565, 68],
        radius=22,
        fill=(37, 132, 255, 255),
    )
    draw_hud.text((1386, 36), "Live 3D Evolution", fill=(255, 255, 255, 255), font=load_font(16, bold=True))

    # 7. Isometric 3D 5x8 RMN Flighting Matrix Inset
    draw_rmn_3d_inset(draw_hud, interp_sched, active_m_idx, progress)

    # 8. Center-Bottom Headline & KPI Dashboard Bar
    draw_hud.text(
        (42, 684),
        "Evolutionary 3D Search Space: Retail Media Flighting",
        fill=(255, 255, 255, 255),
        font=font_title,
    )
    short_sum = active_m["summary"]
    if len(short_sum) > 74:
        short_sum = short_sum[:71] + "..."
    draw_hud.text(
        (42, 728),
        f"Stage [{active_m_idx + 1}/6] ({active_m['nickname']}): {short_sum}",
        fill=(148, 163, 184, 255),
        font=font_subtitle,
    )

    # KPI Cards along bottom-left
    kpis = [
        ("EVALUATOR SCORE", f"{interp_score:.2f}", "+165.8% vs Seed", (16, 185, 129)),
        ("INCREMENTAL LIFT", f"${interp_lift:.2f}M", "Net-New CPG Sales", (56, 189, 248)),
        ("CAMPAIGN iROAS", f"{interp_iroas:.2f}x", "$2.50M Ad Budget", (245, 158, 11)),
        ("ACTIVE MODEL", active_m["model_used"].split()[0], f"Stage {active_m_idx + 1} / 6", (244, 63, 94)),
    ]
    for k_i, (k_lbl, k_val, k_sub, k_col) in enumerate(kpis):
        kx = 42 + k_i * 238
        ky = 772
        draw_hud.rounded_rectangle(
            [kx, ky, kx + 224, ky + 96],
            radius=12,
            fill=(15, 23, 42, 220),
            outline=k_col + (135,),
            width=1,
        )
        draw_hud.text((kx + 14, ky + 12), k_lbl, fill=(148, 163, 184, 255), font=font_kpi_lbl)
        draw_hud.text((kx + 14, ky + 32), k_val, fill=(255, 255, 255, 255), font=font_kpi_val)
        draw_hud.text((kx + 14, ky + 66), k_sub, fill=k_col + (240,), font=font_kpi_lbl)

    # Bottom-Right # EVOLVE-BLOCK Live Code Card
    cx0, cy0, cw, ch = 1015, 705, 550, 163
    draw_hud.rounded_rectangle(
        [cx0, cy0, cx0 + cw, cy0 + ch],
        radius=12,
        fill=(9, 13, 24, 230),
        outline=(99, 102, 241, 140),
        width=1,
    )
    draw_hud.text(
        (cx0 + 14, cy0 + 10),
        f"# EVOLVE-BLOCK ({active_m['nickname']} — {active_m['model_used']})",
        fill=(129, 140, 248, 255),
        font=font_kpi_lbl,
    )
    code_lines = [ln for ln in active_m["evolve_block"].splitlines() if ln.strip()][:6]
    for l_idx, ln in enumerate(code_lines):
        clipped = ln[:64] + ("..." if len(ln) > 64 else "")
        draw_hud.text(
            (cx0 + 14, cy0 + 34 + l_idx * 20),
            clipped,
            fill=(226, 232, 240, 235),
            font=font_code,
        )

    return base.convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("[1/4] Evaluating 6 Circana AlphaEvolve milestones via evaluator.py...")
    milestones = evaluate_milestones()
    for m in milestones:
        print(f"      - {m['nickname']:20s}: Score={m['score']:6.2f} | Lift=${m['lift_musd']:5.2f}M | iROAS={m['iroas']:.2f}x")

    print("[2/4] Building 3D multi-peak fitness landscape mesh...")
    xx, yy, zz = build_fitness_landscape()

    print(f"[3/4] Rendering {N_FRAMES} frames at {WIDTH}x{HEIGHT} ({FPS} fps)...")
    frames: List[Image.Image] = []
    for idx in range(N_FRAMES):
        img = render_frame(idx, xx, yy, zz, milestones)
        frames.append(img)
        if idx == 0:
            img.save(POSTER_PATH, format="PNG")
            print(f"      Saved climax Frame 0 poster -> {POSTER_PATH}")

    print("[4/4] Encoding MP4 video and high-res looping GIF via ffmpeg...")
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-crf",
        "18",
        "-preset",
        "fast",
        str(MP4_PATH),
    ]
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdin is not None
    for f in frames:
        proc.stdin.write(f.tobytes())
    _, stderr_bytes = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg MP4 encoding failed: {stderr_bytes.decode('utf-8', errors='replace')}")

    # Generate high-quality palette-optimized GIF (1280x720 for fast Google Slides embedding)
    gif_cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(MP4_PATH),
        "-vf",
        "fps=15,scale=1280:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=256:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=3",
        "-loop",
        "0",
        str(GIF_PATH),
    ]
    subprocess.run(gif_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Done!\n  MP4:    {MP4_PATH} ({MP4_PATH.stat().st_size / 1024:.1f} KB)\n  GIF:    {GIF_PATH} ({GIF_PATH.stat().st_size / 1024:.1f} KB)\n  Poster: {POSTER_PATH} ({POSTER_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
