#!/usr/bin/env python3
"""Two proof-plate variants for dynamic-dashboard.

A: a custom flat illustration of the dashboard shell, drawn as inline SVG in
   the ambient palette.
B: the same card with a real screenshot of the Personal OS tab.

Both keep the card, type, and specs identical so only the visual changes.
Standalone: production README and build.py are untouched.

    python3 assets/readme/prototype/plates.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
BUILD = HERE.parent / ".build"
ARTIFACT_B = HERE / "artifact-b.png"

ILLUSTRATION = """
<svg viewBox="0 0 360 203" width="360" height="203" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c0a3e"/>
      <stop offset="1" stop-color="#17134f"/>
    </linearGradient>
    <radialGradient id="glow" cx=".5" cy=".5" r=".5">
      <stop offset="0" stop-color="#f9564f" stop-opacity=".22"/>
      <stop offset="1" stop-color="#f9564f" stop-opacity="0"/>
    </radialGradient>
    <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r=".7" fill="#fffaf0" opacity=".07"/>
    </pattern>
  </defs>

  <rect width="360" height="203" fill="url(#sky)"/>
  <rect width="360" height="203" fill="url(#dots)"/>
  <circle cx="304" cy="30" r="104" fill="url(#glow)"/>
  <circle cx="42" cy="186" r="76" fill="#f9564f" opacity=".06"/>

  <rect x="14" y="16" width="332" height="174" rx="13" fill="#f9564f" opacity=".16"/>

  <g>
    <rect x="16" y="18" width="328" height="170" rx="12" fill="#17134f" stroke="#fffaf0" stroke-opacity=".16"/>
    <path d="M16,30 a12,12 0 0 1 12,-12 h304 a12,12 0 0 1 12,12 v6 h-328 z" fill="#0c0a3e"/>
    <line x1="16" y1="36" x2="344" y2="36" stroke="#fffaf0" stroke-opacity=".1"/>
    <circle cx="27" cy="27" r="2.6" fill="#f9564f"/>
    <circle cx="35" cy="27" r="2.6" fill="#dd453d"/>
    <circle cx="43" cy="27" r="2.6" fill="#fffaf0" opacity=".5"/>
    <rect x="286" y="22" width="46" height="10" rx="5" fill="#f9564f"/>
    <circle cx="293" cy="27" r="1.8" fill="#0c0a3e"/>
    <rect x="299" y="25.5" width="24" height="3" rx="1.5" fill="#0c0a3e" opacity=".6"/>
  </g>

  <rect x="16" y="36" width="56" height="152" fill="#0c0a3e" opacity=".55"/>
  <line x1="72" y1="36" x2="72" y2="188" stroke="#fffaf0" stroke-opacity=".08"/>
  <rect x="24" y="46" width="40" height="12" rx="6" fill="#f9564f"/>
  <rect x="30" y="50.5" width="21" height="3" rx="1.5" fill="#0c0a3e"/>
  <g fill="#fffaf0" opacity=".2">
    <rect x="24" y="66" width="34" height="7" rx="3.5"/>
    <rect x="24" y="82" width="34" height="7" rx="3.5"/>
    <rect x="24" y="98" width="34" height="7" rx="3.5"/>
    <rect x="24" y="114" width="34" height="7" rx="3.5"/>
    <rect x="24" y="130" width="34" height="7" rx="3.5"/>
  </g>
  <circle cx="44" cy="172" r="9" fill="#f9564f"/>
  <path d="M40,172 h8 M44,168 v8" stroke="#0c0a3e" stroke-width="1.6" stroke-linecap="round"/>

  <g>
    <rect x="82" y="46" width="112" height="64" rx="7" fill="#0c0a3e" stroke="#f9564f" stroke-width="1.2"/>
    <rect x="88" y="52" width="34" height="4" rx="2" fill="#fffaf0" opacity=".38"/>
    <rect x="88" y="52" width="10" height="4" rx="2" fill="#f9564f"/>
    <g>
      <rect x="88" y="64" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="104" y="64" width="14" height="8" rx="1.5" fill="#f9564f"/>
      <rect x="120" y="64" width="14" height="8" rx="1.5" fill="#dd453d"/>
      <rect x="136" y="64" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="152" y="64" width="14" height="8" rx="1.5" fill="#fffaf0" opacity=".28"/>
      <rect x="168" y="64" width="14" height="8" rx="1.5" fill="#f9564f"/>

      <rect x="88" y="75" width="14" height="8" rx="1.5" fill="#dd453d"/>
      <rect x="104" y="75" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="120" y="75" width="14" height="8" rx="1.5" fill="#f9564f"/>
      <rect x="136" y="75" width="14" height="8" rx="1.5" fill="#fffaf0" opacity=".28"/>
      <rect x="152" y="75" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="168" y="75" width="14" height="8" rx="1.5" fill="#dd453d"/>

      <rect x="88" y="86" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="104" y="86" width="14" height="8" rx="1.5" fill="#f9564f"/>
      <rect x="120" y="86" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="136" y="86" width="14" height="8" rx="1.5" fill="#dd453d"/>
      <rect x="152" y="86" width="14" height="8" rx="1.5" fill="#f9564f"/>
      <rect x="168" y="86" width="14" height="8" rx="1.5" fill="#17134f"/>

      <rect x="88" y="97" width="14" height="8" rx="1.5" fill="#fffaf0" opacity=".28"/>
      <rect x="104" y="97" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="120" y="97" width="14" height="8" rx="1.5" fill="#dd453d"/>
      <rect x="136" y="97" width="14" height="8" rx="1.5" fill="#17134f"/>
      <rect x="152" y="97" width="14" height="8" rx="1.5" fill="#f9564f"/>
      <rect x="168" y="97" width="14" height="8" rx="1.5" fill="#17134f"/>
    </g>
    <rect x="166" y="95" width="8" height="8" rx="1.5" fill="none" stroke="#fffaf0" stroke-width="1.4"/>
  </g>

  <g>
    <rect x="202" y="46" width="64" height="64" rx="7" fill="#f9564f"/>
    <rect x="210" y="54" width="22" height="3.5" rx="1.75" fill="#0c0a3e" opacity=".5"/>
    <text x="210" y="86" font-family="'Days One', sans-serif" font-size="25" fill="#0c0a3e">7.4</text>
    <rect x="210" y="94" width="42" height="3" rx="1.5" fill="#0c0a3e" opacity=".32"/>
    <rect x="210" y="100" width="28" height="3" rx="1.5" fill="#0c0a3e" opacity=".22"/>
  </g>

  <g>
    <rect x="274" y="46" width="62" height="64" rx="7" fill="#0c0a3e" stroke="#fffaf0" stroke-opacity=".16"/>
    <g stroke="#fffaf0" stroke-opacity=".1">
      <line x1="282" y1="60" x2="328" y2="60"/>
      <line x1="282" y1="72" x2="328" y2="72"/>
      <line x1="282" y1="84" x2="328" y2="84"/>
      <line x1="282" y1="96" x2="328" y2="96"/>
    </g>
    <polyline points="282,98 290,88 298,92 306,78 314,84 322,68 330,74" fill="none" stroke="#f9564f" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
    <circle cx="330" cy="74" r="2.2" fill="#fffaf0"/>
  </g>

  <g>
    <rect x="82" y="118" width="152" height="60" rx="7" fill="#0c0a3e" stroke="#fffaf0" stroke-opacity=".16"/>
    <rect x="90" y="124" width="36" height="4" rx="2" fill="#fffaf0" opacity=".32"/>
    <g stroke="#fffaf0" stroke-opacity=".08">
      <line x1="90" y1="140" x2="226" y2="140"/>
      <line x1="90" y1="154" x2="226" y2="154"/>
      <line x1="90" y1="168" x2="226" y2="168"/>
    </g>
    <path d="M90,164 L104,156 L118,160 L132,146 L146,152 L160,138 L174,144 L188,130 L202,136 L216,124 L226,128 L226,172 L90,172 Z" fill="#f9564f" opacity=".12"/>
    <polyline points="90,164 104,156 118,160 132,146 146,152 160,138 174,144 188,130 202,136 216,124 226,128" fill="none" stroke="#f9564f" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  </g>

  <g>
    <rect x="242" y="118" width="94" height="60" rx="7" fill="#0c0a3e" stroke="#fffaf0" stroke-opacity=".16"/>
    <rect x="250" y="124" width="30" height="4" rx="2" fill="#fffaf0" opacity=".32"/>
    <g>
      <rect x="250" y="136" width="6" height="6" rx="1.5" fill="#f9564f"/>
      <rect x="260" y="137.5" width="54" height="3" rx="1.5" fill="#fffaf0" opacity=".38"/>
      <rect x="250" y="148" width="6" height="6" rx="1.5" fill="#f9564f"/>
      <rect x="260" y="149.5" width="44" height="3" rx="1.5" fill="#fffaf0" opacity=".3"/>
      <rect x="250" y="160" width="6" height="6" rx="1.5" fill="#fffaf0" opacity=".22"/>
      <rect x="260" y="161.5" width="50" height="3" rx="1.5" fill="#fffaf0" opacity=".22"/>
    </g>
  </g>

  <g transform="translate(288,166)">
    <rect width="50" height="16" rx="8" fill="#fffaf0"/>
    <circle cx="9" cy="8" r="2.6" fill="#f9564f"/>
    <rect x="16" y="6.5" width="22" height="3" rx="1.5" fill="#0c0a3e" opacity=".55"/>
  </g>
