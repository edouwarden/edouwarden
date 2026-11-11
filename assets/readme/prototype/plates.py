#!/usr/bin/env python3
"""Render the selected proof plate — a custom flat illustration — for every
project in the deck.

Each card keeps the same anatomy: number, title, meta, hook, three project
stats, stack, and a 360 x 203 illustration drawn inline as SVG in the ambient
palette. The illustrations are scenes and objects, not screenshots: a dashboard,
an engine editor, a seeded height field, a shell terminal, a raycast corridor, an
IRC frame, a Docker host, and a VM window on a host.

Standalone: production README and build.py are untouched.

    python3 assets/readme/prototype/plates.py
"""

import math
from pathlib import Path

from playwright.sync_api import sync_playwright

from embed import write_image_svg

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
BUILD = HERE.parent / ".build"

NAVY = "#0c0a3e"
LIFT = "#17134f"
CORAL = "#f9564f"
DEEP = "#dd453d"
PAPER = "#fffaf0"


def label(x, y, text, size=6.5, fill=PAPER, opacity=0.7, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="Plex Mono, monospace" '
        f'font-size="{size}" fill="{fill}" fill-opacity="{opacity}" '
        f'font-weight="{weight}" text-anchor="{anchor}">{text}</text>'
    )


def art(body: str) -> str:
    """Shared ambient backdrop for every non-dashboard illustration."""
    return f"""
<svg viewBox="0 0 360 203" width="360" height="203" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NAVY}"/>
      <stop offset="1" stop-color="{LIFT}"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{CORAL}" stop-opacity=".22"/>
      <stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".7" fill="{PAPER}" opacity=".07"/>
    </pattern>
  </defs>
  <rect width="360" height="203" fill="url(#sky)"/>
  <rect width="360" height="203" fill="url(#dots)"/>
  <circle cx="304" cy="30" r="104" fill="url(#glow)"/>
  <circle cx="42" cy="186" r="76" fill="{CORAL}" opacity=".06"/>
  <rect x="14" y="16" width="332" height="174" rx="13" fill="{CORAL}" opacity=".07"/>
  <rect x="14.5" y="16.5" width="331" height="173" rx="12.5" fill="none" stroke="{CORAL}" stroke-opacity=".24"/>
  {body}
</svg>
"""


DASHBOARD_ART = f"""
<svg viewBox="0 0 360 203" width="360" height="203" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{NAVY}"/>
      <stop offset="1" stop-color="{LIFT}"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="{CORAL}" stop-opacity=".22"/>
      <stop offset="1" stop-color="{CORAL}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".7" fill="{PAPER}" opacity=".07"/>
    </pattern>
  </defs>

  <rect width="360" height="203" fill="url(#sky)"/>
  <rect width="360" height="203" fill="url(#dots)"/>
  <circle cx="304" cy="30" r="104" fill="url(#glow)"/>
  <circle cx="42" cy="186" r="76" fill="{CORAL}" opacity=".06"/>

  <rect x="14" y="16" width="332" height="174" rx="13" fill="{CORAL}" opacity=".16"/>

  <g>
    <rect x="16" y="18" width="328" height="170" rx="12" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".16"/>
    <path d="M16,30 a12,12 0 0 1 12,-12 h304 a12,12 0 0 1 12,12 v6 h-328 z" fill="{NAVY}"/>
    <line x1="16" y1="36" x2="344" y2="36" stroke="{PAPER}" stroke-opacity=".1"/>
    <circle cx="27" cy="27" r="2.6" fill="{CORAL}"/>
    <circle cx="35" cy="27" r="2.6" fill="{DEEP}"/>
    <circle cx="43" cy="27" r="2.6" fill="{PAPER}" opacity=".5"/>
    <rect x="286" y="22" width="46" height="10" rx="5" fill="{CORAL}"/>
    <circle cx="293" cy="27" r="1.8" fill="{NAVY}"/>
    <rect x="299" y="25.5" width="24" height="3" rx="1.5" fill="{NAVY}" opacity=".6"/>
  </g>

  <rect x="16" y="36" width="56" height="152" fill="{NAVY}" opacity=".55"/>
  <line x1="72" y1="36" x2="72" y2="188" stroke="{PAPER}" stroke-opacity=".08"/>
  <rect x="24" y="46" width="40" height="12" rx="6" fill="{CORAL}"/>
  <rect x="30" y="50.5" width="21" height="3" rx="1.5" fill="{NAVY}"/>
  <g fill="{PAPER}" opacity=".2">
    <rect x="24" y="66" width="34" height="7" rx="3.5"/>
    <rect x="24" y="82" width="34" height="7" rx="3.5"/>
    <rect x="24" y="98" width="34" height="7" rx="3.5"/>
    <rect x="24" y="114" width="34" height="7" rx="3.5"/>
    <rect x="24" y="130" width="34" height="7" rx="3.5"/>
  </g>
  <circle cx="44" cy="172" r="9" fill="{CORAL}"/>
  <path d="M40,172 h8 M44,168 v8" stroke="{NAVY}" stroke-width="1.6" stroke-linecap="round"/>

  <g>
    <rect x="82" y="46" width="112" height="64" rx="7" fill="{NAVY}" stroke="{CORAL}" stroke-width="1.2"/>
    <rect x="88" y="52" width="34" height="4" rx="2" fill="{PAPER}" opacity=".38"/>
    <rect x="88" y="52" width="10" height="4" rx="2" fill="{CORAL}"/>
    <g>
      <rect x="88" y="64" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="104" y="64" width="14" height="8" rx="1.5" fill="{CORAL}"/>
      <rect x="120" y="64" width="14" height="8" rx="1.5" fill="{DEEP}"/>
      <rect x="136" y="64" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="152" y="64" width="14" height="8" rx="1.5" fill="{PAPER}" opacity=".28"/>
      <rect x="168" y="64" width="14" height="8" rx="1.5" fill="{CORAL}"/>

      <rect x="88" y="75" width="14" height="8" rx="1.5" fill="{DEEP}"/>
      <rect x="104" y="75" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="120" y="75" width="14" height="8" rx="1.5" fill="{CORAL}"/>
      <rect x="136" y="75" width="14" height="8" rx="1.5" fill="{PAPER}" opacity=".28"/>
      <rect x="152" y="75" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="168" y="75" width="14" height="8" rx="1.5" fill="{DEEP}"/>

      <rect x="88" y="86" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="104" y="86" width="14" height="8" rx="1.5" fill="{CORAL}"/>
      <rect x="120" y="86" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="136" y="86" width="14" height="8" rx="1.5" fill="{DEEP}"/>
      <rect x="152" y="86" width="14" height="8" rx="1.5" fill="{CORAL}"/>
      <rect x="168" y="86" width="14" height="8" rx="1.5" fill="{LIFT}"/>

      <rect x="88" y="97" width="14" height="8" rx="1.5" fill="{PAPER}" opacity=".28"/>
      <rect x="104" y="97" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="120" y="97" width="14" height="8" rx="1.5" fill="{DEEP}"/>
      <rect x="136" y="97" width="14" height="8" rx="1.5" fill="{LIFT}"/>
      <rect x="152" y="97" width="14" height="8" rx="1.5" fill="{CORAL}"/>
      <rect x="168" y="97" width="14" height="8" rx="1.5" fill="{LIFT}"/>
    </g>
    <rect x="166" y="95" width="8" height="8" rx="1.5" fill="none" stroke="{PAPER}" stroke-width="1.4"/>
  </g>

  <g>
    <rect x="202" y="46" width="64" height="64" rx="7" fill="{CORAL}"/>
    <rect x="210" y="54" width="22" height="3.5" rx="1.75" fill="{NAVY}" opacity=".5"/>
    <text x="210" y="86" font-family="Days One, sans-serif" font-size="25" fill="{NAVY}">7.4</text>
    <rect x="210" y="94" width="42" height="3" rx="1.5" fill="{NAVY}" opacity=".32"/>
    <rect x="210" y="100" width="28" height="3" rx="1.5" fill="{NAVY}" opacity=".22"/>
  </g>

  <g>
    <rect x="274" y="46" width="62" height="64" rx="7" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
    <g stroke="{PAPER}" stroke-opacity=".1">
      <line x1="282" y1="60" x2="328" y2="60"/>
      <line x1="282" y1="72" x2="328" y2="72"/>
      <line x1="282" y1="84" x2="328" y2="84"/>
      <line x1="282" y1="96" x2="328" y2="96"/>
    </g>
    <polyline points="282,98 290,88 298,92 306,78 314,84 322,68 330,74" fill="none" stroke="{CORAL}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="330" cy="74" r="2.2" fill="{PAPER}"/>
  </g>

  <g>
    <rect x="82" y="118" width="152" height="60" rx="7" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
    <rect x="90" y="124" width="36" height="4" rx="2" fill="{PAPER}" opacity=".32"/>
    <g stroke="{PAPER}" stroke-opacity=".08">
      <line x1="90" y1="140" x2="226" y2="140"/>
      <line x1="90" y1="154" x2="226" y2="154"/>
      <line x1="90" y1="168" x2="226" y2="168"/>
    </g>
    <path d="M90,164 L104,156 L118,160 L132,146 L146,152 L160,138 L174,144 L188,130 L202,136 L216,124 L226,128 L226,172 L90,172 Z" fill="{CORAL}" opacity=".12"/>
    <polyline points="90,164 104,156 118,160 132,146 146,152 160,138 174,144 188,130 202,136 216,124 226,128" fill="none" stroke="{CORAL}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  </g>

  <g>
    <rect x="242" y="118" width="94" height="60" rx="7" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
    <rect x="250" y="124" width="30" height="4" rx="2" fill="{PAPER}" opacity=".32"/>
    <g>
      <rect x="250" y="136" width="6" height="6" rx="1.5" fill="{CORAL}"/>
      <rect x="260" y="137.5" width="54" height="3" rx="1.5" fill="{PAPER}" opacity=".38"/>
      <rect x="250" y="148" width="6" height="6" rx="1.5" fill="{CORAL}"/>
      <rect x="260" y="149.5" width="44" height="3" rx="1.5" fill="{PAPER}" opacity=".3"/>
      <rect x="250" y="160" width="6" height="6" rx="1.5" fill="{PAPER}" opacity=".22"/>
      <rect x="260" y="161.5" width="50" height="3" rx="1.5" fill="{PAPER}" opacity=".22"/>
    </g>
  </g>

  <g transform="translate(288,166)">
    <rect width="50" height="16" rx="8" fill="{PAPER}"/>
    <circle cx="9" cy="8" r="2.6" fill="{CORAL}"/>
    <rect x="16" y="6.5" width="22" height="3" rx="1.5" fill="{NAVY}" opacity=".55"/>
  </g>
</svg>
"""


