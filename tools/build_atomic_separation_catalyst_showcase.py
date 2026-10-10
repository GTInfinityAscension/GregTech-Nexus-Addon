#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Atomic Separation Catalyst
Cor: #E85E0C (Laranja Termonuclear Incandescente)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/atomic_separation_catalyst_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (232, 94, 12, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (232, 94, 12, 255))

# =========================================================================
# Opção 1: Strong-Force Fission Cascade (Cascata de Fissão & Força Forte)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # 4 núcleos atômicos em coordenadas assimétricas
    nuclei = [(4.5, 5.0), (11.5, 4.5), (6.0, 11.0), (12.0, 11.5)]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Âmbar vulcânico profundo e cobre de fissão (#E85E0C)
        r = 52.0 + t_base * 192.0
        g = 18.0 + (t_base ** 1.3) * 115.0
        b = 4.0 + (t_base ** 1.8) * 35.0
        
        # Trajetórias de partículas ejetadas por quebra do potencial de Yukawa
        fission_rays = 0.0
        for idx, (nx, ny) in enumerate(nuclei):
            dist_n = np.sqrt((x_coords - nx)**2 + (y_coords - ny)**2)
            angle_n = np.arctan2(y_coords - ny, x_coords - nx)
            
            # Ejeção de píons e nêutrons em espirais balísticas de alta velocidade
            ray = np.sin(4.0 * angle_n + dist_n * 1.8 - tau * 3.0 + idx * 1.57)
            core = np.exp(-((dist_n / 1.5)**2)) * (1.2 + 0.8 * np.sin(tau * 2.0 + idx))
            
            fission_rays += np.clip(ray, 0, 1.0) * np.exp(-dist_n / 4.0) * 0.9 + core * 1.2
            
        total_fission = fission_rays * (t_base > 0.22)
        
        # Calor radiante laranja termonuclear e amarelo de plasma
        r += total_fission * 75.0
        g += total_fission * 55.0
        b += total_fission * 10.0
        
        # Picos de fissão branco-solar nos núcleos
        fission_flash = np.clip(total_fission - 1.2, 0, 1.5) * 110.0
        r += fission_flash * 1.00
        g += fission_flash * 0.96
        b += fission_flash * 0.80
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Quark-Gluon Plasma Deconfinement (Plasma de Quarks e Glúons)
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    dx = x_coords - cx
    dy = y_coords - cy
    r_dist = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Fogo atômico de plasma de quarks
        r = 50.0 + t_base * 195.0
        g = 16.0 + (t_base ** 1.35) * 118.0
        b = 3.0 + (t_base ** 1.9) * 32.0
        
        # Vórtice elíptico relativístico SU(3) de viscosidade nula
        # 3 fluxos de carga de cor que giram em contra-fase no QGP
        flow1 = np.sin(3.0 * theta + r_dist * 0.9 - tau * 2.0)
        flow2 = np.cos(3.0 * theta - r_dist * 1.1 + tau * 2.0)
        gluon_vortex = np.exp(-((flow1 * flow2 - 0.3) / 0.35)**2) * (t_base > 0.25)
        
        # Núcleo de desconfinamento assintótico
        qgp_core = np.exp(-((r_dist / 2.8)**2)) * (1.0 + 0.6 * np.cos(tau * 3.0)) * (t_base > 0.3)
        
        total_qgp = (gluon_vortex * 1.1 + qgp_core * 1.3) * (t_base > 0.22)
        
        # Brilho de fogo cromodinâmico laranja-ouro
        r += total_qgp * 78.0
        g += total_qgp * 60.0
        b += total_qgp * 15.0
        
        # Flashes brancos de liberdade assintótica
        flash = np.clip(total_qgp - 1.1, 0, 1.4) * 105.0
        r += flash * 1.00
        g += flash * 0.98
        b += flash * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Spallation Neutron Interference Wavefronts (Espalação Nuclear)
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
        tau = 2 * np.pi * t
        
        # Paleta Base: Âmbar radioativo de espalação
        r = 48.0 + t_base * 194.0
        g = 15.0 + (t_base ** 1.3) * 116.0
        b = 5.0 + (t_base ** 1.8) * 36.0
        
        # Frentes de onda de Bragg-Laue de difração de nêutrons de espalação
        # Duas frentes elípticas de impacto colidindo a 60 graus
        w1 = np.sin((x_coords * 0.8 + y_coords * 1.2) - tau * 2.5)
        w2 = np.cos((x_coords * 1.2 - y_coords * 0.8) + tau * 2.5)
        
        interference = np.exp(-((w1 * w2 - 0.45) / 0.28)**2) * (t_base > 0.25)
        
        # Foco de impacto de espalação que varre ciclicamente
        sweep_x = 2.0 + t * 12.0
        sweep_y = 2.0 + (1.0 - t) * 12.0
        impact_pulse = np.exp(-(((x_coords - sweep_x)**2 + (y_coords - sweep_y)**2) / 4.0)) * 1.6 * (t_base > 0.28)
        
        total_spallation = (interference * 1.0 + impact_pulse * 1.2)
        
        # Emissão luminosa de quebra nuclear
        r += total_spallation * 76.0
        g += total_spallation * 58.0
        b += total_spallation * 12.0
        
        # Picos brancos incandescentes
        flash = np.clip(total_spallation - 1.0, 0, 1.4) * 105.0
        r += flash * 1.00
        g += flash * 0.97
        b += flash * 0.88
        
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
    print("Gerando candidatos para Atomic Separation Catalyst (#E85E0C)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Strong-Force Fission", render_option_1),
        (2, "Quark-Gluon Plasma", render_option_2),
        (3, "Spallation Wavefronts", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"asc_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (atomic_separation_catalyst_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo cobre-âmbar escuro vulcânico
    grid_img = Image.new("RGBA", (grid_w, grid_h), (24, 12, 6, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "ATOMIC SEPARATION CATALYST — CANDIDATES (128x128)", fill=(251, 146, 60, 255), font=font_title)
    draw.text((pad_x, 38), "High-Energy Nuclear Dissociation Catalyst • #E85E0C • Thermonuclear Flare • 30 Frames", fill=(254, 215, 170, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Fission Cascade",
        "OPÇÃO 2: Quark-Gluon Plasma",
        "OPÇÃO 3: Spallation Waves"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(255, 237, 213, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(251, 146, 60, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (38, 20, 10) if (bx // 16 + by // 16) % 2 == 0 else (28, 14, 6)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(251, 146, 60, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "atomic_separation_catalyst_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Atomic Separation Catalyst — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0e0602;
      color: #fff7ed;
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
      background: linear-gradient(135deg, #381504 0%, #1e0901 60%, #0e0602 100%);
      border: 1px solid rgba(232, 94, 12, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(232, 94, 12, 0.3), 0 0 20px rgba(232, 94, 12, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(232, 94, 12, 0.22);
      color: #fb923c;
      border: 1px solid rgba(232, 94, 12, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fed7aa;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #fb923c, #ea580c);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #cbd5e1;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #1c0a02;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #451a05;
    }}
    .btn-toggle {{
      background: #ea580c;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(234, 88, 12, 0.45);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #f97316;
    }}
    .btn-toggle.active {{
      background: #f97316;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(249, 115, 22, 0.75);
    }}
    
    .shape-bar {{
      background: #1a0902;
      border: 1px solid #3c1605;
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
      background: #0d0401;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #3c1605;
    }}
    .btn-shape {{
      background: transparent;
      color: #cbd5e1;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #ea580c;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(234, 88, 12, 0.5);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #3c1605;
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
      background: #170802;
      border: 2px solid #361405;
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
      border-color: rgba(249, 115, 22, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f97316;
      box-shadow: 0 0 24px rgba(249, 115, 22, 0.4);
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
      background: rgba(232, 94, 12, 0.2);
      color: #fb923c;
      border: 1px solid rgba(232, 94, 12, 0.4);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #cbd5e1;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #0a0301;
      border: 1px solid #2a0e03;
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
      transition: transform 0.2s ease, filter 0.3s ease;
    }}
    
    /* SHADER INOVADOR: Thermonuclear Ionization Flare Corona */
    @keyframes ascHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(234, 88, 12, 0.95)) 
          drop-shadow(0 0 20px rgba(249, 115, 22, 0.6)) 
          drop-shadow(0 0 32px rgba(245, 158, 11, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(251, 146, 60, 0.9)) 
          drop-shadow(0 0 44px rgba(234, 88, 12, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-active {{
      animation: ascHaloPulse 2.1s ease-in-out infinite;
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
      background: #2a1004;
      color: #fed7aa;
    }}
    .btn-approve:hover {{
      background: #ea580c;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(234, 88, 12, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #fb923c, #ea580c);
      color: #1a0601;
      font-weight: 800;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
    }}
    .feature-item {{
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 4px;
      background: #260d03;
      color: #fed7aa;
      border: 1px solid #431605;
    }}
    
    .footer-box {{
      background: #1a0902;
      border: 1px solid #3c1605;
      border-radius: 12px;
      padding: 16px 22px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <div>
          <span class="badge">Catalisador de Fissão Atômica</span>
          <span class="formula-tag">#E85E0C • Desconfinamento Nuclear</span>
        </div>
        <h1>Atomic Separation Catalyst — 3 Físicas Nucleares & Shaders</h1>
        <p class="subtitle">
          Catalisador termonuclear que quebra as forças nucleares fortes e fracas. 3 dinâmicas subatômicas combinadas com a <strong>Thermonuclear Flare Corona</strong>.
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#cbd5e1;">Simulador In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#fb923c;">✨ FLARE CORONA ATIVADO</div>
        </div>
        <button class="btn-toggle active" id="btnToggleHalo" onclick="toggleShader()">Alternar Shader</button>
      </div>
    </div>

    <div class="shape-bar">
      <div style="display:flex; align-items:center; gap:12px;">
        <span style="font-size:12px; font-weight:700; color:#cbd5e1; text-transform:uppercase;">Forma:</span>
        <div class="shape-buttons">
          <button class="btn-shape active" id="btn-ingot" onclick="setShape('ingot')">Barra (Ingot)</button>
          <button class="btn-shape" id="btn-plate" onclick="setShape('plate')">Placa (Plate)</button>
          <button class="btn-shape" id="btn-gear" onclick="setShape('gear')">Engrenagem (Gear)</button>
          <button class="btn-shape" id="btn-block" onclick="setShape('block')">Bloco (Block)</button>
        </div>
      </div>
      <div style="font-size:11px; color:#94a3b8;">
        Visualização: <strong>128×128px (Pixel Art Fiel 8× Zoom)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#94a3b8;">Cascata de Yukawa</span>
          </div>
          <div class="card-title">Strong-Force Fission Cascade</div>
          <p class="card-desc">
            Dissociação do potencial de Yukawa da <strong>Força Forte Nuclear</strong>: 4 núcleos atômicos entram em quebra espontânea e expelem píons e nêutrons em trajetórias espirais balísticas de alta energia, com flashes de colapso nos nós nucleares.
          </p>
          <div class="features-list">
            <span class="feature-item">Potencial de Yukawa</span>
            <span class="feature-item">Ejeção de Píons & Nêutrons</span>
            <span class="feature-item">Reação em Cadeia Térmica</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-1" class="halo-active">
            <img id="img-1" class="pixelated-art" src="{b64_data[1]['ingot']}" alt="Opção 1">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(1)">Aprovar Opção 1 (Responder 1)</button>
      </div>

      <!-- Option 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 2</span>
            <span style="font-size:11px; color:#94a3b8;">Plasma de Quarks</span>
          </div>
          <div class="card-title">Quark-Gluon Plasma Deconfinement</div>
          <p class="card-desc">
            Desconfinamento assintótico $SU(3)$ em <strong>Plasma de Quarks-Glúons (QGP)</strong> de viscosidade nula: 3 correntes cromodinâmicas de carga de cor formam vórtices relativísticos entrelaçados de fogo laranja e ouro solar ao redor do núcleo.
          </p>
          <div class="features-list">
            <span class="feature-item">Desconfinamento SU(3)</span>
            <span class="feature-item">Hidrodinâmica Relativística</span>
            <span class="feature-item">Fogo Cromodinâmico</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-2" class="halo-active">
            <img id="img-2" class="pixelated-art" src="{b64_data[2]['ingot']}" alt="Opção 2">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(2)">Aprovar Opção 2 (Responder 2)</button>
      </div>

      <!-- Option 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 3</span>
            <span style="font-size:11px; color:#94a3b8;">Espalação Nuclear</span>
          </div>
          <div class="card-title">Spallation Neutron Interference Waves</div>
          <p class="card-desc">
            Feixes pulsados colidem com o núcleo gerando uma <strong>cascata de espalação nuclear</strong>. Nêutrons ultra-densos se difratam através da malha cristalina em padrões elípticos de interferência de Bragg-Laue com frentes de choque incandescentes.
          </p>
          <div class="features-list">
            <span class="feature-item">Espalação por Prótons</span>
            <span class="feature-item">Difração de Bragg-Laue</span>
            <span class="feature-item">Frentes de Choque Elípticas</span>
          </div>
        </div>

        <div class="image-box">
          <div id="wrapper-3" class="halo-active">
            <img id="img-3" class="pixelated-art" src="{b64_data[3]['ingot']}" alt="Opção 3">
          </div>
        </div>

        <button class="btn-approve" onclick="selectCard(3)">Aprovar Opção 3 (Responder 3)</button>
      </div>

    </div>

    <div class="footer-box">
      <div>
        Qual das 3 opções você prefere aprovar para o <strong>Atomic Separation Catalyst</strong>?
      </div>
      <div style="font-weight:700; color:#fb923c;">
        Basta responder 1, 2 ou 3 no chat!
      </div>
    </div>

  </div>

  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    let haloEnabled = true;

    function updateArt() {{
      for (let opt = 1; opt <= 3; opt++) {{
        const img = document.getElementById('img-' + opt);
        if (img && data[opt] && data[opt][currentShape]) {{
          img.src = data[opt][currentShape];
        }}
      }}
    }}

    function setShape(shape) {{
      currentShape = shape;
      ['ingot', 'plate', 'gear', 'block'].forEach(s => {{
        const btn = document.getElementById('btn-' + s);
        if (btn) {{
          if (s === shape) {{
            btn.classList.add('active');
          }} else {{
            btn.classList.remove('active');
          }}
        }}
      }});
      updateArt();
    }}

    function toggleShader() {{
      haloEnabled = !haloEnabled;
      const statusText = document.getElementById('shaderStatusText');
      const toggleBtn = document.getElementById('btnToggleHalo');

      for (let opt = 1; opt <= 3; opt++) {{
        const wrap = document.getElementById('wrapper-' + opt);
        if (wrap) {{
          if (haloEnabled) {{
            wrap.classList.add('halo-active');
          }} else {{
            wrap.classList.remove('halo-active');
          }}
        }}
      }}

      if (haloEnabled) {{
        statusText.innerText = "✨ FLARE CORONA ATIVADO";
        statusText.style.color = "#fb923c";
        toggleBtn.classList.add('active');
      }} else {{
        statusText.innerText = "OFF (DESATIVADO)";
        statusText.style.color = "#94a3b8";
        toggleBtn.classList.remove('active');
      }}
    }}

    function selectCard(opt) {{
      for (let i = 1; i <= 3; i++) {{
        const card = document.getElementById('card-' + i);
        if (card) {{
          if (i === opt) {{
            card.classList.add('selected');
          }} else {{
            card.classList.remove('selected');
          }}
        }}
      }}
    }}
  </script>
</body>
</html>
"""
    html_path = ARTIFACT_DIR / "atomic_separation_catalyst_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase interativo salvo em: {html_path}")
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
