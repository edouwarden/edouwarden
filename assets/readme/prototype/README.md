# Proof plate prototype

Direction **A** — a custom flat illustration on every project card — applied to
the whole deck. Each card keeps the same anatomy: number, title, meta, hook,
three project-specific stats, stack, and a 360 × 203 illustration drawn inline
as SVG in the ambient palette. The stats sit in one row above the stack, with a
hairline rule separating the numbers from the prose. Forge closes the series as
the same card drawn as an outline: transparent body, coral edge, in-progress
copy, and a slow ember pulse over the anvil.

The illustrations are small scenes and objects, not diagrams: a dashboard, an
engine editor, a seeded height field feeding a core column, a terminal, a raycast
corridor, an IRC frame beside a single-thread server, a Docker host, and a VM
window on a hypervisor host. No node graphs, no layer trees, and no tiny labels
that disappear at README width. Every plate is self-contained, so the public
`build.py` pipeline and the production README are untouched.

After the nine plates, a quiet **More work** ledger adds five projects in slim,
individually linked rows: AEGIS Fabric, Financial-Market-Theories,
Trading-Support-Tools, and the not-yet-public portfolio-webpage and 42 Intra
Tools. It keeps the curated nine as the lead story while giving the rest of the
bench a place on the deck.

The Space plate leads with the **world-generation technique**: a 26 × 15 blocky
height field sampled from six octaves of value noise, contour edges between
height bands, and one highlighted sample feeding an eight-layer core column. It
shows how the terrain is built, not a finished space scene.

## The data rails

Deck-width strips stack flush around the plates. Section boundaries are set by
space, marks and cards rather than full-width rules:

- `deck-stack.svg` — twenty-four technologies in two full-width rows that scroll
  slowly in opposite directions under a `Stack` title: product and data on top,
  systems and security below. Coral vector icons, a soft fade at each edge, no
  count. Vector, 900 × 150, with the rows looping every 20–23 seconds at the
  same scroll speed.
- `deck-languages.png` — a slim language line, most used first: TypeScript,
  JavaScript, Python, C, Java, Go and Bash, each with its share of the counted
  lines (39.2% down to 1.7%). `loc.json` is the `pygount` snapshot behind the
  shares, with HTML, CSS, JSON, YAML, Markdown, lockfiles and generated data
  excluded.
- `deck-projects.svg` — the project-section header that introduces the plates:
  a single `Projects` title and the quiet plate range `01 — 09`. The old Forge
  tease is gone; Forge is a plate now.
- `deck-more.svg` plus `deck-more-10.svg` … `deck-more-14.svg` — the **More work**
  header and five 1200 × 100 rows, one project per row so each can keep its own
  link. The left column holds the index, title and role; the centre holds a
  one-sentence pitch; the right holds three compact stats and a `REPO` or `SOON`
  status. The rows are vector, stack flush, and follow Forge before the review
  marquee.
- `deck-try.svg` — a thin 900 × 44 outline capsule aligned to the dashboard card
  and set directly under plate 01: coral `Try it now`, the
  `dynamic-dashboard.ednormand.fr` URL, a pulsing dot and a nudging arrow. Plate
  01 is clipped just below the card so the capsule sits about 8 px under it; the
  card itself is unchanged. It replaces the old filled live-demo caption.
- `deck-open.svg` — a thin 900 × 44 capsule with the same weight as the try
  strip: a pulsing coral dot, `Open to work · Switzerland`, and the quiet
  `Systems · Infrastructure · AI` meta on the right. It sits directly above the
  header.
- `deck-reviews.svg` — a slow marquee of peer-review cards under a `Reviews`
  title. Each quote wraps into a card, and the section grows with the longest
  quote. The three quotes in `stats.py` are mock placeholders; replace `REVIEWS`
  with real quotes before publishing.
- `deck-header.png`, `deck-footer.png` — prototype copies of the profile header
  and footer with `ed.normand@protonmail.com` in place of the visible GitHub
  handle and URL. The header keeps a single email under the portrait, drops the
  duplicate bottom-line email and the `Profile` suffix, moves the location line
  to `Switzerland · 42 Paris`, and keeps the quiet `Open to hard problems` pill.
  The footer drops the `No forms, no trackers` label and the CTA pill, leads
  with `Bring me a hard problem`, sets a coral square, the 20 px email and 24 px
  coral arrow directly above the footline, and closes with `Open to work ·
  Switzerland · 42 Paris` and `Updated November 2026`. `boards.py` reads the
  production boards, replaces the copy and screenshots the variants at 2x; the
  production boards are not modified.

## Text fallback

The root `README.md` closes with a collapsed `<details>` block: the same
profile, the nine plates, the five More work entries, stack, language shares,
education and contact as plain Markdown. It gives search, screen readers and
no-image readers a complete path without changing the image-first deck.

## What each project leads with

