#!/usr/bin/env python3
"""Render the selected proof plate — a custom flat illustration — for every
project in the deck.

Each card keeps the same anatomy: number, title, meta, hook, three project
stats, stack, and a 360 x 203 illustration drawn inline as SVG in the ambient
palette. The illustrations are deliberately different diagrams, not screenshots:
a dashboard shell, a game-engine world, an orbital chart, a shell pipeline, a
raycast view, a poll loop, a container network, and a disk stack.

Standalone: production README and build.py are untouched.

    python3 assets/readme/prototype/plates.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

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
    strata = []
    for t in (0.22, 0.46, 0.7):
        strata.append(f'<line x1="{86 - 0:.1f}" y1="{64 + 58 * t:.1f}" x2="190" y2="{96 + 58 * t:.1f}"/>')
        strata.append(f'<line x1="294" y1="{64 + 58 * t:.1f}" x2="190" y2="{96 + 58 * t:.1f}"/>')
    strata = "".join(strata)
    return art(f"""
  <defs>
    <clipPath id="topface"><polygon points="86,64 190,32 294,64 190,96"/></clipPath>
  </defs>

  <g stroke="{PAPER}" stroke-opacity=".05">
    <line x1="40" y1="40" x2="320" y2="40"/>
    <line x1="40" y1="80" x2="320" y2="80"/>
    <line x1="40" y1="120" x2="320" y2="120"/>
    <line x1="80" y1="24" x2="80" y2="176"/>
    <line x1="160" y1="24" x2="160" y2="176"/>
    <line x1="240" y1="24" x2="240" y2="176"/>
    <line x1="320" y1="24" x2="320" y2="176"/>
  </g>

  <g stroke="{CORAL}" stroke-opacity=".4" stroke-dasharray="4 5" fill="{LIFT}" fill-opacity=".25">
    <polygon points="30,50 60,38 90,50 60,62"/>
    <path d="M30,50 v14 M60,62 v14 M90,50 v14" fill="none"/>
  </g>
  {label(60, 76, "next chunk", 6.5, CORAL, 0.65, 400, "middle")}
  <path d="M92,52 C102,52 104,56 110,62" fill="none" stroke="{CORAL}" stroke-opacity=".5" stroke-dasharray="3 4"/>
  <polygon points="112,64 104,60 106,68" fill="{CORAL}" opacity=".6"/>
  {label(30, 30, "worldgen", 7, CORAL, 0.65, 500)}

  <polygon points="86,64 190,32 294,64 190,96" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".45"/>
  <g clip-path="url(#topface)">
    <g stroke="{PAPER}" stroke-opacity=".09">
      <line x1="86" y1="50" x2="294" y2="50"/>
      <line x1="86" y1="66" x2="294" y2="66"/>
      <line x1="86" y1="82" x2="294" y2="82"/>
      <line x1="140" y1="30" x2="140" y2="96"/>
      <line x1="192" y1="30" x2="192" y2="96"/>
      <line x1="244" y1="30" x2="244" y2="96"/>
    </g>
    <polygon points="100,66 132,54 150,60 128,76 106,78" fill="{PAPER}" opacity=".1"/>
    <polygon points="210,50 238,40 258,48 236,62" fill="{PAPER}" opacity=".08"/>
    <path d="M92,72 C122,80 142,62 176,66 C208,70 232,86 286,76" fill="none" stroke="{CORAL}" stroke-opacity=".8" stroke-width="6" stroke-linecap="round"/>
    <path d="M92,72 C122,80 142,62 176,66 C208,70 232,86 286,76" fill="none" stroke="{PAPER}" stroke-opacity=".25" stroke-width="1.4"/>
  </g>

  <polygon points="86,64 190,96 190,154 86,122" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".25"/>
  <polygon points="294,64 190,96 190,154 294,122" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".18"/>
  <g stroke="{PAPER}" stroke-opacity=".12">{strata}</g>
  <line x1="86" y1="64" x2="190" y2="96" stroke="{CORAL}" stroke-opacity=".4"/>
  <line x1="294" y1="64" x2="190" y2="96" stroke="{CORAL}" stroke-opacity=".3"/>

  <g>
    <polygon points="118,112 130,106 142,112 130,118" fill="{CORAL}" opacity=".9"/>
    <polygon points="118,112 130,118 130,126 118,120" fill="{DEEP}"/>
    <polygon points="142,112 130,118 130,126 142,120" fill="{CORAL}" opacity=".55"/>
  </g>
  <g>
    <polygon points="156,128 166,123 176,128 166,133" fill="{PAPER}" opacity=".55"/>
    <polygon points="156,128 166,133 166,139 156,134" fill="{PAPER}" opacity=".25"/>
    <polygon points="176,128 166,133 166,139 176,134" fill="{PAPER}" opacity=".35"/>
  </g>
  <g>
    <polygon points="210,120 220,115 230,120 220,125" fill="{CORAL}" opacity=".65"/>
    <polygon points="210,120 220,125 220,131 210,126" fill="{DEEP}" opacity=".8"/>
    <polygon points="230,120 220,125 220,131 230,126" fill="{CORAL}" opacity=".35"/>
  </g>

  <g>
    <polygon points="112,52 120,48 128,52 120,56" fill="{PAPER}" opacity=".25"/>
    <polygon points="112,52 120,56 120,62 112,58" fill="{PAPER}" opacity=".12"/>
    <polygon points="128,52 120,56 120,62 128,58" fill="{PAPER}" opacity=".18"/>
  </g>
  <g>
    <polygon points="222,52 230,48 238,52 230,56" fill="{CORAL}" opacity=".45"/>
    <polygon points="222,52 230,56 230,63 222,59" fill="{CORAL}" opacity=".2"/>
    <polygon points="238,52 230,56 230,63 238,59" fill="{CORAL}" opacity=".3"/>
  </g>

  <g>
    <line x1="144" y1="62" x2="144" y2="68" stroke="{DEEP}" stroke-width="2"/>
    <polygon points="144,48 152,52 144,56 136,52" fill="{CORAL}"/>
    <polygon points="136,52 144,56 144,64 136,60" fill="{DEEP}"/>
    <polygon points="152,52 144,56 144,64 152,60" fill="{CORAL}" opacity=".55"/>
  </g>
  <g>
    <line x1="238" y1="68" x2="238" y2="73" stroke="{DEEP}" stroke-width="1.8"/>
    <polygon points="238,57 245,60 238,64 231,60" fill="{PAPER}" opacity=".55"/>
    <polygon points="231,60 238,64 238,71 231,67" fill="{PAPER}" opacity=".25"/>
    <polygon points="245,60 238,64 238,71 245,67" fill="{PAPER}" opacity=".35"/>
  </g>

  {label(190, 176, "generated chunk · strata + ore", 6.5, PAPER, 0.4, 400, "middle")}
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
def art_inception() -> str:
    return art(f"""
  <g>
    <circle cx="32" cy="52" r="10" fill="none" stroke="{PAPER}" stroke-opacity=".35"/>
    <ellipse cx="32" cy="52" rx="4" ry="10" fill="none" stroke="{PAPER}" stroke-opacity=".25"/>
    <line x1="22" y1="52" x2="42" y2="52" stroke="{PAPER}" stroke-opacity=".2"/>
    <line x1="42" y1="52" x2="62" y2="52" stroke="{CORAL}" stroke-width="2.5"/>
    <path d="M62,52 l-6,-4 v8 z" fill="{CORAL}"/>
    {label(48, 38, "443", 7, CORAL, 0.9, 500, "middle")}
  </g>

  <g>
    <rect x="62" y="30" width="238" height="40" rx="8" fill="{CORAL}"/>
    <g transform="translate(74,41)">
      <polygon points="0,7 8,3 16,7 8,11" fill="{NAVY}" opacity=".65"/>
      <polygon points="0,7 8,11 8,19 0,15" fill="{NAVY}" opacity=".4"/>
      <polygon points="16,7 8,11 8,19 16,15" fill="{NAVY}" opacity=".5"/>
    </g>
    {label(98, 55, "nginx", 13, NAVY, 1, 500)}
    {label(156, 54, "TLS · edge", 6.5, NAVY, 0.55)}
    <rect x="252" y="41" width="40" height="17" rx="8.5" fill="{NAVY}"/>
    {label(272, 53, "443", 7, PAPER, 0.9, 500, "middle")}
  </g>

  <g>
    <rect x="62" y="82" width="238" height="40" rx="8" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
    <g transform="translate(74,93)">
      <polygon points="0,7 8,3 16,7 8,11" fill="{PAPER}" opacity=".5"/>
      <polygon points="0,7 8,11 8,19 0,15" fill="{PAPER}" opacity=".2"/>
      <polygon points="16,7 8,11 8,19 16,15" fill="{PAPER}" opacity=".3"/>
    </g>
    {label(98, 107, "wordpress", 12, PAPER, 0.92, 500)}
    {label(180, 106, "php-fpm :9000", 6.5, PAPER, 0.45)}
    {label(290, 106, "internal", 6.5, PAPER, 0.35, 400, "end")}
  </g>

  <g>
    <rect x="62" y="134" width="238" height="40" rx="8" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".16"/>
    <g transform="translate(74,145)">
      <polygon points="0,7 8,3 16,7 8,11" fill="{PAPER}" opacity=".5"/>
      <polygon points="0,7 8,11 8,19 0,15" fill="{PAPER}" opacity=".2"/>
      <polygon points="16,7 8,11 8,19 16,15" fill="{PAPER}" opacity=".3"/>
    </g>
    {label(98, 159, "mariadb", 12, PAPER, 0.92, 500)}
    {label(180, 158, "3306 · data", 6.5, PAPER, 0.45)}
    {label(290, 158, "internal", 6.5, PAPER, 0.35, 400, "end")}
  </g>

  <g stroke="{CORAL}" stroke-opacity=".5" stroke-dasharray="3 3">
    <line x1="150" y1="70" x2="150" y2="82"/>
    <line x1="150" y1="122" x2="150" y2="134"/>
  </g>
  <g fill="{CORAL}" opacity=".7">
    <polygon points="150,84 146,78 154,78"/>
    <polygon points="150,132 146,138 154,138"/>
  </g>

  {label(181, 23, "docker compose · one network", 6.5, PAPER, 0.4, 400, "middle")}
""")
def art_born2beroot() -> str:
    bolts = []
    for dx, dy in ((0, -34), (24, -24), (34, 0), (24, 24), (0, 34), (-24, 24), (-34, 0), (-24, -24)):
        bolts.append(f'<circle cx="{114 + dx}" cy="{100 + dy}" r="2.2" fill="{PAPER}" opacity=".55"/>')
    bolts = "".join(bolts)
    return art(f"""
  <g>
    <rect x="48" y="26" width="128" height="160" rx="10" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".22"/>
    <rect x="48" y="26" width="128" height="22" rx="10" fill="{NAVY}"/>
    <rect x="48" y="40" width="128" height="8" fill="{NAVY}"/>
    {label(60, 41, "debian", 8, PAPER, 0.6, 500)}
    <circle cx="162" cy="37" r="3" fill="{CORAL}"/>

    <circle cx="114" cy="100" r="46" fill="{NAVY}" stroke="{CORAL}" stroke-width="3"/>
    <circle cx="114" cy="100" r="36" fill="none" stroke="{PAPER}" stroke-opacity=".18"/>
    {bolts}
    <g stroke="{CORAL}" stroke-width="4" stroke-linecap="round">
      <line x1="92" y1="100" x2="136" y2="100"/>
      <line x1="114" y1="78" x2="114" y2="122"/>
    </g>
    <circle cx="114" cy="100" r="7" fill="{CORAL}"/>
    <circle cx="114" cy="100" r="2.5" fill="{NAVY}"/>
    <rect x="90" y="93" width="48" height="15" rx="7.5" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".35"/>
    {label(114, 104, "LUKS", 7.5, CORAL, 0.95, 500, "middle")}

    {label(62, 153, "LVM", 6.5, PAPER, 0.55, 500)}
    <g fill="{PAPER}" opacity=".16">
      <rect x="62" y="158" width="104" height="7" rx="3.5"/>
      <rect x="62" y="169" width="104" height="7" rx="3.5"/>
    </g>
    <g fill="{CORAL}" opacity=".65">
      <rect x="62" y="158" width="30" height="7" rx="3.5"/>
      <rect x="62" y="169" width="46" height="7" rx="3.5"/>
    </g>
  </g>

  <g>
    <rect x="198" y="30" width="138" height="156" rx="9" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    <rect x="198" y="30" width="138" height="22" rx="9" fill="{CORAL}" opacity=".18"/>
    <rect x="198" y="44" width="138" height="8" fill="{CORAL}" opacity=".18"/>
    {label(210, 45, "HARDENING", 6.5, CORAL, 0.9, 500)}

    <g fill="{CORAL}">
      <circle cx="212" cy="72" r="2.4"/>
      <circle cx="212" cy="94" r="2.4"/>
      <circle cx="212" cy="116" r="2.4"/>
      <circle cx="212" cy="138" r="2.4"/>
      <circle cx="212" cy="160" r="2.4"/>
    </g>
    {label(222, 75, "firewall", 8, PAPER, 0.55)}
    {label(326, 75, "ufw on", 8, PAPER, 0.9, 500, "end")}
    {label(222, 97, "ssh", 8, PAPER, 0.55)}
    {label(326, 97, "4242", 8, CORAL, 0.95, 500, "end")}
    {label(222, 119, "sudo", 8, PAPER, 0.55)}
    {label(326, 119, "logged", 8, PAPER, 0.9, 500, "end")}
    {label(222, 141, "wall", 8, PAPER, 0.55)}
    {label(326, 141, "10 min", 8, PAPER, 0.9, 500, "end")}
    {label(222, 163, "disk", 8, PAPER, 0.55)}
    {label(326, 163, "LUKS + LVM", 8, PAPER, 0.9, 500, "end")}
  </g>
""")

