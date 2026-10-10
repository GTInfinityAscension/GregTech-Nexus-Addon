import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path
import colorsys

OUT_DIR = Path("/tmp/chromatic_candidates")
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

# Candidate 1: Prismatic Wave (Diagonal rainbow traveling continuous gradient)
def make_c1_prism(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        # Hue varies diagonally across the item + over time
        hue = (t + (x_coords + y_coords) / 22.0) % 1.0
        
        # Convert hue to RGB map
        r_map = np.zeros((h, w), dtype=np.float32)
        g_map = np.zeros((h, w), dtype=np.float32)
        b_map = np.zeros((h, w), dtype=np.float32)
        
        for y in range(h):
            for x in range(w):
                h_val = hue[y, x]
                # Saturation slightly reduced for sophisticated glass feel (0.80)
                # Value mapped from base shading so shading and bevels are preserved!
                v_val = 0.25 + 0.75 * t_base[y, x]
                s_val = 0.82 if t_base[y, x] < 0.85 else 0.40 # highlights desaturate towards brilliant white
                rgb = colorsys.hsv_to_rgb(h_val, s_val, v_val)
                r_map[y, x] = rgb[0] * 255.0
                g_map[y, x] = rgb[1] * 255.0
                b_map[y, x] = rgb[2] * 255.0
                
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r_map, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g_map, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b_map, 0, 255), 0)
        frame[:, :, 3] = base_arr[:, :, 3].astype(np.uint8)
        frames.append(frame)
    return frames

# Candidate 2: Chromatic Resonance (Global smooth 30-frame color cycle with bevel sheen)
def make_c2_cycle(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        hue = t % 1.0
        r_map = np.zeros((h, w), dtype=np.float32)
        g_map = np.zeros((h, w), dtype=np.float32)
        b_map = np.zeros((h, w), dtype=np.float32)
        
        for y in range(h):
            for x in range(w):
                v_val = 0.25 + 0.75 * t_base[y, x]
                s_val = 0.85 if t_base[y, x] < 0.88 else 0.35
                rgb = colorsys.hsv_to_rgb(hue, s_val, v_val)
                r_map[y, x] = rgb[0] * 255.0
                g_map[y, x] = rgb[1] * 255.0
                b_map[y, x] = rgb[2] * 255.0
                
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r_map, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g_map, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b_map, 0, 255), 0)
        frame[:, :, 3] = base_arr[:, :, 3].astype(np.uint8)
        frames.append(frame)
    return frames

# Candidate 3: Dichroic Prism Shimmer (Electric Cyan/Violet dichroic glass with shifting prism glints)
def make_c3_dichroic(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    
    frames = []
    for f in range(n_frames):
        t = f / n_frames
        # Dichroic glass shifts between cyan-teal (0.50) and violet-magenta (0.85)
        hue_base = 0.52 + 0.30 * (0.5 + 0.5 * np.sin(2 * np.pi * t + (x_coords - y_coords) / 20.0))
        
        # Prism sparkle on highlights
        sparkle = np.sin(2 * np.pi * (t * 2 + (x_coords + y_coords) / 10.0))
        
        r_map = np.zeros((h, w), dtype=np.float32)
        g_map = np.zeros((h, w), dtype=np.float32)
        b_map = np.zeros((h, w), dtype=np.float32)
        
        for y in range(h):
            for x in range(w):
                h_val = hue_base[y, x] % 1.0
                v_val = 0.28 + 0.72 * t_base[y, x]
                if t_base[y, x] > 0.80 and sparkle[y, x] > 0.7:
                    # Prism glint
                    h_val = (h_val + 0.35) % 1.0
                    v_val = min(1.0, v_val + 0.2)
                rgb = colorsys.hsv_to_rgb(h_val, 0.75, v_val)
                r_map[y, x] = rgb[0] * 255.0
                g_map[y, x] = rgb[1] * 255.0
                b_map[y, x] = rgb[2] * 255.0
                
        frame = np.zeros((h, w, 4), dtype=np.uint8)
        frame[:, :, 0] = np.where(alpha, np.clip(r_map, 0, 255), 0)
        frame[:, :, 1] = np.where(alpha, np.clip(g_map, 0, 255), 0)
        frame[:, :, 2] = np.where(alpha, np.clip(b_map, 0, 255), 0)
        frame[:, :, 3] = base_arr[:, :, 3].astype(np.uint8)
        frames.append(frame)
    return frames

def frames_to_b64_gif(frames, scale=5, frametime_ms=100):
    pil_frames = []
    for f in frames:
        im = Image.fromarray(f, mode="RGBA")
        w, h = im.size
        bg = Image.new("RGBA", (w, h), (18, 18, 26, 255))
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
    c1 = make_c1_prism(base)
    c2 = make_c2_cycle(base)
    c3 = make_c3_dichroic(base)
    
    b64_data[name] = {
        "c1_prism": frames_to_b64_gif(c1),
        "c2_cycle": frames_to_b64_gif(c2),
        "c3_dichroic": frames_to_b64_gif(c3)
    }

with open(OUT_DIR / "b64_data.json", "w") as f:
    json.dump(b64_data, f)

print("Generated Chromatic Glass candidate animations!")
