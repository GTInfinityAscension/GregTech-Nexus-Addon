import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/shijima_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (240, 240, 240, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (240, 240, 240, 255))

# =========================================================================
# Opção 1: Absolute Zero Quantum Stillness (Serenidade do Zero Absoluto)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Platina pérola translúcida com sombras azul-ártico
        r = 35.0 + t_base * 195.0
        g = 45.0 + (t_base ** 1.1) * 195.0
        b = 65.0 + (t_base ** 1.2) * 190.0
        
        # Ondas ultra-lentas de condensação quântica (Bose-Einstein relaxamento)
        thermal_stillness = np.sin(2 * np.pi * (t * 1.0 - dist / 6.0))
        condensate = np.exp(-((thermal_stillness - 0.7) / 0.35)**2) * (t_base > 0.25)
        
        # Geada quântica cristalina sutil
        frost_shimmer = np.sin(x_coords * 2.5 + y_coords * 2.5 + 2 * np.pi * t * 2.0) * 0.5 + 0.5
        frost = (frost_shimmer ** 4.0) * condensate * 0.8
        
        total_stillness = (condensate * 0.85 + frost * 0.65) * (t_base > 0.3)
        
        # Tons de gelo celestial e azul-platina
        r += total_stillness * 35.0
        g += total_stillness * 95.0
        b += total_stillness * 165.0
        
        # Picos de reflexo cristalino branco puro
        ice_gleam = np.clip(total_stillness - 0.65, 0, 1.2) * 110.0
        r += ice_gleam * 0.95
        g += ice_gleam * 0.98
        b += ice_gleam * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Zen Silence Lotus Ripple (Ondulações do Vazio de Lótus Zen)
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    angle = np.arctan2(y_coords - cy, x_coords - cx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Prata pura celestial acetinada
        r = 40.0 + t_base * 190.0
        g = 48.0 + (t_base ** 1.1) * 192.0
        b = 68.0 + (t_base ** 1.15) * 187.0
        
        # Simetria de pétalas de lótus de 8 dobras
        lotus_mod = np.cos(8.0 * angle)
        r_lotus = dist * (1.0 + 0.22 * lotus_mod)
        
        # Onda de silêncio meditativo se expandindo suavemente
        wave = np.sin(2 * np.pi * (r_lotus / 4.2 - t * 1.5))
        ripple = np.exp(-((wave - 0.7) / 0.4)**2) * (t_base > 0.28)
        
        # Nós de quietude absoluta no centro
        zen_core = np.exp(-((dist / 3.2)**2)) * (0.6 + 0.4 * np.cos(2 * np.pi * t)) * (t_base > 0.35)
        
        total_zen = (ripple * 0.9 + zen_core * 1.1) * (t_base > 0.25)
        
        # Cores: azul-celeste translúcido e brilho prateado divino
        r += total_zen * 50.0
        g += total_zen * 110.0
        b += total_zen * 175.0
        
        zen_white = np.clip(total_zen - 0.7, 0, 1.2) * 120.0
        r += zen_white * 0.96
        g += zen_white * 0.98
        b += zen_white * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Superluminal Cherenkov Vacuum (Vácuo Cherenkov Hiperluminal)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Eixo diagonal de propagação translúcida sem atrito (ângulo 45°)
    diag = (x_coords * 0.707 + y_coords * 0.707)
    cross_diag = (-x_coords * 0.707 + y_coords * 0.707)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Platina-titânio frio com reflexos safira
        r = 32.0 + t_base * 192.0
        g = 42.0 + (t_base ** 1.1) * 195.0
        b = 62.0 + (t_base ** 1.2) * 193.0
        
        # Frentes de onda de Cherenkov deslizando através do cristal
        sweep = (diag - t * 14.0) % 11.0
        cherenkov_cone = np.exp(-((sweep - 5.5) / 1.5)**2) * (t_base > 0.3)
        
        # Dispersão prismática na frente de onda
        prism_wave = np.sin(2 * np.pi * (cross_diag / 4.0 + t * 1.0)) * 0.5 + 0.5
        prism = cherenkov_cone * prism_wave * 0.8
        
        total_cherenkov = (cherenkov_cone * 0.95 + prism * 0.7) * (t_base > 0.25)
        
        # Brilho Cherenkov azul-turquesa glacial luminoso
        r += total_cherenkov * 40.0
        g += total_cherenkov * 125.0
        b += total_cherenkov * 185.0
        
        white_cone = np.clip(total_cherenkov - 0.75, 0, 1.2) * 125.0
        r += white_cone * 0.94
        g += white_cone * 0.98
        b += white_cone * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

def create_gif(frames, path, duration_ms=66):
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        disposal=2
    )