PROJECTS = [
    {
        "n": "01",
        "file": "plate-01.png",
        "title": "dynamic-dashboard",
        "meta": "2026 · Solo · product &amp; full stack",
        "hook": "A local-first dashboard builder — tabs of isolated HTML widgets on one SQLite database, edited by an agent in place.",
        "stats": [("28", "starter widgets"), ("06", "example tabs"), ("01", "shared DB")],
        "stack": "Bun · Hono · SQLite · Vanilla JS · OpenCode",
        "href": "https://github.com/edouwarden/dynamic-dashboard",
        "art": DASHBOARD_ART,
        "alt": (
            "01 dynamic-dashboard, 2026, solo product and full stack: a local-first "
            "dashboard builder with isolated HTML widgets on one SQLite database, "
            "edited by an agent; 28 starter widgets, 6 example tabs, 1 shared DB; "
            "Bun, Hono, SQLite, Vanilla JS, OpenCode. Opens the repository."
        ),
    },
    {
        "n": "02",
        "file": "plate-02.png",
        "title": "ft_transcendence",
        "meta": "2026 · Team of four · engine &amp; platform",
        "hook": "A browser game engine built on Three.js: World → Environment → Module, physics, editors and live tools. The arena runs on it.",
        "stats": [("04", "engine layers"), ("04", "course maps"), ("20 Hz", "net tick")],
        "stack": "Next.js · Three.js · Rapier · Bun · Go · PostgreSQL",
        "href": "https://github.com/edouwarden/Transcendence-WebGameEngine",
        "art": art_transcendence(),
        "alt": (
            "02 ft_transcendence, 2026, team of four, engine and platform: a browser "
            "game engine on Three.js with World, Environment and Module layers, "
            "physics, editors and live tools, running a parkour arena; 4 engine "
            "layers, 4 course maps, 20 Hz net tick; Next.js, Three.js, Rapier, Bun, "
            "Go, PostgreSQL. Opens the repository."
        ),
    },
    {
        "n": "03",
        "file": "plate-03.png",
        "title": "space-gameserver",
        "meta": "2019 · Solo · systems &amp; geometry",
        "hook": "A 2019 Spigot sandbox: custom space and exoplanet dimensions, ships on an 11 × 11 orbital grid, five weapon systems as closed-form geometry.",
        "stats": [("2,000+", "members"), ("05", "powers"), ("11×11", "orbital slots")],
        "stack": "Java 8 · Paper 1.14.4 · WorldEdit · WorldGuard · Python",
        "href": "https://github.com/edouwarden/space-gameserver-2019-psr",
        "art": art_space(),
        "alt": (
            "03 space-gameserver, 2019, solo, systems and geometry: a Spigot "
            "sandbox with custom space and exoplanet dimensions, a chunk "
            "generator with strata and ore, ships on an 11 by 11 orbital grid, "
            "and five weapon systems as closed-form geometry; 2,000+ members, "
            "5 powers, 11 by 11 orbital slots; Java 8, Paper 1.14.4, WorldEdit, "
            "WorldGuard, Python. Opens the repository."
        ),
    },
    {
        "n": "04",
        "file": "plate-04.png",
        "title": "minishell",
        "meta": "2025 · Pair · systems &amp; parsing",
        "hook": "A Unix shell from the syscall up: quote-aware lexing, expansion, heredocs and 64-stage pipelines.",
        "stats": [("3,000", "lines of C"), ("64", "pipe stages"), ("0", "zombies")],
        "stack": "C99 · POSIX · fork/exec · dup2 · readline",
        "href": "https://github.com/edouwarden/minishell",
        "art": art_minishell(),
        "alt": (
            "04 minishell, 2025, pair, systems and parsing: a Unix shell with "
            "quote-aware lexing, expansion, heredocs and 64-stage pipelines, "
            "readline only; 3,000 lines of C, 64 pipe stages, 0 zombies; C99, "
            "POSIX, fork and exec, dup2, readline. Opens the repository."
        ),
    },
    {
        "n": "05",
        "file": "plate-05.png",
        "title": "cub3D",
        "meta": "2025 · Pair · rendering &amp; math",
        "hook": "A raycast renderer written by hand: 640 rays per frame, textured walls floor to ceiling, every pixel into an X11 buffer — no GPU.",
        "stats": [("640", "rays / frame"), ("03", "showcase maps"), ("~60", "frame cap")],
        "stack": "C99 · X11 · raycasting · XPM · math",
        "href": "https://github.com/edouwarden/cube3D",
        "art": art_cub3d(),
        "alt": (
            "05 cub3D, 2025, pair, rendering and math: a hand-written raycast "
            "renderer with 640 rays per frame, textured walls floor to ceiling and "
            "every pixel written into an X11 buffer without a GPU; 640 rays per "
            "frame, 3 showcase maps, about 60 fps cap; C99, X11, raycasting, XPM, "
            "math. Opens the repository."
        ),
    },
    {
        "n": "06",
        "file": "plate-06.png",
        "title": "ft_irc",
        "meta": "2026 · Pair · protocols &amp; systems",
        "hook": "An IRC server on one thread and one poll() loop: buffered TCP framing, channel modes, and a local Phi-3 answering in #ai-lab.",
        "stats": [("1", "thread"), ("1", "poll loop"), ("3.8B", "local model")],
        "stack": "C++98 · sockets · poll() · llama.cpp",
        "href": "https://github.com/edouwarden/irc",
        "art": art_irc(),
        "alt": (
            "06 ft_irc, 2026, pair, protocols and systems: an IRC server on one "
            "thread and one poll loop with buffered TCP framing, channel modes and "
            "a local Phi-3 answering in #ai-lab; 1 thread, 1 poll loop, 3.8B local "
            "model; C++98, sockets, poll, llama.cpp. Opens the repository."
        ),
    },
    {
        "n": "07",
        "file": "plate-07.png",
        "title": "Inception",
        "meta": "2026 · Solo · containers &amp; infra",
        "hook": "A WordPress stack where every part is a container: nginx holds TLS, MariaDB never leaves the compose network.",
        "stats": [("03", "services"), ("01", "open port"), ("04", "secrets")],
        "stack": "Docker Compose · NGINX · WordPress · MariaDB · TLS",
        "href": "https://github.com/edouwarden/inception",
        "art": art_inception(),
        "alt": (
            "07 Inception, 2026, solo, containers and infrastructure: a WordPress "
            "stack where every part is a container, nginx holds TLS, PHP-FPM runs "
            "WordPress and MariaDB never leaves the compose network; 3 services, "
            "1 open port, 4 secrets; Docker Compose, NGINX, WordPress, MariaDB, "
            "TLS. Opens the repository."
        ),
    },
    {
        "n": "08",
        "file": "plate-08.png",
        "title": "born2beroot",
        "meta": "2024 · Solo · systems &amp; hardening",
        "hook": "A reproducible Debian VM from a self-made ISO: LUKS under LVM, six filesystems, SSH on 4242, and every sudo logged.",
        "stats": [("07", "volumes"), ("01", "open port"), ("10 min", "wall")],
        "stack": "Debian · LUKS · LVM · UFW · systemd",
        "href": "https://github.com/edouwarden/born2beroot",
        "art": art_born2beroot(),
        "alt": (
            "08 born2beroot, 2024, solo, systems and hardening: a reproducible "
            "Debian VM from a self-made ISO with LUKS under LVM, six filesystems, "
            "SSH on port 4242 and every sudo logged; 7 volumes, 1 open port, wall "
            "broadcast every 10 minutes; Debian, LUKS, LVM, UFW, systemd. Opens "
            "the repository."
        ),
    },
]

