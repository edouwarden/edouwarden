#!/usr/bin/env python3
"""Build the GitHub profile poster (HTML -> PNG) for @edouwarden."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent
INK = "#191411"
PAPER = "#FFE9B5"
CREAM = "#FFF7E3"
ORANGE = "#F05A00"
AMBER = "#FFC400"
TEAL = "#00786D"

PROJECTS = [
    dict(
        num="01", title="The Sky Course", sub="ft_transcendence",
        year="2026", kind="42 Paris", role="Team lead · engine & frontend",
        accent=AMBER,
        text="Team lead on a real-time browser game. Four people, one life each, a custom "
             "Three.js engine and a Go backend holding the whole thing together.",
        tags=["TypeScript", "Next.js", "Three.js", "Go", "PostgreSQL"],
    ),
    dict(
        num="02", title="The Shell", sub="minishell",
        year="2025", kind="42 Paris", role="Solo project",
        accent=ORANGE,
        text="Bash rebuilt from scratch in C: lexing, expansion, pipes, redirections, signals, "
             "heredocs. No system(), no shell library — only readline for line editing.",
        tags=["C", "POSIX", "Processes", "210 h"],
    ),
    dict(
        num="03", title="The Maze", sub="cub3D",
        year="2025", kind="42 Paris", role="Solo project · bonus",
        accent=AMBER,
        text="A first-person maze raycast from a 2D map, textured floor to ceiling, every pixel "
             "written by hand into an X11 buffer. No GPU invited.",
        tags=["C", "Raycasting", "X11", "280 h"],
    ),
    dict(
        num="04", title="The Wire", sub="ft_irc",
        year="2026", kind="42 Paris", role="Solo project · bonus",
        accent=TEAL,
        text="An IRC server on one thread and one poll() loop: registration, channels, private "
             "messages, clean disconnects. Bonus: a local LLM wired into the chat.",
        tags=["C++98", "Sockets", "poll()", "Local LLM"],
    ),
    dict(
        num="05", title="The Bunker", sub="Inception",
        year="2026", kind="42 Paris", role="Solo project",
        accent=TEAL,
        text="A WordPress stack where every part is a container and exactly one port faces the "
             "internet: NGINX with TLS, PHP-FPM, MariaDB, secrets mounted at runtime.",
        tags=["Docker", "NGINX", "MariaDB", "TLS"],
    ),
    dict(
        num="06", title="The Vault", sub="Born2beroot",
        year="2024", kind="42 Paris", role="Solo project",
        accent=ORANGE,
        text="A Debian VM built the way a security team would: LUKS + LVM, one SSH port, "
             "unattended install, sudo logs and a monitoring broadcast every ten minutes.",
        tags=["Debian", "LUKS", "LVM", "Hardening"],
    ),
]
# ---------------------------------------------------------------- artwork ---
ART = {}

ART["01"] = f"""
<rect x="60" y="30" width="60" height="116" rx="4" class="cream ln"/>
<path d="M60 52 H120 M60 74 H120 M60 96 H120 M60 118 H120" class="ln"/>
<circle cx="73" cy="41" r="3.4" class="orange"/>
<circle cx="73" cy="63" r="3.4" class="teal"/>
<circle cx="73" cy="85" r="3.4" class="amber"/>
<circle cx="73" cy="107" r="3.4" class="teal"/>
<path d="M84 41 H112 M84 63 H112 M84 85 H112 M84 107 H112" class="ln3 ln"/>
<path d="M68 146 V153 M112 146 V153" class="ln"/>
<path d="M114 126 q-6 0 -7 7 l-2 8 q-2 10 8 10 h6 q6 0 8 -5 l3 -7 q2 -4 6 -4 h6 q4 0 6 4 l3 7 q2 5 8 5 h6 q10 0 8 -10 l-2 -8 q-1 -7 -7 -7 z" class="cream ln"/>
<path d="M132 140 h14 M139 133 v14" class="ln3 ln"/>
<circle cx="165" cy="136" r="4" class="orange ln3"/>
<circle cx="176" cy="144" r="4" class="amber ln3"/>
<path d="M123 130 q-10 4 -20 1" class="ln3 ln"/>
<path d="M172 34 l-16 32 h12 l-10 28 30 -39 h-13 l12 -21 z" class="amber ln"/>
<circle cx="40" cy="55" r="20" class="amber ln"/>
<text x="40" y="63" text-anchor="middle" class="bangers" font-size="22">2K</text>
<path d="M28 92 l-7 5 M190 120 l7 4 M26 66 l-8 -3" class="ln3 ln"/>
"""

ART["02"] = f"""
<path d="M64 55 L83 71 M156 55 L137 71 M64 132 L83 114 M156 132 L137 114" class="dash"/>
<rect x="34" y="33" width="31" height="38" rx="3" class="cream ln"/>
<path d="M57 33 l8 8 h-8 z" class="amber ln3"/>
<path d="M41 51 h16 M41 58 h16 M41 65 h10" class="ln3 ln"/>
<rect x="155" y="33" width="33" height="33" rx="3" class="cream ln"/>
<text x="171" y="57" text-anchor="middle" class="bangers" font-size="19">&lt;/&gt;</text>
<rect x="34" y="125" width="33" height="33" rx="3" class="cream ln"/>
<path d="M42 134 h17 v13 l-6 5 h-11 z" class="ln3 ln"/>
<path d="M52 146 l4 4 l8 -9" class="ln3 ln"/>
<rect x="154" y="125" width="34" height="34" rx="3" class="cream ln"/>
<path d="M160 142 q11 -12 22 0 q-11 12 -22 0 z" class="ln3 ln"/>
<circle cx="171" cy="142" r="4" class="teal"/>
<rect x="76" y="58" width="68" height="60" rx="11" class="cream ln"/>
<path d="M110 58 V43" class="ln"/>
<circle cx="110" cy="38" r="5" class="orange ln3"/>
<circle cx="96" cy="82" r="7" class="ink"/>
<circle cx="124" cy="82" r="7" class="ink"/>
<circle cx="98" cy="80" r="2.2" class="cream"/>
<circle cx="126" cy="80" r="2.2" class="cream"/>
<rect x="94" y="99" width="32" height="10" rx="2" class="ink"/>
<path d="M102 99 v10 M110 99 v10 M118 99 v10" class="cream" stroke="{CREAM}" stroke-width="2"/>
<path d="M80 126 v7 M132 126 v7" class="ln"/>
<path d="M70 45 l-5 -4 M150 45 l5 -4 M70 146 l-5 4 M150 146 l5 4" class="ln3 ln"/>
"""

ART["03"] = f"""
<path d="M110 58 L60 131 M110 58 L160 131 M60 131 L160 131" class="dash" stroke-dasharray="5 7"/>
<rect x="92" y="26" width="36" height="48" rx="4" class="cream ln"/>
<path d="M92 40 H128 M92 54 H128" class="ln3 ln"/>
<circle cx="100" cy="33" r="2.6" class="orange"/>
<circle cx="109" cy="33" r="2.6" class="teal"/>
<path d="M46 126 h30 l5 15 h-40 z" class="cream ln"/>
<rect x="48" y="108" width="26" height="18" rx="2" class="cream ln"/>
<path d="M52 113 h18 M52 118 h12" class="ln3 ln" stroke="{PAPER}"/>
<rect x="155" y="112" width="24" height="42" rx="4" class="cream ln"/>
<path d="M162 147 h10" class="ln3 ln"/>
<rect x="91" y="96" width="38" height="31" rx="4" class="amber ln"/>
<path d="M98 96 v-8 a12 12 0 0 1 24 0 v8" class="ln" fill="none"/>
<circle cx="110" cy="109" r="4.5" class="ink"/>
<path d="M110 113 v7" class="ln" stroke="{INK}" stroke-width="4"/>
<circle cx="173" cy="63" r="19" class="orange ln"/>
<text x="173" y="71" text-anchor="middle" class="bangers" font-size="24">0</text>
<path d="M72 84 l-6 -4 M148 84 l6 -4 M52 108 l-6 -3 M168 104 l7 -2" class="ln3 ln"/>
"""

ART["04"] = f"""
<path d="M40 42 V150 H184" class="ln"/>
<path d="M40 62 h144 M40 90 h144 M40 118 h144 M40 146 h144" class="grid"/>
<path d="M62 132 v-19 M62 105 v-8" class="ln"/><rect x="55" y="113" width="14" height="19" class="orange ln3"/>
<path d="M90 112 v-13 M90 92 v-7" class="ln"/><rect x="83" y="99" width="14" height="13" class="teal ln3"/>
<path d="M118 92 v-14 M118 68 v-7" class="ln"/><rect x="111" y="78" width="14" height="14" class="orange ln3"/>
<path d="M146 72 v-17 M146 48 v-7" class="ln"/><rect x="139" y="55" width="14" height="17" class="teal ln3"/>
<path d="M52 128 L90 102 L118 88 L170 52" class="ln" stroke-width="6"/>
<path d="M170 52 l-17 1 M170 52 l-2 17" class="ln" stroke-width="6"/>
<circle cx="170" cy="38" r="17" class="amber ln"/>
<text x="170" y="46" text-anchor="middle" class="bangers" font-size="21">$</text>
<rect x="130" y="118" width="42" height="30" rx="5" class="cream ln"/>
<path d="M151 118 v-5" class="ln3 ln"/><circle cx="151" cy="110" r="3" class="orange ln3"/>
<circle cx="143" cy="131" r="3" class="ink"/><circle cx="159" cy="131" r="3" class="ink"/>
<path d="M145 140 q6 4 12 0" class="ln3 ln"/>
<path d="M28 70 l-6 -3 M28 108 l-6 3" class="ln3 ln"/>
"""

ART["05"] = f"""
<path d="M42 148 h136 l-12 13 h-112 z" class="cream ln"/>
<rect x="58" y="78" width="104" height="72" rx="4" class="cream ln"/>
<path d="M58 141 l-8 7 M162 141 l8 7" class="ln"/>
<path d="M68 92 h26 M68 102 h44 M68 112 h36" class="ln3 ln" stroke="{TEAL}"/>
<path d="M136 92 h14 M136 102 h9" class="ln3 ln" stroke="{ORANGE}"/>
<circle cx="118" cy="88" r="39" class="lens ln" stroke-width="7"/>
<path d="M146 116 l25 25" class="ln" stroke-width="11" stroke-linecap="round"/>
<ellipse cx="118" cy="89" rx="11" ry="15" class="orange ln3"/>
<circle cx="118" cy="72" r="8" class="orange ln3"/>
<path d="M118 66 v-8 M112 59 l-5 -6 M124 59 l5 -6" class="ln3 ln"/>
<path d="M107 81 l-9 -4 M107 90 l-10 2 M109 99 l-6 8 M129 81 l9 -4 M129 90 l10 2 M127 99 l6 8" class="ln3 ln"/>
<path d="M118 80 v18" class="ln3 ln" stroke="{INK}"/>
<circle cx="111" cy="86" r="2" class="cream"/><circle cx="125" cy="86" r="2" class="cream"/>
<path d="M172 51 l9 16 h-18 z" class="amber ln"/><path d="M172 56 v6" class="ln3 ln"/><circle cx="172" cy="65" r="1.6" class="ink"/>
"""

ART["06"] = f"""
<path d="M32 62 q8 -10 18 -6 q4 -10 15 -8 q12 2 12 13 q10 1 8 10 h-50 q-8 -3 -3 -9 z" class="cream ln"/>
<path d="M172 44 q7 -8 15 -5 q3 -8 12 -6 q10 2 10 11 q8 1 6 8 h-40 q-7 -2 -3 -8 z" class="cream ln" opacity=".85"/>
<path d="M38 130 l42 -17 l42 17 l-42 17 z" class="orange ln"/>
<path d="M38 130 v12 l42 17 v-12 z" class="deep ln"/><path d="M122 130 v12 l-42 17 v-12 z" class="amber ln"/>
<path d="M84 90 l34 -13 l34 13 l-34 14 z" class="orange ln"/>
<path d="M84 90 v9 l34 14 v-9 z" class="deep ln"/><path d="M152 90 v9 l-34 14 v-9 z" class="amber ln"/>
<path d="M138 50 l28 -10 l28 10 l-28 11 z" class="orange ln"/>
<path d="M138 50 v7 l28 11 v-8 z" class="deep ln"/><path d="M194 50 v7 l-28 11 v-8 z" class="amber ln"/>
<circle cx="112" cy="61" r="8" class="cream ln"/><path d="M112 69 v18 M105 76 l-9 8 M119 76 l9 -7 M106 86 l-5 13 M118 86 l6 13" class="ln"/>
<path d="M106 69 l-13 -5 M106 73 l-14 3" class="orange ln3"/>
<path d="M180 26 v-16" class="ln"/><path d="M180 10 h24 v16 h-24 z" class="cream ln3"/>
<path d="M180 10 h8 v8 h8 v8" class="ink l3"/>
<path d="M40 36 l4 4 M28 48 l6 2 M204 78 l4 5" class="ln3 ln"/>
"""

ART["07"] = f"""
<rect x="38" y="40" width="144" height="102" rx="12" class="cream ln"/>
<rect x="50" y="52" width="120" height="72" rx="5" class="ink"/>
<path d="M58 68 h4 M66 68 h4 M74 68 h4" class="ln3 ln" stroke="{INK}"/>
<text x="60" y="88" class="mono" font-size="15" fill="{CREAM}">$ ls | grep .c</text>
<text x="60" y="108" class="mono" font-size="15" fill="{AMBER}">main.c</text>
<rect x="118" y="96" width="8" height="14" class="orange"/>
<path d="M54 142 h112 l12 18 h-136 z" class="cream ln"/>
<path d="M64 148 h6 M76 148 h6 M88 148 h6 M100 148 h6 M112 148 h6 M124 148 h6 M136 148 h6 M148 148 h6" class="ln3 ln"/>
<circle cx="177" cy="55" r="17" class="amber ln"/>
<path d="M177 44 v22" class="ln" stroke="{INK}" stroke-width="6"/>
<path d="M42 33 l-4 -6 M196 126 l6 5" class="ln3 ln"/>
"""

ART["08"] = f"""
<path d="M42 59 h74 a8 8 0 0 1 8 8 v22 a8 8 0 0 1 -8 8 h-50 l-14 13 v-13 h-10 a8 8 0 0 1 -8 -8 v-22 a8 8 0 0 1 8 -8 z" class="cream ln"/>
<circle cx="55" cy="78" r="4" class="ink"/><circle cx="69" cy="78" r="4" class="ink"/><circle cx="83" cy="78" r="4" class="ink"/>
<path d="M112 100 h66 a8 8 0 0 1 8 8 v22 a8 8 0 0 1 -8 8 h-40 l-12 11 v-11 h-14 a8 8 0 0 1 -8 -8 v-22 a8 8 0 0 1 8 -8 z" class="amber ln"/>
<path d="M126 120 h42 M126 130 h30" class="ln3 ln" stroke="{INK}"/>
<path d="M96 120 q10 18 22 5" class="ln" fill="none"/>
<rect x="88" y="113" width="10" height="14" rx="2" class="orange ln3" transform="rotate(-25 93 120)"/>
<circle cx="170" cy="53" r="19" class="teal ln"/>
<text x="170" y="62" text-anchor="middle" class="bangers" font-size="24" fill="{CREAM}">#</text>
<path d="M156 26 q6 -8 14 -2 M162 18 q8 -9 17 -1" class="ln3 ln"/>
<path d="M28 52 l-6 -4 M30 112 l-7 2 M188 92 l7 3" class="ln3 ln"/>
"""

ART["09"] = f"""
<defs><clipPath id="c9"><circle cx="110" cy="94" r="74"/></clipPath></defs>
<g clip-path="url(#c9)">
<rect x="36" y="20" width="148" height="150" class="cream"/>
<path d="M36 150 L110 92 L184 150 z" class="amber ln"/>
<path d="M36 35 L110 92 L184 35 v-15 h-148 z" class="cream ln"/>
<path d="M36 35 L110 92 L36 150 M184 35 L110 92 L184 150" class="deep ln"/>
<path d="M36 58 L110 92 M36 82 L110 92 M36 122 L110 92 M36 145 L110 92 M184 58 L110 92 M184 82 L110 92 M184 122 L110 92 M184 145 L110 92" class="ln3 ln"/>
<path d="M74 150 L110 92 L146 150 M96 150 L110 92 L124 150 M58 122 L110 92 L162 122 M48 78 L110 92 L172 78" class="ln3 ln"/>
<path d="M36 60 H184 M36 92 H184 M36 124 H184" class="ln3 ln"/>
<path d="M36 92 V35 M184 92 V35" class="ln"/>
<rect x="100" y="76" width="20" height="30" class="teal ln"/>
<circle cx="110" cy="91" r="2.5" class="amber"/>
<path d="M36 150 h148" class="ln"/>
</g>
<circle cx="110" cy="94" r="74" class="ln" fill="none" stroke-width="6"/>
<path d="M32 44 l-6 -6 M188 44 l6 -6" class="ln3 ln"/>
"""

ART["10"] = f"""
<path d="M126 8 V26" class="ln"/><path d="M108 26 H144" class="ln"/>
<path d="M126 26 V38 M120 32 h12" class="ln3 ln"/>
<path d="M58 66 L146 54 L192 78 L104 91 Z" class="amber ln"/>
<path d="M58 66 L104 91 L104 148 L58 123 Z" class="cream ln"/>
<path d="M104 91 L192 78 L192 135 L104 148 Z" class="deep ln"/>
<path d="M66 69 V127 M74 71 V130 M82 73 V133 M90 76 V136 M98 78 V139" class="ln3 ln"/>
<path d="M116 90 V146 M128 88 V144 M140 86 V142 M152 84 V140 M164 82 V138 M176 80 V136 M188 78 V134" class="cream" stroke="{CREAM}" stroke-width="2.4"/>
<path d="M70 38 L160 26 L204 50 L114 63 Z" class="orange ln"/>
<path d="M70 38 L114 63 L114 90 L70 65 Z" class="cream ln"/>
<path d="M114 63 L204 50 L204 76 L114 90 Z" class="amber ln"/>
<path d="M78 41 V67 M86 43 V70 M94 46 V73 M102 49 V76 M110 52 V79" class="ln3 ln"/>
<path d="M126 62 V88 M138 60 V86 M150 58 V84 M162 56 V82 M174 54 V80 M186 52 V78" class="cream" stroke="{CREAM}" stroke-width="2.4"/>
<rect x="72" y="100" width="27" height="30" rx="4" class="cream ln"/>
<path d="M79 100 v-7 a7 7 0 0 1 14 0 v7" class="ln" fill="none"/>
<circle cx="85" cy="112" r="4" class="ink"/><path d="M85 116 v6" class="ln" stroke="{INK}" stroke-width="4"/>
<path d="M193 96 h13 v20 h-13" class="ln" fill="none"/>
<text x="199" y="92" text-anchor="middle" class="mono" font-size="10" fill="{INK}">443</text>
<path d="M32 156 q12 -7 24 0 q12 7 24 0 q12 -7 24 0 q12 7 24 0 q12 -7 24 0 q12 7 24 0" class="ln3 ln" stroke="{TEAL}"/>
<path d="M36 44 l-6 -5 M198 44 l6 -5" class="ln3 ln"/>
"""

ART["11"] = f"""
<circle cx="110" cy="94" r="64" class="cream ln" stroke-width="6"/>
<circle cx="110" cy="94" r="49" class="ln3 ln" fill="none"/>
<g>
<circle cx="110" cy="30" r="4" class="ink"/><circle cx="110" cy="158" r="4" class="ink"/>
<circle cx="46" cy="94" r="4" class="ink"/><circle cx="174" cy="94" r="4" class="ink"/>
<circle cx="65" cy="49" r="4" class="ink"/><circle cx="155" cy="49" r="4" class="ink"/>
<circle cx="65" cy="139" r="4" class="ink"/><circle cx="155" cy="139" r="4" class="ink"/>
</g>
<circle cx="110" cy="94" r="13" class="amber ln"/>
<path d="M110 81 V60 M110 107 v21 M97 94 H76 M123 94 h21 M101 85 L86 70 M119 103 l15 15 M119 85 l15 -15 M101 103 l-15 15" class="ln" stroke-width="4"/>
<circle cx="110" cy="94" r="6" class="ink"/>
<rect x="146" y="126" width="46" height="34" rx="3" class="teal ln"/>
<path d="M153 136 h32 M153 143 h20" class="ln3 ln" stroke="{CREAM}"/>
<path d="M158 160 v5 M180 160 v5" class="ln"/>
<path d="M28 52 l-6 -4 M38 158 l-5 4" class="ln3 ln"/>
"""


# keep only the public repo artwork, renumbered for the new card order
for _old, _new in [("06", "01"), ("07", "02"), ("09", "03"), ("08", "04"), ("10", "05"), ("11", "06")]:
    ART[_new] = ART.pop(_old)

def art_svg(num, accent):
    return f"""<svg class="art-svg" viewBox="0 0 220 190" preserveAspectRatio="xMidYMid meet">
  <circle cx="110" cy="94" r="76" fill="{accent}"/>
  <circle cx="110" cy="94" r="76" fill="url(#dotsCream)" opacity=".26"/>
  <circle cx="110" cy="94" r="76" fill="none" stroke="{INK}" stroke-width="3.5"/>
  {ART[num]}
