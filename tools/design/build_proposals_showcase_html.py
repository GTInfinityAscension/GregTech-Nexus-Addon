"""Builds the self-contained interactive Generative UI HTML artifact for the 36 Material Set proposals.
Embeds base64 animated GIFs so the page renders offline and self-contained.
"""

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROPOSALS_DIR = ROOT / "docs/roadmap/design/proposals/originals_material_sets"
MANIFEST_PATH = PROPOSALS_DIR / "manifest.json"
ARTIFACT_PATH = Path("/home/raishxn/.gemini/antigravity/brain/33fb6fd8-065e-4262-bcd3-eb93a1b0e971/originals_material_sets_showcase.html")

def b64(p):
    return f"data:image/gif;base64,{base64.b64encode(p.read_bytes()).decode()}"

def main():
    manifest = json.loads(MANIFEST_PATH.read_text())
    
    # Pre-encode all GIFs to base64
    encoded_data = {}
    print("Encoding GIFs into base64...")
    for mat_id, meta in manifest.items():
        encoded_data[mat_id] = {
            "title": meta["title"],
            "machine": meta["machine"],
            "lore": meta["lore"],
            "primary_form": meta["primary_form"],
            "options": []
        }
        for opt in meta["options"]:
            slot_p = PROPOSALS_DIR / opt["slot_gif"]
            icon_p = PROPOSALS_DIR / opt["icon_gif"]
            halo_p = PROPOSALS_DIR / opt["halo_gif"]
            encoded_data[mat_id]["options"].append({
                "option": opt["option"],
                "name": opt["name"],
                "desc": opt["desc"],
                "halo_name": opt["halo_name"],
                "halo_desc": opt["halo_desc"],
                "accent": opt["accent"],
                "slot_b64": b64(slot_p),
                "icon_b64": b64(icon_p),
                "halo_b64": b64(halo_p),
            })
            
    print("Building HTML file...")
    
    # Build HTML with Tailwind & interactive JS
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>GTNA — Propostas de Material Sets dos Originais</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: -moz-crisp-edges;
      image-rendering: crisp-edges;
    }}
    .custom-scrollbar::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: var(--border);
      border-radius: 4px;
    }}
  </style>
