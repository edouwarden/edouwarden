# Proof plate prototype

Four directions for the `dynamic-dashboard` plate. Every card keeps the same
title, copy, stats, and stack; only the visual and its composition change. The
card carries the project's own numbers — it does not repeat the profile-wide
`2,000+ players served` figure.

- **A — `plate-a.png`**: a flat illustration of the dashboard shell drawn inline
  as SVG in the ambient palette. Sidebar, widget grid, stat panel, sparkline and
  chart, all built from the same navy / coral / paper shapes. No screenshot,
  fully scalable and palette-true.
- **B — `plate-b.png`**: a real screenshot of the Personal OS tab in its native
  colours, cropped to 720 × 405 and given a light contrast lift. It shows the
  actual widgets and typography without a duotone or heavy grade.
- **C — `plate-c.png`**: the same screenshot at 470 × 264, roughly 70% more
  visual area. The screenshot leads the card and the copy gives it room.
- **D — `plate-d.png`**: the illustration becomes a giant background ghost, the
  same device the production plates use for the project number. The copy sits on
  top, with the drawing faded out under the text and readable at the right.

## Card content

- Title: `dynamic-dashboard`
- Meta: `2026 · Solo · product & full stack`
- Hook: a local-first dashboard builder — tabs of isolated HTML widgets on one
  SQLite database, edited by an agent in place.
- Stats: `28 starter widgets / 06 example tabs / 01 shared DB`
- Stack: `Bun · Hono · SQLite · Vanilla JS · OpenCode`

## Files

- `plates.py` — renders all four variants at 1200 × 400, 2x, using the deck
  fonts. HTML goes to the ignored `.build/` folder.
- `artifact-b.png` — the 720 × 405 Personal OS crop used by B and C.
- `plate-a.png` … `plate-d.png` — the rendered plates. Each carries a small
  lettered label in its top margin so the variants read in the project list.

```bash
python3 assets/readme/prototype/plates.py
```

This folder sits outside the production pipeline: `build.py` still generates
the committed plates and the public README is unchanged. Once a direction is
approved, the chosen composition can become a shared slot in `build.py` for all
six projects — a widget grid for dynamic-dashboard, terminal frames for minishell
and IRC, raycast stills for cub3D, topology diagrams for Inception and
born2beroot.
