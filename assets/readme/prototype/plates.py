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
    o = (30, 126)
    u = (110, -60)
    v = (160, 60)
    grid = []
    for i in (0.25, 0.5, 0.75):
        grid.append(
            f'<line x1="{o[0] + u[0] * i:.1f}" y1="{o[1] + u[1] * i:.1f}" '
            f'x2="{o[0] + v[0] + u[0] * i:.1f}" y2="{o[1] + v[1] + u[1] * i:.1f}"/>'
        )
    for j in (0.25, 0.5, 0.75):
        grid.append(
            f'<line x1="{o[0] + v[0] * j:.1f}" y1="{o[1] + v[1] * j:.1f}" '
            f'x2="{o[0] + u[0] + v[0] * j:.1f}" y2="{o[1] + u[1] + v[1] * j:.1f}"/>'
        )
    grid = "".join(grid)
    return art(f"""
  <polygon points="30,126 140,66 300,126 190,186" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".55"/>
  <g stroke="{PAPER}" stroke-opacity=".08">{grid}</g>

  <g fill="{PAPER}" opacity=".06" stroke="{CORAL}" stroke-opacity=".5">
    <polygon points="120,90 150,74 170,90 140,106"/>
    <polygon points="200,60 226,46 244,60 218,74"/>
    <polygon points="230,130 254,117 270,130 246,143"/>
  </g>
  <g stroke="{CORAL}" stroke-opacity=".35" stroke-dasharray="3 4">
    <path d="M150,74 C170,60 196,60 218,60" fill="none"/>
    <path d="M238,74 C252,92 258,112 250,126" fill="none"/>
  </g>

  <g>
    <ellipse cx="155" cy="83" rx="6" ry="3" fill="{DEEP}"/>
    <rect x="149" y="74" width="12" height="9" rx="3" fill="{CORAL}"/>
    <ellipse cx="155" cy="74" rx="6" ry="3" fill="{PAPER}" opacity=".8"/>
  </g>
  <g stroke="{PAPER}" stroke-opacity=".55" fill="none">
    <path d="M143,68 L157,61 L173,68 L159,76 Z"/>
    <path d="M143,80 L157,73 L173,80 L159,88 Z"/>
    <line x1="143" y1="68" x2="143" y2="80"/>
    <line x1="157" y1="61" x2="157" y2="73"/>
    <line x1="173" y1="68" x2="173" y2="80"/>
    <line x1="159" y1="76" x2="159" y2="88"/>
  </g>

  <g>
    <rect x="250" y="34" width="92" height="134" rx="8" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    <rect x="250" y="34" width="92" height="18" rx="8" fill="{CORAL}" opacity=".18"/>
    {label(258, 46, "WORLD", 6, CORAL, 0.9, 500)}
    <circle cx="334" cy="43" r="2" fill="{CORAL}"/>
    <g fill="{CORAL}">
      <rect x="257" y="61" width="3" height="3"/>
      <rect x="257" y="75" width="3" height="3"/>
      <rect x="257" y="89" width="3" height="3"/>
      <rect x="257" y="103" width="3" height="3"/>
    </g>
    {label(264, 65, "1.engine", 6.5, PAPER, 0.7)}
    {label(264, 79, "2.world", 6.5, PAPER, 0.7)}
    {label(264, 93, "3.environment", 6.5, PAPER, 0.7)}
    {label(264, 107, "4.module", 6.5, PAPER, 0.7)}
    <line x1="257" y1="117" x2="335" y2="117" stroke="{PAPER}" stroke-opacity=".12"/>
    {label(258, 130, "world.yml", 6.5, CORAL, 0.95)}
    {label(258, 141, "mode: arena", 5.5, PAPER, 0.45)}
    <rect x="300" y="145" width="30" height="11" rx="5.5" fill="{CORAL}"/>
    {label(315, 152.5, "PLAY", 5, NAVY, 1, 500, "middle")}
  </g>

  <g stroke="{PAPER}" stroke-opacity=".4">
    <line x1="52" y1="54" x2="72" y2="54" stroke="{CORAL}"/>
    <line x1="52" y1="54" x2="52" y2="74" stroke="{PAPER}"/>
    <line x1="52" y1="54" x2="64" y2="66" stroke="{DEEP}"/>
  </g>
  {label(74, 57, "x", 5, CORAL, 0.8)}
  {label(49, 80, "y", 5, PAPER, 0.6)}
""")


