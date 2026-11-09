#!/usr/bin/env python3
"""Render the two data rails that sit between the header and the project
plates: a two-row technology marquee and a language line.

The strip runs 24 technologies through two full-width rows that scroll in
opposite directions. The icons are Simple Icons paths in the deck's coral; there
is no title, count or active state. The language line reads the same pygount
snapshot (loc.json), keeps only the names in order of use, and puts a three-step
meter beside each one.

Both boards use the deck's ambient palette and type, render high-density, and
stack flush with the header and plates. The marquee is captured at 1.5x and
downscaled to 900 × 126 so the loop stays under a megabyte.

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

FPS = 12.5
LOOP_SECONDS = 10
FRAMES = int(FPS * LOOP_SECONDS)
SCALE = 1.5
OUT_WIDTH = 900
OUT_HEIGHT = 126
COLORS = 32

LANG_DISPLAY = {"Other": "Bash"}
LANG_LEVELS = {
    "TypeScript": 3,
    "JavaScript": 3,
    "Python": 3,
    "C": 3,
    "Java": 2,
    "Go": 2,
    "Bash": 1,
}


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


def marquee_items(row: tuple) -> str:
    items = []
    for label, slug in row:
        path = ICONS[slug]
        items.append(
            '<div class="item">'
            f'<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="{path}"/></svg>'
            f'<span class="name">{label}</span>'
            '<span class="dot"></span></div>'
        )
    return "".join(items) * 2


def strip_document() -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{font_faces()}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{ width: 1200px; font-family: 'Plex Mono', monospace; -webkit-font-smoothing: antialiased; }}
.strip {{
  position: relative;
  width: 1200px; height: 168px;
  display: flex; flex-direction: column; justify-content: center;
  gap: 24px;
  overflow: hidden;
  background: {NAVY};
  color: {PAPER};
}}
.strip::after {{
  content: ''; position: absolute; left: 64px; right: 64px; bottom: 0;
  height: 1px; background: rgba(255, 250, 240, 0.09); z-index: 3;
}}
.row {{ width: 100%; overflow: hidden; }}
.track {{
  display: flex; align-items: center;
  width: max-content;
  will-change: transform;
}}
.item {{
  display: flex; align-items: center; gap: 9px;
  margin-right: 52px;
  white-space: nowrap;
}}
.ico {{
  flex: none;
  width: 22px; height: 22px;
  fill: {CORAL};
  opacity: 0.9;
}}
.name {{
  font-size: 12px; font-weight: 500; letter-spacing: 0.05em;
  line-height: 1; text-transform: uppercase;
  color: {PAPER};
  opacity: 0.66;
}}
.dot {{ width: 3px; height: 3px; background: {CORAL}; opacity: 0.5; }}
.fade {{
  position: absolute; top: 0; bottom: 0; width: 140px; z-index: 2;
  pointer-events: none;
}}
.fade.l {{ left: 0; background: linear-gradient(90deg, {NAVY} 0%, rgba(12, 10, 62, 0.9) 34%, rgba(12, 10, 62, 0) 100%); }}
.fade.r {{ right: 0; background: linear-gradient(270deg, {NAVY} 0%, rgba(12, 10, 62, 0.9) 34%, rgba(12, 10, 62, 0) 100%); }}
</style></head><body>
<div class="strip">
  <div class="row"><div class="track">{marquee_items(ROW_TOP)}</div></div>
  <div class="row"><div class="track">{marquee_items(ROW_BOTTOM)}</div></div>
  <div class="fade l"></div>
  <div class="fade r"></div>
</div>
<script>
const FRAMES = {FRAMES};
const tracks = Array.from(document.querySelectorAll('.track'));
function setFrame(frame) {{
  const t = frame / FRAMES;
  tracks.forEach((track, i) => {{
    const half = track.getBoundingClientRect().width / 2;
    const x = i === 0 ? -t * half : -half + t * half;
    track.style.transform = `translate3d(${{x.toFixed(2)}}px, 0, 0)`;
  }});
}}
</script>
</body></html>"""


def meter(level: int) -> str:
    ticks = "".join(
        f'<span class="tick{" on" if i < level else ""}"></span>'
        for i in range(3)
    )
    return f'<span class="meter">{ticks}</span>'


def language_line(data: dict) -> str:
    items = []
    for i, entry in enumerate(data["languages"]):
        name = LANG_DISPLAY.get(entry["name"], entry["name"])
        alpha = max(0.34, 0.80 - i * 0.075)
        level = LANG_LEVELS.get(name, 1)
        items.append(
            f'<span class="lang" style="color:rgba(255,250,240,{alpha:.2f})">'
            f'{meter(level)}<span class="lname">{name}</span></span>'
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
.langs {{ display: flex; align-items: center; }}
.langs::before {{
  content: ''; flex: 1; height: 1px; margin-right: 26px;
  background: rgba(255, 250, 240, 0.10);
}}
.lang {{
  display: flex; align-items: center; gap: 7px;
  font-size: 11px; font-weight: 500; letter-spacing: 0.07em;
  line-height: 1; text-transform: uppercase; white-space: nowrap;
}}
.lang + .lang {{ margin-left: 26px; }}
.meter {{ display: inline-flex; align-items: center; gap: 2px; }}
.tick {{ width: 5px; height: 2px; background: rgba(255, 250, 240, 0.16); }}
.tick.on {{ background: {CORAL}; opacity: 0.92; }}
.lname {{ line-height: 1; }}
</style></head><body>
<div class="line">
  <div class="pin">
    <div class="kicker"><span class="mark"></span>Languages</div>
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
    scale = f"scale={OUT_WIDTH}:{OUT_HEIGHT}:flags=lanczos"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(frames),
            "-vf", f"{scale},palettegen=max_colors={COLORS}:stats_mode=diff",
            str(palette),
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-framerate", str(FPS), "-i", str(frames), "-i", str(palette),
            "-lavfi", f"{scale},paletteuse=dither=none:diff_mode=rectangle",
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
            device_scale_factor=SCALE,
        )
        render_strip(page)
        assemble_gif()
        render_languages(page, data)
        browser.close()


if __name__ == "__main__":
    main()
