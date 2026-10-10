#!/usr/bin/env python3
import base64
import json
from pathlib import Path

OUT_DIR = Path("/tmp/gtna_items_preview")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/443bb87c-4470-4e6b-9b58-a6dde7db835b")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

items = [
    {
        "id": "laser_lens_special",
        "name": "Special Laser Lens",
        "pt_name": "Lente Laser Especial",
        "tier": "UV / UEV",
        "color": "#38bdf8",
        "tag": "Óptica & Laser de Precisão",
        "description": "Lente óptica prismática de refração multidimensional para gravação a laser ultra-precisa na Nano Forge e Plasma Forge.",
        "details": [
            "Aro mecânico usinado em liga de Duranium com ranhuras de calibração micrométrica.",
            "4 grampos de alinhamento com eletrodos de contato folheados a ouro nos pontos cardeais.",
            "Núcleo de cristal quântico com dispersão cromática contínua (feixe laser rotativo em espectro RGB completo).",
            "Ponto focal ultra-concentrado no centro com pulso fotônico e raios de difração em estrela."
        ],
        "recipe": "Duranium + Diamond Lens + Quantum Star + Excited DTRC / UV Circuits"
    },
    {
        "id": "stable_boson_containment_unit",
        "name": "Stable Boson Containment Unit",
        "pt_name": "Unidade de Contenção de Bósons Estável",
        "tier": "UHV / UEV",
        "color": "#818cf8",
        "tag": "Matriz de Contenção Subatômica",
        "description": "Cápsula de vácuo hiperbárico com confinamento magnético UHV para estabilização de bósons de gauge fundamentais (Higgs / W / Z).",
        "details": [
            "Blindagens polares superior e inferior usinadas em placas maciças de Neutronium.",
            "Display LED de monitoramento de integridade e trava de campo de Higgs na tampa superior.",
            "Câmara cilíndrica de vidro de campo de força com curvatura 3D translúcida e reflexo especular.",
            "Núcleo de Bóson radiante pulsante no centro com 2 anéis elípticos de fluxo quântico e fagulhas em órbita precessional."
        ],
        "recipe": "Gravi Star + UHV Field Generator + 4x Neutronium Plates + Krypton"
    },
    {
        "id": "graviton_anomaly",
        "name": "Graviton Anomaly",
        "pt_name": "Anomalia de Gráviton",
        "tier": "UEV / UIV",
        "color": "#f97316",
        "tag": "Singularidade Espaço-Temporal",
        "description": "Micro-buraco negro artificial com horizonte de eventos capturado e ondas de distorção gravitacional concentradas.",
        "details": [
            "Horizonte de Eventos absoluto no centro: vácuo cósmico negro absoluto intransponível.",
            "Esfera de Fótons (anel de Einstein) ultra-luminosa com feixe relativístico (Doppler boosting assimétrico).",
            "Disco de acreção espiral logarítmico em vórtice com matéria superaquecida fluindo para a singularidade.",
            "Ondas de choque gravitacionais e pacotes de grávitons cintilantes em órbita ergoesférica."
        ],
        "recipe": "Quantum Star + 2x Stable Boson Containment + 16x Naquadria + UHV Circuits + Tritanium"
    }
]

