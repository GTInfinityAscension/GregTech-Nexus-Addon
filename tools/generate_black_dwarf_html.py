import json

with open("/tmp/bd_candidates/b64_data.json") as f:
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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></span>
          Black Dwarf Matter — Amostras de Animação
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Silhueta moderna 1.20 retrabalhada com relevo visível e contração quântica</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1: Crimson -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-red-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-red-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_crimson']}" class="w-16 h-16 pixelated object-contain" alt="Crimson Redshift">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Crimson Redshift</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Ondas de horizonte de eventos com desvio gravitacional avermelhado sutil.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-red-500/10 text-red-400 font-mono">Red-shift Cósmico</div>
      </div>

      <!-- Opção 2: Void Purple -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-purple-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-purple-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_void']}" class="w-16 h-16 pixelated object-contain" alt="Void Purple">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Void Purple</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Contração gravitacional de matéria escura em violeta/abissal profundo.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 font-mono">Vácuo Singular</div>
      </div>

      <!-- Opção 3: Cold Obsidian -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-slate-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-slate-500/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_obsidian']}" class="w-16 h-16 pixelated object-contain" alt="Cold Obsidian">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Cold Obsidian</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Obsidiana metálica pura com reflexos prateados escuros nos chanfros.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-slate-500/10 text-slate-300 font-mono">Obsidiana Titânio</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Relevo 100% legível em telas escuras e inventários</span>
      <span class="text-purple-400">30 quadros em loop (frametime 2)</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_crimson'];
      document.getElementById('img-c2').src = images[item]['c2_void'];
      document.getElementById('img-c3').src = images[item]['c3_obsidian'];

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

p1 = "/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/black_dwarf_preview.html"
with open(p1, "w") as f:
    f.write(html_content)

p2 = "/home/raishxn/MineProjects/GregTech-Nexus-Addon/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605/black_dwarf_preview.html"
with open(p2, "w") as f:
    f.write(html_content)

print("Generated Black Dwarf preview HTML in both locations!")
