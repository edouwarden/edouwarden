#!/usr/bin/env python3
"""Render prototype header and footer variants that lead with the email.

The production boards in ``assets/readme/.build/00-header.html`` and
``07-footer.html`` are read, never written. The visible GitHub handle and URL
are replaced with the email, the footer loses its CTA pill, and the email line
moves just above the footer's own footline. The result is screenshotted at 2x.

The header keeps the quiet "open to hard problems" pill and points its
location line at Switzerland. The open-to-work signal is the thin animated
strip in ``stats.py`` (``deck-open.svg``), which sits above the header.

    python3 assets/readme/prototype/boards.py
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent / ".build"

EMAIL = "ed.normand@protonmail.com"

HEADER_CSS = """
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
  font-size: 20px;
  font-weight: 500;
  letter-spacing: 0.04em;
  white-space: nowrap;
  color: #fffaf0;
}
.footer .contact::before {
  content: '';
  flex: none;
  width: 9px;
  height: 9px;
  background: #f9564f;
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


def header_transform(html: str) -> str:
    """Point the location line at Switzerland and keep one email in the header."""
    html = html.replace("Paris, France · 42 Paris", "Switzerland · 42 Paris")
    html = html.replace("Coding since nine", "Coding since age 9")
    html = html.replace(' <span class="slash">/</span> Profile', "")
    html = html.replace(
        '  <div class="bottomline">\n'
        '    <span class="say">github.com/edouwarden</span>\n'
        '    <span>Selected work &nbsp;<span class="arrow">↓</span></span>\n'
        "  </div>\n",
        "",
    )
    return html


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
            680,
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

        browser.close()


if __name__ == "__main__":
    main()
