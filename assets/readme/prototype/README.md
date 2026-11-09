# Proof plate prototype

Direction **A** — a custom flat illustration on every project card — applied to
the whole deck. Each card keeps the same anatomy: number, title, meta, hook,
three project-specific stats, stack, and a 360 × 203 illustration drawn inline
as SVG in the ambient palette.

The illustrations are diagrams of the project's actual subject, not screenshots
and not the same motif reused. Every plate is self-contained, so the public
`build.py` pipeline and the production README are untouched.

## What each project leads with

| Plate | Focus | Stats | Stack |
|---|---|---|---|
| `01` dynamic-dashboard | Tabs of isolated widgets on one SQLite database | 28 widgets · 06 tabs · 01 DB | Bun · Hono · SQLite · Vanilla JS · OpenCode |
| `02` ft_transcendence | The engine (`World → Environment → Module`), not just the match | 04 layers · 04 maps · 20 Hz net | Next.js · Three.js · Rapier · Bun · Go · PostgreSQL |
| `03` space-gameserver | 2019 systems and geometry: orbital grid, five powers, voice relay | 2,000+ members · 05 powers · 11×11 slots | Java 8 · Paper 1.14.4 · WorldEdit · WorldGuard · Python |
| `04` minishell | Lexer, expansion, heredocs and pipelines; readline only | 3,000 lines · 64 stages · 0 zombies | C99 · POSIX · fork/exec · dup2 · readline |
| `05` cub3D | Hand-written raycast into an X11 buffer, no GPU | 640 rays · 03 maps · ~60 fps | C99 · X11 · raycasting · XPM · math |
| `06` ft_irc | One thread, one `poll()` loop, plus a local model | 1 thread · 1 poll loop · 3.8B model | C++98 · sockets · poll() · llama.cpp |
| `07` Inception | Three containers, one published port, TLS at the edge | 03 services · 01 port · 04 secrets | Docker Compose · NGINX · WordPress · MariaDB · TLS |
| `08` born2beroot | Reproducible Debian, LUKS under LVM, hardened perimeter | 07 volumes · 01 port · 10 min wall | Debian · LUKS · LVM · UFW · systemd |

`ft_transcendence` is framed as a browser game engine; the 2,000+ figure belongs
to `space-gameserver`, not to it. The profile header keeps its own profile-wide
stat.

## Files

- `plates.py` — renders all eight plates at 1200 × 400, 2x, using the deck
  fonts. HTML goes to the ignored `.build/` folder.
- `plate-01.png` … `plate-08.png` — the rendered plates.

```bash
python3 assets/readme/prototype/plates.py
```

Once approved, the illustration slot can become a first-class field in
`build.py` for every project: a widget shell for dynamic-dashboard, an engine
world for ft_transcendence, an orbital chart for Space, a pipeline for
minishell, a raycast view for cub3D, a poll loop for ft_irc, a container network
for Inception, and a disk stack for born2beroot.