def art_transcendence() -> str:
    return art(f"""
  <g>
    <rect x="24" y="22" width="312" height="158" rx="12" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".2"/>
    <path d="M24,34 a12,12 0 0 1 12,-12 h288 a12,12 0 0 1 12,12 v16 h-312 z" fill="{LIFT}"/>
    <circle cx="41" cy="36" r="3.2" fill="{CORAL}"/>
    <circle cx="52" cy="36" r="3.2" fill="{DEEP}"/>
    <circle cx="63" cy="36" r="3.2" fill="{PAPER}" opacity=".4"/>
    {label(78, 40, "ThreeWrapper", 9, PAPER, 0.85, 500)}
    {label(171, 40, "scene · course.01", 7.5, PAPER, 0.4)}
    <rect x="270" y="30" width="54" height="14" rx="7" fill="{CORAL}"/>
    {label(297, 40, "EDITOR", 6.5, NAVY, 1, 500, "middle")}
    <line x1="24" y1="50" x2="336" y2="50" stroke="{PAPER}" stroke-opacity=".1"/>

    <rect x="24" y="50" width="84" height="130" fill="{NAVY}" opacity=".6"/>
    {label(34, 64, "SCENE", 6.5, CORAL, 0.8, 500)}
    <rect x="30" y="72" width="72" height="15" rx="4" fill="{CORAL}" opacity=".16"/>
    <path d="M36,77 l3.5,3.5 l-3.5,3.5" fill="none" stroke="{CORAL}" stroke-width="1.4"/>
    {label(45, 83, "environment", 7, PAPER, 0.9)}
    {label(45, 98, "modules", 7, PAPER, 0.55)}
    {label(45, 113, "physics", 7, PAPER, 0.55)}
    {label(45, 128, "camera", 7, PAPER, 0.55)}
    {label(45, 143, "lights", 7, PAPER, 0.55)}
    {label(45, 158, "input", 7, PAPER, 0.55)}
    <line x1="108" y1="50" x2="108" y2="180" stroke="{PAPER}" stroke-opacity=".09"/>

    <g stroke="{PAPER}" stroke-opacity=".055">
      <line x1="108" y1="68" x2="336" y2="68"/>
      <line x1="108" y1="90" x2="336" y2="90"/>
      <line x1="108" y1="112" x2="336" y2="112"/>
      <line x1="108" y1="134" x2="336" y2="134"/>
      <line x1="126" y1="50" x2="126" y2="164"/>
      <line x1="156" y1="50" x2="156" y2="164"/>
      <line x1="186" y1="50" x2="186" y2="164"/>
      <line x1="216" y1="50" x2="216" y2="164"/>
      <line x1="246" y1="50" x2="246" y2="164"/>
      <line x1="276" y1="50" x2="276" y2="164"/>
      <line x1="306" y1="50" x2="306" y2="164"/>
    </g>

    <g>
      <polygon points="168,104 208,84 248,104 208,124" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".55"/>
      <polygon points="168,104 208,124 208,140 168,120" fill="{DEEP}" opacity=".4"/>
      <polygon points="248,104 208,124 208,140 248,120" fill="{NAVY}"/>
      <polyline points="168,104 208,84 248,104" fill="none" stroke="{CORAL}" stroke-opacity=".8"/>
    </g>
    <g stroke="{CORAL}" stroke-opacity=".55" stroke-dasharray="4 4" fill="none">
      <rect x="170" y="86" width="76" height="38" transform="rotate(-1 208 105)"/>
    </g>
    <g fill="{CORAL}">
      <rect x="169" y="85" width="5" height="5"/>
      <rect x="241" y="85" width="5" height="5"/>
      <rect x="169" y="119" width="5" height="5"/>
      <rect x="241" y="119" width="5" height="5"/>
    </g>

    <g stroke="{PAPER}" stroke-opacity=".45" fill="none">
      <path d="M272,126 l14,-7 l14,7 l-14,7 z"/>
      <path d="M272,126 v10 l14,7 v-10"/>
      <path d="M300,126 v10 l-14,7"/>
    </g>

    <g stroke-linecap="round">
      <line x1="136" y1="146" x2="162" y2="146" stroke="{CORAL}" stroke-width="2.2"/>
      <polygon points="166,146 158,142 158,150" fill="{CORAL}"/>
      <line x1="136" y1="146" x2="136" y2="124" stroke="{PAPER}" stroke-width="2.2"/>
      <polygon points="136,120 132,128 140,128" fill="{PAPER}" opacity=".8"/>
      <line x1="136" y1="146" x2="150" y2="138" stroke="{DEEP}" stroke-width="2.2"/>
      <circle cx="136" cy="146" r="3" fill="{PAPER}"/>
    </g>

    <line x1="108" y1="164" x2="336" y2="164" stroke="{PAPER}" stroke-opacity=".09"/>
    {label(116, 175, "physics · rapier", 6.5, PAPER, 0.45)}
    {label(196, 175, "tick 20 Hz", 6.5, CORAL, 0.9, 500)}
    {label(316, 175, "60 fps", 6.5, PAPER, 0.35, 400, "end")}
  </g>
""")


