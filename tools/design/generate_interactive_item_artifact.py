#!/usr/bin/env python3
"""Build an interactive Generative UI HTML artifact for inspecting the Graviton-Tier Endgame Items:
- Embedded Base64 Animated GIFs for live 16-frame inspection
- Zoom toggle (1x, 2x, 3x, 4x)
- Technical shader breakdowns and comparison with Graviton Anomaly
- Tailwind CSS via allowlisted gstatic script and semantic design system tokens
"""

import base64
import os
from pathlib import Path

BASE_DIR = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
PROPOSALS_DIR = BASE_DIR / "tools/design/item_proposals"
ARTIFACT_PATH = Path("/home/raishxn/.gemini/antigravity/brain/4829164a-4e34-4b07-8296-5e07d2393e94/graviton_tier_item_showcase.html")

def b64_gif(path):
    with open(path, "rb") as f:
        return f"data:image/gif;base64,{base64.b64encode(f.read()).decode('utf-8')}"

grav_b64 = b64_gif(PROPOSALS_DIR / "graviton_anomaly_64.gif")
tc_b64 = b64_gif(PROPOSALS_DIR / "target_cartridge/target_cartridge_64.gif")
anti_b64 = b64_gif(PROPOSALS_DIR / "contained_particles/contained_antiproton_64.gif")
higgs_b64 = b64_gif(PROPOSALS_DIR / "contained_particles/contained_higgs_64.gif")
nexus_b64 = b64_gif(PROPOSALS_DIR / "contained_particles/contained_x_nexus_64.gif")
dewar_b64 = b64_gif(PROPOSALS_DIR / "contained_particles/antiproton_cell_64.gif")
rp_b64 = b64_gif(PROPOSALS_DIR / "rift_probe/rift_probe_64.gif")
da_b64 = b64_gif(PROPOSALS_DIR / "depth_anchor/depth_anchor_64.gif")
rs_b64 = b64_gif(PROPOSALS_DIR / "rift_singularity/rift_singularity_64.gif")

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>GTNA — Itens Endgame Graviton-Tier (NumPy Relativistic Shaders)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    .pixelated {{
      image-rendering: pixelated;
      image-rendering: crisp-edges;
    }}
    .glow-cyan {{
      filter: drop-shadow(0 0 16px rgba(0, 240, 255, 0.45));
    }}
    .glow-orange {{
      filter: drop-shadow(0 0 16px rgba(249, 115, 22, 0.45));
    }}
    .glow-purple {{
      filter: drop-shadow(0 0 16px rgba(168, 85, 247, 0.45));
    }}
    .glow-gold {{
      filter: drop-shadow(0 0 16px rgba(255, 215, 80, 0.45));
    }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-4">
  <div class="max-w-6xl mx-auto space-y-6">
    
    <!-- Header Card -->
    <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-6 shadow-md relative overflow-hidden">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-500 border border-amber-500/20 mb-2">
            <span>★ PADRÃO MATEMÁTICO GRAVITON ANOMALY</span>
          </div>
          <h1 class="text-2xl font-bold tracking-tight text-[var(--foreground)]">GTNA — Itens Endgame com Shaders Físicos em 64x64 HD</h1>
          <p class="text-sm text-[var(--muted-foreground)] mt-1">
            Recriação matemática completa utilizando Signed Distance Fields (SDF), iluminação direcional Phong, beaming relativístico Doppler, lentes de Einstein e animações em 16 frames.
          </p>
        </div>
        
        <!-- Zoom Controls -->
        <div class="flex items-center gap-1 bg-[var(--background)] p-1.5 rounded-xl border border-[var(--border)] self-start md:self-auto">
          <span class="text-xs text-[var(--muted-foreground)] px-2 font-medium">Zoom:</span>
          <button onclick="setZoom(64)" class="zoom-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-[var(--card)] border border-[var(--border)] hover:bg-[var(--border)] transition">1x (64px)</button>
          <button onclick="setZoom(128)" class="zoom-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-[var(--card)] border border-[var(--border)] hover:bg-[var(--border)] transition">2x (128px)</button>
          <button onclick="setZoom(192)" class="zoom-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-[var(--card)] border border-[var(--border)] hover:bg-[var(--border)] transition">3x (192px)</button>
          <button onclick="setZoom(256)" class="zoom-btn px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-500 text-black font-bold shadow-sm transition">4x (256px)</button>
        </div>
      </div>
    </div>

    <!-- Benchmark Row: Graviton Anomaly vs New Items -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      
      <!-- 0. REFERENCE: Graviton Anomaly -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border-2 border-orange-500/50 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-orange-500 tracking-wider">0. REFERÊNCIA ORIGINAL</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Graviton Anomaly</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-orange-500/10 text-orange-400 font-mono font-semibold">MOD ASSET</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{grav_b64}" alt="Graviton Anomaly" class="item-img pixelated glow-orange w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-orange-500">✓</span> Shaders vetoriais NumPy (coordenadas mgrid)</li>
            <li class="flex items-start gap-1.5"><span class="text-orange-500">✓</span> Beaming relativístico Doppler assimétrico</li>
            <li class="flex items-start gap-1.5"><span class="text-orange-500">✓</span> Disco de acreção espiral logarítmico 3D</li>
            <li class="flex items-start gap-1.5"><span class="text-orange-500">✓</span> Esfera de fótons & horizonte de eventos puro</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-orange-400">
          Estado: Baseline de Excelência Visual
        </div>
      </div>

      <!-- 1. Target Cartridge -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:border-cyan-500/50 transition">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-cyan-400 tracking-wider">1. LANÇA CINÉTICA (UEV)</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Target Cartridge</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono font-semibold">64x64 HD</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{tc_b64}" alt="Target Cartridge" class="item-img pixelated glow-cyan w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-cyan-400">✓</span> Chassi Duranium chanfrado com iluminação Phong</li>
            <li class="flex items-start gap-1.5"><span class="text-cyan-400">✓</span> Varredura de radar holográfica rotativa contínua</li>
            <li class="flex items-start gap-1.5"><span class="text-cyan-400">✓</span> Retículo de mira a laser com pulso de travamento</li>
            <li class="flex items-start gap-1.5"><span class="text-cyan-400">✓</span> Pinos dourados PCB & LEDs de status em tempo real</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-cyan-400">
          Arquivo: target_cartridge_64.gif / strip
        </div>
      </div>

      <!-- 2. Contained Particle -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:border-indigo-500/50 transition">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-indigo-400 tracking-wider">2. ANEL COLISOR (UIV)</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Contained Particle (Penning Trap)</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono font-semibold">64x64 HD</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{anti_b64}" alt="Contained Particle" class="item-img pixelated glow-purple w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-indigo-400">✓</span> Eletrodo quadrupolo toroidal hiperbólico central</li>
            <li class="flex items-start gap-1.5"><span class="text-indigo-400">✓</span> Tubo de vácuo cilíndrico com duplo reflexo especular</li>
            <li class="flex items-start gap-1.5"><span class="text-indigo-400">✓</span> Anéis de probabilidade quântica giroscópicos 3D</li>
            <li class="flex items-start gap-1.5"><span class="text-indigo-400">✓</span> Descargas de arco elétrico pulsando para o núcleo</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-indigo-400">
          Arquivo: contained_antiproton_64.gif / strip
        </div>
      </div>

      <!-- 3. Rift Probe -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:border-purple-500/50 transition">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-purple-400 tracking-wider">3. PORTÃO DE FENDA (UIV)</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Rift Probe</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 font-mono font-semibold">64x64 HD</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{rp_b64}" alt="Rift Probe" class="item-img pixelated glow-purple w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-purple-400">✓</span> Fuselagem supersônica em agulha cônica a 45°</li>
            <li class="flex items-start gap-1.5"><span class="text-purple-400">✓</span> Anéis cardânicos 3D de astrolábio girando ao redor</li>
            <li class="flex items-start gap-1.5"><span class="text-purple-400">✓</span> Ondas de choque de fase taquiônica expandindo da ponta</li>
            <li class="flex items-start gap-1.5"><span class="text-purple-400">✓</span> Pluma de propulsão iônica turbulenta oscilante</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-purple-400">
          Arquivo: rift_probe_64.gif / strip
        </div>
      </div>

      <!-- 4. Depth Anchor -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:border-gold-500/50 transition">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-amber-400 tracking-wider">4. PORTÃO DE FENDA (UIV)</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Depth Anchor</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-amber-500/10 text-amber-400 font-mono font-semibold">64x64 HD</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{da_b64}" alt="Depth Anchor" class="item-img pixelated glow-gold w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-amber-400">✓</span> Haste pesada forjada com chanfros especulares 3D</li>
            <li class="flex items-start gap-1.5"><span class="text-amber-400">✓</span> Ondas gravitacionais irradiando da coroa (mesma física do Graviton)</li>
            <li class="flex items-start gap-1.5"><span class="text-amber-400">✓</span> Pás de fenda quânticas com corte de fase taquion</li>
            <li class="flex items-start gap-1.5"><span class="text-amber-400">✓</span> Micro-singularidade de trava espacial central</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-amber-400">
          Arquivo: depth_anchor_64.gif / strip
        </div>
      </div>

      <!-- 5. Rift Singularity -->
      <div class="bg-[var(--card)] text-[var(--foreground)] border-2 border-purple-500/50 rounded-2xl p-5 shadow-sm flex flex-col justify-between hover:border-purple-400 transition">
        <div>
          <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
            <div>
              <span class="text-xs font-mono font-bold text-fuchsia-400 tracking-wider">5. PORTÃO DE FENDA (UIV/MAX)</span>
              <h3 class="text-base font-bold text-[var(--foreground)]">Rift Singularity</h3>
            </div>
            <span class="text-xs px-2 py-0.5 rounded bg-fuchsia-500/10 text-fuchsia-400 font-mono font-semibold">RIVAL DO GRAVITON</span>
          </div>
          
          <div class="flex justify-center items-center py-6 bg-[var(--background)] rounded-xl border border-[var(--border)] mb-4 overflow-hidden min-h-[220px]">
            <img src="{rs_b64}" alt="Rift Singularity" class="item-img pixelated glow-purple w-[160px] h-[160px] transition-all duration-300">
          </div>
          
          <ul class="text-xs space-y-1.5 text-[var(--muted-foreground)]">
            <li class="flex items-start gap-1.5"><span class="text-fuchsia-400">✓</span> Disco de acreção inclinado em 3D com micro-turbulência</li>
            <li class="flex items-start gap-1.5"><span class="text-fuchsia-400">✓</span> Beaming relativístico Doppler com gradiente ciano-dourado</li>
            <li class="flex items-start gap-1.5"><span class="text-fuchsia-400">✓</span> Fissuras de relâmpago dimensional rasgando o horizonte</li>
            <li class="flex items-start gap-1.5"><span class="text-fuchsia-400">✓</span> Horizonte de eventos negro absoluto com precessão quântica</li>
          </ul>
        </div>
        <div class="mt-4 pt-3 border-t border-[var(--border)] text-xs font-mono text-fuchsia-400">
          Arquivo: rift_singularity_64.gif / strip
        </div>
      </div>

    </div>

    <!-- Additional Showcase Strip for Particle Variations -->
    <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-6 shadow-sm">
      <div class="flex items-center justify-between pb-3 border-b border-[var(--border)] mb-4">
        <div>
          <h2 class="text-lg font-bold text-[var(--foreground)]">Variações de Partículas na Armadilha de Penning Criogênica</h2>
          <p class="text-xs text-[var(--muted-foreground)]">Todas renderizadas com tubos de quartzo hiperbólicos e núcleos quânticos exclusivos.</p>
        </div>
        <span class="text-xs font-mono text-cyan-400">ColliderCore.java</span>
      </div>
      
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] flex flex-col items-center">
          <img src="{anti_b64}" alt="Antiproton" class="item-img pixelated w-[96px] h-[96px] glow-cyan">
          <span class="text-xs font-bold text-cyan-400 mt-2">Antipróton</span>
          <span class="text-[11px] text-[var(--muted-foreground)]">5.6 GeV · Aniquilação</span>
        </div>
        <div class="bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] flex flex-col items-center">
          <img src="{higgs_b64}" alt="Higgs Boson" class="item-img pixelated w-[96px] h-[96px] glow-gold">
          <span class="text-xs font-bold text-amber-400 mt-2">Bóson de Higgs</span>
          <span class="text-[11px] text-[var(--muted-foreground)]">250 GeV · Escalar</span>
        </div>
        <div class="bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] flex flex-col items-center">
          <img src="{nexus_b64}" alt="X-Nexus" class="item-img pixelated w-[96px] h-[96px] glow-purple">
          <span class="text-xs font-bold text-purple-400 mt-2">X-Nexus</span>
          <span class="text-[11px] text-[var(--muted-foreground)]">4800 GeV · Grande Unif.</span>
        </div>
        <div class="bg-[var(--background)] p-3 rounded-xl border border-[var(--border)] flex flex-col items-center">
          <img src="{dewar_b64}" alt="Dewar Cell" class="item-img pixelated w-[96px] h-[96px] glow-cyan">
          <span class="text-xs font-bold text-cyan-300 mt-2">Célula Dewar</span>
          <span class="text-[11px] text-[var(--muted-foreground)]">1e11 p⁻ · Exo-nervuras</span>
        </div>
      </div>
    </div>

  </div>

  <script>
    function setZoom(size) {{
      const imgs = document.querySelectorAll('.item-img');
      imgs.forEach(img => {{
        img.style.width = size + 'px';
        img.style.height = size + 'px';
      }});
      
      const btns = document.querySelectorAll('.zoom-btn');
      btns.forEach(btn => {{
        btn.classList.remove('bg-amber-500', 'text-black', 'font-bold');
        btn.classList.add('bg-[var(--card)]', 'text-[var(--foreground)]');
      }});
      event.target.classList.add('bg-amber-500', 'text-black', 'font-bold');
      event.target.classList.remove('bg-[var(--card)]', 'text-[var(--foreground)]');
    }}
  </script>
</body>
</html>
"""

with open(ARTIFACT_PATH, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Artifact HTML gerado com sucesso em: {ARTIFACT_PATH}")
