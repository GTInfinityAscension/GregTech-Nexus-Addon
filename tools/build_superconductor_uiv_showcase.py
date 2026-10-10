#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Superconductor Base UIV
Fórmula: (C₁₄Os₁₁O₇Ag₃SpH₂O)₄?₁ • Cor: #E558B1 (Magenta Cósmico Supercondutor)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/superconductor_uiv_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (229, 88, 177, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (229, 88, 177, 255))

# =========================================================================
# Opção 1: Abrikosov Flux Vortex Pinning Lattice (Rede Triangular de Vórtices)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Rede triangular de vórtices de Abrikosov (simetria hexagonal)
    # Vetores de rede: a1 = (1, 0), a2 = (0.5, sqrt(3)/2)
    s3 = 1.73205
    u1 = x_coords * 0.9 + y_coords * 0.52
    u2 = x_coords * 0.9 - y_coords * 0.52
    u3 = y_coords * 1.04
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Magenta profundo / Ameixa supercondutora (#E558B1)
        r = 45.0 + t_base * 184.0
        g = 12.0 + (t_base ** 1.3) * 76.0
        b = 35.0 + (t_base ** 1.1) * 142.0
        
        # Vórtices quantizados de fluxo magnético precessando na rede triangular
        v1 = np.abs(np.sin(u1 * 0.8 + tau))
        v2 = np.abs(np.sin(u2 * 0.8 - tau * 0.5))
        v3 = np.abs(np.sin(u3 * 0.8 + tau * 0.5))
        
        vortex_lattice = (v1 * v2 * v3) ** 2.2 * 3.5 * (t_base > 0.25)
        
        # Supercorrentes perpétuas circulando ao redor dos núcleos de vórtice
        shield_current = np.sin((v1 + v2 + v3) * 3.0 + tau * 2.0) * 0.5 + 0.5
        supercurrent = (shield_current ** 3.0) * (t_base > 0.3) * 0.9
        
        total_fx = vortex_lattice * 0.9 + supercurrent * 0.8
        
        # Brilho eletromagnético neon magenta / violeta quântico
        r += total_fx * 85.0
        g += total_fx * 25.0
        b += total_fx * 65.0
        
        # Flashes brancos puros nos pontos singulares de fluxo magnético nulo
        flash = np.clip(vortex_lattice - 0.75, 0, 1.4) * 95.0
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
# Opção 2: Topological Cooper-Pair Soliton Wave (Sólitons de Pares de Cooper)
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
        
        # Paleta Base: Fúcsia-magenta quântico com sombras violeta escura
        r = 42.0 + t_base * 187.0
        g = 10.0 + (t_base ** 1.35) * 78.0
        b = 38.0 + (t_base ** 1.05) * 139.0
        
        # Propagação de sóliton hiperbólico (sech^2) através de junções topológicas
        # Duas frentes solitônicas em contra-propagação com interferência SQUID
        pos1 = -5.0 + t * 26.0
        pos2 = 21.0 - t * 26.0
        
        dist_s1 = (x_coords * 0.8 + y_coords * 0.6) - pos1
        dist_s2 = (x_coords * 0.6 - y_coords * 0.8) - (pos2 - 8.0)
        
        soliton1 = 1.0 / (np.cosh(dist_s1 / 1.4) ** 2)
        soliton2 = 1.0 / (np.cosh(dist_s2 / 1.4) ** 2)
        
        # Junção quântica de Josephson: interferência não-linear de fase
        josephson = np.sin(dist_s1 * 1.5) * np.cos(dist_s2 * 1.5) * (soliton1 + soliton2)
        
        total_soliton = (soliton1 * 1.1 + soliton2 * 0.9 + np.clip(josephson, 0, 1) * 1.2) * (t_base > 0.22)
        
        # Emissão de energia de par de Cooper: rosa elétrico e magenta neon
        r += total_soliton * 80.0
        g += total_soliton * 20.0
        b += total_soliton * 75.0
        
        # Picos de tunelamento coerente branco-solar
        tunnel_flash = np.clip(total_soliton - 0.7, 0, 1.5) * 90.0
        r += tunnel_flash * 1.00
        g += tunnel_flash * 0.94
        b += tunnel_flash * 0.98
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Phonon-Polariton Standing Wave Resonance (Ressonância Polaritônica)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    # Coordenadas polares para ressonância modal anisotrópica
    r_dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    theta = np.arctan2(y_coords - cy, x_coords - cx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Orquídea imperial / Magenta eletrodinâmico
        r = 46.0 + t_base * 183.0
        g = 14.0 + (t_base ** 1.3) * 74.0
        b = 36.0 + (t_base ** 1.1) * 141.0
        
        # Modos estacionários hiperbólicos de polaritons (ordem quádrupla cos(4*theta))
        mode_anisotropy = np.cos(4.0 * theta)
        radial_standing = np.sin(r_dist * 1.5 - tau) * np.cos(r_dist * 0.8 + tau)
        
        polariton_wave = (radial_standing * (1.0 + 0.35 * mode_anisotropy))
        wave_crests = np.exp(-((polariton_wave - 0.6) / 0.35)**2) * (t_base > 0.28)
        
        # Fônons ópticos no esqueleto de ósmio-carbono: cintilação de micro-cristal
        phonon_lattice = np.sin(x_coords * 2.2 + tau) * np.sin(y_coords * 2.2 - tau)
        phonon_nodes = np.clip(phonon_lattice, 0, 1.0) * (t_base > 0.35) * 0.7
        
        total_resonance = (wave_crests * 1.1 + phonon_nodes * 0.8) * (t_base > 0.25)
        
        # Cores neon: magenta vibrante e rosa-cristalino
        r += total_resonance * 85.0
        g += total_resonance * 22.0
        b += total_resonance * 70.0
        
        # Brilho de transição supercondutora de fase pura
        phase_flash = np.clip(total_resonance - 0.75, 0, 1.4) * 95.0
        r += phase_flash * 0.99
        g += phase_flash * 0.95
        b += phase_flash * 1.00
        
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
    print("Gerando candidatos para Superconductor Base UIV (#E558B1)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Abrikosov Flux Vortex", render_option_1),
        (2, "Topological Soliton Wave", render_option_2),
        (3, "Phonon-Polariton Resonance", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"sc_uiv_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (superconductor_uiv_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo roxo-magenta escuro cósmico
    grid_img = Image.new("RGBA", (grid_w, grid_h), (20, 10, 18, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "SUPERCONDUCTOR BASE UIV — VISUAL CANDIDATES (128x128)", fill=(244, 114, 182, 255), font=font_title)
    draw.text((pad_x, 38), "(C14Os11O7Ag3SpH2O)4?1 • Quantum Meissner Superconductor • #E558B1 • 30 Frames", fill=(216, 180, 254, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Abrikosov Lattice",
        "OPÇÃO 2: Cooper Soliton",
        "OPÇÃO 3: Polariton Standing"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(253, 242, 248, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(244, 114, 182, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (32, 16, 30) if (bx // 16 + by // 16) % 2 == 0 else (24, 12, 22)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(244, 114, 182, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "superconductor_uiv_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Superconductor Base UIV — Avaliação de 3 Opções Visuais</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0d060c;
      color: #fdf2f8;
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
      background: linear-gradient(135deg, #2d0b24 0%, #1a0615 60%, #0d060c 100%);
      border: 1px solid rgba(229, 88, 177, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(229, 88, 177, 0.25), 0 0 20px rgba(229, 88, 177, 0.15);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(229, 88, 177, 0.2);
      color: #f472b6;
      border: 1px solid rgba(229, 88, 177, 0.45);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #fbcfe8;
      font-family: monospace;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #f472b6, #e558b1);
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
      background: #190a16;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #3d1235;
    }}
    .btn-toggle {{
      background: #e558b1;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(229, 88, 177, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #f472b6;
    }}
    .btn-toggle.active {{
      background: #f43f5e;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(244, 63, 94, 0.7);
    }}
    
    .shape-bar {{
      background: #180915;
      border: 1px solid #35102e;
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
      background: #0d040b;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #35102e;
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
      background: #e558b1;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(229, 88, 177, 0.5);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #35102e;
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
      background: #160813;
      border: 2px solid #33102c;
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
      border-color: rgba(229, 88, 177, 0.5);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #f472b6;
      box-shadow: 0 0 24px rgba(229, 88, 177, 0.35);
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
      background: rgba(229, 88, 177, 0.2);
      color: #f472b6;
      border: 1px solid rgba(229, 88, 177, 0.35);
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
      background: #0a0409;
      border: 1px solid #2a0c24;
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
    
    /* SHADER INOVADOR: Quantum Meissner Levitation Aura */
    @keyframes scUivHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(229, 88, 177, 0.9)) 
          drop-shadow(0 0 20px rgba(244, 114, 182, 0.55)) 
          drop-shadow(0 0 32px rgba(192, 132, 252, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(244, 63, 94, 0.85)) 
          drop-shadow(0 0 42px rgba(244, 114, 182, 0.6));
        transform: scale(1.02);
      }}
    }}
    .halo-active {{
      animation: scUivHaloPulse 2.3s ease-in-out infinite;
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
      background: #280e23;
      color: #fbcfe8;
    }}
    .btn-approve:hover {{
      background: #e558b1;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(229, 88, 177, 0.4);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #f472b6, #e558b1);
      color: #1a0615;
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
      background: #240c1f;
      color: #fbcfe8;
      border: 1px solid #3d1235;
    }}
    
    .footer-box {{
      background: #180915;
      border: 1px solid #35102e;
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
          <span class="badge">Supercondutor Tier UIV</span>
          <span class="formula-tag">(C₁₄Os₁₁O₇Ag₃SpH₂O)₄?₁ • #E558B1</span>
        </div>
        <h1>Superconductor Base UIV — 3 Físicas Quânticas & Shaders</h1>
        <p class="subtitle">
          Supercondutor UIV de resistência zero absoluta e confinamento topológico. 3 dinâmicas quânticas combinadas com o <strong>Quantum Meissner Levitation Aura</strong>.
        </p>
      </div>

      <div class="shader-control">
        <div>
          <div style="font-size:10px; text-transform:uppercase; color:#cbd5e1;">Simulador In-Game</div>
          <div id="shaderStatusText" style="font-size:12px; font-weight:800; color:#f472b6;">✨ MEISSNER HALO ATIVADO</div>
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
            <span style="font-size:11px; color:#94a3b8;">Vórtices de Abrikosov</span>
          </div>
          <div class="card-title">Abrikosov Flux Vortex Lattice</div>
          <p class="card-desc">
            Rede triangular periódica de <strong>vórtices magnéticos quantizados de Abrikosov</strong> (flux pinning) precessando suavemente. Supercorrentes de blindagem perpétua circulam ao redor de cada vórtice com flashes de aniquilação nos núcleos normais.
          </p>
          <div class="features-list">
            <span class="feature-item">Rede Triangular de Vórtices</span>
            <span class="feature-item">Supercorrentes Perpétuas</span>
            <span class="feature-item">Flux Pinning Quântico</span>
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
            <span style="font-size:11px; color:#94a3b8;">Sólitons de Cooper</span>
          </div>
          <div class="card-title">Topological Cooper-Pair Soliton Wave</div>
          <p class="card-desc">
            Ondas de <strong>sólitons hiperbólicos (sech²) de Pares de Cooper</strong> deslizando através de junções de Josephson topológicas sem dissipação. A interferência quântica SQUID gera focos pulsantes de coerência de fase em rosa-solar.
          </p>
          <div class="features-list">
            <span class="feature-item">Sólitons Hiperbólicos (sech²)</span>
            <span class="feature-item">Junções de Josephson</span>
            <span class="feature-item">Interferência de Fase SQUID</span>
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
            <span style="font-size:11px; color:#94a3b8;">Fônons-Polaritons</span>
          </div>
          <div class="card-title">Phonon-Polariton Standing Waves</div>
          <p class="card-desc">
            Acoplamento óptico-eletrônico ressonante entre <strong>fônons do esqueleto orgânico-metálico de Ósmio</strong> e polaritons eletromagnéticos. Ondas estacionárias hiperbólicas com simetria quádrupla cos(4θ) respiram ritmicamente nas facetas.
          </p>
          <div class="features-list">
            <span class="feature-item">Simetria Quádrupla cos(4θ)</span>
            <span class="feature-item">Esqueleto Ósmio-Carbono</span>
            <span class="feature-item">Ressonância Modal 2D</span>
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
        Qual das 3 opções você prefere aprovar para o <strong>Superconductor Base UIV</strong>?
      </div>
      <div style="font-weight:700; color:#f472b6;">
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
        statusText.innerText = "✨ MEISSNER HALO ATIVADO";
        statusText.style.color = "#f472b6";
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
    html_path = ARTIFACT_DIR / "superconductor_uiv_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase interativo salvo em: {html_path}")
    print("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