def art_space() -> str:
    """A seeded height field sampled into a core column: how the world was generated."""
    cols, rows = 26, 15
    cell = 8.0
    mx, my = 28.0, 56.0
    seed = 4701234567
    scale = 0.085
    sample_i, sample_j = 14, 8

    def hash01(ix: int, iy: int, salt: int) -> float:
        n = (ix * 374761393 + iy * 668265263 + salt * 1442695041) & 0xFFFFFFFF
        n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
        return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0

    def value_noise(x: float, y: float, salt: int) -> float:
        x0, y0 = math.floor(x), math.floor(y)
        fx, fy = x - x0, y - y0
        sx = fx * fx * (3.0 - 2.0 * fx)
        sy = fy * fy * (3.0 - 2.0 * fy)
        n00 = hash01(x0, y0, salt)
        n10 = hash01(x0 + 1, y0, salt)
        n01 = hash01(x0, y0 + 1, salt)
        n11 = hash01(x0 + 1, y0 + 1, salt)
        top = n00 + (n10 - n00) * sx
        bottom = n01 + (n11 - n01) * sx
        return top + (bottom - top) * sy

    def fbm(x: float, y: float) -> float:
        total = 0.0
        norm = 0.0
        amp = 1.0
        freq = 1.0
        for octave in range(6):
            total += amp * value_noise(x * freq, y * freq, seed + octave * 131)
            norm += amp
            amp *= 0.55
            freq *= 2.0
        return total / norm

    field = [
        [fbm(2.7 + i * scale, 5.1 + j * scale * 0.66) for i in range(cols)]
        for j in range(rows)
    ]
    flat = [value for row in field for value in row]
    low, high = min(flat), max(flat)
    bands = [
        [min(4, int((value - low) / (high - low) * 5)) for value in row]
        for row in field
    ]

    fills = (
        (PAPER, 0.045),
        (PAPER, 0.10),
        (CORAL, 0.30),
        (CORAL, 0.62),
        (CORAL, 0.95),
    )

    cells = []
    grid = []
    contours = []
    for j, row in enumerate(bands):
        for i, band in enumerate(row):
            x = mx + i * cell
            y = my + j * cell
            color, opacity = fills[band]
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell:.1f}" height="{cell:.1f}" '
                f'fill="{color}" fill-opacity="{opacity}"/>'
            )
            if i + 1 < cols and band != bands[j][i + 1]:
                contours.append(
                    f'<line x1="{x + cell:.1f}" y1="{y:.1f}" '
                    f'x2="{x + cell:.1f}" y2="{y + cell:.1f}"/>'
                )
            if j + 1 < rows and band != bands[j + 1][i]:
                contours.append(
                    f'<line x1="{x:.1f}" y1="{y + cell:.1f}" '
                    f'x2="{x + cell:.1f}" y2="{y + cell:.1f}"/>'
                )
    for i in range(cols + 1):
        x = mx + i * cell
        grid.append(
            f'<line x1="{x:.1f}" y1="{my:.1f}" '
            f'x2="{x:.1f}" y2="{my + rows * cell:.1f}"/>'
        )
    for j in range(rows + 1):
        y = my + j * cell
        grid.append(
            f'<line x1="{mx:.1f}" y1="{y:.1f}" '
            f'x2="{mx + cols * cell:.1f}" y2="{y:.1f}"/>'
        )

    sx = mx + sample_i * cell
    sy = my + sample_j * cell
    scx = sx + cell / 2
    scy = sy + cell / 2

    # core column: four blocks wide, eight layers deep
    blocks = []
    bx, by = 273.0, 70.0
    bw, bh, gap = 11.0, 11.0, 1.0
    layer_fill = (
        (PAPER, 0.80),
        (PAPER, 0.30),
        (PAPER, 0.19),
        (PAPER, 0.30),
        (PAPER, 0.19),
        (PAPER, 0.46),
        (PAPER, 0.36),
        (DEEP, 0.30),
    )
    for layer in range(8):
        color, base = layer_fill[layer]
        for col in range(4):
            x = bx + col * (bw + gap)
            y = by + layer * (bh + gap)
            if layer == 7:
                blocks.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="1.5" '
                    f'fill="{color}" fill-opacity="{base}" '
                    f'stroke="{PAPER}" stroke-opacity=".32"/>'
                )
                blocks.append(
                    f'<path d="M{x + 2:.1f},{y + bh - 2:.1f} l3,-{bh - 4:.1f} '
                    f'm2,{bh - 4:.1f} l3,-{bh - 4:.1f}" '
                    f'fill="none" stroke="{PAPER}" stroke-opacity=".22"/>'
                )
            else:
                jitter = ((layer * 5 + col * 3) % 3 - 1) * 0.02
                opacity = max(0.04, min(0.92, base + jitter))
                blocks.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="1.5" '
                    f'fill="{color}" fill-opacity="{opacity:.2f}" '
                    f'stroke="{PAPER}" stroke-opacity=".12"/>'
                )
    for col in (0, 2):
        blocks.append(
            f'<circle cx="{bx + col * 12 + 5.5:.1f}" cy="{by + 5.5:.1f}" r="1.2" '
            f'fill="{CORAL}" opacity=".85"/>'
        )
    ores = (
        (1, 2, "iron"),
        (2, 1, "coal"),
        (3, 3, "iron"),
        (4, 0, "coal"),
        (4, 2, "coal"),
    )
    for layer, col, kind in ores:
        ox = bx + col * 12 + 5.5
        oy = by + layer * 12 + 5.5
        if kind == "iron":
            blocks.append(
                f'<rect x="{ox - 2:.1f}" y="{oy - 2:.1f}" width="4" height="4" '
                f'transform="rotate(45 {ox:.1f} {oy:.1f})" fill="{CORAL}"/>'
            )
        else:
            blocks.append(
                f'<rect x="{ox - 1.8:.1f}" y="{oy - 1.8:.1f}" width="3.6" height="3.6" '
                f'transform="rotate(45 {ox:.1f} {oy:.1f})" fill="{PAPER}" opacity=".72"/>'
            )

    layer_labels = []
    for text, y in (("top", 77.0), ("stone", 101.0), ("end", 137.0), ("rock", 161.0)):
        layer_labels.append(
            f'<line x1="269" y1="{y - 2:.1f}" x2="273" y2="{y - 2:.1f}" '
            f'stroke="{PAPER}" stroke-opacity=".18"/>'
        )
        layer_labels.append(label(256, y, text, 4.1, PAPER, .36))

    return art(f"""
  <rect x="22" y="44" width="220" height="142" rx="7" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
  <g shape-rendering="crispEdges">
    {''.join(cells)}
  </g>
  <g stroke="{PAPER}" stroke-opacity=".06" stroke-width=".5">
    {''.join(grid)}
  </g>
  <g stroke="{PAPER}" stroke-opacity=".24" stroke-width=".8">
    {''.join(contours)}
  </g>

  <rect x="{sx - 1.2:.1f}" y="{sy - 1.2:.1f}" width="{cell + 2.4:.1f}" height="{cell + 2.4:.1f}" fill="none" stroke="{PAPER}" stroke-width="1.3"/>
  <rect x="{sx - 2.8:.1f}" y="{sy - 2.8:.1f}" width="{cell + 5.6:.1f}" height="{cell + 5.6:.1f}" fill="none" stroke="{CORAL}" stroke-width=".9" opacity=".9"/>
  <circle cx="{scx:.1f}" cy="{scy:.1f}" r="1.5" fill="{PAPER}"/>
  <line x1="{sx + cell + 3:.1f}" y1="{scy:.1f}" x2="248" y2="{scy:.1f}" stroke="{CORAL}" stroke-opacity=".65" stroke-width="1.1" stroke-dasharray="2 3"/>
  <polygon points="251,{scy:.1f} 244,{scy - 3.2:.1f} 244,{scy + 3.2:.1f}" fill="{CORAL}" opacity=".85"/>

  <rect x="254" y="44" width="84" height="142" rx="7" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
  {''.join(blocks)}
  {''.join(layer_labels)}

  {label(296, 55, "core sample (8,8)", 5.4, CORAL, .95, 500, "middle")}
  {label(296, 63, "h 65 · 8 layers", 4.1, PAPER, .42, 400, "middle")}
  {label(292, 180, "4 andesite · 2 end · bedrock", 4.0, PAPER, .36, 400, "middle")}

  {label(30, 30, "worldgen · height field", 7.5, PAPER, .85, 500)}
  {label(30, 40, "fbm · 6 octaves · amplitude ×12", 5, PAPER, .38)}
  {label(28, 181, "26 × 15 samples · scale 0.085 · seed 4701234567", 4.3, PAPER, .4)}
""")