# Read assets
b64_assets = {}
for it in items:
    for res in [32, 64]:
        gif_file = OUT_DIR / f"{it['id']}_{res}.gif"
        strip_file = OUT_DIR / f"{it['id']}_{res}_strip.png"
        
        if gif_file.exists():
            b64_assets[f"{it['id']}_{res}_gif"] = f"data:image/gif;base64,{base64.b64encode(gif_file.read_bytes()).decode('utf-8')}"
        if strip_file.exists():
            b64_assets[f"{it['id']}_{res}_strip"] = f"data:image/png;base64,{base64.b64encode(strip_file.read_bytes()).decode('utf-8')}"

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>GTNA — Visualizador de Texturas Animadas</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
    .minecraft-slot {{
      background: #8b8b8b;
      box-shadow: inset -2px -2px #ffffff, inset 2px 2px #373737;
    }}
    .dark-slot {{
      background: #18181b;
      box-shadow: inset -1px -1px rgba(255,255,255,0.1), inset 1px 1px rgba(0,0,0,0.8);
    }}
    .glow-cyan {{
      filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.45));
    }}
    .glow-purple {{
      filter: drop-shadow(0 0 12px rgba(129, 140, 248, 0.45));
    }}
    .glow-orange {{
      filter: drop-shadow(0 0 12px rgba(249, 115, 22, 0.45));
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-4">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-lg max-w-5xl mx-auto space-y-6">
    
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-[var(--border)] gap-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-flex w-3 h-3 rounded-full bg-cyan-400 animate-ping"></span>
          <h1 class="text-xl font-bold tracking-tight text-[var(--foreground)]">
            GTNA — Novas Texturas Procedurais Animadas
          </h1>
        </div>
        <p class="text-sm text-[var(--muted-foreground)] mt-1">
          Special Laser Lens • Stable Boson Containment Unit • Graviton Anomaly (Qualidade 32x e 64x com 16 frames fluidos)
        </p>
      </div>

      <!-- Global Controls Bar -->
      <div class="flex flex-wrap items-center gap-2 bg-[var(--background)] p-1.5 rounded-xl border border-[var(--border)]">
        <!-- Resolution Selector -->
        <div class="flex items-center text-xs font-semibold bg-[var(--card)] rounded-lg p-0.5 border border-[var(--border)]">
          <button id="btn-res-32" onclick="setResolution(32)" class="px-2.5 py-1 rounded-md bg-cyan-600 text-white shadow-sm transition">
            32x (Battery Tier)
          </button>
          <button id="btn-res-64" onclick="setResolution(64)" class="px-2.5 py-1 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition">
            64x (Fuel Rod HD)
          </button>
        </div>

        <!-- Zoom Selector -->
        <div class="flex items-center text-xs font-semibold bg-[var(--card)] rounded-lg p-0.5 border border-[var(--border)]">
          <button onclick="setZoom(1)" class="btn-zoom px-2 py-1 rounded text-[var(--muted-foreground)]" data-zoom="1">1x</button>
          <button onclick="setZoom(2)" class="btn-zoom px-2 py-1 rounded text-[var(--muted-foreground)]" data-zoom="2">2x</button>
          <button onclick="setZoom(4)" class="btn-zoom px-2 py-1 rounded bg-slate-700 text-white font-bold" data-zoom="4">4x</button>
          <button onclick="setZoom(8)" class="btn-zoom px-2 py-1 rounded text-[var(--muted-foreground)]" data-zoom="8">8x</button>
        </div>

        <!-- Slot Background -->
        <div class="flex items-center text-xs font-semibold bg-[var(--card)] rounded-lg p-0.5 border border-[var(--border)]">
          <button onclick="setBg('mc')" class="px-2 py-1 rounded text-[var(--foreground)] hover:bg-[var(--background)]" title="Minecraft Slot">MC Slot</button>
          <button onclick="setBg('dark')" class="px-2 py-1 rounded text-[var(--foreground)] hover:bg-[var(--background)]" title="Dark Obsidian">Escuro</button>
          <button onclick="setBg('light')" class="px-2 py-1 rounded text-[var(--foreground)] hover:bg-[var(--background)]" title="Light REI/JEI">Claro</button>
        </div>
      </div>
    </div>

    <!-- Items Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
"""

for it in items:
    item_id = it["id"]
    glow_class = "glow-cyan" if "lens" in item_id else ("glow-purple" if "boson" in item_id else "glow-orange")
    accent_color = it["color"]
    
    html_content += f"""
      <!-- Card for {it['name']} -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col justify-between hover:border-slate-500 transition-all shadow-sm">
        
        <!-- Header -->
        <div>
          <div class="flex items-center justify-between gap-1 mb-2">
            <span class="text-xs font-semibold px-2 py-0.5 rounded-full border" style="color: {accent_color}; border-color: {accent_color}40; background: {accent_color}15;">
              {it['tier']}
            </span>
            <span class="text-xs font-mono text-[var(--muted-foreground)]">16 frames • 80ms</span>
          </div>

          <h3 class="text-base font-bold text-[var(--foreground)] flex items-center gap-1.5">
            {it['name']}
          </h3>
          <p class="text-xs font-medium text-[var(--muted-foreground)] mb-3">
            {it['pt_name']}
          </p>

          <!-- Interactive Texture Preview Stage -->
          <div class="stage-container flex flex-col items-center justify-center p-6 rounded-xl border border-[var(--border)] minecraft-slot transition-colors min-h-[160px] relative overflow-hidden">
            <img id="img-{item_id}" 
                 src="{b64_assets[f'{item_id}_32_gif']}" 
                 alt="{it['name']}" 
                 class="pixelated {glow_class} transition-transform" 
                 style="width: 128px; height: 128px;" />
          </div>

          <div class="mt-4 space-y-2">
            <p class="text-xs text-[var(--foreground)] font-medium leading-relaxed">
              {it['description']}
            </p>

            <ul class="text-xs text-[var(--muted-foreground)] space-y-1 pl-3 border-l-2" style="border-color: {accent_color}60;">
"""
    for d in it["details"]:
        html_content += f"              <li>• {d}</li>\n"

    html_content += f"""            </ul>
          </div>
        </div>

        <!-- Recipe & Status Footer -->
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs">
          <div class="text-[var(--muted-foreground)] text-[11px] mb-1 font-mono">
            <strong class="text-[var(--foreground)]">Origem:</strong> {it['recipe']}
          </div>
          <div class="flex items-center justify-between mt-2 pt-2 border-t border-[var(--border)]">
            <span class="text-xs font-mono text-emerald-400 flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Pronto p/ Mod
            </span>
            <button onclick="applySingleItem('{item_id}')" class="px-2.5 py-1 text-xs font-semibold rounded bg-[var(--card)] hover:bg-[var(--border)] border border-[var(--border)] text-[var(--foreground)] transition">
              Instalar 32x/64x
            </button>
          </div>
        </div>

      </div>
"""

html_content += f"""
    </div>

    <!-- Technical Specs & Guide Footer -->
    <div class="bg-[var(--background)] p-4 rounded-xl border border-[var(--border)] text-xs text-[var(--muted-foreground)] space-y-2">
      <div class="flex items-center justify-between text-[var(--foreground)] font-bold text-sm">
        <span>Especificações de Renderização no Minecraft 1.20.1</span>
        <span class="text-xs font-normal text-cyan-400 font-mono">Suporte Nativo GTCEu / Registrate</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-1">
        <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
          <strong class="text-[var(--foreground)] block mb-1">Qualidade 32x32 (Really Ultimate Battery Tier)</strong>
          Resolução ideal para pixel art de alta fidelidade: nitidez impecável no inventário e GUI, sem borrão ou pixel stretch.
        </div>
        <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
          <strong class="text-[var(--foreground)] block mb-1">Qualidade 64x64 (Fuel Rod Ultra HD)</strong>
          Máxima densidade de gradientes e efeitos de plasma com 64x1024 no arquivo vertical de textura strip.
        </div>
        <div class="p-2.5 rounded-lg bg-[var(--card)] border border-[var(--border)]">
          <strong class="text-[var(--foreground)] block mb-1">Interpolação .mcmeta (60 FPS Fluido)</strong>
          Configuração com <code class="font-mono text-cyan-300">"interpolate": true</code> para suavização sub-frame de partículas no motor do Minecraft.
        </div>
      </div>
    </div>

  </div>

  <script>
    const assets = {json.dumps(b64_assets)};
    let currentRes = 32;
    let currentZoom = 4;
    const items = ["laser_lens_special", "stable_boson_containment_unit", "graviton_anomaly"];

    function setResolution(res) {{
      currentRes = res;
      document.getElementById("btn-res-32").className = res === 32 
        ? "px-2.5 py-1 rounded-md bg-cyan-600 text-white shadow-sm transition"
        : "px-2.5 py-1 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition";
      document.getElementById("btn-res-64").className = res === 64 
        ? "px-2.5 py-1 rounded-md bg-cyan-600 text-white shadow-sm transition"
        : "px-2.5 py-1 rounded-md text-[var(--muted-foreground)] hover:text-[var(--foreground)] transition";
      
      updateImages();
    }}

    function setZoom(z) {{
      currentZoom = z;
      document.querySelectorAll(".btn-zoom").forEach(btn => {{
        if (parseInt(btn.getAttribute("data-zoom")) === z) {{
          btn.className = "btn-zoom px-2 py-1 rounded bg-slate-700 text-white font-bold";
        }} else {{
          btn.className = "btn-zoom px-2 py-1 rounded text-[var(--muted-foreground)]";
        }}
      }});
      updateZoom();
    }}

    function updateZoom() {{
      const pxSize = currentRes * currentZoom;
      items.forEach(id => {{
        const img = document.getElementById("img-" + id);
        if (img) {{
          img.style.width = pxSize + "px";
          img.style.height = pxSize + "px";
        }}
      }});
    }}

    function updateImages() {{
      items.forEach(id => {{
        const img = document.getElementById("img-" + id);
        const key = id + "_" + currentRes + "_gif";
        if (img && assets[key]) {{
          img.src = assets[key];
        }}
      }});
      updateZoom();
    }}

    function setBg(type) {{
      document.querySelectorAll(".stage-container").forEach(el => {{
        if (type === "mc") {{
          el.className = "stage-container flex flex-col items-center justify-center p-6 rounded-xl border border-[var(--border)] minecraft-slot transition-colors min-h-[160px] relative overflow-hidden";
          el.style.background = "#8b8b8b";
        }} else if (type === "dark") {{
          el.className = "stage-container flex flex-col items-center justify-center p-6 rounded-xl border border-[var(--border)] dark-slot transition-colors min-h-[160px] relative overflow-hidden";
          el.style.background = "#18181b";
        }} else if (type === "light") {{
          el.className = "stage-container flex flex-col items-center justify-center p-6 rounded-xl border border-[var(--border)] transition-colors min-h-[160px] relative overflow-hidden";
          el.style.background = "#f1f5f9";
        }}
      }});
    }}

    function applySingleItem(itemId) {{
      alert("A textura de " + itemId + " (" + currentRes + "x) está gerada em /tmp/gtna_items_preview e pronta para ser aplicada nos recursos do mod!");
    }}
  </script>
</body>
</html>
"""

artifact_file = ARTIFACT_DIR / "item_textures_preview.html"
artifact_file.write_text(html_content, encoding="utf-8")
print(f"Created HTML widget preview artifact: {artifact_file} ({artifact_file.stat().st_size} bytes)")