def art_space() -> str:
    grid = []
    for x in range(30, 341, 16):
        grid.append(f'<line x1="{x}" y1="30" x2="{x}" y2="180"/>')
    for y in range(30, 181, 16):
        grid.append(f'<line x1="30" y1="{y}" x2="340" y2="{y}"/>')
    grid = "".join(grid)
    return art(f"""
  <g stroke="{PAPER}" stroke-opacity=".05">{grid}</g>
  <rect x="48" y="48" width="48" height="48" fill="{CORAL}" opacity=".06" stroke="{CORAL}" stroke-opacity=".5" stroke-dasharray="4 3"/>
  {label(52, 104, "11 × 11", 5.5, CORAL, 0.75)}

  <g stroke="{CORAL}" fill="none">
    <circle cx="136" cy="108" r="34" stroke-opacity=".65"/>
    <circle cx="136" cy="108" r="23" stroke-opacity=".28"/>
    <ellipse cx="136" cy="108" rx="56" ry="20" stroke-opacity=".18" stroke-dasharray="3 4"/>
  </g>
  <g stroke="{PAPER}" stroke-opacity=".35">
    <line x1="136" y1="74" x2="136" y2="82"/>
    <line x1="136" y1="134" x2="136" y2="142"/>
    <line x1="102" y1="108" x2="110" y2="108"/>
    <line x1="162" y1="108" x2="170" y2="108"/>
  </g>
  <circle cx="136" cy="108" r="9" fill="{CORAL}"/>
  <circle cx="136" cy="108" r="3.5" fill="{PAPER}"/>

  <g fill="{CORAL}">
    <polygon points="76,56 88,62 76,68"/>
    <polygon points="214,64 226,70 214,76"/>
    <polygon points="238,146 250,152 238,158"/>
  </g>
  <g stroke="{CORAL}" stroke-opacity=".4" stroke-dasharray="2 4" fill="none">
    <path d="M88,62 C104,70 112,88 126,100"/>
    <path d="M214,70 C192,82 172,94 148,104"/>
    <path d="M238,152 C204,150 174,136 148,118"/>
  </g>

  <g stroke="{CORAL}" fill="none">
    <path d="M286,44 C300,52 312,52 326,44" stroke-opacity=".6"/>
    <path d="M286,54 C300,62 312,62 326,54" stroke-opacity=".4"/>
    <path d="M286,64 C300,72 312,72 326,64" stroke-opacity=".25"/>
  </g>
  <g transform="translate(282,78)">
    <path d="M0,0 C14,10 28,10 42,0" stroke="{PAPER}" stroke-opacity=".4" fill="none"/>
    <path d="M0,8 C14,18 28,18 42,8" stroke="{DEEP}" stroke-opacity=".5" fill="none"/>
  </g>
  {label(288, 100, "PLASMA", 5, PAPER, 0.45)}

  <g stroke="{CORAL}" fill="none">
    <ellipse cx="252" cy="164" rx="40" ry="12" stroke-opacity=".45"/>
    <ellipse cx="252" cy="164" rx="27" ry="8" stroke-opacity=".3"/>
    <ellipse cx="252" cy="164" rx="14" ry="4" stroke-opacity=".2"/>
  </g>
  <g stroke="{PAPER}" stroke-opacity=".18">
    <line x1="286" y1="180" x2="310" y2="140"/>
    <line x1="290" y1="180" x2="322" y2="146"/>
    <line x1="294" y1="180" x2="332" y2="156"/>
  </g>
  {label(300, 126, "FRACTURE", 5, PAPER, 0.4)}

  <g transform="translate(314,30)">
    <circle r="2" fill="{CORAL}"/>
    <path d="M-7,0 a7,7 0 0 1 14,0" fill="none" stroke="{CORAL}" stroke-opacity=".4"/>
    <path d="M-12,0 a12,12 0 0 1 24,0" fill="none" stroke="{CORAL}" stroke-opacity=".2"/>
  </g>
  {label(300, 20, "VOICE", 4.5, PAPER, 0.4)}
""")


