#!/usr/bin/env python3
"""Render prototype header and footer variants that lead with the email.

The production boards in ``assets/readme/.build/00-header.html`` and
``07-footer.html`` are read, never written. The visible GitHub handle and URL
are replaced with the email, the footer loses its CTA pill, and the email line
moves just above the footer's own footline. The result is screenshotted at 2x.

    python3 assets/readme/prototype/boards.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / ".build"

EMAIL = "ed.normand@protonmail.com"

HEADER_CSS = """
.bottomline .say { text-transform: none; letter-spacing: 0.06em; }
.handle b { letter-spacing: 0.05em; }
"""

FOOTER_CSS = """
.footer { grid-template-rows: 1fr auto auto; }
.footer .contact {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 11px;
  padding: 0 0 16px;
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 0.04em;
  color: #fffaf0;
}
.footer .contact .arrow { color: #f9564f; font-size: 19px; line-height: 1; }
"""

FOOTER_CTA = """    <div class="cta">
      <span class="label">No forms, no trackers</span>
      <span class="link">github.com/edouwarden &nbsp;<b>↗</b></span>
    </div>
"""


def footer_transform(html: str) -> str:
    """Drop the CTA pill and set the email directly over the footline."""
    html = html.replace(FOOTER_CTA, "")
    contact = (
        '  <div class="contact">\n'
        f'    <span class="mail">{EMAIL}</span>\n'
        '    <span class="arrow">↗</span>\n'
        "  </div>\n"
    )
    return html.replace('  <div class="footline">', contact + '  <div class="footline">')


def variant(source: Path, name: str, height: int, css: str, transform=None) -> str:
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


def main() -> None:
    boards = (
        ("header", BUILD / "00-header.html", HERE / "deck-header.png", 720, HEADER_CSS, None),
        ("footer", BUILD / "07-footer.html", HERE / "deck-footer.png", 460, FOOTER_CSS, footer_transform),
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 720},
            device_scale_factor=2,
        )
        for name, source, target, height, css, transform in boards:
            root = variant(source, name, height, css, transform)
            page.set_viewport_size({"width": 1200, "height": height})
            page.goto(Path(root).as_uri())
            page.wait_for_function("document.fonts.status === 'loaded'")
            page.screenshot(
                path=str(target),
                clip={"x": 0, "y": 0, "width": 1200, "height": height},
            )
            print(f"rendered {target.name}")
        browser.close()


if __name__ == "__main__":
    main()
