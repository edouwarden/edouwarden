#!/usr/bin/env python3
"""Render the two data rails that sit between the header and the project
plates: a two-row technology marquee and a language line.

The stack is a vector marquee: 24 Simple Icons paths in the deck's coral, laid
over two full-width rows that scroll slowly in opposite directions under a
re-added title. Because it is an SVG, the icons stay sharp at any zoom and the
loop costs almost nothing to load. The language line reads the pygount snapshot
(loc.json) and prints each language's share of the counted lines.

Both boards use the deck's ambient palette and type and stack flush with the
header and plates.

    python3 assets/readme/prototype/stats.py
"""

from __future__ import annotations

import json
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
BUILD = HERE.parent / ".build" / "stats"

NAVY = "#0c0a3e"
CORAL = "#f9564f"
PAPER = "#fffaf0"

TECH_ROWS = (
    (
        ("Next.js", "nextdotjs"),
        ("React", "react"),
        ("Three.js", "threedotjs"),
        ("Vite", "vite"),
        ("Tailwind", "tailwindcss"),
        ("Bun", "bun"),
    ),
    (
        ("Hono", "hono"),
        ("Node.js", "nodedotjs"),
        ("WordPress", "wordpress"),
        ("Postgres", "postgresql"),
        ("SQLite", "sqlite"),
        ("MariaDB", "mariadb"),
    ),
    (
        ("Docker", "docker"),
        ("Nginx", "nginx"),
        ("Linux", "linux"),
        ("Debian", "debian"),
        ("VirtualBox", "virtualbox"),
        ("OpenSSL", "openssl"),
    ),
    (
        ("Let's Encrypt", "letsencrypt"),
        ("Git", "git"),
        ("GitHub", "github"),
        ("GH Actions", "githubactions"),
        ("npm", "npm"),
        ("VS Code", "visualstudiocode"),
    ),
)

ROW_TOP = TECH_ROWS[0] + TECH_ROWS[1]
ROW_BOTTOM = TECH_ROWS[2] + TECH_ROWS[3]

ICONS = json.loads((HERE / "tech-icons.json").read_text())

LANG_DISPLAY = {"Other": "Bash"}

STACK_W = 900
STACK_H = 136
MARGIN = 48
ICON = 24
LABEL_SIZE = 12.0
LABEL_TRACK = 0.72
SPEED = 70.0  # marquee units per second

FONT = TTFont(FONTS / "ibm-plex-mono-500-v1.woff2")
UPM = FONT["head"].unitsPerEm
CMAP = FONT.getBestCmap()
GLYPHS = FONT.getGlyphSet()
HMTX = FONT["hmtx"]


def text_width(text: str, size: float, tracking: float) -> float:
    if not text:
        return 0.0
    total = 0.0
    for ch in text:
        glyph = CMAP.get(ord(ch))
        if glyph:
            total += HMTX[glyph][0] / UPM * size + tracking
    return total - tracking


def text_path(
    text: str, size: float, tracking: float, x: float = 0.0, baseline: float = 0.0
) -> str:
    parts = []
    pen_x = x
    for ch in text:
        glyph = CMAP.get(ord(ch))
        if glyph is None:
            continue
        pen = SVGPathPen(GLYPHS)
        transform = Transform(size / UPM, 0, 0, -size / UPM, pen_x, baseline)
        GLYPHS[glyph].draw(TransformPen(pen, transform))
        commands = pen.getCommands()
        if commands:
            parts.append(commands)
        pen_x += HMTX[glyph][0] / UPM * size + tracking
    return " ".join(parts)


