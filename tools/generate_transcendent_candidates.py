import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/transcendent_candidates")
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

def to_palette_transcendent(gray_val):
    t = gray_val / 255.0
    # Shadow: [28, 28, 34] (dark dimensional void slate)
    # Midtone: [50, 50, 58] (0x323232 Transcendent Metal titanium charcoal)
    # Highlight: [120, 122, 138] (polished dimensional metal luster)
    mask_low = t < 0.42
    s_low = np.clip(t / 0.42, 0, 1)
    r_low = 18 + s_low * (50 - 18)
    g_low = 18 + s_low * (50 - 18)
    b_low = 22 + s_low * (58 - 22)
    
    s_high = np.clip((t - 0.42) / 0.58, 0, 1)
    r_high = 50 + s_high * (120 - 50)
    g_high = 50 + s_high * (122 - 50)
    b_high = 58 + s_high * (138 - 58)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Candidate 1: 4D Tesseract Spatial Folding (Projeção e Dobra de Hipercubo 4D)
def make_c1_tesseract(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_transcendent(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # 4D Hypercube projection vertices
    # In 4D, a tesseract rotates in the XW or ZW plane:
    # x' = x * cos(theta) - w * sin(theta), w' = x * sin(theta) + w * cos(theta)
    # Project to 2D screen: x_proj = x' / (distance - w'), y_proj = y / (distance - w')
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        theta = 2 * np.pi * t
        
        # Grid of high-dimensional coordinate folding
        # Two folding coordinate systems that twist around each other:
        u = (x_coords - 7.5) * np.cos(theta) - (y_coords - 7.5) * np.sin(theta)
        v = (x_coords - 7.5) * np.sin(theta) + (y_coords - 7.5) * np.cos(theta)
        
        # Tesseract wireframe edge lines: squares folding in 4D space
        # Inner square and outer square connected by isometric diagonals
        scale_inner = 2.5 + 1.2 * np.sin(theta)
        scale_outer = 5.5 - 1.2 * np.sin(theta)
        
        d_inner = np.maximum(np.abs(u), np.abs(v)) - scale_inner
        d_outer = np.maximum(np.abs(u), np.abs(v)) - scale_outer
        
        edge_inner = np.exp(-(d_inner ** 2) / 0.8)
        edge_outer = np.exp(-(d_outer ** 2) / 1.0)
        
        # 4D diagonal connecting vertices
        diag = np.exp(-(np.abs(np.abs(u) - np.abs(v)) ** 2) / 0.6) * (np.abs(u) <= 5.5) * (np.abs(u) >= 1.5)
        
        tesseract_field = (edge_inner * 1.2 + edge_outer * 0.9 + diag * 0.7) * (0.3 + 0.7 * t_base)
        
        # Dimensional silver-cyan-violet luminescence
        frame[:, :, 0] += tesseract_field * 70.0
        frame[:, :, 1] += tesseract_field * 100.0
        frame[:, :, 2] += tesseract_field * 140.0
        
        # Subtle dimensional breathing
        breathe = np.sin(theta * 2) * 8.0 * (t_base > 0.4)
        frame[:, :, 0] += breathe * 0.8
        frame[:, :, 1] += breathe * 0.9
        frame[:, :, 2] += breathe * 1.1
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 2: Gravitational Lensing & Spacetime Curvature (Lente Gravitacional / Anéis de Einstein)
def make_c2_gravitational_lens(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_transcendent(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # Gravitational micro-singularity coordinates (slightly off-center for asymmetry)
    gx, gy = 7.5, 7.5
    r = np.sqrt((x_coords - gx) ** 2 + (y_coords - gy) ** 2)
    angle = np.arctan2(y_coords - gy, x_coords - gx) # [-pi, pi]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Gravitational lensing distortion: Einstein rings with rotating relativistic beaming
        # Relativistic beam angle
        beam_angle = angle - 2 * np.pi * t
        # Beaming intensity: Doppler boosting makes the approaching arc brighter
        doppler = np.clip(np.cos(beam_angle), 0, 1) ** 2
        
        # Two Einstein ring radii: inner photon sphere (r=3.2) and outer lensing caustic (r=5.8)
        ring1 = np.exp(-((r - 3.2) ** 2) / 0.9) * (0.6 + 0.8 * doppler)
        ring2 = np.exp(-((r - 5.8) ** 2) / 1.1) * (0.4 + 0.9 * (1.0 - doppler)) # opposite beam
        
        # Gravitational shear flare
        caustic = (ring1 + ring2) * (0.35 + 0.65 * t_base)
        
        # Luminous spacetime distortion: pearl violet-silver [140, 150, 200]
        frame[:, :, 0] += caustic * 85.0
        frame[:, :, 1] += caustic * 95.0
        frame[:, :, 2] += caustic * 145.0
        
        # Singularity core void (dark center, bright accretion rim)
        rim = np.exp(-((r - 1.8) ** 2) / 0.5) * 45.0
        frame[:, :, 0] += rim * 0.9
        frame[:, :, 1] += rim * 0.9
        frame[:, :, 2] += rim * 1.3
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 3: Spatiotemporal Dimensional Tear (Fendas Espaço-Temporais & Fratura do Vazio)
def make_c3_spatiotemporal_tear(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_transcendent(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # 3 distinct dimensional fissure paths across the geometry
    # Fissure A: diagonal jagged rift (frames 0-10)
    # Fissure B: horizontal cross-cut fissure (frames 10-20)
    # Fissure C: vertical dimensional crack (frames 20-30)
    np.random.seed(999)
    
    # Pre-generate jagged crack coordinates
    crack_a = []
    cx = 3
    for cy in range(3, 13):
        crack_a.append((cy, cx))
        cx += np.random.choice([0, 1, 1])
        
    crack_b = []
    cy = 8
    for cx in range(2, 14):
        crack_b.append((cy, cx))
        cy += np.random.choice([-1, 0, 1])
        
    crack_c = []
    cx = 10
    for cy in range(2, 14):
        crack_c.append((cy, cx))
        cx += np.random.choice([-1, 0, 1])
        
    cracks = [
        (crack_a, 0.0),
        (crack_b, 0.33),
        (crack_c, 0.66)
    ]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Dimensional background void hum
        void_hum = 8.0 * np.sin(2 * np.pi * (t * 2 + (x_coords + y_coords) / 16.0))
        frame[:, :, 2] += void_hum * 1.2
        
        # Process each crack
        for crack_pts, start_phase in cracks:
            p = (t - start_phase) % 1.0
            # Fissure cycle: 0.0 to 0.05 opens violently, 0.05 to 0.18 glows and heals with smoke, >0.18 dormant
            if p < 0.22:
                if p < 0.06:
                    intensity = p / 0.06 # snap open
                else:
                    intensity = np.exp(-(p - 0.06) * 18.0) # exponential healing
                    
                for cy, cx in crack_pts:
                    if 0 <= cy < h and 0 <= cx < w and alpha[cy, cx]:
                        # Brilliant pearlescent rift emission [220, 230, 255]
                        val = intensity * 190.0
                        frame[cy, cx, 0] += val * 0.85
                        frame[cy, cx, 1] += val * 0.95
                        frame[cy, cx, 2] += val * 1.15
                        
                        # Soft glow halo
                        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                                halo = intensity * 70.0
                                frame[ny, nx, 0] += halo * 0.6
                                frame[ny, nx, 1] += halo * 0.7
                                frame[ny, nx, 2] += halo * 1.0
                                
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def save_gif(frames, out_path, duration=66):
    pil_frames = [Image.fromarray(f) for f in frames]
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
        
        f1 = make_c1_tesseract(arr)
        f2 = make_c2_gravitational_lens(arr)
        f3 = make_c3_spatiotemporal_tear(arr)
        
        p1 = OUT_DIR / f"{item_name}_c1.gif"
        p2 = OUT_DIR / f"{item_name}_c2.gif"
        p3 = OUT_DIR / f"{item_name}_c3.gif"
        
        save_gif(f1, p1)
        save_gif(f2, p2)
        save_gif(f3, p3)
        
        b64_data[item_name] = {
            "c1_tesseract": to_base64_gif(p1),
            "c2_lens": to_base64_gif(p2),
            "c3_tear": to_base64_gif(p3)
        }
        
    with open(OUT_DIR / "b64_data.json", "w") as f:
        json.dump(b64_data, f)
    print("Done! Saved to", OUT_DIR)

if __name__ == "__main__":
    main()
