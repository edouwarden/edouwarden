#!/usr/bin/env python3
"""Render the image-only profile README.

Every panel is a 1200 px wide HTML artboard rendered at 2x through Playwright,
then stacked in README.md with <img align="top"> so the plates touch without a
single pixel of gap. Run from the repository root:

    python assets/readme/build.py

Palette and type come from the portfolio's ambient edition:
navy #0c0a3e, coral #f9564f, paper #fffaf0, Days One + IBM Plex Mono.
"""

from __future__ import annotations

import html
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / ".build"
WIDTH = 1200
SCALE = 2

NAVY = "#0c0a3e"
NAVY_LIFT = "#17134f"
CORAL = "#f9564f"
CORAL_DEEP = "#dd453d"
RED_DEEP = "#c9332d"
RED_DARK = "#7d1a17"
PAPER = "#fffaf0"

PROJECTS = [
    {
        "n": "01",
        "slug": "01-transcendence",
        "title": "ft_transcendence",
        "year": "2026",
        "role": "Team lead · engine &amp; frontend",
        "summary": (
            "A real-time browser battle royale: one life each, a custom "
            "Three.js engine, and a Go backend. Four people, five containers "
            "behind nginx, 2,000+ players served."
        ),
        "stack": "TypeScript · Next.js · Three.js · Go · PostgreSQL",
    },
    {
        "n": "02",
        "slug": "02-minishell",
        "title": "minishell",
        "year": "2025",
        "role": "Pair · C99 · POSIX",
        "summary": (
            "Bash rebuilt from scratch: lexing, expansion, pipes, "
            "redirections, signals, and heredocs. No system(), no shell "
            "library — readline only for line editing."
        ),
        "stack": "C · POSIX · Processes · Readline",
    },
    {
        "n": "03",
        "slug": "03-cub3d",
        "title": "cub3D",
        "year": "2025",
        "role": "Pair · bonus",
        "summary": (
            "A first-person raycast from a 2D map, textured floor to ceiling, "
            "every pixel written by hand into an X11 buffer. No GPU, and the "
            "map file carries the whole scene."
        ),
        "stack": "C · Raycasting · X11 · Math",
    },
    {
        "n": "04",
        "slug": "04-irc",
        "title": "ft_irc",
        "year": "2026",
        "role": "Pair · bonus",
        "summary": (
            "An IRC server on one thread and one poll() loop: registration, "
            "channels, private messages, clean disconnects — plus a local "
            "Phi-3 answering in #ai\u2011lab."
        ),
        "stack": "C++98 · Sockets · poll() · Local LLM",
    },
    {
        "n": "05",
        "slug": "05-inception",
        "title": "Inception",
        "year": "2026",
        "role": "Solo · Docker",
        "summary": (
            "A WordPress stack where every part is a container and exactly "
            "one port faces the internet. nginx holds TLS, MariaDB never "
            "leaves the compose network."
        ),
        "stack": "Docker · Compose · nginx · MariaDB · WordPress",
    },
    {
        "n": "06",
        "slug": "06-born2beroot",
        "title": "born2beroot",
        "year": "2024",
        "role": "Solo · Debian",
        "summary": (
            "A reproducible hardened Debian VM: LUKS + LVM, one SSH port, "
            "AppArmor, UFW, and every security setting stored in the repo. "
            "The ISO is the build artifact."
        ),
        "stack": "Debian · LUKS · LVM · AppArmor · UFW",
    },
]

PLATE_HEIGHT = 400
HEADER_HEIGHT = 720
FOOTER_HEIGHT = 460

