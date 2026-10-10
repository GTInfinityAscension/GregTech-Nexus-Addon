import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/celestial_tungsten_candidates")
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

def to_palette_celestial_tungsten(gray_val):
    t = gray_val / 255.0
    # Shadow: [24, 25, 34] (deep cosmic graphite slate)
    # Midtone: [64, 68, 86] (dense dark celestial tungsten)
    # Highlight: [142, 150, 182] (polished silvery-blue starlight sheen)
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 24 + s_low * (64 - 24)
    g_low = 25 + s_low * (68 - 25)
    b_low = 34 + s_low * (86 - 34)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 64 + s_high * (142 - 64)
    g_high = 68 + s_high * (150 - 68)
    b_high = 86 + s_high * (182 - 86)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Candidate 1: Constellation Sparkle (Micro-centelhas estelares cintilando)
def make_c1_sparkle(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_celestial_tungsten(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    # 6 distinct starlight glint centers on the item
    np.random.seed(42)
    valid_coords = np.argwhere((alpha) & (t_base > 0.35))
    star_indices = [3, 15, 28, 45, 62, 80] if len(valid_coords) > 85 else [0, 5, 10]
    star_pts = [valid_coords[i % len(valid_coords)] for i in star_indices]
    star_phases = [0.0, 0.2, 0.35, 0.55, 0.7, 0.85]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Base subtle ambient starlight wave
        ambient = 12.0 * np.sin(2 * np.pi * (t + (x_coords + y_coords) / 20.0))
        for c, boost in enumerate([0.9, 0.95, 1.15]):
            frame[:, :, c] += ambient * boost
            
        # Starlight sparkles
        for (sy, sx), s_phase in zip(star_pts, star_phases):
            # Sparkle peaks at s_phase
            phase_diff = (t - s_phase) % 1.0
            glint = max(0.0, np.cos(phase_diff * 2 * np.pi)) ** 12
            if glint > 0.05:
                # 3x3 glint cross
                for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)]:
                    ny, nx = sy + dy, sx + dx
                    if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                        val_add = glint * weight * 160.0
                        frame[ny, nx, 0] += val_add * 0.85
                        frame[ny, nx, 1] += val_add * 0.92
                        frame[ny, nx, 2] += val_add * 1.00 # pure brilliant diamond starlight
                        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 2: Celestial Starlight Resonance (Onda de plasma cósmico azul-prateado)
def make_c2_resonance(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_celestial_tungsten(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    edge_mask = np.clip((t_base - 0.18) / 0.82, 0, 1)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        wave1 = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 18.0))
        wave2 = np.cos(2 * np.pi * (t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
        interf = (wave1 + wave2) * 0.5
        
        intensity = interf * 42.0 * edge_mask
        frame[:, :, 0] += intensity * 0.80
        frame[:, :, 1] += intensity * 0.90
        frame[:, :, 2] += intensity * 1.25 # cool starlight sheen
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 3: Stellar Core Pulse (Pulso denso do núcleo de tungstênio)
def make_c3_pulse(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_celestial_tungsten(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    r = np.sqrt((x_coords - 7.5)**2 + (y_coords - 7.5)**2)
    r_weight = np.clip(1.0 - r / 12.0, 0.35, 1.0)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        phase = (f / n_frames) * 2 * np.pi
        pulse = 0.5 + 0.5 * (np.sin(phase) * 0.75 + np.sin(phase * 2) * 0.25)
        
        intensity = pulse * r_weight * 52.0
        frame[:, :, 0] += intensity * 0.85
        frame[:, :, 1] += intensity * 0.95
        frame[:, :, 2] += intensity * 1.20
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def frames_to_b64_gif(frames, scale=5, frametime_ms=100):
    pil_frames = []
    for f in frames:
        im = Image.fromarray(f, mode="RGBA")
        w, h = im.size
        bg = Image.new("RGBA", (w, h), (14, 16, 24, 255))
        bg.paste(im, (0, 0), im)
        scaled = bg.resize((w * scale, h * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
        
    import io
    buf = io.BytesIO()
    pil_frames[0].save(buf, format="GIF", save_all=True, append_images=pil_frames[1:], duration=frametime_ms, loop=0)
    return "data:image/gif;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

b64_data = {}
for name, path in SAMPLES.items():
    base = load_base(path)
    c1 = make_c1_sparkle(base)
    c2 = make_c2_resonance(base)
    c3 = make_c3_pulse(base)
    
    b64_data[name] = {
        "c1_sparkle": frames_to_b64_gif(c1),
        "c2_resonance": frames_to_b64_gif(c2),
        "c3_pulse": frames_to_b64_gif(c3)
    }

with open(OUT_DIR / "b64_data.json", "w") as f:
    json.dump(b64_data, f)

print("Generated Celestial Tungsten candidate animations!")
