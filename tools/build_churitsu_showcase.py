import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/churitsu_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (130, 130, 130, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (130, 130, 130, 255))

# =========================================================================
# Opção 1: Neutral Dipole Yin-Yang Precession (Precessão de Dipolo Yin-Yang)
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
    angle = np.arctan2(y_coords - cy, x_coords - cx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Grafite monocromático metálico neutro (#828282)
        base_gray = 32.0 + t_base * 145.0
        r = base_gray.copy()
        g = base_gray.copy()
        b = base_gray.copy()
        
        # Dipolo rotativo Yin-Yang no plano da peça
        rot_angle = angle - 2 * np.pi * t
        dipole_wave = np.sin(rot_angle) * np.exp(-((dist - 4.5) / 2.5)**2)
        
        # Lóbulo positivo (platina brilhante) e lóbulo negativo (grafite denso)
        pos_lobe = np.maximum(0, dipole_wave) * (t_base > 0.28)
        neg_lobe = np.maximum(0, -dipole_wave) * (t_base > 0.28)
        
        # Ponto de aniquilação/equilíbrio central
        neutral_core = np.exp(-((dist / 2.2)**2)) * (0.5 + 0.5 * np.cos(4 * np.pi * t)) * (t_base > 0.35)
        
        total_fx = (pos_lobe * 1.5 - neg_lobe * 0.45 + neutral_core * 1.2)
        
        # Brilho neutro monocromático
        boost = total_fx * 95.0
        r += boost
        g += boost
        b += boost
        
        # Picos de equilíbrio supercrítico branco
        flash = np.clip(pos_lobe * 1.5 + neutral_core - 0.7, 0, 1.2) * 115.0
        r += flash
        g += flash
        b += flash
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Baryon-Lepton Symmetry Wave (Ondas Estacionárias de Simetria)
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
        
        base_gray = 30.0 + t_base * 148.0
        r = base_gray.copy()
        g = base_gray.copy()
        b = base_gray.copy()
        
        # Interferência de ondas esféricas contrárias -> Onda Estacionária Pura
        standing_wave = np.sin(2 * np.pi * (dist / 3.8)) * np.cos(2 * np.pi * (t * 2.0))
        standing_pattern = (np.abs(standing_wave) ** 1.8) * (t_base > 0.25)
        
        # Anel de contenção de simetria estável
        nodal_ring = np.exp(-((dist - 5.0) / 1.0)**2) * 0.7 * (t_base > 0.3)
        
        total_sym = (standing_pattern * 1.3 + nodal_ring * 0.8)
        
        boost = total_sym * 90.0
        r += boost
        g += boost
        b += boost
        
        crest = np.clip(total_sym - 0.7, 0, 1.2) * 120.0
        r += crest
        g += crest
        b += crest
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Charge Neutralization Sweep Grid (Grade de Neutralização de Carga)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        base_gray = 28.0 + t_base * 150.0
        r = base_gray.copy()
        g = base_gray.copy()
        b = base_gray.copy()
        
        # Duas frentes ortogonais de varredura de neutralização
        sweep_x = (x_coords - t * 18.0) % 12.0
        sweep_y = (y_coords + t * 18.0) % 12.0
        
        beam_x = np.exp(-((sweep_x - 6.0) / 1.3)**2)
        beam_y = np.exp(-((sweep_y - 6.0) / 1.3)**2)
        
        # Cruzamento de varredura
        nodes = beam_x * beam_y * 2.5
        total_sweep = (beam_x * 0.7 + beam_y * 0.7 + nodes) * (t_base > 0.28)
        
        boost = total_sweep * 105.0
        r += boost
        g += boost
        b += boost
        
        node_flash = np.clip(nodes - 0.6, 0, 1.2) * 125.0
        r += node_flash
        g += node_flash
        b += node_flash
        
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
    print("Gerando candidatos para Churitsu (中立)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Neutral Dipole Yin-Yang", render_option_1),
        (2, "Baryon-Lepton Symmetry", render_option_2),
        (3, "Neutralization Sweep Grid", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"churitsu_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (churitsu_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 40
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 18, 18, 255)) # Sleek dark graphite
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "CHURITSU — VISUAL CANDIDATES (128x128)", fill=(229, 231, 235, 255), font=font_title)
    draw.text((pad_x, 38), "Absolute Neutral Equilibrium • Graphite & Platinum Monochrome • 30 Frames", fill=(156, 163, 175, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Dipole Yin-Yang",
        "OPÇÃO 2: Symmetry Wave",
        "OPÇÃO 3: Neutralizer Grid"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(209, 213, 219, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(156, 163, 175, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][12]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez neutro para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (28, 28, 28) if (bx // 16 + by // 16) % 2 == 0 else (22, 22, 22)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(156, 163, 175, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "churitsu_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Churitsu (中立) — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b0b0b;
      color: #e5e7eb;
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
      background: linear-gradient(135deg, #262626 0%, #171717 60%, #0b0b0b 100%);
      border: 1px solid rgba(209, 213, 219, 0.35);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(255, 255, 255, 0.08);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(229, 231, 235, 0.15);
      color: #f3f4f6;
      border: 1px solid rgba(229, 231, 235, 0.35);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #d1d5db;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #e5e7eb, #9ca3af);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #9ca3af;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #1f1f1f;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #333333;
    }}
    .btn-toggle {{
      background: #4b5563;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #6b7280;
    }}
    
    .shape-bar {{
      background: #171717;
      border: 1px solid #2e2e2e;
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
      background: #0d0d0d;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #2e2e2e;
    }}
    .btn-shape {{
      background: transparent;
      color: #9ca3af;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #4b5563;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #2e2e2e;
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
      background: #171717;
      border: 2px solid #2e2e2e;
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
      border-color: rgba(229, 231, 235, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f3f4f6;
      box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
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
      background: rgba(229, 231, 235, 0.15);
      color: #f3f4f6;
      border: 1px solid rgba(229, 231, 235, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #f9fafb;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #9ca3af;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #0d0d0d;
      border: 1px solid #262626;
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
    
    @keyframes neutralGlowPulse {{
      0%, 100% {{
        filter: drop-shadow(0 0 6px rgba(229, 231, 235, 0.75)) drop-shadow(0 0 18px rgba(156, 163, 175, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: drop-shadow(0 0 14px rgba(255, 255, 255, 0.95)) drop-shadow(0 0 28px rgba(209, 213, 219, 0.65));
        transform: scale(1.02);
      }}
    }}
    .glow-effect {{
      animation: neutralGlowPulse 2.5s ease-in-out infinite;
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
      background: #262626;
      color: #e5e7eb;
    }}
    .btn-approve:hover {{
      background: #4b5563;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(255, 255, 255, 0.2);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #e5e7eb, #9ca3af);
      color: #111827;
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
      background: #242424;
      color: #e5e7eb;
      border: 1px solid #383838;
    }}
    
    .footer-box {{
      background: #171717;
      border: 1px solid #2e2e2e;
      border-radius: 12px;
      padding: 14px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 12px;
      color: #9ca3af;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <div>
          <span class="badge">GTNA Legendary Material</span>
          <span class="formula-tag">Churitsu (中立) • #828282</span>
        </div>
        <h1>Churitsu — 3 Opções de Animação</h1>
        <p class="subtitle">
          Texturas monocromáticas fluidas de 30 frames combinadas com o <strong>Platinum Neutral Glow Edge Shader</strong> (<code style="color:#e5e7eb">renderblender:glow_edge</code>).
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#9ca3af;">Shader In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#f3f4f6;">GLOW ATIVADO</div>
        </div>
        <button class="btn-toggle" id="btnToggleGlow" onclick="toggleShader()">Alternar Shader</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#9ca3af; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-plate" onclick="setShape('plate')">Placa (Plate)</button>
          <button class="btn-shape" id="btn-gear" onclick="setShape('gear')">Engrenagem (Gear)</button>
          <button class="btn-shape" id="btn-block" onclick="setShape('block')">Bloco (Block)</button>
        </div>
      </div>
      <div style="font-size:11px; color:#6b7280;">
        Tamanho: <strong>128×128px (8× Zoom Pixel Art Nítido)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#9ca3af;">Dipole Orbit</span>
          </div>
          <div class="card-title">Neutral Dipole Yin-Yang Precession</div>
          <p class="card-desc">
            Equilíbrio perfeito de cargas opostas: <strong>dois lóbulos rotativos em contra-órbita contínua</strong> (grafite denso vs platina líquida) que trocam cargas continuamente por um ponto central sem atrito.
          </p>
          <div class="features-list">
            <span class="feature-item">Lóbulos Yin-Yang</span>
            <span class="feature-item">Linha Equipotencial V=0</span>
            <span class="feature-item">Centro de Aniquilação Neutra</span>
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
            <span style="font-size:11px; color:#9ca3af;">Symmetry Wave</span>
          </div>
          <div class="card-title">Baryon-Lepton Symmetry Wave</div>
          <p class="card-desc">
            Conservação quântica estrita: <strong>interferência de duas ondas esféricas contrárias</strong> colidindo no centro e gerando anéis nodais perfeitamente concêntricos que respiram em harmonia monocromática.
          </p>
          <div class="features-list">
            <span class="feature-item">Onda Estacionária Pura</span>
            <span class="feature-item">Anéis Nodais Concêntricos</span>
            <span class="feature-item">Respiração de Simetria</span>
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
            <span style="font-size:11px; color:#9ca3af;">Neutralizer Grid</span>
          </div>
          <div class="card-title">Charge Neutralization Sweep Grid</div>
          <p class="card-desc">
            Matriz estática de equalização atômica: <strong>frentes planas ortogonais de potencial zero</strong> em alta velocidade varrendo a rede cristalina com flashes de descarga nos cruzamentos de drenagem.
          </p>
          <div class="features-list">
            <span class="feature-item">Varredura Cruzada X/Y</span>
            <span class="feature-item">Drenagem Instantânea</span>
            <span class="feature-item">Acabamento Tungstênio Polido</span>
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
        Status: <strong style="color:#e5e7eb;">Aguardando aprovação do autor</strong>
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
        statusText.style.color = '#f3f4f6';
        btn.innerText = 'Desativar Glow';
        btn.style.background = '#4b5563';
      }} else {{
        statusText.innerText = 'SHADER DESLIGADO';
        statusText.style.color = '#6b7280';
        btn.innerText = 'Ativar Glow';
        btn.style.background = '#262626';
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
    html_path = ARTIFACT_DIR / "churitsu_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