CARD = """
<div class="plate">
  <div class="card">
    <div class="copy">
      <div class="head">
        <div class="num">{n}</div>
        <h2 class="title">{title}</h2>
      </div>
      <p class="meta">{meta}</p>
      <p class="hook">{hook}</p>
      <div class="specs">{specs}</div>
      <p class="stack">{stack}</p>
    </div>
    <div class="art">{art}<span class="go">↗</span></div>
  </div>
</div>
"""

SPEC = '<div class="spec"><b>{value}</b><span>{label}</span></div>'

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
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 32px;
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
  margin: 0; font-family: 'Days One', sans-serif; font-size: 46px;
  font-weight: 400; line-height: 1; letter-spacing: -0.02em;
}}
.meta {{
  margin: 14px 0 0; font-size: 10.5px; font-weight: 500;
  letter-spacing: 0.14em; text-transform: uppercase; color: rgba(12, 10, 62, 0.62);
}}
.hook {{
  max-width: 500px; margin: 14px 0 0; font-size: 18px;
  line-height: 1.5; color: rgba(12, 10, 62, 0.88);
}}
.specs {{
  display: flex; gap: 26px; margin-top: auto; padding-top: 14px;
  border-top: 1px solid rgba(12, 10, 62, 0.24);
}}
.spec {{ display: flex; flex-direction: column; gap: 2px; }}
.spec b {{
  display: flex; align-items: center; gap: 7px;
  font-family: 'Days One', sans-serif; font-size: 22px; font-weight: 400; line-height: 1;
}}
.spec b::before {{ content: ''; width: 6px; height: 6px; background: {NAVY}; }}
.spec span {{
  font-size: 8.5px; font-weight: 500; letter-spacing: 0.13em;
  text-transform: uppercase; color: rgba(12, 10, 62, 0.6);
}}
.stack {{
  margin: 12px 0 0; font-size: 9px; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(12, 10, 62, 0.5);
}}
.art {{ position: relative; align-self: center; width: 360px; height: 203px; }}
.art svg {{
  display: block; width: 360px; height: 203px; border-radius: 16px;
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(12, 10, 62, 0.35);
}}
.art .go {{
  position: absolute; right: -13px; bottom: -13px;
  display: grid; place-items: center; width: 46px; height: 46px;
  border-radius: 50%; background: #ffffff;
  font-family: 'Days One', sans-serif; font-size: 19px;
}}
"""


def card(project: dict) -> str:
    specs = "".join(
        SPEC.format(value=value, label=name) for value, name in project["stats"]
    )
    return CARD.format(
        n=project["n"],
        title=project["title"],
        meta=project["meta"],
        hook=project["hook"],
        specs=specs,
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


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 400},
            device_scale_factor=2,
        )
        for project in PROJECTS:
            page_path = BUILD / project["file"].replace(".png", ".html")
            page_path.write_text(document(project))
            page.goto(page_path.as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.screenshot(
                path=str(HERE / project["file"]),
                clip={"x": 0, "y": 0, "width": 1200, "height": 400},
            )
            print(f"rendered {project['file']}")
        browser.close()


if __name__ == "__main__":
    main()
