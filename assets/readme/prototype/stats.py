#!/usr/bin/env python3
"""Render the two data rails that sit between the header and the project
plates: an animated technology strip and a language line counter.

The strip is a 24-cell sequencer over four rows — web, data, infra and tools —
using monochrome Simple Icons paths recoloured to the deck palette. The counter
reads a pygount snapshot of every public repository (loc.json) and draws a
stacked bar plus a legend, with HTML and CSS left out of the code total.

Both boards use the deck's ambient palette and type, render at 2x, and stack
flush with the header and plates.

    python3 assets/readme/prototype/stats.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
BUILD = HERE.parent / ".build" / "stats"

NAVY = "#0c0a3e"
CORAL = "#f9564f"
DEEP = "#dd453d"
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

ICONS = json.loads((HERE / "tech-icons.json").read_text())

FPS = 25
FRAMES_PER_CELL = 4
CELLS = sum(len(row) for row in TECH_ROWS)
FRAMES = CELLS * FRAMES_PER_CELL

SEGMENT_FILL = (
    (CORAL, 1.0),
    (CORAL, 0.62),
    (PAPER, 0.92),
    (PAPER, 0.72),
    (PAPER, 0.56),
    (PAPER, 0.42),
    (PAPER, 0.28),
)


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


def cells_html() -> str:
    cells = []
    for row in TECH_ROWS:
        for label, slug in row:
            path = ICONS[slug]
            cells.append(
                '<div class="cell">'
                f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="{path}"/></svg>'
                f'<span class="name">{label}</span>'
                '<span class="bar"></span></div>'
            )
    return "".join(cells)


def strip_document() -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_faces()}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: 1200px; font-family: 'Plex Mono', monospace; -webkit-font-smoothing: antialiased; }}
.strip {{
  position: relative;
  width: 1200px; height: 168px;
  padding: 0 64px;
  display: grid;
  grid-template-columns: 232px minmax(0, 1fr);
  align-items: center;
  background: {NAVY};
  color: {PAPER};
}}
.strip::after {{
  content: ''; position: absolute; left: 64px; right: 64px; bottom: 0;
  height: 1px; background: rgba(255, 250, 240, 0.09);
}}
.kicker {{
  display: flex; align-items: center; gap: 11px;
  font-size: 13px; font-weight: 500; letter-spacing: 0.16em;
  text-transform: uppercase; color: {PAPER};
}}
.kicker .mark {{ width: 10px; height: 10px; background: {CORAL}; }}
.kicker .slash {{ color: {CORAL}; }}
.sub {{
  margin-top: 9px;
  font-size: 9.5px; letter-spacing: 0.12em; text-transform: uppercase;
  color: rgba(255, 250, 240, 0.36);
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  column-gap: 22px;
  grid-auto-rows: 36px;
}}
.cell {{
  position: relative;
  display: flex; align-items: center; gap: 7px;
  min-width: 0;
  border-bottom: 1px solid rgba(255, 250, 240, 0.13);
}}
.ico {{
  flex: none;
  width: 18px; height: 18px;
  fill: rgba(255, 250, 240, 0.52);
}}
.cell .name {{
  overflow: hidden;
  font-size: 11px; font-weight: 500; letter-spacing: 0.03em;
  line-height: 1; text-transform: uppercase; white-space: nowrap;
  color: rgba(255, 250, 240, 0.52);
}}
.cell .bar {{
  position: absolute; left: 0; right: 0; bottom: -1px; height: 2px;
  background: {CORAL};
  transform: scaleX(0); transform-origin: left;
}}
.cell.on .ico {{ fill: {CORAL}; }}
.cell.on .name {{ color: {PAPER}; }}
</style></head><body>
<div class="strip">
  <div class="pin">
    <div class="kicker"><span class="mark"></span>Stack <span class="slash">/</span> Used</div>
    <div class="sub">24 technologies · shipped</div>
  </div>
  <div class="grid">{cells_html()}</div>
</div>
<script>
const cells = Array.from(document.querySelectorAll('.cell'));
function setFrame(frame) {{
  const active = Math.floor(frame / {FRAMES_PER_CELL}) % {CELLS};
  const phase = (frame % {FRAMES_PER_CELL} + 1) / {FRAMES_PER_CELL};
  cells.forEach((cell, i) => {{
    cell.classList.toggle('on', i === active);
    const bar = cell.querySelector('.bar');
    bar.style.transform = i === active ? `scaleX(${{phase}})` : 'scaleX(0)';
  }});
}}
</script>
</body></html>"""


def legend(data: dict) -> str:
    items = []
    for i, entry in enumerate(data["languages"]):
        color, opacity = SEGMENT_FILL[i]
        items.append(
            f'<div class="lang"><span class="chip" style="background:{color};opacity:{opacity}"></span>'
            f'<span class="lname">{entry["name"]}</span>'
            f'<span class="lcount">{entry["lines"]:,}</span></div>'
        )
    return "".join(items)


def bar(data: dict) -> str:
    total = data["total"]
    spans = []
    for i, entry in enumerate(data["languages"]):
        color, opacity = SEGMENT_FILL[i]
        width = entry["lines"] / total * 100
        spans.append(
            f'<span style="width:{width:.3f}%;background:{color};opacity:{opacity}"></span>'
        )
    return "".join(spans)


