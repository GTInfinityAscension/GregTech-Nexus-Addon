import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/gtna_texture_preview")
ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

materials = [
    ("echoite", "Echoite (Ec)", "#26734d", "Sculk & Pulso Sônico do Warden", "Material assinatura do GTNA com ondas sônicas e bio-luminescência sculk"),
    ("universium", "Universium (Σ§kX)", "#a855f7", "Cosmo Contínuo (30 Frames)", "Rework fluido do port legado GTNH com transição nebular e estelar"),
    ("ichorium", "Ichorium (IcMa)", "#d37806", "Âmbar Solar Táumico", "Ouro celestial thaumaturgo com aura arcana e reflexo dourado divino"),
    ("tengam_purified", "Purified Tengam (M)", "#badf70", "Fluxo Magnético Supercondutor", "Verde-limão denso com curvas de fluxo eletromagnético contínuo"),
    ("tengam_attuned", "Attuned Tengam (M)", "#d5ff80", "Ressonância Dipolar Elétrica", "Hiper-saturação elétrica com oscilação dipolar e micro-arcos"),
    ("fallking", "Fallking (HeLiCoPtEr)", "#FFCF6B", "Vórtice Cinético Aerodinâmico", "Superliga especial do GTNA com reflexo cinético rotacional e brilho solar"),
    ("odyssey", "Odyssey Nano Superalloy", "#4c7a6a", "Matriz Hexagonal Nanotecnológica", "Superliga espacial com pulso de rede nano-cristalina em favo de mel"),
    ("draconium", "Draconium (Dc)", "#9b30ff", "Respiração do Coração Dracônico", "Metal dragão púrpura profundo com pulsação abissal e ondas do vazio"),
    ("awakened_draconium", "Awakened Draconium (✵Dc✵)", "#ff6600", "Chama Solar Incandescente", "Despertar violento do dragão com plasma em ebulição e explosões no núcleo"),
    ("cosmic_neutronium", "Cosmic Neutronium", "#00d4ff", "Horizonte de Eventos & Galáxias", "Singularidade ultra-densa negra com constelações iridescentes cintilantes")
]

b64_data = {}
for m_id, name, color, badge, desc in materials:
    gif_path = OUT_DIR / f"{m_id}_ingot.gif"
    if gif_path.exists():
        b64 = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
        b64_data[m_id] = f"data:image/gif;base64,{b64}"
    else:
        b64_data[m_id] = ""

html = f"""<!DOCTYPE html>
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
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-xl p-4 shadow-sm max-w-4xl mx-auto">
    <div class="flex items-center justify-between pb-3 border-b border-[var(--border)]">
      <div>
        <h2 class="text-base font-bold text-[var(--foreground)] flex items-center gap-2">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          GTNA — Amostras de Texturas e Animações (30 Frames Fluidos)
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Visualização interativa das novas texturas procedurais animadas para os materiais</p>
      </div>
      <div class="text-xs font-mono px-2 py-1 rounded bg-[var(--background)] border border-[var(--border)] text-[var(--muted-foreground)]">
        10 Materiais
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3 pt-4">
"""

for m_id, name, color, badge, desc in materials:
    img_src = b64_data.get(m_id, "")
    html += f"""
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-2.5 flex flex-col items-center text-center hover:border-emerald-500/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-[var(--border)] flex items-center justify-center p-1 shadow-inner relative overflow-hidden group">
          <img src="{img_src}" class="w-16 h-16 pixelated object-contain transform group-hover:scale-110 transition-transform" alt="{name}">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)] leading-tight">{name}</div>
        <div class="mt-1 text-[11px] px-1.5 py-0.5 rounded border border-[var(--border)] font-mono text-[var(--muted-foreground)] truncate max-w-full" style="color: {color};">
          {badge}
        </div>
        <p class="text-[11px] text-[var(--muted-foreground)] mt-1.5 leading-tight line-clamp-3">
          {desc}
        </p>
      </div>
"""

html += """
    </div>
    <div class="mt-4 pt-3 border-t border-[var(--border)] flex items-center justify-between text-xs text-[var(--muted-foreground)]">
      <span>Taxa: 30 frames (frametime: 2 ticks, interpolação bilinear ativa)</span>
      <span class="text-emerald-500 font-medium">Renderizado a 16x16 nativo (upscaled no preview)</span>
    </div>
  </div>
</body>
</html>
"""

target = ARTIFACT_DIR / "texture_refactor_showcase.html"
target.write_text(html)
print(f"Widget gerado com sucesso em: {target}")
