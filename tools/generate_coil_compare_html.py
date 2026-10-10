import json

with open("/tmp/hypogen_compare/results.json") as f:
    data = json.load(f)

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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-orange-500 animate-pulse"></span>
          Hypogen — Comparação de Tom com a Bobina (Coil)
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Ajuste de saturação e calor para perfeita harmonia visual</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setMode('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setMode('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setMode('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Referência: Bobina -->
      <div class="bg-[var(--background)] border border-orange-500/40 rounded-lg p-3 flex flex-col items-center text-center">
        <div class="w-20 h-20 bg-slate-950 rounded border border-orange-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img src="{data['coil']}" class="w-16 h-16 pixelated object-contain" alt="Hypogen Coil">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">Bobina Atual (Coil)</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Textura do bloco de bobina (12.600K) ativa no GTNA.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 font-mono">Referência</div>
      </div>

      <!-- Opção A: Laranja Solar (Coil Match) -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-orange-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-amber-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-orange" src="{data['ingot_orange']}" class="w-16 h-16 pixelated object-contain" alt="Tom Laranja da Bobina">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">A. Laranja da Bobina</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Laranja solar vibrante e filamentos dourados idênticos à bobina.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono">100% Harmônico</div>
      </div>

      <!-- Opção B: Bronze Escuro -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-amber-700/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-amber-700/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-bronze" src="{data['ingot_bronze']}" class="w-16 h-16 pixelated object-contain" alt="Bronze Escuro">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">B. Bronze Âmbar</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Mais escuro, mais puxado para cobre/bronze envelhecido do GT5U.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-amber-700/10 text-amber-300 font-mono">Mais Escuro</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>A opção A deixa todos os itens de Hypogen com a mesma cor da bobina</span>
      <span class="text-orange-400">Recomendado: Opção A</span>
    </div>
  </div>

  <script>
    const data = {json.dumps(data)};
    let current = 'ingot';

    function setMode(item) {{
      current = item;
      document.getElementById('img-orange').src = data[item + '_orange'];
      document.getElementById('img-bronze').src = data[item + '_bronze'];

      ['ingot', 'plate', 'block'].forEach(i => {{
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

p1 = "/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/hypogen_coil_compare.html"
with open(p1, "w") as f:
    f.write(html_content)

p2 = "/home/raishxn/MineProjects/GregTech-Nexus-Addon/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/hypogen_coil_compare.html"
with open(p2, "w") as f:
    f.write(html_content)

print("Generated Hypogen coil compare HTML!")