CSS = f"""
@font-face {{
  font-family: 'Days One';
  src: url('../fonts/days-one-v1.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}}
@font-face {{
  font-family: 'Plex Mono';
  src: url('../fonts/ibm-plex-mono-400-v1.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}}
@font-face {{
  font-family: 'Plex Mono';
  src: url('../fonts/ibm-plex-mono-500-v1.woff2') format('woff2');
  font-weight: 500;
  font-style: normal;
}}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
  width: {WIDTH}px;
  font-family: 'Plex Mono', monospace;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}}

.board {{
  position: relative;
  width: {WIDTH}px;
  overflow: hidden;
}}

/* ── Header ─────────────────────────────────────────────────────────── */

.header {{
  height: {HEADER_HEIGHT}px;
  padding: 40px 64px 34px;
  display: grid;
  grid-template-rows: auto 1fr auto;
  background: {NAVY};
  color: {PAPER};
}}

.topline,
.bottomline {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}}
.topline {{ color: rgba(255, 250, 240, 0.62); }}
.topline b {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
  color: {PAPER};
}}
.topline .mark {{
  width: 12px;
  height: 12px;
  background: {CORAL};
}}
.topline .slash {{ color: {CORAL}; }}

.hero {{
  display: grid;
  grid-template-columns: minmax(0, 1fr) 330px;
  gap: 48px;
  align-items: start;
  padding-top: 34px;
}}

.wordmark {{
  margin: 0;
  font-family: 'Days One', 'Arial Black', sans-serif;
  font-size: 120px;
  font-weight: 400;
  line-height: 0.84;
  letter-spacing: -0.03em;
  text-transform: uppercase;
  color: {CORAL};
  white-space: nowrap;
}}
.wordmark span {{ display: block; }}
.wordmark span + span {{ margin-top: 6px; }}
.wordmark span {{
  text-shadow:
    0.012em 0.012em 0 {RED_DEEP},
    0.024em 0.024em 0 {RED_DEEP},
    0.036em 0.036em 0 {RED_DEEP},
    0.048em 0.048em 0 {RED_DEEP},
    0.060em 0.060em 0 {RED_DARK},
    0.072em 0.072em 0 {RED_DARK},
    0.084em 0.084em 0 {RED_DARK},
    0.096em 0.096em 0 {RED_DARK};
}}

.lede {{
  max-width: 610px;
  margin: 42px 0 0;
  font-size: 23px;
  line-height: 1.5;
  color: rgba(255, 250, 240, 0.9);
}}
.lede strong {{ color: {PAPER}; font-weight: 500; }}

.pill {{
  display: inline-flex;
  align-items: center;
  gap: 12px;
  margin-top: 34px;
  padding: 15px 22px 14px;
  border-radius: 999px;
  background: {CORAL};
  color: {NAVY};
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}}
.pill i {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: {NAVY};
}}

.portrait {{
  position: relative;
  width: 320px;
  height: 320px;
  justify-self: end;
}}
.portrait img {{
  display: block;
  width: 320px;
  height: 320px;
}}
.portrait::after {{
  content: '';
  position: absolute;
  inset: -14px;
  border: 4px solid {CORAL};
  border-radius: 50%;
}}
.handle {{
  margin-top: 24px;
  text-align: right;
  font-size: 13px;
  letter-spacing: 0.14em;
  color: rgba(255, 250, 240, 0.72);
}}
.handle b {{ color: {CORAL}; font-weight: 500; }}

.stats {{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 22px 26px;
  margin: 34px 0 0;
}}
.stats div {{ display: flex; flex-direction: column; gap: 3px; }}
.stats dt {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Days One', sans-serif;
  font-size: 27px;
  line-height: 1;
  color: {PAPER};
}}
.stats dt::before {{
  content: '';
  flex: none;
  width: 8px;
  height: 8px;
  background: {CORAL};
}}
.stats dd {{
  margin: 0;
  font-size: 11px;
  letter-spacing: 0.12em;
  line-height: 1.35;
  text-transform: uppercase;
  color: rgba(255, 250, 240, 0.6);
}}

.bottomline {{
  padding-top: 20px;
  border-top: 1px solid rgba(255, 250, 240, 0.18);
  color: rgba(255, 250, 240, 0.66);
}}
.bottomline .say {{ color: {PAPER}; }}
.bottomline .arrow {{ color: {CORAL}; }}

/* ── Project plates ─────────────────────────────────────────────────── */

.plate {{
  height: {PLATE_HEIGHT}px;
  padding: 34px 84px;
  background: {NAVY};
}}
.plate .card {{
  position: relative;
  height: 100%;
  padding: 34px 42px;
  overflow: hidden;
  border-radius: 30px;
  background: {CORAL};
  color: {NAVY};
}}
.plate .ghost {{
  position: absolute;
  right: 14px;
  bottom: -54px;
  font-family: 'Days One', sans-serif;
  font-size: 230px;
  line-height: 1;
  color: rgba(12, 10, 62, 0.08);
}}
.plate .inner {{
  position: relative;
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr) 180px;
  gap: 22px;
  align-items: start;
  height: 100%;
}}
.plate .num {{
  display: grid;
  place-items: center;
  width: 56px;
  height: 56px;
  border-radius: 8px;
  background: #ffffff;
  color: {NAVY};
  font-family: 'Days One', sans-serif;
  font-size: 22px;
}}
.plate .title {{
  margin: -4px 0 0;
  font-family: 'Days One', sans-serif;
  font-size: 58px;
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.02em;
  color: {NAVY};
}}
.plate .meta {{
  margin: 12px 0 0;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(12, 10, 62, 0.62);
}}
.plate .body {{
  display: flex;
  flex-direction: column;
  height: 100%;
}}
.plate .summary {{
  max-width: 690px;
  margin: 16px 0 0;
  font-size: 20px;
  line-height: 1.45;
  color: rgba(12, 10, 62, 0.86);
}}
.plate .stack {{
  margin: auto 0 0;
  padding-top: 14px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: {NAVY};
}}
.plate .stack span {{ color: rgba(12, 10, 62, 0.45); }}
.plate .side {{
  align-self: end;
  justify-self: end;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 14px;
}}
.plate .repo {{
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(12, 10, 62, 0.66);
}}
.plate .go {{
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: #ffffff;
  color: {NAVY};
  font-family: 'Days One', sans-serif;
  font-size: 24px;
}}
.plate .year {{
  position: absolute;
  top: 34px;
  right: 42px;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.16em;
  color: rgba(12, 10, 62, 0.55);
}}

/* ── Footer ─────────────────────────────────────────────────────────── */

.footer {{
  height: {FOOTER_HEIGHT}px;
  padding: 58px 64px 34px;
  display: grid;
  grid-template-rows: 1fr auto;
  background: {NAVY};
  color: {PAPER};
}}
.footer .big {{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 40px;
}}
.footer h2 {{
  margin: 0;
  font-family: 'Days One', sans-serif;
  font-size: 104px;
  font-weight: 400;
  line-height: 0.9;
  letter-spacing: -0.03em;
  text-transform: uppercase;
  color: {CORAL};
  white-space: nowrap;
}}
.footer .cta {{
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 14px;
  padding-top: 8px;
}}
.footer .cta .label {{
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(255, 250, 240, 0.6);
}}
.footer .cta .link {{
  display: inline-flex;
  align-items: center;
  gap: 14px;
  padding: 17px 24px 16px;
  border-radius: 999px;
  background: {PAPER};
  color: {NAVY};
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.04em;
}}
.footer .cta .link b {{ color: {CORAL_DEEP}; }}
.footer .footline {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 22px;
  border-top: 1px solid rgba(255, 250, 240, 0.18);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(255, 250, 240, 0.6);
}}
.footer .footline b {{ color: {PAPER}; font-weight: 500; }}
"""


