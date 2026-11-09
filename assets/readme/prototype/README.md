# Proof plate prototype

Two directions for the `dynamic-dashboard` plate, side by side. Both keep the
card, type, and specs identical; only the right-hand visual changes. The card
carries the project's own stack and stats — it does not repeat the profile-wide
`2,000+ players served` figure.

- **A — `plate-a.png`**: a flat illustration of the dashboard shell drawn inline
  as SVG in the ambient palette. Sidebar, widget grid, stat panel, sparkline and
  chart, all built from the same navy / coral / paper shapes. No screenshot,
  fully scalable and palette-true.
- **B — `plate-b.png`**: a real screenshot of the Personal OS tab in its native
  colours, cropped to 720 × 405 and given a light contrast lift. It shows the
  actual widgets and typography without a duotone or heavy grade.

## Card content

- Title: `dynamic-dashboard`
- Meta: `2026 · Solo · product & full stack`
- Hook: a local-first dashboard builder — tabs of isolated HTML widgets on one
  SQLite database, edited by an agent in place.
- Stats: `28 starter widgets / 06 example tabs / 01 shared DB`
- Stack: `Bun · Hono · SQLite · Vanilla JS · OpenCode`

## Files

- `plates.py` — renders both variants at 1200 × 400, 2x, using the deck fonts.
  HTML goes to the ignored `.build/` folder.
- `artifact-b.png` — the 720 × 405 Personal OS crop used by B.
- `plate-a.png`, `plate-b.png` — the rendered plates.

```bash
python3 assets/readme/prototype/plates.py
```

This folder sits outside the production pipeline: `build.py` still generates
the committed plates and the public README is unchanged. Once a direction is
approved, the artifact panel can become a shared slot in `build.py` for all six
projects — a widget grid for dynamic-dashboard, terminal frames for minishell
and IRC, raycast stills for cub3D, topology diagrams for Inception and
born2beroot.