def stack_svg() -> str:
    label_w = max(
        text_width(label.upper(), LABEL_SIZE, LABEL_TRACK)
        for label, _ in ROW_TOP + ROW_BOTTOM
    )
    pitch = ICON + 10 + label_w + 46
    half = pitch * 12
    duration = half / SPEED

    row1_y = 52
    row2_y = 96
    rule_y = STACK_H - 1
    fade_w = 96
    band_y = row1_y - 8
    band_h = row2_y + ICON + 8 - band_y

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{STACK_W}" height="{STACK_H}" '
        f'viewBox="0 0 {STACK_W} {STACK_H}" role="img">',
        "<title>Stack used</title>",
        "<defs>",
    ]

    for _, slug in ROW_TOP + ROW_BOTTOM:
        out.append(
            f'<symbol id="ico-{slug}" viewBox="0 0 24 24"><path d="{ICONS[slug]}"/></symbol>'
        )

    for i, (label, _) in enumerate(ROW_TOP + ROW_BOTTOM):
        d = text_path(label.upper(), LABEL_SIZE, LABEL_TRACK)
        out.append(f'<path id="lab-{i}" d="{d}"/>')

    for i, (_, slug) in enumerate(ROW_TOP + ROW_BOTTOM):
        out.append(
            f'<g id="it-{i}">'
            f'<use href="#ico-{slug}" xlink:href="#ico-{slug}" width="{ICON}" height="{ICON}" fill="{CORAL}"/>'
            f'<use href="#lab-{i}" xlink:href="#lab-{i}" x="34" y="16.5" fill="{PAPER}" fill-opacity="0.64"/>'
            "</g>"
        )

    out.append(
        f'<linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>'
        "</linearGradient>"
    )
    out.append(
        f'<linearGradient id="fadeR" x1="1" y1="0" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>'
        "</linearGradient>"
    )
    out.append("</defs>")

    out.append(f'<rect width="{STACK_W}" height="{STACK_H}" fill="{NAVY}"/>')

    # Title.
    title_size = 13.0
    title_track = 2.08
    out.append(f'<rect x="{MARGIN}" y="21" width="9" height="9" fill="{CORAL}"/>')
    tx = MARGIN + 9 + 10
    d = text_path("STACK", title_size, title_track, tx, 30)
    out.append(f'<path d="{d}" fill="{PAPER}"/>')
    tx += text_width("STACK", title_size, title_track) + title_track + 8
    d = text_path("/", title_size, title_track, tx, 30)
    out.append(f'<path d="{d}" fill="{CORAL}"/>')
    tx += text_width("/", title_size, title_track) + title_track + 8
    d = text_path("USED", title_size, title_track, tx, 30)
    out.append(f'<path d="{d}" fill="{PAPER}" fill-opacity="0.55"/>')

    # Two marquee rows, each duplicated once so the loop is seamless.
    for idx, base in enumerate((0, 12)):
        y = row1_y if idx == 0 else row2_y
        reverse = idx == 1
        start, end = (0, -half) if not reverse else (-half, 0)
        out.append(f'<g transform="translate(0 {y})"><g>')
        out.append(
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{start:.2f} 0" to="{end:.2f} 0" dur="{duration:.3f}s" repeatCount="indefinite"/>'
        )
        for k in range(24):
            item = base + k % 12
            out.append(
                f'<use href="#it-{item}" xlink:href="#it-{item}" x="{k * pitch:.2f}"/>'
            )
        out.append("</g></g>")

    out.append(
        f'<rect x="0" y="{band_y}" width="{fade_w}" height="{band_h}" fill="url(#fadeL)"/>'
    )
    out.append(
        f'<rect x="{STACK_W - fade_w}" y="{band_y}" width="{fade_w}" height="{band_h}" '
        'fill="url(#fadeR)"/>'
    )
    out.append(
        f'<line x1="{MARGIN}" y1="{rule_y}" x2="{STACK_W - MARGIN}" y2="{rule_y}" '
        'stroke="#fffaf0" stroke-opacity="0.09"/>'
    )
    out.append("</svg>")
    return "".join(out)


def font_faces() -> str:
    return f"""
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
"""


def language_line(data: dict) -> str:
    items = []
    for entry in data["languages"]:
        name = LANG_DISPLAY.get(entry["name"], entry["name"])
        share = entry["lines"] / data["total"] * 100
        items.append(
            '<span class="lang">'
            f'<span class="lname">{name}</span>'
            f'<span class="lshare">{share:.1f}%</span></span>'
        )
    return "".join(items)


def language_document(data: dict) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_faces()}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: 1200px; font-family: 'Plex Mono', monospace; -webkit-font-smoothing: antialiased; }}
.line {{
  position: relative;
  width: 1200px; height: 84px;
  padding: 0 64px;
  display: grid;
  grid-template-columns: 232px minmax(0, 1fr);
  align-items: center;
  background: {NAVY};
  color: {PAPER};
}}
.line::after {{
  content: ''; position: absolute; left: 64px; right: 64px; bottom: 0;
  height: 1px; background: rgba(255, 250, 240, 0.09);
}}
.kicker {{
  display: flex; align-items: center; gap: 11px;
  font-size: 13px; font-weight: 500; letter-spacing: 0.16em;
  text-transform: uppercase; color: {PAPER};
}}
.kicker .mark {{ width: 10px; height: 10px; background: {CORAL}; }}
.sub {{
  margin-top: 8px;
  font-size: 9.5px; letter-spacing: 0.12em; text-transform: uppercase;
  color: rgba(255, 250, 240, 0.36);
}}
.langs {{ display: flex; align-items: baseline; }}
.langs::before {{
  content: ''; align-self: center; flex: 1; height: 1px; margin-right: 26px;
  background: rgba(255, 250, 240, 0.10);
}}
.lang {{
  display: flex; align-items: baseline; gap: 7px;
  font-size: 11px; font-weight: 500; letter-spacing: 0.07em;
  line-height: 1; text-transform: uppercase; white-space: nowrap;
}}
.lang + .lang {{ margin-left: 26px; }}
.lname {{ color: rgba(255, 250, 240, 0.62); }}
.lshare {{ font-size: 10px; letter-spacing: 0.04em; color: {CORAL}; opacity: 0.82; }}
</style></head><body>
<div class="line">
  <div class="pin">
    <div class="kicker"><span class="mark"></span>Languages</div>
    <div class="sub">share of {data['total']:,} lines</div>
  </div>
  <div class="langs">{language_line(data)}</div>
</div>
</body></html>"""


def write_stack() -> None:
    out = HERE / "deck-stack.svg"
    out.write_text(stack_svg())
    print(f"wrote {out.name} ({out.stat().st_size / 1024:.0f} KiB)")


def render_languages(page, data: dict) -> None:
    page.set_viewport_size({"width": 1200, "height": 84})
    board = BUILD / "languages.html"
    board.write_text(language_document(data))
    page.goto(board.as_uri())
    page.wait_for_function("document.fonts.status === 'loaded'")
    page.screenshot(
        path=str(HERE / "deck-languages.png"),
        clip={"x": 0, "y": 0, "width": 1200, "height": 84},
    )
    print("wrote deck-languages.png")


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    data = json.loads((HERE / "loc.json").read_text())
    write_stack()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 84},
            device_scale_factor=1.5,
        )
        render_languages(page, data)
        browser.close()


if __name__ == "__main__":
    main()
