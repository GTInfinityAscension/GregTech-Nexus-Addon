import os
import math
import numpy as np
from PIL import Image
from pathlib import Path

OUT_DIR = Path("/tmp/ichorium_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/ichorium")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/ichorium/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (200, 150, 50, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (200, 150, 50, 255))

# Opção 1: Celestial Vis Streams (Fluxos Harmônicos de Vis)
def render_option_1(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: âmbar dourado táumico rico
        r = 55.0 + t_base * 165.0
        g = 22.0 + (t_base ** 1.3) * 110.0
        b = 2.0 + (t_base ** 2.2) * 15.0
        
        # Correntes de fluxo laminar curvilíneo entrelaçadas (Vis Streams)
        s1 = np.sin(2 * np.pi * (x_coords * 0.18 - t * 1.6) + np.cos(2 * np.pi * (y_coords * 0.25 + t * 0.8)))
        s2 = np.cos(2 * np.pi * (y_coords * 0.22 + t * 1.4) - np.sin(2 * np.pi * (x_coords * 0.24 - t * 1.0)))
        stream_mix = (s1 * 0.6 + s2 * 0.4)
        streams = np.exp(-(stream_mix**2) / 0.16) * (0.5 + 0.5 * t_base) * (t_base > 0.25)
        
        # Nódulos orbitais de orbes de Vis fluindo pelos canais
        orb_x = 8.0 + np.sin(2 * np.pi * t) * 4.5
        orb_y = 8.0 + np.cos(2 * np.pi * (t * 2.0)) * 4.0
        orb_dist = np.sqrt((x_coords - orb_x)**2 + (y_coords - orb_y)**2)
        orb_glow = np.exp(-orb_dist / 1.5) * 1.3 * (t_base > 0.35)
        
        total_vis = streams * 1.1 + orb_glow
        
        # Cores: ouro solar celestial vivo (#fbbf24 a #f59e0b)
        r += total_vis * 165.0
        g += total_vis * 135.0
        b += total_vis * 35.0
        
        # Cristas sagradas brancas-douradas
        holy_white = np.clip(total_vis - 0.85, 0, 1.2) * 110.0
        r += holy_white * 0.95
        g += holy_white * 0.95
        b += holy_white * 0.80
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 2: Thaumic Mandala Resonance (Geometria Sagrada de 8 Pontas)
def render_option_2(base_arr, n_frames=30):
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
        
        # Paleta Base: bronze âmbar profundo temperado
        r = 48.0 + t_base * 160.0
        g = 18.0 + (t_base ** 1.3) * 105.0
        b = 2.0 + (t_base ** 2.5) * 12.0
        
        # Geometria sagrada octogonal (mandala de 8 pontas)
        rot_angle = angle + 2 * np.pi * t * 0.75
        mandala_petal = np.sin(8.0 * rot_angle)
        
        # Anéis concêntricos de pulso harmônico
        ring_phase = (dist / 2.8 - t * 1.5) % 1.0
        ring_wave = np.exp(-((ring_phase - 0.5) / 0.18)**2)
        
        # Interseção da mandala com os anéis
        mandala = ring_wave * (0.6 + 0.4 * mandala_petal) * (t_base > 0.28)
        
        # Glint nos 8 eixos cardeais e colaterais
        axis_align = np.abs(np.sin(4.0 * rot_angle)) ** 8
        axis_sparks = axis_align * (np.sin(2 * np.pi * (t * 3.0 + dist * 0.5)) ** 12) * (t_base > 0.4) * 1.2
        
        total_mandala = mandala * 1.1 + axis_sparks
        
        # Cores: ouro alquímico puro e âmbar solar
        r += total_mandala * 170.0
        g += total_mandala * 140.0
        b += total_mandala * 25.0
        
        # Cristas centrais incandescentes
        divine_core = np.clip(total_mandala - 0.8, 0, 1.2) * 95.0
        r += divine_core * 0.95
        g += divine_core * 0.95
        b += divine_core * 0.75
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 3: Ichor Divine Crucible (Ascensão de Gotas do Sangue dos Deuses)
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # 5 fontes de ascensão de gotas em x com fases distintas
    drop_x_seeds = [4.0, 7.5, 11.5, 5.5, 9.5]
    drop_phases = [0.0, 0.2, 0.45, 0.65, 0.85]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: âmbar mel rubi profundo
        r = 52.0 + t_base * 170.0
        g = 16.0 + (t_base ** 1.4) * 100.0
        b = 2.0 + (t_base ** 2.2) * 10.0
        
        # Ascensão de micro-gotas de Ichor flutuando para cima (contra a gravidade)
        total_drops = np.zeros((h, w), dtype=np.float32)
        for i, (seed_x, phase) in enumerate(zip(drop_x_seeds, drop_phases)):
            cur_t = (t + phase) % 1.0
            cur_y = 15.0 - cur_t * 15.0
            cur_x = seed_x + np.sin(2 * np.pi * (cur_t * 2.0 + i)) * 1.0
            d = np.sqrt((x_coords - cur_x)**2 + (y_coords - cur_y)**2)
            
            # Gota brilhante com cauda de ascensão
            drop = np.exp(-(d / 1.1)**2) * (1.2 - cur_t * 0.4)
            total_drops += drop
            
        drops_fx = total_drops * (t_base > 0.25)
        
        # Dissolução na borda superior (detonação de luz suave)
        top_dissolve = np.exp(-((y_coords - 2.5) / 1.5)**2) * (np.sin(2 * np.pi * t * 2.0) * 0.5 + 0.5) * 0.6 * (t_base > 0.4)
        
        # Efervescência de fundo no metal líquido
        simmer = (np.sin(2 * np.pi * (t * 3.0 + x_coords * 0.7 + y_coords * 0.5)) ** 10) * 0.45 * (t_base > 0.35)
        
        total_fx = drops_fx + top_dissolve + simmer
        
        # Cores: ouro solar celestial incandescente
        r += total_fx * 175.0
        g += total_fx * 135.0
        b += total_fx * 30.0
        
        # Centros das gotas em branco puro
        white_drop = np.clip(total_fx - 0.9, 0, 1.2) * 105.0
        r += white_drop * 0.95
        g += white_drop * 0.95
        b += white_drop * 0.85
        
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
        (1, "vis_streams", render_option_1),
        (2, "thaumic_mandala", render_option_2),
        (3, "ichor_crucible", render_option_3),
    ]
    
    for opt_idx, opt_name, renderer in options:
        print(f"Gerando Ichorium Opção {opt_idx}: {opt_name}...")
        for shape in shapes:
            base_im = get_base_image(shape)
            base_arr = np.array(base_im, dtype=np.float32)
            frames = renderer(base_arr, n_frames=30)
            
            out_file = OUT_DIR / f"ichorium_opt{opt_idx}_{shape}.gif"
            save_gif(frames, out_file)
            print(f"  ✓ {out_file.name}")
            
    print("Todas as opções para Ichorium geradas com sucesso!")

if __name__ == "__main__":
    main()
