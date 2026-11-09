# Proof plate prototype

Two directions for the ft_transcendence plate, side by side. Both keep the
card, type, and specs identical; only the right-hand visual changes.

- **A — `plate-a.png`**: a flat illustration of the crowned runner at the gate,
  drawn inline as SVG in the ambient palette. No screenshot, fully scalable.
- **B — `plate-b.png`**: frame 16 of the launch trailer (`trailer-short.gif`),
  the final-stretch crown run. Grayscale, contrast ×1.2, then gradient-mapped
  navy `#0c0a3e` → navy lift `#17134f` → coral deep `#dd453d` → coral
  `#f9564f` → paper `#fffaf0`, so the sky lands in paper and the course in
  coral. `artifact-b.png` is that 720 × 405 source.

## Files

- `plates.py` — renders both variants at 1200 × 400, 2x, using the deck fonts.
  HTML goes to the ignored `.build/` folder.
- `artifact-b.png` — duotoned trailer frame used by B.
- `plate-a.png`, `plate-b.png` — the rendered plates.

```bash
python3 assets/readme/prototype/plates.py
```

This folder sits outside the production pipeline: `build.py` still generates
the eight committed plates and `README.md` is unchanged. Once a direction is
approved, the artifact panel can become a shared slot in `build.py` for all six
projects — terminal frames for minishell and IRC, raycast stills for cub3D,
duotoned topology diagrams for Inception and born2beroot.