</svg>"""


def card(p):
    tags = "".join(f"<span>{t}</span>" for t in p["tags"])
    return f"""
<article class="card" style="--accent:{p['accent']}">
  <div class="art">
    {art_svg(p['num'], p['accent'])}
    <span class="fig">FIG. {p['num']}</span>
  </div>
  <div class="copy">
    <div class="meta">
      <span class="num">{p['num']}</span>
      <span class="kind {'school' if p['kind']=='42 Paris' else ''}">{p['kind']}</span>
      <span class="year">{p['year']}</span>
    </div>
    <h2>{p['title']}</h2>
    <div class="sub">{p['sub']} <i>· {p['role']}</i></div>
    <p>{p['text']}</p>
    <div class="tags">{tags}</div>
  </div>
</article>"""


CSS = """
@font-face{font-family:'Bangers';src:url('fonts/Bangers-Regular.ttf');}
@font-face{font-family:'Anton';src:url('fonts/Anton-Regular.ttf');}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-Regular.ttf');font-weight:400;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-Medium.ttf');font-weight:500;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-SemiBold.ttf');font-weight:600;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-Bold.ttf');font-weight:700;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-ExtraBold.ttf');font-weight:800;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-Black.ttf');font-weight:900;}
@font-face{font-family:'Barlow';src:url('fonts/BarlowCondensed-Italic.ttf');font-style:italic;font-weight:400;}
@font-face{font-family:'Elite';src:url('fonts/SpecialElite-Regular.ttf');}

