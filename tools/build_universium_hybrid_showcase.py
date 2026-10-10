import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/universium_hybrid_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
USER_IMG = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06/.user_uploaded/media_1791473914510.png")

shapes = ["ingot", "plate", "gear", "block"]
options = [1, 2, 3]

b64_data = {}
for opt in options:
    b64_data[opt] = {}
    for shape in shapes:
        gif_file = OUT_DIR / f"universium_hybrid_opt{opt}_{shape}.gif"
        if gif_file.exists():
            b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
            b64_data[opt][shape] = f"data:image/gif;base64,{b64}"
        else:
            b64_data[opt][shape] = ""

# Modernity/GTNH original opt0
b64_opt0 = {}
for shape in shapes:
    gif_file = Path("/tmp/universium_candidates") / f"universium_opt0_{shape}.gif"
    if gif_file.exists():
        b64 = base64.b64encode(gif_file.read_bytes()).decode("utf-8")
        b64_opt0[shape] = f"data:image/gif;base64,{b64}"
    else:
        b64_opt0[shape] = ""

json_b64 = json.dumps(b64_data)
json_b64_0 = json.dumps(b64_opt0)

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
          Universium (Σ§kX) — Fusão: Opção 3 + Starfield GTNH
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Combinação do fundo estelar/crista branca do GTNH com a dinâmica espiral da Opção 3.</p>
      </div>
      <div class="flex items-center gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs">
        <button onclick="setShape('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-cyan-600 text-white transition-colors">Barra</button>
        <button onclick="setShape('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Placa</button>
        <button onclick="setShape('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Engrenagem</button>
        <button onclick="setShape('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors">Bloco</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-4">
      
      <!-- Opção 3A -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-cyan-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-cyan-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt1" src="{b64_data[1]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 3A">
        </div>
        <div class="mt-3 font-bold text-sm text-cyan-300">3A. Galactic Starfield Spiral</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-cyan-950/60 text-cyan-400 font-mono border border-cyan-800/40">
          Órbita Estelar Suave & Crista Metálica
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          As estrelas (ciano, lilás e brancas) giram suavemente em órbitas galácticas acompanhando os dois braços espirais. A crista branca pura do GTNH tem um reflexo metálico fluido.
        </p>
        <div class="mt-3 text-[11px] text-cyan-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Fundo: Azul-marinho cósmico GTNH (#172343)<br>
          • Movimento: Órbitas estelares completas<br>
          • Crista: Branco puro com sheen suave
        </div>
      </div>

      <!-- Opção 3B -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-blue-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-blue-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt2" src="{b64_data[2]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 3B">
        </div>
        <div class="mt-3 font-bold text-sm text-blue-300">3B. Avaritia Nebula Starburst</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-blue-950/60 text-blue-400 font-mono border border-blue-800/40">
          Vórtice Cósmico & Flashes de Supernova
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Nebulosa com ondas de densidade estelar. Quando os braços espirais colidem, ocorrem <em>starbursts</em> (cintilações explosivas em cruz 3x3 com faíscas cósmicas).
        </p>
        <div class="mt-3 text-[11px] text-blue-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Fundo: Nebulosa com contraste dinâmico<br>
          • Movimento: Flashes de starbursts pontuais<br>
          • Crista: Branco níveo com pulso celeste
        </div>
      </div>

      <!-- Opção 3C -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-purple-500 transition-colors relative group">
        <div class="w-24 h-24 bg-slate-950 rounded-lg border border-purple-900/60 flex items-center justify-center p-2 shadow-inner relative overflow-hidden">
          <img id="img-opt3" src="{b64_data[3]['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Opção 3C">
        </div>
        <div class="mt-3 font-bold text-sm text-purple-300">3C. Relativistic Keplerian Drift</div>
        <div class="mt-1 text-[11px] px-2 py-0.5 rounded bg-purple-950/60 text-purple-400 font-mono border border-purple-800/40">
          Rotação Diferencial de Acreção
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-2 leading-relaxed">
          Velocidade de rotação física diferencial: o centro gira muito mais rápido que as bordas exteriores, simulando um buraco negro supermassivo no interior do metal.
        </p>
        <div class="mt-3 text-[11px] text-purple-300/80 font-mono bg-[var(--card)] p-2 rounded border border-[var(--border)] text-left w-full">
          • Fundo: Gradiente kepleriano do espaço profundo<br>
          • Movimento: Vórtice orbital com aceleração central<br>
          • Crista: Branco intenso de alta precisão
        </div>
      </div>

    </div>

    <!-- Footer info -->
    <div class="mt-4 pt-3 border-t border-[var(--border)] flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-[var(--muted-foreground)]">
      <span>Qual das 3 variações você mais gostou (<strong>3A, 3B ou 3C</strong>)?</span>
      <span class="text-cyan-400 font-medium">Basta responder 3A, 3B ou 3C para aprovar e aplicar!</span>
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
          btn.className = 'px-2.5 py-1 rounded font-medium bg-cyan-600 text-white transition-colors';
        }} else {{
          btn.className = 'px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition-colors';
        }}
      }});

      for (let opt = 1; opt <= 3; opt++) {{
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

target = ARTIFACT_DIR / "universium_hybrid_preview.html"
target.write_text(html)
print(f"Showcase salvo em: {target}")