def art_minishell() -> str:
    return art(f"""
  <g>
    <rect x="24" y="24" width="312" height="155" rx="12" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".2"/>
    <path d="M24,36 a12,12 0 0 1 12,-12 h288 a12,12 0 0 1 12,12 v14 h-312 z" fill="{LIFT}"/>
    <circle cx="42" cy="41" r="3.4" fill="{CORAL}"/>
    <circle cx="54" cy="41" r="3.4" fill="{DEEP}"/>
    <circle cx="66" cy="41" r="3.4" fill="{PAPER}" opacity=".4"/>
    {label(82, 45, "minishell", 7.5, PAPER, 0.5)}
    <line x1="24" y1="54" x2="336" y2="54" stroke="{PAPER}" stroke-opacity=".1"/>
    {label(42, 82, "$", 15, CORAL, 1, 500)}
    {label(58, 82, "echo hi | cat | cat", 15, PAPER, 0.92)}
    {label(42, 108, "hi", 15, PAPER, 0.55)}
    {label(42, 136, "$", 15, CORAL, 1, 500)}
    {label(58, 136, "echo $?", 15, PAPER, 0.92)}
    {label(42, 162, "0", 15, PAPER, 0.55)}
    <rect x="60" y="149" width="9" height="17" fill="{CORAL}" opacity=".9"/>
    <line x1="330" y1="66" x2="330" y2="168" stroke="{CORAL}" stroke-opacity=".22"/>
  </g>
""")


def art_cub3d() -> str:
    stripes = []
    for i in range(9):
        t = i / 8
        x = 176 + 63 * t
        top = 34 + 53 * t
        bottom = 180 - 53 * t
        color = CORAL if i % 3 == 0 else (DEEP if i % 3 == 1 else PAPER)
        opacity = 0.4 if i % 3 != 2 else 0.16
        stripes.append(
            f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{bottom:.1f}" '
            f'stroke="{color}" stroke-opacity="{opacity}" stroke-width="2"/>'
        )
    for i in range(9):
        t = i / 8
        x = 342 - 63 * t
        top = 34 + 53 * t
        bottom = 180 - 53 * t
        color = CORAL if i % 3 == 0 else (DEEP if i % 3 == 1 else PAPER)
        opacity = 0.3 if i % 3 != 2 else 0.12
        stripes.append(
            f'<line x1="{x:.1f}" y1="{top:.1f}" x2="{x:.1f}" y2="{bottom:.1f}" '
            f'stroke="{color}" stroke-opacity="{opacity}" stroke-width="2"/>'
        )
    depth = []
    for t in (0.2, 0.4, 0.6, 0.8):
        depth.append(
            f'<line x1="{176 + 166 * t:.1f}" y1="180" x2="{239 + 40 * t:.1f}" y2="127"/>'
        )
        depth.append(
            f'<line x1="{176 + 166 * t:.1f}" y1="34" x2="{239 + 40 * t:.1f}" y2="87"/>'
        )
    stripes = "".join(stripes)
    depth = "".join(depth)
    return art(f"""
  <g>
    <rect x="18" y="34" width="150" height="146" rx="8" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".14"/>
    {label(26, 46, "MAP", 5, PAPER, 0.4)}
    <g stroke="{CORAL}" stroke-width="3" stroke-linecap="square">
      <line x1="30" y1="56" x2="156" y2="56"/>
      <line x1="30" y1="56" x2="30" y2="168"/>
      <line x1="30" y1="168" x2="156" y2="168"/>
      <line x1="156" y1="56" x2="156" y2="168"/>
      <line x1="66" y1="56" x2="66" y2="104"/>
      <line x1="66" y1="130" x2="66" y2="168"/>
      <line x1="96" y1="56" x2="96" y2="84"/>
      <line x1="96" y1="110" x2="96" y2="168"/>
      <line x1="126" y1="56" x2="126" y2="132"/>
      <line x1="30" y1="84" x2="66" y2="84"/>
      <line x1="96" y1="84" x2="126" y2="84"/>
      <line x1="66" y1="130" x2="96" y2="130"/>
      <line x1="126" y1="132" x2="156" y2="132"/>
      <line x1="30" y1="140" x2="66" y2="140"/>
    </g>
    <g stroke="{CORAL}" stroke-opacity=".3">
      <line x1="72" y1="146" x2="30" y2="112"/>
      <line x1="72" y1="146" x2="40" y2="56"/>
      <line x1="72" y1="146" x2="66" y2="104"/>
      <line x1="72" y1="146" x2="96" y2="110"/>
      <line x1="72" y1="146" x2="126" y2="132"/>
      <line x1="72" y1="146" x2="156" y2="144"/>
    </g>
    <circle cx="72" cy="146" r="4" fill="{CORAL}"/>
    <circle cx="72" cy="146" r="7" fill="none" stroke="{PAPER}" stroke-opacity=".45"/>
    {label(26, 176, "FOV 60°", 4.5, PAPER, 0.35)}
  </g>

  <g>
    <rect x="176" y="34" width="166" height="146" rx="8" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".25"/>
    <g>
      <polygon points="176,34 239,87 239,127 176,180" fill="{LIFT}"/>
      <polygon points="342,34 279,87 279,127 342,180" fill="{NAVY}"/>
      <polygon points="176,34 342,34 279,87 239,87" fill="{NAVY}"/>
      <polygon points="176,180 342,180 279,127 239,127" fill="{LIFT}"/>
      {stripes}
      <g stroke="{PAPER}" stroke-opacity=".1">{depth}</g>
      <rect x="239" y="87" width="40" height="40" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".55"/>
      <rect x="251" y="101" width="16" height="26" fill="none" stroke="{CORAL}" stroke-opacity=".75"/>
      <circle cx="259" cy="98" r="1.5" fill="{PAPER}" opacity=".5"/>
      <line x1="176" y1="180" x2="239" y2="127" stroke="{CORAL}" stroke-opacity=".55"/>
      <line x1="342" y1="180" x2="279" y2="127" stroke="{CORAL}" stroke-opacity=".45"/>
      <line x1="176" y1="34" x2="239" y2="87" stroke="{PAPER}" stroke-opacity=".25"/>
      <line x1="342" y1="34" x2="279" y2="87" stroke="{PAPER}" stroke-opacity=".18"/>
    </g>
    <rect x="176" y="34" width="166" height="15" fill="{NAVY}" opacity=".75"/>
    {label(184, 44, "cub3D", 5.5, CORAL, 0.95, 500)}
    {label(210, 44, "courtyard.cub", 5, PAPER, 0.45)}
    <g stroke="{PAPER}" stroke-opacity=".7">
      <line x1="255" y1="107" x2="263" y2="107"/>
      <line x1="259" y1="103" x2="259" y2="111"/>
    </g>
    {label(184, 172, "640 RAYS", 4.5, PAPER, 0.4)}
    {label(320, 172, "~60", 4.5, CORAL, 0.6, 500, "end")}
  </g>
""")


def art_irc() -> str:
    return art(f"""
  <g>
    <rect x="28" y="34" width="74" height="58" rx="9" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
    <path d="M28,43 a9,9 0 0 1 9,-9 h56 a9,9 0 0 1 9,9 v9 h-74 z" fill="{NAVY}"/>
    <circle cx="41" cy="43" r="2.6" fill="{CORAL}"/>
    {label(52, 47, "alice", 7.5, PAPER, 0.82, 500)}
    {label(38, 70, "#ai-lab", 8, CORAL, 0.9, 500)}
    <rect x="38" y="77" width="48" height="3" rx="1.5" fill="{PAPER}" opacity=".18"/>
  </g>

  <line x1="102" y1="63" x2="244" y2="63" stroke="{PAPER}" stroke-opacity=".18" stroke-width="3"/>
  <g>
    <rect x="118" y="55" width="16" height="10" rx="2.5" fill="{CORAL}"/>
    <rect x="156" y="55" width="16" height="10" rx="2.5" fill="{PAPER}" opacity=".5"/>
    <rect x="194" y="55" width="16" height="10" rx="2.5" fill="{DEEP}"/>
  </g>
  <path d="M212,63 l6,-4 v8 z" fill="{CORAL}" opacity=".8"/>

  <g>
    <rect x="244" y="30" width="92" height="72" rx="10" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".65"/>
    <circle cx="324" cy="42" r="3" fill="{CORAL}"/>
    {label(256, 45, "IRC SERVER", 6.5, PAPER, 0.4, 500)}
    {label(290, 76, "poll()", 18, CORAL, 0.95, 500, "middle")}
    {label(290, 92, "1 thread · 1 loop", 6.5, PAPER, 0.45, 400, "middle")}
  </g>

  <g>
    <rect x="28" y="112" width="308" height="62" rx="9" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    <rect x="40" y="122" width="26" height="11" rx="2.5" fill="{CORAL}"/>
    {label(53, 130.5, "TCP", 5.5, NAVY, 1, 500, "middle")}
    {label(74, 130.5, "6667 · alice → server", 7, PAPER, 0.5)}

    <rect x="40" y="140" width="26" height="11" rx="2.5" fill="{PAPER}"/>
    {label(53, 148.5, "IRC", 5.5, NAVY, 1, 500, "middle")}
    {label(74, 148.5, "PRIVMSG #ai-lab :hello", 11, PAPER, 0.92, 500)}

    <rect x="40" y="158" width="26" height="11" rx="2.5" fill="{DEEP}"/>
    {label(53, 166.5, "BOT", 5.5, NAVY, 1, 500, "middle")}
    {label(74, 166.5, "Phi-3 · 3.8B · llama.cpp", 7.5, PAPER, 0.55)}
  </g>
""")