def art_minishell() -> str:
    return art(f"""
  <g>
    <rect x="18" y="30" width="208" height="142" rx="9" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    <path d="M18,39 a9,9 0 0 1 9,-9 h190 a9,9 0 0 1 9,9 v7 h-208 z" fill="{LIFT}"/>
    <circle cx="30" cy="38" r="2.4" fill="{CORAL}"/>
    <circle cx="38" cy="38" r="2.4" fill="{DEEP}"/>
    <circle cx="46" cy="38" r="2.4" fill="{PAPER}" opacity=".45"/>
    {label(60, 41, "minishell", 5.5, PAPER, 0.55)}
    <line x1="18" y1="46" x2="226" y2="46" stroke="{PAPER}" stroke-opacity=".1"/>

    {label(28, 60, "~/projects &gt;", 6.5, CORAL, 0.95)}
    {label(88, 60, "echo hi | cat", 6.5, PAPER, 0.85)}
    {label(28, 73, "hi", 6.5, PAPER, 0.55)}
    {label(28, 88, "~/projects &gt;", 6.5, CORAL, 0.95)}
    {label(88, 88, "echo $?", 6.5, PAPER, 0.85)}
    {label(28, 101, "0", 6.5, PAPER, 0.55)}
    {label(28, 116, "cat &lt;&lt;'L1'", 6.5, CORAL, 0.95)}
    {label(28, 129, "&lt;&lt;L2 | ./minishell", 6, PAPER, 0.45)}
    {label(28, 142, "&lt;&lt;L3 | cat -A", 6, PAPER, 0.35)}
    {label(28, 160, "no system() · no shell lib", 5.5, PAPER, 0.3)}
  </g>

  <g>
    <line x1="250" y1="50" x2="250" y2="158" stroke="{CORAL}" stroke-opacity=".35"/>
    <g fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".5">
      <rect x="238" y="42" width="32" height="15" rx="4"/>
      <rect x="238" y="77" width="32" height="15" rx="4"/>
      <rect x="238" y="112" width="32" height="15" rx="4"/>
      <rect x="238" y="147" width="32" height="15" rx="4"/>
    </g>
    {label(254, 52, "sh", 5.5, PAPER, 0.75, 500, "middle")}
    {label(254, 87, "cat", 5.5, PAPER, 0.75, 500, "middle")}
    {label(254, 122, "cat", 5.5, PAPER, 0.75, 500, "middle")}
    {label(254, 157, "wc", 5.5, PAPER, 0.75, 500, "middle")}
    <g stroke="{CORAL}" stroke-opacity=".45">
      <line x1="270" y1="57" x2="278" y2="57"/>
      <line x1="278" y1="57" x2="278" y2="77"/>
      <line x1="278" y1="92" x2="278" y2="112"/>
      <line x1="278" y1="127" x2="278" y2="147"/>
    </g>
    {label(286, 61, "fork", 5, PAPER, 0.45)}
    {label(286, 96, "dup2", 5, PAPER, 0.45)}
    {label(286, 131, "execve", 5, PAPER, 0.45)}
    {label(286, 166, "waitpid", 5, PAPER, 0.45)}
    <rect x="230" y="170" width="62" height="12" rx="6" fill="{CORAL}"/>
    {label(261, 178, "64 STAGES", 4.8, NAVY, 1, 500, "middle")}
  </g>

  <g transform="translate(298,42)">
    <rect width="38" height="52" rx="5" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
    {label(19, 12, "GC", 4.5, CORAL, 0.8, 500, "middle")}
    <g fill="{PAPER}" opacity=".25">
      <rect x="6" y="20" width="26" height="2.5" rx="1.25"/>
      <rect x="6" y="27" width="20" height="2.5" rx="1.25"/>
      <rect x="6" y="34" width="23" height="2.5" rx="1.25"/>
      <rect x="6" y="41" width="16" height="2.5" rx="1.25"/>
    </g>
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
    clients = [(30, 48, "fd 4"), (30, 82, "fd 5"), (30, 116, "fd 6"), (30, 150, "fd 7")]
    nodes = []
    for x, y, name in clients:
        nodes.append(
            f'<rect x="{x}" y="{y}" width="38" height="17" rx="4" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>'
            + label(x + 19, y + 11, name, 5, PAPER, 0.55, 400, "middle")
        )
        nodes.append(
            f'<line x1="{x + 38}" y1="{y + 8.5}" x2="126" y2="110" stroke="{CORAL}" stroke-opacity=".3"/>'
        )
    nodes = "".join(nodes)
    return art(f"""
  <ellipse cx="166" cy="110" rx="74" ry="76" fill="none" stroke="{CORAL}" stroke-opacity=".14" stroke-dasharray="3 5"/>
  {label(166, 26, "1 THREAD", 5, CORAL, 0.55, 500, "middle")}
  {nodes}

  <g>
    <rect x="126" y="82" width="80" height="56" rx="10" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".75"/>
    {label(166, 105, "poll()", 10, CORAL, 0.95, 500, "middle")}
    {label(166, 119, "one loop", 5.5, PAPER, 0.45, 400, "middle")}
    {label(166, 130, "no threads", 5, PAPER, 0.3, 400, "middle")}
  </g>

  <g fill="{CORAL}" opacity=".14" stroke="{CORAL}" stroke-opacity=".5">
    <rect x="238" y="54" width="64" height="16" rx="8"/>
    <rect x="238" y="82" width="64" height="16" rx="8"/>
    <rect x="238" y="110" width="64" height="16" rx="8"/>
  </g>
  {label(270, 65, "#general", 5.5, PAPER, 0.75, 500, "middle")}
  {label(270, 93, "#ai-lab", 5.5, PAPER, 0.75, 500, "middle")}
  {label(270, 121, "#ops", 5.5, PAPER, 0.75, 500, "middle")}
  <g stroke="{CORAL}" stroke-opacity=".35">
    <line x1="206" y1="96" x2="238" y2="62"/>
    <line x1="206" y1="106" x2="238" y2="90"/>
    <line x1="206" y1="116" x2="238" y2="118"/>
  </g>

  <g>
    <rect x="238" y="144" width="78" height="34" rx="6" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    {label(246, 156, "Phi-3 · Q4", 5.5, CORAL, 0.85, 500)}
    {label(246, 167, "loopback TCP", 4.8, PAPER, 0.45)}
    <line x1="238" y1="160" x2="206" y2="120" stroke="{CORAL}" stroke-opacity=".4" stroke-dasharray="3 3"/>
  </g>

  <g fill="{PAPER}" opacity=".2">
    <rect x="72" y="51" width="16" height="3" rx="1.5"/>
    <rect x="72" y="85" width="10" height="3" rx="1.5"/>
    <rect x="72" y="119" width="14" height="3" rx="1.5"/>
    <rect x="72" y="153" width="8" height="3" rx="1.5"/>
  </g>
""")


def art_inception() -> str:
    return art(f"""
  <rect x="22" y="36" width="250" height="142" rx="14" fill="none" stroke="{PAPER}" stroke-opacity=".14" stroke-dasharray="4 4"/>
  {label(30, 48, "compose network", 4.8, PAPER, 0.35)}

  <g>
    <rect x="36" y="58" width="80" height="38" rx="6" fill="{CORAL}"/>
    {label(76, 73, "nginx", 8, NAVY, 1, 500, "middle")}
    {label(76, 86, "TLS 1.3", 5, NAVY, 0.6, 400, "middle")}
    <rect x="100" y="106" width="94" height="38" rx="6" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
    {label(147, 121, "wordpress", 7, PAPER, 0.9, 500, "middle")}
    {label(147, 134, "php-fpm :9000", 4.8, PAPER, 0.45, 400, "middle")}
    <rect x="190" y="58" width="74" height="38" rx="6" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
    {label(227, 73, "mariadb", 7, PAPER, 0.9, 500, "middle")}
    {label(227, 86, "3306 internal", 4.8, PAPER, 0.45, 400, "middle")}
  </g>

  <g stroke="{CORAL}" stroke-opacity=".6" fill="none">
    <path d="M116,78 C126,88 132,96 140,106"/>
    <path d="M194,124 C208,110 218,98 226,96"/>
  </g>
  {label(128, 98, "fastcgi", 4.5, PAPER, 0.4)}
  {label(200, 104, "sql", 4.5, PAPER, 0.4)}

  <g>
    <line x1="20" y1="77" x2="36" y2="77" stroke="{CORAL}" stroke-width="2"/>
    <rect x="6" y="69" width="14" height="16" rx="3" fill="{CORAL}"/>
    <path d="M10,69 v-4 a3,3 0 0 1 6,0 v4" fill="none" stroke="{CORAL}" stroke-width="1.6"/>
    {label(13, 63, "443", 5, CORAL, 0.9, 500, "middle")}
    {label(13, 94, "one door", 4.5, PAPER, 0.4, 400, "middle")}
  </g>

  <g>
    <rect x="112" y="156" width="20" height="16" rx="2" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".2"/>
    <path d="M116,156 v-4 h12 v4" fill="none" stroke="{PAPER}" stroke-opacity=".25"/>
    {label(122, 167, "0600", 4, CORAL, 0.8, 400, "middle")}
    <rect x="190" y="156" width="20" height="16" rx="2" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".2"/>
    <path d="M194,156 v-4 h12 v4" fill="none" stroke="{PAPER}" stroke-opacity=".25"/>
    {label(200, 167, "0600", 4, CORAL, 0.8, 400, "middle")}
    <line x1="132" y1="164" x2="140" y2="144" stroke="{CORAL}" stroke-opacity=".3" stroke-dasharray="3 3"/>
    <line x1="190" y1="164" x2="180" y2="144" stroke="{CORAL}" stroke-opacity=".3" stroke-dasharray="3 3"/>
  </g>

  <g transform="translate(282,86)">
    <rect width="56" height="70" rx="8" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".16"/>
    {label(28, 14, "PORTS", 4.5, PAPER, 0.4, 400, "middle")}
    {label(28, 34, "443", 13, CORAL, 0.95, 500, "middle")}
    {label(28, 48, "open", 4.5, PAPER, 0.4, 400, "middle")}
    {label(28, 62, "1", 9, PAPER, 0.7, 500, "middle")}
  </g>
""")


def art_born2beroot() -> str:
    return art(f"""
  <g>
    <polygon points="30,150 118,112 208,150 120,188" fill="{NAVY}" stroke="{CORAL}" stroke-opacity=".7"/>
    <polygon points="30,136 118,98 208,136 120,174" fill="{LIFT}" stroke="{CORAL}" stroke-opacity=".55"/>
    <polygon points="30,122 118,84 208,122 120,160" fill="{LIFT}" stroke="{PAPER}" stroke-opacity=".2"/>
    {label(120, 150, "LUKS", 7, CORAL, 0.9, 500, "middle")}
    {label(120, 136, "LVM", 7, PAPER, 0.65, 500, "middle")}
    {label(120, 122, "XFS ×6 + swap", 6, PAPER, 0.55, 500, "middle")}
    <g stroke="{PAPER}" stroke-opacity=".12">
      <line x1="30" y1="122" x2="120" y2="160"/>
      <line x1="118" y1="84" x2="208" y2="122"/>
      <line x1="30" y1="136" x2="120" y2="174"/>
      <line x1="118" y1="98" x2="208" y2="136"/>
    </g>
  </g>

  <g transform="translate(40,58)">
    <rect x="0" y="8" width="22" height="17" rx="3" fill="{CORAL}"/>
    <path d="M5,8 v-5 a6,6 0 0 1 12,0 v5" fill="none" stroke="{CORAL}" stroke-width="2"/>
    <circle cx="11" cy="16" r="2" fill="{NAVY}"/>
  </g>
  {label(74, 70, "encrypted disk", 5, PAPER, 0.45)}

  <g>
    <rect x="232" y="36" width="106" height="112" rx="8" fill="{NAVY}" stroke="{PAPER}" stroke-opacity=".18"/>
    <rect x="232" y="36" width="106" height="17" rx="8" fill="{CORAL}" opacity=".18"/>
    {label(240, 48, "wall · 600 s", 5.5, CORAL, 0.9, 500)}
    <g stroke="{PAPER}" stroke-opacity=".1">
      <line x1="240" y1="62" x2="330" y2="62"/>
      <line x1="240" y1="76" x2="330" y2="76"/>
      <line x1="240" y1="90" x2="330" y2="90"/>
      <line x1="240" y1="104" x2="330" y2="104"/>
      <line x1="240" y1="118" x2="330" y2="118"/>
    </g>
    {label(240, 72, "arch", 5, PAPER, 0.45)}
    {label(270, 72, "x86_64", 5, PAPER, 0.75)}
    {label(240, 86, "mem", 5, PAPER, 0.45)}
    {label(270, 86, "2.4 G", 5, PAPER, 0.75)}
    {label(240, 100, "disk", 5, PAPER, 0.45)}
    {label(270, 100, "28 G", 5, PAPER, 0.75)}
    {label(240, 114, "users", 5, PAPER, 0.45)}
    {label(270, 114, "2", 5, PAPER, 0.75)}
    {label(240, 128, "sudo", 5, PAPER, 0.45)}
    {label(270, 128, "14", 5, CORAL, 0.85)}
    <g fill="{CORAL}" opacity=".35">
      <rect x="240" y="132" width="64" height="2" rx="1"/>
      <rect x="240" y="137" width="42" height="2" rx="1"/>
    </g>
  </g>

  <g>
    <rect x="230" y="158" width="88" height="18" rx="9" fill="{CORAL}"/>
    {label(274, 170, "SSH 4242", 6, NAVY, 1, 500, "middle")}
    <circle cx="250" cy="167" r="2" fill="{NAVY}"/>
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
        "hook": "A 2019 Spigot sandbox: ships on an 11 × 11 orbital grid, five weapon systems as closed-form geometry, voice over a TCP relay.",
        "stats": [("2,000+", "members"), ("05", "powers"), ("11×11", "orbital slots")],
        "stack": "Java 8 · Paper 1.14.4 · WorldEdit · WorldGuard · Python",
        "href": "https://github.com/edouwarden/space-gameserver-2019-psr",
        "art": art_space(),
        "alt": (
            "03 space-gameserver, 2019, solo, game systems and geometry: a Spigot "
            "sandbox with ships on an 11 by 11 orbital grid, five weapon systems "
            "as closed-form geometry and a TCP proximity-voice relay; 2,000+ "
            "members, 5 powers, 11 by 11 orbital slots; Java 8, Paper 1.14.4, "
            "WorldEdit, WorldGuard, Python. Opens the repository."
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
