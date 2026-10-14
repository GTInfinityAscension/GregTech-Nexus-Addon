import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/advanced_nitinol_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (210, 180, 140, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (210, 180, 140, 255))

# =========================================================================
# Opção 1: Thermo-Elastic Martensite Twin Lattice (Geminação Martensítica)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Eixos cristalográficos de cisalhamento a 45 graus
    u1 = (x_coords + y_coords) * 0.707
    u2 = (x_coords - y_coords) * 0.707
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Bronze-champanhe / Níquel-Titânio aquecido (#D2B48C)
        r = 50.0 + t_base * 160.0
        g = 36.0 + (t_base ** 1.15) * 144.0
        b = 20.0 + (t_base ** 1.35) * 120.0
        
        # Planos de geminação martensítica alternando por ciclo térmico
        thermal_cycle = np.sin(2 * np.pi * t)
        weight_u1 = (thermal_cycle + 1.0) * 0.5
        weight_u2 = 1.0 - weight_u1
        
        stripes_1 = np.exp(-(((u1 % 3.0) - 1.5) / 0.4)**2)
        stripes_2 = np.exp(-(((u2 % 3.0) - 1.5) / 0.4)**2)
        
        twin_lattice = (stripes_1 * weight_u1 + stripes_2 * weight_u2) * (t_base > 0.28)
        
        # Flashes nos nós de estresse de cisalhamento
        shear_nodes = (stripes_1 * stripes_2) * 2.2 * (t_base > 0.35)
        
        total_fx = twin_lattice * 0.8 + shear_nodes * 1.1
        
        # Brilho dourado/âmbar termo-mecânico
        r += total_fx * 155.0
        g += total_fx * 125.0
        b += total_fx * 45.0
        
        # Picos de alívio superelástico branco-solar
        flash = np.clip(shear_nodes - 0.7, 0, 1.2) * 115.0
        r += flash * 0.98
        g += flash * 0.95
        b += flash * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Shape-Memory Hysteresis Pulse (Pulso de Histerese com Memória de Forma)
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
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Ouro-bronze acetinado
        r = 48.0 + t_base * 162.0
        g = 35.0 + (t_base ** 1.2) * 145.0
        b = 18.0 + (t_base ** 1.4) * 122.0
        
        # Ciclo assimétrico de histerese: compressão lenta (70%) e disparo elástico (30%)
        if t < 0.7:
            # Fase de absorção de estresse térmico
            phase_t = t / 0.7
            wave_rad = 7.0 * (1.0 - phase_t)
            hysteresis = np.exp(-((dist - wave_rad) / 1.5)**2) * 0.65
            shock = 0.0
        else:
            # Disparo superelástico de recuperação geométrica instantânea
            phase_t = (t - 0.7) / 0.3
            wave_rad = phase_t * 9.0
            hysteresis = 0.0
            shock = np.exp(-((dist - wave_rad) / 1.2)**2) * 1.5
            
        total_mem = (hysteresis + shock) * (t_base > 0.25)
        
        r += total_mem * 160.0
        g += total_mem * 130.0
        b += total_mem * 50.0
        
        flash = np.clip(shock - 0.8, 0, 1.4) * 120.0
        r += flash * 0.98
        g += flash * 0.95
        b += flash * 0.88
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Superelastic Kinetic Slipstream (Esteira Cinética Superelástica)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        r = 45.0 + t_base * 165.0
        g = 34.0 + (t_base ** 1.2) * 146.0
        b = 18.0 + (t_base ** 1.4) * 122.0
        
        # Feixes lineares contínuos de escoamento superelástico sem histerese permanente
        slipstream = np.sin(2 * np.pi * (x_coords / 4.5 - t * 2.5)) * np.cos(2 * np.pi * (y_coords / 6.0))
        slip_glow = (np.maximum(0, slipstream) ** 2.2) * (t_base > 0.3)
        
        # Vórtices térmicos de alívio rápido
        vortex = np.sin(2 * np.pi * (t * 3.0 + np.arctan2(y_coords - cy, x_coords - cx) * 2.0))
        vort_glow = (np.maximum(0, vortex) ** 3.0) * np.exp(-((np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2) - 4.5) / 1.5)**2) * (t_base > 0.35)
        
        total_kin = slip_glow * 1.2 + vort_glow * 0.9
        
        r += total_kin * 155.0
        g += total_kin * 125.0
        b += total_kin * 45.0
        
        flash = np.clip(total_kin - 0.75, 0, 1.2) * 115.0
        r += flash * 0.98
        g += flash * 0.95
        b += flash * 0.85
        
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
    print("Gerando candidatos para Advanced Nitinol (⚷⚙⚷ Ni4Ti6)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Martensite Twin Lattice", render_option_1),
        (2, "Hysteresis Shape Memory", render_option_2),
        (3, "Superelastic Slipstream", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"nitinol_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (advanced_nitinol_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (24, 18, 12, 255)) # Dark titanium-tan/bronze
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "ADVANCED NITINOL — VISUAL CANDIDATES (128x128)", fill=(245, 158, 11, 255), font=font_title)
    draw.text((pad_x, 38), "Shape Memory Superalloy • Ni4Ti6 • Titanium-Tan & Gold-Bronze • 30 Frames", fill=(217, 119, 6, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Martensite",
        "OPÇÃO 2: Hysteresis",
        "OPÇÃO 3: Slipstream"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(254, 243, 199, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(217, 119, 6, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][12]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez bronze sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (38, 28, 18) if (bx // 16 + by // 16) % 2 == 0 else (28, 20, 12)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(245, 158, 11, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "advanced_nitinol_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Advanced Nitinol — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0f0a05;
      color: #fef3c7;
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
      background: linear-gradient(135deg, #3d2309 0%, #241405 60%, #0f0a05 100%);
      border: 1px solid rgba(245, 158, 11, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(245, 158, 11, 0.18);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fde68a;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #fbbf24, #d97706);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #d1d5db;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #1c1004;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #3d2508;
    }}
    .btn-toggle {{
      background: #d97706;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(217, 119, 6, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #f59e0b;
    }}
    
    .shape-bar {{
      background: #1a1006;
      border: 1px solid #38200a;
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
      background: #0f0803;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #38200a;
    }}
    .btn-shape {{
      background: transparent;
      color: #d1d5db;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #d97706;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.5);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #38200a;
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
      background: #191007;
      border: 2px solid #38220c;
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
      border-color: rgba(245, 158, 11, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #fbbf24;
      box-shadow: 0 0 20px rgba(245, 158, 11, 0.25);
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
      background: rgba(245, 158, 11, 0.18);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #fef3c7;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #d1d5db;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #0d0703;
      border: 1px solid #2e1a07;
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
    
    @keyframes nitinolGlowPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.8)) drop-shadow(0 0 18px rgba(217, 119, 6, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 14px rgba(251, 191, 36, 1.0)) drop-shadow(0 0 28px rgba(254, 243, 199, 0.7));
        transform: scale(1.02);
      }}
    }}
    .glow-effect {{
      animation: nitinolGlowPulse 2.5s ease-in-out infinite;
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
      background: #2a1707;
      color: #fde68a;
    }}
    .btn-approve:hover {{
      background: #d97706;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(217, 119, 6, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #f59e0b, #d97706);
      color: #1a0e03;
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
      background: #261506;
      color: #fde68a;
      border: 1px solid #452408;
    }}
    
    .footer-box {{
      background: #1a1006;
      border: 1px solid #38200a;
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: #d1d5db;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <div>
          <span class="badge">GTNA Shape-Memory Superalloy</span>
          <span class="formula-tag">⚷⚙⚷ Ni4Ti6 • #D2B48C</span>
        </div>
        <h1>Advanced Nitinol — 3 Opções de Animação</h1>
        <p class="subtitle">
          Superliga com memória de forma termo-elástica de 30 frames combinada com o <strong>Titanium-Amber Glow Edge Shader</strong> (<code style="color:#fbbf24">gtna:glow_edge</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#d1d5db;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#fbbf24;">GLOW ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleGlow" onclick="toggleShader()">Alternar Shader</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#d1d5db; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-plate" onclick="setShape('plate')">Placa (Plate)</button>
          <button class="btn-shape" id="btn-gear" onclick="setShape('gear')">Engrenagem (Gear)</button>
          <button class="btn-shape" id="btn-block" onclick="setShape('block')">Bloco (Block)</button>
        </div>
      </div>
      <div style="font-size:11px; color:#d1d5db;">
        Tamanho: <strong>128×128px (8× Zoom Pixel Art Nítido)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#d1d5db;">Martensite Twins</span>
          </div>
          <div class="card-title">Thermo-Elastic Martensite Twin Lattice</div>
          <p class="card-desc">
            Transição cristalográfica de fase: <strong>linhas de geminação em ângulos de cisalhamento alternados (45° / -45°)</strong> que se realinham como uma sanfona atômica microscópica com flashes termo-mecânicos dourados.
          </p>
          <div class="features-list">
            <span class="feature-item">Geminação Martensítica 45°</span>
            <span class="feature-item">Ciclo Térmico de Fase</span>
            <span class="feature-item">Flashes de Alívio de Tensão</span>
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
            <span style="font-size:11px; color:#d1d5db;">Hysteresis Pulse</span>
          </div>
          <div class="card-title">Shape-Memory Hysteresis Pulse</div>
          <p class="card-desc">
            Ciclo completo de memória de forma: <strong>compressão térmica lenta acumulando energia de histerese</strong>, seguida por um disparo superelástico ultrarrápido restaurando a malha original com um anel de choque dourado.
          </p>
          <div class="features-list">
            <span class="feature-item">Curva de Histerese Térmica</span>
            <span class="feature-item">Disparo Superelástico 30%</span>
            <span class="feature-item">Anel de Choque Expansivo</span>
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
            <span style="font-size:11px; color:#d1d5db;">Kinetic Slipstream</span>
          </div>
          <div class="card-title">Superelastic Kinetic Slipstream</div>
          <p class="card-desc">
            Superelasticidade contínua sob alto estresse: <strong>feixes lineares de absorção de impacto</strong> que deslizam longitudinalmente pela peça, dissipando calor através de micro-vórtices de titânio aquecido e ouro metálico.
          </p>
          <div class="features-list">
            <span class="feature-item">Escoamento Sem Deformação</span>
            <span class="feature-item">Vórtices de Dissipação</span>
            <span class="feature-item">Bronze Polido Cintilante</span>
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
        Status: <strong style="color:#fbbf24;">Aguardando aprovação do autor</strong>
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
        statusText.style.color = '#fbbf24';
        btn.innerText = 'Desativar Glow';
        btn.style.background = '#d97706';
      }} else {{
        statusText.innerText = 'SHADER DESLIGADO';
        statusText.style.color = '#78716c';
        btn.innerText = 'Ativar Glow';
        btn.style.background = '#38200a';
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
    html_path = ARTIFACT_DIR / "advanced_nitinol_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
