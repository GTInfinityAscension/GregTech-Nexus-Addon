#!/usr/bin/env python3
"""High-detail procedural synthesis of 512x512 cosmic backgrounds for the Dimensional Rift Gate."""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def generate_fbm_noise(w, h, octaves=6, persistence=0.5, lacunarity=2.0, seed=42):
    """Generate high-density fractal brownian motion noise using vectorized spectral synthesis."""
    rng = np.random.default_rng(seed)
    grid = np.zeros((h, w), dtype=np.float32)
    amplitude = 1.0
    total_amp = 0.0
    
    for oct_idx in range(octaves):
        freq = int(4 * (lacunarity ** oct_idx))
        if freq >= min(w, h):
            break
        # Random phase and frequency components
        sub_h = max(2, int(h / (lacunarity ** (octaves - 1 - oct_idx))))
        sub_w = max(2, int(w / (lacunarity ** (octaves - 1 - oct_idx))))
        noise_small = rng.uniform(0.0, 1.0, (sub_h, sub_w)).astype(np.float32)
        im_noise = Image.fromarray(noise_small).resize((w, h), Image.BICUBIC)
        grid += np.array(im_noise) * amplitude
        total_amp += amplitude
        amplitude *= persistence
        
    return grid / total_amp

def domain_warp_vortex(w, h, noise_map, swirl_strength=8.0, center=None):
    """Apply domain warping: logarithmic swirl + turbulent displacement."""
    if center is None:
        cx, cy = w / 2.0, h / 2.0
    else:
        cx, cy = center
        
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    r_norm = r / (w * 0.5)
    
    theta = np.arctan2(dy, dx)
    
    # Swirl twist increasing towards center
    swirl = swirl_strength * np.exp(-r_norm * 2.2)
    theta_swirled = theta + swirl + noise_map * 1.5
    
    # Compute warped coordinates
    x_warped = cx + r * np.cos(theta_swirled)
    y_warped = cy + r * np.sin(theta_swirled)
    
    # Normalised map with spiral bands
    spiral_arms = 0.5 + 0.5 * np.sin(theta_swirled * 4.0 - np.log(np.maximum(r, 1.0)) * 3.5)
    
    return r_norm, spiral_arms

def color_ramp(values, stops):
    """Map normalized values [0, 1] through an RGB color ramp: [(pos, (r, g, b)), ...]."""
    h, w = values.shape
    out = np.zeros((h, w, 3), dtype=np.float32)
    
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        mask = (values >= p0) & (values <= p1)
        if not np.any(mask):
            continue
        t = (values[mask] - p0) / (p1 - p0)
        t = t[:, np.newaxis]
        c0_arr = np.array(c0, dtype=np.float32)
        c1_arr = np.array(c1, dtype=np.float32)
        out[mask] = c0_arr + (c1_arr - c0_arr) * t
        
    # Clamp below lowest and above highest
    out[values < stops[0][0]] = np.array(stops[0][1], dtype=np.float32)
    out[values > stops[-1][0]] = np.array(stops[-1][1], dtype=np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)

