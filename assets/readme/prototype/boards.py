#!/usr/bin/env python3
"""Render prototype header and footer variants that lead with the email.

The production boards in ``assets/readme/.build/00-header.html`` and
``07-footer.html`` are read, never written. The visible GitHub handle and URL
are replaced with the email, a small amount of CSS keeps the longer address
inside its column, and the result is screenshotted at 2x.

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
.footer .cta .link { font-size: 15px; }
"""


def variant(source: Path, name: str, height: int, css: str) -> str:
    html = source.read_text()
    html = html.replace("@edouwarden", EMAIL)
    html = html.replace("github.com/edouwarden", EMAIL)
    html = html.replace("</style>", css + "</style>")
    BUILD.mkdir(parents=True, exist_ok=True)
    path = BUILD / f"prototype-{name}.html"
    path.write_text(html)
    return str(path)


def main() -> None:
    boards = (
        ("header", BUILD / "00-header.html", HERE / "deck-header.png", 720, HEADER_CSS),
        ("footer", BUILD / "07-footer.html", HERE / "deck-footer.png", 460, FOOTER_CSS),
    )
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1200, "height": 720},
            device_scale_factor=2,
        )
        for name, source, target, height, css in boards:
            root = variant(source, name, height, css)
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
