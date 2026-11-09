#!/usr/bin/env python3
"""Small helper for wrapping a rendered PNG in an SVG with a live overlay.

GitHub renders README images as standalone ``<img>`` elements, so a separate
overlay image cannot be positioned on top of a PNG. Embedding the PNG as a data
URI inside an SVG gives the browser one image to lay out, and SMIL inside that
SVG still moves when the image is viewed through GitHub's camo proxy.

    from embed import write_image_svg
"""

import base64
from pathlib import Path


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode(
        "ascii"
    )


def write_image_svg(
    source: Path,
    target: Path,
    width: int,
    height: int,
    overlay: str,
    title: str,
) -> None:
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f"<title>{title}</title>"
        f'<image href="{data_uri(source)}" width="{width}" height="{height}"/>'
        f"{overlay}"
        "</svg>"
    )
    target.write_text(svg)
