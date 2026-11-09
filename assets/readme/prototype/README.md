# Proof plate prototype

A single ft_transcendence plate exploring the next step for the project cards:
real evidence instead of only title and prose.

- `artifact-01.png` — frame 21 from the game's own `docs/clips/gameplay.gif`,
  contrast +12%, then gradient-mapped from navy `#0c0a3e` through navy lift
  `#17134f`, coral deep `#dd453d`, coral `#f9564f`, to paper `#fffaf0`.
- `plate.py` — renders the plate at 1200 × 400, 2x, using the same fonts as
  the main deck. HTML goes to the ignored `.build/` folder.
- `plate.png` — the rendered prototype.

```bash
python assets/readme/prototype/plate.py
```

This folder is deliberately outside the production pipeline: `build.py` still
generates the eight committed plates and `README.md` is unchanged. Once the
direction is approved, the artifact panel becomes a shared slot in `build.py`
for all six projects — terminal frames for minishell and IRC, raycast stills
for cub3D, duotoned topology diagrams for Inception and born2beroot.
