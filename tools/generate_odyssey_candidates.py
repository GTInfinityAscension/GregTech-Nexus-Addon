import os
import math
import base64
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/tmp/odyssey_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/9c95a421-582d-4dd9-a627-e59f2d3d6c06")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (76, 122, 106, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (76, 122, 106, 255))

# =========================================================================
# Opção 1: Sub-Atomic Nano-Lattice Weave (Trama de Nano-Rede Subatômica)
# =========================================================================
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Rotação da treliça a 30 graus
    theta = np.pi / 6.0
    u = (x_coords * np.cos(theta) + y_coords * np.sin(theta)) * 1.6
    v = (-x_coords * np.sin(theta) + y_coords * np.cos(theta)) * 1.6
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Superliga titânio-ciano espacial escuro
        r = 18.0 + t_base * 75.0
        g = 36.0 + (t_base ** 1.15) * 115.0
        b = 32.0 + (t_base ** 1.25) * 98.0
        
        # Linhas de nano-fios da treliça molecular
        dist_u = np.abs((u % 2.5) - 1.25)
        dist_v = np.abs((v % 2.5) - 1.25)
        wire_u = np.exp(-((dist_u / 0.38) ** 2))
        wire_v = np.exp(-((dist_v / 0.38) ** 2))
        lattice = (wire_u + wire_v) * 0.75
        
        # Pacotes de dados quânticos coerentes trafegando nos fios
        pulse_u = np.exp(-(((u - t * 5.0) % 5.0 - 2.5) / 0.45) ** 2) * wire_u
        pulse_v = np.exp(-(((v + t * 5.0) % 5.0 - 2.5) / 0.45) ** 2) * wire_v
        
        # Nós quânticos nos cruzamentos moleculares
        nodes = (wire_u * wire_v) * 2.2 * (0.8 + 0.4 * np.sin(2 * np.pi * (t * 2.0 + (u + v) / 4.0)))
        
        total_fx = (lattice * 0.45 + (pulse_u + pulse_v) * 1.4 + nodes) * (t_base > 0.25)
        
        # Brilho de condutividade turquesa/ciano-elétrico
        r += total_fx * 55.0
        g += total_fx * 185.0
        b += total_fx * 165.0
        
        # Picos de fluorescência quântica branca
        flash = np.clip(total_fx - 0.75, 0, 1.5) * 125.0
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
# Opção 2: Nanite Swarm Self-Assembly (Enxame de Nanites em Auto-Montagem)
# =========================================================================
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Superliga metalizada densa ciano-esmeralda
        r = 16.0 + t_base * 78.0
        g = 34.0 + (t_base ** 1.2) * 125.0
        b = 28.0 + (t_base ** 1.3) * 105.0
        
        # 4 núcleos móveis de enxame de nanites em órbitas Lissajous
        nanite_field = np.zeros((h, w), dtype=np.float32)
        
        attractors = [
            (cx + 4.2 * np.cos(2 * np.pi * t), cy + 4.2 * np.sin(2 * np.pi * t)),
            (cx + 4.5 * np.cos(-2 * np.pi * t * 1.5 + 1.2), cy + 3.2 * np.sin(-2 * np.pi * t * 1.5 + 1.2)),
            (cx + 3.0 * np.sin(2 * np.pi * t * 2.0), cy + 4.0 * np.cos(2 * np.pi * t * 2.0)),
            (cx + 3.8 * np.cos(2 * np.pi * t + np.pi), cy + 3.8 * np.sin(2 * np.pi * t + np.pi))
        ]
        
        for ax, ay in attractors:
            d = np.sqrt((x_coords - ax)**2 + (y_coords - ay)**2)
            nanite_field += np.exp(-((d / 1.6)**2)) * 1.1
            
        # Filamentos de montagem conectando os nanites
        interf = np.sin(nanite_field * 4.0 - 2 * np.pi * t * 2.0)
        assembly_mesh = (nanite_field * 0.8 + np.maximum(0, interf) * 0.6) * (t_base > 0.3)
        
        # Picos de solda a frio / sinterização nanotecnológica
        weld_flash = np.clip(assembly_mesh - 1.1, 0, 1.4) * 140.0
        
        # Cores: verde-menta elétrico e ciano brilhante
        r += assembly_mesh * 40.0 + weld_flash * 0.85
        g += assembly_mesh * 195.0 + weld_flash * 1.00
        b += assembly_mesh * 160.0 + weld_flash * 0.95
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# =========================================================================
# Opção 3: Quantum Coherence Hex-Field (Campo de Coerência Quântica Hexagonal)
# =========================================================================
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    angle = np.arctan2(y_coords - cy, x_coords - cx)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: Superliga aeroespacial de Naquadria-Trinium
        r = 14.0 + t_base * 72.0
        g = 32.0 + (t_base ** 1.25) * 128.0
        b = 30.0 + (t_base ** 1.35) * 118.0
        
        # Simetria Hexagonal (ordem 6) modulando o raio
        hex_mod = np.cos(6.0 * angle)
        eff_radius = dist * (1.0 + 0.18 * hex_mod)
        
        # Onda de coerência quântica propagando-se em direção às bordas
        wave1 = np.sin(2 * np.pi * (eff_radius / 3.6 - t * 2.0))
        wave2 = np.cos(2 * np.pi * (eff_radius / 5.2 + t * 1.5))
        coherence = ((wave1 * 0.6 + wave2 * 0.4) + 1.0) * 0.5
        coherence_ring = (coherence ** 3.5) * (t_base > 0.28)
        
        # Anel de ressonância hexagonal estacionário
        hex_lattice = np.exp(-((np.abs(np.sin(eff_radius * 1.5 - hex_mod * 0.5)) - 0.75) / 0.25)**2)
        total_hex = (coherence_ring * 1.3 + hex_lattice * 0.55) * (t_base > 0.25)
        
        # Refracção dielétrica iridescente: ciano-água-marinha e verde-esmeralda quântico
        r += total_hex * 45.0
        g += total_hex * 190.0
        b += total_hex * 185.0
        
        # Picos de coerência supercrítica
        crest = np.clip(total_hex - 0.85, 0, 1.5) * 130.0
        r += crest * 0.90
        g += crest * 0.98
        b += crest * 1.00
        
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
    print("Renderizando candidatos para Odyssey Nano Superalloy...")
    shapes = ["ingot", "gear", "block"]
    
    # 1. Gerar frames para cada opção e forma
    all_frames = {}
    options = [
        ("opt1", "Sub-Atomic Nano-Lattice Weave", render_option_1),
        ("opt2", "Nanite Swarm Self-Assembly", render_option_2),
        ("opt3", "Quantum Coherence Hex-Field", render_option_3)
    ]
    
    for opt_id, opt_name, render_fn in options:
        all_frames[opt_id] = {}
        for s in shapes:
            base_im = get_base_image(s)
            base_arr = np.array(base_im)
            frames = render_fn(base_arr, n_frames=30)
            all_frames[opt_id][s] = frames
            
            gif_path = OUT_DIR / f"{opt_id}_{s}.gif"
            create_gif(frames, gif_path)
            print(f"  ✓ Gerado: {gif_path.name}")

    # 2. Criar Imagem de Grid Comparativo em Alta Resolução (128px por ícone)
    # 3 Linhas (Opção 1, 2, 3), 3 Colunas (Ingot, Gear, Block)
    # Tamanho de cada célula: 128x128. Com margens e títulos:
    cell_size = 128
    pad_x = 40
    pad_y = 20
    header_h = 65
    label_h = 35
    
    grid_w = 660
    grid_h = header_h + (label_h + cell_size + pad_y) * 3 + pad_y
    
    grid_img = Image.new("RGBA", (grid_w, grid_h), (11, 20, 18, 255)) # Dark nano-teal background
    draw = ImageDraw.Draw(grid_img)
    
    font_title = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 15)
    font_sub = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 11)
    font_opt = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 12)
    
    # Título Principal
    draw.text((pad_x, 14), "ODYSSEY NANO SUPERALLOY — VISUAL CANDIDATES (128x128)", fill=(72, 242, 197, 255), font=font_title)
    draw.text((pad_x, 38), "30 Frames Fluidos • Ingot, Gear, Block • GTNA Advanced Materials", fill=(148, 163, 158, 255), font=font_sub)
    
    # Carregar frame 10 (meio do ciclo) de cada um para o grid estático comparativo
    opt_y = header_h
    opt_labels = [
        "OPÇÃO 1: Sub-Atomic Nano-Lattice Weave (Trama de Nano-Rede Subatômica)",
        "OPÇÃO 2: Nanite Swarm Self-Assembly (Enxame de Nanites em Auto-Montagem)",
        "OPÇÃO 3: Quantum Coherence Hex-Field (Campo de Coerência Quântica Hexagonal)"
    ]
    
    for idx, (opt_id, opt_name, _) in enumerate(options):
        # Header da opção
        draw.text((pad_x, opt_y), opt_labels[idx], fill=(240, 253, 244, 255), font=font_opt)
        opt_y += label_h
        
        spacing = (grid_w - 2 * pad_x - 3 * cell_size) // 2
        for col_idx, s in enumerate(shapes):
            x = pad_x + col_idx * (cell_size + spacing)
            frame_img = all_frames[opt_id][s][10] # frame 10
            # Redimensionar para 128x128 usando NEAREST para preservar pixel art pura
            scaled = frame_img.resize((cell_size, cell_size), Image.NEAREST)
            
            # Fundo quadriculado sutil para transparência
            for by in range(0, cell_size, 16):
                for bx in range(0, cell_size, 16):
                    c = (24, 38, 33) if (bx // 16 + by // 16) % 2 == 0 else (18, 29, 25)
                    draw.rectangle([x + bx, opt_y + by, x + bx + 15, opt_y + by + 15], fill=c)
            
            grid_img.paste(scaled, (x, opt_y), scaled)
            # Borda do slot
            draw.rectangle([x - 1, opt_y - 1, x + cell_size, opt_y + cell_size], outline=(45, 212, 191, 120), width=1)
            
        opt_y += cell_size + pad_y
        
    grid_png_path = ARTIFACT_DIR / "odyssey_grid.png"
    grid_img.save(grid_png_path)
    print(f"  ✓ Grid comparativo PNG salvo em: {grid_png_path}")

    # 3. Gerar Showcase HTML Autossuficiente com GIFs Base64 Embutidos e CSS Puro
    def b64_gif(opt_id, shape):
        p = OUT_DIR / f"{opt_id}_{shape}.gif"
        return base64.b64encode(p.read_bytes()).decode("utf-8")

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Odyssey Nano Superalloy — Visual Candidates Showcase</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #091311;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            padding: 30px;
            line-height: 1.5;
        }}
        .header {{
            background: linear-gradient(135deg, #0e241f 0%, #134e4a 100%);
            border: 1px solid #14b8a6;
            border-radius: 12px;
            padding: 24px 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px -5px rgba(20, 184, 166, 0.2);
        }}
        .badge {{
            display: inline-block;
            background: #0d9488;
            color: #ccfbf1;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            padding: 4px 10px;
            border-radius: 9999px;
            margin-bottom: 12px;
        }}
        h1 {{ font-size: 26px; font-weight: 800; color: #f0fdfa; margin-bottom: 6px; }}
        .subtitle {{ font-size: 14px; color: #99f6e4; }}
        
        .shader-alert {{
            background: rgba(13, 148, 136, 0.15);
            border: 1px solid #2dd4bf;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 28px;
            font-size: 13px;
            color: #ccfbf1;
        }}
        .shader-alert strong {{ color: #5eead4; }}
        
        .grid-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
            margin-bottom: 32px;
        }}
        .card {{
            background: #0d1e1a;
            border: 1px solid #194339;
            border-radius: 12px;
            padding: 22px;
            display: flex;
            flex-direction: column;
            transition: all 0.2s ease;
        }}
        .card:hover {{
            border-color: #2dd4bf;
            box-shadow: 0 8px 24px -4px rgba(45, 212, 191, 0.25);
            transform: translateY(-2px);
        }}
        .card-header {{
            border-bottom: 1px solid #1e3a32;
            padding-bottom: 14px;
            margin-bottom: 16px;
        }}
        .opt-title {{ font-size: 17px; font-weight: 700; color: #5eead4; margin-bottom: 4px; }}
        .opt-desc {{ font-size: 12px; color: #94a3b8; }}
        
        .preview-row {{
            display: flex;
            justify-content: space-around;
            background: #060e0d;
            border: 1px solid #162f27;
            border-radius: 8px;
            padding: 16px 10px;
            margin-bottom: 18px;
        }}
        .preview-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }}
        .pixel-art {{
            width: 128px !important;
            height: 128px !important;
            image-rendering: pixelated;
            image-rendering: -moz-crisp-edges;
            image-rendering: crisp-edges;
            border-radius: 6px;
            background: #091311;
            padding: 4px;
            border: 1px solid #1a3c33;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }}
        
        /* Shaders simulados via CSS filters */
        .shader-glow-edge {{
            filter: drop-shadow(0 0 1px #5eead4) drop-shadow(0 0 4px #14b8a6) drop-shadow(0 0 10px rgba(20, 184, 166, 0.5));
        }}
        .shader-halo {{
            filter: drop-shadow(0 0 8px #2dd4bf) drop-shadow(0 0 16px rgba(45, 212, 191, 0.4));
        }}
        
        .item-label {{
            font-size: 11px;
            font-weight: 600;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .physics-box {{
            background: #081714;
            border: 1px solid #133329;
            border-radius: 6px;
            padding: 12px;
            font-size: 12px;
            color: #cbd5e1;
            margin-bottom: 16px;
            flex-grow: 1;
        }}
        .physics-box ul {{ padding-left: 18px; margin-top: 6px; }}
        .physics-box li {{ margin-bottom: 4px; }}
        
        .specs {{
            font-size: 11px;
            color: #64748b;
            border-top: 1px solid #142d25;
            padding-top: 10px;
        }}
        
        .vote-footer {{
            background: #0c1c18;
            border: 1px solid #1a4439;
            border-radius: 10px;
            padding: 20px 24px;
            text-align: center;
        }}
        .vote-footer h3 {{ font-size: 16px; color: #f0fdfa; margin-bottom: 8px; }}
        .vote-footer p {{ font-size: 13px; color: #94a3b8; }}
        .vote-options {{
            display: inline-flex;
            gap: 16px;
            margin-top: 14px;
        }}
        .btn-opt {{
            background: #134e4a;
            color: #f0fdfa;
            border: 1px solid #2dd4bf;
            padding: 8px 20px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 14px;
        }}
    </style>
</head>
<body>

    <div class="header">
        <span class="badge">GTNA Material Overhaul • GTO Space-Era</span>
        <h1>Odyssey Nano Superalloy (Tr₁₄Nq₈Mo₁₇ • #4c7a6a)</h1>
        <p class="subtitle">Superliga nanotecnológica espacial de Trinium, Naquadria e Molibdênio • 3 Propostas Visuais Exclusivas em 30 Frames Fluidos (128×128)</p>
    </div>

    <div class="shader-alert">
        <strong>⚡ Original Shader Integration:</strong> Os modelos JSON serão gerados com o shader <code>gtna:glow_edge</code> (com contorno nanotecnológico ciano-elétrico <code>#2dd4bf</code>) ou <code>gtna:halo</code>, reproduzindo a iluminação física em tempo real no cliente 1.20.1!
    </div>

    <div class="grid-container">
        <!-- OPÇÃO 1 -->
        <div class="card">
            <div class="card-header">
                <div class="opt-title">Opção 1: Sub-Atomic Nano-Lattice Weave</div>
                <div class="opt-desc">Trama geométrica de nano-fios de Trinium com pacotes de dados quânticos</div>
            </div>
            <div class="preview-row">
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt1', 'ingot')}" alt="Ingot 1">
                    <span class="item-label">Ingot</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt1', 'gear')}" alt="Gear 1">
                    <span class="item-label">Gear</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt1', 'block')}" alt="Block 1">
                    <span class="item-label">Block</span>
                </div>
            </div>
            <div class="physics-box">
                <strong>Fundamentos Físico-Matemáticos:</strong>
                <ul>
                    <li>Treliça molecular orientada a 30° com periodicidade nanométrica de alta densidade.</li>
                    <li>Pacotes de dados coerentes viajam em sentidos opostos pelos eixos <code>u</code> e <code>v</code>.</li>
                    <li>Nós moleculares pulsam em sincronicidade com micro-estalos de fluorescência turquesa.</li>
                </ul>
            </div>
            <div class="specs">
                Paleta: Titânio espacial escuro (#12241f) • Matriz (#4c7a6a) • Linhas quânticas (#34d399) • Picos (#f0fdf4)
            </div>
        </div>

        <!-- OPÇÃO 2 -->
        <div class="card">
            <div class="card-header">
                <div class="opt-title">Opção 2: Nanite Swarm Self-Assembly</div>
                <div class="opt-desc">Auto-reparação por enxame de nanorrobôs com solda iônica instantânea</div>
            </div>
            <div class="preview-row">
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt2', 'ingot')}" alt="Ingot 2">
                    <span class="item-label">Ingot</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt2', 'gear')}" alt="Gear 2">
                    <span class="item-label">Gear</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt2', 'block')}" alt="Block 2">
                    <span class="item-label">Block</span>
                </div>
            </div>
            <div class="physics-box">
                <strong>Fundamentos Físico-Matemáticos:</strong>
                <ul>
                    <li>4 atratores de enxame nanite em trajetórias orbitais Lissajous acopladas.</li>
                    <li>Campos de polimerização que formam pontes cinemáticas de plasma verde-menta.</li>
                    <li>Sinterização a frio estocástica com flashes supercríticos incandescentes nos vértices.</li>
                </ul>
            </div>
            <div class="specs">
                Paleta: Base esmeralda-ciano (#10221c) • Chapa (#3d6b5e) • Trilhas nanite (#2dd4bf) • Solda flash (#ffffff)
            </div>
        </div>

        <!-- OPÇÃO 3 -->
        <div class="card">
            <div class="card-header">
                <div class="opt-title">Opção 3: Quantum Coherence Hex-Field</div>
                <div class="opt-desc">Blindagem de Naquadria com simetria hexagonal pura e ondas de Chladni</div>
            </div>
            <div class="preview-row">
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt3', 'ingot')}" alt="Ingot 3">
                    <span class="item-label">Ingot</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt3', 'gear')}" alt="Gear 3">
                    <span class="item-label">Gear</span>
                </div>
                <div class="preview-item">
                    <img class="pixel-art shader-glow-edge" src="data:image/gif;base64,{b64_gif('opt3', 'block')}" alt="Block 3">
                    <span class="item-label">Block</span>
                </div>
            </div>
            <div class="physics-box">
                <strong>Fundamentos Físico-Matemáticos:</strong>
                <ul>
                    <li>Simetria de ordem 6 (cos(6θ)) modulando o tensor de tensão quântica radial.</li>
                    <li>Ondas acústico-quânticas concêntricas de interferência construtiva/destrutiva.</li>
                    <li>Reflexos dielétricos com transição suave entre esmeralda escuro e ciano elétrico brilhante.</li>
                </ul>
            </div>
            <div class="specs">
                Paleta: Sombra titânio profundo (#0e1f1a) • Base (#4c7a6a) • Ressonância (#22d3ee) • Cristas (#f0fdfa)
            </div>
        </div>
    </div>

    <div class="vote-footer">
        <h3>Qual das opções você prefere para o Odyssey Nano Superalloy?</h3>
        <p>Responda <strong>1</strong>, <strong>2</strong> ou <strong>3</strong> para aplicar instantaneamente os 28 itens, 2 blocos e shader no mod!</p>
        <div class="vote-options">
            <span class="btn-opt">Opção 1: Nano-Lattice Weave</span>
            <span class="btn-opt">Opção 2: Nanite Swarm</span>
            <span class="btn-opt">Opção 3: Quantum Hex-Field</span>
        </div>
    </div>

</body>
</html>
"""
    html_path = ARTIFACT_DIR / "odyssey_showcase.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Showcase HTML salvo em: {html_path}")

if __name__ == "__main__":
    main()