def header() -> str:
    return f"""
<div class="board header">
  <div class="topline">
    <b><span class="mark"></span> Edouard Normand <span class="slash">/</span> Profile</b>
    <span>Paris, France · 42 Paris</span>
  </div>

  <div class="hero">
    <div>
      <h1 class="wordmark"><span>Edouard</span><span>Normand</span></h1>
      <p class="lede">
        Software engineer at <strong>42 Paris</strong>. I build systems end to
        end — bare metal, networks, engines, and AI agents. Hard constraints,
        small surfaces, nothing wasted.
      </p>
      <div class="pill"><i></i> Open to hard problems</div>
    </div>

    <div>
      <div class="portrait"><img src="../portrait-disc.png" alt=""></div>
      <div class="handle"><b>@edouwarden</b> &nbsp;↗</div>
      <dl class="stats">
        <div><dt>13 yrs</dt><dd>Coding since nine</dd></div>
        <div><dt>2,000+</dt><dd>Players served</dd></div>
        <div><dt>214</dt><dd>Peer reviews</dd></div>
        <div><dt>€0</dt><dd>Infra bill</dd></div>
      </dl>
    </div>
  </div>

  <div class="bottomline">
    <span class="say">github.com/edouwarden</span>
    <span>Selected work &nbsp;<span class="arrow">↓</span></span>
  </div>
</div>
"""


