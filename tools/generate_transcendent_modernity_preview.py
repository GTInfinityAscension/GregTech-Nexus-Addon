import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/transcendent_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/ae8c45a3-c2ac-4603-b702-fb14928ac605")
PREVIEWS_DEST = ARTIFACT_DIR / "previews_transcendent"
PREVIEWS_DEST.mkdir(parents=True, exist_ok=True)

MODERNITY_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_SPACETIME_BLOCK = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/iconsets/BLOCK_SPACETIME.png")

SAMPLES = {
    "ingot": MODERNITY_ITEMS / "ingot.png",
    "plate": MODERNITY_ITEMS / "plate.png",
    "gear": MODERNITY_ITEMS / "gearGt.png",
    "block": MODERNITY_BLOCKS / "block1.png"
}

def load_base(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    h, w = arr.shape[:2]
    if h > w:
        arr = arr[:w, :, :]
    return arr

# 1. Spacetime 113-frame source
im_st = Image.open(MODERNITY_SPACETIME_BLOCK).convert("RGB")
w = 16
n_st = im_st.size[1] // w
frames_st_lum = []
for i in range(n_st):
    f_rgb = np.array(im_st.crop((0, i * w, w, (i + 1) * w)), dtype=np.float32)
    lum = 0.299 * f_rgb[:, :, 0] + 0.587 * f_rgb[:, :, 1] + 0.114 * f_rgb[:, :, 2]
    frames_st_lum.append(lum)

sample_indices_st = [int(round(i * (n_st - 1) / 29)) for i in range(30)]

def render_spacetime_recolor(base_arr):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_item = gray / 255.0
    
    frames = []
    for idx in sample_indices_st:
        lum = frames_st_lum[idx]
        cube_norm = np.clip((lum - 20.0) / 150.0, 0, 1)
        base_r = 18.0 + t_item * 65.0
        base_g = 18.0 + t_item * 65.0
        base_b = 24.0 + t_item * 75.0
        
        add_r = cube_norm * 160.0 * (0.35 + 0.65 * t_item)
        add_g = cube_norm * 175.0 * (0.35 + 0.65 * t_item)
        add_b = cube_norm * 210.0 * (0.35 + 0.65 * t_item)
        
        frame = np.zeros((16, 16, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(base_r + add_r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(base_g + add_g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(base_b + add_b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# 2. True 4D Mathematical Tesseract
vertices_4d = []
for x in [-1, 1]:
    for y in [-1, 1]:
        for z in [-1, 1]:
            for w_c in [-1, 1]:
                vertices_4d.append(np.array([x, y, z, w_c], dtype=np.float32))

edges_4d = []
for i in range(16):
    for j in range(i + 1, 16):
        if np.sum(np.abs(vertices_4d[i] - vertices_4d[j]) > 0.1) == 1:
            edges_4d.append((i, j))

def rotate_4d(v, theta, phi):
    x, y, z, w_c = v
    x_rot = x * np.cos(theta) - w_c * np.sin(theta)
    w_rot = x * np.sin(theta) + w_c * np.cos(theta)
    y_rot = y * np.cos(phi) - z * np.sin(phi)
    z_rot = y * np.sin(phi) + z * np.cos(phi)
    return np.array([x_rot, y_rot, z_rot, w_rot])

def project_to_2d(v4):
    d4 = 2.4
    scale_w = 1.0 / (d4 - v4[3] * 0.45)
    x3 = v4[0] * scale_w
    y3 = v4[1] * scale_w
    z3 = v4[2] * scale_w
    iso_x = 7.5 + (x3 - y3) * 3.6
    iso_y = 7.5 + ((x3 + y3) * 0.5 - z3) * 3.2
    return iso_x, iso_y

def draw_line(grid, p1, p2, val=1.0):
    x0, y0 = p1
    x1, y1 = p2
    steps = max(int(np.hypot(x1 - x0, y1 - y0) * 4), 2)
    for s in range(steps + 1):
        t = s / steps
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        ix, iy = int(round(x)), int(round(y))
        if 0 <= ix < 16 and 0 <= iy < 16:
            dist = np.hypot(ix - x, iy - y)
            w_val = max(0.0, 1.0 - dist)
            grid[iy, ix] = max(grid[iy, ix], w_val * val)

def render_true_4d_tesseract(base_arr):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_item = gray / 255.0
    
    frames = []
    for f in range(30):
        theta = 2 * np.pi * (f / 30.0)
        phi = 2 * np.pi * (f / 30.0) * 0.5
        v2d = [project_to_2d(rotate_4d(v, theta, phi)) for v in vertices_4d]
        
        grid = np.zeros((16, 16), dtype=np.float32)
        for i, j in edges_4d:
            w_avg = (rotate_4d(vertices_4d[i], theta, phi)[3] + rotate_4d(vertices_4d[j], theta, phi)[3]) * 0.5
            edge_brightness = 0.55 + 0.45 * ((w_avg + 1.4) / 2.8)
            draw_line(grid, v2d[i], v2d[j], val=edge_brightness)
            
        for pt in v2d:
            ix, iy = int(round(pt[0])), int(round(pt[1]))
            if 0 <= ix < 16 and 0 <= iy < 16:
                grid[iy, ix] = 1.0
                
        base_r = 18.0 + t_item * 68.0
        base_g = 18.0 + t_item * 68.0
        base_b = 24.0 + t_item * 78.0
        
        add_r = grid * 165.0 * (0.35 + 0.65 * t_item)
        add_g = grid * 180.0 * (0.35 + 0.65 * t_item)
        add_b = grid * 220.0 * (0.35 + 0.65 * t_item)
        
        frame = np.zeros((16, 16, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(base_r + add_r, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(base_g + add_g, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(base_b + add_b, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

# 3. Gravitational Lensing & Horizon
def render_gravitational_lens(base_arr):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_item = gray / 255.0
    
    y_coords, x_coords = np.ogrid[:h, :w]
    gx, gy = 7.5, 7.5
    r = np.sqrt((x_coords - gx) ** 2 + (y_coords - gy) ** 2)
    angle = np.arctan2(y_coords - gy, x_coords - gx)
    
    frames = []
    for f in range(30):
        t = f / 30.0
        beam_angle = angle - 2 * np.pi * t
        doppler = np.clip(np.cos(beam_angle), 0, 1) ** 2
        
        ring1 = np.exp(-((r - 3.2) ** 2) / 0.9) * (0.6 + 0.8 * doppler)
        ring2 = np.exp(-((r - 5.8) ** 2) / 1.1) * (0.4 + 0.9 * (1.0 - doppler))
        caustic = (ring1 + ring2) * (0.35 + 0.65 * t_item)
        
        base_r = 18.0 + t_item * 68.0
        base_g = 18.0 + t_item * 68.0
        base_b = 24.0 + t_item * 78.0
        
        add_r = caustic * 145.0
        add_g = caustic * 155.0
        add_b = caustic * 205.0
        
        rim = np.exp(-((r - 1.8) ** 2) / 0.5) * 45.0
        
        frame = np.zeros((16, 16, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(base_r + add_r + rim * 0.9, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(base_g + add_g + rim * 0.9, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(base_b + add_b + rim * 1.3, 0, 255), 0)
        frame[:, :, 3] = np.where(alpha, 255, 0)
        frames.append(frame)
    return frames

def save_gif(frames, out_path, duration=66):
    pil_frames = [Image.fromarray(f) for f in frames]
    scaled_frames = [f.resize((80, 80), Image.NEAREST) for f in pil_frames]
    scaled_frames[0].save(
        out_path,
        save_all=True,
        append_images=scaled_frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )

def to_base64_gif(gif_path):
    with open(gif_path, "rb") as f:
        return "data:image/gif;base64," + base64.b64encode(f.read()).decode("utf-8")

def main():
    b64_data = {}
    for item_name, path in SAMPLES.items():
        arr = load_base(path)
        
        f1 = render_spacetime_recolor(arr)
        f2 = render_true_4d_tesseract(arr)
        f3 = render_gravitational_lens(arr)
        
        p1 = OUT_DIR / f"{item_name}_c1.gif"
        p2 = OUT_DIR / f"{item_name}_c2.gif"
        p3 = OUT_DIR / f"{item_name}_c3.gif"
        
        save_gif(f1, p1)
        save_gif(f2, p2)
        save_gif(f3, p3)
        
        save_gif(f1, PREVIEWS_DEST / f"{item_name}_c1.gif")
        save_gif(f2, PREVIEWS_DEST / f"{item_name}_c2.gif")
        save_gif(f3, PREVIEWS_DEST / f"{item_name}_c3.gif")
        
        b64_data[item_name] = {
            "c1_spacetime_asset": to_base64_gif(p1),
            "c2_true_4d": to_base64_gif(p2),
            "c3_lens": to_base64_gif(p3)
        }
        
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
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-slate-300 animate-pulse"></span>
          Transcendent Metal (TsЖ) — Comparativo 3D/4D
        </h2>
        <p class="text-xs text-[var(--muted-foreground)]">Asset do Spacetime vs Novo Tesseract 4D Dedicado vs Lente Gravitacional</p>
      </div>
      <div class="flex gap-1 bg-[var(--background)] p-1 rounded-lg border border-[var(--border)] text-xs" id="itemSelector">
        <button onclick="setItem('ingot')" id="btn-ingot" class="px-2.5 py-1 rounded font-medium bg-[var(--primary)] text-[var(--primary-foreground)]">Barra</button>
        <button onclick="setItem('plate')" id="btn-plate" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Placa</button>
        <button onclick="setItem('gear')" id="btn-gear" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Engrenagem</button>
        <button onclick="setItem('block')" id="btn-block" class="px-2.5 py-1 rounded font-medium text-[var(--muted-foreground)] hover:text-[var(--foreground)]">Bloco</button>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-3 pt-3">
      <!-- Opção 1: Asset do Spacetime do Modernity -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-slate-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-slate-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c1" src="{b64_data['ingot']['c1_spacetime_asset']}" class="w-16 h-16 pixelated object-contain" alt="Asset do Spacetime">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">1. Asset Spacetime (Modernity)</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          A textura 3D/4D original do Spacetime do Modernity recolorida em titânio grafite.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-slate-400/10 text-slate-300 font-mono">Asset Spacetime</div>
      </div>

      <!-- Opção 2: Tesseract 4D Matemático Dedicado -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-violet-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-violet-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c2" src="{b64_data['ingot']['c2_true_4d']}" class="w-16 h-16 pixelated object-contain" alt="Tesseract 4D Dedicado">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">2. Tesseract 4D Dedicado</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Verdadeiro hipercubo 4D com 32 arestas rotacionando e se invertendo em perspectiva isométrica (único para TsЖ).
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-violet-400/10 text-violet-300 font-mono">4D Schlegel Próprio</div>
      </div>

      <!-- Opção 3: Lente Gravitacional -->
      <div class="bg-[var(--background)] border border-[var(--border)] rounded-lg p-3 flex flex-col items-center text-center hover:border-indigo-400/50 transition-colors">
        <div class="w-20 h-20 bg-slate-950 rounded border border-indigo-400/30 flex items-center justify-center p-1 shadow-inner relative overflow-hidden">
          <img id="img-c3" src="{b64_data['ingot']['c3_lens']}" class="w-16 h-16 pixelated object-contain" alt="Lente Gravitacional">
        </div>
        <div class="mt-2 font-semibold text-xs text-[var(--foreground)]">3. Lente Gravitacional</div>
        <p class="text-[12px] text-[var(--muted-foreground)] mt-1 leading-tight">
          Distorção óptica da Spatially Transcendent Gravitational Lens com anéis de Einstein e horizonte de eventos.
        </p>
        <div class="mt-2 text-[12px] px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-400 font-mono">Anéis de Einstein</div>
      </div>
    </div>

    <div class="mt-3 pt-2 border-t border-[var(--border)] flex justify-between items-center text-xs text-[var(--muted-foreground)]">
      <span>Escolha entre o asset do Spacetime ou o novo Tesseract 4D dedicado</span>
      <span class="text-slate-400">30 quadros em loop contínuo</span>
    </div>
  </div>

  <script>
    const images = {json.dumps(b64_data)};
    let currentItem = 'ingot';

    function setItem(item) {{
      currentItem = item;
      document.getElementById('img-c1').src = images[item]['c1_spacetime_asset'];
      document.getElementById('img-c2').src = images[item]['c2_true_4d'];
      document.getElementById('img-c3').src = images[item]['c3_lens'];

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
    with open(ARTIFACT_DIR / "transcendent_metal_preview.html", "w") as f:
        f.write(html_content)
    print("Done! Updated transcendent_metal_preview.html")

if __name__ == "__main__":
    main()
