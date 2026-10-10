import json
import shutil
from pathlib import Path

OUT_DIR = Path("/tmp/transcendent_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605")
PREVIEWS_DEST = ARTIFACT_DIR / "previews_transcendent"
PREVIEWS_DEST.mkdir(parents=True, exist_ok=True)

# Copy gif files to artifact directory
for gif in OUT_DIR.glob("*.gif"):
    shutil.copy(gif, PREVIEWS_DEST / gif.name)

with open(OUT_DIR / "b64_data.json") as f:
    b64_data = json.load(f)

html_content = f"""<!DOCTYPE html>
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
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-xl p-4 shadow-sm max-w-2xl mx-auto">
    <div class="flex items-center justify-between pb-3 border-b border-[var(--border)]">
      <div>
        <h2 class="text-base font-bold text-[var(--foreground)] flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-violet-400 animate-pulse"></span>
          Transcendent Metal (TsЖ) — Amostras de Animação
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Metal dimensional hiperdenso UMV/UXV em titânio-grafite profundo (#323232)</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1: 4D Tesseract Spatial Folding -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-violet-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-violet-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_tesseract']}" class="w-16 h-16 pixelated object-contain" alt="4D Tesseract Folding">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Dobra Tesseract 4D</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Projeção quadridimensional de hipercubo com arestas e vértices geométricos que dobram e rotacionam pelo espaço tridimensional.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-violet-400/10 text-violet-300 font-mono">Geometria 4D Tesseract</div>
      </div>

      <!-- Opção 2: Gravitational Lensing & Event Horizon -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-indigo-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-indigo-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_lens']}" class="w-16 h-16 pixelated object-contain" alt="Gravitational Lens">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Lente Gravitacional</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Distorção da luz e curvatura do espaço-tempo em anéis de Einstein e arcos cáusticos orbitando a micro-singularidade central.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono">Anéis de Einstein</div>
      </div>

      <!-- Opção 3: Spatiotemporal Dimensional Tear -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-cyan-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-cyan-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_tear']}" class="w-16 h-16 pixelated object-contain" alt="Spatiotemporal Tear">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Fenda Dimensional</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Fissuras assimétricas no contínuo que se rasgam espontaneamente em relâmpagos de luz hiperdimensional e cicatrizam no vácuo.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-cyan-400/10 text-cyan-300 font-mono">Fratura Espaço-Temporal</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Substitui o METALLIC cinza estático por animação dimensional ativa</span>
      <span class="text-violet-400">30 quadros em loop (frametime 2)</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_tesseract'];
      document.getElementById('img-c2').src = images[item]['c2_lens'];
      document.getElementById('img-c3').src = images[item]['c3_tear'];

      ['ingot', 'plate', 'gear', 'block'].forEach(i => {{
        const btn = document.getElementById('btn-' + i);
        if (i === item) {{
          btn.className = "px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]";
        }} else {{
          btn.className = "px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]";
        }}
      }});
    }}
  </script>
</body>
</html>
"""

html_dest = ARTIFACT_DIR / "transcendent_metal_preview.html"
with open(html_dest, "w") as f:
    f.write(html_content)

print("Generated HTML at:", html_dest)
