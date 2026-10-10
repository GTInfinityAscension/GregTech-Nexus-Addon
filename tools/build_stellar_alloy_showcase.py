#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Stellar Alloy (Liga Estelar)
Fórmula: ✦Nt₄Nq₂Ke₂✦ (4 Neutronium + 2 Naquadria + 2 Trinium)
Cor: #C5CED8 / #FFE164 (Platina Estelar Cósmica & Fulgor Termonuclear)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/stellar_alloy_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (197, 206, 216, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (197, 206, 216, 255))

# =========================================================================
# Opção 1: Photospheric Magnetoconvection & Solar Flares (Células Fotosféricas & Flares)
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
        
        # Paleta Base: Platina Estelar com tons de titânio (#c5ced8)
        # Núcleo denso metálico, relevo prateado
        r = 35.0 + t_base * 165.0
        g = 38.0 + t_base * 170.0
        b = 48.0 + t_base * 182.0
        
        # Rede de convecção de Bénard em padrão de Voronoi/trigonal dinâmico
        c1 = np.sin(x_coords * 0.9 + tau) * np.cos(y_coords * 0.9 - tau * 0.5)
        c2 = np.sin((x_coords * 0.7 - y_coords * 0.7) + tau * 0.8)
        c3 = np.cos((x_coords * 0.5 + y_coords * 0.8) - tau * 1.2)
        granulation = (c1 + c2 + c3) / 3.0
        
        # Células de subida convectiva (quentes/ouro-estelar) vs bordas frias
        granules = np.exp(-((granulation - 0.4)**2) / 0.18) * (t_base > 0.22)
        
        # Reconexões magnéticas aleatórias ejetando micro-flares (relâmpagos solares)
        flare_trigger = np.sin(tau * 3.0) * np.cos(x_coords * 1.2 + y_coords * 0.6 + tau)
        flare = np.clip(flare_trigger - 0.7, 0, 1.0) * 2.5 * (t_base > 0.3)
        
        total_mhd = granules * 1.1 + flare * 1.4
        
        # Fulgor de ouro estelar e platina ionizada (#ffe164)
        r += total_mhd * 78.0
        g += total_mhd * 72.0
        b += total_mhd * 42.0
        
        # Picos incandescentes branco-solares nos flares
        flash = np.clip(total_mhd - 1.1, 0, 1.5) * 105.0
        r += flash * 1.00
        g += flash * 0.98
        b += flash * 0.90
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Magnetar Crustal Seismic Shear & Torsional Waves (Sismos de Magnetar)
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
    # Coordenadas elípticas de cisalhamento magnético
    r_ellip = np.sqrt(dx**2 + (dy * 1.4)**2)
    theta = np.arctan2(dy * 1.4, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Platina Cósmica e Titânio Denso (#c5ced8)
        r = 32.0 + t_base * 162.0
        g = 36.0 + t_base * 168.0
        b = 46.0 + t_base * 184.0
        
        # Ciclo assimétrico de starquake: 75% acúmulo de estresse de cisalhamento, 25% disparo sísmico
        stress_phase = (t % 1.0)
        if stress_phase < 0.75:
            # Acúmulo de deformação torcional elástica na crosta de nêutrons
            progress = stress_phase / 0.75
            shear_wave = np.sin(r_ellip * 1.2 - progress * np.pi) * (progress ** 1.8)
            quake_pulse = 0.0
        else:
            # Ruptura sísmica catastrófica da crosta (Starquake de Magnetar)
            progress = (stress_phase - 0.75) / 0.25
            decay = np.exp(-progress * 4.0)
            # Ondas torcionais de alta frequência viajando pela crosta
            shear_wave = np.sin(r_ellip * 2.8 - progress * 14.0) * decay * 1.6
            quake_pulse = decay * 1.8 * (r_ellip < 6.0)
            
        total_quake = (np.clip(shear_wave, 0, 1.0) * 1.3 + quake_pulse) * (t_base > 0.22)
        
        # Luminescência sísmica de alta energia em platina-aço e azul magnético
        r += total_quake * 68.0
        g += total_quake * 76.0
        b += total_quake * 94.0
        
        # Flashes estroboscópicos de quebra de vácuo QED no momento da ruptura
        flash = np.clip(total_quake - 1.05, 0, 1.6) * 110.0
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
# Opção 3: Nova Nucleosynthesis Shockwave & Reverse-Shock (Frente de Choque de Nova)
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
        
        # Paleta Base: Platina-Estelar com nuances de síntese nuclear
        r = 34.0 + t_base * 164.0
        g = 36.0 + t_base * 168.0
        b = 50.0 + t_base * 186.0
        
        # Frente de choque convergente e choque reverso divergente
        # Choque de ida colapsando no centro e rebatendo para fora
        shock_radius = 7.5 * np.abs(np.cos(tau))
        shock_front = np.exp(-((dist - shock_radius)**2) / 0.8) * (1.2 + 0.5 * np.sin(4.0 * angle + tau * 2.0))
        
        # Ejeção de neutrinos e convecção em filamentos de nucleossíntese
        filaments = np.sin(6.0 * angle + dist * 1.2 - tau * 3.0) * np.exp(-dist / 5.0)
        core_burn = np.exp(-((dist / 1.8)**2)) * (1.0 + 0.8 * np.sin(tau * 2.0))
        
        total_shock = (shock_front * 1.35 + np.clip(filaments, 0, 1.0) * 0.8 + core_burn * 1.2) * (t_base > 0.22)
        
        # Brilho de síntese nuclear em ouro-âmbar e platina celestial
        r += total_shock * 74.0
        g += total_shock * 70.0
        b += total_shock * 60.0
        
        # Picos de detonação na frente de choque reversa
        flash = np.clip(total_shock - 1.1, 0, 1.5) * 105.0
        r += flash * 1.00
        g += flash * 0.96
        b += flash * 0.92
        
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
    print("Gerando candidatos para Stellar Alloy (✦Nt₄Nq₂Ke₂✦, #C5CED8 / #FFE164)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Photospheric Convection & Flares", render_option_1),
        (2, "Magnetar Crustal Starquake", render_option_2),
        (3, "Nova Nucleosynthesis Shock", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"sa_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (stellar_alloy_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo espaço profundo estelar
    grid_img = Image.new("RGBA", (grid_w, grid_h), (16, 20, 26, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "STELLAR ALLOY (✦Nt₄Nq₂Ke₂✦) — 128x128 CANDIDATES", fill=(254, 240, 138, 255), font=font_title)
    draw.text((pad_x, 38), "High-Energy Stellar Matter • 10,800K EBF • #C5CED8 / #FFE164 • 30 Frames", fill=(203, 213, 225, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Solar Flares",
        "OPÇÃO 2: Magnetar Starquake",
        "OPÇÃO 3: Nova Shockwave"
    ]
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        draw.text((col_x, header_h - 18), col_titles[opt_idx], fill=(241, 245, 249, 255), font=font_header)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(253, 224, 71, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo xadrez sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (26, 32, 42) if (bx // 16 + by // 16) % 2 == 0 else (18, 24, 32)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(253, 224, 71, 100), width=1)
            
    grid_png_path = ARTIFACT_DIR / "stellar_alloy_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stellar Alloy — 3 Opções Visuais & Shaders Astrofísicos</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0a0d14;
      color: #f8fafc;
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
      background: linear-gradient(135deg, #242938 0%, #151a24 60%, #0a0d14 100%);
      border: 1px solid rgba(253, 224, 71, 0.4);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(253, 224, 71, 0.15), 0 0 20px rgba(197, 206, 216, 0.2);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(253, 224, 71, 0.15);
      color: #fde047;
      border: 1px solid rgba(253, 224, 71, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 13px;
      color: #cbd5e1;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #fef08a, #facc15);
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
      background: #111827;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #1f2937;
    }}
    .btn-toggle {{
      background: #eab308;
      color: #0f172a;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(234, 179, 8, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #facc15;
    }}
    .btn-toggle.active {{
      background: #facc15;
      color: #0f172a;
      box-shadow: 0 0 16px rgba(250, 204, 21, 0.7);
    }}
    
    .shape-bar {{
      background: #0f172a;
      border: 1px solid #1e293b;
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
      background: #090d14;
      padding: 4px;
      border-radius: 8px;
      border: 1px solid #1e293b;
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
      background: #eab308;
      color: #0f172a;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(234, 179, 8, 0.4);
    }}
    .btn-shape:hover:not(.active) {{
      color: #ffffff;
      background: #1e293b;
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
      background: #0d121c;
      border: 2px solid #1e293b;
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
      border-color: rgba(250, 204, 21, 0.6);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #facc15;
      box-shadow: 0 0 24px rgba(250, 204, 21, 0.35);
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
      background: rgba(253, 224, 71, 0.15);
      color: #fde047;
      border: 1px solid rgba(253, 224, 71, 0.35);
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
      background: #06090e;
      border: 1px solid #172033;
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
    
    /* SHADER 1: Photospheric Granulation Corona & Solar Flare */
    @keyframes flareHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(250, 204, 21, 0.85)) 
          drop-shadow(0 0 18px rgba(253, 224, 71, 0.6)) 
          drop-shadow(0 0 30px rgba(245, 158, 11, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(254, 240, 138, 0.9)) 
          drop-shadow(0 0 44px rgba(250, 204, 21, 0.7));
        transform: scale(1.02);
      }}
    }}
    .halo-active-1 {{
      animation: flareHaloPulse 2.1s ease-in-out infinite;
    }}
    
    /* SHADER 2: Magnetar Seismic Torsional Strain Halo */
    @keyframes magnetarQuakePulse {{
      0%, 65% {{
        filter: 
          drop-shadow(0 0 6px rgba(197, 206, 216, 0.6)) 
          drop-shadow(0 0 14px rgba(148, 163, 184, 0.4));
        transform: scale(1);
      }}
      70% {{
        filter: 
          drop-shadow(0 0 20px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 36px rgba(248, 250, 252, 0.95)) 
          drop-shadow(0 0 50px rgba(56, 189, 248, 0.8));
        transform: scale(1.04);
      }}
      85% {{
        filter: 
          drop-shadow(0 0 12px rgba(203, 213, 225, 0.8)) 
          drop-shadow(0 0 24px rgba(125, 211, 252, 0.6));
        transform: scale(1.01);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 6px rgba(197, 206, 216, 0.6)) 
          drop-shadow(0 0 14px rgba(148, 163, 184, 0.4));
        transform: scale(1);
      }}
    }}
    .halo-active-2 {{
      animation: magnetarQuakePulse 2.5s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
    }}
    
    /* SHADER 3: Supernova Reverse-Shock Wavefront Halo */
    @keyframes supernovaShockPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 10px rgba(253, 224, 71, 0.8)) 
          drop-shadow(0 0 22px rgba(251, 146, 60, 0.55)) 
          drop-shadow(0 0 36px rgba(248, 113, 113, 0.4));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 0 30px rgba(254, 240, 138, 0.85)) 
          drop-shadow(0 0 46px rgba(251, 191, 36, 0.65));
        transform: scale(1.025);
      }}
    }}
    .halo-active-3 {{
      animation: supernovaShockPulse 2.0s ease-in-out infinite;
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
      background: #1e293b;
      color: #e2e8f0;
    }}
    .btn-approve:hover {{
      background: #eab308;
      color: #0f172a;
      box-shadow: 0 4px 14px rgba(234, 179, 8, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #fde047, #eab308);
      color: #0f172a;
      font-weight: 800;
    }}

    .features-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-top: 8px;
    }}
    .feat-tag {{
      background: #111827;
      border: 1px solid #1f2937;
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
      background: #1e293b;
      color: #ffffff;
    }}
    .btn-card-shader.active {{
      background: rgba(234, 179, 8, 0.2);
      border-color: #eab308;
      color: #fde047;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">Hyperdense Degenerate Superalloy</span>
        <span class="formula-tag">✦Nt₄Nq₂Ke₂✦</span>
        <h1>Stellar Alloy</h1>
        <p class="subtitle">EBF 10,800K • Tier UV • Matriz de Neutronium, Naquadria e Trinium • Paleta #C5CED8 / #FFE164</p>
      </div>
      
      <div class="shader-control">
        <div>
          <div style="font-size: 12px; font-weight: 700; color: #ffffff;">Simulador de Shaders</div>
          <div id="shader-status-text" style="font-size: 11px; color: #fde047;">Shader Ativo (RenderBlender)</div>
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
            <span style="font-size: 11px; color: #94a3b8;">Física: Solar Convection & Flares</span>
          </div>
          <div class="card-title">Photospheric Magnetoconvection</div>
          <p class="card-desc">
            Células convectivas fotosféricas de Bénard em ebulição térmica contínua: plasma estelar ascendente em ouro-âmbar quente cercado por fendas de resfriamento, com reconexões magnéticas disparando micro-flares solares de alta velocidade através das facetas.
          </p>
          <div class="features-list">
            <span class="feat-tag">Células Convectivas Bénard</span>
            <span class="feat-tag">Micro-Flares Espiculares</span>
            <span class="feat-tag">Ouro-Estelar #FFE164</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-1" class="pixelated-art halo-active-1" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-1" class="btn-card-shader active" onclick="toggleCardShader(1)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(1)">ESCOLHER OPÇÃO 1 (SOLAR FLARES)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 2</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Magnetar Starquake</span>
          </div>
          <div class="card-title">Magnetar Crustal Seismic Shear</div>
          <p class="card-desc">
            Ondas sísmicas torcionais na crosta de nêutrons de 10¹⁴ g/cm³: acúmulo elástico de tensão de cisalhamento (75% do ciclo) em platina-aço seguido por ruptura sísmica catastrófica (25%), propagando ondas elípticas de alta frequência com flashes de quebra de vácuo magnético.
          </p>
          <div class="features-list">
            <span class="feat-tag">Histerese Sísmica 75/25</span>
            <span class="feat-tag">Ondas Torcionais Elípticas</span>
            <span class="feat-tag">Ruptura QED Magnetar</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-2" class="pixelated-art halo-active-2" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-2" class="btn-card-shader active" onclick="toggleCardShader(2)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(2)">ESCOLHER OPÇÃO 2 (STARQUAKE)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 3</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Nova Nucleosynthesis Shock</span>
          </div>
          <div class="card-title">Nova Nucleosynthesis Shockwave</div>
          <p class="card-desc">
            Frente de choque termonuclear impulsionada por aprisionamento de neutrinos: frente esférica de compressão que colapsa radialmente no núcleo e rebate em choque reverso divergente, sintetizando núcleos pesados com filamentos luminosos e brilho celestial estelar.
          </p>
          <div class="features-list">
            <span class="feat-tag">Choque Reverso Divergente</span>
            <span class="feat-tag">Colapso Termonuclear Radiano</span>
            <span class="feat-tag">Filamentos de Neutrinos</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-3" class="pixelated-art halo-active-3" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-3" class="btn-card-shader active" onclick="toggleCardShader(3)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(3)">ESCOLHER OPÇÃO 3 (NOVA SHOCK)</button>
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
        text.style.color = '#fde047';
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
    
    html_path = ARTIFACT_DIR / "stellar_alloy_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
