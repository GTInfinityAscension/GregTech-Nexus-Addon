#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Hastelloy-N75
Fórmula: Ni₁₅Mo₉Cr₄Ti₂Er₂ (Molten Salt Resistant Rare-Earth Superalloy)
Cor: #8b6914 / #cdad00 / #22c55e (Dourado-Âmbar de Molibdênio, Érbio e Passivação Fluoretada)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/hastelloy_n_75_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (139, 105, 20, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (139, 105, 20, 255))

# =========================================================================
# Opção 1: Molten Fluoride Boundary Passivation & Erbium Solute Drag
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
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Dourado-Âmbar de Hastelloy-N (#8b6914)
        r = 32.0 + t_base * 125.0
        g = 24.0 + t_base * 95.0
        b = 6.0 + t_base * 20.0
        
        # Onda de passivação eletroquímica por sais fluoretados fundidos a 4550K
        fluoride_wave = np.sin(dist * 1.3 - tau * 2.5 + np.cos(4.0 * angle) * 1.4)
        passivation = np.clip(fluoride_wave, 0, 1.0) * (t_base > 0.22)
        
        # Zonas de arrasto de soluto de Érbio (solute drag pinning) nos contornos de grão
        erbium_pinning = np.exp(-((fluoride_wave - 0.72)**2) / 0.09) * (t_base > 0.25)
        
        # Realce dourado-ouro e verde-esmeralda da barreira passivante de fluoreto
        r += passivation * 75.0
        g += passivation * 68.0
        b += passivation * 14.0
        
        # Barreira de soluto de Érbio reluzente em ouro-âmbar vivo
        r += erbium_pinning * 85.0
        g += erbium_pinning * 80.0
        b += erbium_pinning * 30.0
        
        # Flashes cristalinos nos sítios de ancoramento de soluto
        flash = np.clip(erbium_pinning - 0.75, 0, 1.5) * 95.0
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
# Opção 2: Intergranular M₂₃C₆ Carbide Pinning & Laves Phase Network
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
        
        # Paleta Base: Âmbar Escuro e Bronze de Molibdênio (#8b6914)
        r = 30.0 + t_base * 122.0
        g = 22.0 + t_base * 92.0
        b = 5.0 + t_base * 18.0
        
        # Rede celular intergranular de carbetos secundários M₂₃C₆ (tripla família de planos)
        w1 = np.sin(x_coords * 0.95 + y_coords * 0.55 - tau * 1.5)
        w2 = np.sin(-x_coords * 0.55 + y_coords * 0.95 + tau * 1.5)
        w3 = np.sin(x_coords * 0.70 - y_coords * 0.70 - tau * 1.0)
        
        carbide_net = np.abs(w1 * w2 + w2 * w3 + w3 * w1)
        carbides = np.clip(carbide_net * 0.8, 0, 1.2) * (t_base > 0.22)
        
        # Nós intermetálicos de fase de Laves (Ni₂Er / Fe₂Mo) nas junções triplas
        laves_nodes = np.exp(-((w1**2 + w2**2 + w3**2) / 0.55)) * (t_base > 0.25)
        
        # Ouro-bronze refratário ao longo dos carbetos
        r += carbides * 78.0
        g += carbides * 62.0
        b += carbides * 15.0
        
        # Nós de ancoramento de fase de Laves em platina-dourada intensa
        r += laves_nodes * 95.0
        g += laves_nodes * 92.0
        b += laves_nodes * 45.0
        
        # Flashes pontuais nos nós de bloqueio de cisalhamento
        flash = np.clip(laves_nodes - 0.7, 0, 1.6) * 105.0
        r += flash * 1.00
        g += flash * 0.96
        b += flash * 0.80
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Rare-Earth Resonant Neutron Absorption & Thermal Micro-Plasmonics
# =========================================================================
def render_option_3(base_arr, n_frames=30):
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
        
        # Paleta Base: Ouro-Âmbar Metálico Profundo (#8b6914)
        r = 34.0 + t_base * 128.0
        g = 25.0 + t_base * 96.0
        b = 6.0 + t_base * 19.0
        
        # Ressonância plasmônica acoplada aos orbitais 4f de Er³⁺ em modos espirais
        mode1 = np.sin(3.0 * angle - dist * 0.85 + tau * 3.0)
        mode2 = np.cos(2.0 * angle + dist * 1.15 - tau * 2.0)
        
        plasmon = np.clip(mode1 * mode2 * 1.5, 0, 1.2) * (t_base > 0.22)
        
        # Emissão óptica estimulada por upconversion fotônica de Érbio (luminescência verde-esmeralda característica de 550nm)
        r += plasmon * 70.0
        g += plasmon * 105.0  # Realce espectral verde de terra rara
        b += plasmon * 28.0
        
        # Onda de choque de absorção neutrônica ressonante (seção de choque térmica de Er)
        neutron_shock = np.exp(-((dist - (f % 15) * 0.8)**2) / 1.2) * (t_base > 0.26)
        r += neutron_shock * 80.0
        g += neutron_shock * 85.0
        b += neutron_shock * 55.0
        
        # Flashes quânticos de decaimento radiativo ultra-rápido
        flash = np.clip(plasmon + neutron_shock - 1.2, 0, 1.6) * 98.0
        r += flash * 0.98
        g += flash * 1.00
        b += flash * 0.90
        
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
    print("Gerando candidatos para Hastelloy-N75 (Ni₁₅Mo₉Cr₄Ti₂Er₂, #8b6914)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Fluoride Passivation & Er Drag", render_option_1),
        (2, "M₂₃C₆ Carbides & Laves Network", render_option_2),
        (3, "Resonant Neutron Micro-Plasmonics", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"hastelloy_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (hastelloy_n_75_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (20, 16, 10, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "HASTELLOY-N75 (Ni₁₅Mo₉Cr₄Ti₂Er₂) — 128x128", fill=(251, 191, 36, 255), font=font_title)
    draw.text((pad_x, 38), "Molten Salt Resistant Superalloy • 4,550K EBF • EV Tier • #8b6914 • 30 Frames", fill=(217, 119, 6, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Fluoride Passivation",
        "OPÇÃO 2: Carbides & Laves Net",
        "OPÇÃO 3: Resonant Plasmonics"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(254, 243, 199, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(217, 119, 6, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (34, 26, 14) if (bx // 16 + by // 16) % 2 == 0 else (24, 18, 10)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(180, 83, 9, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "hastelloy_n_75_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hastelloy-N75 — 3 Opções Visuais & Shaders Refratários</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0c0905;
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
      background: linear-gradient(135deg, #26190a 0%, #160e04 60%, #0c0905 100%);
      border: 1px solid rgba(217, 119, 6, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(15, 10, 4, 0.7), 0 0 25px rgba(217, 119, 6, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(217, 119, 6, 0.25);
      color: #fde68a;
      border: 1px solid rgba(217, 119, 6, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fbbf24;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #fde68a, #d97706);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #d97706;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #171007;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #36220b;
    }}
    .btn-toggle {{
      background: #78350f;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(120, 53, 15, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #92400e;
    }}
    .btn-toggle.active {{
      background: #f59e0b;
      color: #1a0e02;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(245, 158, 11, 0.7);
    }}
    .status-text {{
      font-size: 12px;
      font-weight: 600;
      color: #92400e;
    }}
    .status-text.active {{
      color: #fde68a;
      text-shadow: 0 0 8px rgba(251, 191, 36, 0.5);
    }}
    
    .shape-bar {{
      background: #150f06;
      border: 1px solid #33200b;
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
      background: #0d0903;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #2e1c09;
    }}
    .btn-shape {{
      background: transparent;
      color: #b45309;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #78350f;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #fde68a;
      background: #261606;
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
      background: #120d06;
      border: 2px solid #2e1c09;
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
      border-color: rgba(245, 158, 11, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f59e0b;
      box-shadow: 0 0 24px rgba(245, 158, 11, 0.35);
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
      background: rgba(217, 119, 6, 0.2);
      color: #fde68a;
      border: 1px solid rgba(217, 119, 6, 0.4);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #d97706;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #080603;
      border: 1px solid #261706;
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
    
    /* SHADER 1: Molten Fluoride Boundary Diffusion Halo */
    @keyframes fluorideHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(217, 119, 6, 0.8)) 
          drop-shadow(0 0 18px rgba(251, 191, 36, 0.55)) 
          drop-shadow(0 0 32px rgba(34, 197, 94, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(251, 191, 36, 0.85)) 
          drop-shadow(0 0 44px rgba(34, 197, 94, 0.6));
        transform: scale(1.025);
      }}
    }}
    .halo-active-1 {{
      animation: fluorideHaloPulse 2.2s ease-in-out infinite;
    }}
    
    /* SHADER 2: Intermetallic Stacking-Fault Refraction Corona */
    @keyframes lavesRefractPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(245, 158, 11, 0.75)) 
          drop-shadow(0 0 16px rgba(217, 119, 6, 0.5)) 
          drop-shadow(0 0 28px rgba(180, 83, 9, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 15px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 26px rgba(253, 230, 138, 0.85)) 
          drop-shadow(0 0 40px rgba(245, 158, 11, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-active-2 {{
      animation: lavesRefractPulse 1.9s ease-in-out infinite;
    }}
    
    /* SHADER 3: Photonic Upconversion Plasmonic Corona */
    @keyframes plasmonUpconversionPulse {{
      0% {{
        filter: 
          drop-shadow(0 0 8px rgba(234, 179, 8, 0.8)) 
          drop-shadow(0 0 18px rgba(34, 197, 94, 0.65)) 
          drop-shadow(0 0 32px rgba(245, 158, 11, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 18px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 30px rgba(34, 197, 94, 0.9)) 
          drop-shadow(0 0 46px rgba(251, 191, 36, 0.8));
        transform: scale(1.03);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 8px rgba(234, 179, 8, 0.8)) 
          drop-shadow(0 0 18px rgba(34, 197, 94, 0.65)) 
          drop-shadow(0 0 32px rgba(245, 158, 11, 0.45));
        transform: scale(1);
      }}
    }}
    .halo-active-3 {{
      animation: plasmonUpconversionPulse 2.4s ease-in-out infinite;
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
      background: #2a1807;
      color: #fde68a;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}
    .btn-approve:hover {{
      background: #78350f;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.5);
    }}
    
    .features-list {{
      list-style: none;
      font-size: 11px;
      color: #b45309;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 6px;
    }}
    .features-list li::before {{
      content: "▹ ";
      color: #f59e0b;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">GTNA Material Set Showcase</span>
        <span class="formula-tag">Ni₁₅Mo₉Cr₄Ti₂Er₂</span>
        <h1>Hastelloy-N75</h1>
        <p class="subtitle">Superliga de Terras Raras Resistente a Sais Fundidos • 4,550K EBF • EV Tier • 30 Frames Fluídos</p>
      </div>
      <div class="shader-control">
        <button id="btnShader" class="btn-toggle active" onclick="toggleShader()">Shader: ATIVO</button>
        <span id="shaderStatus" class="status-text active">Halo & Corona Dinâmicos</span>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 12px; font-weight: 700; color: #fde68a;">Formas do Conjunto de Texturas:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
      <div style="font-size: 11px; color: #b45309;">Zoom 8× nativo (128×128 pixel art fiel)</div>
    </div>
    
    <div class="grid-options">
      
      <!-- Opção 1 -->
      <div class="card" id="card1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 10px; color: #b45309;">Passivação Eletroquímica</span>
          </div>
          <div class="card-title">Fluoride Passivation & Er Drag</div>
          <div class="card-desc">
            Passivação em banho de sais fluoretados fundidos a 4550K: ondas eletroquímicas radiais com efeito de arrasto de soluto de Érbio (solute drag pinning) estabilizando contornos de grão.
          </div>
          <ul class="features-list">
            <li>Matriz de Hastelloy-N dourado-âmbar (#8b6914)</li>
            <li>Frentes de passivação verde-ouro sob fluoreto</li>
            <li>Flashes cristalinos nos sítios de ancoramento de Érbio</li>
            <li><strong>Shader:</strong> Molten Fluoride Boundary Diffusion Halo</li>
          </ul>
        </div>
        <div class="image-box">
          <img id="imgOpt1" class="pixelated-art halo-active-1" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
        </div>
        <button class="btn-approve" onclick="selectOption(1)">Aprovar Opção 1</button>
      </div>
      
      <!-- Opção 2 -->
      <div class="card" id="card2">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 2</span>
            <span style="font-size: 10px; color: #b45309;">Rede Intermetálica</span>
          </div>
          <div class="card-title">M₂₃C₆ Carbides & Laves Net</div>
          <div class="card-desc">
            Rede celular intergranular de carbetos secundários de molibdênio M₂₃C₆ e fases de Laves hexagonais (Ni₂Er) nas junções triplas com rigidez a cisalhamento térmico.
          </div>
          <ul class="features-list">
            <li>Estrutura celular Voronoi em relevo metálico de ouro-bronze</li>
            <li>Nós intermetálicos de fase de Laves em platina-dourada</li>
            <li>Contraste marcante entre matriz profunda e contornos de grão</li>
            <li><strong>Shader:</strong> Intermetallic Stacking-Fault Refraction Corona</li>
          </ul>
        </div>
        <div class="image-box">
          <img id="imgOpt2" class="pixelated-art halo-active-2" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
        </div>
        <button class="btn-approve" onclick="selectOption(2)">Aprovar Opção 2</button>
      </div>
      
      <!-- Opção 3 -->
      <div class="card" id="card3">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 3</span>
            <span style="font-size: 10px; color: #b45309;">Ressonância Quântica</span>
          </div>
          <div class="card-title">Resonant Neutron Plasmonics</div>
          <div class="card-desc">
            Acoplamento plasmônico de superfície com os orbitais 4f de Er³⁺: emissão estimulada de upconversion fotônica em ondas estacionárias espirais acopladas com flashes de absorção neutrônica.
          </div>
          <ul class="features-list">
            <li>Luminescência verde-esmeralda característica de Er³⁺ (550nm)</li>
            <li>Ondas espirais de ressonância plasmônica térmica</li>
            <li>Ondas de choque de absorção neutrônica de alta velocidade</li>
            <li><strong>Shader:</strong> Photonic Upconversion Plasmonic Corona</li>
          </ul>
        </div>
        <div class="image-box">
          <img id="imgOpt3" class="pixelated-art halo-active-3" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
        </div>
        <button class="btn-approve" onclick="selectOption(3)">Aprovar Opção 3</button>
      </div>
      
    </div>
    
  </div>
  
  <script>
    const data = {json_b64};
    let currentShape = 'ingot';
    let shaderActive = true;
    
    function setShape(shape, btn) {{
      currentShape = shape;
      document.querySelectorAll('.btn-shape').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      document.getElementById('imgOpt1').src = data[1][shape];
      document.getElementById('imgOpt2').src = data[2][shape];
      document.getElementById('imgOpt3').src = data[3][shape];
    }}
    
    function toggleShader() {{
      shaderActive = !shaderActive;
      const btn = document.getElementById('btnShader');
      const status = document.getElementById('shaderStatus');
      const img1 = document.getElementById('imgOpt1');
      const img2 = document.getElementById('imgOpt2');
      const img3 = document.getElementById('imgOpt3');
      
      if (shaderActive) {{
        btn.classList.add('active');
        btn.innerText = 'Shader: ATIVO';
        status.classList.add('active');
        status.innerText = 'Halo & Corona Dinâmicos';
        img1.className = 'pixelated-art halo-active-1';
        img2.className = 'pixelated-art halo-active-2';
        img3.className = 'pixelated-art halo-active-3';
      }} else {{
        btn.classList.remove('active');
        btn.innerText = 'Shader: DESATIVADO';
        status.classList.remove('active');
        status.innerText = 'Render Estático Vanilla';
        img1.className = 'pixelated-art';
        img2.className = 'pixelated-art';
        img3.className = 'pixelated-art';
      }}
    }}
    
    function selectOption(opt) {{
      document.querySelectorAll('.card').forEach(c => c.classList.remove('selected'));
      document.getElementById('card' + opt).classList.add('selected');
      alert('Você escolheu a Opção ' + opt + '! Digite ' + opt + ' no chat para confirmar.');
    }}
  </script>
</body>
</html>
"""
    
    showcase_path = ARTIFACT_DIR / "hastelloy_n_75_showcase.html"
    showcase_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {showcase_path}")
    print("\nTodos os artefatos para Hastelloy-N75 foram gerados com sucesso!")

if __name__ == "__main__":
    main()
