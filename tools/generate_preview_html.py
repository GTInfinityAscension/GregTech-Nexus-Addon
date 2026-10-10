import json

with open('/tmp/wd_candidates/b64_data.json') as f:
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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
          White Dwarf Matter — Amostras de Animação
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Base Moderna 1.20 (Modernity) retrabalhada com paleta estelar</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-cyan-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950/80 rounded border border-cyan-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_sweep']}" class="w-16 h-16 pixelated object-contain" alt="Starlight Sweep">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Starlight Sweep</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Onda diagonal de brilho cósmico que varre a superfície periodicamente.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono">Destaque & Brilho</div>
      </div>

      <!-- Opção 2 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-indigo-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950/80 rounded border border-indigo-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_pulse']}" class="w-16 h-16 pixelated object-contain" alt="Gravitational Pulse">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Gravitational Pulse</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Pulsação rítmica do núcleo estelar que varia de platina azulada a branco puro.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono">Pulso & Densidade</div>
      </div>

      <!-- Opção 3 -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-blue-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950/80 rounded border border-blue-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_resonance']}" class="w-16 h-16 pixelated object-contain" alt="Degenerate Resonance">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Degenerate Resonance</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Ondas quânticas de plasma que interferem continuamente, mantendo a peça viva.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 font-mono">Plasma Ativo</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Taxa: 30 quadros em loop (frametime 2 = 10 fps)</span>
      <span class="text-cyan-400">Totalmente compatível com atlas GTCEu 1.20</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_sweep'];
      document.getElementById('img-c2').src = images[item]['c2_pulse'];
      document.getElementById('img-c3').src = images[item]['c3_resonance'];

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

target_path = "/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/white_dwarf_preview.html"
with open(target_path, "w") as f:
    f.write(html_content)

print(f"Widget HTML written to {target_path}")
