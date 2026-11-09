#!/usr/bin/env python3
"""Prototype: one proof plate for the profile deck.

This is a standalone experiment. It does not touch the eight production
plates or README.md. It renders a single 1200 x 400 plate for
ft_transcendence with a real gameplay capture duotoned into the ambient
palette, a one-line hook, and three scannable specs.

Run from anywhere:

    python assets/readme/prototype/plate.py

Output: plate.png next to this script.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
ARTIFACT = HERE / "artifact-01.png"
BUILD = HERE.parent / ".build"

HTML = f"""
<!doctype html><html><head><meta charset="utf-8"><style>
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

.plate {{
  width: 1200px;
  height: 400px;
  padding: 34px 84px;
  background: #0c0a3e;
}}
.card {{
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 32px;
  height: 100%;
  padding: 30px 36px;
  border-radius: 30px;
  background: #f9564f;
  color: #0c0a3e;
  overflow: hidden;
}}

.copy {{ display: flex; flex-direction: column; min-width: 0; }}

.head {{ display: flex; align-items: center; gap: 18px; }}
.num {{
  display: grid;
  place-items: center;
  flex: none;
  width: 54px;
  height: 54px;
  border-radius: 10px;
  background: #ffffff;
  font-family: 'Days One', sans-serif;
  font-size: 21px;
}}
.title {{
  margin: 0;
  font-family: 'Days One', sans-serif;
  font-size: 46px;
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.02em;
}}
.meta {{
  margin: 14px 0 0;
  font-size: 10.5px;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: rgba(12, 10, 62, 0.62);
}}
.hook {{
  max-width: 500px;
  margin: 14px 0 0;
  font-size: 18px;
  line-height: 1.5;
  color: rgba(12, 10, 62, 0.88);
}}

.specs {{
  display: flex;
  gap: 26px;
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid rgba(12, 10, 62, 0.24);
}}
.spec {{ display: flex; flex-direction: column; gap: 2px; }}
.spec b {{
  display: flex;
  align-items: center;
  gap: 7px;
  font-family: 'Days One', sans-serif;
  font-size: 22px;
  font-weight: 400;
  line-height: 1;
}}
.spec b::before {{
  content: '';
  width: 6px;
  height: 6px;
  background: #0c0a3e;
}}
.spec span {{
  font-size: 8.5px;
  font-weight: 500;
  letter-spacing: 0.13em;
  text-transform: uppercase;
  color: rgba(12, 10, 62, 0.6);
}}
.stack {{
  margin: 12px 0 0;
  font-size: 9px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(12, 10, 62, 0.5);
}}

.art {{ position: relative; align-self: center; }}
.art img {{
  display: block;
  width: 360px;
  height: 203px;
  border-radius: 16px;
  object-fit: cover;
}}
.art .go {{
  position: absolute;
  right: -13px;
  bottom: -13px;
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: #ffffff;
  font-family: 'Days One', sans-serif;
  font-size: 19px;
}}
</style></head><body>
<div class="plate">
  <div class="card">
    <div class="copy">
      <div class="head">
        <div class="num">01</div>
        <h2 class="title">ft_transcendence</h2>
      </div>
      <p class="meta">2026 · Team lead · Engine &amp; frontend</p>
      <p class="hook">One life each in a shrinking arena — a custom Three.js engine and a Go backend.</p>
      <div class="specs">
        <div class="spec"><b>2,000+</b><span>players served</span></div>
        <div class="spec"><b>05</b><span>containers</span></div>
        <div class="spec"><b>04</b><span>builders</span></div>
      </div>
      <p class="stack">TypeScript · Next.js · Three.js · Go · PostgreSQL</p>
    </div>
    <div class="art">
      <img src="file://{ARTIFACT}" alt="">
      <span class="go">↗</span>
    </div>
  </div>
</div>
</body></html>
"""


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    page_path = BUILD / "prototype-plate.html"
    page_path.write_text(HTML)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 400},
            device_scale_factor=2,
        )
        page.goto(page_path.as_uri())
        page.wait_for_function("document.fonts.status === 'loaded'")
        page.screenshot(
            path=str(HERE / "plate.png"),
            clip={"x": 0, "y": 0, "width": 1200, "height": 400},
        )
        browser.close()
    print("rendered prototype/plate.png")


if __name__ == "__main__":
    main()
