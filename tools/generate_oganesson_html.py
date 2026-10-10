import json
import shutil
from pathlib import Path

OUT_DIR = Path("/tmp/oganesson_candidates")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605")
PREVIEWS_DEST = ARTIFACT_DIR / "previews_oganesson"
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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse"></span>
          Metastable Oganesson (Og*) — Amostras de Animação
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Elemento superpesado 118 em estado isomérico excitado nobre-metálico (#14397f)</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1: Cherenkov Shockwave & Ionizing Decay -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-cyan-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-cyan-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_cherenkov']}" class="w-16 h-16 pixelated object-contain" alt="Cherenkov Shockwave">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Choque Cherenkov</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Ondas de choque Cherenkov azul-ciano com micro-cintilações ionizantes radioativas instantâneas de decaimento alfa/beta.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-cyan-400/10 text-cyan-300 font-mono">Cherenkov & Decaimento</div>
      </div>

      <!-- Opção 2: Relativistic Shell Contraction -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-blue-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-blue-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_shells']}" class="w-16 h-16 pixelated object-contain" alt="Relativistic Shells">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Camadas Relativísticas</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Ondulações concêntricas de orbitais relativísticos em contração que se propagam radialmente pelo volume em azul cobalto neon.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono">Orbitais Radiais Z=118</div>
      </div>

      <!-- Opção 3: Isomeric Spin Inversion -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-indigo-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-indigo-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_isomeric']}" class="w-16 h-16 pixelated object-contain" alt="Isomeric Spin">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Spin Isomérico Duplo</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Bandas diagonais de valência em contra-fluxo harmônico que colidem gerando nós de interferência violeta-actinídeo e azul elétrico.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono">Bandas de Valência</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Substitui o SHINY azul genérico por animação física customizada</span>
      <span class="text-blue-400">30 quadros em loop (frametime 2)</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_cherenkov'];
      document.getElementById('img-c2').src = images[item]['c2_shells'];
      document.getElementById('img-c3').src = images[item]['c3_isomeric'];

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

html_dest = ARTIFACT_DIR / "oganesson_preview.html"
with open(html_dest, "w") as f:
    f.write(html_content)

print("Generated HTML at:", html_dest)