def box3d(x, y, w, h, dx=9, dy=-9, front=LIFT, top=NAVY, side=NAVY, stroke=PAPER, stroke_opacity=0.18):
    return f"""
  <polygon points="{x},{y} {x + dx},{y + dy} {x + w + dx},{y + dy} {x + w},{y}" fill="{top}" stroke="{stroke}" stroke-opacity=".1"/>
  <polygon points="{x + w},{y} {x + w + dx},{y + dy} {x + w + dx},{y + h + dy} {x + w},{y + h}" fill="{side}" stroke="{stroke}" stroke-opacity=".08"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{front}" stroke="{stroke}" stroke-opacity="{stroke_opacity}"/>
"""


def art_inception() -> str:
    return art(f"""
  <rect x="54" y="22" width="278" height="166" rx="12" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".2"/>
  <path d="M54,34 a12,12 0 0 1 12,-12 h254 a12,12 0 0 1 12,12 v10 h-278 z" fill="{LIFT}"/>
  {label(68, 38, "docker host", 7.5, PAPER, .6, 500)}
  {label(252, 38, "compose · 3 services", 5.5, PAPER, .35, 400, "end")}

  <rect x="62" y="52" width="262" height="98" rx="8" fill="{CORAL}" opacity=".04" stroke="{CORAL}" stroke-opacity=".3" stroke-dasharray="4 5"/>
  {label(70, 61, "bridge network · internal", 4.8, PAPER, .32)}

  <g>
    <circle cx="28" cy="114" r="9" fill="none" stroke="{PAPER}" stroke-opacity=".4"/>
    <ellipse cx="28" cy="114" rx="4" ry="9" fill="none" stroke="{PAPER}" stroke-opacity=".28"/>
    <line x1="19" y1="114" x2="37" y2="114" stroke="{PAPER}" stroke-opacity=".22"/>
    <line x1="37" y1="114" x2="66" y2="114" stroke="{CORAL}" stroke-width="2.6"/>
    <polygon points="68,114 59,109 59,119" fill="{CORAL}"/>
    {label(47, 106, "443", 6, CORAL, .95, 500, "middle")}
  </g>

  {box3d(68, 88, 70, 58, front=CORAL, top=DEEP, side=DEEP, stroke=NAVY, stroke_opacity=.16)}
  <line x1="73" y1="84" x2="142" y2="84" stroke="{PAPER}" stroke-opacity=".18"/>
  <line x1="75" y1="81.5" x2="144" y2="81.5" stroke="{PAPER}" stroke-opacity=".12"/>
  <g transform="translate(76,96)">
    <rect y="4" width="11" height="8" rx="1.5" fill="{NAVY}"/>
    <path d="M2.2,4 v-2.2 a3.3,3.3 0 0 1 6.6,0 v2.2" fill="none" stroke="{NAVY}" stroke-width="1.5"/>
  </g>
  {label(92, 105, "nginx", 9.5, NAVY, 1, 500)}
  {label(76, 120, "TLS 1.3", 5.5, NAVY, .7, 500)}
  {label(76, 129, "static + fastcgi", 4.8, NAVY, .55)}
  <circle cx="132" cy="93" r="1.6" fill="{NAVY}" opacity=".55"/>

  {box3d(154, 74, 82, 66, front=LIFT, top=NAVY, side=NAVY)}
  <line x1="160" y1="70" x2="238" y2="70" stroke="{PAPER}" stroke-opacity=".1"/>
  <line x1="162" y1="67.5" x2="240" y2="67.5" stroke="{PAPER}" stroke-opacity=".07"/>
  <circle cx="166" cy="91" r="7.5" fill="{PAPER}" opacity=".14"/>
  {label(166, 94, "W", 7.5, PAPER, .9, 500, "middle")}
  {label(179, 95, "wordpress", 8.5, PAPER, .95, 500)}
  {label(164, 114, "php-fpm", 5.5, PAPER, .5)}
  {label(164, 123, "wp-cli", 4.8, PAPER, .4)}
  <rect x="198" y="126" width="30" height="11" rx="5.5" fill="{PAPER}" opacity=".08" stroke="{PAPER}" stroke-opacity=".2"/>
  {label(213, 133.5, "9000", 5, PAPER, .6, 500, "middle")}
  <circle cx="229" cy="79" r="1.6" fill="{CORAL}" opacity=".8"/>

  {box3d(250, 88, 72, 58, front=LIFT, top=NAVY, side=NAVY)}
  <g transform="translate(260,96)">
    <ellipse cx="7" cy="3" rx="7" ry="2.6" fill="{PAPER}" opacity=".26"/>
    <path d="M0,3 v10 c0,1.4 3.1,2.6 7,2.6 s7,-1.2 7,-2.6 v-10" fill="none" stroke="{PAPER}" stroke-opacity=".34"/>
    <path d="M0,8 c0,1.4 3.1,2.6 7,2.6 s7,-1.2 7,-2.6" fill="none" stroke="{PAPER}" stroke-opacity=".2"/>
  </g>
  {label(280, 104, "mariadb", 8, PAPER, .95, 500)}
  {label(260, 124, "3306", 6, CORAL, .75, 500)}
  {label(260, 133, "internal only", 4.5, PAPER, .4)}
  <circle cx="314" cy="93" r="1.6" fill="{PAPER}" opacity=".4"/>

  <g stroke="{CORAL}" stroke-width="1.8" fill="none">
    <line x1="138" y1="116" x2="154" y2="116"/>
    <line x1="236" y1="112" x2="250" y2="112"/>
  </g>
  <g fill="{CORAL}">
    <polygon points="154,116 146,112 146,120"/>
    <polygon points="250,112 242,108 242,116"/>
  </g>

  <line x1="64" y1="154" x2="322" y2="154" stroke="{PAPER}" stroke-opacity=".12"/>

  <g>
    <rect x="64" y="158" width="80" height="18" rx="9" fill="{PAPER}" opacity=".05" stroke="{PAPER}" stroke-opacity=".12"/>
    <g fill="{PAPER}" fill-opacity=".12" stroke="{CORAL}" stroke-opacity=".55">
      <rect x="70" y="161" width="6" height="10" rx="1.5"/>
      <rect x="78" y="161" width="6" height="10" rx="1.5"/>
      <rect x="86" y="161" width="6" height="10" rx="1.5"/>
      <rect x="94" y="161" width="6" height="10" rx="1.5"/>
    </g>
    {label(106, 171, "4 secrets", 5.5, PAPER, .6, 500)}
  </g>

  <g>
    <rect x="152" y="158" width="84" height="18" rx="9" fill="{PAPER}" opacity=".05" stroke="{PAPER}" stroke-opacity=".12"/>
    <g transform="translate(160,162)">
      <ellipse cx="5" cy="2" rx="5" ry="1.8" fill="none" stroke="{PAPER}" stroke-opacity=".4"/>
      <path d="M0,2 v9 c0,1 2.2,1.8 5,1.8 s5,-0.8 5,-1.8 v-9" fill="none" stroke="{PAPER}" stroke-opacity=".4"/>
    </g>
    <g transform="translate(172,162)">
      <ellipse cx="5" cy="2" rx="5" ry="1.8" fill="none" stroke="{PAPER}" stroke-opacity=".28"/>
      <path d="M0,2 v9 c0,1 2.2,1.8 5,1.8 s5,-0.8 5,-1.8 v-9" fill="none" stroke="{PAPER}" stroke-opacity=".28"/>
    </g>
    {label(186, 171, "2 volumes", 5.5, PAPER, .6, 500)}
  </g>

  <g>
    <rect x="244" y="158" width="78" height="18" rx="9" fill="{PAPER}" opacity=".05" stroke="{PAPER}" stroke-opacity=".12"/>
    <rect x="252" y="162" width="9" height="11" rx="1.5" fill="none" stroke="{CORAL}" stroke-opacity=".7"/>
    <line x1="254" y1="165" x2="259" y2="165" stroke="{CORAL}" stroke-opacity=".55"/>
    <line x1="254" y1="168" x2="259" y2="168" stroke="{CORAL}" stroke-opacity=".55"/>
    {label(266, 171, "setup.sh", 5.5, CORAL, .85, 500)}
  </g>
""")


