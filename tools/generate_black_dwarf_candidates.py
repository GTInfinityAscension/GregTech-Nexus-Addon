import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/bd_candidates")
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

# Palette 1: Deep Crimson Redshift
def to_palette_crimson(gray_val):
    t = gray_val / 255.0
    # Shadow: [14, 10, 14]
    # Midtone: [38, 22, 28]
    # Highlight: [115, 65, 80]
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 14 + s_low * (38 - 14)
    g_low = 10 + s_low * (22 - 10)
    b_low = 14 + s_low * (28 - 14)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 38 + s_high * (115 - 38)
    g_high = 22 + s_high * (65 - 22)
    b_high = 28 + s_high * (80 - 28)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Palette 2: Void Purple Singularity
def to_palette_void(gray_val):
    t = gray_val / 255.0
    # Shadow: [12, 10, 18]
    # Midtone: [32, 26, 46]
    # Highlight: [95, 80, 135]
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 12 + s_low * (32 - 12)
    g_low = 10 + s_low * (26 - 10)
    b_low = 18 + s_low * (46 - 18)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 32 + s_high * (95 - 32)
    g_high = 26 + s_high * (80 - 26)
    b_high = 46 + s_high * (135 - 46)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Palette 3: Cold Obsidian Silver
def to_palette_obsidian(gray_val):
    t = gray_val / 255.0
    # Shadow: [14, 14, 18]
    # Midtone: [36, 36, 44]
    # Highlight: [105, 108, 125]
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 14 + s_low * (36 - 14)
    g_low = 14 + s_low * (36 - 14)
    b_low = 18 + s_low * (44 - 18)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 36 + s_high * (105 - 36)
    g_high = 36 + s_high * (108 - 36)
    b_high = 44 + s_high * (125 - 44)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

def animate_dark_resonance(base_arr, palette_fn, r_boost, g_boost, b_boost, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored_rgb = palette_fn(gray)
    
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = colored_rgb
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    edge_mask = np.clip((t_base - 0.18) / 0.82, 0, 1)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Dual wave pattern (reverse direction: matter collapsing inward)
        wave1 = np.sin(2 * np.pi * (-t + (x_coords + y_coords) / 18.0))
        wave2 = np.cos(2 * np.pi * (-t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
        interf = (wave1 + wave2) * 0.5
        
        intensity = interf * 40.0 * edge_mask
        
        frame[:, :, 0] += intensity * r_boost
        frame[:, :, 1] += intensity * g_boost
        frame[:, :, 2] += intensity * b_boost
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def frames_to_b64_gif(frames, scale=5, frametime_ms=100):
    pil_frames = []
    for f in frames:
        im = Image.fromarray(f, mode="RGBA")
        w, h = im.size
        # Background: dark contrast slate #0a0b12 so the dark pixels are clearly distinguishable
        bg = Image.new("RGBA", (w, h), (14, 16, 26, 255))
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
    # Option 1: Crimson Redshift
    c1 = animate_dark_resonance(base, to_palette_crimson, 1.35, 0.55, 0.70)
    # Option 2: Void Purple
    c2 = animate_dark_resonance(base, to_palette_void, 0.90, 0.70, 1.40)
    # Option 3: Cold Obsidian
    c3 = animate_dark_resonance(base, to_palette_obsidian, 0.95, 1.00, 1.15)
    
    b64_data[name] = {
        "c1_crimson": frames_to_b64_gif(c1),
        "c2_void": frames_to_b64_gif(c2),
        "c3_obsidian": frames_to_b64_gif(c3)
    }

with open(OUT_DIR / "b64_data.json", "w") as f:
    json.dump(b64_data, f)

print("Generated Black Dwarf candidate animations!")
