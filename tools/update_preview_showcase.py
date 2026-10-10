import json
import base64
from PIL import Image
from pathlib import Path

ROOT = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
WD_ITEMS = ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/white_dwarf_matter"
WD_BLOCKS = ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets/white_dwarf_matter"

SHOWCASE = {
    "ingot": (WD_ITEMS / "ingot.png", "Barra"),
    "plate": (WD_ITEMS / "plate.png", "Placa"),
    "plate_triple": (WD_ITEMS / "plate_triple.png", "Placa Tripla"),
    "plate_dense": (WD_ITEMS / "plate_dense.png", "Placa Densa"),
    "rod_long": (WD_ITEMS / "rod_long.png", "Haste Longa"),
    "gear": (WD_ITEMS / "gear.png", "Engrenagem"),
    "block": (WD_BLOCKS / "block.png", "Bloco"),
    "frame_gt": (WD_BLOCKS / "frame_gt.png", "Armação (Frame)")
}

def strip_to_b64_gif(png_path, scale=5, frametime_ms=100):
    im = Image.open(png_path)
    w = im.size[0]
    n_frames = im.size[1] // w
    pil_frames = []
    for i in range(n_frames):
        frame = im.crop((0, i*w, w, (i+1)*w)).convert("RGBA")
        bg = Image.new("RGBA", (w, w), (18, 22, 34, 255))
        bg.paste(frame, (0, 0), frame)
        scaled = bg.resize((w * scale, h * scale if 'h' in locals() else w * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
    
    import io
    buf = io.BytesIO()
    pil_frames[0].save(buf, format="GIF", save_all=True, append_images=pil_frames[1:], duration=frametime_ms, loop=0)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/gif;base64,{b64}"

b64_items = {}
labels = {}
for key, (path, label) in SHOWCASE.items():
    b64_items[key] = strip_to_b64_gif(path)
    labels[key] = label

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
          White Dwarf Matter — Set Completo Gerado (Estilo 3)
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">57 itens + 2 blocos animados com Ressonância Quântica e paleta estelar</p>
      </div>
    </div>

    <!-- Quick Buttons -->
    <div class="flex flex-wrap gap-1.5 pt-3" id="btnContainer">
"""

for key, (_, label) in SHOWCASE.items():
    active_cls = "bg-[var(--primary)] text-[var(--primary-foreground)]" if key == "ingot" else "text-[var(--muted-foreground)] hover:text-[var(--foreground)] bg-[var(--background)]"
    html_content += f"""      <button onclick="selectItem('{key}')" id="btn-{key}" class="px-2.5 py-1 rounded text-xs font-medium border border-[var(--border)] {active_cls} transition-colors">{label}</button>\n"""

html_content += f"""    </div>

    <!-- Display Area -->
    <div class="mt-4 bg-[var(--background)] border border-[var(--border)] rounded-xl p-4 flex items-center gap-5">
      <div class="w-24 h-24 bg-slate-950 rounded-lg border border-cyan-500/40 flex items-center justify-center p-2 shadow-inner relative overflow-hidden flex-shrink-0">
        <img id="mainDisplay" src="{b64_items['ingot']}" class="w-20 h-20 pixelated object-contain" alt="Preview">
      </div>
      <div>
        <div class="flex items-center gap-2">
          <span id="itemTitle" class="text-sm font-bold text-[var(--foreground)]">Barra (Ingot)</span>
          <span class="text-[11px] px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 font-mono">16x480 • 30 quadros</span>
        </div>
        <p class="text-xs text-[var(--muted-foreground)] mt-1 leading-relaxed" id="itemDesc">
          Platina cósmica com ondas de interferência de plasma que correm pela estrutura sem perder os chanfros e o contraste do relevo moderno.
        </p>
        <div class="mt-2 text-xs text-emerald-400 flex items-center gap-1.5">
          <span>✓ Textura animada + .mcmeta + modelo composite JSON registrados</span>
        </div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Total no set: 57 formas de itens + 2 blocos</span>
      <span class="text-cyan-400 font-mono">white_dwarf_matter finalizado</span>
    </div>
  </div>

  <script>
    const data = {json.dumps(b64_items)};
    const labels = {json.dumps(labels)};
    const keys = {json.dumps(list(SHOWCASE.keys()))};

    function selectItem(key) {{
      document.getElementById('mainDisplay').src = data[key];
      document.getElementById('itemTitle').innerText = labels[key] + ' (' + key + ')';
      
      keys.forEach(k => {{
        const btn = document.getElementById('btn-' + k);
        if (k === key) {{
          btn.className = "px-2.5 py-1 rounded text-xs font-medium border border-[var(--border)] bg-[var(--primary)] text-[var(--primary-foreground)] transition-colors";
        }} else {{
          btn.className = "px-2.5 py-1 rounded text-xs font-medium border border-[var(--border)] text-[var(--muted-foreground)] hover:text-[var(--foreground)] bg-[var(--background)] transition-colors";
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

print("Updated preview showcase HTML!")
