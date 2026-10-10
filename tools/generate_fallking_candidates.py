import os
import math
import numpy as np
from PIL import Image
from pathlib import Path

OUT_DIR = Path("/tmp/fallking_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (255, 207, 107, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (255, 207, 107, 255))

# Opção 1: Helicopter Rotor Blade Sweep (Varredura de Pás de Rotor em Hiper-Rotação)
def render_option_1(base_arr, n_frames=30):
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
        
        # Paleta Base: superliga aeroespacial ouro-titânio aquecido
        r = 65.0 + t_base * 175.0
        g = 42.0 + (t_base ** 1.3) * 145.0
        b = 10.0 + (t_base ** 2.2) * 55.0
        
        # 3 pás de rotor aeroespacial girando a alta velocidade
        blade_angle = angle + 2 * np.pi * t * 3.0
        blade_beam = np.cos(3.0 * blade_angle)
        blade_sweep = (np.maximum(0, blade_beam) ** 8) * (dist / 8.0) * (t_base > 0.25)
        
        # Vórtices na ponta da pá (tip vortex) com estalo de brilho
        tip_pulse = (np.sin(2 * np.pi * (t * 6.0 + angle * 1.5)) ** 12) * np.exp(-((dist - 6.5) / 1.5)**2) * (t_base > 0.4)
        
        total_fx = blade_sweep * 1.2 + tip_pulse * 0.9
        
        # Cores: ouro aeroespacial cintilante
        r += total_fx * 170.0
        g += total_fx * 145.0
        b += total_fx * 45.0
        
        # Picos de vórtice branco puro
        vortex_white = np.clip(total_fx - 0.85, 0, 1.2) * 115.0
        r += vortex_white * 0.95
        g += vortex_white * 0.95
        b += vortex_white * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 2: Centrifugal Gyroscopic Resonance (Precessão Giroscópica Centrífuga)
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
        
        # Paleta Base: ouro-champanhe aeroespacial
        r = 60.0 + t_base * 175.0
        g = 45.0 + (t_base ** 1.3) * 140.0
        b = 14.0 + (t_base ** 2.0) * 60.0
        
        # Giroscópio 1: elipse inclinada precessando a velocidade 1.0
        rot1 = 2 * np.pi * t
        rx1 = (x_coords - cx) * np.cos(rot1) - (y_coords - cy) * np.sin(rot1)
        ry1 = (x_coords - cx) * np.sin(rot1) + (y_coords - cy) * np.cos(rot1)
        el1 = np.sqrt((rx1 / 1.0)**2 + (ry1 / 2.5)**2)
        gyro1 = np.exp(-((el1 - 4.5) / 0.8)**2)
        
        # Giroscópio 2: elipse perpendicular precessando em contra-rotação
        rot2 = -2 * np.pi * (t * 1.5)
        rx2 = (x_coords - cx) * np.cos(rot2) - (y_coords - cy) * np.sin(rot2)
        ry2 = (x_coords - cx) * np.sin(rot2) + (y_coords - cy) * np.cos(rot2)
        el2 = np.sqrt((rx2 / 2.5)**2 + (ry2 / 1.0)**2)
        gyro2 = np.exp(-((el2 - 4.0) / 0.8)**2)
        
        # Picos nos nós de gimbal lock
        nodes = (gyro1 * gyro2) * 2.0
        total_gyro = (gyro1 * 0.7 + gyro2 * 0.7 + nodes) * (t_base > 0.28)
        
        r += total_gyro * 165.0
        g += total_gyro * 135.0
        b += total_gyro * 50.0
        
        node_flash = np.clip(nodes - 0.6, 0, 1.2) * 110.0
        r += node_flash * 0.95
        g += node_flash * 0.95
        b += node_flash * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 3: Turbofan Plasma Compression (Ondas de Choque Transônicas de Turbofan)
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: ouro aeroespacial de pós-combustão
        r = 68.0 + t_base * 170.0
        g = 38.0 + (t_base ** 1.4) * 135.0
        b = 8.0 + (t_base ** 2.3) * 45.0
        
        # Cones de choque Mach oblíquos viajando longitudinalmente
        wave_pos = (t * 24.0) % 24.0
        cone = np.abs((x_coords * 0.8 + y_coords * 0.6) - wave_pos)
        shock_front = np.exp(-(cone / 1.1)**2) * (t_base > 0.25)
        
        # Faixas de compressão de pressão estática periódica
        compress = (np.sin(2 * np.pi * (t * 2.5 - (x_coords - y_coords) * 0.25)) * 0.5 + 0.5) ** 4 * 0.6 * (t_base > 0.35)
        
        total_shock = shock_front * 1.3 + compress
        
        # Cores: ouro quente incandescente e frente Mach
        r += total_shock * 175.0
        g += total_shock * 140.0
        b += total_shock * 30.0
        
        shock_crest = np.clip(total_shock - 0.8, 0, 1.2) * 115.0
        r += shock_crest * 0.95
        g += shock_crest * 0.95
        b += shock_crest * 0.80
        
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
        (1, "rotor_sweep", render_option_1),
        (2, "gyroscopic_resonance", render_option_2),
        (3, "turbofan_compression", render_option_3),
    ]
    
    for opt_idx, opt_name, renderer in options:
        print(f"Gerando Fallking Opção {opt_idx}: {opt_name}...")
        for shape in shapes:
            base_im = get_base_image(shape)
            base_arr = np.array(base_im, dtype=np.float32)
            frames = renderer(base_arr, n_frames=30)
            
            out_file = OUT_DIR / f"fallking_opt{opt_idx}_{shape}.gif"
            save_gif(frames, out_file)
            print(f"  ✓ {out_file.name}")
            
    print("Todas as opções para Fallking geradas com sucesso!")

if __name__ == "__main__":
    main()
