#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Mar-M-200 Steel
Fórmula: Nb₂Cr₉Al₅Ti₂Co₁₀W₁₃Ni₁₈ (8-Element Refractory Superalloy)
Cor: #515151 / #88929E / #38BDF8 (Cinza Aeroespacial, Tungstênio Refratário e Óxido Térmico)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/marm200_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (81, 81, 81, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (81, 81, 81, 255))

# =========================================================================
# Opção 1: Cuboidal γ'-Phase Precipitation Lattice & Orowan Loops
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
        
        # Paleta Base: Cinza Titânico-Aeroespacial (#515151)
        r = 24.0 + t_base * 105.0
        g = 25.0 + t_base * 108.0
        b = 28.0 + t_base * 115.0
        
        # Rede cuboidal ordenada periódica de fase gama-linha (γ')
        cube_x = np.abs((x_coords + tau * 1.5) % 3.5 - 1.75)
        cube_y = np.abs((y_coords - tau * 1.0) % 3.5 - 1.75)
        gamma_cubes = np.exp(-(cube_x**2 + cube_y**2) / 0.8) * (t_base > 0.22)
        
        # Anéis de contorno de Orowan deslizando entre os precipitados
        orowan_loops = np.sin((x_coords * 0.8 + y_coords * 0.8) - tau * 2.5) * np.cos(cube_x - cube_y)
        loops = np.clip(orowan_loops, 0, 1.0) * (t_base > 0.25)
        
        total_precip = gamma_cubes * 1.25 + loops * 0.95
        
        # Realces em prata-tungstênio e cobalto metálico
        r += total_precip * 65.0
        g += total_precip * 70.0
        b += total_precip * 82.0
        
        # Picos nos vértices dos nanocubos
        flash = np.clip(total_precip - 1.1, 0, 1.5) * 95.0
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
# Opção 2: Aerodynamic Thermal Oxidation & Iridescence Sheen
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
        
        # Paleta Base: Cinza Aço Refratário (#515151)
        r = 22.0 + t_base * 102.0
        g = 24.0 + t_base * 106.0
        b = 27.0 + t_base * 114.0
        
        # Frentes de oxidação térmica refratária varrendo a superfície em alta velocidade
        wave_phase = (x_coords * 0.75 - y_coords * 0.45) - tau * 2.0
        irid_film = np.sin(wave_phase)
        
        # Cores de têmpera por interferência de película fina:
        # Azul cobalto/titânio em crista positiva, âmbar de nióbio em crista negativa
        blue_sheen = np.clip(irid_film, 0, 1.0) * (t_base > 0.22)
        amber_sheen = np.clip(-irid_film, 0, 1.0) * (t_base > 0.25)
        
        # Reflexo azul-cobalto aeroespacial
        r += blue_sheen * 35.0
        g += blue_sheen * 65.0
        b += blue_sheen * 95.0
        
        # Reflexo bronze-âmbar de óxido de cromo
        r += amber_sheen * 75.0
        g += amber_sheen * 55.0
        b += amber_sheen * 20.0
        
        # Cristas especulares de reflexão metálica pura
        sheen_flash = np.exp(-((irid_film - 0.7)**2) / 0.12) * (t_base > 0.3)
        flash = np.clip(sheen_flash - 0.3, 0, 1.5) * 85.0
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
# Opção 3: Adiabatic Shear Banding & Dislocation Avalanches
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # 3 planos de clivagem adiabática com ângulos distintos (45°, -30°, 60°)
    shear_lines = [
        (0.707, 0.707, 0.0),
        (0.866, -0.500, 2.09),
        (0.500, 0.866, 4.18)
    ]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Aço-Carbono e Nióbio escuro (#515151)
        r = 23.0 + t_base * 104.0
        g = 24.0 + t_base * 107.0
        b = 26.0 + t_base * 112.0
        
        asb_total = 0.0
        for cos_a, sin_a, phase in shear_lines:
            proj = x_coords * cos_a + y_coords * sin_a
            # Onda de cisalhamento adiabático com disparo rápido e relaxamento térmico
            asb_wave = np.sin(proj * 1.4 - tau * 3.0 + phase)
            burst = np.exp(-((asb_wave - 0.85)**2) / 0.08)
            asb_total += burst
            
        total_shear = asb_total * (t_base > 0.22)
        
        # Brilho de fricção mecânica ultra-rápida em platina-aço
        r += total_shear * 68.0
        g += total_shear * 72.0
        b += total_shear * 85.0
        
        # Picos de temperatura localizada nos planos de escorregamento
        flash = np.clip(total_shear - 1.1, 0, 1.6) * 105.0
        r += flash * 1.00
        g += flash * 0.98
        b += flash * 0.96
        
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
    print("Gerando candidatos para Mar-M-200 Steel (Nb₂Cr₉Al₅Ti₂Co₁₀W₁₃Ni₁₈, #515151)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Cuboidal γ'-Precipitation", render_option_1),
        (2, "Thermal Oxidation Sheen", render_option_2),
        (3, "Adiabatic Shear Bands", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"marm_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (mar_m_200_steel_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo aço aeroespacial escuro
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 20, 24, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "MAR-M-200 STEEL (Nb₂Cr₉Al₅Ti₂Co₁₀W₁₃Ni₁₈) — 128x128", fill=(203, 213, 225, 255), font=font_title)
    draw.text((pad_x, 38), "8-Element Refractory Superalloy • 4,600K EBF • Tier IV • #515151 • 30 Frames", fill=(148, 163, 184, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: γ'-Precipitation",
        "OPÇÃO 2: Thermal Oxidation",
        "OPÇÃO 3: Adiabatic Shear"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(241, 245, 249, 255), font=font_header)
        
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
                    c = (28, 32, 38) if (bx // 16 + by // 16) % 2 == 0 else (20, 24, 30)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(148, 163, 184, 100), width=1)
            
    grid_png_path = ARTIFACT_DIR / "mar_m_200_steel_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mar-M-200 Steel — 3 Opções Visuais & Shaders Refratários</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b0d11;
      color: #f1f5f9;
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
      background: linear-gradient(135deg, #1e242d 0%, #111419 60%, #0b0d11 100%);
      border: 1px solid rgba(148, 163, 184, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.6), 0 0 20px rgba(148, 163, 184, 0.15);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(148, 163, 184, 0.2);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.45);
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
      background: linear-gradient(to right, #ffffff, #cbd5e1, #94a3b8);
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
      background: #11151c;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #1f2530;
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
      box-shadow: 0 4px 12px rgba(71, 85, 105, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #64748b;
    }}
    .btn-toggle.active {{
      background: #38bdf8;
      color: #0b1120;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.7);
    }}
    
    .shape-bar {{
      background: #11141a;
      border: 1px solid #1e2430;
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
      background: #090b0e;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1e2430;
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
      background: #334155;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #1e2430;
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
      background: #0f1218;
      border: 2px solid #1e2430;
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
      border-color: rgba(56, 189, 248, 0.55);
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
      background: rgba(148, 163, 184, 0.18);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.35);
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
      background: #07090c;
      border: 1px solid #171c26;
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
    
    /* SHADER 1: Refractory Coherent Strain Field Halo */
    @keyframes gammaHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(148, 163, 184, 0.75)) 
          drop-shadow(0 0 18px rgba(203, 213, 225, 0.5)) 
          drop-shadow(0 0 30px rgba(71, 85, 105, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 14px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 26px rgba(226, 232, 240, 0.8)) 
          drop-shadow(0 0 40px rgba(148, 163, 184, 0.6));
        transform: scale(1.02);
      }}
    }}
    .halo-active-1 {{
      animation: gammaHaloPulse 2.1s ease-in-out infinite;
    }}
    
    /* SHADER 2: Aerothermal Shockwave Thin-Film Iridescence Corona */
    @keyframes aeroIridPulse {{
      0% {{
        filter: 
          drop-shadow(0 0 8px rgba(56, 189, 248, 0.8)) 
          drop-shadow(0 0 18px rgba(251, 191, 36, 0.6)) 
          drop-shadow(0 0 32px rgba(148, 163, 184, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(56, 189, 248, 0.9)) 
          drop-shadow(0 0 44px rgba(251, 191, 36, 0.75));
        transform: scale(1.025);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 8px rgba(56, 189, 248, 0.8)) 
          drop-shadow(0 0 18px rgba(251, 191, 36, 0.6)) 
          drop-shadow(0 0 32px rgba(148, 163, 184, 0.4));
        transform: scale(1);
      }}
    }}
    .halo-active-2 {{
      animation: aeroIridPulse 2.3s ease-in-out infinite;
    }}
    
    /* SHADER 3: Adiabatic Stress Burst Flare Halo */
    @keyframes asbBurstPulse {{
      0%, 70% {{
        filter: 
          drop-shadow(0 0 6px rgba(148, 163, 184, 0.6)) 
          drop-shadow(0 0 14px rgba(71, 85, 105, 0.4));
        transform: scale(1);
      }}
      75% {{
        filter: 
          drop-shadow(0 0 18px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 32px rgba(241, 245, 249, 0.95)) 
          drop-shadow(0 0 48px rgba(148, 163, 184, 0.8));
        transform: scale(1.03);
      }}
      85% {{
        filter: 
          drop-shadow(0 0 10px rgba(203, 213, 225, 0.7)) 
          drop-shadow(0 0 20px rgba(148, 163, 184, 0.5));
        transform: scale(1.01);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 6px rgba(148, 163, 184, 0.6)) 
          drop-shadow(0 0 14px rgba(71, 85, 105, 0.4));
        transform: scale(1);
      }}
    }}
    .halo-active-3 {{
      animation: asbBurstPulse 1.9s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
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
      background: #1e2430;
      color: #e2e8f0;
    }}
    .btn-approve:hover {{
      background: #38bdf8;
      color: #0b1120;
      box-shadow: 0 4px 14px rgba(56, 189, 248, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #38bdf8, #0284c7);
      color: #0b1120;
      font-weight: 800;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
    }}
    .feat-tag {{
      background: #11151c;
      border: 1px solid #1f2530;
      color: #94a3b8;
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
      border: 1px solid #334155;
      color: #94a3b8;
      font-size: 11px;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-card-shader:hover {{
      background: #1e2430;
      color: #ffffff;
    }}
    .btn-card-shader.active {{
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      color: #7dd3fc;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">8-Element Refractory Superalloy</span>
        <span class="formula-tag">Nb₂Cr₉Al₅Ti₂Co₁₀W₁₃Ni₁₈</span>
        <h1>Mar-M-200 Steel</h1>
        <p class="subtitle">EBF 4,600K • Tier IV • Lâminas de Turbina & Aeroespacial • Paleta #515151 / #88929E</p>
      </div>
      
      <div class="shader-control">
        <div>
          <div style="font-size: 12px; font-weight: 700; color: #ffffff;">Simulador de Shaders</div>
          <div id="shader-status-text" style="font-size: 11px; color: #38bdf8;">Shader Ativo (RenderBlender)</div>
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
            <span style="font-size: 11px; color: #94a3b8;">Física: γ'-Precipitation</span>
          </div>
          <div class="card-title">Cuboidal γ'-Phase Precipitation</div>
          <p class="card-desc">
            Nanoprecipitados cuboidais ordenados de Ni₃(Al,Ti) distribuídos na matriz refratária: anéis de tensão elástica de Orowan deslizam entre os cubos com realces em prata-tungstênio e picos especulares nos vértices dos precipitados.
          </p>
          <div class="features-list">
            <span class="feat-tag">Precipitados Cuboidais γ'</span>
            <span class="feat-tag">Anéis de Orowan</span>
            <span class="feat-tag">Prata-Tungstênio Nobre</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-1" class="pixelated-art halo-active-1" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-1" class="btn-card-shader active" onclick="toggleCardShader(1)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(1)">ESCOLHER OPÇÃO 1 (γ'-PRECIPITATION)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 2</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Thermal Oxidation</span>
          </div>
          <div class="card-title">Aerothermal Oxidation Sheen</div>
          <p class="card-desc">
            Película de passivação térmica refratária de Cr₂O₃/Al₂O₃ sob atrito supersônico a 4.600K: ondas de iridescência de filme fino varrem a superfície em cobalto-azul aeroespacial (#38BDF8) e bronze-âmbar com brilho metálico acetinado.
          </p>
          <div class="features-list">
            <span class="feat-tag">Passivação Refratária Cr₂O₃</span>
            <span class="feat-tag">Iridescência Azul/Âmbar</span>
            <span class="feat-tag">Atrito Hipersônico</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-2" class="pixelated-art halo-active-2" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-2" class="btn-card-shader active" onclick="toggleCardShader(2)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(2)">ESCOLHER OPÇÃO 2 (THERMAL SHEEN)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 3</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Adiabatic Shear</span>
          </div>
          <div class="card-title">Adiabatic Shear Banding</div>
          <p class="card-desc">
            Bandas de cisalhamento adiabático (ASB) ao longo de 3 planos cristalográficos de clivagem: avalanches de discordância rompem barreiras de grão com fendas de deformação relampejantes de alta velocidade e picos térmicos localizados.
          </p>
          <div class="features-list">
            <span class="feat-tag">3 Planos de Clivagem</span>
            <span class="feat-tag">Avalanches de Discordância</span>
            <span class="feat-tag">Picos Térmicos Instantâneos</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-3" class="pixelated-art halo-active-3" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-3" class="btn-card-shader active" onclick="toggleCardShader(3)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(3)">ESCOLHER OPÇÃO 3 (SHEAR BANDS)</button>
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
        text.style.color = '#38bdf8';
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
    
    html_path = ARTIFACT_DIR / "marm200_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
