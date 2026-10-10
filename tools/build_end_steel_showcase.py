#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para End Steel
Fórmula: St₄E (Ender-Infused Vacuum Resistant Superalloy)
Cor: #d6d980 / #8b5cf6 / #fef08a (Ouro-Espectral do Endstone, Violeta Dimensional e Vácuo Puro)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/end_steel_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (214, 217, 128, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (214, 217, 128, 255))

# =========================================================================
# Opção 1: Dimensional Vacuum Polarization & Spacetime Pinning
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
        
        # Paleta Base: Ouro-Espectral de Endstone (#d6d980)
        r = 42.0 + t_base * 172.0
        g = 45.0 + t_base * 172.0
        b = 20.0 + t_base * 108.0
        
        # Planos de onda de polarização do vácuo dimensional (30° e -60°)
        p1 = np.sin((x_coords * 0.866 + y_coords * 0.5) - tau * 2.2)
        p2 = np.sin((x_coords * 0.5 - y_coords * 0.866) + tau * 2.2)
        
        vacuum_wave = (p1 + p2) * 0.6
        polarize = np.clip(vacuum_wave, 0, 1.0) * (t_base > 0.22)
        
        # Nós de ancoramento de espaço-tempo (spacetime pinning)
        pinning = np.exp(-((vacuum_wave - 0.72)**2) / 0.09) * (t_base > 0.25)
        
        # Fendas de obsidiana/vácuo com desvio gravitacional para o violeta do End
        void_fringe = np.clip(-vacuum_wave, 0, 1.0) * (t_base > 0.24)
        r += void_fringe * 25.0
        g += void_fringe * 8.0
        b += void_fringe * 65.0
        
        # Realce ouro-espectral nas frentes de polarização
        r += polarize * 45.0
        g += polarize * 48.0
        b += polarize * 15.0
        
        # Flashes brancos de ancoramento dimensional puro
        flash = np.clip(pinning - 0.7, 0, 1.5) * 95.0
        r += flash * 1.00
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
# Opção 2: Non-Euclidean Hyperbolic Tessellation & Ender Resonances
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dx = (x_coords - cx) / 7.5
    dy = (y_coords - cy) / 7.5
    r_sq = dx**2 + dy**2
    # Métrica de Poincaré conformada
    r_hyp = 2.0 * np.sqrt(r_sq) / np.maximum(0.1, 1.0 - r_sq * 0.6)
    theta = np.arctan2(dy, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Amarelo-Verde Pálido (#d6d980)
        r = 40.0 + t_base * 174.0
        g = 43.0 + t_base * 174.0
        b = 18.0 + t_base * 110.0
        
        # Tesselação hiperbólica {7,3} deformada derivando angularmente
        tess = np.sin(7.0 * theta + r_hyp * 2.0 - tau * 2.5) * np.cos(r_hyp * 1.5 + tau * 1.5)
        hyp_rings = np.clip(tess, 0, 1.2) * (t_base > 0.22)
        
        # Vórtices de ressonância de Poincaré
        poincare_core = np.exp(-((r_hyp - 1.2 - 0.5 * np.sin(tau * 2.0))**2) / 0.15) * (t_base > 0.25)
        
        # Realce ouro-espectral
        r += hyp_rings * 50.0
        g += hyp_rings * 52.0
        b += hyp_rings * 20.0
        
        # Vórtices violeta-obsidiana hiperbólicos
        r += poincare_core * 60.0
        g += poincare_core * 30.0
        b += poincare_core * 90.0
        
        # Flashes estelares nos nós de Poincaré
        flash = np.clip(hyp_rings * poincare_core - 0.35, 0, 1.6) * 110.0
        r += flash * 1.00
        g += flash * 1.00
        b += flash * 0.90
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Quantum Teleportation Flux Filaments & Entanglement Drift
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Família de 3 micro-wormholes helicoidais de Einstein-Rosen
    filaments = [
        (1.2, 0.8, 0.0),
        (0.6, 1.4, 2.09),
        (-1.0, 1.0, 4.18)
    ]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Amarelo Ouro-Espectral (#d6d980)
        r = 44.0 + t_base * 170.0
        g = 46.0 + t_base * 171.0
        b = 22.0 + t_base * 106.0
        
        wormhole_total = 0.0
        for kx, ky, phase in filaments:
            fil_wave = np.sin((x_coords * kx + y_coords * ky) - tau * 3.5 + phase)
            burst = np.exp(-((fil_wave - 0.85)**2) / 0.07)
            wormhole_total += burst
            
        teleport = wormhole_total * (t_base > 0.22)
        
        # Salto quântico de emaranhamento (flash estocástico superluminal)
        step_phase = (f * 7) % 30
        quantum_jump = np.exp(-((x_coords - step_phase * 0.5)**2 + (y_coords - (30 - step_phase) * 0.5)**2) / 2.0) * (t_base > 0.25)
        
        # Realce violeta-esmeralda do túnel quântico
        r += teleport * 42.0
        g += teleport * 46.0
        b += teleport * 75.0
        
        # Flashes instantâneos do salto de teleportação
        r += quantum_jump * 115.0
        g += quantum_jump * 115.0
        b += quantum_jump * 125.0
        
        flash = np.clip(teleport - 1.1, 0, 1.5) * 85.0
        r += flash * 1.00
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
    print("Gerando candidatos para End Steel (St₄E, #d6d980)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Vacuum Polarization & Pinning", render_option_1),
        (2, "Hyperbolic Poincaré Tessellation", render_option_2),
        (3, "Quantum Teleportation Wormholes", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"end_steel_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (end_steel_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (20, 22, 14, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "END STEEL (St₄E) — 128x128", fill=(254, 240, 138, 255), font=font_title)
    draw.text((pad_x, 38), "Vacuum Resistant Ender Superalloy • 3,250K EBF • HV Tier • #d6d980 • 30 Frames", fill=(202, 138, 4, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Vacuum Pinning",
        "OPÇÃO 2: Poincaré Tessellation",
        "OPÇÃO 3: Teleport Wormholes"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(254, 252, 232, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(234, 179, 8, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (32, 36, 22) if (bx // 16 + by // 16) % 2 == 0 else (24, 28, 16)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(202, 138, 4, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "end_steel_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>End Steel — 3 Opções Visuais & Shaders do Vácuo</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0a0c06;
      color: #fefce8;
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
      background: linear-gradient(135deg, #242912 0%, #131709 60%, #0a0c06 100%);
      border: 1px solid rgba(234, 179, 8, 0.45);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(12, 14, 6, 0.7), 0 0 25px rgba(234, 179, 8, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(234, 179, 8, 0.2);
      color: #fef08a;
      border: 1px solid rgba(234, 179, 8, 0.5);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #facc15;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #fef08a, #ca8a04);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 13px;
      color: #ca8a04;
      margin-top: 4px;
    }}
    .shader-control {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #171b0b;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #333a18;
    }}
    .btn-toggle {{
      background: #854d0e;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(133, 77, 14, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #a16207;
    }}
    .btn-toggle.active {{
      background: #eab308;
      color: #171a06;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(234, 179, 8, 0.7);
    }}
    .status-text {{
      font-size: 12px;
      font-weight: 600;
      color: #a16207;
    }}
    .status-text.active {{
      color: #fef08a;
      text-shadow: 0 0 8px rgba(254, 240, 138, 0.5);
    }}
    
    .shape-bar {{
      background: #121509;
      border: 1px solid #282f13;
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
      background: #0b0d05;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #232a0f;
    }}
    .btn-shape {{
      background: transparent;
      color: #ca8a04;
      border: none;
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .btn-shape.active {{
      background: #854d0e;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #fef08a;
      background: #232910;
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
      background: #0f1207;
      border: 2px solid #272d12;
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
      border-color: rgba(234, 179, 8, 0.55);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #eab308;
      box-shadow: 0 0 24px rgba(234, 179, 8, 0.35);
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
      background: rgba(234, 179, 8, 0.2);
      color: #fef08a;
      border: 1px solid rgba(234, 179, 8, 0.4);
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-top: 6px;
    }}
    .card-desc {{
      font-size: 12px;
      color: #ca8a04;
      margin-top: 4px;
      line-height: 1.45;
    }}
    
    .image-box {{
      background: #070804;
      border: 1px solid #1f240e;
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
    
    /* SHADER 1: Spacetime Vacuum Distortion Halo */
    @keyframes vacuumDistortPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(214, 217, 128, 0.8)) 
          drop-shadow(0 0 18px rgba(254, 240, 138, 0.55)) 
          drop-shadow(0 0 32px rgba(139, 92, 246, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 28px rgba(254, 240, 138, 0.9)) 
          drop-shadow(0 0 44px rgba(139, 92, 246, 0.7));
        transform: scale(1.025);
      }}
    }}
    .halo-active-1 {{
      animation: vacuumDistortPulse 2.2s ease-in-out infinite;
    }}
    
    /* SHADER 2: Hyperbolic Poincaré Metric Corona */
    @keyframes poincareCoronaPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(234, 179, 8, 0.75)) 
          drop-shadow(0 0 16px rgba(168, 85, 247, 0.5)) 
          drop-shadow(0 0 30px rgba(202, 138, 4, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 15px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 26px rgba(254, 240, 138, 0.85)) 
          drop-shadow(0 0 42px rgba(168, 85, 247, 0.75));
        transform: scale(1.02);
      }}
    }}
    .halo-active-2 {{
      animation: poincareCoronaPulse 2.0s ease-in-out infinite;
    }}
    
    /* SHADER 3: Einstein-Rosen Wormhole Bridge Corona */
    @keyframes wormholeBridgePulse {{
      0%, 75% {{
        filter: 
          drop-shadow(0 0 6px rgba(214, 217, 128, 0.6)) 
          drop-shadow(0 0 14px rgba(139, 92, 246, 0.4));
        transform: scale(1);
      }}
      80% {{
        filter: 
          drop-shadow(0 0 20px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 34px rgba(254, 240, 138, 0.95)) 
          drop-shadow(0 0 48px rgba(168, 85, 247, 0.85));
        transform: scale(1.035);
      }}
      90% {{
        filter: 
          drop-shadow(0 0 10px rgba(254, 240, 138, 0.75)) 
          drop-shadow(0 0 20px rgba(139, 92, 246, 0.5));
        transform: scale(1.01);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 6px rgba(214, 217, 128, 0.6)) 
          drop-shadow(0 0 14px rgba(139, 92, 246, 0.4));
        transform: scale(1);
      }}
    }}
    .halo-active-3 {{
      animation: wormholeBridgePulse 1.9s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
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
      background: #22280f;
      color: #fef08a;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}
    .btn-approve:hover {{
      background: #854d0e;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(234, 179, 8, 0.5);
    }}
    
    .features-list {{
      list-style: none;
      font-size: 11px;
      color: #a16207;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 6px;
    }}
    .features-list li::before {{
      content: "▹ ";
      color: #eab308;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">GTNA Material Set Showcase</span>
        <span class="formula-tag">St₄E</span>
        <h1>End Steel</h1>
        <p class="subtitle">Superliga de Ancoramento no Vácuo do End • 3,250K EBF • HV Tier • 30 Frames Fluídos</p>
      </div>
      <div class="shader-control">
        <button id="btnShader" class="btn-toggle active" onclick="toggleShader()">Shader: ATIVO</button>
        <span id="shaderStatus" class="status-text active">Halo & Corona Dinâmicos</span>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 12px; font-weight: 700; color: #fef08a;">Formas do Conjunto de Texturas:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
      <div style="font-size: 11px; color: #ca8a04;">Zoom 8× nativo (128×128 pixel art fiel)</div>
    </div>
    
    <div class="grid-options">
      
      <!-- Opção 1 -->
      <div class="card" id="card1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 10px; color: #ca8a04;">Polarização do Vácuo</span>
          </div>
          <div class="card-title">Vacuum Polarization & Pinning</div>
          <div class="card-desc">
            Polarização do vácuo dimensional do End com ancoramento quadridimensional: ondas planares de polarização com desvio gravitacional em violeta e picos de coerência pura.
          </div>
          <ul class="features-list">
            <li>Ouro-espectral pálido de Endstone (#d6d980)</li>
            <li>Fendas de obsidiana com desvio para violeta do End</li>
            <li>Flashes de coerência pura de ancoramento do espaço-tempo</li>
            <li><strong>Shader:</strong> Spacetime Vacuum Distortion Halo</li>
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
            <span style="font-size: 10px; color: #ca8a04;">Geometria Hiperbólica</span>
          </div>
          <div class="card-title">Hyperbolic Poincaré Tessellation</div>
          <div class="card-desc">
            Rede atômica com métrica hiperbólica não-euclidiana de Poincaré e curvatura constante negativa: projeção de anéis hiperbólicos em expansão com ressonância de Ender.
          </div>
          <ul class="features-list">
            <li>Tesselação hiperbólica {7,3} deformada derivando angularmente</li>
            <li>Vórtices de ressonância dimensional de Poincaré</li>
            <li>Flashes estelares nos nós de interferência não-euclidiana</li>
            <li><strong>Shader:</strong> Hyperbolic Poincaré Metric Corona</li>
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
            <span style="font-size: 10px; color: #ca8a04;">Túneis Quânticos</span>
          </div>
          <div class="card-title">Teleportation Wormholes</div>
          <div class="card-desc">
            Túneis microscópicos de emaranhamento quântico (wormholes de Einstein-Rosen em nanoescala) que transportam matéria em loops instantâneos com saltos superluminais.
          </div>
          <ul class="features-list">
            <li>Três famílias de filamentos helicoidais de wormhole</li>
            <li>Saltos quânticos estocásticos de teleportação de Ender</li>
            <li>Realce violeta-esmeralda em trajectórias superluminais</li>
            <li><strong>Shader:</strong> Einstein-Rosen Wormhole Bridge Corona</li>
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
    
    showcase_path = ARTIFACT_DIR / "end_steel_showcase.html"
    showcase_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {showcase_path}")
    print("\nTodos os artefatos para End Steel foram gerados com sucesso!")

if __name__ == "__main__":
    main()
