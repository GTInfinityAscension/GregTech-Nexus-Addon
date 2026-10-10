#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Indalloy 140
Fórmula: In₂PbAg (Eutectic Quantum Solder Alloy)
Cor: #6a5acd / #93c5fd / #a855f7 (Azul-Ardósia Slate Blue, Ciano Elétrico e Violeta Quântico)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/indalloy140_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (106, 90, 205, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (106, 90, 205, 255))

# =========================================================================
# Opção 1: Eutectic Capillary Marangoni Convection & Wetting Fronts
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
        
        # Paleta Base: Azul-Ardósia Slate Blue (#6a5acd)
        r = 22.0 + t_base * 84.0
        g = 18.0 + t_base * 72.0
        b = 42.0 + t_base * 163.0
        
        # Frentes capilares com instabilidade de Saffman-Taylor (dedos de Marangoni)
        fingering = np.cos(5.0 * angle + np.sin(dist * 0.8 - tau * 2.0)) * 1.2
        marangoni_wave = np.sin(dist * 1.3 - tau * 2.5 + fingering)
        wetting = np.clip(marangoni_wave, 0, 1.0) * (t_base > 0.22)
        
        # Meniscos capilares de alta tensão superficial nos pontos de contato
        meniscus = np.exp(-((marangoni_wave - 0.75)**2) / 0.08) * (t_base > 0.25)
        
        # Realce azul-ciano elétrico de molhamento
        r += wetting * 45.0
        g += wetting * 75.0
        b += wetting * 85.0
        
        # Brilho de menisco em prata-índio pura
        r += meniscus * 85.0
        g += meniscus * 92.0
        b += meniscus * 98.0
        
        # Flashes nos vértices do menisco capilar
        flash = np.clip(meniscus - 0.72, 0, 1.5) * 100.0
        r += flash * 0.95
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
# Opção 2: Cryogenic Superconducting Josephson Vortex Lattice
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
        
        # Paleta Base: Ardósia Criogênica Profunda (#6a5acd)
        r = 20.0 + t_base * 86.0
        g = 16.0 + t_base * 74.0
        b = 45.0 + t_base * 160.0
        
        # Rede triangular de vórtices de Josephson (passos de Shapiro quânticos)
        v1 = np.sin((x_coords * 1.1 + y_coords * 0.65) - tau * 2.2)
        v2 = np.sin((-x_coords * 0.65 + y_coords * 1.1) + tau * 2.2)
        v3 = np.cos((x_coords * 0.9 - y_coords * 0.9) - tau * 1.5)
        
        vortex_lattice = np.clip((v1 * v2 + v2 * v3) * 1.2, 0, 1.2) * (t_base > 0.22)
        
        # Nós de tunelamento quântico com salto de fase (phase-slip centers)
        phase_slip = np.exp(-((v1**2 + v2**2 + v3**2) / 0.45)) * (t_base > 0.25)
        
        # Realce violeta-quântico ao longo das supercorrentes de Josephson
        r += vortex_lattice * 68.0
        g += vortex_lattice * 55.0
        b += vortex_lattice * 95.0
        
        # Centros de salto de fase em platina-índigo incandescente
        r += phase_slip * 95.0
        g += phase_slip * 95.0
        b += phase_slip * 105.0
        
        # Flashes estocásticos de tunelamento de Cooper
        flash = np.clip(phase_slip - 0.68, 0, 1.6) * 110.0
        r += flash * 0.92
        g += flash * 0.95
        b += flash * 1.00
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Interfacial Intermetallic IMC Whisker Growth & Solute Micro-Segregation
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Eixos ortogonais de difusão de soluto (0° e 90°)
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Ardósia-Prata (#6a5acd)
        r = 23.0 + t_base * 83.0
        g = 19.0 + t_base * 71.0
        b = 40.0 + t_base * 164.0
        
        # Crescimento de whiskers monocristalinos intermetálicos dirigidos por compressão
        whisker_x = np.exp(-((np.abs((x_coords - tau * 1.5) % 4.0 - 2.0))**2) / 0.25)
        whisker_y = np.exp(-((np.abs((y_coords + tau * 1.2) % 4.0 - 2.0))**2) / 0.25)
        whiskers = (whisker_x + whisker_y) * (t_base > 0.24)
        
        # Ondas cruzadas de micro-segregação de soluto de In-Sn
        solute_wave = np.sin(x_coords * 0.9 - y_coords * 0.9 - tau * 2.5)
        solute = np.clip(solute_wave, 0, 1.0) * (t_base > 0.22)
        
        # Realce violeta e ciano nas frentes de soluto
        r += solute * 45.0
        g += solute * 62.0
        b += solute * 85.0
        
        # Reflexos especulares agudos em prata pura ao longo das agulhas
        r += whiskers * 92.0
        g += whiskers * 95.0
        b += whiskers * 105.0
        
        flash = np.clip(whiskers * solute - 0.45, 0, 1.5) * 95.0
        r += flash * 0.96
        g += flash * 0.98
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
    print("Gerando candidatos para Indalloy 140 (In₂PbAg, #6a5acd)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Capillary Marangoni Fronts", render_option_1),
        (2, "Josephson Vortex Lattice", render_option_2),
        (3, "IMC Whiskers & Solute Segregation", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"indalloy_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (indalloy_140_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (14, 13, 24, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "INDALLOY 140 (In₂PbAg) — 128x128", fill=(224, 231, 255, 255), font=font_title)
    draw.text((pad_x, 38), "Eutectic Quantum Solder • 2,600K EBF • EV Tier • #6a5acd • 30 Frames", fill=(129, 140, 248, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Marangoni Fronts",
        "OPÇÃO 2: Josephson Lattice",
        "OPÇÃO 3: Whisker Growth"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(238, 242, 255, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(165, 180, 252, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (26, 24, 44) if (bx // 16 + by // 16) % 2 == 0 else (18, 16, 32)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(129, 140, 248, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "indalloy_140_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Indalloy 140 — 3 Opções Visuais & Shaders Eutéticos</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #07060e;
      color: #eef2ff;
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
      background: linear-gradient(135deg, #1e1b4b 0%, #111029 60%, #07060e 100%);
      border: 1px solid rgba(129, 140, 248, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(8, 7, 18, 0.7), 0 0 25px rgba(129, 140, 248, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(129, 140, 248, 0.2);
      color: #c7d2fe;
      border: 1px solid rgba(129, 140, 248, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #93c5fd;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #c7d2fe, #818cf8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #818cf8;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #100f24;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #232048;
    }}
    .btn-toggle {{
      background: #4338ca;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(67, 56, 202, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #4f46e5;
    }}
    .btn-toggle.active {{
      background: #6366f1;
      color: #0c0a1f;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(99, 102, 241, 0.7);
    }}
    .status-text {{
      font-size: 12px;
      font-weight: 600;
      color: #6366f1;
    }}
    .status-text.active {{
      color: #c7d2fe;
      text-shadow: 0 0 8px rgba(199, 210, 254, 0.5);
    }}
    
    .shape-bar {{
      background: #0d0c1c;
      border: 1px solid #1f1d3e;
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
      background: #080712;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1c1a38;
    }}
    .btn-shape {{
      background: transparent;
      color: #818cf8;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #4338ca;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #c7d2fe;
      background: #1c1942;
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
      background: #0c0b1a;
      border: 2px solid #1f1c3d;
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
      border-color: rgba(129, 140, 248, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #6366f1;
      box-shadow: 0 0 24px rgba(99, 102, 241, 0.35);
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
      background: rgba(129, 140, 248, 0.2);
      color: #c7d2fe;
      border: 1px solid rgba(129, 140, 248, 0.4);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #818cf8;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #05040a;
      border: 1px solid #16142c;
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
    
    /* SHADER 1: Capillary Surface-Tension Meniscus Corona */
    @keyframes marangoniCoronaPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(106, 90, 205, 0.8)) 
          drop-shadow(0 0 18px rgba(147, 197, 253, 0.55)) 
          drop-shadow(0 0 30px rgba(99, 102, 241, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(147, 197, 253, 0.85)) 
          drop-shadow(0 0 42px rgba(129, 140, 248, 0.7));
        transform: scale(1.025);
      }}
    }}
    .halo-active-1 {{
      animation: marangoniCoronaPulse 2.2s ease-in-out infinite;
    }}
    
    /* SHADER 2: Josephson Phase-Slip Quantum Corona */
    @keyframes josephsonQuantumPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(99, 102, 241, 0.8)) 
          drop-shadow(0 0 18px rgba(168, 85, 247, 0.6)) 
          drop-shadow(0 0 32px rgba(67, 56, 202, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 18px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(199, 210, 254, 0.9)) 
          drop-shadow(0 0 46px rgba(168, 85, 247, 0.75));
        transform: scale(1.03);
      }}
    }}
    .halo-active-2 {{
      animation: josephsonQuantumPulse 2.0s ease-in-out infinite;
    }}
    
    /* SHADER 3: Interfacial Whisker Field Diffraction Halo */
    @keyframes whiskerDiffractPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 6px rgba(129, 140, 248, 0.7)) 
          drop-shadow(0 0 16px rgba(224, 231, 255, 0.5)) 
          drop-shadow(0 0 28px rgba(79, 70, 229, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 14px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 24px rgba(199, 210, 254, 0.85)) 
          drop-shadow(0 0 38px rgba(129, 140, 248, 0.65));
        transform: scale(1.02);
      }}
    }}
    .halo-active-3 {{
      animation: whiskerDiffractPulse 1.9s ease-in-out infinite;
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
      background: #1c1945;
      color: #c7d2fe;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}
    .btn-approve:hover {{
      background: #4338ca;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(99, 102, 241, 0.5);
    }}
    
    .features-list {{
      list-style: none;
      font-size: 11px;
      color: #6366f1;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 6px;
    }}
    .features-list li::before {{
      content: "▹ ";
      color: #818cf8;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">GTNA Material Set Showcase</span>
        <span class="formula-tag">In₂PbAg</span>
        <h1>Indalloy 140</h1>
        <p class="subtitle">Superliga Eutética de Solda Quântica Criogênica • 2,600K EBF • EV Tier • 30 Frames Fluídos</p>
      </div>
      <div class="shader-control">
        <button id="btnShader" class="btn-toggle active" onclick="toggleShader()">Shader: ATIVO</button>
        <span id="shaderStatus" class="status-text active">Halo & Corona Dinâmicos</span>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 12px; font-weight: 700; color: #c7d2fe;">Formas do Conjunto de Texturas:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
      <div style="font-size: 11px; color: #818cf8;">Zoom 8× nativo (128×128 pixel art fiel)</div>
    </div>
    
    <div class="grid-options">
      
      <!-- Opção 1 -->
      <div class="card" id="card1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 10px; color: #818cf8;">Convecção de Marangoni</span>
          </div>
          <div class="card-title">Capillary Marangoni Fronts</div>
          <div class="card-desc">
            Gradientes térmicos induzem convecção de Marangoni eutética e espalhamento capilar de Saffman-Taylor (dedos de viscosidade) promovendo molhamento molecular perfeito.
          </div>
          <ul class="features-list">
            <li>Matriz clássica azul-ardósia Slate Blue (#6a5acd)</li>
            <li>Frentes capilares em ciano elétrico e prata-índio</li>
            <li>Brilho de menisco ultra-refletivo nos vértices</li>
            <li><strong>Shader:</strong> Capillary Surface-Tension Meniscus Corona</li>
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
            <span style="font-size: 10px; color: #818cf8;">Supercondutividade Quântica</span>
          </div>
          <div class="card-title">Josephson Vortex Lattice</div>
          <div class="card-desc">
            Rede periódica de vórtices supercondutores de Josephson/Abrikosov com precessão quântica de supercorrentes em passos de Shapiro e saltos de fase de tunelamento.
          </div>
          <ul class="features-list">
            <li>Rede triangular de vórtices quânticos em azul-índigo</li>
            <li>Supercorrentes deslizando em contrafase simétrica</li>
            <li>Flashes nos centros de salto de fase (phase-slip centers)</li>
            <li><strong>Shader:</strong> Josephson Phase-Slip Quantum Corona</li>
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
            <span style="font-size: 10px; color: #818cf8;">Crescimento Intermetálico</span>
          </div>
          <div class="card-title">IMC Whiskers & Segregation</div>
          <div class="card-desc">
            Crescimento espontâneo de whiskers intermetálicos monocristalinos dirigidos por alívio de tensões bi-axiais na solda, alimentados por micro-segregação cruzada de In-Sn.
          </div>
          <ul class="features-list">
            <li>Micro-agulhas monocristalinas afiadas em eixos ortogonais</li>
            <li>Ondas diagonais de micro-segregação de soluto de índio</li>
            <li>Reflexos especulares metálicos puros de alta rigidez</li>
            <li><strong>Shader:</strong> Interfacial Whisker Field Diffraction Halo</li>
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
    
    showcase_path = ARTIFACT_DIR / "indalloy140_showcase.html"
    showcase_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {showcase_path}")
    print("\nTodos os artefatos para Indalloy 140 foram gerados com sucesso!")

if __name__ == "__main__":
    main()
