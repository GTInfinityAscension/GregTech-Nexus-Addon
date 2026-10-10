#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Dark Steel
Fórmula: FeCOb (Carbon & Obsidian Infused Heavy Steel Superalloy)
Cor Base: #414751 (Cinza-Grafite / Ardósia Escura / Vidro Vulcânico Negro)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/dark_steel_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (65, 71, 81, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (65, 71, 81, 255))

# =========================================================================
# Opção 1: Vitreous Obsidian Conchoidal Fracture Bands & Amorphous Shear Toughening
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Centro baricêntrico para cristas conchoidais
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dx = (x_coords - cx)
    dy = (y_coords - cy)
    dist = np.sqrt(dx**2 + dy**2)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base Dark Steel: Grafite / Ardósia Escura (#414751)
        # Sombra profunda: #181b22 (R:24, G:27, B:34)
        # Base: #414751 (R:65, G:71, B:81)
        # Highlight: #7a889b (R:122, G:136, B:155)
        r = 18.0 + t_base * 75.0
        g = 20.0 + t_base * 80.0
        b = 25.0 + t_base * 92.0
        
        # 1. Cristas concêntricas conchoidais deslizando pela lâmina (ondas de Rayleigh vítreas)
        conchoidal_wave = np.sin(dist * 1.6 - tau * 2.2)
        conchoidal_crest = np.exp(-((conchoidal_wave - 0.75)**2) / 0.12) * (t_base > 0.20)
        
        # 2. Estrias parabólicas de Wallner cruzadas (cisalhamento de choque a 45°)
        wallner_shear = np.sin((dx * 0.707 + dy * 0.707) * 1.8 + tau * 1.5)
        wallner_laths = np.exp(-((wallner_shear - 0.82)**2) / 0.10) * (t_base > 0.24)
        
        # 3. Zonas de fratura conchoidal e reflexo vítreo negro-azulado
        r += conchoidal_crest * 36.0
        g += conchoidal_crest * 42.0
        b += conchoidal_crest * 54.0
        
        # 4. Reflexos especulares nas arestas de corte de espessura atômica
        r += wallner_laths * 45.0
        g += wallner_laths * 50.0
        b += wallner_laths * 62.0
        
        # 5. Picos prismáticos vítreos incandescentes nos nós de interferência
        prism_spark = np.clip(conchoidal_crest * wallner_laths - 0.35, 0, 1.5) * 115.0
        r += prism_spark * 0.95
        g += prism_spark * 1.00
        b += prism_spark * 1.05
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 2: Martensitic Carbon Supersaturation & Tetragonal Bainite Needle Laths
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Ângulos cristalográficos da martensita e bainita inferior: 54.7° e -35.3°
    theta1 = np.radians(54.7)
    theta2 = np.radians(-35.3)
    
    k1_x, k1_y = np.cos(theta1), np.sin(theta1)
    k2_x, k2_y = np.cos(theta2), np.sin(theta2)
    
    u1 = x_coords * k1_x + y_coords * k1_y
    u2 = x_coords * k2_x + y_coords * k2_y
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base Dark Steel: Aço de Alta Têmpera Martensítico
        # Sombra profunda grafite: #15171c (R:21, G:23, B:28)
        # Corpo da liga temperada: #414751 (R:65, G:71, B:81)
        r = 16.0 + t_base * 76.0
        g = 18.0 + t_base * 80.0
        b = 22.0 + t_base * 90.0
        
        # 1. Família 1 de agulhas aciculares (laths) em avanço adifusional rápido
        lath1_wave = np.sin(u1 * 1.9 - tau * 3.2)
        lath1 = np.exp(-((lath1_wave - 0.82)**2) / 0.08) * (t_base > 0.22)
        
        # 2. Família 2 conjugada de agulhas aciculares cruzadas
        lath2_wave = np.sin(u2 * 1.9 + tau * 2.8)
        lath2 = np.exp(-((lath2_wave - 0.85)**2) / 0.08) * (t_base > 0.22)
        
        # 3. Micro-avalanches de emissão acústica (bursts estocásticos de relaxamento)
        burst_phase = (f * 11) % 30
        acoustic_burst = np.exp(-((x_coords - (burst_phase % 16))**2 + (y_coords - ((burst_phase * 3) % 16))**2) / 2.2) * (t_base > 0.28)
        
        # 4. Brilho metálico dos laths de bainita/martensita em cinza-aço afiado
        r += lath1 * 48.0 + lath2 * 36.0
        g += lath1 * 52.0 + lath2 * 40.0
        b += lath1 * 62.0 + lath2 * 48.0
        
        # 5. Nós de colisão e ancoramento de discordâncias de Cottrell
        cross_nodes = lath1 * lath2
        r += cross_nodes * 75.0
        g += cross_nodes * 80.0
        b += cross_nodes * 95.0
        
        # 6. Flashes brancos de liberação acústica nos pontos de nucleação
        r += acoustic_burst * 130.0
        g += acoustic_burst * 135.0
        b += acoustic_burst * 145.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Void-Absorbing Obsidian Acoustic Resonance & Gravitational Shadow
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dx = (x_coords - cx)
    dy = (y_coords - cy)
    r_dist = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base Dark Steel: Grafite-Vácuo com Matriz de Absorção
        # Tons escuros de absorção: #101217 (R:16, G:18, B:23)
        # Base: #414751 (R:65, G:71, B:81)
        r = 14.0 + t_base * 74.0
        g = 15.0 + t_base * 78.0
        b = 20.0 + t_base * 92.0
        
        # 1. Ondas acústicas centrípetas de absorção (sugadas em espiral para o centro)
        centripetal_radius = (r_dist + tau * 1.8) % 8.0
        absorption_ring = np.exp(-((centripetal_radius - 4.0)**2) / 0.8) * (t_base > 0.20)
        
        # 2. Modulação em espiral de momento angular óptico (vórtice de Casimir)
        spiral_phase = np.sin(3.0 * theta + r_dist * 1.5 - tau * 2.5)
        spiral_trap = np.clip(spiral_phase, 0, 1.2) * (t_base > 0.22)
        
        # 3. Gradiente de absorção de luz (escurecimento por armadilha de fótons)
        shadow_dip = np.clip(1.0 - 0.35 * spiral_trap, 0.4, 1.0)
        r *= shadow_dip
        g *= shadow_dip
        b *= shadow_dip
        
        # 4. Emissão Cherenkov ressonante em violeta-obsidiana profundo nas bordas de escape
        cherenkov_ring = absorption_ring * (t_base > 0.25)
        r += cherenkov_ring * 42.0
        g += cherenkov_ring * 16.0
        b += cherenkov_ring * 68.0
        
        # 5. Reflexos nos limites do horizonte de escape em violeta elétrico e prata
        violet_glow = spiral_trap * 0.7
        r += violet_glow * 32.0
        g += violet_glow * 14.0
        b += violet_glow * 55.0
        
        # 6. Micro-flashes de horizonte de eventos
        flash = np.clip(cherenkov_ring * spiral_trap - 0.45, 0, 1.5) * 110.0
        r += flash * 0.95
        g += flash * 0.92
        b += flash * 1.05
        
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
    print("Gerando candidatos para Dark Steel (FeCOb, #414751)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Vitreous Obsidian Conchoidal Fracture", render_option_1),
        (2, "Martensitic Tetragonal Needle Laths", render_option_2),
        (3, "Void-Absorbing Obsidian Resonance", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"dark_steel_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (dark_steel_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (14, 16, 20, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "DARK STEEL (FeCOb) — 128x128", fill=(241, 245, 249, 255), font=font_title)
    draw.text((pad_x, 38), "Carbon & Obsidian Infused Heavy Steel Superalloy • 1,450K EBF • MV Tier • #414751 • 30 Frames", fill=(148, 163, 184, 255), font=font_sub)
    
    col_titles = [
        ("OPÇÃO 1", "Conchoidal Fracture"),
        ("OPÇÃO 2", "Martensitic Laths"),
        ("OPÇÃO 3", "Void Resonance")
    ]
    font_subhdr = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 9)
    for opt_idx in range(3):
        col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
        opt_hdr, opt_sub = col_titles[opt_idx]
        draw.text((col_x, header_h - 26), opt_hdr, fill=(241, 245, 249, 255), font=font_header)
        draw.text((col_x, header_h - 13), opt_sub, fill=(148, 163, 184, 255), font=font_subhdr)
        
    for row_idx, s in enumerate(shapes):
        row_y = header_h + row_idx * (cell_size + pad_y)
        draw.text((pad_x, row_y + cell_size // 2 - 6), s.upper(), fill=(148, 163, 184, 255), font=font_label)
        
        for opt_idx in range(3):
            col_x = pad_x + label_w + opt_idx * (cell_size + col_spacing)
            frame_img = all_frames[opt_idx + 1][s][14]
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (24, 28, 36) if (bx // 16 + by // 16) % 2 == 0 else (18, 20, 26)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(100, 116, 139, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "dark_steel_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dark Steel — 3 Opções Visuais & Shaders Metálicos/Vítreos</title>
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
      background: linear-gradient(135deg, #1e232d 0%, #11141b 60%, #0b0d11 100%);
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 14px;
      padding: 22px 26px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7), 0 0 25px rgba(65, 71, 81, 0.25);
    }}
    .badge {{
      display: inline-block;
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      background: rgba(100, 116, 139, 0.2);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.4);
      margin-bottom: 6px;
    }}
    .formula-tag {{
      font-size: 12px;
      color: #94a3b8;
      font-family: monospace;
      font-weight: 700;
      margin-left: 8px;
    }}
    h1 {{
      font-size: 24px;
      font-weight: 800;
      background: linear-gradient(to right, #ffffff, #cbd5e1, #64748b);
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
      background: #141720;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #282f3d;
    }}
    .btn-toggle {{
      background: #334155;
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
      background: #475569;
    }}
    .btn-toggle.active {{
      background: #64748b;
      color: #f8fafc;
      font-weight: 800;
      box-shadow: 0 0 16px rgba(148, 163, 184, 0.6);
    }}
    .status-text {{
      font-size: 12px;
      font-weight: 600;
      color: #64748b;
    }}
    .status-text.active {{
      color: #e2e8f0;
      text-shadow: 0 0 8px rgba(226, 232, 240, 0.5);
    }}
    
    .shape-bar {{
      background: #11141b;
      border: 1px solid #1f2533;
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
      border: 1px solid #191f2c;
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
      transition: all 0.15s;
    }}
    .btn-shape:hover {{
      color: #f1f5f9;
      background: rgba(255, 255, 255, 0.05);
    }}
    .btn-shape.active {{
      background: #334155;
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    
    .grid-options {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
    }}
    @media (max-width: 860px) {{
      .grid-options {{
        grid-template-columns: 1fr;
      }}
    }}
    
    .card {{
      background: #11141b;
      border: 1px solid #1f2533;
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
      transition: transform 0.2s, border-color 0.2s;
    }}
    .card:hover {{
      transform: translateY(-2px);
      border-color: rgba(148, 163, 184, 0.5);
    }}
    .card-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 4px;
    }}
    .tag-opt {{
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: rgba(100, 116, 139, 0.2);
      color: #cbd5e1;
      border: 1px solid rgba(148, 163, 184, 0.4);
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
      background: #08090d;
      border: 1px solid #181d28;
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
    
    /* SHADER 1: Vitreous Conchoidal Refraction & Obsidian Prism Glare */
    @keyframes conchoidalRefractPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 6px rgba(65, 71, 81, 0.9)) 
          drop-shadow(0 0 16px rgba(100, 116, 139, 0.6)) 
          drop-shadow(0 0 30px rgba(148, 163, 184, 0.35));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 15px rgba(248, 250, 252, 0.95)) 
          drop-shadow(0 0 26px rgba(148, 163, 184, 0.85)) 
          drop-shadow(0 0 42px rgba(100, 116, 139, 0.7));
        transform: scale(1.025);
      }}
    }}
    .halo-active-1 {{
      animation: conchoidalRefractPulse 2.3s ease-in-out infinite;
    }}
    
    /* SHADER 2: Martensitic Acoustic Burst & Needle Flare */
    @keyframes martensiticBurstPulse {{
      0%, 78% {{
        filter: 
          drop-shadow(0 0 6px rgba(71, 85, 105, 0.7)) 
          drop-shadow(0 0 14px rgba(100, 116, 139, 0.45));
        transform: scale(1);
      }}
      82% {{
        filter: 
          drop-shadow(0 0 20px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 34px rgba(203, 213, 225, 0.95)) 
          drop-shadow(0 0 48px rgba(100, 116, 139, 0.8));
        transform: scale(1.035);
      }}
      90% {{
        filter: 
          drop-shadow(0 0 10px rgba(203, 213, 225, 0.75)) 
          drop-shadow(0 0 20px rgba(71, 85, 105, 0.5));
        transform: scale(1.01);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 6px rgba(71, 85, 105, 0.7)) 
          drop-shadow(0 0 14px rgba(100, 116, 139, 0.45));
        transform: scale(1);
      }}
    }}
    .halo-active-2 {{
      animation: martensiticBurstPulse 1.9s cubic-bezier(0.2, 0.8, 0.2, 1) infinite;
    }}
    
    /* SHADER 3: Gravitational Acoustic Shadow & Obsidian Cherenkov Corona */
    @keyframes acousticShadowPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(0 0 8px rgba(88, 28, 135, 0.75)) 
          drop-shadow(0 0 18px rgba(126, 34, 206, 0.45)) 
          drop-shadow(0 0 32px rgba(30, 27, 75, 0.6));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(241, 245, 249, 0.95)) 
          drop-shadow(0 0 28px rgba(168, 85, 247, 0.85)) 
          drop-shadow(0 0 44px rgba(88, 28, 135, 0.75));
        transform: scale(1.02);
      }}
    }}
    .halo-active-3 {{
      animation: acousticShadowPulse 2.1s ease-in-out infinite;
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
      color: #f1f5f9;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}
    .btn-approve:hover {{
      background: #475569;
      color: #ffffff;
      box-shadow: 0 0 12px rgba(148, 163, 184, 0.5);
    }}
    
    .features-list {{
      list-style: none;
      font-size: 11px;
      color: #94a3b8;
      display: flex;
      flex-direction: column;
      gap: 4px;
      margin-top: 6px;
    }}
    .features-list li::before {{
      content: "▹ ";
      color: #cbd5e1;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">GTNA Material Set Showcase</span>
        <span class="formula-tag">FeCOb</span>
        <h1>Dark Steel</h1>
        <p class="subtitle">Superliga de Aço com Carbono e Obsidiana • 1,450K EBF • MV Tier • 30 Frames Fluídos</p>
      </div>
      <div class="shader-control">
        <button id="btnShader" class="btn-toggle active" onclick="toggleShader()">Shader: ATIVO</button>
        <span id="shaderStatus" class="status-text active">Halo & Corona Dinâmicos</span>
      </div>
    </div>
    
    <div class="shape-bar">
      <div style="font-size: 12px; font-weight: 700; color: #f1f5f9;">Formas do Conjunto de Texturas:</div>
      <div class="shape-buttons">
        <button class="btn-shape active" onclick="setShape('ingot', this)">Ingot</button>
        <button class="btn-shape" onclick="setShape('plate', this)">Plate</button>
        <button class="btn-shape" onclick="setShape('gear', this)">Gear</button>
        <button class="btn-shape" onclick="setShape('block', this)">Block</button>
      </div>
      <div style="font-size: 11px; color: #94a3b8;">Zoom 8× nativo (128×128 pixel art fiel)</div>
    </div>
    
    <div class="grid-options">
      
      <!-- Opção 1 -->
      <div class="card" id="card1">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 1</span>
            <span style="font-size: 10px; color: #94a3b8;">Fratura Conchoidal</span>
          </div>
          <div class="card-title">Vitreous Conchoidal Fracture</div>
          <div class="card-desc">
            Mecânica de fratura conchoidal em vidro vulcânico de obsidiana com ondas elásticas de Rayleigh: cristas curvas de cisalhamento amorfo e arestas de corte com reflexão prismática vítrea.
          </div>
          <ul class="features-list">
            <li>Cristas concêntricas conchoidais deslizando em arcos suaves</li>
            <li>Estrias de Wallner em cisalhamento a 45°</li>
            <li>Arestas de corte atômico com reflexão especular afiada</li>
            <li><strong>Shader:</strong> Vitreous Conchoidal Refraction & Obsidian Prism Glare</li>
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
            <span style="font-size: 10px; color: #94a3b8;">Agulhas Martensíticas</span>
          </div>
          <div class="card-title">Martensitic Tetragonal Needle Laths</div>
          <div class="card-desc">
            Transformação martensítica sem difusão para rede tetragonal (BCT) com supersaturação extrema de carbono: laths em agulhas entrelaçadas a 54.7° e -35.3° com avalanches acústicas.
          </div>
          <ul class="features-list">
            <li>Agulhas aciculares conjugadas de bainita/martensita em avanço rápido</li>
            <li>Pontos de ancoramento de Cottrell com alta dureza elástica</li>
            <li>Flashes brancos de emissão acústica instantânea nos nós</li>
            <li><strong>Shader:</strong> Martensitic Acoustic Burst & Needle Flare</li>
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
            <span style="font-size: 10px; color: #94a3b8;">Ressonância do Vácuo</span>
          </div>
          <div class="card-title">Void-Absorbing Obsidian Resonance</div>
          <div class="card-desc">
            Cavidade acústica fonônica de Casimir na rede vítrea de obsidiana: absorção centrípeta de luz incidente com horizonte de escape e luminescência Cherenkov em violeta-obsidiana.
          </div>
          <ul class="features-list">
            <li>Ondulações concêntricas de absorção centrípeta de luz</li>
            <li>Vórtices de momento angular óptico na matriz de carbono</li>
            <li>Franjas de emissão Cherenkov ressonante em violeta-obsidiana</li>
            <li><strong>Shader:</strong> Gravitational Acoustic Shadow & Cherenkov Corona</li>
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
        btn.textContent = 'Shader: ATIVO';
        status.classList.add('active');
        status.textContent = 'Halo & Corona Dinâmicos';
        img1.className = 'pixelated-art halo-active-1';
        img2.className = 'pixelated-art halo-active-2';
        img3.className = 'pixelated-art halo-active-3';
      }} else {{
        btn.classList.remove('active');
        btn.textContent = 'Shader: DESATIVADO';
        status.classList.remove('active');
        status.textContent = 'Apenas Pixel Art Crua';
        img1.className = 'pixelated-art';
        img2.className = 'pixelated-art';
        img3.className = 'pixelated-art';
      }}
    }}
    
    function selectOption(opt) {{
      alert('Você selecionou a Opção ' + opt + '! Por favor, envie sua escolha no chat para continuar.');
    }}
  </script>
</body>
</html>
"""
    showcase_path = ARTIFACT_DIR / "dark_steel_showcase.html"
    showcase_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase interativo HTML salvo em: {showcase_path}")

if __name__ == "__main__":
    main()