def art_born2beroot() -> str:
    """A guest VM window on a hypervisor host: one disk, one open port."""
    bricks = []
    row = 0
    y = 58.0
    while y < 142.0:
        offset = 0.0 if row % 2 == 0 else -7.5
        x = 252.0 + offset
        while x < 284.0:
            if x >= 251.5:
                bricks.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="14" height="6.2" rx="1" '
                    f'fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".10"/>'
                )
            x += 15.0
        y += 8.0
        row += 1
    bricks = "".join(bricks)

    slots = []
    for i in range(7):
        x = 126 + i * 15
        slots.append(
            f'<rect x="{x}" y="110" width="12" height="18" rx="2" '
            f'fill="{PAPER}" fill-opacity=".06" stroke="{PAPER}" stroke-opacity=".22"/>'
        )
        slots.append(
            f'<rect x="{x + 3}" y="114" width="6" height="1.6" rx=".8" fill="{CORAL}" opacity=".55"/>'
        )
        slots.append(
            f'<rect x="{x + 3}" y="118" width="4" height="1.6" rx=".8" fill="{PAPER}" opacity=".22"/>'
        )
        slots.append(
            f'<circle cx="{x + 6}" cy="124" r="1.1" fill="{CORAL}" opacity="{0.9 if i in (0, 5) else 0.25}"/>'
        )
    slots = "".join(slots)

    return art(f"""
  <defs><clipPath id="b2br-wall"><rect x="252" y="56" width="32" height="86" rx="3"/></clipPath></defs>

  <rect x="24" y="148" width="312" height="38" rx="8" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
  <path d="M24,156 a8,8 0 0 1 8,-8 h296 a8,8 0 0 1 8,8" fill="none" stroke="{CORAL}" stroke-opacity=".28"/>
  <rect x="56" y="186" width="34" height="3" rx="1.5" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".12"/>
  <rect x="270" y="186" width="34" height="3" rx="1.5" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".12"/>
  {label(38, 166, "host machine", 6.4, PAPER, .72, 500)}
  {label(38, 175, "hypervisor", 4.4, PAPER, .35)}
  {label(322, 166, "virtualbox", 4.6, CORAL, .6, 500, "end")}
  {label(322, 175, "guest disk · 30 gb", 4.2, PAPER, .3, 400, "end")}

  <rect x="47" y="21" width="272" height="132" rx="9" fill="{NAVY}" opacity=".45"/>
  <rect x="44" y="18" width="272" height="132" rx="9" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".3"/>
  <path d="M44,27 a9,9 0 0 1 9,-9 h254 a9,9 0 0 1 9,9 v9 h-272 z" fill="{LIFT}"/>
  <line x1="44" y1="36" x2="316" y2="36" stroke="{PAPER}" stroke-opacity=".14"/>
  <circle cx="56" cy="27" r="2.6" fill="{CORAL}"/>
  <circle cx="64" cy="27" r="2.6" fill="{DEEP}"/>
  <circle cx="72" cy="27" r="2.6" fill="{PAPER}" opacity=".4"/>
  {label(84, 30.5, "born2beroot", 6.4, PAPER, .9, 500)}
  {label(288, 30.5, "debian 12", 4.4, PAPER, .42, 400, "end")}
  <rect x="294" y="22" width="18" height="11" rx="5.5" fill="{CORAL}"/>
  {label(303, 30, "VM", 4.8, NAVY, 1, 500, "middle")}

  <rect x="52" y="46" width="60" height="36" rx="4" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".38" stroke-dasharray="3 3"/>
  {label(58, 61, "/boot", 6.2, PAPER, .9, 500)}
  {label(58, 70, "outside luks", 3.9, PAPER, .4)}
  {label(58, 77, "unencrypted", 3.9, CORAL, .55)}
  <g transform="translate(97,55)" fill="none" stroke="{PAPER}" stroke-opacity=".45">
    <rect x="0" y="2" width="11" height="10" rx="1.5"/>
    <circle cx="3.6" cy="7" r="2"/>
    <line x1="8" y1="5" x2="8" y2="9"/>
  </g>

  <rect x="118" y="40" width="120" height="106" rx="7" fill="{CORAL}" fill-opacity=".03" stroke="{CORAL}" stroke-opacity=".22" stroke-dasharray="3 4"/>
  {label(124, 47, "luks", 3.8, CORAL, .5)}

  <path d="M164,68 v-9 a16,16 0 0 1 32,0 v9" fill="none" stroke="{CORAL}" stroke-width="4.6" stroke-linecap="round"/>
  <rect x="156" y="68" width="48" height="32" rx="6" fill="{CORAL}" stroke="{DEEP}" stroke-opacity=".45"/>
  <circle cx="180" cy="80" r="3.4" fill="{NAVY}"/>
  <rect x="178" y="80" width="4" height="9" rx="2" fill="{NAVY}"/>
  {label(180, 94, "LUKS", 5.4, NAVY, .95, 500, "middle")}

  {slots}
  {label(180, 141, "7 volumes · lvm", 4.1, PAPER, .42, 400, "middle")}

  <rect x="252" y="56" width="32" height="86" rx="3" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".22"/>
  <g clip-path="url(#b2br-wall)">{bricks}</g>
  {label(268, 45, "ufw", 6, CORAL, .95, 500, "middle")}
  {label(268, 53, "default deny", 3.8, PAPER, .4, 400, "middle")}
  <g stroke="{CORAL}" stroke-opacity=".55" stroke-width="1.2">
    <line x1="264" y1="68" x2="272" y2="76"/>
    <line x1="272" y1="68" x2="264" y2="76"/>
    <line x1="264" y1="124" x2="272" y2="132"/>
    <line x1="272" y1="124" x2="264" y2="132"/>
  </g>

  <circle cx="268" cy="100" r="4.4" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".7" stroke-width="1.1"/>
  <line x1="230" y1="100" x2="294" y2="100" stroke="{CORAL}" stroke-width="2.2"/>
  <rect x="294" y="92" width="14" height="16" rx="2.4" fill="{CORAL}" stroke="{DEEP}" stroke-opacity=".55"/>
  <rect x="294" y="96" width="4" height="8" rx="1" fill="{NAVY}" opacity=".5"/>
  {label(301, 119, "4242", 5.2, CORAL, .95, 500, "middle")}
  {label(301, 126, "ssh only", 3.8, PAPER, .4, 400, "middle")}

  <rect x="52" y="92" width="60" height="46" rx="5" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
  <path d="M52,97 a5,5 0 0 1 5,-5 h50 a5,5 0 0 1 5,5 v5 h-60 z" fill="{LIFT}"/>
  <circle cx="59" cy="97" r="1.3" fill="{CORAL}"/>
  {label(65, 100, "wall", 4.8, CORAL, .9, 500)}
  {label(106, 100, "600s", 3.8, PAPER, .4, 400, "end")}
  <path d="M58,113 h5 l2,-6 l3,11 l3,-9 l2,4 h6 l2,-2 l3,2 h5 l2,-3 l3,3 h7"
        fill="none" stroke="{CORAL}" stroke-opacity=".7" stroke-width="1.3"/>
  {label(58, 132, "every 600s", 3.8, PAPER, .32)}
""")


