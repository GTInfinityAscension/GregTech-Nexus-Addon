#!/usr/bin/env python3
import base64
import json
from pathlib import Path

OUT_DIR = Path("/tmp/gtna_items_preview")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/443bb87c-4470-4e6b-9b58-a6dde7db835b")

assets = {}

# Helper to load and encode
def load_b64(name):
    p = OUT_DIR / name
    if p.exists():
        mime = "image/gif" if name.endswith(".gif") else "image/png"
        return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode('utf-8')}"
    return ""

assets["lens_32"] = load_b64("laser_lens_special_32.gif")
assets["lens_64"] = load_b64("laser_lens_special_64.gif")

assets["grav_32"] = load_b64("graviton_anomaly_32.gif")
assets["grav_64"] = load_b64("graviton_anomaly_64.gif")
assets["grav_128"] = load_b64("graviton_anomaly_128.gif")

assets["tokamak_32"] = load_b64("boson_tokamak_32.gif")
assets["tokamak_64"] = load_b64("boson_tokamak_64.gif")
assets["tokamak_128"] = load_b64("boson_tokamak_128.gif")

assets["cube_32"] = load_b64("boson_cube_32.gif")
assets["cube_64"] = load_b64("boson_cube_64.gif")
assets["cube_128"] = load_b64("boson_cube_128.gif")

