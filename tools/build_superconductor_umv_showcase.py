#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Superconductor Base UMV
Tier: UMV (UXV GTCEu) • Cor: #B526CD (Violeta Multiversal Quântico)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/superconductor_umv_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (181, 38, 205, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (181, 38, 205, 255))

# =========================================================================
# Opção 1: Calabi-Yau Manifold Wormhole Tunneling (Micro-Buracos de Minhoca)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
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
        
        # Paleta Base: Púrpura/Violeta abissal multiversal (#B526CD)
        r = 38.0 + t_base * 145.0
        g = 8.0 + (t_base ** 1.35) * 32.0
        b = 48.0 + (t_base ** 1.05) * 162.0
        
        # Projeção 2D de micro-variedade de Calabi-Yau com 5 lóbulos dimensionais
        # Canais de tunelamento espaciais onde supercorrentes dobram o vácuo
        manifold = np.sin(5.0 * theta + tau) * np.cos(r_dist * 1.2 - tau * 0.7)
        wormhole_throat = np.exp(-((r_dist - (2.5 + 2.0 * np.sin(tau)))**2) / 1.2)
        
        tunnel_flux = np.abs(manifold) * (t_base > 0.25) * 1.3 + wormhole_throat * 1.5 * (t_base > 0.22)
        
        # Supercorrentes multiversais em trânsito instantâneo
        tunnel_flash = np.clip(tunnel_flux - 0.75, 0, 1.4) * (t_base > 0.3)
        
        total_fx = tunnel_flux * 0.85 + tunnel_flash * 1.1
        
        # Brilho violeta-choque neon e magenta dimensional
        r += total_fx * 78.0
        g += total_fx * 24.0
        b += total_fx * 92.0
        
        # Flashes singulares de tunelamento multiversal branco-estrela
        flash = np.clip(tunnel_flash - 0.4, 0, 1.5) * 105.0
        r += flash * 0.98
        g += flash * 0.92
        b += flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Non-Abelian Anyon Braid Currents (Tranças de Anyons de Majorana)
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Ameixa cósmica e violeta profundo
        r = 36.0 + t_base * 148.0
        g = 6.0 + (t_base ** 1.4) * 34.0
        b = 46.0 + (t_base ** 1.05) * 164.0
        
        # Teoria de Tranças Quânticas (Braiding de 3 anyons de Majorana)
        # Trajetórias senoidais entrelaçadas não-comutativas
        strand1 = np.exp(-((y_coords - (7.5 + 4.5 * np.sin(x_coords * 0.6 + tau))) / 1.0)**2)
        strand2 = np.exp(-((y_coords - (7.5 + 4.5 * np.sin(x_coords * 0.6 + tau + 2.094))) / 1.0)**2)
        strand3 = np.exp(-((y_coords - (7.5 + 4.5 * np.sin(x_coords * 0.6 + tau + 4.188))) / 1.0)**2)
        
        # Nós topológicos onde as tranças anyônicas se cruzam
        braid_crossings = (strand1 * strand2 + strand2 * strand3 + strand3 * strand1) * 2.8 * (t_base > 0.3)
        braids = (strand1 + strand2 + strand3) * 0.7 * (t_base > 0.22)
        
        total_braid = braids + braid_crossings
        
        # Emissão de coerência topológica violeta e rosa neon
        r += total_braid * 75.0
        g += total_braid * 20.0
        b += total_braid * 88.0
        
        # Flashes nos pontos protegidos de entrelaçamento quântico
        braid_flash = np.clip(braid_crossings - 0.7, 0, 1.5) * 95.0
        r += braid_flash * 0.99
        g += braid_flash * 0.93
        b += braid_flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Spacetime Metric Dynamic Casimir Superfluid (Superfluidez Métrica)
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
        
        # Paleta Base: Violeta multiversal com sombras índigo escuro
        r = 35.0 + t_base * 149.0
        g = 7.0 + (t_base ** 1.35) * 33.0
        b = 49.0 + (t_base ** 1.05) * 163.0
        
        # Efeito Casimir Dinâmico: ondas métricas hiperbólicas de alta frequência no tensor g_uv
        # Frentes de choque de modulação do vácuo quântico
        metric_wave1 = np.sin((x_coords * 1.1 + y_coords * 0.9) - tau * 2.0)
        metric_wave2 = np.cos((x_coords * 0.9 - y_coords * 1.1) + tau * 2.0)
        
        casimir_fringe = np.exp(-((metric_wave1 * metric_wave2 - 0.4) / 0.3)**2) * (t_base > 0.25)
        
        # Pulsos de superfluidez métrica do vácuo
        vacuum_swell = (np.sin(tau) * 0.5 + 0.5) * np.sin(x_coords * 0.5 + y_coords * 0.5)
        swell_glow = np.clip(vacuum_swell, 0, 1.0) * 0.7 * (t_base > 0.28)
        
        total_casimir = (casimir_fringe * 1.2 + swell_glow * 0.9)
        
        # Brilho eletrodinâmico violeta profundo e ametista pulsante
        r += total_casimir * 80.0
        g += total_casimir * 22.0
        b += total_casimir * 94.0
        
        # Picos de fótons virtuais convertidos em luz real
        photon_flash = np.clip(total_casimir - 0.75, 0, 1.4) * 98.0
        r += photon_flash * 0.98
        g += photon_flash * 0.94
        b += photon_flash * 1.00
        
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
    print("Gerando candidatos para Superconductor Base UMV (#B526CD)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Calabi-Yau Wormhole", render_option_1),
        (2, "Anyon Braid Currents", render_option_2),
        (3, "Casimir Superfluidity", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"sc_umv_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (superconductor_umv_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo violeta escuro multiversal
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 8, 24, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "SUPERCONDUCTOR BASE UMV — VISUAL CANDIDATES (128x128)", fill=(217, 70, 239, 255), font=font_title)
    draw.text((pad_x, 38), "Topological Multiverse Superconductor • Tier UMV • #B526CD • 30 Frames", fill=(192, 132, 252, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Calabi-Yau",
        "OPÇÃO 2: Anyon Braid",
        "OPÇÃO 3: Casimir Fluid"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(250, 232, 255, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(217, 70, 239, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (28, 14, 38) if (bx // 16 + by // 16) % 2 == 0 else (20, 10, 28)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(217, 70, 239, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "superconductor_umv_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Superconductor Base UMV — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b040e;
      color: #faf5ff;
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
      background: linear-gradient(135deg, #2a0833 0%, #16041c 60%, #0b040e 100%);
      border: 1px solid rgba(181, 38, 205, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(181, 38, 205, 0.3), 0 0 20px rgba(181, 38, 205, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(181, 38, 205, 0.22);
      color: #e879f9;
      border: 1px solid rgba(181, 38, 205, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #f0abfc;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #e879f9, #b526cd);
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
      background: #17051f;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #3d0d4f;
    }}
    .btn-toggle {{
      background: #b526cd;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(181, 38, 205, 0.45);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #d946ef;
    }}
    .btn-toggle.active {{
      background: #c026d3;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(217, 70, 239, 0.75);
    }}
    
    .shape-bar {{
      background: #15051c;
      border: 1px solid #330b42;
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
      background: #0a020d;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #330b42;
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
      background: #b526cd;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(181, 38, 205, 0.5);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #330b42;
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
      background: #14041b;
      border: 2px solid #300a40;
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
      border-color: rgba(181, 38, 205, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #d946ef;
      box-shadow: 0 0 24px rgba(181, 38, 205, 0.4);
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
      background: rgba(181, 38, 205, 0.2);
      color: #e879f9;
      border: 1px solid rgba(181, 38, 205, 0.4);
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
      background: #09020c;
      border: 1px solid #260733;
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
    
    /* SHADER INOVADOR: Multiverse Dimensional Warp Corona */
    @keyframes scUmvHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(181, 38, 205, 0.95)) 
          drop-shadow(0 0 20px rgba(217, 70, 239, 0.6)) 
          drop-shadow(0 0 32px rgba(147, 51, 234, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(232, 121, 249, 0.9)) 
          drop-shadow(0 0 44px rgba(181, 38, 205, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-active {{
      animation: scUmvHaloPulse 2.2s ease-in-out infinite;
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
      background: #24072f;
      color: #f5d0fe;
    }}
    .btn-approve:hover {{
      background: #b526cd;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(181, 38, 205, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #e879f9, #b526cd);
      color: #120217;
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
      background: #20062a;
      color: #f5d0fe;
      border: 1px solid #3b0d4d;
    }}
    
    .footer-box {{
      background: #15051c;
      border: 1px solid #330b42;
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
          <span class="badge">Supercondutor Tier UMV</span>
          <span class="formula-tag">Tier UMV (UXV) • #B526CD</span>
        </div>
        <h1>Superconductor Base UMV — 3 Físicas Multiversais & Shaders</h1>
        <p class="subtitle">
          Supercondutor supremo de escala cósmica multiversal. 3 físicas quânticas não-triviais combinadas com o <strong>Dimensional Warp Corona Shader</strong>.
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#cbd5e1;">Simulador In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#e879f9;">✨ WARP CORONA ATIVADO</div>
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
            <span style="font-size:11px; color:#94a3b8;">Calabi-Yau 5D</span>
          </div>
          <div class="card-title">Calabi-Yau Manifold Wormhole Tunneling</div>
          <p class="card-desc">
            Projeção 2D de micro-variedade de <strong>Calabi-Yau com 5 lóbulos dimensionais</strong>. As supercorrentes multiversais dobram a garganta métrica do vácuo, realizando tunelamento quântico instantâneo com flashes de singularidade branca nas singularidades de Poincaré.
          </p>
          <div class="features-list">
            <span class="feature-item">Variedade de Calabi-Yau</span>
            <span class="feature-item">Garganta de Micro-Wormhole</span>
            <span class="feature-item">Singularidades de Poincaré</span>
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
            <span style="font-size:11px; color:#94a3b8;">Tranças de Anyons</span>
          </div>
          <div class="card-title">Non-Abelian Anyon Braid Currents</div>
          <p class="card-desc">
            Dinâmica topológica de <strong>tranças de Anyons de Majorana</strong>: 3 correntes quânticas senoidais entrelaçadas tecem nós protegidos topologicamente. Nos cruzamentos de trança não-comutativos, acendem nós estáveis de entrelaçamento quântico rosa-fúcsia.
          </p>
          <div class="features-list">
            <span class="feature-item">Anyons de Majorana</span>
            <span class="feature-item">Tranças Não-Comutativas</span>
            <span class="feature-item">Proteção Topológica</span>
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
            <span style="font-size:11px; color:#94a3b8;">Casimir Dinâmico</span>
          </div>
          <div class="card-title">Spacetime Metric Casimir Superfluid</div>
          <p class="card-desc">
            Oscilações métricas hiperbólicas de alta frequência no tensor do vácuo geram <strong>fótons virtuais convertidos em supercorrente de luz real</strong> (Efeito Casimir Dinâmico). Frentes de interferência métrica violeta respiram como um superfluido de energia de ponto zero.
          </p>
          <div class="features-list">
            <span class="feature-item">Efeito Casimir Dinâmico</span>
            <span class="feature-item">Superfluidez Métrica 2D</span>
            <span class="feature-item">Energia de Ponto Zero</span>
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
        Qual das 3 opções você prefere aprovar para o <strong>Superconductor Base UMV</strong>?
      </div>
      <div style="font-weight:700; color:#e879f9;">
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
        statusText.innerText = "✨ WARP CORONA ATIVADO";
        statusText.style.color = "#e879f9";
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
    html_path = ARTIFACT_DIR / "superconductor_umv_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase interativo salvo em: {html_path}")
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
