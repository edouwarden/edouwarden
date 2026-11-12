#!/usr/bin/env python3
"""Render the data rails that sit around the project plates: the stack
marquee, the language line, the project-section header, the try-it strip, the
open-to-work strip and the peer-review cards.

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
LIFT = "#17134f"
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

PROJECTS_W, PROJECTS_H = 900, 84
TRY_W, TRY_H = 900, 44
OPEN_W, OPEN_H = 900, 44
REVIEWS_W = 900

# Quotes from 42 peer evaluations, translated from French and trimmed to the
# substantive clause. The verbatim originals live in the review notes. Credit
# is first name, last initial, project and score, so a quote stays checkable
# without publishing anyone's full name or 42 login.
REVIEWS = (
    (
        "An excellent ft_irc: genuinely clean, well-structured code for a "
        "tough subject, gorgeous logs, and a bot with real personality. The "
        "local sLLM was perfect.",
        "Alexis L. · FT_IRC · 110%",
    ),
    (
        "They explained everything, showing a deep understanding of every "
        "module they built. The game is fun and cute — 24 modules where the "
        "minimum was 14.",
        "Amanda F. · TRANSCENDENCE · 125%",
    ),
    (
        "An extremely well-done project, maybe even overdone on the config. "
        "Great work making a boring project fascinating.",
        "Nitai G. · BORN2BEROOT · 115%",
    ),
    (
        "Good team, solid understanding overall. A hiccup with the bot, fixed "
        "in under a minute — validated. Good luck with the rest.",
        "Andy K. · FT_IRC · 110%",
    ),
    (
        "Great project, well understood and well explained. Bravo, and good "
        "luck with what comes next.",
        "Dorian M. · CUB3D · 115%",
    ),
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


def wrap_text(
    text: str, size: float, tracking: float, max_width: float
) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if not current or text_width(candidate, size, tracking) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


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


def kicker(main: str, x: float, baseline: float) -> str:
    size, track = 13.0, 2.08
    return (
        f'<path d="{text_path(main, size, track, x, baseline)}" '
        f'fill="{PAPER}"/>'
    )


def arrow_path(
    x: float, y: float, length: float = 10, color: str = CORAL
) -> str:
    return (
        f'<path d="M{x} {y} h{length} '
        f'M{x + length - 4} {y - 4} l4 4 -4 4" '
        f'stroke="{color}" stroke-width="1.6" fill="none" '
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
    out.append("</svg>")
    return "".join(out)


def projects_svg() -> str:
    out = [svg_open(PROJECTS_W, PROJECTS_H, "Projects")]
    right = PROJECTS_W - MARGIN

    # Left: the section title that introduces the plates.
    out.append(f'<rect x="{MARGIN}" y="41" width="9" height="9" fill="{CORAL}"/>')
    out.append(kicker("PROJECTS", MARGIN + 19, 50))

    # Right: the range of plates, kept quiet so the header has one centre.
    size, track = 10.0, 1.4
    range_text = "01 — 12"
    range_w = text_width(range_text, size, track)
    out.append(
        f'<path d="{text_path(range_text, size, track, right - range_w, 50)}" '
        f'fill="{PAPER}" fill-opacity="0.4"/>'
    )
    out.append(
        f'<rect x="{right - range_w - 19}" y="43" width="5" height="5" '
        f'fill="{CORAL}" fill-opacity="0.7"/>'
    )
    out.append("</svg>")
    return "".join(out)


def try_svg() -> str:
    out = [svg_open(TRY_W, TRY_H, "Try it now: dynamic-dashboard")]
    left, right = 63, 836
    bar_y, bar_h = 1, 36
    centre = bar_y + bar_h / 2

    # A thin outline capsule aligned to the dashboard card above it. It reads
    # as a link, not as another full-width rule.
    out.append(
        f'<rect x="{left}" y="{bar_y}" width="{right - left}" height="{bar_h}" '
        f'rx="{bar_h / 2}" fill="{CORAL}" fill-opacity="0.06" '
        f'stroke="{CORAL}" stroke-opacity="0.5"/>'
    )
    out.append(
        f'<circle cx="{left + 22}" cy="{centre}" r="3.1" fill="{CORAL}">'
        '<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" '
        'repeatCount="indefinite"/></circle>'
    )

    label = "TRY IT NOW"
    label_size, label_track = 10.5, 1.7
    out.append(
        f'<path d="{text_path(label, label_size, label_track, left + 34, 23)}" '
        f'fill="{CORAL}"/>'
    )

    url = "dynamic-dashboard.ednormand.fr"
    url_size, url_track = 10.2, 0.55
    url_w = text_width(url, url_size, url_track)
    arrow_x = right - 20 - 10
    url_x = arrow_x - 14 - url_w
    out.append(
        f'<path d="{text_path(url, url_size, url_track, url_x, 23)}" '
        f'fill="{PAPER}" fill-opacity="0.62"/>'
    )
    out.append(
        f'<g><animateTransform attributeName="transform" type="translate" '
        'values="0 0;4 0;0 0" dur="2.8s" repeatCount="indefinite"/>'
        f'{arrow_path(arrow_x, centre)}</g>'
    )
    out.append("</svg>")
    return "".join(out)


def open_svg() -> str:
    out = [svg_open(OPEN_W, OPEN_H, "Open to work in Switzerland")]
    left, right = 63, 836
    bar_y, bar_h = 1, 36
    centre = bar_y + bar_h / 2

    # A thin capsule with the same weight as the try strip, so the deck gains
    # the signal without another full-width rule.
    out.append(
        f'<rect x="{left}" y="{bar_y}" width="{right - left}" height="{bar_h}" '
        f'rx="{bar_h / 2}" fill="{CORAL}" fill-opacity="0.05" '
        f'stroke="{CORAL}" stroke-opacity="0.38"/>'
    )
    out.append(
        f'<circle cx="{left + 22}" cy="{centre}" r="3.1" fill="{CORAL}">'
        '<animate attributeName="opacity" values="0.35;1;0.35" dur="2.4s" '
        'repeatCount="indefinite"/></circle>'
    )

    label = "OPEN TO WORK"
    label_size, label_track = 10.5, 1.7
    x = left + 34
    out.append(
        f'<path d="{text_path(label, label_size, label_track, x, 23)}" '
        f'fill="{CORAL}"/>'
    )
    x += text_width(label, label_size, label_track) + 9
    out.append(
        f'<path d="{text_path("·", label_size, label_track, x, 23)}" '
        f'fill="{PAPER}" fill-opacity="0.35"/>'
    )
    x += text_width("·", label_size, label_track) + 9
    out.append(
        f'<path d="{text_path("SWITZERLAND", label_size, label_track, x, 23)}" '
        f'fill="{PAPER}" fill-opacity="0.64"/>'
    )

    meta = "SYSTEMS · INFRASTRUCTURE · AI"
    meta_size, meta_track = 9.2, 1.25
    meta_w = text_width(meta, meta_size, meta_track)
    out.append(
        f'<path d="{text_path(meta, meta_size, meta_track, right - 22 - meta_w, 23)}" '
        f'fill="{PAPER}" fill-opacity="0.34"/>'
    )
    out.append("</svg>")
    return "".join(out)


def reviews_svg() -> str:
    card_w = 430
    pad = 22
    quote_size, quote_track, line_h = 11.5, 0.12, 17.5
    attr_size, attr_track = 8.8, 1.2
    mark_size, mark_track = 26.0, 0.12
    mark_w = text_width("“", mark_size, mark_track)
    text_x = pad + mark_w + 8
    text_w = card_w - text_x - pad

    blocks = [
        wrap_text(quote, quote_size, quote_track, text_w)
        for quote, _ in REVIEWS
    ]
    max_lines = max(len(lines) for lines in blocks)
    last_baseline = 40 + (max_lines - 1) * line_h
    hair_y = last_baseline + 23
    attr_y = hair_y + 20
    card_h = attr_y + 14
    height = 56 + card_h + 20

    out = [svg_open(REVIEWS_W, height, "Peer reviews")]
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

    widths = []
    for i, (lines, (_, source)) in enumerate(zip(blocks, REVIEWS)):
        parts = [
            f'<rect x="0" y="0" width="{card_w}" height="{card_h}" rx="14" '
            f'fill="{LIFT}" stroke="{PAPER}" stroke-opacity="0.07"/>',
            f'<rect x="0" y="20" width="3" height="{card_h - 40}" fill="{CORAL}"/>',
            f'<path d="{text_path("“", mark_size, mark_track, pad, 46)}" '
            f'fill="{CORAL}" fill-opacity="0.9"/>',
        ]
        for j, line in enumerate(lines):
            parts.append(
                f'<path d="{text_path(line, quote_size, quote_track, text_x, 40 + j * line_h)}" '
                f'fill="{PAPER}" fill-opacity="0.82"/>'
            )
        parts.append(
            f'<line x1="{pad}" y1="{hair_y}" x2="{card_w - pad}" y2="{hair_y}" '
            f'stroke="{PAPER}" stroke-opacity="0.08"/>'
        )
        parts.append(
            f'<path d="{text_path("— " + source, attr_size, attr_track, pad, attr_y)}" '
            f'fill="{CORAL}" fill-opacity="0.78"/>'
        )
        out.append(f'<g id="rev-{i}">' + "".join(parts) + "</g>")
        widths.append(card_w + 28)
    out.append("</defs>")

    out.append(f'<rect x="{MARGIN}" y="18" width="9" height="9" fill="{CORAL}"/>')
    out.append(kicker("REVIEWS", MARGIN + 19, 28.5))

    row_width = sum(widths)
    row_start = 80.0 - row_width
    duration = row_width / 32.0
    out.append(
        '<g transform="translate(0 56)"><g>'
        '<animateTransform attributeName="transform" type="translate" '
        f'from="{row_start:.2f} 0" to="{row_start - row_width:.2f} 0" '
        f'dur="{duration:.3f}s" repeatCount="indefinite"/>'
    )
    x = 0.0
    for _ in range(3):
        for i, item_w in enumerate(widths):
            out.append(
                f'<use href="#rev-{i}" xlink:href="#rev-{i}" x="{x:.2f}"/>'
            )
            x += item_w
    out.append("</g></g>")

    out.append(
        f'<rect x="0" y="64" width="80" height="{card_h}" fill="url(#revFadeL)"/>'
    )
    out.append(
        f'<rect x="{REVIEWS_W - 80}" y="64" width="80" height="{card_h}" '
        'fill="url(#revFadeR)"/>'
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
.kicker {{
  display: flex; align-items: center; gap: 11px;
  font-size: 13px; font-weight: 500; letter-spacing: 0.16em;
  text-transform: uppercase; color: {PAPER};
}}
.kicker .mark {{ width: 10px; height: 10px; background: {CORAL}; }}
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
    write_rail("deck-projects.svg", projects_svg())
    write_rail("deck-try.svg", try_svg())
    write_rail("deck-open.svg", open_svg())
    write_rail("deck-reviews.svg", reviews_svg())
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
