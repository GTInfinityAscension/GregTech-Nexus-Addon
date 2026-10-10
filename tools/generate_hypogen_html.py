import json

with open("/tmp/hypogen_candidates/b64_data.json") as f:
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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse"></span>
          Hypogen — Amostras de Animação Moderna
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Silhuetas modernas 1.20 com calor estelar (12.600K) e bronze solar incandescente</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1: Solar Fusion Resonance -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-amber-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-amber-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_resonance']}" class="w-16 h-16 pixelated object-contain" alt="Solar Resonance">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Solar Resonance</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Ondas harmônicas de calor de fusão correndo pela liga de bronze estelar.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">Calor Contínuo</div>
      </div>

      <!-- Opção 2: Solar Flare Sweep -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-yellow-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-yellow-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_sweep']}" class="w-16 h-16 pixelated object-contain" alt="Solar Flare Sweep">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Flare Sweep</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Varredura diagonal periódica de fogo estelar com brilho ofuscante dourado.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-yellow-500/10 text-yellow-400 font-mono">Chama Radiante</div>
      </div>

      <!-- Opção 3: Thermal Core Pulse -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-orange-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-orange-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_pulse']}" class="w-16 h-16 pixelated object-contain" alt="Thermal Pulse">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Thermal Pulse</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Pulsação nuclear térmica rítmica expandindo do núcleo para as bordas.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 font-mono">Pulso Térmico</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Substitui 100% dos sprites 1.7.10 do GT5U</span>
      <span class="text-amber-400">30 quadros em loop (frametime 2)</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_resonance'];
      document.getElementById('img-c2').src = images[item]['c2_sweep'];
      document.getElementById('img-c3').src = images[item]['c3_pulse'];

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

p1 = "/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/hypogen_preview.html"
with open(p1, "w") as f:
    f.write(html_content)

p2 = "/home/raishxn/MineProjects/GregTech-Nexus-Addon/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/hypogen_preview.html"
with open(p2, "w") as f:
    f.write(html_content)

print("Generated Hypogen preview HTML in both locations!")
