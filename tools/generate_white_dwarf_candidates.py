import numpy as np
from PIL import Image
import os

OUT_DIR = "/tmp/wd_candidates"
os.makedirs(OUT_DIR, exist_ok=True)

# Sources
ITEMS = {
    "ingot": "src/main/resources/assets/gtceu/textures/item/material_sets/white_dwarf_matter/ingot.png",
    "plate": "src/main/resources/assets/gtceu/textures/item/material_sets/white_dwarf_matter/plate.png",
    "gear": "src/main/resources/assets/gtceu/textures/item/material_sets/white_dwarf_matter/gear.png",
    "block": "src/main/resources/assets/gtceu/textures/block/material_sets/white_dwarf_matter/block.png"
}

def load_base(path):
    im = Image.open(path).convert("RGBA")
    return np.array(im, dtype=np.float32)

def to_celestial_palette(arr):
    # Modernity gray values: map to celestial white dwarf tones
    # Preserve alpha
    res = np.zeros_like(arr)
    res[:, :, 3] = arr[:, :, 3]
    gray = arr[:, :, 0] # grayscale since R=G=B
    
    t = gray / 255.0
    # Shadow: [60, 64, 92] (deep cosmic indigo-silver)
    # Midtone: [208, 222, 240] (bright star silver with slight cool sheen)
    # Highlight: [255, 255, 255] (pure brilliant white)
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 60 + s_low * (208 - 60)
    g_low = 64 + s_low * (222 - 64)
    b_low = 92 + s_low * (240 - 92)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 208 + s_high * (255 - 208)
    g_high = 222 + s_high * (255 - 222)
    b_high = 240 + s_high * (255 - 240)
    
    res[:, :, 0] = np.where(mask_low, r_low, r_high)
    res[:, :, 1] = np.where(mask_low, g_low, g_high)
    res[:, :, 2] = np.where(mask_low, b_low, b_high)
    return res

def make_candidate_1_sweep(base_arr, n_frames=30):
    # Starlight Sweep
    colored = to_celestial_palette(base_arr)
    alpha = colored[:, :, 3] > 0
    h, w = base_arr.shape[:2]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        # Sweep wave position from -6 to 38
        wave_pos = (f / n_frames) * (w + h + 10) - 5
        
        # Grid coordinates
        y_coords, x_coords = np.ogrid[:h, :w]
        diag_dist = (x_coords + y_coords) - wave_pos
        
        # Wave intensity
        sigma = 2.2
        wave = np.exp(-(diag_dist**2) / (2 * (sigma**2)))
        
        # Secondary small glint trailing by 8 frames
        glint_phase = (f / n_frames) * 2 * np.pi
        shimmer = 0.08 * np.sin(glint_phase + (x_coords * 0.7 - y_coords * 0.5))
        
        # Apply brightening and cool white/cyan tint
        for c, boost, tint in [(0, 75, 245), (1, 85, 255), (2, 95, 255)]:
            val = frame[:, :, c] + wave * boost + shimmer * 30
            # Blend towards pure tinted highlight when wave hits
            val = np.clip(val, 0, 255)
            frame[:, :, c] = np.where(alpha, val, 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def make_candidate_2_pulse(base_arr, n_frames=30):
    # Gravitational Pulse
    colored = to_celestial_palette(base_arr)
    alpha = colored[:, :, 3] > 0
    h, w = base_arr.shape[:2]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        phase = (f / n_frames) * 2 * np.pi
        # Smooth pulse curve with sharp crest and soft trough
        pulse = 0.5 + 0.5 * (np.sin(phase) * 0.7 + np.sin(phase * 2) * 0.3)
        
        # Radial distance from center (7.5, 7.5)
        y_coords, x_coords = np.ogrid[:h, :w]
        r = np.sqrt((x_coords - 7.5)**2 + (y_coords - 7.5)**2)
        r_weight = np.clip(1.0 - r / 12.0, 0.4, 1.0)
        
        intensity = pulse * r_weight
        
        # Boost RGB
        # R gets boosted up to +50, G up to +60, B up to +70
        frame[:, :, 0] += intensity * 50
        frame[:, :, 1] += intensity * 62
        frame[:, :, 2] += intensity * 75
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def make_candidate_3_resonance(base_arr, n_frames=30):
    # Degenerate Resonance / Multi-Harmonic Shimmer
    colored = to_celestial_palette(base_arr)
    alpha = colored[:, :, 3] > 0
    h, w = base_arr.shape[:2]
    
    frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        y_coords, x_coords = np.ogrid[:h, :w]
        # Two traveling interference waves
        wave1 = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 18.0))
        wave2 = np.cos(2 * np.pi * (t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
        
        interf = (wave1 + wave2) * 0.5 # [-1, 1]
        
        # Shimmer only on non-dark pixels to preserve sharp edges
        t_base = base_arr[:, :, 0] / 255.0
        edge_mask = np.clip((t_base - 0.25) / 0.75, 0, 1)
        
        boost = interf * 45.0 * edge_mask
        
        frame[:, :, 0] += boost * 0.85
        frame[:, :, 1] += boost * 0.95
        frame[:, :, 2] += boost * 1.15
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        frames.append(frame.astype(np.uint8))
    return frames

def save_gif(frames, path, scale=6, frametime_ms=100):
    pil_frames = []
    for f in frames:
        im = Image.fromarray(f, mode="RGBA")
        # Upscale with nearest neighbor for pixel-art clarity
        w, h = im.size
        # Background: dark slate #141724 so the white/silver contrast pops
        bg = Image.new("RGBA", (w, h), (20, 23, 36, 255))
        bg.paste(im, (0, 0), im)
        scaled = bg.resize((w * scale, h * scale), Image.Resampling.NEAREST)
        pil_frames.append(scaled)
    pil_frames[0].save(path, save_all=True, append_images=pil_frames[1:], duration=frametime_ms, loop=0)
    print(f"Saved {path}")

for item_name, item_path in ITEMS.items():
    base = load_base(item_path)
    c1 = make_candidate_1_sweep(base)
    c2 = make_candidate_2_pulse(base)
    c3 = make_candidate_3_resonance(base)
    
    save_gif(c1, f"{OUT_DIR}/{item_name}_c1_sweep.gif")
    save_gif(c2, f"{OUT_DIR}/{item_name}_c2_pulse.gif")
    save_gif(c3, f"{OUT_DIR}/{item_name}_c3_resonance.gif")

print("All candidate animations generated successfully!")
