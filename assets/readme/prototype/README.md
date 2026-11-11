# Proof plate prototype

Direction **A** — a custom flat illustration on every project card — applied to
the whole deck. The seven lead cards keep the full anatomy: number, title, hook,
three project-specific stats, a full-width footer with date and team chips on
the left and the stack chip on the right, and a 360 × 203 illustration drawn
inline as SVG in the ambient palette. The five
bench cards repeat the same anatomy at 1200 × 260 with 230 × 130 art and smaller
type, minus the stat row, so the hierarchy reads before any copy is parsed. On the
lead cards the stats and footer chips sit under one hairline rule; the bench cards
keep the rule above the chips. The chips show only the date, the team or solo
label and the stack. Project-type labels and Minecraft plugin names such as
WorldEdit are deliberately left out. Forge opens the series as the same card
drawn as an outline: transparent body, coral edge, in-progress copy, and a slow
ember pulse over the anvil.

The illustrations are small scenes and objects, not diagrams: a dashboard, an
engine editor, a policy gate with six egress lanes, a trading terminal, a theory
notebook, a seeded height field feeding a core column, a terminal, a raycast
corridor, an IRC frame beside a single-thread server, a Docker host, and a VM
window on a hypervisor host. No node graphs, no layer trees, and no tiny labels
that disappear at README width. Every plate is self-contained, so the public
`build.py` pipeline and the production README are untouched.

The deck opens with Forge, Financial-Market-Theories, AEGIS Fabric and
Trading-Support-Tools, then space-gameserver, dynamic-dashboard and
ft_transcendence. The five school projects after them — minishell, cub3D, ft_irc,
Inception and born2beroot — use the compact card, so the strongest work carries
the page and the rest stays available without competing.

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
  a single `Projects` title and the quiet plate range `01 — 12`. The old Forge
  tease is gone; Forge is a plate now.
- `deck-try.svg` — a thin 900 × 44 outline capsule aligned to the dashboard card
  and set directly under plate 06: coral `Try it now`, the
  `dynamic-dashboard.ednormand.fr` URL, a pulsing dot and a nudging arrow. Plate
  06 is clipped just below the card so the capsule sits about 8 px under it; the
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
profile, the twelve plates, stack, language shares, education and contact as
plain Markdown. It gives search, screen readers and no-image readers a complete
path without changing the image-first deck.

## What each project leads with

| Plate | Format | Focus | Stats (lead cards only) | Stack |
|---|---|---|---|---|
| `01` Forge | outline | The public slice of a controlled code-generation pipeline, with a slow ember pulse | 28 steps · 06 model-served · 21/21 checks | Bun · TypeScript · SQLite · Docker · Linux |
| `02` Financial-Market-Theories | full | Claim, mechanism, test and verdict, negative results kept | 21 theories · 04 parts · 00 signals | Python · JavaScript |
| `03` AEGIS Fabric | full | One ingress, six egress lanes and no public admin plane | 24 devices · 06 egress lanes · 00 admin ports | nftables · Tailscale · Suricata · Firecracker · Vault |
| `04` Trading-Support-Tools | full | A crash-safe order lifecycle and the journal that survived it | 1,059 rows · 98 trade IDs · 1.84 PF | JavaScript · Python · SQLite |
| `05` space-gameserver | full | World generation first: a seeded six-octave height field sampled into a core column | 2,000+ members · 05 powers · 11×11 slots | Java 8 · Paper 1.14.4 · Python |
| `06` dynamic-dashboard | full | Tabs of isolated widgets on one SQLite database | 28 widgets · 06 tabs · 01 DB | Bun · Hono · SQLite · Vanilla JS · OpenCode |
| `07` ft_transcendence | full | The engine (`World → Environment → Module`), not just the match | 04 layers · 04 maps · 20 Hz net | Next.js · Three.js · Rapier · Bun · Go · PostgreSQL |
| `08` minishell | compact | Lexer, expansion, heredocs and pipelines; readline only | — | C99 · POSIX · readline |
| `09` cub3D | compact | Hand-written raycast into an X11 buffer, no GPU | — | C99 · X11 |
| `10` ft_irc | compact | One thread, one `poll()` loop, plus a local model | — | C++98 · POSIX sockets · llama.cpp |
| `11` Inception | compact | Three containers, one published port, TLS at the edge | — | Docker Compose · NGINX · WordPress · MariaDB · TLS |
| `12` born2beroot | compact | A guest VM window on a hypervisor host: LUKS under LVM, hardened perimeter | — | Debian · LUKS · LVM · UFW · systemd |

`ft_transcendence` is framed as a browser game engine; the 2,000+ figure belongs
to `space-gameserver`, not to it. The profile header keeps its own profile-wide
stat. Its role reads `Team lead · engine & frontend`, matching the portfolio.
`minishell`, `cub3D` and `ft_irc` are labelled `Pair`, matching the credits in
their project READMEs.

Forge now uses the published public-slice numbers: a 28-step run, 6 model-served
steps and 21/21 checks. The card still opens `github.com/edouwarden/theforge`
and stays an outline because the engine is larger and still in progress.

The three promoted projects are public repositories, so each one is a full card
with its own illustration and link. `portfolio-webpage` and `42 Intra Tools` are
not public, so they are not on the deck. The five compact cards close the deck
after the seven leads.

## Files

- `plates.py` — renders all twelve plates at 1200 × 400 (the five compact cards
  at 1200 × 260), 2x, using the deck fonts; plate 06 is clipped to 1200 × 376 so
  the try strip can sit close to it. HTML goes to the ignored `.build/` folder.
- `plate-01.png`, `plate-02.png`, `plate-03.png` … `plate-12.png`
  — the rendered plates. `plate-01.svg` wraps the Forge PNG and adds the ember
  pulse over the anvil; the other plates stay PNG.
- `stats.py` — writes the stack, project-section, try-it, open-to-work and
  review rails as SVG and renders the language line at 2x. HTML goes to the
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
  `deck-open.svg`, `deck-reviews.svg`, `deck-header.png`,
  `deck-footer.png` — the rendered data rails and board variants.

```bash
python3 assets/readme/prototype/plates.py
python3 assets/readme/prototype/stats.py
python3 assets/readme/prototype/boards.py
```

Once approved, the illustration slot can become a first-class field in
`build.py` for every project: an anvil and hammer for Forge, a theory notebook
for Financial-Market-Theories, a policy gate for AEGIS Fabric, a trading terminal
for Trading-Support-Tools, a seeded height field and core sample for Space, a
widget shell for dynamic-dashboard, an engine editor for ft_transcendence, a
terminal for minishell, a raycast view for cub3D, a protocol frame for ft_irc, a
Docker host for Inception, and a VM window on a hypervisor host for born2beroot.
