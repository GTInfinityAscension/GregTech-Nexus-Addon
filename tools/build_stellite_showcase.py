#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Stellite
Fórmula: Co₉Cr₉Mn₅Ti₂ (High-Hardness Wear-Resistant Cobalt Superalloy)
Cor: #888192 / #b0a8ba / #c4b5fd (Aço-Cobalto Acetinado, Lilás Metálico e Brilho Estelar)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/stellite_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (136, 129, 146, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (136, 129, 146, 255))

# =========================================================================
# Opção 1: Martensitic Tribological Shock & Cavitation Resilience
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
    # Ondas de tensão elípticas de cisalhamento tribológico
    dist = np.sqrt(dx**2 + 1.4 * dy**2 + 0.6 * dx * dy)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Aço-Cobalto acetinado profundo (#888192)
        r = 28.0 + t_base * 108.0
        g = 26.0 + t_base * 103.0
        b = 32.0 + t_base * 114.0
        
        # Ondas concêntricas de choque de transformação martensítica (FCC -> HCP)
        shock_wave = np.sin(dist * 1.5 - tau * 3.0)
        compress = np.clip(shock_wave, 0, 1.0) * (t_base > 0.22)
        
        # Anéis de ancoramento de discordância de alto impacto
        pinning = np.exp(-((shock_wave - 0.75)**2) / 0.08) * (t_base > 0.25)
        
        # Realce violeta-platina de cobalto deformado
        r += compress * 65.0
        g += compress * 62.0
        b += compress * 82.0
        
        # Flashes estelares nos nós de relaxamento compressivo
        r += pinning * 85.0
        g += pinning * 85.0
        b += pinning * 95.0
        
        flash = np.clip(pinning - 0.7, 0, 1.5) * 105.0
        r += flash * 1.00
        g += flash * 0.98
        b += flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: HCP Cobalt Stacking Faults & Spinodal Decomposition
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Rede hexagonal de planos de escorregamento HCP em 60°
    cos60, sin60 = 0.5, 0.866025
    u1 = x_coords
    u2 = x_coords * cos60 + y_coords * sin60
    u3 = -x_coords * cos60 + y_coords * sin60
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Aço e Cromo de Alta Dureza (#888192)
        r = 27.0 + t_base * 106.0
        g = 25.0 + t_base * 101.0
        b = 31.0 + t_base * 115.0
        
        # Decomposição espinodal periódica (flutuações senoidais de composição)
        spinodal1 = np.sin(u1 * 0.85 + tau * 2.0)
        spinodal2 = np.sin(u2 * 0.85 - tau * 2.0)
        spinodal3 = np.sin(u3 * 0.85 + tau * 1.0)
        
        spinodal_net = (spinodal1 + spinodal2 + spinodal3) / 3.0
        spin_pos = np.clip(spinodal_net, 0, 1.0) * (t_base > 0.22)
        
        # Falhas de empilhamento (stacking faults) com interferência Moiré cristalina
        moire = np.abs(np.sin(u1 * 1.2 - tau * 1.5) * np.sin(u2 * 1.2 + tau * 1.5))
        faults = np.clip(moire * 1.4, 0, 1.2) * (t_base > 0.25)
        
        # Realces em prata-titânio e lilás de cobalto
        r += spin_pos * 68.0
        g += spin_pos * 65.0
        b += spin_pos * 88.0
        
        r += faults * 72.0
        g += faults * 70.0
        b += faults * 92.0
        
        # Picos de difração nos cruzamentos das falhas de empilhamento
        flash = np.clip(faults * spin_pos - 0.45, 0, 1.6) * 110.0
        r += flash * 0.98
        g += flash * 0.98
        b += flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Self-Healing Tribofilm & Haynes Stellar Gleam
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
        
        # Paleta Base: Cinza-Cobalto Estelar (#888192)
        r = 29.0 + t_base * 109.0
        g = 27.0 + t_base * 104.0
        b = 33.0 + t_base * 116.0
        
        # Fluxo laminar do tribofilme vítreo auto-regenerativo deslizando pela diagonal
        diag_flow = (x_coords * 0.707 + y_coords * 0.707) - tau * 2.8
        flow_wave = np.sin(diag_flow)
        tribofilm = np.clip(flow_wave, 0, 1.0) * (t_base > 0.22)
        
        # Brilho estelar pontual itinerante ("Haynes Stellar Gleam")
        # Centro do foco estelar viajando na superfície
        pos_x = 4.0 + 8.0 * (0.5 + 0.5 * np.cos(tau))
        pos_y = 4.0 + 8.0 * (0.5 + 0.5 * np.sin(tau))
        d_gleam = np.sqrt((x_coords - pos_x)**2 + (y_coords - pos_y)**2)
        
        # Difração estelar cruciforme (+)
        gleam_core = np.exp(-(d_gleam**2) / 1.5)
        gleam_cross_x = np.exp(-((x_coords - pos_x)**2) / 0.6) * np.exp(-((y_coords - pos_y)**2) / 8.0)
        gleam_cross_y = np.exp(-((y_coords - pos_y)**2) / 0.6) * np.exp(-((x_coords - pos_x)**2) / 8.0)
        stellar_gleam = (gleam_core * 1.2 + (gleam_cross_x + gleam_cross_y) * 0.8) * (t_base > 0.25)
        
        # Realce lilás-prateado do tribofilme vítreo
        r += tribofilm * 55.0
        g += tribofilm * 52.0
        b += tribofilm * 75.0
        
        # Brilho estelar incandescente puro nos raios de difração
        r += stellar_gleam * 110.0
        g += stellar_gleam * 110.0
        b += stellar_gleam * 125.0
        
        flash = np.clip(stellar_gleam - 0.7, 0, 1.5) * 85.0
        r += flash * 1.00
        g += flash * 1.00
        b += flash * 1.00
        
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
    print("Gerando candidatos para Stellite (Co₉Cr₉Mn₅Ti₂, #888192)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Tribological Shock Hardening", render_option_1),
        (2, "HCP Stacking & Spinodal Net", render_option_2),
        (3, "Self-Healing Stellar Gleam", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"stellite_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (stellite_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 17, 22, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "STELLITE (Co₉Cr₉Mn₅Ti₂) — 128x128", fill=(226, 232, 240, 255), font=font_title)
    draw.text((pad_x, 38), "Wear-Resistant Cobalt Superalloy • 4,310K EBF • EV Tier • #888192 • 30 Frames", fill=(167, 139, 250, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Tribological Shock",
        "OPÇÃO 2: HCP Spinodal Net",
        "OPÇÃO 3: Stellar Gleam Flow"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(243, 244, 246, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(196, 181, 253, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (30, 28, 38) if (bx // 16 + by // 16) % 2 == 0 else (22, 20, 28)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(167, 139, 250, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "stellite_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stellite — 3 Opções Visuais & Shaders Tribológicos</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #09080c;
      color: #f3f4f6;
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
      background: linear-gradient(135deg, #221c2c 0%, #14111c 60%, #09080c 100%);
      border: 1px solid rgba(167, 139, 250, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(10, 8, 14, 0.7), 0 0 25px rgba(167, 139, 250, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(167, 139, 250, 0.2);
      color: #ddd6fe;
      border: 1px solid rgba(167, 139, 250, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #c4b5fd;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #ddd6fe, #a78bfa);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #a78bfa;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #15121c;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #2e263c;
    }}
    .btn-toggle {{
      background: #6d28d9;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(109, 40, 217, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #7c3aed;
    }}
    .btn-toggle.active {{
      background: #a855f7;
      color: #0f071d;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(168, 85, 247, 0.7);
    }}
    .status-text {{
      font-size: 12px;
      font-weight: 600;
      color: #7c3aed;
    }}
    .status-text.active {{
      color: #ddd6fe;
      text-shadow: 0 0 8px rgba(196, 181, 253, 0.5);
    }}
    
    .shape-bar {{
      background: #120f18;
      border: 1px solid #262032;
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
      background: #0c0a10;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #221d2e;
    }}
    .btn-shape {{
      background: transparent;
      color: #a78bfa;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #6d28d9;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ddd6fe;
      background: #241d32;
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
      background: #0f0d14;
      border: 2px solid #241d30;
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
      border-color: rgba(167, 139, 250, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #a855f7;
      box-shadow: 0 0 24px rgba(168, 85, 247, 0.35);
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
      background: rgba(167, 139, 250, 0.2);
      color: #ddd6fe;
      border: 1px solid rgba(167, 139, 250, 0.4);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #a78bfa;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #070609;
      border: 1px solid #1c1726;
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
    
    /* SHADER 1: Tribological Kinetic Impact Halo */
    @keyframes shockHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(167, 139, 250, 0.75)) 
          drop-shadow(0 0 18px rgba(221, 214, 254, 0.5)) 
          drop-shadow(0 0 30px rgba(109, 40, 217, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(196, 181, 253, 0.85)) 
          drop-shadow(0 0 42px rgba(167, 139, 250, 0.7));
        transform: scale(1.025);
      }}
    }}
    .halo-active-1 {{
      animation: shockHaloPulse 2.1s ease-in-out infinite;
    }}
    
    /* SHADER 2: Spinodal Crystallographic Moiré Corona */
    @keyframes spinodalMoiréPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(192, 132, 252, 0.8)) 
          drop-shadow(0 0 18px rgba(167, 139, 250, 0.55)) 
          drop-shadow(0 0 32px rgba(147, 51, 234, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 15px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 26px rgba(233, 213, 255, 0.85)) 
          drop-shadow(0 0 44px rgba(192, 132, 252, 0.75));
        transform: scale(1.02);
      }}
    }}
    .halo-active-2 {{
      animation: spinodalMoiréPulse 2.3s ease-in-out infinite;
    }}
    
    /* SHADER 3: Haynes Stellar Nova Diffraction Halo */
    @keyframes stellarGleamPulse {{
      0%, 75% {{
        filter: 
          drop-shadow(0 0 6px rgba(167, 139, 250, 0.6)) 
          drop-shadow(0 0 14px rgba(109, 40, 217, 0.4));
        transform: scale(1);
      }}
      80% {{
        filter: 
          drop-shadow(0 0 20px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 36px rgba(221, 214, 254, 0.95)) 
          drop-shadow(0 0 52px rgba(168, 85, 247, 0.85));
        transform: scale(1.035);
      }}
      90% {{
        filter: 
          drop-shadow(0 0 10px rgba(196, 181, 253, 0.75)) 
          drop-shadow(0 0 22px rgba(167, 139, 250, 0.5));
        transform: scale(1.01);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 6px rgba(167, 139, 250, 0.6)) 
          drop-shadow(0 0 14px rgba(109, 40, 217, 0.4));
        transform: scale(1);
      }}
    }}
    .halo-active-3 {{
      animation: stellarGleamPulse 2.0s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
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
      background: #241b33;
      color: #ddd6fe;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}
    .btn-approve:hover {{
      background: #6d28d9;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(168, 85, 247, 0.5);
    }}
    
    .features-list {{
      list-style: none;
      font-size: 11px;
      color: #9333ea;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 6px;
    }}
    .features-list li::before {{
      content: "▹ ";
      color: #c084fc;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">GTNA Material Set Showcase</span>
        <span class="formula-tag">Co₉Cr₉Mn₅Ti₂</span>
        <h1>Stellite</h1>
        <p class="subtitle">Superliga de Cobalto de Altíssima Dureza Tribológica • 4,310K EBF • EV Tier • 30 Frames Fluídos</p>
      </div>
      <div class="shader-control">
        <button id="btnShader" class="btn-toggle active" onclick="toggleShader()">Shader: ATIVO</button>
        <span id="shaderStatus" class="status-text active">Halo & Corona Dinâmicos</span>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 12px; font-weight: 700; color: #ddd6fe;">Formas do Conjunto de Texturas:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
      <div style="font-size: 11px; color: #a78bfa;">Zoom 8× nativo (128×128 pixel art fiel)</div>
    </div>
    
    <div class="grid-options">
      
      <!-- Opção 1 -->
      <div class="card" id="card1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 10px; color: #a78bfa;">Transformação Martensítica</span>
          </div>
          <div class="card-title">Tribological Shock Hardening</div>
          <div class="card-desc">
            Endurecimento sob impacto severo via transformação de fase martensítica (FCC → HCP): ondas de choque compressivas em anéis elípticos concêntricos com ancoramento de discordâncias.
          </div>
          <ul class="features-list">
            <li>Matriz de aço-cobalto acetinada (#888192)</li>
            <li>Ondas de choque compressivo em violeta-platina</li>
            <li>Flashes estelares nos nós de relaxamento compressivo</li>
            <li><strong>Shader:</strong> Tribological Kinetic Impact Halo</li>
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
            <span style="font-size: 10px; color: #a78bfa;">Decomposição Espinodal</span>
          </div>
          <div class="card-title">HCP Stacking & Spinodal Net</div>
          <div class="card-desc">
            Rede hexagonal de falhas de empilhamento HCP (60°) com decomposição espinodal periódica (flutuações senoidais de Co-Cr-Mn) e franjas de interferência Moiré cristalográfica.
          </div>
          <ul class="features-list">
            <li>Estrias hexagonais entrelaçadas em contra-fase suave</li>
            <li>Contraste marcante entre fases ricas em cobalto e cromo</li>
            <li>Picos de difração nos cruzamentos das falhas de empilhamento</li>
            <li><strong>Shader:</strong> Spinodal Crystallographic Moiré Corona</li>
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
            <span style="font-size: 10px; color: #a78bfa;">Tribofilme & Brilho Estelar</span>
          </div>
          <div class="card-title">Self-Healing Stellar Gleam</div>
          <div class="card-desc">
            Fluxo laminar de tribofilme vítreo auto-regenerativo de atrito quase-zero a 4310K, com brilho estelar itinerante cruciforme de difração óptica ("Haynes Stellar Gleam").
          </div>
          <ul class="features-list">
            <li>Fluxo laminar vítreo em onda suave lilás-prateada</li>
            <li>Ponto de brilho estelar itinerante com difração em cruz (+)</li>
            <li>Realces de alta pureza ótica em diamante e cobalto</li>
            <li><strong>Shader:</strong> Haynes Stellar Nova Diffraction Halo</li>
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
    
    showcase_path = ARTIFACT_DIR / "stellite_showcase.html"
    showcase_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {showcase_path}")
    print("\nTodos os artefatos para Stellite foram gerados com sucesso!")

if __name__ == "__main__":
    main()
