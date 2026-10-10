import numpy as np
from PIL import Image
import os
import json
import base64
from pathlib import Path

OUT_DIR = Path("/tmp/hypogen_compare")
OUT_DIR.mkdir(parents=True, exist_ok=True)

ROOT = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
MODERNITY_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")
COIL_PATH = ROOT / "src/main/resources/assets/gtna/textures/block/casings/coils/machine_coil_hypogen.png"

def load_base(path):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im, dtype=np.float32)
    h, w = arr.shape[:2]
    if h > w:
        arr = arr[:w, :, :]
    return arr

# Exact Coil-matched vibrant orange palette
def palette_coil_orange(gray_val):
    t = gray_val / 255.0
    # Shadow: [70, 36, 12] (deep amber shadow)
    # Midtone: [215, 125, 42] (vibrant hypogen coil glowing orange)
    # Highlight: [255, 228, 140] (solar incandescent filament highlight)
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 70 + s_low * (215 - 70)
    g_low = 36 + s_low * (125 - 36)
    b_low = 12 + s_low * (42 - 12)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 215 + s_high * (255 - 215)
    g_high = 125 + s_high * (228 - 125)
    b_high = 42 + s_high * (140 - 42)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])

# Earlier bronze test
def palette_bronze(gray_val):
    t = gray_val / 255.0
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

def animate_resonance_with_palette(base_arr, palette_fn, r_boost, g_boost, b_boost, n_frames=30):
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    colored = np.zeros_like(base_arr)
    colored[:, :, :3] = palette_fn(gray)
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
        frame[:, :, 0] += intensity * r_boost
        frame[:, :, 1] += intensity * g_boost
        frame[:, :, 2] += intensity * b_boost
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def frames_to_b64(frames, scale=5, frametime_ms=100):
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

# Extract Coil GIF (first 16 frames)
im_coil = Image.open(COIL_PATH).convert("RGBA")
coil_frames = []
for i in range(16):
    f = np.array(im_coil.crop((0, i*16, 16, (i+1)*16)))
    coil_frames.append(f)
coil_b64 = frames_to_b64(coil_frames)

# Compare Ingot in both palettes
ingot_base = load_base(MODERNITY_ITEMS / "ingot.png")
ingot_orange_frames = animate_resonance_with_palette(ingot_base, palette_coil_orange, 1.25, 1.10, 0.60)
ingot_bronze_frames = animate_resonance_with_palette(ingot_base, palette_bronze, 1.15, 0.95, 0.50)

# Compare Block in both palettes
block_base = load_base(MODERNITY_BLOCKS / "block1.png")
block_orange_frames = animate_resonance_with_palette(block_base, palette_coil_orange, 1.25, 1.10, 0.60)
block_bronze_frames = animate_resonance_with_palette(block_base, palette_bronze, 1.15, 0.95, 0.50)

# Compare Plate
plate_base = load_base(MODERNITY_ITEMS / "plate.png")
plate_orange_frames = animate_resonance_with_palette(plate_base, palette_coil_orange, 1.25, 1.10, 0.60)
plate_bronze_frames = animate_resonance_with_palette(plate_base, palette_bronze, 1.15, 0.95, 0.50)

results = {
    "coil": coil_b64,
    "ingot_orange": frames_to_b64(ingot_orange_frames),
    "ingot_bronze": frames_to_b64(ingot_bronze_frames),
    "plate_orange": frames_to_b64(plate_orange_frames),
    "plate_bronze": frames_to_b64(plate_bronze_frames),
    "block_orange": frames_to_b64(block_orange_frames),
    "block_bronze": frames_to_b64(block_bronze_frames),
}

with open(OUT_DIR / "results.json", "w") as f:
    json.dump(results, f)

print("Generated Hypogen orange vs coil comparison!")
