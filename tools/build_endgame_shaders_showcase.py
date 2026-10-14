import json
import base64
from pathlib import Path
from PIL import Image

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
OUT_DIR = Path("/tmp/endgame_previews")
OUT_DIR.mkdir(parents=True, exist_ok=True)

materials = [
    {
        "id": "cosmic_neutronium",
        "name": "Cosmic Neutronium",
        "loader": "gtna:cosmic",
        "effect": "Avaritia Cosmic Starfield",
        "desc": "Shader estelar dinâmico com céu infinito de estrelas móveis e glints cintilantes nos vértices.",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_cosmic_neutronium"),
        "color_badge": "bg-indigo-950/60 text-indigo-400 border-indigo-800/40"
    },
    {
        "id": "eternity",
        "name": "Eternity (En⦼)",
        "loader": "gtna:eternal",
        "effect": "Temporal Continuity Shader",
        "desc": "Animação contínua de 20 frames de fluxo temporal com halo celestial de resplendor puro.",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_eternity"),
        "color_badge": "bg-sky-950/60 text-sky-400 border-sky-800/40"
    },
    {
        "id": "magmatter",
        "name": "Magmatter",
        "loader": "gtna:halo",
        "effect": "Antimatter Magnetic Vacuum",
        "desc": "8 frames de pulso de contração magnética com halo de antimatéria escura (#212121).",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_magmatter"),
        "color_badge": "bg-rose-950/60 text-rose-400 border-rose-800/40"
    },
    {
        "id": "exo_halkonite",
        "name": "Exo-Halkonite",
        "loader": "gtna:cosmic",
        "effect": "Alien Exotic Plasma",
        "desc": "57 frames fluidos de plasma exótico alienígena com refração de energia extraterrestre.",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_exo_halkonite"),
        "color_badge": "bg-emerald-950/60 text-emerald-400 border-emerald-800/40"
    },
    {
        "id": "chaos_matter",
        "name": "Chaos Matter",
        "loader": "gtna:unstable",
        "effect": "Dimensional Unstable Fissure",
        "desc": "Shader de quebra dimensional e vácuo caótico com estática do Chaos Vortex.",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_chaos_matter"),
        "color_badge": "bg-purple-950/60 text-purple-400 border-purple-800/40"
    },
    {
        "id": "axonium",
        "name": "Axonium (煥律璨金)",
        "loader": "gtna:glow_edge",
        "effect": "Harmonic Golden Resonance",
        "desc": "Ouro cósmico harmônico do TST com ressonância áurea e bordas luminescentes.",
        "tex_path": Path("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_axonium"),
        "color_badge": "bg-amber-950/60 text-amber-400 border-amber-800/40"
    }
]

shapes = ["ingot", "plate", "gear", "rod"]
b64_data = {}

for mat in materials:
    mat_id = mat["id"]
    b64_data[mat_id] = {}
    tex_dir = mat["tex_path"]
    
    for shape in shapes:
        p_base = tex_dir / f"{shape}.png"
        p_ov = tex_dir / f"{shape}_overlay.png"
        
        if p_base.exists():
            base_im = Image.open(p_base).convert("RGBA")
            h = base_im.size[1]
            n_frames = max(1, h // 16)
            
            # Check overlay
            if p_ov.exists():
                ov_im = Image.open(p_ov).convert("RGBA")
                ov_h = ov_im.size[1]
                ov_frames = max(1, ov_h // 16)
            else:
                ov_im = None
                ov_frames = 1
                
            total_frames = max(n_frames, ov_frames)
            frames = []
            
            for f in range(min(total_frames, 30)):
                bf_idx = f % n_frames
                frame_base = base_im.crop((0, bf_idx * 16, 16, (bf_idx + 1) * 16))
                
                if ov_im:
                    of_idx = f % ov_frames
                    frame_ov = ov_im.crop((0, of_idx * 16, 16, (of_idx + 1) * 16))
                    comp = Image.alpha_composite(frame_base, frame_ov)
                else:
                    comp = frame_base
                    
                frames.append(comp)
                
            gif_file = OUT_DIR / f"{mat_id}_{shape}.gif"
            frames[0].save(
                gif_file,
                save_all=True,
                append_images=frames[1:],
                duration=80,
                loop=0,
                disposal=2
            )
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[mat_id][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[mat_id][shape] = ""

json_b64 = json.dumps(b64_data)

cards_html = ""
for mat in materials:
    mid = mat["id"]
    cards_html += f"""
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-slate-400 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-slate-800 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-{mid}" src="{b64_data[mid]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="{mat['name']}">
        </div>
        <div class="mt-3 font-bold text-sm text-[var(--foreground)]">{mat['name']}</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded {mat['color_badge']} font-mono border">
          {mat['effect']}
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          {mat['desc']}
        </p>
        <div class="mt-3 text-[11px] text-[var(--muted-foreground)] font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Loader: <span class="text-cyan-400">{mat['loader']}</span><br>
          • Fonte: <span class="text-purple-400">Modernity GTNH</span>
        </div>
      </div>
    """

html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-2">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-xl p-4 shadow-sm max-w-5xl mx-auto">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-[var(--border)] gap-2">
      <div>
        <h2 class="text-base font-bold text-[var(--foreground)] flex items-center gap-2">
          <span class="inline-block w-3 h-3 rounded-full bg-cyan-400 animate-pulse"></span>
          Shaders & Materiais Lendários do Endgame (GTNH / Modernity)
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Texturas autênticas do Modernity integradas com os loaders nativos de shaders do RenderBlender.</p>
      </div>
      <div class="flex items-center gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs">
        <button onclick="setShape('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-cyan-600 text-white transition-colors">Barra</button>
        <button onclick="setShape('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Placa</button>
        <button onclick="setShape('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Engrenagem</button>
        <button onclick="setShape('rod')" id="btn-rod" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Haste</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-4">
      {cards_html}
    </div>

    <!-- Footer info -->
    <div class="mt-4 pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-[var(--muted-foreground)]">
      <span>Todos os 6 materiais estão integrados com shaders e validados no compilador.</span>
      <span class="text-cyan-400 font-medium">Pronto para visualização no jogo!</span>
    </div>
  </div>

  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    const buttons = ['ingot', 'plate', 'gear', 'rod'];
    const mats = {json.dumps([m['id'] for m in materials])};

    function setShape(shape) {{
      currentShape = shape;
      buttons.forEach(b => {{
        const btn = document.getElementById('btn-' + b);
        if (b === shape) {{
          btn.className = 'px-2.5 py-1 rounded font-medium bg-cyan-600 text-white transition-colors';
        }} else {{
          btn.className = 'px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors';
        }}
      }});

      mats.forEach(mid => {{
        const img = document.getElementById('img-' + mid);
        if (img && data[mid] && data[mid][shape]) {{
          img.src = data[mid][shape];
        }}
      }});
    }}
  </script>
</body>
</html>
"""

target = ARTIFACT_DIR / "endgame_shaders_showcase.html"
target.write_text(html)
print(f"Showcase salvo com sucesso em: {target}")