html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>GTNA — Painel de Aprovação de Texturas Animadas</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
    .minecraft-slot {{
      background: #8b8b8b;
      box-shadow: inset -3px -3px #ffffff, inset 3px 3px #373737;
    }}
    .dark-slot {{
      background: #141417;
      box-shadow: inset -1px -1px rgba(255,255,255,0.08), inset 1px 1px rgba(0,0,0,0.8);
    }}
    .glow-cyan {{ filter: drop-shadow(0 0 14px rgba(56, 189, 248, 0.5)); }}
    .glow-orange {{ filter: drop-shadow(0 0 16px rgba(249, 115, 22, 0.55)); }}
    .glow-purple {{ filter: drop-shadow(0 0 16px rgba(168, 85, 247, 0.55)); }}
    .glow-emerald {{ filter: drop-shadow(0 0 16px rgba(52, 211, 153, 0.5)); }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-3 sm:p-5">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-xl max-w-6xl mx-auto space-y-6">
    
    <!-- Top Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-4 border-b border-[var(--border)] gap-3">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-flex w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
          <h1 class="text-xl font-bold tracking-tight text-[var(--foreground)]">
            GTNA — Revisão de Texturas & Redesign do Bóson
          </h1>
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-0.5">
          Graviton Anomaly com suporte a <strong>128x Ultra HD</strong> + 2 novos conceitos para a <strong>Stable Boson Containment Unit</strong>
        </p>
      </div>

      <!-- Global Preview Controls -->
      <div class="flex flex-wrap items-center gap-2 bg-[var(--background)] p-1.5 rounded-xl border border-[var(--border)] text-xs">
        <span class="text-[var(--muted-foreground)] font-semibold px-1">Fundo:</span>
        <button onclick="setBg('mc')" class="px-2.5 py-1 rounded bg-[var(--card)] border border-[var(--border)] font-medium hover:bg-slate-700">MC Slot</button>
        <button onclick="setBg('dark')" class="px-2.5 py-1 rounded bg-[var(--card)] border border-[var(--border)] font-medium hover:bg-slate-700">Escuro</button>
        <button onclick="setBg('light')" class="px-2.5 py-1 rounded bg-[var(--card)] border border-[var(--border)] font-medium hover:bg-slate-700">Claro</button>
      </div>
    </div>

    <!-- Section 1: Graviton Anomaly & Special Laser Lens -->
    <div>
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-sm font-bold uppercase tracking-wider text-[var(--foreground)] flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
          Itens Aprovados (com Upgrade 128x na Singularidade)
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- 1. Special Laser Lens -->
        <div class="bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
                UV / UEV • Óptica Quântica
              </span>
              <span class="text-xs font-mono text-emerald-400">✓ Aprovado</span>
            </div>
            <h3 class="text-base font-bold text-[var(--foreground)]">Special Laser Lens</h3>
            <p class="text-xs text-[var(--muted-foreground)] mb-3">Lente Laser Especial — Aro de Duranium com refração prismática contínua</p>
            
            <div class="stage-container flex flex-col items-center justify-center p-4 rounded-xl minecraft-slot min-h-[160px] relative">
              <img id="img-lens" src="{assets['lens_32']}" class="pixelated glow-cyan transition-all" style="width: 128px; height: 128px;" />
            </div>

            <div class="flex items-center justify-center gap-2 mt-3">
              <button onclick="setLensRes(32)" id="btn-lens-32" class="px-2.5 py-1 text-xs rounded-md bg-cyan-600 text-white font-semibold">32x (Battery Tier)</button>
              <button onclick="setLensRes(64)" id="btn-lens-64" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">64x (Fuel Rod HD)</button>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs text-[var(--muted-foreground)]">
            Aro metálico usinado de Duranium, feixes em rotação espectral (RGB contínuo) e ponto focal central com estrelas de difração.
          </div>
        </div>

        <!-- 2. Graviton Anomaly (Agora com 128x!) -->
        <div class="bg-[var(--background)] border-2 border-orange-500/40 rounded-xl p-4 flex flex-col justify-between shadow-md">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-orange-500/15 text-orange-400 border border-orange-500/30">
                UEV / UIV • Singularidade Espaço-Temporal
              </span>
              <span class="text-xs font-mono text-orange-400 font-bold animate-pulse">★ 128x Disponível!</span>
            </div>
            <h3 class="text-base font-bold text-[var(--foreground)]">Graviton Anomaly</h3>
            <p class="text-xs text-[var(--muted-foreground)] mb-3">Anomalia de Gráviton — Micro-buraco negro com horizonte de eventos e disco de acreção</p>
            
            <div class="stage-container flex flex-col items-center justify-center p-4 rounded-xl minecraft-slot min-h-[160px] relative">
              <img id="img-grav" src="{assets['grav_128']}" class="pixelated glow-orange transition-all" style="width: 140px; height: 140px;" />
            </div>

            <div class="flex items-center justify-center gap-2 mt-3">
              <button onclick="setGravRes(32)" id="btn-grav-32" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">32x</button>
              <button onclick="setGravRes(64)" id="btn-grav-64" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">64x</button>
              <button onclick="setGravRes(128)" id="btn-grav-128" class="px-3 py-1 text-xs rounded-md bg-orange-600 text-white font-bold shadow">128x Ultra HD</button>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs text-[var(--muted-foreground)]">
            Horizonte de eventos negro absoluto no centro, esfera de fótons relativística (Doppler ciano/âmbar), turbulência de plasma e 8 grávitons orbitantes em 128x128!
          </div>
        </div>

      </div>
    </div>

    <!-- Section 2: Redesigns for Stable Boson Containment Unit -->
    <div class="pt-2">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-3 gap-1">
        <h2 class="text-sm font-bold uppercase tracking-wider text-purple-400 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-purple-400"></span>
          Novos Conceitos para Stable Boson Containment Unit
        </h2>
        <span class="text-xs text-[var(--muted-foreground)]">Escolha o seu design favorito abaixo:</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <!-- Concept A: Tokamak / Anel Magnético Quântico -->
        <div class="bg-[var(--background)] border border-purple-500/40 rounded-xl p-4 flex flex-col justify-between hover:border-purple-400 transition-all">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-purple-500/15 text-purple-400 border border-purple-500/30">
                Opção A • Tokamak Quântico Industrial
              </span>
              <span class="text-xs font-mono text-cyan-400">32x / 64x / 128x</span>
            </div>
            <h3 class="text-base font-bold text-[var(--foreground)]">Anel Magnético Tokamak (Conceito A)</h3>
            <p class="text-xs text-[var(--muted-foreground)] mb-3">Chassi octogonal de Neutronium com bobinas supercondutoras e pinças a laser</p>
            
            <div class="stage-container flex flex-col items-center justify-center p-4 rounded-xl minecraft-slot min-h-[160px] relative">
              <img id="img-tokamak" src="{assets['tokamak_64']}" class="pixelated glow-purple transition-all" style="width: 135px; height: 135px;" />
            </div>

            <div class="flex items-center justify-center gap-2 mt-3">
              <button onclick="setTokamakRes(32)" id="btn-tok-32" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">32x</button>
              <button onclick="setTokamakRes(64)" id="btn-tok-64" class="px-2.5 py-1 text-xs rounded-md bg-purple-600 text-white font-bold shadow">64x HD</button>
              <button onclick="setTokamakRes(128)" id="btn-tok-128" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">128x Ultra</button>
            </div>

            <div class="mt-4 space-y-1.5 text-xs text-[var(--foreground)]">
              <div class="font-semibold text-purple-300">Destaques visuais:</div>
              <ul class="text-[var(--muted-foreground)] space-y-1 pl-3 border-l-2 border-purple-500/40">
                <li>• Chassi octogonal pesado de Neutronium com chanfros metálicos nítidos.</li>
                <li>• 4 solenoides supercondutores dourados nos eixos principais.</li>
                <li>• 4 agulhas emissoras quânticas disparando micro-arcos elétricos no núcleo.</li>
                <li>• Bóson de Higgs radiante suspenso no centro com 2 anéis giroscópicos intertravados.</li>
              </ul>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-[var(--border)] flex items-center justify-between text-xs">
            <span class="text-[var(--muted-foreground)] font-mono">Recomendado p/ Tokamak / Máquinas</span>
            <button onclick="selectBoson('tokamak')" class="px-3 py-1 bg-purple-600 hover:bg-purple-500 text-white font-semibold rounded-lg transition">
              Aprovar Opção A
            </button>
          </div>
        </div>

        <!-- Concept B: Cubo de Estase Quântica (Tesseract Lattice) -->
        <div class="bg-[var(--background)] border border-emerald-500/40 rounded-xl p-4 flex flex-col justify-between hover:border-emerald-400 transition-all">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                Opção B • Cassete de Estase Quântica
              </span>
              <span class="text-xs font-mono text-cyan-400">32x / 64x / 128x</span>
            </div>
            <h3 class="text-base font-bold text-[var(--foreground)]">Cubo de Estase & Matriz Tesseract (Conceito B)</h3>
            <p class="text-xs text-[var(--muted-foreground)] mb-3">Cassete de blindagem quântica com rede cristalina tesseract rotativa</p>
            
            <div class="stage-container flex flex-col items-center justify-center p-4 rounded-xl minecraft-slot min-h-[160px] relative">
              <img id="img-cube" src="{assets['cube_64']}" class="pixelated glow-emerald transition-all" style="width: 135px; height: 135px;" />
            </div>

            <div class="flex items-center justify-center gap-2 mt-3">
              <button onclick="setCubeRes(32)" id="btn-cub-32" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">32x</button>
              <button onclick="setCubeRes(64)" id="btn-cub-64" class="px-2.5 py-1 text-xs rounded-md bg-emerald-600 text-white font-bold shadow">64x HD</button>
              <button onclick="setCubeRes(128)" id="btn-cub-128" class="px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white">128x Ultra</button>
            </div>

            <div class="mt-4 space-y-1.5 text-xs text-[var(--foreground)]">
              <div class="font-semibold text-emerald-300">Destaques visuais:</div>
              <ul class="text-[var(--muted-foreground)] space-y-1 pl-3 border-l-2 border-emerald-500/40">
                <li>• Blindagem externa de alta densidade com cantos chanfrados e barra de telemetria dourada.</li>
                <li>• 4 portas criogênicas nos cantos com indicadores luminosos ciano.</li>
                <li>• Janela de estase de vácuo profundo com moldura cromada.</li>
                <li>• Matriz geométrica tesseract interna (rede hexagonal multidimensional) que gira em tempo real com vértices estelares.</li>
              </ul>
            </div>
          </div>

          <div class="mt-4 pt-3 border-t border-[var(--border)] flex items-center justify-between text-xs">
            <span class="text-[var(--muted-foreground)] font-mono">Estilo Sci-Fi Futurista / AE2</span>
            <button onclick="selectBoson('cube')" class="px-3 py-1 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg transition">
              Aprovar Opção B
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>

  <script>
    const assets = {json.dumps(assets)};

    function setLensRes(res) {{
      document.getElementById("img-lens").src = assets["lens_" + res];
      document.getElementById("btn-lens-32").className = res === 32 ? "px-2.5 py-1 text-xs rounded-md bg-cyan-600 text-white font-semibold" : "px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white";
      document.getElementById("btn-lens-64").className = res === 64 ? "px-2.5 py-1 text-xs rounded-md bg-cyan-600 text-white font-semibold" : "px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white";
    }}

    function setGravRes(res) {{
      document.getElementById("img-grav").src = assets["grav_" + res];
      [32, 64, 128].forEach(r => {{
        const btn = document.getElementById("btn-grav-" + r);
        if (r === res) {{
          btn.className = "px-3 py-1 text-xs rounded-md bg-orange-600 text-white font-bold shadow";
        }} else {{
          btn.className = "px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white";
        }}
      }});
    }}

    function setTokamakRes(res) {{
      document.getElementById("img-tokamak").src = assets["tokamak_" + res];
      [32, 64, 128].forEach(r => {{
        const btn = document.getElementById("btn-tok-" + r);
        btn.className = r === res ? "px-2.5 py-1 text-xs rounded-md bg-purple-600 text-white font-bold shadow" : "px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white";
      }});
    }}

    function setCubeRes(res) {{
      document.getElementById("img-cube").src = assets["cube_" + res];
      [32, 64, 128].forEach(r => {{
        const btn = document.getElementById("btn-cub-" + r);
        btn.className = r === res ? "px-2.5 py-1 text-xs rounded-md bg-emerald-600 text-white font-bold shadow" : "px-2.5 py-1 text-xs rounded-md text-[var(--muted-foreground)] hover:text-white";
      }});
    }}

    function setBg(type) {{
      document.querySelectorAll(".stage-container").forEach(el => {{
        if (type === "mc") {{
          el.className = "stage-container flex flex-col items-center justify-center p-4 rounded-xl minecraft-slot min-h-[160px] relative";
          el.style.background = "#8b8b8b";
        }} else if (type === "dark") {{
          el.className = "stage-container flex flex-col items-center justify-center p-4 rounded-xl dark-slot min-h-[160px] relative";
          el.style.background = "#141417";
        }} else if (type === "light") {{
          el.className = "stage-container flex flex-col items-center justify-center p-4 rounded-xl min-h-[160px] relative";
          el.style.background = "#f1f5f9";
        }}
      }});
    }}

    function selectBoson(choice) {{
      alert("Você selecionou o " + (choice === 'tokamak' ? 'Conceito A (Tokamak Quântico)' : 'Conceito B (Cubo de Estase Tesseract)') + "! Ele será configurado nos recursos do mod.");
    }}
  </script>
</body>
</html>
"""

preview_path = ARTIFACT_DIR / "item_textures_preview.html"
preview_path.write_text(html, encoding="utf-8")
print(f"Updated preview HTML widget: {preview_path} ({preview_path.stat().st_size} bytes)")
