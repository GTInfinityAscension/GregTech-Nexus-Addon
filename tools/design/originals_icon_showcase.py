"""Builds the approval page for one material's three icon options (see originals_icon_variants.py).

Usage: python3 tools/design/originals_icon_showcase.py <spec.json> <gif dir> <out.html>
spec: {"material", "title", "lede", "shapes": [[id, label]], "options": [[name, description, effect]]}
"""

import base64
import json
import sys
from pathlib import Path

spec = json.loads(Path(sys.argv[1]).read_text())
gifs, out = Path(sys.argv[2]), Path(sys.argv[3])


def data(p, mime):
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


cards = ""
for n, (name, desc, fx) in enumerate(spec["options"], 1):
    cells = "".join(
        f'<figure><img src="{data(gifs / f"{spec["material"]}_opt{n}_{s}.gif", "image/gif")}" '
        f'alt="{label}, opção {n}" width="96" height="96"><figcaption>{label}</figcaption></figure>'
        for s, label in spec["shapes"])
    cards += (f'<section class="opt"><header><span class="n">Opção {n}</span><h2>{name}</h2></header>'
              f'<p>{desc}</p><p class="fx">Efeito no jogo: {fx}</p><div class="row">{cells}</div></section>')
accent = spec.get("accent", "#0f8f86")
accent_dark = spec.get("accent_dark", "#3fd6c8")
html = f"""<title>{spec["title"]}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono&display=swap">
<style>
/* Layout: uma coluna; cada opção é um painel com as formas do material */
:root{{--bg:#f2f1ef;--fg:#1d1a19;--muted:#5d5653;--card:#ffffff;--line:#dcd7d3;--accent:{accent};--slot:#8b8b8b;
--display:"Chakra Petch",system-ui,sans-serif;--body:"IBM Plex Sans",system-ui,sans-serif;--mono:"IBM Plex Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#141212;--fg:#eeeae7;--muted:#a9a19c;--card:#1d1a19;--line:#35302d;--accent:{accent_dark};color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#141212;--fg:#eeeae7;--muted:#a9a19c;--card:#1d1a19;--line:#35302d;--accent:{accent_dark};color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.55 var(--body)}}
main{{max-width:860px;margin:0 auto;padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:20px}}
h1,h2{{font-family:var(--display);margin:0;text-wrap:balance}} h1{{font-size:1.8rem}} h2{{font-size:1.2rem;color:var(--accent)}}
p{{margin:0;max-width:66ch}} .muted,.fx{{color:var(--muted)}} code{{font:.85em var(--mono)}}
.opt{{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px;display:grid;gap:10px;min-width:0}}
.opt header{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
.n{{font:600 .72rem var(--body);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}}
.row{{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px}}
figure{{margin:0;display:grid;gap:4px;justify-items:center}}
.row img{{image-rendering:pixelated;width:96px;height:96px;background:var(--slot);border-radius:2px}}
figcaption{{font-size:.8rem;color:var(--muted)}}
</style>
<main>
<header style="display:grid;gap:6px"><h1>{spec["title"]}</h1><p class="muted">{spec["lede"]}</p></header>
{cards}
</main>"""
out.write_text(html)
print(out)
