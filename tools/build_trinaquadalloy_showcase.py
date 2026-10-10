#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Trinaquadalloy
Fórmula: Nq₂WsHs (Trinium-Naquadah-Carbon Superalloy)
Cor: #281832 / #10B981 / #A855F7 (Roxo-Obsidiana, Esmeralda Radioativa e Violeta Cósmico)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/trinaquadalloy_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (40, 24, 50, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (40, 24, 50, 255))

# =========================================================================
# Opção 1: Heavy-Fermion Band Hybridization (Bandas de Fermions Pesados)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Roxo-Obsidiana profundo (#281832) com sombra grafite
        r = 18.0 + t_base * 95.0
        g = 10.0 + t_base * 65.0
        b = 26.0 + t_base * 125.0
        
        # Duas bandas de hibridização de férmions pesados deslizando em ângulos cruzados
        band_purple = np.sin((x_coords * 0.8 + y_coords * 0.4) - tau * 2.0)
        band_green = np.cos((x_coords * 0.4 - y_coords * 0.8) + tau * 1.5)
        
        # Densidade de carga modulada (CDW)
        hybrid_purple = np.exp(-((band_purple - 0.5)**2) / 0.15) * (t_base > 0.25)
        hybrid_green = np.exp(-((band_green - 0.5)**2) / 0.15) * (t_base > 0.22)
        
        # Brilho violeta-trinium
        r += hybrid_purple * 85.0
        g += hybrid_purple * 15.0
        b += hybrid_purple * 110.0
        
        # Brilho esmeralda-naquadah
        r += hybrid_green * 10.0
        g += hybrid_green * 95.0
        b += hybrid_green * 55.0
        
        # Nós de interferência construtiva quântica (cruzamento das duas bandas)
        cross_nodes = (hybrid_purple * hybrid_green) * 2.5
        flash = np.clip(cross_nodes - 0.7, 0, 1.5) * 115.0
        r += flash * 0.95
        g += flash * 1.00
        b += flash * 0.95
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Helical Fluxon Supercurrent Vortices (Hélice Dupla de Fluxons)
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
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Roxo-Obsidiana Metálico (#281832)
        r = 20.0 + t_base * 92.0
        g = 12.0 + t_base * 68.0
        b = 28.0 + t_base * 120.0
        
        # Hélice dupla de supercorrentes girando em contra-fase ao redor do baricentro
        helix1 = np.sin(2.0 * angle + dist * 1.2 - tau * 2.5)
        helix2 = np.cos(2.0 * angle - dist * 1.2 + tau * 2.5)
        
        flux_violet = np.clip(helix1, 0, 1.0) * np.exp(-dist / 5.5) * (t_base > 0.22)
        flux_green = np.clip(helix2, 0, 1.0) * np.exp(-dist / 5.5) * (t_base > 0.22)
        
        # Brilho das hélices de Trinium (violeta) e Naquadah (verde)
        r += flux_violet * 90.0
        g += flux_violet * 18.0
        b += flux_violet * 115.0
        
        r += flux_green * 8.0
        g += flux_green * 105.0
        b += flux_green * 60.0
        
        # Ancoramento quântico no núcleo de supercorrente
        core_flux = np.exp(-((dist / 1.5)**2)) * (1.0 + 0.7 * np.sin(tau * 3.0)) * (t_base > 0.3)
        flash = np.clip(core_flux - 0.8, 0, 1.5) * 110.0
        r += flash * 0.90
        g += flash * 1.00
        b += flash * 0.95
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Spontaneous Decay Cavitation & Cherenkov (Cavitação & Cherenkov)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # 4 núcleos de cavitação de decaimento subatômico em coordenadas assimétricas
    cavities = [(5.0, 5.5), (11.0, 5.0), (6.5, 11.5), (11.5, 11.0)]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Roxo-Obsidiana Noturno (#281832)
        r = 18.0 + t_base * 94.0
        g = 11.0 + t_base * 66.0
        b = 27.0 + t_base * 122.0
        
        cherenkov_pulses = 0.0
        for idx, (cx, cy) in enumerate(cavities):
            dist_c = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
            
            # Ciclo de cada cavidade: contração de vácuo métrico seguida por detonação Cherenkov
            phase_c = (tau + idx * 1.57) % (2 * np.pi)
            burst = np.exp(-((phase_c - np.pi)**2) / 0.35)
            
            # Onda de choque esférica de Cherenkov
            shock_radius = 4.0 * (phase_c / (2 * np.pi))
            wave = np.exp(-((dist_c - shock_radius)**2) / 0.8) * burst
            core = np.exp(-((dist_c / 1.3)**2)) * burst * 1.5
            
            cherenkov_pulses += wave * 1.2 + core * 1.5
            
        total_cherenkov = cherenkov_pulses * (t_base > 0.22)
        
        # Radiação de Cherenkov verde-esmeralda/ciano luminosa
        r += total_cherenkov * 25.0
        g += total_cherenkov * 95.0
        b += total_cherenkov * 75.0
        
        # Auréola violeta ao redor das cavitações
        r += total_cherenkov * 40.0
        b += total_cherenkov * 60.0
        
        # Picos de flash nos colapsos de cavidade
        flash = np.clip(total_cherenkov - 1.1, 0, 1.5) * 110.0
        r += flash * 0.88
        g += flash * 1.00
        b += flash * 0.95
        
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
    print("Gerando candidatos para Trinaquadalloy (Nq₂WsHs, #281832 / #10B981 / #A855F7)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Heavy-Fermion Hybridization", render_option_1),
        (2, "Helical Fluxon Vortices", render_option_2),
        (3, "Decay Cavitation Cherenkov", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"tna_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (trinaquadalloy_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo roxo-abissal profundo
    grid_img = Image.new("RGBA", (grid_w, grid_h), (20, 12, 28, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "TRINAQUADALLOY (Nq₂WsHs) — 128x128 CANDIDATES", fill=(192, 132, 252, 255), font=font_title)
    draw.text((pad_x, 38), "Trinium-Naquadah-Carbon Superalloy • 8,747K EBF • #281832 / #10B981 • 30 Frames", fill=(167, 243, 208, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Heavy-Fermion",
        "OPÇÃO 2: Helical Fluxons",
        "OPÇÃO 3: Cherenkov Cavitation"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(243, 232, 255, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(192, 132, 252, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (32, 18, 44) if (bx // 16 + by // 16) % 2 == 0 else (24, 14, 34)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(168, 85, 247, 100), width=1)
            
    grid_png_path = ARTIFACT_DIR / "trinaquadalloy_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trinaquadalloy — 3 Opções Visuais & Shaders Quânticos</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0d0614;
      color: #f5f3ff;
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
      background: linear-gradient(135deg, #2b1238 0%, #170822 60%, #0d0614 100%);
      border: 1px solid rgba(168, 85, 247, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.25), 0 0 20px rgba(16, 185, 129, 0.15);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.45);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 13px;
      color: #6ee7b7;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #c084fc, #34d399);
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
      background: #190a26;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #3b1754;
    }}
    .btn-toggle {{
      background: #9333ea;
      color: #ffffff;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(147, 51, 234, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #a855f7;
    }}
    .btn-toggle.active {{
      background: #a855f7;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(168, 85, 247, 0.7);
    }}
    
    .shape-bar {{
      background: #150920;
      border: 1px solid #301442;
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
      background: #0d0514;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #301442;
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
      background: #9333ea;
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(147, 51, 234, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #301442;
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
      background: #13071c;
      border: 2px solid #2d123d;
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
      border-color: rgba(168, 85, 247, 0.65);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #a855f7;
      box-shadow: 0 0 24px rgba(168, 85, 247, 0.4);
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
      background: rgba(168, 85, 247, 0.2);
      color: #c084fc;
      border: 1px solid rgba(168, 85, 247, 0.4);
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
      background: #08030c;
      border: 1px solid #250d32;
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
    
    /* SHADER 1: Heavy-Fermion Biaxial Kondo Resonance Corona */
    @keyframes kondoHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(-3px 0 8px rgba(168, 85, 247, 0.9)) 
          drop-shadow(3px 0 12px rgba(16, 185, 129, 0.8)) 
          drop-shadow(0 0 28px rgba(192, 132, 252, 0.5));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 -3px 14px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 3px 20px rgba(52, 211, 153, 0.9)) 
          drop-shadow(0 0 40px rgba(168, 85, 247, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-active-1 {{
      animation: kondoHaloPulse 2.2s ease-in-out infinite;
    }}
    
    /* SHADER 2: Helical Fluxon Precession Gyro-Halo */
    @keyframes fluxonGyroPulse {{
      0% {{
        filter: 
          drop-shadow(0 0 10px rgba(168, 85, 247, 0.85)) 
          drop-shadow(0 0 20px rgba(16, 185, 129, 0.65)) 
          drop-shadow(0 0 32px rgba(147, 51, 234, 0.5));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(110, 231, 183, 0.9)) 
          drop-shadow(0 0 46px rgba(168, 85, 247, 0.75));
        transform: scale(1.025);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 10px rgba(168, 85, 247, 0.85)) 
          drop-shadow(0 0 20px rgba(16, 185, 129, 0.65)) 
          drop-shadow(0 0 32px rgba(147, 51, 234, 0.5));
        transform: scale(1);
      }}
    }}
    .halo-active-2 {{
      animation: fluxonGyroPulse 2.4s ease-in-out infinite;
    }}
    
    /* SHADER 3: Cherenkov Micro-Cavitation Pulse Halo */
    @keyframes cherenkovPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(16, 185, 129, 0.85)) 
          drop-shadow(0 0 18px rgba(168, 85, 247, 0.6)) 
          drop-shadow(0 0 30px rgba(5, 150, 105, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 18px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 32px rgba(52, 211, 153, 0.95)) 
          drop-shadow(0 0 46px rgba(192, 132, 252, 0.7));
        transform: scale(1.03);
      }}
    }}
    .halo-active-3 {{
      animation: cherenkovPulse 1.9s ease-in-out infinite;
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
      background: #250d32;
      color: #e9d5ff;
    }}
    .btn-approve:hover {{
      background: #9333ea;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(147, 51, 234, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #c084fc, #10b981);
      color: #0d0514;
      font-weight: 800;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
    }}
    .feat-tag {{
      background: #1b0a24;
      border: 1px solid #371448;
      color: #c084fc;
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 4px;
    }}

    .card-footer {{
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}
    .btn-card-shader {{
      background: transparent;
      border: 1px solid #431956;
      color: #cbd5e1;
      font-size: 11px;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-card-shader:hover {{
      background: #2b1238;
      color: #ffffff;
    }}
    .btn-card-shader.active {{
      background: rgba(168, 85, 247, 0.25);
      border-color: #a855f7;
      color: #e9d5ff;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">Trinium-Naquadah-Carbon Superalloy</span>
        <span class="formula-tag">Nq₂WsHs</span>
        <h1>Trinaquadalloy</h1>
        <p class="subtitle">EBF 8,747K • Tier ZPM/UV • Resistência à Curvatura de Espaço • Paleta #281832 / #10B981 / #A855F7</p>
      </div>
      
      <div class="shader-control">
        <div>
          <div style="font-size: 12px; font-weight: 700; color: #ffffff;">Simulador de Shaders</div>
          <div id="shader-status-text" style="font-size: 11px; color: #c084fc;">Shader Ativo (RenderBlender)</div>
        </div>
        <button id="toggle-shader-btn" class="btn-toggle active" onclick="toggleAllShaders()">SHADER ATIVO</button>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 13px; font-weight: 600; color: #cbd5e1;">Visualizar Forma do Material:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
    </div>
    
    <div class="grid-options">
      
      <!-- OPÇÃO 1 -->
      <div class="card" id="card-1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 11px; color: #c084fc;">Física: Heavy-Fermion Hybridization</span>
          </div>
          <div class="card-title">Heavy-Fermion Kondo Bands</div>
          <p class="card-desc">
            Acoplamento Kondo entre orbitais 5f de Naquadah e elétrons de condução de Trinium: duas ondas de densidade de carga (CDW) cruzam as facetas em ângulos opostos, gerando filamentos entrelaçados em roxo-obsidiana e esmeralda com nós quânticos nos cruzamentos.
          </p>
          <div class="features-list">
            <span class="feat-tag">Hibridização Kondo 5f</span>
            <span class="feat-tag">Bandas Cruzadas CDW</span>
            <span class="feat-tag">Nós de Interferência</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-1" class="pixelated-art halo-active-1" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-1" class="btn-card-shader active" onclick="toggleCardShader(1)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(1)">ESCOLHER OPÇÃO 1 (HEAVY-FERMION)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 2</span>
            <span style="font-size: 11px; color: #c084fc;">Física: Helical Fluxons</span>
          </div>
          <div class="card-title">Helical Fluxon Supercurrents</div>
          <p class="card-desc">
            Hélice dupla de supercorrentes quirais viajando ao redor do baricentro do cristal: filamentos de fluxo magnético em rotação helicoidal oposta em violeta-trinium e esmeralda-naquadah com ancoramento quântico central pulsante.
          </p>
          <div class="features-list">
            <span class="feat-tag">Dupla Hélice Quiral</span>
            <span class="feat-tag">Fluxons de Trinium-Naquadah</span>
            <span class="feat-tag">Ancoramento Central</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-2" class="pixelated-art halo-active-2" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-2" class="btn-card-shader active" onclick="toggleCardShader(2)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(2)">ESCOLHER OPÇÃO 2 (HELICAL FLUXONS)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 3</span>
            <span style="font-size: 11px; color: #c084fc;">Física: Cherenkov Cavitation</span>
          </div>
          <div class="card-title">Decay Cavitation & Cherenkov</div>
          <p class="card-desc">
            Decaimento estocástico subatômico de Naquadah sob compressão de Trinium: 4 núcleos de cavitação acumulam energia métrica escura e colapsam em ondas de choque esféricas de radiação Cherenkov verde-esmeralda luminescente cercadas por vácuo roxo.
          </p>
          <div class="features-list">
            <span class="feat-tag">Cavitação de Vácuo Métrico</span>
            <span class="feat-tag">Radiação Cherenkov #10B981</span>
            <span class="feat-tag">Ondas de Choque Locais</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-3" class="pixelated-art halo-active-3" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-3" class="btn-card-shader active" onclick="toggleCardShader(3)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(3)">ESCOLHER OPÇÃO 3 (CHERENKOV)</button>
        </div>
      </div>
      
    </div>
    
  </div>

  <script>
    const b64Data = {json_b64};
    let currentShape = 'ingot';
    let globalShaderActive = true;
    let cardShaderActive = {{ 1: true, 2: true, 3: true }};

    function setShape(shape, btn) {{
      currentShape = shape;
      document.querySelectorAll('.btn-shape').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      for (let opt = 1; opt <= 3; opt++) {{
        const img = document.getElementById('img-opt-' + opt);
        if (img && b64Data[opt] && b64Data[opt][shape]) {{
          img.src = b64Data[opt][shape];
        }}
      }}
    }}

    function toggleAllShaders() {{
      globalShaderActive = !globalShaderActive;
      const btn = document.getElementById('toggle-shader-btn');
      const text = document.getElementById('shader-status-text');
      
      if (globalShaderActive) {{
        btn.classList.add('active');
        btn.innerText = 'SHADER ATIVO';
        text.innerText = 'Shader Ativo (RenderBlender)';
        text.style.color = '#c084fc';
        cardShaderActive = {{ 1: true, 2: true, 3: true }};
      }} else {{
        btn.classList.remove('active');
        btn.innerText = 'SHADER DESATIVADO';
        text.innerText = 'Pixel Art Pura (Sem Shader)';
        text.style.color = '#94a3b8';
        cardShaderActive = {{ 1: false, 2: false, 3: false }};
      }}
      
      for (let opt = 1; opt <= 3; opt++) {{
        updateCardShaderState(opt);
      }}
    }}

    function toggleCardShader(opt) {{
      cardShaderActive[opt] = !cardShaderActive[opt];
      updateCardShaderState(opt);
    }}

    function updateCardShaderState(opt) {{
      const img = document.getElementById('img-opt-' + opt);
      const btn = document.getElementById('btn-shader-' + opt);
      const activeClass = 'halo-active-' + opt;
      
      if (cardShaderActive[opt]) {{
        img.classList.add(activeClass);
        btn.classList.add('active');
        btn.innerText = 'Shader Desta Opção: ATIVO';
      }} else {{
        img.classList.remove(activeClass);
        btn.classList.remove('active');
        btn.innerText = 'Shader Desta Opção: DESATIVADO';
      }}
    }}

    function selectOption(opt) {{
      document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
      document.getElementById('card-' + opt).classList.add('selected');
      console.log('Opção ' + opt + ' selecionada');
    }}
  </script>
</body>
</html>
"""
    
    html_path = ARTIFACT_DIR / "trinaquadalloy_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
