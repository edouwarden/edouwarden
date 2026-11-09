#!/usr/bin/env python3
"""Two proof-plate variants for ft_transcendence.

A: a custom flat illustration of the crowned runner at the gate, drawn as
   inline SVG in the ambient palette.
B: the same card with a real in-game frame (the crown run) duotoned to the
   palette.

Both keep the card, type, and specs identical so only the visual changes.
Standalone: production README and build.py are untouched.

    python assets/readme/prototype/plates.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
FONTS = HERE.parent / "fonts"
BUILD = HERE.parent / ".build"
ARTIFACT_B = HERE / "artifact-b.png"

# Ground lines fan out from the horizon to the bottom edge.
PERSPECTIVE = " ".join(f"M180,112 L{x},203" for x in range(-120, 481, 30))

ILLUSTRATION = f"""
<svg viewBox="0 0 360 203" width="360" height="203" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="body" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#f9564f"/>
      <stop offset=".55" stop-color="#f9564f"/>
      <stop offset="1" stop-color="#dd453d"/>
    </linearGradient>
    <linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c0a3e" stop-opacity="0"/>
      <stop offset="1" stop-color="#0c0a3e" stop-opacity=".42"/>
    </linearGradient>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0c0a3e"/>
      <stop offset="1" stop-color="#17134f"/>
    </linearGradient>
    <radialGradient id="vignette" cx=".5" cy=".52" r=".72">
      <stop offset=".45" stop-color="#0c0a3e" stop-opacity="0"/>
      <stop offset="1" stop-color="#0c0a3e" stop-opacity=".38"/>
    </radialGradient>
  </defs>

  <rect width="360" height="203" fill="url(#sky)"/>
  <circle cx="180" cy="106" r="86" fill="#f9564f" opacity=".12"/>
  <circle cx="180" cy="106" r="86" fill="none" stroke="#fffaf0" opacity=".10"/>

  <g fill="#f9564f">
    <path d="M10,64 C10,56 18,50 26,52 C30,44 42,42 48,50 C56,48 64,54 64,62 C72,62 74,69 70,73 L16,73 C11,71 8,68 10,64 Z" opacity=".20" transform="translate(10,14) scale(1.2)"/>
    <path d="M10,64 C10,56 18,50 26,52 C30,44 42,42 48,50 C56,48 64,54 64,62 C72,62 74,69 70,73 L16,73 C11,71 8,68 10,64 Z" opacity=".16" transform="translate(254,6) scale(1.0)"/>
    <path d="M10,64 C10,56 18,50 26,52 C30,44 42,42 48,50 C56,48 64,54 64,62 C72,62 74,69 70,73 L16,73 C11,71 8,68 10,64 Z" opacity=".09" transform="translate(138,2) scale(.66)"/>
  </g>

  <rect y="112" width="360" height="91" fill="#dd453d"/>
  <path d="{PERSPECTIVE}" stroke="#0c0a3e" stroke-width="1" opacity=".16"/>

  <path d="M166,112 L194,112 L246,203 L114,203 Z" fill="#0c0a3e"/>
  <path d="M166,112 L194,112 L246,203 L114,203 Z" fill="none" stroke="#fffaf0" opacity=".14"/>
  <path d="M170,112 L174,112 L126,203 L120,203 Z" fill="#fffaf0" opacity=".05"/>
  <path d="M190,112 L194,112 L240,203 L234,203 Z" fill="#fffaf0" opacity=".05"/>

  <ellipse cx="180" cy="114" rx="80" ry="6" fill="#0c0a3e" opacity=".25"/>

  <g>
    <rect x="86" y="56" width="24" height="56" fill="#f9564f"/>
    <rect x="110" y="56" width="6" height="56" fill="#c9332d"/>
    <rect x="250" y="56" width="24" height="56" fill="#f9564f"/>
    <rect x="274" y="56" width="6" height="56" fill="#c9332d"/>
    <rect x="80" y="48" width="36" height="10" fill="#f9564f"/>
    <rect x="244" y="48" width="36" height="10" fill="#f9564f"/>
    <rect x="80" y="32" width="200" height="18" fill="#f9564f"/>
    <rect x="80" y="32" width="200" height="3" fill="#fffaf0" opacity=".38"/>
    <rect x="80" y="47" width="200" height="3" fill="#c9332d" opacity=".55"/>
    <rect x="84" y="36" width="3" height="10" fill="#fffaf0" opacity=".18"/>
    <rect x="273" y="36" width="3" height="10" fill="#fffaf0" opacity=".18"/>
  </g>

  <rect y="164" width="360" height="39" fill="url(#floor)"/>

  <g opacity=".22" stroke="#fffaf0" stroke-width="2" stroke-linecap="round">
    <path d="M132,166 L120,172"/>
    <path d="M139,174 L129,182"/>
    <path d="M228,166 L240,172"/>
    <path d="M221,174 L231,182"/>
  </g>

  <ellipse cx="180" cy="185" rx="25" ry="5" fill="#0c0a3e" opacity=".4"/>

  <g transform="translate(180,156) scale(1.15)">
    <path d="M-16,20 C-18,8 -17,-4 -12,-12 C-8,-19 8,-19 12,-12 C17,-4 18,8 16,20 C13,24 6,26 0,26 C-6,26 -13,24 -16,20 Z" fill="url(#body)"/>
    <path d="M-14,-2 q-8,4 -9,12" stroke="#dd453d" stroke-width="6" stroke-linecap="round" fill="none"/>
    <path d="M14,-2 q8,4 9,12" stroke="#dd453d" stroke-width="6" stroke-linecap="round" fill="none"/>
    <rect x="-10" y="23" width="10" height="6" rx="3" fill="#dd453d"/>
    <rect x="2" y="23" width="10" height="6" rx="3" fill="#dd453d"/>
    <path d="M-11,-18 L-11,-31 L-5,-24 L0,-34 L5,-24 L11,-31 L11,-18 Z" fill="#fffaf0"/>
    <path d="M-11,-18 L11,-18" stroke="#dd453d" stroke-width="1.4"/>
    <circle cx="-11" cy="-31" r="1.3" fill="#dd453d"/>
    <circle cx="0" cy="-34" r="1.3" fill="#dd453d"/>
    <circle cx="11" cy="-31" r="1.3" fill="#dd453d"/>
  </g>

  <rect width="360" height="203" fill="url(#vignette)"/>
</svg>
"""

CARD = """
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