def main():
    print("Gerando candidatos para Shijima (静寂)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Absolute Zero Stillness", render_option_1),
        (2, "Zen Silence Lotus Ripple", render_option_2),
        (3, "Superluminal Cherenkov Vacuum", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"shijima_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (shijima_grid.png)
    # Linhas: 4 shapes (Ingot, Plate, Gear, Block). Colunas: 3 Opções
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 36
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (11, 16, 24, 255)) # Dark celestial navy
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "SHIJIMA — VISUAL CANDIDATES (128x128)", fill=(196, 214, 242, 255), font=font_title)
    draw.text((pad_x, 38), "Absolute Silence • Platinum Pearl & Celestial Ice • 30 Frames Fluidos", fill=(148, 163, 184, 255), font=font_sub)
    
    # Headers das colunas
    col_titles = [
        "OPÇÃO 1: Zero Stillness",
        "OPÇÃO 2: Zen Lotus",
        "OPÇÃO 3: Cherenkov Vacuum"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(226, 232, 240, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        # Label da forma
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(148, 163, 184, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][12]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (18, 25, 36) if (bx // 16 + by // 16) % 2 == 0 else (13, 19, 29)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(147, 197, 253, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "shijima_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML com a estrutura interativa completa
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shijima (静寂) — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #080d14;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      padding: 20px;
      line-height: 1.5;
    }}
    .container {{
      max-width: 1040px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 18px;
    }}
    .header-card {{
      background: linear-gradient(135deg, #102038 0%, #0d1726 60%, #080d14 100%);
      border: 1px solid rgba(196, 214, 242, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(147, 197, 253, 0.18);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(147, 197, 253, 0.18);
      color: #bfdbfe;
      border: 1px solid rgba(147, 197, 253, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #e0f2fe;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #c4d6f2, #93c5fd);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #94a3b8;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #0f1926;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #1e2e42;
    }}
    .btn-toggle {{
      background: #2563eb;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #3b82f6;
    }}
    
    .shape-bar {{
      background: #0f1926;
      border: 1px solid #1e2e42;
      border-radius: 12px;
      padding: 12px 18px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .shape-buttons {{
      display: flex;
      gap: 6px;
      background: #090e17;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1e2e42;
    }}
    .btn-shape {{
      background: transparent;
      color: #94a3b8;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #2563eb;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #1e2e42;
    }}
    
    .grid-options {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    @media (max-width: 820px) {{
      .grid-options {{
        grid-template-columns: 1fr;
      }}
    }}
    
    .card {{
      background: #0e1724;
      border: 2px solid #1a2a3e;
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      transition: all 0.25s ease;
      position: relative;
    }}
    .card:hover {{
      border-color: rgba(147, 197, 253, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #93c5fd;
      box-shadow: 0 0 20px rgba(147, 197, 253, 0.25);
    }}
    
    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .tag-opt {{
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: rgba(147, 197, 253, 0.18);
      color: #bfdbfe;
      border: 1px solid rgba(147, 197, 253, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #f1f5f9;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #060a10;
      border: 1px solid #162436;
      border-radius: 12px;
      padding: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 180px;
      position: relative;
      overflow: hidden;
    }}
    
    .pixelated-art {{
      image-rendering: -moz-crisp-edges;
      image-rendering: -webkit-crisp-edges;
      image-rendering: pixelated;
      image-rendering: crisp-edges;
      width: 128px !important;
      height: 128px !important;
      min-width: 128px;
      min-height: 128px;
      max-width: 128px;
      max-height: 128px;
      object-fit: contain;
      display: block;
      transition: transform 0.2s ease;
    }}
    
    @keyframes celestialGlowPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 8px rgba(147, 197, 253, 0.8)) drop-shadow(0 0 20px rgba(96, 165, 250, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 16px rgba(191, 219, 254, 1.0)) drop-shadow(0 0 32px rgba(147, 197, 253, 0.7));
        transform: scale(1.02);
      }}
    }}
    .glow-effect {{
      animation: celestialGlowPulse 2.6s ease-in-out infinite;
    }}
    
    .btn-approve {{
      width: 100%;
      padding: 11px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      border: none;
      cursor: pointer;
      transition: all 0.2s;
      background: #16263b;
      color: #cbd5e1;
    }}
    .btn-approve:hover {{
      background: #2563eb;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #2563eb, #60a5fa);
      color: #ffffff;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      margin-top: 8px;
    }}
    .feature-item {{
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #132236;
      color: #bfdbfe;
      border: 1px solid #1d334f;
    }}
    
    .footer-box {{
      background: #0f1926;
      border: 1px solid #1e2e42;
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: #94a3b8;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <div>
          <span class="badge">GTNA Legendary Material</span>
          <span class="formula-tag">Shijima (静寂) • #C4D6F2</span>
        </div>
        <h1>Shijima — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas fluidas de 30 frames combinadas com o <strong>Celestial Glow/Halo Shader</strong> (<code style="color:#bfdbfe">gtna:glow_edge / halo</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#93c5fd;">GLOW ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleGlow" onclick="toggleShader()">Alternar Shader</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-plate" onclick="setShape('plate')">Placa (Plate)</button>
          <button class="btn-shape" id="btn-gear" onclick="setShape('gear')">Engrenagem (Gear)</button>
          <button class="btn-shape" id="btn-block" onclick="setShape('block')">Bloco (Block)</button>
        </div>
      </div>
      <div style="font-size:11px; color:#64748b;">
        Tamanho: <strong>128×128px (8× Zoom Pixel Art Nítido)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#64748b;">Zero Stillness</span>
          </div>
          <div class="card-title">Absolute Zero Quantum Stillness</div>
          <p class="card-desc">
            Cessação completa de vibração térmica atômica: <strong>anéis ultra-suaves de condensação de Bose-Einstein</strong> expandindo em câmera lenta com névoa azul-ártico e geada quântica estelar.
          </p>
          <div class="features-list">
            <span class="feature-item">Condensação Bose-Einstein</span>
            <span class="feature-item">Geada Quântica</span>
            <span class="feature-item">Relaxamento Térmico Frio</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-1" class="glow-effect">
            <img id="img-1" class="pixelated-art" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(1)">Aprovar Opção 1 (Responder 1)</button>
      </div>

      <!-- Option 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 2</span>
            <span style="font-size:11px; color:#64748b;">Zen Lotus</span>
          </div>
          <div class="card-title">Zen Silence Lotus Ripple</div>
          <p class="card-desc">
            A quietude do vazio sagrado (静寂): <strong>gota no espelho de metal líquido</strong> gerando ondulações concêntricas harmônicas que formam uma flor de lótus de luz etérea respirando em ritmo meditativo.
          </p>
          <div class="features-list">
            <span class="feature-item">Lótus de 8 Pétalas</span>
            <span class="feature-item">Ondulação Meditativa</span>
            <span class="feature-item">Nós de Silêncio Perfeito</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-2" class="glow-effect">
            <img id="img-2" class="pixelated-art" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(2)">Aprovar Opção 2 (Responder 2)</button>
      </div>

      <!-- Option 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 3</span>
            <span style="font-size:11px; color:#64748b;">Cherenkov Vacuum</span>
          </div>
          <div class="card-title">Superluminal Cherenkov Vacuum</div>
          <p class="card-desc">
            Silêncio acústico absoluto em meio superluminal: <strong>feixes translúcidos de luz Cherenkov azul-celeste e platina</strong> deslizando sem atrito através da rede cristalina com dispersão prismática nas bordas.
          </p>
          <div class="features-list">
            <span class="feature-item">Feixes Cherenkov 45°</span>
            <span class="feature-item">Dispersão Prismática</span>
            <span class="feature-item">Vácuo Sem Ruído Térmico</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-3" class="glow-effect">
            <img id="img-3" class="pixelated-art" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(3)">Aprovar Opção 3 (Responder 3)</button>
      </div>

    </div>

    <div class="footer-box">
      <div>
        Status: <strong style="color:#93c5fd;">Aguardando aprovação do autor</strong>
      </div>
      <div>
        Responda <strong>1</strong>, <strong>2</strong> ou <strong>3</strong> para aplicar no GTNA.
      </div>
    </div>

  </div>

  <script>
    const b64Data = {json_b64};
    let currentShape = 'ingot';
    let shaderActive = true;
    let selectedOption = 1;

    function setShape(shape) {{
      currentShape = shape;
      document.querySelectorAll('.btn-shape').forEach(btn => btn.classList.remove('active'));
      document.getElementById('btn-' + shape).classList.add('active');

      for (let opt = 1; opt <= 3; opt++) {{
        const img = document.getElementById('img-' + opt);
        if (b64Data[opt] && b64Data[opt][shape]) {{
          img.src = b64Data[opt][shape];
        }}
      }}
    }}

    function toggleShader() {{
      shaderActive = !shaderActive;
      const statusText = document.getElementById('shaderStatusText');
      const btn = document.getElementById('btnToggleGlow');

      for (let opt = 1; opt <= 3; opt++) {{
        const wrapper = document.getElementById('wrapper-' + opt);
        if (shaderActive) {{
          wrapper.classList.add('glow-effect');
        }} else {{
          wrapper.classList.remove('glow-effect');
        }}
      }}

      if (shaderActive) {{
        statusText.innerText = 'GLOW ATIVADO';
        statusText.style.color = '#93c5fd';
        btn.innerText = 'Desativar Glow';
        btn.style.background = '#2563eb';
      }} else {{
        statusText.innerText = 'SHADER DESLIGADO';
        statusText.style.color = '#64748b';
        btn.innerText = 'Ativar Glow';
        btn.style.background = '#334155';
      }}
    }}

    function selectCard(opt) {{
      selectedOption = opt;
      for (let i = 1; i <= 3; i++) {{
        const card = document.getElementById('card-' + i);
        if (i === opt) {{
          card.classList.add('selected');
        }} else {{
          card.classList.remove('selected');
        }}
      }}
    }}
  </script>
</body>
</html>
"""
    html_path = ARTIFACT_DIR / "shijima_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