*{box-sizing:border-box;}
html,body{margin:0;padding:0;background:#F2D69E;}
body{width:846px;overflow-x:hidden;font-family:'Barlow';color:#191411;}
::-webkit-scrollbar{display:none;}

.poster{position:relative;width:846px;overflow:hidden;padding:16px 18px 0;
  background:
    radial-gradient(circle at 78% 2%, rgba(242,167,27,.25), transparent 24%),
    radial-gradient(circle at 4% 20%, rgba(232,90,24,.13), transparent 22%),
    linear-gradient(180deg,#F7E8C8 0%, #FFE9B5 42%, #FFE1A6 100%);
}
.poster:before{content:'';position:absolute;inset:0;background:url('grain.png');opacity:.55;mix-blend-mode:multiply;pointer-events:none;z-index:60;}
.poster:after{content:'';position:absolute;inset:0;background:url('blotch.png');opacity:.7;mix-blend-mode:multiply;pointer-events:none;z-index:59;}

.edge{position:absolute;inset:8px;border:2px solid rgba(25,20,17,.45);pointer-events:none;z-index:58;}
.crop{position:absolute;width:14px;height:14px;z-index:58;opacity:.55;}
.crop.tl{top:4px;left:4px;border-top:2px solid #191411;border-left:2px solid #191411;}
.crop.tr{top:4px;right:4px;border-top:2px solid #191411;border-right:2px solid #191411;}
.crop.bl{bottom:4px;left:4px;border-bottom:2px solid #191411;border-left:2px solid #191411;}
.crop.br{bottom:4px;right:4px;border-bottom:2px solid #191411;border-right:2px solid #191411;}

/* ---------- masthead ---------- */
.topline{position:relative;z-index:2;display:flex;align-items:center;justify-content:space-between;
  border-bottom:3px solid #191411;padding:0 2px 6px;font-family:'Elite';font-size:11px;letter-spacing:.6px;text-transform:uppercase;}
.topline b{font-family:'Barlow';font-weight:800;letter-spacing:2px;font-size:12px;}
.hero{position:relative;z-index:2;display:grid;grid-template-columns:1fr 280px;gap:4px;padding:10px 0 0;}
.hero-copy{position:relative;z-index:1;}
.hero-copy:before{content:'';position:absolute;left:-16px;top:52px;width:390px;height:190px;z-index:-1;
  background-image:radial-gradient(#F05A00 1.35px, transparent 1.55px);background-size:9px 9px;opacity:.16;transform:rotate(-2deg);}
.kicker{display:inline-block;background:#191411;color:#FFF7E3;font-weight:800;text-transform:uppercase;
  letter-spacing:2.4px;font-size:12.5px;padding:4px 9px 3px;transform:rotate(-.6deg);}
h1{font-family:'Anton';font-weight:400;font-size:104px;line-height:.86;margin:12px 0 3px 8px;
  letter-spacing:4px;text-transform:uppercase;
  background:linear-gradient(180deg,#FFFDF2 0%,#FFE28A 16%,#FFC400 44%,#F05A00 78%,#C43D00 100%);
  -webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent;
  -webkit-text-stroke:3px #191411;paint-order:stroke fill;
  text-shadow:4px 4px 0 #F05A00, 7px 7px 0 #191411;
  transform:skew(-7deg) rotate(-1deg);transform-origin:left bottom;position:relative;z-index:1;}
.handle{display:flex;align-items:center;gap:8px;font-family:'Elite';font-size:13px;letter-spacing:.4px;margin-top:13px;}
.handle:before{content:'';width:30px;height:3px;background:#F05A00;}
.subline{font-family:'Anton';text-transform:uppercase;letter-spacing:1.2px;font-size:14px;margin-top:9px;}
.subline span{background:#F05A00;color:#fff8e6;padding:2px 6px;margin-right:5px;}
.toolkit{margin-top:15px;max-width:440px;border-top:2px solid #191411;padding-top:6px;font-size:10.8px;font-weight:700;
  letter-spacing:1.25px;text-transform:uppercase;}
.toolkit b{display:inline-block;background:#F05A00;color:#FFF7E3;padding:1px 5px 0;margin-right:6px;letter-spacing:1.6px;}
.portrait-wrap{position:relative;height:100%;min-height:264px;display:flex;align-items:center;justify-content:center;}
.burst{position:absolute;width:270px;height:270px;left:50%;top:50%;transform:translate(-50%,-50%) rotate(8deg);z-index:0;}
.portrait{position:relative;z-index:1;width:224px;height:224px;object-fit:cover;border-radius:50%;
  border:4px solid #191411;box-shadow:7px 7px 0 #191411;background:#FFC400;}
.sticker{position:absolute;z-index:3;right:0;bottom:6px;background:#FFF7E3;border:3px solid #191411;
  font-family:'Bangers';font-size:19px;padding:2px 10px 1px;transform:rotate(6deg);box-shadow:3px 3px 0 #191411;}
.tape{position:absolute;z-index:4;width:86px;height:24px;background:rgba(238,207,145,.78);border:1px solid rgba(25,20,17,.25);
  box-shadow:0 1px 2px rgba(0,0,0,.12);transform:rotate(-8deg);left:2px;top:-4px;mix-blend-mode:multiply;}

.bubble{position:relative;z-index:2;margin:8px 0 0;background:#FFFDF2;border:3px solid #191411;
  box-shadow:5px 5px 0 #191411;padding:10px 14px 10px;font-size:17px;font-weight:500;line-height:1.24;letter-spacing:.1px;}
.bubble b{font-weight:800;}
.bubble:after{content:'';position:absolute;left:41px;bottom:-16px;width:0;height:0;border-top:16px solid #191411;border-right:17px solid transparent;}
.bubble:before{content:'';position:absolute;left:44px;bottom:-10px;width:0;height:0;border-top:11px solid #FFFDF2;border-right:12px solid transparent;z-index:1;}
.bubble .hi{background:linear-gradient(transparent 58%, #FFC400 58%);font-weight:700;}

.stats{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,1fr);background:#191411;color:#FFF7E3;
  margin:22px 0 0;border:3px solid #191411;}
.stats div{padding:8px 6px 7px;text-align:center;border-right:2px solid #F05A00;}
.stats div:last-child{border-right:0;}
.stats b{display:block;font-family:'Bangers';font-weight:400;font-size:25px;line-height:1;color:#FFC400;letter-spacing:1px;}
.stats span{display:block;font-family:'Barlow';font-weight:700;font-size:10.5px;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;}

/* ---------- section title ---------- */
.section{position:relative;z-index:2;margin:26px 0 16px;padding-left:28px;display:flex;align-items:flex-end;justify-content:space-between;}
.section .big{position:relative;font-family:'Bangers';font-size:60px;line-height:.85;letter-spacing:1px;
  color:#FFF7E3;-webkit-text-stroke:3px #191411;paint-order:stroke fill;text-shadow:5px 5px 0 #F05A00,8px 8px 0 #191411;transform:rotate(-1deg);}
.section .big em{font-style:normal;color:#FFC400;}
.section .note{font-family:'Elite';font-size:10.5px;text-align:right;line-height:1.45;text-transform:uppercase;padding-bottom:4px;}
.section .note b{font-family:'Barlow';font-weight:800;font-size:11px;letter-spacing:1.4px;}
.section:before{content:'';position:absolute;left:36px;top:-22px;width:310px;height:104px;z-index:-2;
  background-image:radial-gradient(#F05A00 1.5px, transparent 1.7px);background-size:8px 8px;opacity:.18;transform:rotate(-2deg);}

/* ---------- cards ---------- */
.cards{position:relative;z-index:2;}
.card{display:grid;grid-template-columns:214px 1fr;min-height:192px;background:#FFF7E3;border:3.5px solid #191411;
  box-shadow:6px 6px 0 #191411;margin:0 0 20px;position:relative;}
.card:after{content:'';position:absolute;right:-10px;top:34px;width:7px;height:44px;background:#F05A00;border:2px solid #191411;transform:rotate(2deg);}
.art{position:relative;border-right:3.5px solid #191411;background:
  radial-gradient(circle at 30% 20%, rgba(255,255,255,.4), transparent 50%), #FFF0CC;overflow:hidden;}
.art-svg{position:absolute;inset:0;width:100%;height:100%;}
.fig{position:absolute;left:7px;bottom:5px;font-family:'Elite';font-size:9px;letter-spacing:.6px;background:#191411;color:#FFF7E3;padding:1px 5px;transform:rotate(-1deg);}
.copy{padding:11px 14px 10px 15px;position:relative;min-width:0;}
.meta{display:flex;align-items:center;gap:8px;height:23px;}
.num{font-family:'Bangers';font-size:30px;line-height:1;color:#F05A00;-webkit-text-stroke:1.3px #191411;paint-order:stroke fill;letter-spacing:1px;}
.kind{font-family:'Barlow';font-weight:800;font-size:9.5px;letter-spacing:1.5px;text-transform:uppercase;
  background:#FFC400;border:2px solid #191411;padding:1px 5px;transform:rotate(-1deg);}
.kind.school{background:#00786D;color:#FFF7E3;}
.year{margin-left:auto;font-family:'Elite';font-size:11px;letter-spacing:.4px;}
h2{font-family:'Anton';font-weight:400;font-size:31px;line-height:.98;margin:1px 0 0;text-transform:uppercase;letter-spacing:.2px;}
.sub{font-weight:700;font-size:13.5px;letter-spacing:.3px;margin-top:2px;text-transform:uppercase;}
.sub i{font-weight:500;font-style:normal;color:#A63E00;}
p{font-size:15.4px;font-weight:500;line-height:1.22;margin:6px 0 7px;letter-spacing:.05px;}
.tags{display:flex;flex-wrap:wrap;gap:5px;}
.tags span{font-weight:700;font-size:9.8px;letter-spacing:1px;text-transform:uppercase;border:1.6px solid #191411;
  padding:1px 5px 0;background:#FFE9B5;box-shadow:1.5px 1.5px 0 #191411;}
.card:nth-child(even){transform:rotate(.12deg);}
.card:nth-child(odd){transform:rotate(-.1deg);}

/* ---------- footer ---------- */
.footer{position:relative;z-index:2;margin:12px -18px 0;background:#191411;color:#FFF7E3;padding:18px 22px 20px;
  border-top:4px solid #F05A00;}
.footer .row{display:flex;align-items:center;justify-content:space-between;gap:16px;}
.footer .shout{font-family:'Bangers';font-size:46px;line-height:.9;color:#FFC400;letter-spacing:1px;transform:rotate(-1deg);}
.footer .shout span{color:#FFF7E3;}
.footer .side{text-align:right;font-family:'Elite';font-size:10.5px;line-height:1.5;text-transform:uppercase;}
.footer .side b{font-family:'Barlow';font-weight:800;font-size:13px;letter-spacing:1.1px;}
.footer .rule{height:2px;background:#F05A00;margin:12px 0 9px;opacity:.75;}
.footer .bottom{display:flex;align-items:center;justify-content:space-between;font-family:'Elite';font-size:9.5px;letter-spacing:.5px;text-transform:uppercase;}
.barcode{width:88px;height:24px;background:repeating-linear-gradient(90deg,#FFF7E3 0 2px,#191411 2px 4px,#FFF7E3 4px 7px,#191411 7px 8px);}
.stamp{position:absolute;right:22px;top:-23px;width:96px;height:46px;border:3px double #F05A00;color:#F05A00;
  font-family:'Bangers';font-size:16px;text-align:center;line-height:1.05;padding-top:5px;transform:rotate(-8deg);opacity:.9;background:rgba(25,20,17,.15);}

/* svg */
.ln{fill:none;stroke:#191411;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;}
.ln3{fill:none;stroke:#191411;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;}
.dash{fill:none;stroke:#191411;stroke-width:3;stroke-linecap:round;stroke-dasharray:5 7;}
.grid{fill:none;stroke:#191411;stroke-width:1.6;opacity:.35;stroke-dasharray:3 4;}
.ink{fill:#191411;}
.cream{fill:#FFF7E3;}
.orange{fill:#F05A00;}
.amber{fill:#FFC400;}
.teal{fill:#00786D;}
.deep{fill:#C43D00;}
.lens{fill:rgba(255,248,230,.55);}
.bangers{font-family:'Bangers';fill:#191411;letter-spacing:1px;}
.mono{font-family:'Elite';}
"""


def build_html():
    cards = "".join(card(p) for p in PROJECTS)
    burst = """<svg class="burst" viewBox="0 0 300 300"><path d="M150 4 L171 41 L208 18 L215 60 L258 52 L247 93 L288 100 L263 132 L298 153 L265 172 L286 209 L246 213 L251 255 L211 243 L198 283 L167 257 L150 296 L133 257 L102 283 L89 243 L49 255 L54 213 L14 209 L35 172 L2 153 L37 132 L12 100 L53 93 L42 52 L85 60 L92 18 L129 41 Z" fill="#FFC400" stroke="#191411" stroke-width="4"/></svg>"""
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Edouard — profile poster</title>
<link rel="stylesheet" href="style.css"></head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<pattern id="dotsCream" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.5" fill="#FFF7E3"/></pattern>
<pattern id="dotsInk" width="7" height="7" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#191411"/></pattern>
</defs></svg>
<div class="poster">
  <div class="edge"></div><div class="crop tl"></div><div class="crop tr"></div><div class="crop bl"></div><div class="crop br"></div>
  <div class="topline"><span><b>PROFILE COMICS</b> · PARIS</span><span>VOL. 1 — ISSUE 01</span><span>PUBLIC EDITION · 2026</span></div>

  <header class="hero">
    <div class="hero-copy">
      <div class="kicker">Self-taught software engineer</div>
      <h1>EDOUARD</h1>
      <div class="handle">@edouwarden · github.com/edouwarden</div>
      <div class="subline"><span>42 PARIS</span> AI-AUGMENTED · INFRA · APPSEC</div>
      <div class="toolkit"><b>TOOLKIT</b> C · Python · TypeScript · Bash · Java · SQL · Go</div>
    </div>
    <div class="portrait-wrap">
      {burst}
      <img class="portrait" src="portrait.png" alt="Comic-style portrait of Edouard at a retro computer">
      <div class="sticker">42 PARIS</div>
    </div>
  </header>

  <div class="bubble">I build systems <b>end to end</b> — bare metal, networks, engines, AI agents. I like <span class="hi">hard constraints</span>, because they force elegant solutions. Currently at 42 Paris, shipping anyway.</div>

  <div class="stats">
    <div><b>13 YRS</b><span>coding since age 9</span></div>
    <div><b>2,000+</b><span>players served</span></div>
    <div><b>€0</b><span>infra bill</span></div>
    <div><b>214</b><span>peer reviews</span></div>
  </div>

  <div class="section">
    <div class="big">THE <em>PROJECTS</em></div>
    <div class="note"><b>6 PUBLIC REPOS · 2024—2026</b><br>in order of importance<br>(my call)</div>
  </div>

  <div class="cards">{cards}</div>

  <footer class="footer">
    <div class="stamp">SHIP<br>IT</div>
    <div class="row">
      <div class="shout">STILL <span>COMPILING.</span></div>
      <div class="side"><b>NEXT ISSUE:</b><br>whatever breaks next.<br>Paris, France · 2026</div>
    </div>
    <div class="rule"></div>
    <div class="bottom"><span>© 2026 Edouard · hand-coded & hand-inked</span><span class="barcode"></span><span>Printed on recycled packets</span></div>
  </footer>
</div>
</body></html>"""


def main():
    (ROOT / "poster.html").write_text(build_html(), encoding="utf-8")
    (ROOT / "style.css").write_text(CSS, encoding="utf-8")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 846, "height": 1200}, device_scale_factor=2)
        page.goto((ROOT / "poster.html").as_uri())
        page.wait_for_timeout(500)
        page.evaluate("document.fonts.ready")
        height = page.evaluate("document.querySelector('.poster').getBoundingClientRect().height")
        print("poster height:", height)
        raw = ROOT / "_poster-raw.png"
        page.screenshot(path=str(raw), full_page=True)
        browser.close()

    master = Image.open(raw).convert("RGB")
    # exact 846 px wide for the README, plus a 2x master
    master.resize((846, round(master.height * 846 / master.width)), Image.LANCZOS).quantize(
        colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG
    ).save(ROOT / "profile-poster.png", optimize=True)
    master.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG).save(
        ROOT / "profile-poster@2x.png", optimize=True
    )
    raw.unlink()
    print("written", ROOT / "profile-poster.png", "and", ROOT / "profile-poster@2x.png")


if __name__ == "__main__":
    main()