</svg>
"""

CARD = """
<div class="plate">
  <div class="card">
    <div class="copy">
      <div class="head">
        <div class="num">01</div>
        <h2 class="title">dynamic-dashboard</h2>
      </div>
      <p class="meta">2026 · Solo · product &amp; full stack</p>
      <p class="hook">A local-first dashboard builder — tabs of isolated HTML widgets on one SQLite database, edited by an agent in place.</p>
      <div class="specs">
        <div class="spec"><b>28</b><span>starter widgets</span></div>
        <div class="spec"><b>06</b><span>example tabs</span></div>
        <div class="spec"><b>01</b><span>shared DB</span></div>
      </div>
      <p class="stack">Bun · Hono · SQLite · Vanilla JS · OpenCode</p>
    </div>
    <div class="art">{artifact}<span class="go">↗</span></div>
  </div>
</div>
"""

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
.plate {{ width: 1200px; height: 400px; padding: 34px 84px; background: #0c0a3e; }}
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
.spec b::before {{ content: ''; width: 6px; height: 6px; background: #0c0a3e; }}
.spec span {{
  font-size: 8.5px; font-weight: 500; letter-spacing: 0.13em;
  text-transform: uppercase; color: rgba(12, 10, 62, 0.6);
}}
.stack {{
  margin: 12px 0 0; font-size: 9px; font-weight: 500; letter-spacing: 0.1em;
  text-transform: uppercase; color: rgba(12, 10, 62, 0.5);
}}
.art {{ position: relative; align-self: center; width: 360px; height: 203px; }}
.art svg, .art img {{
  display: block; width: 360px; height: 203px; border-radius: 16px;
  overflow: hidden; object-fit: cover;
  box-shadow: inset 0 0 0 1px rgba(12, 10, 62, 0.35);
}}
.art .go {{
  position: absolute; right: -13px; bottom: -13px;
  display: grid; place-items: center; width: 46px; height: 46px;
  border-radius: 50%; background: #ffffff;
  font-family: 'Days One', sans-serif; font-size: 19px;
}}
"""


def document(artifact: str) -> str:
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><style>"
        + STYLE
        + "</style></head><body>"
        + CARD.format(artifact=artifact)
        + "</body></html>"
    )


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    variants = {
        "plate-a.png": ILLUSTRATION,
        "plate-b.png": f'<img src="file://{ARTIFACT_B}" alt="">',
    }

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 400},
            device_scale_factor=2,
        )
        for name, artifact in variants.items():
            page_path = BUILD / name.replace(".png", ".html")
            page_path.write_text(document(artifact))
            page.goto(page_path.as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.screenshot(
                path=str(HERE / name),
                clip={"x": 0, "y": 0, "width": 1200, "height": 400},
            )
            print(f"rendered {name}")
        browser.close()


if __name__ == "__main__":
    main()