| Plate | Focus | Stats | Stack |
|---|---|---|---|
| `01` dynamic-dashboard | Tabs of isolated widgets on one SQLite database | 28 widgets · 06 tabs · 01 DB | Bun · Hono · SQLite · Vanilla JS · OpenCode |
| `02` ft_transcendence | The engine (`World → Environment → Module`), not just the match | 04 layers · 04 maps · 20 Hz net | Next.js · Three.js · Rapier · Bun · Go · PostgreSQL |
| `03` space-gameserver | World generation first: a seeded six-octave height field sampled into a core column | 2,000+ members · 05 powers · 11×11 slots | Java 8 · Paper 1.14.4 · WorldEdit · WorldGuard · Python |
| `04` minishell | Lexer, expansion, heredocs and pipelines; readline only | 3,000 lines · 64 stages · 0 zombies | C99 · POSIX · fork/exec · dup2 · readline |
| `05` cub3D | Hand-written raycast into an X11 buffer, no GPU | 640 rays · 03 maps · ~60 fps | C99 · X11 · raycasting · XPM · math |
| `06` ft_irc | One thread, one `poll()` loop, plus a local model | 1 thread · 1 poll loop · 3.8B model | C++98 · sockets · poll() · llama.cpp |
| `07` Inception | Three containers, one published port, TLS at the edge | 03 services · 01 port · 04 secrets | Docker Compose · NGINX · WordPress · MariaDB · TLS |
| `08` born2beroot | A guest VM window on a hypervisor host: LUKS under LVM, hardened perimeter | 07 volumes · 01 port · 10 min wall | Debian · LUKS · LVM · UFW · systemd |
| `09` Forge | The public slice of a controlled code-generation pipeline, drawn as an in-progress outline card with a slow ember pulse | 28 steps · 06 model-served · 21/21 checks | Bun · TypeScript · SQLite · Docker · Linux |

`ft_transcendence` is framed as a browser game engine; the 2,000+ figure belongs
to `space-gameserver`, not to it. The profile header keeps its own profile-wide
stat. Its role reads `Team lead · engine & frontend`, matching the portfolio.
`minishell`, `cub3D` and `ft_irc` are labelled `Pair`, matching the credits in
their project READMEs.

Forge now uses the published public-slice numbers: a 28-step run, 6 model-served
steps and 21/21 checks. The card still opens `github.com/edouwarden/theforge`
and stays an outline because the engine is larger and still in progress.

### More work

| Row | Focus | Stats | Status |
|---|---|---|---|
| `10` AEGIS Fabric | A zero-trust studio network: one way in, one way out, no public admin plane | 24 devices · 06 egress lanes · 00 admin ports | repo |
| `11` Financial-Market-Theories | 21 falsifiable market ideas with claim, mechanism, test and verdict | 21 theories · 04 parts · 00 signals | repo |
| `12` Trading-Support-Tools | A live futures bot, its order lifecycle and an auditable journal | 1,059 rows · 98 trade IDs · 1.84 PF | repo |
| `13` portfolio-webpage | A four-locale static Astro portfolio with no framework runtime | 69 pages · 04 locales · €0 infra | soon |
| `14` 42 Intra Tools | Small tools over the Intra API v2, including correction-slot pressure | v2 API · 01 analysis · WIP | soon |

The two `SOON` rows are deliberately unlinked: they are on the bench, not in a
public repository yet. The three `REPO` rows each link their own SVG, so the
ledger stays clickable without becoming one opaque image.

## Files

- `plates.py` — renders all nine plates at 1200 × 400, 2x, using the deck
  fonts; plate 01 is clipped to 1200 × 376 so the try strip can sit close to it.
  HTML goes to the ignored `.build/` folder.
- `plate-01.png`, `plate-02.png`, `plate-03.png`, `plate-04.png` … `plate-09.png`
  — the rendered plates. `plate-09.svg` wraps the Forge PNG and adds the ember
  pulse over the anvil; the other plates stay PNG.
- `stats.py` — writes the stack, project-section, try-it, open-to-work, More work
  and review rails as SVG and renders the language line at 2x. HTML goes to the
  ignored `.build/` folder.
- `boards.py` — reads the production header and footer boards and renders
  `deck-header.png` and `deck-footer.png` with the email in place of the visible
  GitHub copy. HTML goes to the ignored `.build/` folder.
- `embed.py` — base64-embeds a rendered PNG inside an SVG so a live SMIL overlay
  can sit on top of a raster board.
- `tech-icons.json` — monochrome Simple Icons paths keyed by slug for the strip.
- `tech-icons-generic.json` — solid glyphs for the tools that are not brands.
- `loc.json` — the pygount snapshot: total, per-language lines, and exclusions.
- `deck-stack.svg`, `deck-languages.png`, `deck-projects.svg`, `deck-try.svg`,
  `deck-open.svg`, `deck-more.svg`, `deck-more-10.svg` … `deck-more-14.svg`,
  `deck-reviews.svg`, `deck-header.png`, `deck-footer.png` — the rendered data
  rails and board variants.

```bash
python3 assets/readme/prototype/plates.py
python3 assets/readme/prototype/stats.py
python3 assets/readme/prototype/boards.py
```

Once approved, the illustration slot can become a first-class field in
`build.py` for every project: a widget shell for dynamic-dashboard, an engine
editor for ft_transcendence, a seeded height field and core sample for Space, a
terminal for minishell, a raycast view for cub3D, a protocol frame for ft_irc, a
Docker host for Inception, a VM window on a hypervisor host for born2beroot, and
an anvil and hammer for Forge.
