#!/usr/bin/env python3
"""Render the two data rails that sit between the header and the project
plates: an animated technology strip and a language line counter.

The strip lays 24 technologies over four rows — web, data, infra and tools — and
sends a slow diagonal scan across them. The icons are Simple Icons paths in the
deck's coral; the scan only lifts their brightness. The language line reads the
same pygount snapshot (loc.json) and shows only the names, in order of use, so it
signals fluency without turning into a line-count contest.

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
COLS = 6
CELLS = sum(len(row) for row in TECH_ROWS)
FRAMES = 225

LANG_DISPLAY = {"Other": "Bash"}


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
                f'<span class="name">{label}</span></div>'
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
  fill: {CORAL};
  opacity: 0.42;
  will-change: opacity;
}}
.cell .name {{
  overflow: hidden;
  font-size: 11px; font-weight: 500; letter-spacing: 0.03em;
  line-height: 1; text-transform: uppercase; white-space: nowrap;
  color: {PAPER};
  opacity: 0.52;
}}
</style></head><body>
<div class="strip">
  <div class="pin">
    <div class="kicker"><span class="mark"></span>Stack <span class="slash">/</span> Used</div>
    <div class="sub">24 technologies · shipped</div>
  </div>
  <div class="grid">{cells_html()}</div>
</div>
<script>
const COLS = {COLS};
const FRAMES = {FRAMES};
const cells = Array.from(document.querySelectorAll('.cell'));
function setFrame(frame) {{
  const t = frame / FRAMES;
  const u = Math.min(1, t / 0.86);
  const band = -1 + u * 9.5;
  let env;
  if (u < 0.12) env = u / 0.12;
  else if (u > 0.88) env = (1 - u) / 0.12;
  else env = 1;
  cells.forEach((cell, i) => {{
    const col = i % COLS;
    const row = Math.floor(i / COLS);
    const x = col + row * 0.6;
    let prox = 1 - Math.abs(x - band) / 1.5;
    prox = Math.max(0, Math.min(1, prox));
    prox = prox * prox * (3 - 2 * prox);
    const wave = Math.round(prox * env * 16) / 16;
    const ico = cell.querySelector('.ico');
    ico.style.opacity = (0.42 + 0.58 * wave).toFixed(3);
  }});
}}
</script>
</body></html>"""


def language_line(data: dict) -> str:
    items = []
    for i, entry in enumerate(data["languages"]):
        name = LANG_DISPLAY.get(entry["name"], entry["name"])
        alpha = max(0.34, 0.80 - i * 0.075)
        items.append(
            f'<span class="lang" style="color:rgba(255,250,240,{alpha:.2f})">{name}</span>'
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
.kicker .slash {{ color: {CORAL}; }}
.sub {{
  margin-top: 8px;
  font-size: 9.5px; letter-spacing: 0.12em; text-transform: uppercase;
  color: rgba(255, 250, 240, 0.36);
}}
.langs {{ display: flex; align-items: center; }}
.langs::before {{
  content: ''; flex: 1; height: 1px; margin-right: 26px;
  background: rgba(255, 250, 240, 0.10);
}}
.lang {{
  font-size: 11px; font-weight: 500; letter-spacing: 0.07em;
  line-height: 1; text-transform: uppercase; white-space: nowrap;
}}
.lang + .lang {{ margin-left: 28px; }}
</style></head><body>
<div class="line">
  <div class="pin">
    <div class="kicker"><span class="mark"></span>Languages <span class="slash">/</span> Confident</div>
    <div class="sub">most used first</div>
  </div>
  <div class="langs">{language_line(data)}</div>
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
            "-vf", "palettegen=max_colors=64:stats_mode=diff",
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
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 168},
            device_scale_factor=2,
        )
        render_strip(page)
        assemble_gif()
        render_languages(page, data)
        browser.close()


if __name__ == "__main__":
    main()