def art_forge() -> str:
    """A workbench anvil with a glowing blank and a hammer caught mid-swing."""
    sparks = []
    for x1, y1, x2, y2, opacity in (
        (166, 74, 146, 54, 0.9),
        (172, 72, 180, 48, 0.7),
        (178, 76, 198, 60, 0.55),
        (160, 78, 138, 72, 0.5),
        (184, 80, 206, 84, 0.45),
    ):
        sparks.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{CORAL}" stroke-opacity="{opacity}" stroke-width="1.4" '
            'stroke-linecap="round"/>'
        )
    sparks = "".join(sparks)

    return art(f"""
  <ellipse cx="176" cy="78" rx="78" ry="34" fill="{CORAL}" opacity=".12"/>

  <g>
    <rect x="36" y="154" width="288" height="13" rx="4" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".18"/>
    <rect x="54" y="167" width="12" height="22" rx="2" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".1"/>
    <rect x="294" y="167" width="12" height="22" rx="2" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".1"/>
    <line x1="48" y1="158" x2="312" y2="158" stroke="{PAPER}" stroke-opacity=".08"/>
  </g>

  <g>
    <path d="M96,88 l-26,10 l26,10 z" fill="{DEEP}"/>
    <rect x="92" y="84" width="118" height="15" rx="5" fill="{CORAL}"/>
    <path d="M116,99 h70 v10 l16,33 h-102 l16,-33 z" fill="{CORAL}"/>
    <path d="M186,99 h0 v10 l16,33 h-16 z" fill="{DEEP}" opacity=".55"/>
    <rect x="84" y="142" width="134" height="13" rx="5" fill="{CORAL}"/>
    <rect x="84" y="142" width="134" height="4" rx="2" fill="{PAPER}" opacity=".18"/>
  </g>

  <g>
    <rect x="124" y="76" width="54" height="9" rx="3" fill="{PAPER}" opacity=".92"/>
    <rect x="124" y="76" width="54" height="3" rx="1.5" fill="#ffffff" opacity=".55"/>
    <ellipse cx="151" cy="80" rx="34" ry="8" fill="{CORAL}" opacity=".22"/>
  </g>

  <g transform="rotate(-34 208 58)">
    <rect x="198" y="50" width="38" height="16" rx="4" fill="{CORAL}" stroke="{DEEP}" stroke-opacity=".6"/>
    <rect x="228" y="53" width="62" height="9" rx="4.5" fill="{PAPER}" opacity=".8"/>
    <rect x="282" y="51" width="10" height="13" rx="3" fill="{DEEP}"/>
  </g>

  <path d="M202,40 a26,26 0 0 1 18,-14" fill="none" stroke="{CORAL}" stroke-opacity=".32" stroke-width="1.4"/>
  <path d="M214,34 a18,18 0 0 1 13,-8" fill="none" stroke="{PAPER}" stroke-opacity=".2" stroke-width="1.2"/>
  {sparks}

  <g fill="none" stroke="{CORAL}" stroke-opacity=".55" stroke-width="1.2">
    <path d="M58,58 h20 v20 h-20 z"/>
    <path d="M62,58 v-8 M74,58 v-8"/>
    <path d="M58,94 h20 v20 h-20 z"/>
    <path d="M68,94 v20"/>
  </g>
  <g fill="{CORAL}" opacity=".45">
    <rect x="304" y="54" width="6" height="6" rx="1"/>
    <rect x="316" y="54" width="6" height="6" rx="1"/>
    <rect x="304" y="66" width="6" height="6" rx="1"/>
    <rect x="316" y="66" width="6" height="6" rx="1"/>
  </g>
""")


PROJECTS = [
    {
        "n": "01",
        "file": "plate-01.png",
        # Clip the empty navy below the card so the try-it strip can sit close
        # to it. The card itself is unchanged.
        "clip_h": 376,
        "title": "dynamic-dashboard",
        "meta": "2026 · Solo · product &amp; full stack",
        "hook": "A local-first dashboard builder — tabs of isolated HTML widgets on one SQLite database, edited by an agent in place.",
        "stack": "Bun · Hono · SQLite · Vanilla JS · OpenCode",
        "href": "https://github.com/edouwarden/dynamic-dashboard",
        "art": DASHBOARD_ART,
        "alt": (
            "01 dynamic-dashboard, 2026, solo product and full stack: a local-first "
            "dashboard builder with isolated HTML widgets on one SQLite database, "
            "edited by an agent; Bun, Hono, SQLite, Vanilla JS, OpenCode. Opens "
            "the repository."
        ),
    },
    {
        "n": "02",
        "file": "plate-02.png",
        "title": "ft_transcendence",
        "meta": "2026 · Team lead · engine &amp; frontend",
        "hook": "A four-person browser game engine on Three.js: World → Environment → Module, physics and live editors.",
        "stack": "Next.js · Three.js · Rapier · Bun · Go · PostgreSQL",
        "href": "https://github.com/edouwarden/Transcendence-WebGameEngine",
        "art": art_transcendence(),
        "alt": (
            "02 ft_transcendence, 2026, team lead for engine and frontend on a team "
            "of four: a browser game engine on Three.js with World, Environment and "
            "Module layers, physics, editors and live tools, running a parkour "
            "arena; Next.js, Three.js, Rapier, Bun, Go, PostgreSQL. Opens the "
            "repository."
        ),
    },
    {
        "n": "03",
        "file": "plate-03.png",
        "title": "space-gameserver",
        "meta": "2019 · Solo · systems &amp; geometry",
        "hook": "A 2019 Spigot sandbox: custom space and exoplanet dimensions, ships on an 11 × 11 orbital grid, five weapon systems as closed-form geometry.",
        "stack": "Java 8 · Paper 1.14.4 · WorldEdit · WorldGuard · Python",
        "href": "https://github.com/edouwarden/space-gameserver-2019-psr",
        "art": art_space(),
        "alt": (
            "03 space-gameserver, 2019, solo, systems and geometry: a Spigot "
            "sandbox whose space and exoplanet terrain comes from a seeded six-"
            "octave height field sampled into a core column, ships on an 11 by "
            "11 orbital grid, and five weapon systems as closed-form geometry; "
            "Java 8, Paper 1.14.4, WorldEdit, WorldGuard, Python. Opens the "
            "repository."
        ),
    },
    {
        "n": "04",
        "file": "plate-04.png",
        "title": "minishell",
        "meta": "2025 · Pair · systems &amp; parsing",
        "hook": "A Unix shell from the syscall up: quote-aware lexing, expansion, heredocs and 64-stage pipelines.",
        "stack": "C99 · POSIX · fork/exec · dup2 · readline",
        "href": "https://github.com/edouwarden/minishell",
        "art": art_minishell(),
        "alt": (
            "04 minishell, 2025, pair, systems and parsing: a Unix shell with "
            "quote-aware lexing, expansion, heredocs and 64-stage pipelines, "
            "readline only; C99, POSIX, fork and exec, dup2, readline. Opens the "
            "repository."
        ),
    },
    {
        "n": "05",
        "file": "plate-05.png",
        "title": "cub3D",
        "meta": "2025 · Pair · rendering &amp; math",
        "hook": "A raycast renderer written by hand: 640 rays per frame, textured walls floor to ceiling, every pixel into an X11 buffer — no GPU.",
        "stack": "C99 · X11 · raycasting · XPM · math",
        "href": "https://github.com/edouwarden/cube3D",
        "art": art_cub3d(),
        "alt": (
            "05 cub3D, 2025, pair, rendering and math: a hand-written raycast "
            "renderer with 640 rays per frame, textured walls floor to ceiling and "
            "every pixel written into an X11 buffer without a GPU; C99, X11, "
            "raycasting, XPM, math. Opens the repository."
        ),
    },
    {
        "n": "06",
        "file": "plate-06.png",
        "title": "ft_irc",
        "meta": "2026 · Pair · protocols &amp; systems",
        "hook": "An IRC server on one thread and one poll() loop: buffered TCP framing, channel modes, and a local Phi-3 answering in #ai-lab.",
        "stack": "C++98 · sockets · poll() · llama.cpp",
        "href": "https://github.com/edouwarden/irc",
        "art": art_irc(),
        "alt": (
            "06 ft_irc, 2026, pair, protocols and systems: an IRC server on one "
            "thread and one poll loop with buffered TCP framing, channel modes and "
            "a local Phi-3 answering in #ai-lab; C++98, sockets, poll, llama.cpp. "
            "Opens the repository."
        ),
    },
    {
        "n": "07",
        "file": "plate-07.png",
        "title": "Inception",
        "meta": "2026 · Solo · containers &amp; infra",
        "hook": "A WordPress stack where every part is a container: nginx holds TLS, MariaDB never leaves the compose network.",
        "stack": "Docker Compose · NGINX · WordPress · MariaDB · TLS",
        "href": "https://github.com/edouwarden/inception",
        "art": art_inception(),
        "alt": (
            "07 Inception, 2026, solo, containers and infrastructure: a WordPress "
            "stack where every part is a container, nginx holds TLS, PHP-FPM runs "
            "WordPress and MariaDB never leaves the compose network; Docker "
            "Compose, NGINX, WordPress, MariaDB, TLS. Opens the repository."
        ),
    },
    {
        "n": "08",
        "file": "plate-08.png",
        "title": "born2beroot",
        "meta": "2024 · Solo · systems &amp; hardening",
        "hook": "A reproducible Debian VM from a self-made ISO: LUKS under LVM, six filesystems, SSH on 4242, and every sudo logged.",
        "stack": "Debian · LUKS · LVM · UFW · systemd",
        "href": "https://github.com/edouwarden/born2beroot",
        "art": art_born2beroot(),
        "alt": (
            "08 born2beroot, 2024, solo, systems and hardening: a reproducible "
            "Debian VM running in a guest window on a VirtualBox host, built from "
            "a self-made ISO with LUKS under LVM, six filesystems, SSH on port "
            "4242 and every sudo logged; Debian, LUKS, LVM, UFW, systemd. Opens "
            "the repository."
        ),
    },
    # Placeholder framing for Forge. Replace the copy and stack once the
    # repository has a public shape; it is already published under this URL.
    {
        "n": "09",
        "file": "plate-09.png",
        "variant": "outline",
        "motion": "forge",
        "title": "Forge",
        "meta": "2026 · Solo · systems &amp; tooling",
        "hook": "The next systems project: a workshop for building, running and keeping software on one machine — published in parts.",
        "stack": "Bun · TypeScript · SQLite · Docker · Linux",
        "href": "https://github.com/edouwarden/theforge",
        "art": art_forge(),
        "alt": (
            "09 Forge, 2026, solo, systems and tooling, in progress: a workshop "
            "for building, running and keeping software on one machine, "
            "published in parts; Bun, TypeScript, SQLite, Docker, Linux. "
            "Opens the repository."
        ),
    },
]

