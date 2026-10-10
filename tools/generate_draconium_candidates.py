import os
import math
import numpy as np
from PIL import Image
from pathlib import Path

OUT_DIR = Path("/tmp/draconium_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/draconium")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/draconium/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (150, 150, 150, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (150, 150, 150, 255))

# Opção 1: Crystalline Dragon Matrix (Facetas Lapidadas & Refração Interna)
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Gerar facetas geométricas Voronoi lapidadas
    np.random.seed(137)
    pts = np.array([
        [2.5, 3.0], [8.0, 2.0], [13.5, 3.5],
        [4.0, 7.5], [8.5, 8.5], [13.0, 8.0],
        [3.0, 13.0], [8.0, 14.0], [13.5, 12.5]
    ])
    
    # Distâncias aos pontos e índices das facetas
    dists = [np.sqrt((x_coords - p[0])**2 + (y_coords - p[1])**2) for p in pts]
    dists_arr = np.array(dists)
    closest_facet = np.argmin(dists_arr, axis=0)
    
    # Normais simuladas das facetas para reflexão de luz
    facet_normals = np.random.uniform(-0.8, 0.8, size=(len(pts), 2))
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: metal obsidiana roxo abissal profundo
        r = 18.0 + t_base * 75.0
        g = 4.0 + (t_base ** 1.3) * 22.0
        b = 32.0 + t_base * 125.0
        
        # Vetor de luz interna orbitante
        lx = np.cos(2 * np.pi * t)
        ly = np.sin(2 * np.pi * t)
        
        # Reflexão interna por faceta
        cur_nx = facet_normals[closest_facet, 0]
        cur_ny = facet_normals[closest_facet, 1]
        dot_light = np.clip(cur_nx * lx + cur_ny * ly, 0, 1)
        
        # Refração interna e brilho prismático nas facetas
        internal_refract = (dot_light ** 1.8) * 1.4 * (t_base > 0.3)
        
        # Glints cintilantes nos cantos das facetas
        d_sorted = np.sort(dists_arr, axis=0)
        edge_facet = np.exp(-((d_sorted[1] - d_sorted[0]) / 0.7)**2)
        glint_pulse = (np.sin(2 * np.pi * (t * 2.0 + closest_facet * 0.4)) ** 14) * 1.2
        glints = edge_facet * glint_pulse * (t_base > 0.45)
        
        # Cores:
        # Violeta dracônico radiante nas facetas
        r += internal_refract * 120.0
        g += internal_refract * 25.0
        b += internal_refract * 170.0
        
        # Glints ultravioleta / lavanda cintilante
        r += glints * 180.0
        g += glints * 130.0
        b += glints * 240.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 2: Void Dragon Breathing Waves (Respiração Ondulatória Especular)
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: púrpura escuro metálico acetinado
        r = 22.0 + t_base * 80.0
        g = 5.0 + (t_base ** 1.4) * 20.0
        b = 38.0 + t_base * 135.0
        
        # 1. Ondas de névoa de plasma do vácuo deslizando suavemente
        w1 = np.sin(2 * np.pi * (x_coords * 0.12 + y_coords * 0.28 - t * 1.5))
        w2 = np.cos(2 * np.pi * (y_coords * 0.22 - x_coords * 0.14 + t * 0.9))
        combined_wave = ((w1 * 0.6 + w2 * 0.4) * 0.5 + 0.5) ** 2.2
        
        plasma_mist = combined_wave * (t_base > 0.25) * 1.3
        
        # 2. Respiração profunda do vácuo no centroide
        breath = (np.sin(2 * np.pi * t) * 0.5 + 0.5) ** 1.5
        core_breath = np.exp(-dist / 3.8) * breath * 0.8 * (t_base > 0.3)
        
        # 3. Crista de luz especular diagonal
        diag = (x_coords * 0.8 + y_coords * 0.6)
        spec = np.exp(-((diag - ((t * 24.0) % 24.0)) / 1.8)**2) * 0.7 * (t_base > 0.5)
        
        total_fx = plasma_mist + core_breath + spec
        
        # Aplicação de cores: orquídea e magenta cósmico
        r += total_fx * 135.0
        g += total_fx * 35.0
        b += total_fx * 190.0
        
        # Cristas lavanda suaves
        white_shimmer = np.clip(total_fx - 0.9, 0, 1.0) * 80.0
        r += white_shimmer * 0.8
        g += white_shimmer * 0.7
        b += white_shimmer * 1.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 3: Draconic Rune Pulse & Lattice (Batimento Cardíaco Bio-Mecânico)
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
    
    # Linhas de rede hexagonal / rúnica
    hex1 = np.abs((x_coords * 1.0 + y_coords * 0.577) % 3.6 - 1.8)
    hex2 = np.abs((x_coords * 1.0 - y_coords * 0.577) % 3.6 - 1.8)
    hex3 = np.abs((y_coords * 1.155) % 3.6 - 1.8)
    lattice_lines = np.exp(-np.minimum(np.minimum(hex1, hex2), hex3) * 2.5) * (t_base > 0.28)
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: grafite-ametista temperado
        r = 16.0 + t_base * 70.0
        g = 4.0 + (t_base ** 1.3) * 18.0
        b = 30.0 + t_base * 115.0
        
        # Função de batimento cardíaco biológico (sístole + diástole rápida)
        # Pico 1 a t=0.2, Pico 2 a t=0.38
        t_phase = (t - dist / 16.0) % 1.0
        beat1 = np.exp(-((t_phase - 0.22) / 0.05)**2) * 1.2
        beat2 = np.exp(-((t_phase - 0.38) / 0.045)**2) * 0.85
        heartbeat = beat1 + beat2
        
        # Pulso na rede hexagonal
        lattice_glow = lattice_lines * (0.35 + 0.85 * heartbeat)
        
        # Choque no núcleo central durante o batimento
        core_shock = np.exp(-dist / 3.0) * heartbeat * 1.1
        
        # Picos de arco elétrico nos nós da rede
        nodes = (lattice_lines > 0.5) * heartbeat * 0.9
        
        total_beat = lattice_glow + core_shock + nodes
        
        # Cores: violeta elétrico incandescente (#8b00ff a #b026ff)
        r += total_beat * 145.0
        g += total_beat * 30.0
        b += total_beat * 215.0
        
        # Picos de choque lilás-branco
        white_shock = np.clip(total_beat - 0.8, 0, 1.2) * 95.0
        r += white_shock * 0.9
        g += white_shock * 0.85
        b += white_shock * 1.0
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

def save_gif(frames, out_path):
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        disposal=2
    )

def main():
    shapes = ["ingot", "plate", "gear", "block"]
    options = [
        (1, "crystalline_matrix", render_option_1),
        (2, "void_waves", render_option_2),
        (3, "rune_heartbeat", render_option_3),
    ]
    
    for opt_idx, opt_name, renderer in options:
        print(f"Gerando Draconium Opção {opt_idx}: {opt_name}...")
        for shape in shapes:
            base_im = get_base_image(shape)
            base_arr = np.array(base_im, dtype=np.float32)
            frames = renderer(base_arr, n_frames=30)
            
            out_file = OUT_DIR / f"draconium_opt{opt_idx}_{shape}.gif"
            save_gif(frames, out_file)
            print(f"  ✓ {out_file.name}")
            
    print("Todas as opções para Draconium geradas com sucesso!")

if __name__ == "__main__":
    main()
