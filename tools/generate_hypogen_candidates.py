import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/hypogen_candidates")
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

def to_palette_hypogen(gray_val):
    t = gray_val / 255.0
    # Shadow: [62, 30, 16] (deep molten umber)
    # Midtone: [184, 96, 44] (rich stellar bronze-amber)
    # Highlight: [255, 205, 125] (incandescent solar flare gold)
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 62 + s_low * (184 - 62)
    g_low = 30 + s_low * (96 - 30)
    b_low = 16 + s_low * (44 - 16)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 184 + s_high * (255 - 184)
    g_high = 96 + s_high * (205 - 96)
    b_high = 44 + s_high * (125 - 44)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Candidate 1: Solar Fusion Resonance
def make_c1_resonance(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_hypogen(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    edge_mask = np.clip((t_base - 0.20) / 0.80, 0, 1)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        wave1 = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 18.0))
        wave2 = np.cos(2 * np.pi * (t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
        interf = (wave1 + wave2) * 0.5
        
        intensity = interf * 42.0 * edge_mask
        
        # Golden fire boost
        frame[:, :, 0] += intensity * 1.15
        frame[:, :, 1] += intensity * 0.95
        frame[:, :, 2] += intensity * 0.50
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 2: Solar Flare Sweep
def make_c2_sweep(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_hypogen(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = gray / 255.0
    edge_mask = np.clip((t_base - 0.20) / 0.80, 0, 1)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        wave_pos = (f / n_frames) * (w + h + 10) - 5
        diag_dist = (x_coords + y_coords) - wave_pos
        wave = np.exp(-(diag_dist**2) / (2 * (2.2**2)))
        
        flare = wave * 65.0 * edge_mask
        frame[:, :, 0] += flare * 1.20
        frame[:, :, 1] += flare * 1.00
        frame[:, :, 2] += flare * 0.60
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

# Candidate 3: Thermal Core Pulse
def make_c3_pulse(base_arr, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = to_palette_hypogen(gray)
    colored[:, :, 3] = base_arr[:, :, 3]
    
    y_coords, x_coords = np.ogrid[:h, :w]
    r = np.sqrt((x_coords - 7.5)**2 + (y_coords - 7.5)**2)
    r_weight = np.clip(1.0 - r / 12.0, 0.3, 1.0)
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        phase = (f / n_frames) * 2 * np.pi
        pulse = 0.5 + 0.5 * (np.sin(phase) * 0.75 + np.sin(phase * 2) * 0.25)
        
        intensity = pulse * r_weight * 50.0
        frame[:, :, 0] += intensity * 1.15
        frame[:, :, 1] += intensity * 0.90
        frame[:, :, 2] += intensity * 0.45
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def frames_to_b64_gif(frames, scale=5, frametime_ms=100):
    pil_frames = []
    for f in frames:
        im = Image.fromarray(f, mode="RGBA")
        w, h = im.size
        bg = Image.new("RGBA", (w, h), (18, 20, 28, 255))
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
    c1 = make_c1_resonance(base)
    c2 = make_c2_sweep(base)
    c3 = make_c3_pulse(base)
    
    b64_data[name] = {
        "c1_resonance": frames_to_b64_gif(c1),
        "c2_sweep": frames_to_b64_gif(c2),
        "c3_pulse": frames_to_b64_gif(c3)
    }

with open(OUT_DIR / "b64_data.json", "w") as f:
    json.dump(b64_data, f)

print("Generated Hypogen candidate animations!")
