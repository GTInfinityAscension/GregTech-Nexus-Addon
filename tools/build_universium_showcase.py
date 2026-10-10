import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/universium_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

shapes = ["ingot", "plate", "gear", "block"]
options = [0, 1, 2, 3]

b64_data = {}
for opt in options:
    b64_data[opt] = {}
    for shape in shapes:
        gif_file = OUT_DIR / f"universium_opt{opt}_{shape}.gif"
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[opt][shape] = ""

json_b64 = json.dumps(b64_data)

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
          <span class="inline-block w-3 h-3 rounded-full bg-purple-400 animate-pulse"></span>
          Universium (Σ§kX) — Modernity GTNH vs 3 Reworks Modernos
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Comparativo entre o sprite estático do Modernity GTNH e 3 opções fluidas de 30 frames.</p>
      </div>
      <div class="flex items-center gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs">
        <button onclick="setShape('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-purple-600 text-white transition-colors">Barra</button>
        <button onclick="setShape('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Placa</button>
        <button onclick="setShape('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Engrenagem</button>
        <button onclick="setShape('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Bloco</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-4">
      
      <!-- Opção 0 (Modernity GTNH Original) -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-slate-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-slate-700/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt0" src="{b64_data[0]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Modernity Original">
        </div>
        <div class="mt-3 font-bold text-sm text-slate-300">Modernity GTNH</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono border border-slate-700">
          Original (Estático)
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Sprite original do Modernity GTNH. Metal grafite/ardósia escuro com subtom índigo (#4a4957) e contorno de bisel claro. Totalmente estático (sem animação).
        </p>
        <div class="mt-3 text-[11px] text-slate-400 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Estilo: Ardósia/chumbo cósmico<br>
          • Ritmo: Estático (1 frame)<br>
          • Paleta: #1a1a20 a #616075
        </div>
      </div>

      <!-- Opção 1 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-purple-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-purple-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt1" src="{b64_data[1]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 1">
        </div>
        <div class="mt-3 font-bold text-sm text-purple-300">1. Event Horizon</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-purple-950/60 text-purple-400 font-mono border border-purple-800/40">
          Anel Doppler Relativístico
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Singularidade cósmica com disco de acreção em rotação relativística, efeito Doppler beaming (ciano ao aproximar) e feixes de radiação estelar de alta energia.
        </p>
        <div class="mt-3 text-[11px] text-purple-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Estilo: Singularidade relativística<br>
          • Ritmo: Rotação de acreção (30 frames)<br>
          • Destaque: Feixe ciano-violeta Doppler
        </div>
      </div>

      <!-- Opção 2 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-fuchsia-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-fuchsia-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt2" src="{b64_data[2]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 2">
        </div>
        <div class="mt-3 font-bold text-sm text-fuchsia-300">2. Prismatic Caustics</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-fuchsia-950/60 text-fuchsia-400 font-mono border border-fuchsia-800/40">
          Refração Hipercristalina
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Metal hiper-denso com dispersão espectral interna. Cáusticas geométricas prismáticas que se decompõem nas cores do arco-íris cósmico através das facetas.
        </p>
        <div class="mt-3 text-[11px] text-fuchsia-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Estilo: Cristalino multifacetado<br>
          • Ritmo: Ondulação espectral (30 frames)<br>
          • Destaque: Aberração cromática RGB
        </div>
      </div>

      <!-- Opção 3 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-indigo-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-indigo-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt3" src="{b64_data[3]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 3">
        </div>
        <div class="mt-3 font-bold text-sm text-indigo-300">3. Spiral Collision</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-indigo-950/60 text-indigo-400 font-mono border border-indigo-800/40">
          Braços Espirais & Starburst
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Fusão de duas galáxias espirais com braços logarítmicos entrelaçados. Ondas de choque gravitacional acendem pontualmente berçários de estrelas cintilantes.
        </p>
        <div class="mt-3 text-[11px] text-indigo-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Estilo: Galáctico astronômico<br>
          • Ritmo: Rotação diferencial (30 frames)<br>
          • Destaque: Starbursts pontuais cintilantes
        </div>
      </div>

    </div>

    <!-- Footer info -->
    <div class="mt-4 pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-[var(--muted-foreground)]">
      <span>Deseja adotar uma das opções modernas (<strong>1, 2, 3</strong>) ou prefere manter a do <strong>Modernity original</strong>?</span>
      <span class="text-purple-400 font-medium">Basta responder sua preferência (0 para Modernity original, ou 1, 2, 3).</span>
    </div>
  </div>

  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    const buttons = ['ingot', 'plate', 'gear', 'block'];

    function setShape(shape) {{
      currentShape = shape;
      buttons.forEach(b => {{
        const btn = document.getElementById('btn-' + b);
        if (b === shape) {{
          btn.className = 'px-2.5 py-1 rounded font-medium bg-purple-600 text-white transition-colors';
        }} else {{
          btn.className = 'px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors';
        }}
      }});

      for (let opt = 0; opt <= 3; opt++) {{
        const img = document.getElementById('img-opt' + opt);
        if (img && data[opt] && data[opt][shape]) {{
          img.src = data[opt][shape];
        }}
      }}
    }}
  </script>
</body>
</html>
"""

target = ARTIFACT_DIR / "universium_preview.html"
target.write_text(html)
print(f"Showcase salvo com sucesso em: {target}")
