import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/oganesson_candidates")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ROOT = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
MODERNITY_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")

SAMPLES = {
    "ingot": MODERNITY_ITEMS / "ingot.png",
    "plate": MODERNITY_ITEMS / "plate.png",
    "gear": MODERNITY_ITEMS / "gearGt.png",
    "block": MODERNITY_BLOCKS / "block1.png"
}

def load_base(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    h, w = arr.shape[:2]
    if h > w:
        arr = arr[:w, :, :]
    return arr

def to_palette_oganesson(gray_val):
    t = gray_val / 255.0
    # Shadow: [12, 22, 58] (deep midnight navy)
    # Midtone: [20, 57, 127] (0x14397f - Metastable Oganesson royal cobalt)
    # Highlight: [70, 130, 225] (bright polished noble metal sheen)
    mask_low = t < 0.42
    s_low = np.clip(t / 0.42, 0, 1)
    r_low = 10 + s_low * (20 - 10)
    g_low = 18 + s_low * (57 - 18)
    b_low = 52 + s_low * (127 - 52)
    
    s_high = np.clip((t - 0.42) / 0.58, 0, 1)
    r_high = 20 + s_high * (70 - 20)
    g_high = 57 + s_high * (130 - 57)
    b_high = 127 + s_high * (225 - 127)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Candidate 1: Cherenkov Shockwave & Ionizing Scintillations
def make_c1_cherenkov(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_oganesson(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # 5 radioactive ionization scintillation sites (micro-bursts)
    np.random.seed(118) # Element 118!
    valid_coords = np.argwhere((alpha) & (t_base > 0.3))
    burst_indices = [5, 22, 45, 68, 88] if len(valid_coords) > 90 else [0, 4, 8, 12, 16]
    burst_pts = [valid_coords[i % len(valid_coords)] for i in burst_indices]
    burst_phases = [0.08, 0.28, 0.48, 0.68, 0.88] # staggered decay events
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # 1. Cherenkov shock cone wave moving across the lattice
        # High velocity shockwave angled at 30 degrees
        wave_pos = (x_coords * 0.8 + y_coords * 0.6) / 16.0
        # Fast sweep with steep exponential wavefront (shock front)
        phase = (wave_pos - t) % 1.0
        # Cherenkov shock profile: steep rise, trailing wake
        shock = np.exp(-((phase - 0.2) ** 2) / 0.02) * 1.0
        wake = np.where((phase >= 0.2) & (phase < 0.6), np.exp(-(phase - 0.2) * 6.0), 0.0)
        total_cherenkov = (shock + wake * 0.6) * (0.4 + 0.6 * t_base)
        
        # Cherenkov color: intense electric cyan-blue [0, 220, 255]
        frame[:, :, 0] += total_cherenkov * 15.0
        frame[:, :, 1] += total_cherenkov * 110.0
        frame[:, :, 2] += total_cherenkov * 160.0
        
        # 2. Radioactive ionizing scintillation pinprick bursts (exponential half-life decay)
        for (sy, sx), b_phase in zip(burst_pts, burst_phases):
            p_diff = (t - b_phase) % 1.0
            # Instantaneous burst at 0, decaying sharply within ~0.15 of cycle (4-5 frames)
            if p_diff < 0.16:
                decay = np.exp(-p_diff * 22.0) # sharp ionizing spike
                # 3x3 burst kernel with cross
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            dist = abs(dy) + abs(dx)
                            w_burst = (1.2 if dist == 0 else 0.5) * decay
                            # Brilliant ionizing flash [180, 245, 255]
                            frame[ny, nx, 0] += w_burst * 140.0
                            frame[ny, nx, 1] += w_burst * 190.0
                            frame[ny, nx, 2] += w_burst * 210.0
                            
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 2: Relativistic Orbital Shell Contraction (Camadas Eletrônicas Relativísticas)
def make_c2_relativistic_shells(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_oganesson(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # Center of mass of the item
    cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
    cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
    
    dist_from_core = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Concentric relativistic electron shells expanding outward and breathing
        # Wave frequency k = 2 * pi / wavelength
        wavelength = 4.5
        shell_phase = 2 * np.pi * (dist_from_core / wavelength - t)
        
        # Harmonic shell resonance
        shell_val = np.sin(shell_phase) * 0.6 + np.sin(shell_phase * 2.0 - t * 2 * np.pi) * 0.4
        shell_glow = np.clip((shell_val + 0.3) / 1.3, 0, 1) ** 2
        
        # Attenuation by core distance so outer valence boundary is distinctive
        boundary_modulation = np.cos(2 * np.pi * (t + dist_from_core / 10.0)) * 0.25 + 0.75
        effective_glow = shell_glow * boundary_modulation * (0.35 + 0.65 * t_base)
        
        # Intense cobalt-neon royal blue shell glow [50, 130, 255]
        frame[:, :, 0] += effective_glow * 35.0
        frame[:, :, 1] += effective_glow * 90.0
        frame[:, :, 2] += effective_glow * 145.0
        
        # Highlight rim pulsation
        rim_pulse = np.sin(2 * np.pi * t) * 12.0 * (t_base > 0.65)
        frame[:, :, 2] += rim_pulse
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 3: Isomeric Valence Inversion / Dual-Band Spin State (Inversão de Spin Isomérico)
def make_c3_isomeric_spin(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_oganesson(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Dual counter-propagating diagonal valence energy bands
        # Band A: top-left to bottom-right (45 deg)
        phase_a = 2 * np.pi * ((x_coords + y_coords) / 12.0 - t)
        band_a = np.cos(phase_a) ** 4 # Sharp high-energy crests
        
        # Band B: bottom-left to top-right (-45 deg) with opposite speed
        phase_b = 2 * np.pi * ((x_coords - y_coords) / 12.0 + t)
        band_b = np.cos(phase_b) ** 4 # Sharp high-energy crests
        
        # Constructive interference nodes
        node_interference = band_a * band_b # Where the two bands cross
        
        # Color shifting: Band A carries actinide violet, Band B carries electric blue, interference carries ultra-bright cyan
        # Base valence flow
        frame[:, :, 0] += (band_a * 55.0 + node_interference * 80.0) * (0.4 + 0.6 * t_base)
        frame[:, :, 1] += (band_b * 70.0 + node_interference * 130.0) * (0.4 + 0.6 * t_base)
        frame[:, :, 2] += (band_a * 90.0 + band_b * 120.0 + node_interference * 170.0) * (0.4 + 0.6 * t_base)
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def save_gif(frames, out_path, duration=66):
    pil_frames = [Image.fromarray(f) for f in frames]
    # Scale up 5x with nearest neighbor for crisp pixel art preview
    scaled_frames = [f.resize((80, 80), Image.NEAREST) for f in pil_frames]
    scaled_frames[0].save(
        out_path,
        save_all=True,
        append_images=scaled_frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )

def to_base64_gif(gif_path):
    with open(gif_path, "rb") as f:
        return "data:image/gif;base64," + base64.b64encode(f.read()).decode("utf-8")

def main():
    b64_data = {}
    for item_name, path in SAMPLES.items():
        print(f"Processing sample: {item_name} from {path}")
        arr = load_base(path)
        
        f1 = make_c1_cherenkov(arr)
        f2 = make_c2_relativistic_shells(arr)
        f3 = make_c3_isomeric_spin(arr)
        
        p1 = OUT_DIR / f"{item_name}_c1.gif"
        p2 = OUT_DIR / f"{item_name}_c2.gif"
        p3 = OUT_DIR / f"{item_name}_c3.gif"
        
        save_gif(f1, p1)
        save_gif(f2, p2)
        save_gif(f3, p3)
        
        b64_data[item_name] = {
            "c1_cherenkov": to_base64_gif(p1),
            "c2_shells": to_base64_gif(p2),
            "c3_isomeric": to_base64_gif(p3)
        }
        
    with open(OUT_DIR / "b64_data.json", "w") as f:
        json.dump(b64_data, f)
    print("Done! Saved to", OUT_DIR)

if __name__ == "__main__":
    main()
