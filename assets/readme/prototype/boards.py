#!/usr/bin/env python3
"""Render prototype header and footer variants that lead with the email.

The production boards in ``assets/readme/.build/00-header.html`` and
``07-footer.html`` are read, never written. The visible GitHub handle and URL
are replaced with the email, the footer loses its CTA pill, and the email line
moves just above the footer's own footline. The result is screenshotted at 2x.

There are two headers: the base ``deck-header.png`` keeps the quiet
"open to hard problems" pill, while ``deck-header-work.svg`` carries the
animated "open to work · Switzerland" tag. The PNG is embedded in the SVG so
one image can hold both the static board and the live pulsing dot.

    python3 assets/readme/prototype/boards.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

from embed import write_image_svg

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / ".build"

EMAIL = "ed.normand@protonmail.com"
NAVY = "#0c0a3e"

HEADER_CSS = """
.bottomline .say { text-transform: none; letter-spacing: 0.06em; }
.handle b { letter-spacing: 0.05em; }
"""

HEADER_WORK_CSS = HEADER_CSS + """
.pill.work i { visibility: hidden; }
"""

FOOTER_CSS = """
.footer { grid-template-rows: 1fr auto auto; }
.footer .contact {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 11px;
  padding: 0 0 16px;
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 0.04em;
  white-space: nowrap;
  color: #fffaf0;
}
.footer .contact .arrow { color: #f9564f; font-size: 24px; line-height: 1; }
"""

FOOTER_CTA = """    <div class="cta">
      <span class="label">No forms, no trackers</span>
      <span class="link">github.com/edouwarden &nbsp;<b>↗</b></span>
    </div>
"""

FOOTER_HEAD = "<h2>Let's build<br>something.</h2>"
FOOTER_HEAD_NEW = "<h2>Bring me a<br>hard problem</h2>"

FOOTER_LEFT = (
    "<span><b>Open to hard problems</b> · Paris, FR · 42 Paris</span>"
)
FOOTER_LEFT_NEW = "<span><b>Open to work</b> · Switzerland · 42 Paris</span>"
FOOTER_RIGHT = "<span>Systems · Infrastructure · AI</span>"
FOOTER_RIGHT_NEW = "<span>Updated November 2026</span>"

HEADER_PILL = '<div class="pill"><i></i> Open to hard problems</div>'
HEADER_PILL_WORK = (
    '<div class="pill work"><i></i> Open to work · Switzerland</div>'
)


def header_transform(html: str) -> str:
    """Point the location line at Switzerland."""
    return html.replace("Paris, France · 42 Paris", "Switzerland · 42 Paris")


def header_work_transform(html: str) -> str:
    """Swap the pill for the open-to-work tag; its dot is drawn in the SVG."""
    return header_transform(html).replace(HEADER_PILL, HEADER_PILL_WORK)


def footer_transform(html: str) -> str:
    """Drop the CTA pill, rewrite the copy, set the email over the footline."""
    html = html.replace(FOOTER_CTA, "")
    html = html.replace(FOOTER_HEAD, FOOTER_HEAD_NEW)
    html = html.replace(FOOTER_LEFT, FOOTER_LEFT_NEW)
    html = html.replace(FOOTER_RIGHT, FOOTER_RIGHT_NEW)
    contact = (
        '  <div class="contact">\n'
        f'    <span class="mail">{EMAIL}</span>\n'
        '    <span class="arrow">↗</span>\n'
        "  </div>\n"
    )
    return html.replace('  <div class="footline">', contact + '  <div class="footline">')


def variant(source: Path, name: str, css: str, transform=None) -> str:
    html = source.read_text()
    if transform is not None:
        html = transform(html)
    html = html.replace("@edouwarden", EMAIL)
    html = html.replace("github.com/edouwarden", EMAIL)
    html = html.replace("</style>", css + "</style>")
    BUILD.mkdir(parents=True, exist_ok=True)
    path = BUILD / f"prototype-{name}.html"
    path.write_text(html)
    return str(path)


def work_pulse(cx: float, cy: float, radius: float) -> str:
    """A paper-dark dot and an expanding ring, scaled to the 2x board."""
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{NAVY}">'
        '<animate attributeName="opacity" values="1;0.45;1" dur="2.6s" '
        'repeatCount="indefinite"/></circle>'
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="{NAVY}" stroke-width="2" opacity="0">'
        f'<animate attributeName="r" values="{radius};{radius + 14};{radius + 14}" '
        'dur="2.6s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0.55;0;0" dur="2.6s" '
        'repeatCount="indefinite"/></circle>'
    )


def render(page, source: Path, name: str, height: int, css: str, transform, target: Path) -> None:
    root = variant(source, name, css, transform)
    page.set_viewport_size({"width": 1200, "height": height})
    page.goto(Path(root).as_uri())
    page.wait_for_function("document.fonts.status === 'loaded'")
    page.screenshot(
        path=str(target),
        clip={"x": 0, "y": 0, "width": 1200, "height": height},
    )
    print(f"rendered {target.name}")


def main() -> None:
    BUILD.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 720},
            device_scale_factor=2,
        )

        render(
            page,
            BUILD / "00-header.html",
            "header",
            720,
            HEADER_CSS,
            header_transform,
            HERE / "deck-header.png",
        )
        render(
            page,
            BUILD / "07-footer.html",
            "footer",
            460,
            FOOTER_CSS,
            footer_transform,
            HERE / "deck-footer.png",
        )

        # The work header is rendered to the build folder, then wrapped in an
        # SVG so the hidden pill dot can pulse without a second image.
        work_png = BUILD / "header-work.png"
        render(
            page,
            BUILD / "00-header.html",
            "header-work",
            720,
            HEADER_WORK_CSS,
            header_work_transform,
            work_png,
        )
        try:
            dot = page.evaluate(
                """() => {
                    const box = document.querySelector('.pill i').getBoundingClientRect();
                    return {x: box.x + box.width / 2, y: box.y + box.height / 2, r: box.width / 2};
                }"""
            )
        except Exception:
            dot = None
        if dot is None:
            raise SystemExit("could not measure the open-to-work dot")
        overlay = work_pulse(dot["x"] * 2, dot["y"] * 2, dot["r"] * 2)
        write_image_svg(
            work_png,
            HERE / "deck-header-work.svg",
            2400,
            1440,
            overlay,
            "Edouard Normand — open to work in Switzerland",
        )
        print("wrote deck-header-work.svg")

        browser.close()


if __name__ == "__main__":
    main()
