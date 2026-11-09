#!/usr/bin/env python3
"""Render the data rails that sit around the project plates: the stack
marquee, the language line, the now line, the live-demo strip, the peer-review
marquee and the contact line.

The stack is a vector marquee: 24 coral icons over two full-width rows that
scroll slowly in opposite directions under a re-added title. The names are the
interesting parts of the projects, not the generic tools around them. The review
rail uses the same trick for quotes. Because they are SVGs, the type stays sharp
at any zoom and the loops cost almost nothing to load. The language line reads
the pygount snapshot (loc.json) and prints each language's share of the counted
lines.

All boards use the deck's ambient palette and type and stack flush with the
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

ROW_TOP = (
    ("Bun", "bun"),
    ("Hono", "hono"),
    ("SQLite", "sqlite"),
    ("OpenCode", "opencode"),
    ("Next.js", "nextdotjs"),
    ("Three.js", "threedotjs"),
    ("Rapier", "rapier"),
    ("Spigot", "spigotmc"),
    ("llama.cpp", "llamacpp"),
    ("PostgreSQL", "postgresql"),
    ("Tailscale", "tailscale"),
    ("Cloudflare", "cloudflareworkers"),
)

ROW_BOTTOM = (
    ("C", "c"),
    ("C++", "cplusplus"),
    ("Go", "go"),
    ("Docker", "docker"),
    ("NGINX", "nginx"),
    ("Debian", "debian"),
    ("LUKS", "luks"),
    ("LVM", "lvm"),
    ("Vault", "vault"),
    ("nftables", "nftables"),
    ("Suricata", "suricata"),
    ("Firecracker", "firecracker"),
)

ICONS = json.loads((HERE / "tech-icons.json").read_text())
ICONS.update(json.loads((HERE / "tech-icons-generic.json").read_text()))

LANG_DISPLAY = {"Other": "Bash"}

STACK_W = 900
STACK_H = 150
MARGIN = 48
ICON = 34
ICON_GAP = 6
ITEM_GAP = 20
LABEL_SIZE = 12.5
LABEL_TRACK = 0.72
SPEED = 62.0  # marquee units per second

NOW_W, NOW_H = 900, 63
LIVE_W, LIVE_H = 900, 72
REVIEWS_W, REVIEWS_H = 900, 132
CONTACT_W, CONTACT_H = 900, 63

# Placeholder copy for the mockup. Replace with real reviews before publishing.
REVIEWS = (
    ("Read the whole shell before asking a single question.", "42 PARIS · PEER REVIEW"),
    ("The raycaster held 60 fps on every map. Clean C.", "42 PARIS · PEER REVIEW"),
    ("Shipped the engine, the editor and the docs.", "42 PARIS · PEER REVIEW"),
)

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


def short_number(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return "0" if text in ("", "-0") else text


def text_path(
    text: str, size: float, tracking: float, x: float = 0.0, baseline: float = 0.0
) -> str:
    parts = []
    pen_x = x
    for ch in text:
        glyph = CMAP.get(ord(ch))
        if glyph is None:
            continue
        pen = SVGPathPen(GLYPHS, ntos=short_number)
        transform = Transform(size / UPM, 0, 0, -size / UPM, pen_x, baseline)
        GLYPHS[glyph].draw(TransformPen(pen, transform))
        commands = pen.getCommands()
        if commands:
            parts.append(commands)
        pen_x += HMTX[glyph][0] / UPM * size + tracking
    return " ".join(parts)


def svg_open(width: int, height: int, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f"<title>{title}</title>"
        f'<rect width="{width}" height="{height}" fill="{NAVY}"/>'
    )


def kicker(main: str, alt: str, x: float, baseline: float) -> str:
    size, track = 13.0, 2.08
    parts = []
    d = text_path(main, size, track, x, baseline)
    parts.append(f'<path d="{d}" fill="{PAPER}"/>')
    x += text_width(main, size, track) + track + 8
    d = text_path("/", size, track, x, baseline)
    parts.append(f'<path d="{d}" fill="{CORAL}"/>')
    x += text_width("/", size, track) + track + 8
    d = text_path(alt, size, track, x, baseline)
    parts.append(f'<path d="{d}" fill="{PAPER}" fill-opacity="0.55"/>')
    return "".join(parts)


def subline(text: str, x: float, baseline: float) -> str:
    return (
        f'<path d="{text_path(text, 9.5, 1.14, x, baseline)}" '
        f'fill="{PAPER}" fill-opacity="0.36"/>'
    )


def hairline(x1: float, y: float, x2: float, opacity: float = 0.09) -> str:
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" '
        f'stroke="{PAPER}" stroke-opacity="{opacity}"/>'
    )


def arrow_path(x: float, y: float, length: float = 10) -> str:
    return (
        f'<path d="M{x} {y} h{length} '
        f'M{x + length - 4} {y - 4} l4 4 -4 4" '
        f'stroke="{CORAL}" stroke-width="1.6" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def icon_symbol(slug: str) -> str:
    icon = ICONS[slug]
    if isinstance(icon, str):
        return f'<symbol id="ico-{slug}" viewBox="0 0 24 24"><path d="{icon}"/></symbol>'
    scale = 24 / icon.get("viewBox", 24)
    return (
        f'<symbol id="ico-{slug}" viewBox="0 0 24 24">'
        f'<g transform="scale({scale:.6f})"><path d="{icon["path"]}"/></g>'
        "</symbol>"
    )


def item_width(label: str) -> float:
    return (
        ICON
        + ICON_GAP
        + text_width(label.upper(), LABEL_SIZE, LABEL_TRACK)
        + ITEM_GAP
    )


def stack_svg() -> str:
    row1_y = 52
    row2_y = 100
    rule_y = STACK_H - 1
    fade_w = 88
    band_y = row1_y - 8
    band_h = row2_y + ICON + 8 - band_y
    label_y = 21.5

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{STACK_W}" height="{STACK_H}" '
        f'viewBox="0 0 {STACK_W} {STACK_H}" role="img">',
        "<title>Stack used</title>",
        "<defs>",
    ]

    for _, slug in ROW_TOP + ROW_BOTTOM:
        out.append(icon_symbol(slug))

    for i, (label, _) in enumerate(ROW_TOP + ROW_BOTTOM):
        d = text_path(label.upper(), LABEL_SIZE, LABEL_TRACK)
        out.append(f'<path id="lab-{i}" d="{d}"/>')

    for i, (_, slug) in enumerate(ROW_TOP + ROW_BOTTOM):
        out.append(
            f'<g id="it-{i}">'
            f'<use href="#ico-{slug}" xlink:href="#ico-{slug}" width="{ICON}" height="{ICON}" fill="{CORAL}"/>'
            f'<use href="#lab-{i}" xlink:href="#lab-{i}" x="{ICON + ICON_GAP}" y="{label_y}" fill="{PAPER}" fill-opacity="0.64"/>'
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
    out.append(f'<rect x="{MARGIN}" y="19" width="9" height="9" fill="{CORAL}"/>')
    tx = MARGIN + 9 + 10
    d = text_path("STACK", title_size, title_track, tx, 28)
    out.append(f'<path d="{d}" fill="{PAPER}"/>')
    tx += text_width("STACK", title_size, title_track) + title_track + 8
    d = text_path("/", title_size, title_track, tx, 28)
    out.append(f'<path d="{d}" fill="{CORAL}"/>')
    tx += text_width("/", title_size, title_track) + title_track + 8
    d = text_path("USED", title_size, title_track, tx, 28)
    out.append(f'<path d="{d}" fill="{PAPER}" fill-opacity="0.55"/>')

    # Two marquee rows, each duplicated once so the loop is seamless. The gap
    # is measured from each label, not from the longest label in the deck.
    for idx, row in enumerate((ROW_TOP, ROW_BOTTOM)):
        y = row1_y if idx == 0 else row2_y
        reverse = idx == 1
        row_width = sum(item_width(label) for label, _ in row)
        duration = row_width / SPEED
        start, end = (0, -row_width) if not reverse else (-row_width, 0)
        out.append(f'<g transform="translate(0 {y})"><g>')
        out.append(
            f'<animateTransform attributeName="transform" type="translate" '
            f'from="{start:.2f} 0" to="{end:.2f} 0" dur="{duration:.3f}s" repeatCount="indefinite"/>'
        )
        base = idx * len(ROW_TOP)
        x = 0.0
        for _ in range(2):
            for i, (label, _) in enumerate(row):
                item = base + i
                out.append(
                    f'<use href="#it-{item}" xlink:href="#it-{item}" x="{x:.2f}"/>'
                )
                x += item_width(label)
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


def now_svg() -> str:
    out = [svg_open(NOW_W, NOW_H, "Now: Forge, publishing in parts")]
    out.append(f'<rect x="{MARGIN}" y="18" width="9" height="9" fill="{CORAL}"/>')
    out.append(kicker("NOW", "FORGE", MARGIN + 19, 28.5))
    out.append(subline("A NEW SYSTEMS PROJECT", MARGIN + 19, 45))

    label = "PUBLISHING IN PARTS"
    label_w = text_width(label, 9.5, 1.14)
    right = NOW_W - MARGIN
    out.append(
        f'<circle cx="{right - label_w - 15}" cy="25" r="3.5" fill="{CORAL}">'
        '<animate attributeName="opacity" values="1;0.3;1" dur="2.8s" '
        'repeatCount="indefinite"/></circle>'
    )
    out.append(
        f'<path d="{text_path(label, 9.5, 1.14, right - label_w, 28)}" '
        f'fill="{PAPER}" fill-opacity="0.55"/>'
    )
    out.append(hairline(360, 31.5, right - label_w - 34))
    out.append(hairline(MARGIN, NOW_H - 1, right))
    out.append("</svg>")
    return "".join(out)


def live_svg() -> str:
    out = [svg_open(LIVE_W, LIVE_H, "Live demo: dynamic-dashboard")]
    out.append(
        f'<circle cx="{MARGIN + 4}" cy="25" r="3.5" fill="{CORAL}">'
        '<animate attributeName="opacity" values="1;0.3;1" dur="2.6s" '
        'repeatCount="indefinite"/></circle>'
    )
    out.append(kicker("LIVE", "DEMO", MARGIN + 19, 30.5))
    out.append(
        subline(
            "DYNAMIC-DASHBOARD · NO SIGNUP · FICTIONAL DATA", MARGIN + 19, 47
        )
    )

    url = "dynamic-dashboard.ednormand.fr"
    size, track = 10.5, 0.7
    url_w = text_width(url, size, track)
    pill_h = 34.0
    pill_w = 18 + url_w + 14 + 10 + 18
    pill_x = LIVE_W - MARGIN - pill_w
    pill_y = (LIVE_H - pill_h) / 2
    out.append(
        f'<rect x="{pill_x:.2f}" y="{pill_y:.2f}" width="{pill_w:.2f}" '
        f'height="{pill_h:.2f}" rx="{pill_h / 2}" fill="{PAPER}"/>'
    )
    out.append(
        f'<path d="{text_path(url, size, track, pill_x + 18, pill_y + 22.5)}" '
        f'fill="{NAVY}"/>'
    )
    out.append(arrow_path(pill_x + 18 + url_w + 14, pill_y + pill_h / 2))
    out.append(hairline(400, LIVE_H / 2, pill_x - 30, 0.08))
    out.append(hairline(MARGIN, LIVE_H - 1, LIVE_W - MARGIN))
    out.append("</svg>")
    return "".join(out)


def contact_svg() -> str:
    out = [svg_open(CONTACT_W, CONTACT_H, "Contact")]
    out.append(f'<rect x="{MARGIN}" y="18" width="9" height="9" fill="{CORAL}"/>')
    out.append(kicker("CONTACT", "EMAIL", MARGIN + 19, 28.5))
    out.append(subline("DIRECT LINE", MARGIN + 19, 45))

    email = "ed.normand@protonmail.com"
    size, track = 10.5, 0.7
    email_w = text_width(email, size, track)
    right = CONTACT_W - MARGIN
    start = right - email_w - 10 - 10
    out.append(
        f'<path d="{text_path(email, size, track, start, 35.5)}" '
        f'fill="{PAPER}" fill-opacity="0.82"/>'
    )
    out.append(arrow_path(start + email_w + 10, 31.5))
    out.append(hairline(360, 31.5, start - 28))
    out.append(hairline(MARGIN, CONTACT_H - 1, right))
    out.append("</svg>")
    return "".join(out)


def reviews_svg() -> str:
    out = [svg_open(REVIEWS_W, REVIEWS_H, "Peer reviews")]
    out.append("<defs>")
    out.append(
        f'<linearGradient id="revFadeL" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>'
        "</linearGradient>"
    )
    out.append(
        f'<linearGradient id="revFadeR" x1="1" y1="0" x2="0" y2="0">'
        f'<stop offset="0" stop-color="{NAVY}"/>'
        f'<stop offset="1" stop-color="{NAVY}" stop-opacity="0"/>'
        "</linearGradient>"
    )

    mark_size, quote_size, quote_track = 26.0, 12.5, 0.1
    attr_size, attr_track = 9.5, 1.14
    item_gap = 64.0
    widths = []
    for i, (quote, source) in enumerate(REVIEWS):
        mark_w = text_width("“", mark_size, quote_track)
        quote_w = text_width(quote, quote_size, quote_track)
        attr = f"— {source}"
        attr_w = text_width(attr, attr_size, attr_track)
        out.append(
            f'<g id="rev-{i}">'
            f'<path d="{text_path("“", mark_size, quote_track, 0, 0)}" '
            f'fill="{CORAL}" fill-opacity="0.9"/>'
            f'<path d="{text_path(quote, quote_size, quote_track, mark_w + 6, 0)}" '
            f'fill="{PAPER}" fill-opacity="0.8"/>'
            f'<path d="{text_path(attr, attr_size, attr_track, mark_w + 6 + quote_w + 18, 0)}" '
            f'fill="{CORAL}" fill-opacity="0.82"/>'
            "</g>"
        )
        widths.append(mark_w + 6 + quote_w + 18 + attr_w + item_gap)
    out.append("</defs>")

    out.append(f'<rect x="{MARGIN}" y="18" width="9" height="9" fill="{CORAL}"/>')
    out.append(kicker("PEER", "REVIEWS", MARGIN + 19, 28.5))
    out.append(subline("SELECTED NOTES · 42 PARIS", MARGIN + 19, 45))
    out.append(hairline(MARGIN, 57, REVIEWS_W - MARGIN, 0.08))

    row_width = sum(widths)
    duration = row_width / 34.0
    out.append(
        '<g transform="translate(0 92)"><g>'
        '<animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="{-row_width:.2f} 0" dur="{duration:.3f}s" '
        'repeatCount="indefinite"/>'
    )
    x = 0.0
    for _ in range(2):
        for i, item_w in enumerate(widths):
            out.append(
                f'<use href="#rev-{i}" xlink:href="#rev-{i}" x="{x:.2f}"/>'
            )
            x += item_w
    out.append("</g></g>")

    out.append(
        f'<rect x="0" y="66" width="64" height="48" fill="url(#revFadeL)"/>'
    )
    out.append(
        f'<rect x="{REVIEWS_W - 64}" y="66" width="64" height="48" '
        'fill="url(#revFadeR)"/>'
    )
    out.append(hairline(MARGIN, REVIEWS_H - 1, REVIEWS_W - MARGIN))
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


def write_rail(name: str, svg: str) -> None:
    out = HERE / name
    out.write_text(svg)
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
    write_rail("deck-stack.svg", stack_svg())
    write_rail("deck-now.svg", now_svg())
    write_rail("deck-live.svg", live_svg())
    write_rail("deck-reviews.svg", reviews_svg())
    write_rail("deck-contact.svg", contact_svg())
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