</head>
<body class="bg-[var(--background)] text-[var(--foreground)] antialiased p-4 md:p-8 custom-scrollbar">

  <!-- Header Section -->
  <header class="max-w-7xl mx-auto mb-8 border-b border-[var(--border)] pb-6">
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
            Fase de Design & Aprovação
          </span>
          <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-cyan-500/10 text-cyan-500 border border-cyan-500/20">
            Modernity-GTNH Art + Shaders GTNA
          </span>
          <span class="px-2.5 py-0.5 text-xs font-semibold rounded-full bg-purple-500/10 text-purple-500 border border-purple-500/20">
            32 Frames • 60 FPS
          </span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold tracking-tight">Propostas de Material Sets dos Originais</h1>
        <p class="text-[var(--muted-foreground)] text-sm mt-1 max-w-3xl">
          12 novos materiais exclusivos do endgame (Lança Orbital, Câmara de Contenção, Fenda Dimensional e Colisor).
          Cada material possui 3 opções únicas com paleta dedicada, física de animação orgânica e halos quânticos 64×64.
        </p>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        <button id="btn-export" onclick="exportChoices()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-medium rounded-lg shadow-sm transition flex items-center gap-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
          Copiar Escolhas (<span id="count-selected">12</span>/12)
        </button>
      </div>
    </div>

    <!-- Controls Bar -->
    <div class="mt-6 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 bg-[var(--card)] border border-[var(--border)] rounded-xl p-3">
      <!-- Filter by Machine -->
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 custom-scrollbar text-xs">
        <span class="text-[var(--muted-foreground)] font-medium mr-1">Origem:</span>
        <button onclick="setFilter('all')" class="filter-btn active px-3 py-1.5 rounded-lg border border-[var(--border)] font-medium transition" data-filter="all">Todos (12)</button>
        <button onclick="setFilter('lance')" class="filter-btn px-3 py-1.5 rounded-lg border border-[var(--border)] font-medium transition" data-filter="lance">Lança Orbital (2)</button>
        <button onclick="setFilter('stellar')" class="filter-btn px-3 py-1.5 rounded-lg border border-[var(--border)] font-medium transition" data-filter="stellar">Câmara Estelar (3)</button>
        <button onclick="setFilter('rift')" class="filter-btn px-3 py-1.5 rounded-lg border border-[var(--border)] font-medium transition" data-filter="rift">Fenda Dimensional (7)</button>
      </div>

      <!-- View Mode Toggle -->
      <div class="flex items-center gap-1.5 text-xs border-t md:border-t-0 md:border-l border-[var(--border)] pt-2 md:pt-0 md:pl-4">
        <span class="text-[var(--muted-foreground)] font-medium mr-1">Visualização:</span>
        <button onclick="setViewMode('slot')" id="btn-view-slot" class="px-2.5 py-1.5 rounded-md bg-[var(--accent)] text-[var(--foreground)] font-medium shadow-sm transition">In-Slot + Halo</button>
        <button onclick="setViewMode('icon')" id="btn-view-icon" class="px-2.5 py-1.5 rounded-md border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-medium transition">Apenas Ícone</button>
        <button onclick="setViewMode('halo')" id="btn-view-halo" class="px-2.5 py-1.5 rounded-md border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-medium transition">Apenas Halo</button>
      </div>
    </div>
  </header>

  <!-- Materials Grid Container -->
  <main class="max-w-7xl mx-auto space-y-10" id="materials-container">
    <!-- Populated by JavaScript -->
  </main>

  <!-- Sticky Notification / Confirmation Toast -->
  <div id="toast" class="fixed bottom-6 right-6 transform translate-y-24 opacity-0 transition-all duration-300 z-50 bg-emerald-600 text-white px-4 py-3 rounded-xl shadow-lg flex items-center gap-3 text-sm">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
    <span id="toast-msg">Escolhas copiadas para a área de transferência!</span>
  </div>

  <script>
    const data = {json.dumps(encoded_data)};
    let activeFilter = 'all';
    let activeViewMode = 'slot'; // 'slot', 'icon', 'halo'
    const choices = {{}};

    // Default choices: Option 1 for all
    Object.keys(data).forEach(matId => {{
      choices[matId] = 1;
    }});

    function getMachineKey(machineStr) {{
      if (machineStr.includes('Lance')) return 'lance';
      if (machineStr.includes('Stellar')) return 'stellar';
      return 'rift';
    }}

    function renderMaterials() {{
      const container = document.getElementById('materials-container');
      container.innerHTML = '';

      Object.entries(data).forEach(([matId, mat]) => {{
        const mKey = getMachineKey(mat.machine);
        if (activeFilter !== 'all' && activeFilter !== mKey) return;

        const card = document.createElement('article');
        card.className = "bg-[var(--card)] border border-[var(--border)] rounded-2xl p-5 shadow-sm";
        card.id = `mat-${{matId}}`;

        let optionsHtml = '';
        mat.options.forEach(opt => {{
          const isSelected = choices[matId] === opt.option;
          const imgSrc = activeViewMode === 'slot' ? opt.slot_b64 : (activeViewMode === 'icon' ? opt.icon_b64 : opt.halo_b64);
          const imgSizeClass = activeViewMode === 'slot' ? 'w-24 h-24' : (activeViewMode === 'icon' ? 'w-20 h-20' : 'w-24 h-24');

          optionsHtml += `
            <div onclick="selectOption('${{matId}}', ${{opt.option}})" 
                 class="cursor-pointer group flex flex-col justify-between rounded-xl p-4 border transition-all ${{isSelected ? 'border-emerald-500 bg-emerald-500/5 ring-2 ring-emerald-500/30' : 'border-[var(--border)] hover:border-[var(--accent)] hover:bg-[var(--accent)]/5'}}">
              
              <!-- Preview Header -->
              <div>
                <div class="flex items-center justify-between mb-3">
                  <span class="text-xs font-semibold px-2 py-0.5 rounded-full border" 
                        style="color: ${{opt.accent}}; border-color: ${{opt.accent}}40; background: ${{opt.accent}}15;">
                    Opção ${{opt.option}}
                  </span>
                  <div class="w-5 h-5 rounded-full flex items-center justify-center border ${{isSelected ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-[var(--border)] text-transparent'}}">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                  </div>
                </div>

                <!-- Animated GIF Preview -->
                <div class="flex items-center justify-center p-3 rounded-lg bg-[var(--background)] border border-[var(--border)] mb-3">
                  <img src="${{imgSrc}}" alt="${{matId}} op ${{opt.option}}" class="${{imgSizeClass}} pixelated object-contain transition-transform group-hover:scale-105 duration-200">
                </div>

                <!-- Titles & Info -->
                <h4 class="font-semibold text-sm mb-1">${{opt.name}}</h4>
                <p class="text-xs text-[var(--muted-foreground)] leading-relaxed mb-3">${{opt.desc}}</p>
              </div>

              <!-- Halo Specs -->
              <div class="mt-2 pt-2.5 border-t border-[var(--border)]/70 text-xs">
                <div class="flex items-center gap-1.5 font-medium text-[var(--foreground)] mb-1">
                  <svg class="w-3.5 h-3.5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  <span>Halo: <code class="text-[11px] font-mono text-purple-300">${{opt.halo_name}}</code></span>
                </div>
                <p class="text-[11px] text-[var(--muted-foreground)]">${{opt.halo_desc}}</p>
              </div>
            </div>
          `;
        }});

        card.innerHTML = `
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-4 pb-3 border-b border-[var(--border)]">
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-bold">${{mat.title}}</h3>
                <span class="text-xs font-mono uppercase px-2 py-0.5 rounded bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]">${{mat.primary_form}}</span>
              </div>
              <p class="text-xs text-[var(--muted-foreground)] mt-0.5">${{mat.lore}}</p>
            </div>
            <div class="text-xs text-[var(--muted-foreground)] font-medium">
              Origem: <span class="text-[var(--foreground)]">${{mat.machine}}</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            ${{optionsHtml}}
          </div>
        `;

        container.appendChild(card);
      }});

      updateCounter();
    }}

    function selectOption(matId, optNum) {{
      choices[matId] = optNum;
      renderMaterials();
    }}

    function setFilter(filter) {{
      activeFilter = filter;
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        if (btn.dataset.filter === filter) {{
          btn.className = "filter-btn active px-3 py-1.5 rounded-lg bg-[var(--accent)] text-[var(--foreground)] font-medium transition";
        }} else {{
          btn.className = "filter-btn px-3 py-1.5 rounded-lg border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-medium transition";
        }}
      }});
      renderMaterials();
    }}

    function setViewMode(mode) {{
      activeViewMode = mode;
      ['slot', 'icon', 'halo'].forEach(m => {{
        const btn = document.getElementById(`btn-view-${{m}}`);
        if (m === mode) {{
          btn.className = "px-2.5 py-1.5 rounded-md bg-[var(--accent)] text-[var(--foreground)] font-medium shadow-sm transition";
        }} else {{
          btn.className = "px-2.5 py-1.5 rounded-md border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] font-medium transition";
        }}
      }});
      renderMaterials();
    }}

    function updateCounter() {{
      const count = Object.keys(choices).length;
      document.getElementById('count-selected').textContent = count;
    }}

    function exportChoices() {{
      const text = JSON.stringify(choices, null, 2);
      navigator.clipboard.writeText(text).then(() => {{
        showToast("Seleção copiada em JSON para a área de transferência!");
      }}).catch(() => {{
        showToast("Suas escolhas: " + JSON.stringify(choices));
      }});
    }}

    function showToast(msg) {{
      const t = document.getElementById('toast');
      document.getElementById('toast-msg').textContent = msg;
      t.classList.remove('translate-y-24', 'opacity-0');
      setTimeout(() => {{
        t.classList.add('translate-y-24', 'opacity-0');
      }}, 3000);
    }}

    // Initial Render
    renderMaterials();
  </script>
</body>
</html>
"""
    ARTIFACT_PATH.write_text(html, encoding="utf-8")
    print(f"Artifact written to {ARTIFACT_PATH}")

if __name__ == "__main__":
    main()