def render_rift_bg_1a_volumetric(w=512, h=512):
    """Variação 1A: Vórtice Cósmico Volumétrico & Singularidade de Acleção."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Base Multi-octave FBM Noise
    noise1 = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=101)
    noise2 = generate_fbm_noise(w, h, octaves=4, persistence=0.6, seed=202)
    
    # 2. Polar swirl
    r_norm, spiral = domain_warp_vortex(w, h, noise1, swirl_strength=6.5, center=(cx, cy))
    
    # 3. Volumetric Accretion Field: Core glow + spiral filaments + turbulence
    core_glow = np.exp(-r_norm * 2.8) * 1.4
    filament_field = (spiral * 0.6 + noise2 * 0.4) * np.exp(-r_norm * 1.5)
    
    # Relativistic jet / coronal spikes
    y, x = np.ogrid[:h, :w]
    ang = np.arctan2(y - cy, x - cx)
    rays = 0.5 + 0.5 * np.cos(ang * 8.0 + noise1 * 4.0)
    ray_glow = rays * np.exp(-r_norm * 1.8) * 0.35
    
    total_lum = np.clip(core_glow * 0.8 + filament_field * 0.9 + ray_glow + noise1 * 0.2, 0.0, 1.0)
    
    # Color Ramp: Void Black -> Dark Cosmic Purple -> Radiant Magenta -> Electric Cyan -> Blazing White
    stops = [
        (0.00, (8, 4, 16)),
        (0.18, (28, 10, 48)),
        (0.35, (68, 20, 96)),
        (0.55, (140, 35, 165)),
        (0.72, (215, 60, 220)),
        (0.88, (0, 225, 255)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(total_lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 4. Deep Field Star Dust (Micro-stars & Twinkles)
    rng = np.random.default_rng(999)
    for _ in range(240):
        sx = rng.integers(8, w - 8)
        sy = rng.integers(8, h - 8)
        # Avoid stars right inside the dark rift center
        if math.hypot(sx - cx, sy - cy) < 30:
            continue
        b = rng.uniform(0.3, 1.0)
        if b > 0.94:
            # 4-point cross diffraction star
            star_col = (255, 240, 180, 255) if rng.random() > 0.4 else (160, 240, 255, 255)
            d.line([(sx - 3, sy), (sx + 3, sy)], fill=star_col, width=1)
            d.line([(sx, sy - 3), (sx, sy + 3)], fill=star_col, width=1)
            d.point((sx, sy), fill=(255, 255, 255, 255))
        elif b > 0.65:
            d.point((sx, sy), fill=(200, 220, 255, int(200 * b)))
        else:
            d.point((sx, sy), fill=(140, 150, 190, int(150 * b)))
            
    # 5. Magitech Pylon Containment Ring (Precision Vector Graphics)
    r_pylons = 125
    # Outer degree ticks ring
    for deg in range(0, 360, 5):
        rad = math.radians(deg)
        t_len = 5 if deg % 45 == 0 else (3 if deg % 15 == 0 else 2)
        p1 = (cx + int((r_pylons + 8) * math.cos(rad)), cy + int((r_pylons + 8) * math.sin(rad)))
        p2 = (cx + int((r_pylons + 8 + t_len) * math.cos(rad)), cy + int((r_pylons + 8 + t_len) * math.sin(rad)))
        col_tick = (255, 215, 80, 220) if deg % 45 == 0 else (140, 100, 220, 120)
        d.line([p1, p2], fill=col_tick, width=1)
        
    # Energy containment circle
    d.ellipse([cx - r_pylons, cy - r_pylons, cx + r_pylons, cy + r_pylons], outline=(180, 80, 255, 140), width=2)
    d.ellipse([cx - r_pylons + 6, cy - r_pylons + 6, cx + r_pylons - 6, cy + r_pylons - 6], outline=(0, 230, 255, 90), width=1)
    
    # 8 Anchor Pylons (Detailed sprite-like geometric structures)
    pylon_positions = []
    for i in range(8):
        ang = i * (360 / 8)
        rad = math.radians(ang)
        px_pos = cx + int(r_pylons * math.cos(rad))
        py_pos = cy + int(r_pylons * math.sin(rad))
        pylon_positions.append((px_pos, py_pos))
        
        # Power conduit lines connecting pylon back to core
        d.line([(px_pos, py_pos), (cx, cy)], fill=(160, 60, 220, 60), width=1)
        
        # Pylon heavy housing
        d.rectangle([px_pos - 7, py_pos - 7, px_pos + 7, py_pos + 7], fill=(22, 14, 38, 240), outline=(130, 70, 190, 255), width=1)
        # Inner glowing crystal/emitter
        d.polygon([
            (px_pos, py_pos - 5), (px_pos + 5, py_pos), (px_pos, py_pos + 5), (px_pos - 5, py_pos)
        ], fill=(255, 215, 80, 255), outline=(255, 255, 255, 255))
        
    # Magnetic energy arcs jumping between neighboring pylons (Octagram of containment)
    for i in range(8):
        p1 = pylon_positions[i]
        p2 = pylon_positions[(i + 1) % 8]
        # Curved or segmented arc
        mid_x = (p1[0] + p2[0]) // 2 + int(6 * math.cos(math.radians(i * 45 + 22.5)))
        mid_y = (p1[1] + p2[1]) // 2 + int(6 * math.sin(math.radians(i * 45 + 22.5)))
        d.line([p1, (mid_x, mid_y)], fill=(0, 230, 255, 160), width=1)
        d.line([(mid_x, mid_y), p2], fill=(0, 230, 255, 160), width=1)
        d.point((mid_x, mid_y), fill=(255, 255, 255, 220))
        
    # Central Event Horizon & Singularity Core
    # Singularity dark core
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(6, 3, 10, 255), outline=(255, 100, 240, 240), width=2)
    # Photon sphere ring
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], outline=(0, 240, 255, 190), width=1)
    # Luminous white core diamond
    d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], fill=(255, 255, 255, 255))

    # 6. Integrated Oscilloscope / Harmonic Interference Screen (Bottom 130px)
    box_y = int(h * 0.70)
    box_h = 136
    # Outer CRT bezel
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(10, 6, 20, 235), outline=(70, 35, 115, 255), width=2)
    d.rectangle([16, box_y + 2, w - 16, box_y + box_h - 2], outline=(30, 16, 50, 255), width=1)
    
    # CRT Phosphor Grid
    for gx in range(30, w - 30, 24):
        d.line([(gx, box_y + 8), (gx, box_y + box_h - 8)], fill=(32, 20, 56, 120), width=1)
    for gy in range(box_y + 12, box_y + box_h - 8, 16):
        d.line([(20, gy), (w - 20, gy)], fill=(32, 20, 56, 120), width=1)
    # Central zero line
    zero_y = box_y + box_h // 2 - 10
    d.line([(20, zero_y), (w - 20, zero_y)], fill=(85, 45, 140, 180), width=1)
    
    # Detailed Multi-Harmonic Waves with Glow
    # Phosphor bloom under-layer (drawn thick with alpha)
    pts_f, pts_harm = [], []
    for x in range(22, w - 22):
        rad = (x - 22) * 0.058
        y_f = zero_y + int(28 * math.sin(rad) + 6 * math.sin(rad * 3.0))
        y_h = zero_y + int(20 * math.sin(rad * 1.5 + 0.6) + 5 * math.cos(rad * 2.5))
        pts_f.append((x, y_f))
        pts_harm.append((x, y_h))
        
    # Draw glow trails
    d.line(pts_harm, fill=(255, 50, 180, 100), width=4)
    d.line(pts_harm, fill=(255, 100, 220, 240), width=2)
    
    d.line(pts_f, fill=(0, 200, 255, 100), width=4)
    d.line(pts_f, fill=(0, 240, 255, 240), width=2)
    d.line(pts_f, fill=(255, 255, 255, 200), width=1)
    
    # Bottom Harmonic Spectrum bars (FFT analyzer in lower screen)
    fft_y = box_y + box_h - 22
    for b_idx in range(16):
        bx = 32 + b_idx * 16
        bh = int(12 * (0.3 + 0.7 * math.sin(b_idx * 0.65) ** 2))
        d.rectangle([bx, fft_y - bh, bx + 10, fft_y], fill=(0, 220, 240, 180), outline=(80, 255, 255, 240))
        
    # Screen Telemetry Labels (drawn crisp)
    d.text((26, box_y + 8), "CANAL 1: f = 412.7 THz (Carrier)", fill=(0, 240, 255, 220))
    d.text((w - 180, box_y + 8), "CANAL 2: 3:2 (Quinta Harm.)", fill=(255, 120, 220, 220))
    d.text((26, box_y + box_h - 18), "ESPECTRO FFT [32-CANAL]", fill=(120, 90, 170, 200))
    d.text((w - 140, box_y + box_h - 18), "RESSONÂNCIA: R = 0.942", fill=(255, 215, 80, 240))
    
    # 7. Deluxe Outer Beveled Frame with corner brackets
    for b in range(6):
        alpha = int(255 * (1.0 - b / 6))
        d.rectangle([b, b, w - 1 - b, h - 1 - b], outline=(15, 8, 28, alpha))
        
    d.rectangle([5, 5, w - 6, h - 6], outline=(120, 50, 180, 255), width=2)
    d.rectangle([7, 7, w - 8, h - 8], outline=(50, 22, 85, 255), width=1)
    
    # Corner brackets (Godforge high-tech)
    for bx, by, sx, sy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(255, 215, 80, 255), width=2)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(255, 215, 80, 255), width=2)
        d.point((bx, by), fill=(255, 255, 255, 255))
        
    return im

if __name__ == '__main__':
    im = render_rift_bg_1a_volumetric(512, 512)
    im.save('/home/raishxn/MineProjects/GregTech-Nexus-Addon/tools/design/ui_proposals/rift_gate/backgrounds/bg_test_1a_volumetric.png')
    print("Done generating test 1A!")