def lang_document(data: dict) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_faces()}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: 1200px; font-family: 'Plex Mono', monospace; -webkit-font-smoothing: antialiased; }}
.card {{
  position: relative;
  width: 1200px; height: 178px;
  padding: 20px 64px 16px;
  display: grid;
  grid-template-columns: 300px minmax(0, 1fr);
  grid-template-rows: auto 1fr auto;
  column-gap: 48px;
  background: {NAVY};
  color: {PAPER};
  border-bottom: 1px solid rgba(255, 250, 240, 0.09);
}}
.top {{
  grid-column: 1 / -1;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 12px; font-weight: 500; letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 250, 240, 0.72);
}}
.top .left {{ display: flex; align-items: center; gap: 11px; color: {PAPER}; }}
.top .mark {{ width: 10px; height: 10px; background: {CORAL}; }}
.top .slash {{ color: {CORAL}; }}
.top .meta {{ color: rgba(255, 250, 240, 0.36); }}
.total {{ align-self: center; }}
.total b {{
  display: block;
  margin-top: 4px;
  font-family: 'Days One', sans-serif; font-size: 62px; font-weight: 400;
  line-height: 0.95; letter-spacing: -0.02em; color: {CORAL};
}}
.total span {{
  display: block; margin-top: 9px;
  font-size: 10px; font-weight: 500; letter-spacing: 0.15em;
  text-transform: uppercase; color: rgba(255, 250, 240, 0.44);
}}
.note {{
  grid-column: 1 / -1;
  align-self: end;
  padding-top: 7px;
  border-top: 1px solid rgba(255, 250, 240, 0.08);
  font-size: 8.5px; letter-spacing: 0.04em; line-height: 1.4;
  color: rgba(255, 250, 240, 0.28);
}}
.detail {{ align-self: center; }}
.bar {{
  display: flex; gap: 2px;
  width: 100%; height: 13px;
  overflow: hidden; border-radius: 2px;
}}
.bar span {{ display: block; height: 100%; }}
.legend {{
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  column-gap: 26px;
  row-gap: 9px;
  margin-top: 16px;
}}
.lang {{ display: flex; align-items: baseline; gap: 7px; min-width: 0; }}
.chip {{ flex: none; width: 7px; height: 7px; transform: translateY(-1px); }}
.lname {{
  overflow: hidden; text-overflow: ellipsis;
  font-size: 9.5px; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(255, 250, 240, 0.65); white-space: nowrap;
}}
.lcount {{ margin-left: auto; font-size: 9.5px; color: rgba(255, 250, 240, 0.4); }}
</style></head><body>
<div class="card">
  <div class="top">
    <div class="left"><span class="mark"></span>Lines <span class="slash">/</span> of code</div>
    <div class="meta">Across {data['repos']} public repositories</div>
  </div>
  <div class="total">
    <b>{data['total']:,}</b>
    <span>lines · html and css excluded</span>
  </div>
  <div class="detail">
    <div class="bar">{bar(data)}</div>
    <div class="legend">{legend(data)}</div>
  </div>
  <div class="note">{data['note']}</div>
</div>
</body></html>"""


def render_strip(page) -> None:
    page.set_viewport_size({"width": 1200, "height": 168})
    board = BUILD / "strip.html"
    board.write_text(strip_document())
    page.goto(board.as_uri())
    page.wait_for_function("document.fonts.status === 'loaded'")
    frames = BUILD / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True)
    for frame in range(FRAMES):
        page.evaluate("(frame) => setFrame(frame)", frame)
        page.screenshot(
            path=str(frames / f"frame-{frame:03d}.png"),
            clip={"x": 0, "y": 0, "width": 1200, "height": 168},
        )
    print(f"rendered {FRAMES} strip frames")


def assemble_gif() -> None:
    out = HERE / "deck-stack.gif"
    palette = BUILD / "palette.png"
    frames = BUILD / "frames" / "frame-%03d.png"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(frames),
            "-vf", "palettegen=max_colors=128:stats_mode=diff",
            str(palette),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(frames), "-i", str(palette),
            "-lavfi", "paletteuse=dither=none:diff_mode=rectangle",
            "-loop", "0", str(out),
        ],
        check=True,
    )
    subprocess.run(["gifsicle", "-O3", "--careful", str(out), "-o", str(out)], check=True)
    print(f"wrote {out.name} ({out.stat().st_size / 1024:.0f} KiB)")


def render_languages(page, data: dict) -> None:
    page.set_viewport_size({"width": 1200, "height": 178})
    board = BUILD / "languages.html"
    board.write_text(lang_document(data))
    page.goto(board.as_uri())
    page.wait_for_function("document.fonts.status === 'loaded'")
    page.screenshot(
        path=str(HERE / "deck-languages.png"),
        clip={"x": 0, "y": 0, "width": 1200, "height": 178},
    )
    print("wrote deck-languages.png")


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    data = json.loads((HERE / "loc.json").read_text())
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 178},
            device_scale_factor=2,
        )
        render_strip(page)
        assemble_gif()
        render_languages(page, data)
        browser.close()


if __name__ == "__main__":
    main()
