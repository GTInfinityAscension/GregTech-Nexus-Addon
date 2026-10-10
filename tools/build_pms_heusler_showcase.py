#!/usr/bin/env python3
"""
Gerador de Candidatos e Showcase Interativo para Platinum-Manganese-Antimony Heusler Alloy (PtMnSb)
Cor: #B0BCC8 / #E6E6E6 (Platina-Manganês Spintrônica Nobre)
GregTech Nexus Addon (GTNA)
"""

import os
import math
import json
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/pms_heusler_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (176, 188, 200, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (176, 188, 200, 255))

# =========================================================================
# Opção 1: Spintronic Half-Metallic Spin-Filter Polarization Waves (Filtro 100% de Spin & MOKE)
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
        
        # Paleta Base: Platina-Aço Spintrônica nobre (#b0bcc8)
        # Sombra grafite-antimônio profunda, corpo platina polida, realces prateados
        r = 30.0 + t_base * 155.0
        g = 35.0 + t_base * 162.0
        b = 45.0 + t_base * 175.0
        
        # Duas frentes planares de onda de polarização de spin em ângulos conjugados de 35° e -55°
        # Canal spin-up sem resistência, spin-down em reflexão de gap total
        wave1 = np.sin((x_coords * 0.75 + y_coords * 0.52) - tau * 2.0)
        wave2 = np.cos((x_coords * 0.52 - y_coords * 0.75) + tau * 1.5)
        
        # Batimento de polarização 100% com modulação de envelope
        spin_envelope = np.sin(tau) * 0.35 + 0.65
        polarization_wave = np.clip(wave1 * wave2, 0, 1.0) * spin_envelope * (t_base > 0.22)
        
        # Efeito Magneto-Óptico de Kerr (MOKE) - Cristas de reflexão de Kerr com rotação do vetor elétrico
        kerr_crest = np.exp(-((wave1 - 0.65)**2) / 0.16) * (t_base > 0.28)
        
        total_spin = polarization_wave * 1.25 + kerr_crest * 0.95
        
        # Realce metálico de platina pura e reflexo especular birrefringente azul-gelo
        r += total_spin * 66.0
        g += total_spin * 74.0
        b += total_spin * 86.0
        
        # Flashes especulares de Kerr de platina ultra-pura
        flash = np.clip(total_spin - 1.1, 0, 1.5) * 95.0
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
# Opção 2: Topological Chiral Skyrmion Lattice Drift & Hall Precession (Deriva de Skyrmions Quirais)
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    # 3 vórtices de Skyrmion em coordenadas relativas com precessão de Hall em órbita elíptica
    skyrmion_radii = [4.2, 5.0, 4.6]
    skyrmion_phases = [0.0, 2.094, 4.188]  # 120° apart
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Prata-Manganês Magnética com gradiente quiral
        r = 28.0 + t_base * 150.0
        g = 32.0 + t_base * 160.0
        b = 44.0 + t_base * 178.0
        
        skyrmion_field = 0.0
        core_sparks = 0.0
        
        for sr, phase in zip(skyrmion_radii, skyrmion_phases):
            # Trajetória girotópica com ângulo de Hall de Skyrmion
            sk_x = cx + sr * np.cos(tau + phase)
            sk_y = cy + (sr * 0.72) * np.sin(tau + phase)
            
            dx = x_coords - sk_x
            dy = y_coords - sk_y
            dist = np.sqrt(dx**2 + dy**2)
            angle = np.arctan2(dy, dx)
            
            # Vórtice espiral quiral (Dzyaloshinskii-Moriya) com torção dextrogira
            chiral_spiral = np.sin(angle * 2.0 - dist * 1.45 + tau * 2.5) * np.exp(-dist / 3.4)
            
            # Núcleo magnético condensado (perpendicular ao plano)
            core = np.exp(-((dist / 1.15)**2)) * (1.2 + 0.65 * np.sin(tau * 3.0 + phase))
            
            skyrmion_field += np.clip(chiral_spiral, 0, 1.0) * 1.15 + core * 1.4
            core_sparks += core
            
        total_sk = skyrmion_field * (t_base > 0.2)
        
        # Luminescência de vórtice quiral em platina-aço
        r += total_sk * 62.0
        g += total_sk * 72.0
        b += total_sk * 90.0
        
        # Picos de energia topológica no núcleo do skyrmion
        flash = np.clip(core_sparks - 0.9, 0, 1.5) * 110.0
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
# Opção 3: Weyl Semimetal Chiral Anomaly Fermi-Arc Resonant Beams (Arcos de Fermi & Nós de Weyl)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    # Polos de Weyl conjugados opostos (nós quirais W+ e W-)
    weyl_plus = (cx - 4.5, cy - 3.5)
    weyl_minus = (cx + 4.5, cy + 3.5)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        tau = 2 * np.pi * t
        
        # Paleta Base: Platina-Antimônio com nuances de semi-metal quântico
        r = 32.0 + t_base * 152.0
        g = 34.0 + t_base * 162.0
        b = 48.0 + t_base * 178.0
        
        # Distâncias aos nós de Weyl
        d_plus = np.sqrt((x_coords - weyl_plus[0])**2 + (y_coords - weyl_plus[1])**2)
        d_minus = np.sqrt((x_coords - weyl_minus[0])**2 + (y_coords - weyl_minus[1])**2)
        
        # Coordenadas bipolares hiperbólicas (conectando os dois polos de Weyl)
        # Arcos de Fermi tangenciais de condução balística de superfície
        fermi_phase = (d_plus - d_minus) * 1.25 - tau * 3.0
        arc_lines = np.exp(-((np.sin(fermi_phase))**2) / 0.12) * np.exp(-(d_plus + d_minus) / 11.5)
        
        # Bombeamento quiral por anomalia eletromagnética (E · B != 0)
        pumping_pulse = np.sin(tau * 2.0)**4
        nodes_glow = (np.exp(-(d_plus / 1.5)**2) + np.exp(-(d_minus / 1.5)**2)) * (1.0 + 0.8 * np.cos(tau * 2.0))
        
        total_weyl = (arc_lines * 1.45 + nodes_glow * 1.2 * pumping_pulse) * (t_base > 0.22)
        
        # Emissão de feixes de Fermi em platina-aço com sutil fluorescência violeta-fria
        r += total_weyl * 65.0
        g += total_weyl * 68.0
        b += total_weyl * 90.0
        
        # Picos nos nós e cruzamentos de fase quântica
        flash = np.clip(total_weyl - 1.15, 0, 1.5) * 102.0
        r += flash * 0.98
        g += flash * 0.96
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
    print("Gerando candidatos para Platinum-Manganese-Antimony Heusler Alloy (PtMnSb, #B0BCC8 / #E6E6E6)...")
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "Spin-Filter Kerr Waves", render_option_1),
        (2, "Topological Skyrmion Lattice", render_option_2),
        (3, "Weyl Fermi-Arc Interference", render_option_3)
    ]
    
    b64_data = {1: {}, 2: {}, 3: {}}
    all_frames = {1: {}, 2: {}, 3: {}}
    
    for opt_num, opt_name, render_fn in options:
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_num][s] = frames
            
            gif_path = OUT_DIR / f"pms_opt{opt_num}_{s}.gif"
            create_gif(frames, gif_path)
            b64_str = base64.b64encode(gif_path.read_bytes()).decode("utf-8")
            b64_data[opt_num][s] = f"data:image/gif;base64,{b64_str}"
            print(f"  ✓ {gif_path.name}")
            
    # 2. Gerar Grid Comparativo Estático de 128px (platinum_manganese_antimony_heusler_alloy_grid.png)
    cell_size = 128
    pad_x = 35
    pad_y = 18
    header_h = 70
    label_w = 75
    col_spacing = 45
    
    grid_w = pad_x + label_w + (cell_size + col_spacing) * 3 + pad_x
    grid_h = header_h + (cell_size + pad_y) * 4 + 20
    
    # Fundo platina-grafite profundo com contraste técnico
    grid_img = Image.new("RGBA", (grid_w, grid_h), (18, 22, 28, 255))
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_header = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_label = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    
    draw.text((pad_x, 14), "PLATINUM-MANGANESE-ANTIMONY HEUSLER ALLOY (PtMnSb) — 128x128", fill=(203, 213, 225, 255), font=font_title)
    draw.text((pad_x, 38), "Half-Metallic Spintronic Superalloy • 100% Spin Polarization • #B0BCC8 • 30 Frames", fill=(148, 163, 184, 255), font=font_sub)
    
    col_titles = [
        "OPÇÃO 1: Spin-Filter Waves",
        "OPÇÃO 2: Skyrmion Lattice",
        "OPÇÃO 3: Weyl Fermi-Arcs"
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
            
            # Fundo xadrez metálico para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (30, 36, 45) if (bx // 16 + by // 16) % 2 == 0 else (22, 28, 36)
                    draw.rectangle([col_x + bx, row_y + by, col_x + bx + 15, row_y + by + 15], fill=c)
                    
            grid_img.paste(scaled, (col_x, row_y), scaled)
            draw.rectangle([col_x - 1, row_y - 1, col_x + cell_size, row_y + cell_size], outline=(148, 163, 184, 120), width=1)
            
    grid_png_path = ARTIFACT_DIR / "platinum_manganese_antimony_heusler_alloy_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML completo e inovador
    json_b64 = json.dumps(b64_data)
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PtMnSb Heusler Alloy — 3 Opções Visuais & Shaders Spintrônicos</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background-color: #0b0f15;
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
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 60%, #080c12 100%);
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
      font-size: 13px;
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
      background: #111827;
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid #1f2937;
    }}
    .btn-toggle {{
      background: #3b82f6;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
      transition: all 0.2s;
    }}
    .btn-toggle:hover {{
      background: #60a5fa;
    }}
    .btn-toggle.active {{
      background: #2563eb;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(59, 130, 246, 0.7);
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
      background: #334155;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
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
      border-color: rgba(148, 163, 184, 0.6);
      transform: translateY(-2px);
    }}
    .card.selected {{
      border-color: #60a5fa;
      box-shadow: 0 0 24px rgba(96, 165, 250, 0.35);
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
    
    /* SHADER 1: Spintronic Kerr-Rotation Anisotropic Birefringent Halo */
    @keyframes kerrHaloPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(-2px 0 8px rgba(147, 197, 253, 0.85)) 
          drop-shadow(2px 0 16px rgba(241, 245, 249, 0.7)) 
          drop-shadow(0 0 28px rgba(96, 165, 250, 0.45));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 -3px 14px rgba(255, 255, 255, 0.95)) 
          drop-shadow(0 3px 24px rgba(147, 197, 253, 0.8)) 
          drop-shadow(0 0 38px rgba(191, 219, 254, 0.6));
        transform: scale(1.02);
      }}
    }}
    .halo-active-1 {{
      animation: kerrHaloPulse 2.0s ease-in-out infinite;
    }}
    
    /* SHADER 2: Chiral Skyrmion Topology Flux Vortex Aura */
    @keyframes skyrmionVortexPulse {{
      0% {{
        filter: 
          drop-shadow(0 0 10px rgba(203, 213, 225, 0.9)) 
          drop-shadow(0 0 20px rgba(56, 189, 248, 0.6)) 
          drop-shadow(0 0 32px rgba(148, 163, 184, 0.5));
        transform: rotate(0deg) scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(0 0 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(0 0 28px rgba(125, 211, 252, 0.85)) 
          drop-shadow(0 0 44px rgba(56, 189, 248, 0.65));
        transform: scale(1.02);
      }}
      100% {{
        filter: 
          drop-shadow(0 0 10px rgba(203, 213, 225, 0.9)) 
          drop-shadow(0 0 20px rgba(56, 189, 248, 0.6)) 
          drop-shadow(0 0 32px rgba(148, 163, 184, 0.5));
        transform: rotate(0deg) scale(1);
      }}
    }}
    .halo-active-2 {{
      animation: skyrmionVortexPulse 2.4s ease-in-out infinite;
    }}
    
    /* SHADER 3: Weyl Semimetal Chiral Anomaly Dual-Node Flare */
    @keyframes weylArcPulse {{
      0%, 100% {{
        filter: 
          drop-shadow(-4px -4px 10px rgba(199, 210, 254, 0.9)) 
          drop-shadow(4px 4px 10px rgba(248, 250, 252, 0.9)) 
          drop-shadow(0 0 26px rgba(129, 140, 248, 0.55));
        transform: scale(1);
      }}
      50% {{
        filter: 
          drop-shadow(-6px -6px 16px rgba(255, 255, 255, 1.0)) 
          drop-shadow(6px 6px 16px rgba(224, 231, 255, 0.95)) 
          drop-shadow(0 0 40px rgba(165, 180, 252, 0.75));
        transform: scale(1.025);
      }}
    }}
    .halo-active-3 {{
      animation: weylArcPulse 1.8s ease-in-out infinite;
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
      background: #3b82f6;
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.45);
    }}
    .card.selected .btn-approve {{
      background: linear-gradient(135deg, #60a5fa, #2563eb);
      color: #ffffff;
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
      background: rgba(59, 130, 246, 0.2);
      border-color: #3b82f6;
      color: #93c5fd;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <div class="header-card">
      <div>
        <span class="badge">Ferromagnetic Heusler Superalloy</span>
        <span class="formula-tag">PtMnSb</span>
        <h1>Platinum-Manganese-Antimony Heusler Alloy</h1>
        <p class="subtitle">100% Spin Polarization • Half-Metallic Bandgap • Efeito Kerr Extremo • Paleta #B0BCC8 / #E6E6E6</p>
      </div>
      
      <div class="shader-control">
        <div>
          <div style="font-size: 12px; font-weight: 700; color: #ffffff;">Simulador de Shaders</div>
          <div id="shader-status-text" style="font-size: 11px; color: #60a5fa;">Shader Ativo (RenderBlender)</div>
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
            <span style="font-size: 11px; color: #94a3b8;">Física: Spin-Filter & MOKE</span>
          </div>
          <div class="card-title">Half-Metallic Spin-Filter Waves</div>
          <p class="card-desc">
            Bandgap proibido total para spin-down e condução ideal para spin-up: ondas transversais de polarização 100% de spin deslizam pelas facetas com cristas de reflexão do Efeito Kerr Magneto-Óptico (MOKE) e flashes birrefringentes em platina pura.
          </p>
          <div class="features-list">
            <span class="feat-tag">100% Spin Polarization</span>
            <span class="feat-tag">Ondas de Kerr Conjugadas</span>
            <span class="feat-tag">Reflexão Especular Platina</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-1" class="pixelated-art halo-active-1" src="{b64_data[1]['ingot']}" alt="Opção 1 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-1" class="btn-card-shader active" onclick="toggleCardShader(1)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(1)">ESCOLHER OPÇÃO 1 (SPIN-FILTER)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 2 -->
      <div class="card" id="card-2">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 2</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Skyrmion Hall Drift</span>
          </div>
          <div class="card-title">Topological Chiral Skyrmion Lattice</div>
          <p class="card-desc">
            Interação Dzyaloshinskii-Moriya na interface Pt-Mn estabiliza redemoinhos de spin com enrolamento topológico Q = -1. Três vórtices helicoidais quirais derivam angularmente sob precessão de Hall, gerando ondas espiralantes e flashes nos núcleos.
          </p>
          <div class="features-list">
            <span class="feat-tag">Dzyaloshinskii-Moriya DMI</span>
            <span class="feat-tag">Vórtices Quirais Helicoidais</span>
            <span class="feat-tag">Efeito Hall de Skyrmion</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-2" class="pixelated-art halo-active-2" src="{b64_data[2]['ingot']}" alt="Opção 2 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-2" class="btn-card-shader active" onclick="toggleCardShader(2)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(2)">ESCOLHER OPÇÃO 2 (SKYRMION)</button>
        </div>
      </div>
      
      <!-- OPÇÃO 3 -->
      <div class="card" id="card-3">
        <div>
          <div class="card-header">
            <span class="tag-opt">OPÇÃO 3</span>
            <span style="font-size: 11px; color: #94a3b8;">Física: Weyl Fermi-Arcs</span>
          </div>
          <div class="card-title">Weyl Semimetal Fermi-Arc Interference</div>
          <p class="card-desc">
            Semi-metal ferromagnético de Weyl com nós quirais W+ e W-: Arcos de Fermi hiperbólicos conectam os polos de Weyl pela superfície com condução balística livre de dissipação, gerando espículas de bombeamento quiral por anomalia eletromagnética.
          </p>
          <div class="features-list">
            <span class="feat-tag">Arcos de Fermi Balísticos</span>
            <span class="feat-tag">Nós Quirais de Weyl W±</span>
            <span class="feat-tag">Anomalia Quiral E·B</span>
          </div>
        </div>
        
        <div class="image-box">
          <img id="img-opt-3" class="pixelated-art halo-active-3" src="{b64_data[3]['ingot']}" alt="Opção 3 Ingot">
        </div>
        
        <div class="card-footer">
          <button id="btn-shader-3" class="btn-card-shader active" onclick="toggleCardShader(3)">Shader Desta Opção: ATIVO</button>
          <button class="btn-approve" onclick="selectOption(3)">ESCOLHER OPÇÃO 3 (WEYL ARCS)</button>
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
        text.style.color = '#60a5fa';
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
    
    html_path = ARTIFACT_DIR / "platinum_manganese_antimony_heusler_alloy_showcase.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
