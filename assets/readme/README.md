# Profile artwork

The root `README.md` is image-only: a header, six project plates, and a footer.
Every plate is a separate linked PNG, and all eight sit in one `<p>` with
`<img align="top">` so they stack with zero gap. Do not add blank lines or
whitespace between the tags — that is what keeps the seams invisible.

Project plates are inset cards: each 1200 px artboard is a continuous navy
field with a coral rounded card sitting inside it (84 px side gutters,
34 px top and bottom). The gutters belong to the image, so the cards read
narrower than the column while the stack still touches edge to edge.

Palette and type follow the portfolio's ambient edition:

| Token | Value |
| --- | --- |
| Navy | `#0c0a3e` |
| Navy lift | `#17134f` |
| Coral | `#f9564f` |
| Coral deep | `#dd453d` |
| Paper | `#fffaf0` |
| Display | Days One |
| Mono | IBM Plex Mono |

## Rebuild

```bash
python assets/readme/build.py
```

Requires Python 3, Pillow, and Playwright with Chromium installed. The script
cuts `portrait-source.jpg` into a soft-edged disc, then renders each 1200 px
artboard at 2x into the PNGs next to it. `.build/` holds throwaway HTML,
`portrait-disc.png` is generated, and both are ignored by git.

## Files

| File | What it is |
| --- | --- |
| `00-header.png` | Wordmark, portrait, lede, stats. |
| `01-transcendence.png` … `06-born2beroot.png` | One plate per project. |
| `07-footer.png` | Contact panel. |
| `portrait-source.jpg` | Original profile illustration. |
| `fonts/` | Days One and IBM Plex Mono subsets with their OFL licenses. |

The colors are flat by design: changing a token in `build.py` and re-running it
regenerates the whole set.
