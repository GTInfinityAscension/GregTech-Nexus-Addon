#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Nitinol 60 (Ni4Ti6 • #c8c8c8)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/nitinol60_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (200, 200, 200, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (200, 200, 200, 255))

# =========================================================================
# Opção 1: Martensitic Twin-Boundary Shear Slip (Planos de Cisalhamento & Twinning)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Eixos cristalográficos de cisalhamento a 45 graus
    u = (x_coords + y_coords) * 0.7071
    v = (x_coords - y_coords) * 0.7071
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Cromo-prata polida pura com sombras de titânio (#C8C8C8)
        r = 34.0 + t_base * 172.0
        g = 37.0 + (t_base ** 1.05) * 174.0
        b = 44.0 + (t_base ** 1.1) * 178.0
        
        # Deslizamento relativo de bandas de cisalhamento atômico em direções opostas
        phase_u = 2 * np.pi * (u / 3.4 - t * 1.5)
        phase_v = 2 * np.pi * (v / 3.4 + t * 1.5)
        
        band_u = np.exp(-((np.sin(phase_u))**2) / 0.14)
        band_v = np.exp(-((np.sin(phase_v))**2) / 0.14)
        
        # Nós de tensão de cisalhamento nas interseções de geminação
        twin_nodes = (band_u * band_v) * 2.8 * (t_base > 0.3)
        
        # Modulação de reflexão especular polarizada dependente do ângulo do retículo
        lattice_shimmer = np.sin(phase_u * 0.5 + phase_v * 0.5) * 0.5 + 0.5
        specular = (lattice_shimmer ** 3.0) * (band_u + band_v) * 0.7 * (t_base > 0.25)
        
        total_fx = (band_u * 0.45 + band_v * 0.45 + twin_nodes * 1.2 + specular * 0.8) * (t_base > 0.22)
        
        # Realce metálico de platina-diamante
        r += total_fx * 65.0
        g += total_fx * 72.0
        b += total_fx * 85.0
        
        # Flashes brancos puros nas cristas de cisalhamento
        flash = np.clip(twin_nodes - 0.75, 0, 1.4) * 90.0
        r += flash * 0.98
        g += flash * 0.99
        b += flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Shock-Induced Pseudoelastic Healing (Onda de Impacto & Auto-Cura Elástica)
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
    
    # Linhas de contorno de micro-grão para filamentos de trinca
    grain_pattern = np.abs(np.sin(x_coords * 1.7 + y_coords * 1.1) * np.cos(x_coords * 1.1 - y_coords * 1.7))
    is_boundary = grain_pattern > 0.62
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Titânio acetinado e prata de alta tenacidade (#C8C8C8)
        r = 36.0 + t_base * 170.0
        g = 39.0 + (t_base ** 1.05) * 172.0
        b = 46.0 + (t_base ** 1.1) * 176.0
        
        shock = 0.0
        cracks = 0.0
        healing = 0.0
        
        # Ciclo de 3 Fases: Impacto (0-40%) -> Micro-Trincas (40-65%) -> Auto-Cura Instantânea (65-100%)
        if t < 0.40:
            # Fase 1: Onda oblíqua de choque hiperbólico de alta velocidade
            p1 = t / 0.40
            front_pos = -4.0 + p1 * 26.0
            coord_proj = (x_coords * 0.7 + y_coords * 0.7)
            shock = np.exp(-((coord_proj - front_pos) / 1.3)**2) * 1.6 * (t_base > 0.25)
        elif t < 0.65:
            # Fase 2: Aparecimento de micro-trincas de estresse nos contornos de grão
            p2 = (t - 0.40) / 0.25
            crack_intensity = np.sin(np.pi * p2)
            cracks = is_boundary.astype(float) * crack_intensity * 2.2 * (t_base > 0.3)
        else:
            # Fase 3: Auto-Cura Reversível Superelástica (Recristalização centrípeta instantânea)
            p3 = (t - 0.65) / 0.35
            heal_radius = 8.5 * (1.0 - p3)
            healing = np.exp(-((dist - heal_radius) / 1.2)**2) * 2.0 * (t_base > 0.28)
            
        total_effect = (shock * 1.1 + cracks * 1.3 + healing * 1.4)
        
        # Iluminação prata fria de estresse
        r += total_effect * 60.0
        g += total_effect * 68.0
        b += total_effect * 82.0
        
        # Flash de auto-cura branco especular diamantino
        specular_flash = np.clip(healing + shock * 0.8 - 0.7, 0, 1.5) * 85.0
        r += specular_flash * 0.98
        g += specular_flash * 0.99
        b += specular_flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Spinodal Decomposition Phase-Lattice (Decomposição Espinodal Cahn-Hilliard)
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
        
        # Equação contínua de decomposição espinodal de fases (Cahn-Hilliard multi-harmônico)
        # Separação entre fases ricas em Ni (superfície polida espelhada) e ricas em Ti (matriz tenaz)
        k1 = np.sin(x_coords * 0.85 + tau) * np.cos(y_coords * 0.95 - tau * 0.5)
        k2 = np.cos((x_coords + y_coords) * 0.65 - tau) * np.sin((x_coords - y_coords) * 0.65 + tau * 0.7)
        k3 = np.sin(y_coords * 1.1 + tau * 1.2) * 0.4
        
        order_param = (k1 + k2 + k3) / 2.0  # de -1.0 a +1.0
        
        # Domínios ricos em Ni: lustro prateado espelhado brilhante
        ni_rich = np.clip(order_param * 1.5, 0, 1.0) * (t_base > 0.22)
        # Domínios ricos em Ti: grafite titânico resistente e profundo
        ti_rich = np.clip(-order_param * 1.5, 0, 1.0) * (t_base > 0.22)
        # Interfaces de fase: linhas de fronteira de alto gradiente eletroquímico
        interfaces = np.exp(-((order_param / 0.18)**2)) * 1.6 * (t_base > 0.28)
        
        # Paleta Base de Nitinol 60
        r = 35.0 + t_base * 170.0
        g = 38.0 + (t_base ** 1.05) * 173.0
        b = 45.0 + (t_base ** 1.1) * 177.0
        
        # Modulação pelos domínios spinodais
        r += ni_rich * 48.0 - ti_rich * 18.0 + interfaces * 70.0
        g += ni_rich * 52.0 - ti_rich * 15.0 + interfaces * 75.0
        b += ni_rich * 64.0 - ti_rich * 10.0 + interfaces * 85.0
        
        # Reflexo especular diamantino nas interfaces de fase atômica
        specular = np.clip(interfaces - 0.75, 0, 1.4) * 85.0
        r += specular * 0.98
        g += specular * 0.99
        b += specular * 1.00
        
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
    print("Gerando candidatos para Nitinol 60 (Ni4Ti6 • #C8C8C8)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Martensitic Twin Slip", render_option_1),
        (2, "Pseudoelastic Healing", render_option_2),
        (3, "Spinodal Phase Lattice", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"nitinol60_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (nitinol60_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo grafite-platina escuro
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 20, 24, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "NITINOL 60 — VISUAL CANDIDATES (128x128)", fill=(241, 245, 249, 255), font=font_title)
    draw.text((pad_x, 38), "High-Hardness Superelastic Intermetallic • Ni4Ti6 • Chrome-Platinum • 30 Frames", fill=(148, 163, 184, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Twin Slip",
        "OPÇÃO 2: Healing Shock",
        "OPÇÃO 3: Spinodal Lattice"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(226, 232, 240, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(148, 163, 184, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (28, 32, 38) if (bx // 16 + by // 16) % 2 == 0 else (22, 25, 30)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(148, 163, 184, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "nitinol60_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Nitinol 60 — Avaliação de 3 Opções Visuais Inovadoras</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b0d11;
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
      background: linear-gradient(135deg, #1e2430 0%, #121620 60%, #0b0d11 100%);
      border: 1px solid rgba(200, 200, 200, 0.35);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 20px rgba(200, 200, 200, 0.1);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(200, 200, 200, 0.15);
      color: #f1f5f9;
      border: 1px solid rgba(200, 200, 200, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #cbd5e1;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #e2e8f0, #94a3b8);
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
      background: #141822;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #273042;
    }}
    .btn-toggle {{
      background: #475569;
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
      background: #64748b;
    }}
    .btn-toggle.active {{
      background: #38bdf8;
      color: #04121e;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
    }}
    
    .shape-bar {{
      background: #131722;
      border: 1px solid #242c3d;
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
      background: #090c10;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #242c3d;
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
      background: #cbd5e1;
      color: #0b0d11;
      box-shadow: 0 2px 8px rgba(255, 255, 255, 0.3);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #242c3d;
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
      background: #121620;
      border: 2px solid #232a3a;
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
      border-color: rgba(226, 232, 240, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #38bdf8;
      box-shadow: 0 0 24px rgba(56, 189, 248, 0.35);
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
      background: rgba(200, 200, 200, 0.15);
      color: #f1f5f9;
      border: 1px solid rgba(200, 200, 200, 0.3);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #080a0e;
      border: 1px solid #1e2433;
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
    
    /* SHADER INOVADOR: Polarized Stress Refraction Halo */
    @keyframes nitinolPolarizedHalo {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(226, 232, 240, 0.9)) 
          drop-shadow(0 0 18px rgba(56, 189, 248, 0.5)) 
          drop-shadow(0 0 28px rgba(148, 163, 184, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 26px rgba(125, 211, 252, 0.75)) 
          drop-shadow(0 0 38px rgba(203, 213, 225, 0.5));
        transform: scale(1.02);
      }}
    }}
    .halo-active {{
      animation: nitinolPolarizedHalo 2.5s ease-in-out infinite;
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
      background: #1e2536;
      color: #e2e8f0;
    }}
    .btn-approve:hover {{
      background: #334155;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #38bdf8, #0ea5e9);
      color: #04121e;
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
      background: #182030;
      color: #cbd5e1;
      border: 1px solid #28344c;
    }}
    
    .footer-box {{
      background: #131722;
      border: 1px solid #242c3d;
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
          <span class="badge">Refatoração de Textura & Shaders</span>
          <span class="formula-tag">Ni4Ti6 • #C8C8C8 • Superliga Tribológica</span>
        </div>
        <h1>Nitinol 60 — 3 Físicas Matemáticas & Shaders</h1>
        <p class="subtitle">
          Superliga ultra-dura de Níquel-Titânio (HRC 62, superelasticidade a frio). 3 matemáticas originais combinadas com o <strong>Polarized Stress Refraction Halo</strong>.
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#94a3b8;">Simulador In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#38bdf8;">✨ HALO ATIVADO</div>
        </div>
        <button class="btn-toggle active" id="btnToggleHalo" onclick="toggleShader()">Alternar Shader</button>
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
        Visualização: <strong>128×128px (Pixel Art Fiel 8× Zoom)</strong>
      </div>
    </div>

    <div class="grid-options">
      
      <!-- Option 1 -->
      <div class="card selected" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">Opção 1</span>
            <span style="font-size:11px; color:#64748b;">Twinning Cristalográfico</span>
          </div>
          <div class="card-title">Martensitic Twin-Boundary Shear Slip</div>
          <p class="card-desc">
            Rede de <strong>planos cristalográficos de cisalhamento em ±45°</strong> com bandas atômicas que deslizam em direções opostas sem atrito. As interseções geram nós de estresse de altíssima dureza que viajam pelas facetas com cintilação especular polarizada de titânio-platina.
          </p>
          <div class="features-list">
            <span class="feature-item">Cisalhamento Atômico ±45°</span>
            <span class="feature-item">Interferência de Geminação</span>
            <span class="feature-item">Reflexo Polarizado de Cromo</span>
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
            <span style="font-size:11px; color:#64748b;">Auto-Cura Reversível</span>
          </div>
          <div class="card-title">Shock-Induced Pseudoelastic Healing</div>
          <p class="card-desc">
            Ciclo não-linear balístico: <strong>onda oblíqua hiperbólica de choque</strong> varre a malha, micro-trincas de tensão surgem nos contornos de grão como relâmpagos cristalinos e sofrem <strong>auto-cura instantânea superelástica</strong> num flash concêntrico de recristalização espelhada.
          </p>
          <div class="features-list">
            <span class="feature-item">Onda Oblíqua Hiperbólica</span>
            <span class="feature-item">Micro-Fraturas de Estresse</span>
            <span class="feature-item">Auto-Cura Superelástica</span>
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
            <span style="font-size:11px; color:#64748b;">Dinâmica de Cahn-Hilliard</span>
          </div>
          <div class="card-title">Spinodal Phase Decomposition Lattice</div>
          <p class="card-desc">
            Modelagem física direta da <strong>equação de Cahn-Hilliard</strong>: nano-domínios vermiculares auto-organizados de fase Ni3Ti (prata lustrosa de alta reflexão) e fase Ti (grafite denso de absorção) que coalescem e se separam continuamente, com linhas de contorno em constante dança topológica.
          </p>
          <div class="features-list">
            <span class="feature-item">Decomposição Espinodal</span>
            <span class="feature-item">Nano-Domínios Ni3Ti & Ti</span>
            <span class="feature-item">Fluxo Hipnótico Vermicular</span>
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
        Qual das 3 opções você prefere aprovar para o <strong>Nitinol 60</strong>?
      </div>
      <div style="font-weight:700; color:#38bdf8;">
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
        statusText.innerText = "✨ HALO ATIVADO";
        statusText.style.color = "#38bdf8";
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
    html_path = ARTIFACT_DIR / "nitinol60_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase interativo salvo em: {html_path}")
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
