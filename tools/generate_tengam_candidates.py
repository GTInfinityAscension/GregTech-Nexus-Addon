import os
import math
import numpy as np
from PIL import Image
from pathlib import Path

OUT_DIR = Path("/tmp/tengam_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
BLOCK_MODERNITY = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter/block1.png")

def get_base_image(shape):
    if shape == "block":
        if BLOCK_MODERNITY.exists():
            return Image.open(BLOCK_MODERNITY).convert("RGBA")
        return Image.new("RGBA", (16, 16), (150, 200, 100, 255))
    
    file_name = f"{shape}.png"
    p = BASE_MODERNITY / file_name
    if p.exists():
        return Image.open(p).convert("RGBA")
    
    if shape == "gear":
        p = BASE_MODERNITY / "gearGt.png"
        if p.exists():
            return Image.open(p).convert("RGBA")
            
    return Image.new("RGBA", (16, 16), (150, 200, 100, 255))

# Opção 1: Lorentz Flux Lines (Linhas de Indução Dipolar e Força de Lorentz)
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
        
        # Paleta Base: metal magnético verde-oliva profundo
        r = 15.0 + t_base * 90.0
        g = 32.0 + t_base * 160.0
        b = 6.0 + (t_base ** 1.6) * 45.0
        
        # Linhas de indução dipolar magnética: r = R0 * sin^2(theta)
        # Plasma deriva ao longo das linhas
        field_r = (dist + 0.5) / (np.sin(angle)**2 + 0.2)
        flux_phase = (field_r * 0.4 - t * 2.0) % 1.0
        flux_line = np.exp(-((flux_phase - 0.5) / 0.16)**2) * (t_base > 0.25)
        
        # Partículas aceleradas pela força de Lorentz nos polos
        polar_pulse = np.abs(np.sin(angle)) * (np.sin(2 * np.pi * (t * 3.0 + dist * 0.4)) ** 8) * (t_base > 0.4)
        
        total_mag = flux_line * 1.1 + polar_pulse * 0.9
        
        # Cores: verde-limão supercondutor brilhante (#a3e635 a #bef264)
        r += total_mag * 140.0
        g += total_mag * 185.0
        b += total_mag * 35.0
        
        # Cristas elétricas brancas-limão
        electric_core = np.clip(total_mag - 0.8, 0, 1.2) * 110.0
        r += electric_core * 0.90
        g += electric_core * 1.00
        b += electric_core * 0.70
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 2: Quantum Spin Precession (Precessão de Larmor e Magnons)
def render_option_2(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: metal neodímio verde-escuro
        r = 12.0 + t_base * 80.0
        g = 28.0 + t_base * 150.0
        b = 10.0 + (t_base ** 1.5) * 55.0
        
        # Precessão de Larmor: ondas de spin bidimensionais
        w_x = np.sin(2 * np.pi * (x_coords * 0.22 - t * 2.0))
        w_y = np.sin(2 * np.pi * (y_coords * 0.22 - t * 2.0))
        magnon_grid = (w_x * w_y)
        
        # Ondas transversais de magnetização
        spin_wave = np.clip(magnon_grid * 1.3, 0, 1.0) * (t_base > 0.28)
        
        # Ressonância de alta frequência nas arestas
        diag = (x_coords * 0.707 - y_coords * 0.707)
        resonance = (np.sin(2 * np.pi * (t * 4.0 + diag * 0.6)) ** 12) * (t_base > 0.45) * 1.2
        
        total_spin = spin_wave * 1.0 + resonance
        
        # Cores: verde-neon esmeralda (#4ade80 e #22c55e)
        r += total_spin * 95.0
        g += total_spin * 195.0
        b += total_spin * 90.0
        
        # Picos de spin branco-verde
        spin_peak = np.clip(total_spin - 0.75, 0, 1.2) * 90.0
        r += spin_peak * 0.85
        g += spin_peak * 1.00
        b += spin_peak * 0.85
        
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
        frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
        frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
        frame[:, :, 3] = base_arr[:, :, 3]
        frames.append(Image.fromarray(frame))
        
    return frames

# Opção 3: Superconducting Meissner Vortex (Vórtices de Abrikosov e Efeito Meissner)
def render_option_3(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    y_coords, x_coords = np.ogrid[:h, :w]
    
    # Rede triangular de vórtices de Abrikosov
    vortices = [
        (4.0, 4.0), (12.0, 4.0), (8.0, 8.0), (4.0, 12.0), (12.0, 12.0)
    ]
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        
        # Paleta Base: supercondutor verde-ácido profundo
        r = 16.0 + t_base * 85.0
        g = 35.0 + t_base * 165.0
        b = 8.0 + (t_base ** 1.8) * 40.0
        
        # Vórtices de fluxo quântico girando orbitalmente
        total_vortex = np.zeros((h, w), dtype=np.float32)
        for i, (vx, vy) in enumerate(vortices):
            rot_vx = vx + np.cos(2 * np.pi * (t + i / 5.0)) * 1.2
            rot_vy = vy + np.sin(2 * np.pi * (t + i / 5.0)) * 1.2
            d = np.sqrt((x_coords - rot_vx)**2 + (y_coords - rot_vy)**2)
            
            # Núcleo de Londres: decaimento de campo magnético quantizado
            vortex_field = np.exp(-d / 1.6) * (0.6 + 0.4 * np.sin(2 * np.pi * (t * 2.0 - d * 0.8)))
            total_vortex += vortex_field
            
        vortex_fx = total_vortex * (t_base > 0.26)
        
        # Efeito Meissner: repulsão do fluxo para as bordas exteriores
        gy, gx = np.gradient(gray)
        edge_mag = np.sqrt(gx**2 + gy**2)
        norm_edge = edge_mag / max(1.0, np.max(edge_mag))
        meissner_edge = (norm_edge ** 1.5) * (np.sin(2 * np.pi * (t * 1.5 + (x_coords + y_coords) * 0.2)) * 0.4 + 0.6) * (t_base > 0.3)
        
        total_fx = vortex_fx * 1.1 + meissner_edge * 0.7
        
        # Cores: verde-limão elétrico fluorescente (#bef264 a #84cc16)
        r += total_fx * 155.0
        g += total_fx * 195.0
        b += total_fx * 25.0
        
        # Singularidades dos vórtices em branco puro
        vortex_core = np.clip(total_fx - 0.85, 0, 1.2) * 115.0
        r += vortex_core * 0.95
        g += vortex_core * 1.00
        b += vortex_core * 0.75
        
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
        (1, "lorentz_flux", render_option_1),
        (2, "spin_precession", render_option_2),
        (3, "meissner_vortex", render_option_3),
    ]
    
    for opt_idx, opt_name, renderer in options:
        print(f"Gerando Tengam Opção {opt_idx}: {opt_name}...")
        for shape in shapes:
            base_im = get_base_image(shape)
            base_arr = np.array(base_im, dtype=np.float32)
            frames = renderer(base_arr, n_frames=30)
            
            out_file = OUT_DIR / f"tengam_opt{opt_idx}_{shape}.gif"
            save_gif(frames, out_file)
            print(f"  ✓ {out_file.name}")
            
    print("Todas as opções para Tengam geradas com sucesso!")

if __name__ == "__main__":
    main()