CARD = """
<div class="plate">
  <div class="card {variant}">
    <div class="copy">
      <div class="head">
        <div class="num">{n}</div>
        <h2 class="title">{title}</h2>
      </div>
      <p class="meta">{meta}</p>
      <p class="hook">{hook}</p>
      <p class="stack">{stack}</p>
    </div>
    <div class="art">{art}<span class="go">↗</span></div>
  </div>
</div>
"""

STYLE = f"""
@font-face {{
  font-family: 'Days One';
  src: url('file://{FONTS}/days-one-v1.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Plex Mono';
  src: url('file://{FONTS}/ibm-plex-mono-400-v1.woff2') format('woff2');
}}
@font-face {{
  font-family: 'Plex Mono';
  src: url('file://{FONTS}/ibm-plex-mono-500-v1.woff2') format('woff2');
  font-weight: 500;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  width: 1200px;
  font-family: 'Plex Mono', monospace;
  -webkit-font-smoothing: antialiased;
}}
.plate {{ width: 1200px; height: 400px; padding: 34px 84px; background: {NAVY}; }}
.card {{
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: 36px;
  height: 100%;
  padding: 30px 36px;
  border-radius: 30px;
  background: {CORAL};
  color: {NAVY};
  overflow: hidden;
}}
.copy {{ display: flex; flex-direction: column; min-width: 0; }}
.head {{ display: flex; align-items: center; gap: 18px; }}
.num {{
  display: grid; place-items: center; flex: none;
  width: 54px; height: 54px; border-radius: 10px;
  background: #ffffff; font-family: 'Days One', sans-serif; font-size: 21px;
}}
.title {{
  margin: 0; font-family: 'Days One', sans-serif; font-size: 42px;
  font-weight: 400; line-height: 1; letter-spacing: -0.02em;
}}
.meta {{
  margin: 14px 0 0; font-size: 10.5px; font-weight: 500;
  letter-spacing: 0.14em; text-transform: uppercase; color: rgba(12, 10, 62, 0.62);
}}
.hook {{
  max-width: 510px; margin: 16px 0 0; font-size: 19px;
  line-height: 1.55; color: rgba(12, 10, 62, 0.88);
}}
.stack {{
  margin: auto 0 0; padding-top: 18px; font-size: 9.5px; font-weight: 500;
  letter-spacing: 0.1em; text-transform: uppercase; color: rgba(12, 10, 62, 0.5);
}}
.art {{ position: relative; align-self: center; width: 420px; height: 237px; }}
.art svg {{
  display: block; width: 420px; height: 237px; border-radius: 18px;
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(12, 10, 62, 0.35);
}}
.art .go {{
  position: absolute; right: -13px; bottom: -13px;
  display: grid; place-items: center; width: 46px; height: 46px;
  border-radius: 50%; background: #ffffff;
  font-family: 'Days One', sans-serif; font-size: 19px;
}}

/* In-progress card: the same anatomy, drawn as an outline on the deck. */
.card.outline {{
  background: transparent;
  color: {PAPER};
  border: 1.5px solid {CORAL};
}}
.card.outline .num {{
  background: transparent;
  color: {CORAL};
  border: 1.5px solid {CORAL};
}}
.card.outline .meta {{ color: rgba(255, 250, 240, 0.54); }}
.card.outline .hook {{ color: rgba(255, 250, 240, 0.84); }}
.card.outline .stack {{ color: rgba(255, 250, 240, 0.42); }}
.card.outline .art .go {{
  background: transparent;
  color: {CORAL};
  box-shadow: inset 0 0 0 1.5px {CORAL};
}}
"""


def card(project: dict) -> str:
    return CARD.format(
        variant=project.get("variant", ""),
        n=project["n"],
        title=project["title"],
        meta=project["meta"],
        hook=project["hook"],
        stack=project["stack"],
        art=project["art"],
    )


def document(project: dict) -> str:
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><style>"
        + STYLE
        + "</style></head><body>"
        + card(project)
        + "</body></html>"
    )


def forge_overlay(x: float, y: float) -> str:
    """A slow ember pulse over the anvil, drawn on the wrapped plate."""
    sparks = (
        (166, 74, 146, 54, 0.9),
        (172, 72, 180, 48, 0.7),
        (178, 76, 198, 60, 0.55),
        (160, 78, 138, 72, 0.5),
        (184, 80, 206, 84, 0.45),
    )
    lines = []
    for index, (x1, y1, x2, y2, opacity) in enumerate(sparks):
        lines.append(
            f'<line x1="{x + x1}" y1="{y + y1}" x2="{x + x2}" y2="{y + y2}" '
            f'stroke="{CORAL}" stroke-width="1.4" stroke-linecap="round" opacity="0">'
            f'<animate attributeName="opacity" values="0;{opacity};0" '
            f'dur="3.6s" begin="{index * 0.45:.2f}s" repeatCount="indefinite"/>'
            "</line>"
        )

    return (
        f'<circle cx="{x + 176}" cy="{y + 78}" r="16" fill="none" '
        f'stroke="{CORAL}" opacity="0">'
        '<animate attributeName="r" values="16;42;16" dur="3.6s" '
        'repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;0.18;0" dur="3.6s" '
        'repeatCount="indefinite"/>'
        "</circle>"
        f'<circle cx="{x + 166}" cy="{y + 74}" r="2.4" fill="{CORAL}">'
        '<animate attributeName="opacity" values="0.25;1;0.25" dur="2.8s" '
        'repeatCount="indefinite"/>'
        "</circle>" + "".join(lines)
    )


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 400},
            device_scale_factor=2,
        )
        for project in PROJECTS:
            page_path = BUILD / Path(project["file"]).with_suffix(".html")
            page_path.write_text(document(project))
            page.goto(page_path.as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            clip_h = project.get("clip_h", 400)
            page.screenshot(
                path=str(HERE / project["file"]),
                clip={"x": 0, "y": 0, "width": 1200, "height": clip_h},
            )
            print(f"rendered {project['file']}")
            if project.get("motion") == "forge":
                box = page.evaluate(
                    """() => {
                        const r = document.querySelector('.art svg').getBoundingClientRect();
                        return {x: r.x, y: r.y};
                    }"""
                )
                overlay = (
                    '<g transform="scale(2)">'
                    + forge_overlay(box["x"], box["y"])
                    + "</g>"
                )
                write_image_svg(
                    HERE / project["file"],
                    HERE / Path(project["file"]).with_suffix(".svg"),
                    2400,
                    800,
                    overlay,
                    "Forge — in progress",
                )
                print("wrote plate-09.svg")
        browser.close()


if __name__ == "__main__":
    main()