def plate(project: dict) -> str:
    return f"""
<div class="board plate">
  <div class="card">
    <div class="ghost">{project['n']}</div>
    <div class="year">{project['year']}</div>
    <div class="inner">
      <div class="num">{project['n']}</div>
      <div class="body">
        <h2 class="title">{project['title']}</h2>
        <p class="meta">{project['role']}</p>
        <p class="summary">{project['summary']}</p>
        <p class="stack">{project['stack'].replace(' · ', ' <span>·</span> ')}</p>
      </div>
      <div class="side">
        <span class="repo">Open repo</span>
        <span class="go">↗</span>
      </div>
    </div>
  </div>
</div>
"""


def footer() -> str:
    return f"""
<div class="board footer">
  <div class="big">
    <h2>Let's build<br>something.</h2>
    <div class="cta">
      <span class="label">No forms, no trackers</span>
      <span class="link">github.com/edouwarden &nbsp;<b>↗</b></span>
    </div>
  </div>
  <div class="footline">
    <span><b>Open to hard problems</b> · Paris, FR · 42 Paris</span>
    <span>Systems · Infrastructure · AI</span>
  </div>
</div>
"""


def portrait() -> None:
    """Cut the source portrait into a soft-edged disc so it sits on navy."""
    source = ROOT / "portrait-source.jpg"
    target = ROOT / "portrait-disc.png"
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime:
        return

    image = Image.open(source).convert("RGBA")
    width, height = image.size
    cx, cy = width / 2, height / 2
    inner, outer = 468, 506
    alpha = Image.new("L", (width, height), 0)
    pixels = alpha.load()
    for y in range(height):
        for x in range(width):
            distance = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if distance <= inner:
                value = 255
            elif distance >= outer:
                value = 0
            else:
                value = int(255 * (outer - distance) / (outer - inner))
            pixels[x, y] = value
    image.putalpha(alpha)
    image.save(target)
    print("rendered portrait-disc.png")


def render() -> None:
    portrait()
    BUILD.mkdir(exist_ok=True)
    boards = [("00-header", HEADER_HEIGHT, header())]
    for project in PROJECTS:
        boards.append((project["slug"], PLATE_HEIGHT, plate(project)))
    boards.append(("07-footer", FOOTER_HEIGHT, footer()))

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": WIDTH, "height": HEADER_HEIGHT},
            device_scale_factor=SCALE,
        )
        for name, height, body in boards:
            page.set_viewport_size({"width": WIDTH, "height": height})
            doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>{CSS}</style></head>
<body>{body}</body></html>"""
            path = BUILD / f"{name}.html"
            path.write_text(doc)
            page.goto(path.as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.screenshot(
                path=str(ROOT / f"{name}.png"),
                clip={"x": 0, "y": 0, "width": WIDTH, "height": height},
            )
            print(f"rendered {name}.png")
        browser.close()


if __name__ == "__main__":
    render()
