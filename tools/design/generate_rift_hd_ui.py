#!/usr/bin/env python3
"""High-Detail UI Asset Generator for GTNA Multiblock 2: Portão de Fenda Dimensional (Dimensional Rift Gate).

Generates 3 Ultra-Detailed 512x512 Variations based on the user's preferred Godforge Cosmic Purple theme:
  - Variation 1A: "Vórtice Cósmico Volumétrico" (Fibrous Accretion Singularity, Coronal Filaments & Octagram Arc Cage)
  - Variation 1B: "Nebulosa da Fenda & Atlas Celestial" (Rim-Lit Volumetric Space Clouds, Spacetime Tear & Constellation Lattice)
  - Variation 1C: "Matriz Rúnica dos 8 Pilones" (Sacred Harmonic Geometry, Multi-Tier Vernier Astrolabe & Harmonic Staff)

Outputs to: tools/design/ui_proposals/rift_gate/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'rift_gate')
BG_DIR = os.path.join(OUT_DIR, 'backgrounds')
BTN_DIR = os.path.join(OUT_DIR, 'buttons')
ICO_DIR = os.path.join(OUT_DIR, 'icons')
BAR_DIR = os.path.join(OUT_DIR, 'progressbars')
PREV_DIR = os.path.join(OUT_DIR, 'previews')

os.makedirs(BG_DIR, exist_ok=True)
os.makedirs(BTN_DIR, exist_ok=True)
os.makedirs(ICO_DIR, exist_ok=True)
os.makedirs(BAR_DIR, exist_ok=True)
os.makedirs(PREV_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
def get_font(size=12, bold=False):
    paths = [
        f"/usr/share/fonts/TTF/JetBrainsMonoNLNerdFont-{'Bold' if bold else 'Regular'}.ttf",
        f"/usr/share/fonts/TTF/DejaVuSans{'-Bold' if bold else ''}.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

FONT_HEADER = get_font(15, bold=True)
FONT_SUB = get_font(12, bold=False)
FONT_PANEL = get_font(11, bold=True)
FONT_TEXT = get_font(10, bold=False)
FONT_BTN = get_font(10, bold=True)
FONT_MICRO = get_font(9, bold=False)

# ---------------------------------------------------------------------------
# Procedural Noise & Spectral Synthesis
# ---------------------------------------------------------------------------
def generate_fbm_noise(w, h, octaves=7, persistence=0.52, lacunarity=2.0, seed=42):
    """Vectorized multi-octave Perlin/spectral synthesis for rich textural density."""
    rng = np.random.default_rng(seed)
    grid = np.zeros((h, w), dtype=np.float32)
    amplitude = 1.0
    total_amp = 0.0
    
    for oct_idx in range(octaves):
        freq = int(4 * (lacunarity ** oct_idx))
        if freq >= min(w, h):
            break
        sub_h = max(3, int(h / (lacunarity ** (octaves - 1 - oct_idx))))
        sub_w = max(3, int(w / (lacunarity ** (octaves - 1 - oct_idx))))
        noise_small = rng.uniform(0.0, 1.0, (sub_h, sub_w)).astype(np.float32)
        im_noise = Image.fromarray(noise_small).resize((w, h), Image.BICUBIC)
        grid += np.array(im_noise) * amplitude
        total_amp += amplitude
        amplitude *= persistence
        
    return grid / total_amp

def color_ramp(values, stops):
    """Map normalized values [0, 1] through a multi-stop RGB gradient."""
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
        
    out[values < stops[0][0]] = np.array(stops[0][1], dtype=np.float32)
    out[values > stops[-1][0]] = np.array(stops[-1][1], dtype=np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)


# ===========================================================================
# 1. HIGH-DETAIL BACKGROUND 1A: VÓRTICE CÓSMICO VOLUMÉTRICO
# ===========================================================================

def generate_bg_1a_volumetric(w=512, h=512):
    """Accretion Singularity with Fibrous Coronal Tendrils & CRT Waveform Chamber."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Multi-octave FBM Noise
    n_base = generate_fbm_noise(w, h, octaves=7, persistence=0.55, seed=303)
    n_swirl = generate_fbm_noise(w, h, octaves=5, persistence=0.6, seed=404)
    n_fine = generate_fbm_noise(w, h, octaves=4, persistence=0.7, seed=505)
    
    # 2. Polar Accretion Dynamics
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    r_norm = r / (w * 0.5)
    theta = np.arctan2(dy, dx)
    
    # Non-linear logarithmic swirl twist
    twist = 7.5 * np.exp(-r_norm * 2.5) + n_swirl * 1.8
    theta_twist = theta + twist
    
    # Spiral arms & fine filament ridges
    spiral_arms = 0.5 + 0.5 * np.sin(theta_twist * 5.0 - np.log(np.maximum(r, 2.0)) * 4.0)
    filaments = np.abs(np.sin(theta_twist * 12.0 + n_fine * 6.0)) ** 1.8
    
    # Volumetric Coronal Discharge Rays
    rays = 0.5 + 0.5 * np.cos(theta * 16.0 + n_base * 5.0)
    ray_intensity = rays * np.exp(-r_norm * 1.6) * 0.4
    
    # Accretion Ring Intensity: Bright ring at r ~ 60..100px with falloff
    ring_dist = np.abs(r - 75.0) / 45.0
    ring_glow = np.exp(-ring_dist * ring_dist * 2.0) * 0.85
    
    # Core event horizon plunge (dark center)
    core_hole = np.clip((r - 24.0) / 18.0, 0.0, 1.0)
    
    # Total luminance composite
    lum = (n_base * 0.25 + spiral_arms * 0.35 + filaments * 0.3 + ring_glow + ray_intensity) * core_hole
    lum = np.clip(lum, 0.0, 1.0)
    
    # Palette Ramp: Deep Void -> Velvet Purple -> Radiant Magenta -> Electric Cyan -> Coronal Gold & White
    stops = [
        (0.00, (6, 3, 14)),
        (0.18, (26, 8, 45)),
        (0.36, (65, 18, 92)),
        (0.55, (135, 32, 160)),
        (0.72, (205, 55, 215)),
        (0.85, (0, 220, 255)),
        (0.95, (255, 240, 180)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 3. Dense Field of Micro-Stars with Diffraction Flares
    rng = np.random.default_rng(777)
    for _ in range(260):
        sx = rng.integers(10, w - 10)
        sy = rng.integers(10, h - 10)
        if math.hypot(sx - cx, sy - cy) < 28:
            continue
        bright = rng.uniform(0.2, 1.0)
        if bright > 0.94:
            scol = (255, 235, 170, 255) if rng.random() > 0.5 else (160, 240, 255, 255)
            d.line([(sx - 4, sy), (sx + 4, sy)], fill=scol, width=1)
            d.line([(sx, sy - 4), (sx, sy + 4)], fill=scol, width=1)
            d.point((sx, sy), fill=(255, 255, 255, 255))
        elif bright > 0.6:
            d.point((sx, sy), fill=(200, 220, 255, int(220 * bright)))
        else:
            d.point((sx, sy), fill=(140, 150, 190, int(150 * bright)))
            
    # 4. Precision Magitech Containment Ring & Vernier Scales
    r_pylons = 126
    # Outer tick marks (every 5 degrees, long every 15, cardinal golden)
    for deg in range(0, 360, 5):
        rad = math.radians(deg)
        t_len = 6 if deg % 45 == 0 else (4 if deg % 15 == 0 else 2)
        p1 = (cx + int((r_pylons + 10) * math.cos(rad)), cy + int((r_pylons + 10) * math.sin(rad)))
        p2 = (cx + int((r_pylons + 10 + t_len) * math.cos(rad)), cy + int((r_pylons + 10 + t_len) * math.sin(rad)))
        col_t = (255, 215, 80, 240) if deg % 45 == 0 else (160, 110, 230, 140)
        d.line([p1, p2], fill=col_t, width=1)
        
    d.ellipse([cx - r_pylons, cy - r_pylons, cx + r_pylons, cy + r_pylons], outline=(170, 80, 255, 160), width=2)
    d.ellipse([cx - r_pylons + 6, cy - r_pylons + 6, cx + r_pylons - 6, cy + r_pylons - 6], outline=(0, 230, 255, 110), width=1)
    d.ellipse([cx - r_pylons - 6, cy - r_pylons - 6, cx + r_pylons + 6, cy + r_pylons + 6], outline=(100, 50, 160, 90), width=1)
    
    # 8 Anchor Pylons (Geometric sprite structures with conduit lines)
    pylon_pts = []
    for i in range(8):
        ang = i * (360 / 8)
        rad = math.radians(ang)
        px_pos = cx + int(r_pylons * math.cos(rad))
        py_pos = cy + int(r_pylons * math.sin(rad))
        pylon_pts.append((px_pos, py_pos))
        
        # Conduit line to singularity core
        d.line([(px_pos, py_pos), (cx, cy)], fill=(160, 60, 220, 60), width=1)
        
        # Pylon heavy housing & glowing crystal
        d.rectangle([px_pos - 7, py_pos - 7, px_pos + 7, py_pos + 7], fill=(22, 14, 38, 255), outline=(140, 75, 210, 255), width=1)
        d.polygon([
            (px_pos, py_pos - 5), (px_pos + 5, py_pos), (px_pos, py_pos + 5), (px_pos - 5, py_pos)
        ], fill=(255, 215, 80, 255), outline=(255, 255, 255, 255))
        
    # Magnetic Arc Cage bridging between pylons
    for i in range(8):
        p1 = pylon_pts[i]
        p2 = pylon_pts[(i + 1) % 8]
        mid_x = (p1[0] + p2[0]) // 2 + int(6 * math.cos(math.radians(i * 45 + 22.5)))
        mid_y = (p1[1] + p2[1]) // 2 + int(6 * math.sin(math.radians(i * 45 + 22.5)))
        d.line([p1, (mid_x, mid_y)], fill=(0, 240, 255, 180), width=1)
        d.line([(mid_x, mid_y), p2], fill=(0, 240, 255, 180), width=1)
        d.point((mid_x, mid_y), fill=(255, 255, 255, 240))
        
    # Central Event Horizon & Photon Sphere
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(5, 2, 8, 255), outline=(255, 90, 230, 255), width=2)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=(0, 240, 255, 200), width=1)
    d.polygon([(cx, cy - 8), (cx + 8, cy), (cx, cy + 8), (cx - 8, cy)], fill=(255, 255, 255, 255))

    # 5. Integrated Oscilloscope / Harmonic Interference Screen (Bottom 136px)
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(10, 6, 20, 240), outline=(75, 38, 120, 255), width=2)
    d.rectangle([16, box_y + 2, w - 16, box_y + box_h - 2], outline=(32, 16, 52, 255), width=1)
    
    # CRT Phosphor Grid
    for gx in range(30, w - 30, 24):
        d.line([(gx, box_y + 8), (gx, box_y + box_h - 8)], fill=(34, 20, 58, 120), width=1)
    for gy in range(box_y + 12, box_y + box_h - 8, 16):
        d.line([(20, gy), (w - 20, gy)], fill=(34, 20, 58, 120), width=1)
    zero_y = box_y + box_h // 2 - 10
    d.line([(20, zero_y), (w - 20, zero_y)], fill=(85, 45, 140, 180), width=1)
    
    # Multi-Harmonic Waves with Glow
    pts_f, pts_harm = [], []
    for x_pos in range(22, w - 22):
        rad = (x_pos - 22) * 0.058
        y_f = zero_y + int(28 * math.sin(rad) + 6 * math.sin(rad * 3.0))
        y_h = zero_y + int(20 * math.sin(rad * 1.5 + 0.6) + 5 * math.cos(rad * 2.5))
        pts_f.append((x_pos, y_f))
        pts_harm.append((x_pos, y_h))
        
    d.line(pts_harm, fill=(255, 50, 180, 100), width=4)
    d.line(pts_harm, fill=(255, 100, 220, 240), width=2)
    d.line(pts_f, fill=(0, 200, 255, 100), width=4)
    d.line(pts_f, fill=(0, 240, 255, 240), width=2)
    d.line(pts_f, fill=(255, 255, 255, 220), width=1)
    
    # FFT Spectrum Bars
    fft_y = box_y + box_h - 22
    for b_idx in range(16):
        bx = 32 + b_idx * 16
        bh = int(12 * (0.3 + 0.7 * math.sin(b_idx * 0.65) ** 2))
        d.rectangle([bx, fft_y - bh, bx + 10, fft_y], fill=(0, 220, 240, 180), outline=(80, 255, 255, 240))
        
    # Screen Labels (rendered with TTF FONT_MICRO)
    d.text((26, box_y + 8), "CANAL 1: f = 412.7 THz (Carrier)", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 180, box_y + 8), "CANAL 2: 3:2 (Quinta Harm.)", fill=(255, 120, 220, 240), font=FONT_MICRO)
    d.text((26, box_y + box_h - 18), "ESPECTRO FFT [32-CANAL]", fill=(130, 100, 180, 220), font=FONT_MICRO)
    d.text((w - 146, box_y + box_h - 18), "RESSONÂNCIA: R = 0.942", fill=(255, 215, 80, 255), font=FONT_MICRO)
    
    # 6. Deluxe Beveled Frame with Gold Corner Brackets
    for b in range(6):
        alpha = int(255 * (1.0 - b / 6))
        d.rectangle([b, b, w - 1 - b, h - 1 - b], outline=(14, 7, 26, alpha))
        
    d.rectangle([5, 5, w - 6, h - 6], outline=(125, 55, 185, 255), width=2)
    d.rectangle([7, 7, w - 8, h - 8], outline=(55, 24, 90, 255), width=1)
    
    for bx, by, sx, sy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(255, 215, 80, 255), width=2)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(255, 215, 80, 255), width=2)
        d.point((bx, by), fill=(255, 255, 255, 255))
        
    return im


# ===========================================================================
# 2. HIGH-DETAIL BACKGROUND 1B: NEBULOSA DA FENDA & ATLAS CELESTIAL
# ===========================================================================

def generate_bg_1b_nebula_atlas(w=512, h=512):
    """Rim-Lit Cosmic Dust Clouds (Godforge background_space style) + Spacetime Tear & Constellations."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Multi-layered Volumetric Gas Clouds
    n_clouds = generate_fbm_noise(w, h, octaves=7, persistence=0.58, seed=606)
    n_dust = generate_fbm_noise(w, h, octaves=5, persistence=0.65, seed=707)
    
    # Compute Sobel-like edge detection for illuminated cloud rim lighting
    gx = np.gradient(n_clouds, axis=1)
    gy = np.gradient(n_clouds, axis=0)
    rim_lighting = np.sqrt(gx * gx + gy * gy) * 4.5
    rim_lighting = np.clip(rim_lighting, 0.0, 1.0)
    
    # Central diagonal spacetime tear fracture
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    tear_dist = np.abs(dy - 0.4 * dx) / 45.0
    tear_glow = np.exp(-tear_dist * tear_dist * 2.5) * 0.75
    
    lum = np.clip(n_clouds * 0.55 + rim_lighting * 0.35 + tear_glow + n_dust * 0.15, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.20, (20, 12, 38)),
        (0.40, (52, 24, 78)),
        (0.60, (110, 45, 140)),
        (0.75, (175, 70, 200)),
        (0.88, (0, 230, 220)),
        (0.96, (200, 255, 250)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 2. Celestial Astrometric Grid & Constellation Seed Network
    for r in [60, 110, 160, 210]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 90, 140, 75), width=1)
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            t1 = (cx + int((r - 3) * math.cos(rad)), cy + int((r - 3) * math.sin(rad)))
            t2 = (cx + int((r + 3) * math.cos(rad)), cy + int((r + 3) * math.sin(rad)))
            d.line([t1, t2], fill=(0, 240, 255, 120), width=1)
            
    # Constellation Seeds
    seeds = [
        (cx - 130, cy - 70, 'A3F-19', (255, 215, 80)),
        (cx - 60, cy - 130, '7C2-04', (0, 240, 255)),
        (cx + 70, cy - 120, '9D8-27', (255, 120, 220)),
        (cx + 140, cy - 50, '1B4-09', (0, 240, 255)),
        (cx + 90, cy + 60, 'E5K-88', (255, 215, 80)),
        (cx - 30, cy + 90, 'Omega-0', (255, 80, 140)),
        (cx - 120, cy + 40, 'V-404', (0, 240, 255)),
        (cx, cy, 'SINGULARIDADE', (255, 255, 255))
    ]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (1, 7), (4, 7), (6, 7), (0, 7)]
    for a, b in edges:
        d.line([(seeds[a][0], seeds[a][1]), (seeds[b][0], seeds[b][1])], fill=(120, 80, 200, 110), width=1)
        
    for sx, sy, sname, scol in seeds:
        d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=scol + (255,), outline=(255, 255, 255, 255))
        d.ellipse([sx - 9, sy - 9, sx + 9, sy + 9], outline=scol + (120,), width=1)
        d.text((sx + 8, sy - 6), sname, fill=(220, 230, 255, 200), font=FONT_MICRO)
        
    # 3. 8 Anchor Pylons placed around the perimeter
    for i in range(8):
        ang = i * (360 / 8) + 22.5
        rad = math.radians(ang)
        px_pos = cx + int(210 * math.cos(rad))
        py_pos = cy + int(210 * math.sin(rad))
        d.rectangle([px_pos - 6, py_pos - 6, px_pos + 6, py_pos + 6], fill=(20, 15, 35, 255), outline=(0, 240, 255, 240))
        d.point((px_pos, py_pos), fill=(255, 215, 80, 255))

    # 4. Integrated Oscilloscope / Harmonic Screen
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(8, 6, 18, 240), outline=(50, 70, 120, 255), width=2)
    d.rectangle([16, box_y + 2, w - 16, box_y + box_h - 2], outline=(20, 30, 50, 255), width=1)
    
    zero_y = box_y + box_h // 2 - 10
    d.line([(20, zero_y), (w - 20, zero_y)], fill=(40, 60, 100, 180), width=1)
    
    pts_f, pts_harm = [], []
    for x_pos in range(22, w - 22):
        rad = (x_pos - 22) * 0.058
        y_f = zero_y + int(26 * math.sin(rad) + 5 * math.sin(rad * 3.0))
        y_h = zero_y + int(18 * math.sin(rad * 1.5 + 0.6))
        pts_f.append((x_pos, y_f))
        pts_harm.append((x_pos, y_h))
        
    d.line(pts_harm, fill=(255, 100, 220, 240), width=2)
    d.line(pts_f, fill=(0, 240, 255, 240), width=2)
    
    d.text((26, box_y + 8), "ATLAS CELESTIAL · SINTONIA MULTI-SEMENTE", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 170, box_y + 8), "TOLERÂNCIA: ±3.4 THz (6 Sondas)", fill=(255, 215, 80, 240), font=FONT_MICRO)
    
    # 5. Deluxe Beveled Frame
    d.rectangle([5, 5, w - 6, h - 6], outline=(70, 110, 180, 255), width=2)
    d.rectangle([7, 7, w - 8, h - 8], outline=(30, 45, 80, 255), width=1)
    for bx, by, sx, sy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(0, 240, 255, 255), width=2)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(0, 240, 255, 255), width=2)
        
    return im


# ===========================================================================
# 3. HIGH-DETAIL BACKGROUND 1C: MATRIZ RÚNICA DOS 8 PILONES
# ===========================================================================

def generate_bg_1c_sacred_matrix(w=512, h=512):
    """Sacred Octagram Harmonic Matrix, Vernier Astrolabe Scales & Musical Staff."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Background Turbulent Plasma
    n_plasma = generate_fbm_noise(w, h, octaves=6, persistence=0.54, seed=808)
    n_swirl = generate_fbm_noise(w, h, octaves=4, persistence=0.62, seed=909)
    
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    r_norm = r / (w * 0.5)
    
    core_glow = np.exp(-r_norm * 2.2) * 0.9
    lum = np.clip(n_plasma * 0.45 + n_swirl * 0.25 + core_glow, 0.0, 1.0)
    
    stops = [
        (0.00, (8, 4, 16)),
        (0.22, (28, 10, 48)),
        (0.42, (68, 22, 98)),
        (0.62, (130, 36, 155)),
        (0.78, (195, 65, 210)),
        (0.90, (255, 180, 70)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 2. Sacred Octagram (Interlocking 8-Pointed Star of Containment)
    r_oct = 126
    oct_pts = []
    for i in range(8):
        ang = i * (360 / 8)
        rad = math.radians(ang)
        oct_pts.append((cx + int(r_oct * math.cos(rad)), cy + int(r_oct * math.sin(rad))))
        
    # Draw intersecting golden laser beams (interlocking squares: 0-2-4-6-0 and 1-3-5-7-1)
    sq1 = [oct_pts[0], oct_pts[2], oct_pts[4], oct_pts[6], oct_pts[0]]
    sq2 = [oct_pts[1], oct_pts[3], oct_pts[5], oct_pts[7], oct_pts[1]]
    
    for i in range(4):
        d.line([sq1[i], sq1[i+1]], fill=(255, 215, 80, 160), width=2)
        d.line([sq2[i], sq2[i+1]], fill=(0, 240, 255, 160), width=2)
        
    # Star diagonals through center
    for i in range(4):
        d.line([oct_pts[i], oct_pts[i + 4]], fill=(180, 80, 255, 80), width=1)
        
    # Circular Calibration Dials
    d.ellipse([cx - r_oct, cy - r_oct, cx + r_oct, cy + r_oct], outline=(255, 215, 80, 200), width=2)
    d.ellipse([cx - r_oct - 12, cy - r_oct - 12, cx + r_oct + 12, cy + r_oct + 12], outline=(140, 60, 220, 140), width=1)
    
    # Vernier Ticks
    for deg in range(0, 360, 2):
        rad = math.radians(deg)
        t_len = 5 if deg % 10 == 0 else 2
        p1 = (cx + int((r_oct - t_len) * math.cos(rad)), cy + int((r_oct - t_len) * math.sin(rad)))
        p2 = (cx + int(r_oct * math.cos(rad)), cy + int(r_oct * math.sin(rad)))
        d.line([p1, p2], fill=(255, 215, 80, 120), width=1)

    # 8 Anchor Pylons
    for i, pt in enumerate(oct_pts):
        d.rectangle([pt[0] - 8, pt[1] - 8, pt[0] + 8, pt[1] + 8], fill=(26, 16, 42, 255), outline=(255, 215, 80, 255), width=2)
        d.polygon([
            (pt[0], pt[1] - 6), (pt[0] + 6, pt[1]), (pt[0], pt[1] + 6), (pt[0] - 6, pt[1])
        ], fill=(0, 240, 255, 255))
        d.text((pt[0] - 4, pt[1] + 10), f"P{i+1}", fill=(255, 255, 255, 220), font=FONT_MICRO)

    # Central Harmonizer Eye
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(12, 6, 22, 255), outline=(255, 215, 80, 255), width=2)
    d.polygon([(cx, cy - 10), (cx + 10, cy), (cx, cy + 10), (cx - 10, cy)], fill=(255, 255, 255, 255))

    # 3. Musical Resonance Staff (Partitura de 5 Linhas com Harmônicos)
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(12, 6, 24, 240), outline=(130, 80, 210, 255), width=2)
    
    # 5 Staff lines
    staff_top = box_y + 36
    for k in range(5):
        sy = staff_top + k * 14
        d.line([(24, sy), (w - 24, sy)], fill=(120, 100, 160, 160), width=1)
        
    # Musical harmonic notes placed on staff
    notes = [
        (60, staff_top + 42, "Oitava (2:1)", (0, 240, 255)),
        (160, staff_top + 28, "Quinta (3:2)", (255, 215, 80)),
        (260, staff_top + 14, "Terça (5:4)", (255, 120, 220)),
        (360, staff_top + 56, "Quarta (4:3)", (80, 255, 140)),
        (440, staff_top + 0,  "Trítono (45:32)", (255, 80, 80))
    ]
    for nx, ny, nlabel, ncol in notes:
        d.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=ncol + (255,), outline=(255, 255, 255, 255))
        d.line([(nx + 5, ny), (nx + 5, ny - 20)], fill=ncol + (255,), width=2)
        d.text((nx - 24, ny + 8), nlabel, fill=ncol + (240,), font=FONT_MICRO)

    d.text((26, box_y + 10), "PARTITURA HARMÔNICA DE RESSONÂNCIA · CONSONÂNCIA C = 0.693", fill=(255, 215, 80, 255), font=FONT_MICRO)
    d.text((w - 170, box_y + 10), "MODO: ESTÁVEL & PROFUNDO", fill=(80, 255, 140, 255), font=FONT_MICRO)

    # 4. Deluxe Outer Beveled Frame
    d.rectangle([5, 5, w - 6, h - 6], outline=(145, 85, 220, 255), width=2)
    d.rectangle([7, 7, w - 8, h - 8], outline=(60, 25, 95, 255), width=1)
    for bx, by, sx, sy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(255, 215, 80, 255), width=2)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(255, 215, 80, 255), width=2)
        
    return im


# ===========================================================================
# 4. COMPOSED UI PREVIEW (640x480)
# ===========================================================================

def compose_preview_hd(bg_img, title, palette_desc):
    """Compose full GUI mockup at 640x480."""
    canvas = Image.new('RGBA', (640, 480), (10, 10, 15, 255))
    d = ImageDraw.Draw(canvas)
    
    # 1. Viewport
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(70, 75, 95, 255), width=2)
    
    # 2. Side Panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 18, 26, 255), outline=(50, 55, 75, 255), width=2)
    
    # Header
    d.rectangle([16, 12, 624, 40], fill=(24, 24, 34, 255), outline=(60, 65, 85, 255))
    d.text((24, 18), f"GTNA · PORTÃO DE FENDA DIMENSIONAL [UIV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel contents
    d.text((panel_x + 10, panel_y + 12), "SINTONIA DIMENSIONAL", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(60, 65, 85, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Semente: A3F-19", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Bioma: Planície Cristalina", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Pilones Ativos: 8/8", fill=(80, 255, 140, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Consumo: 0.03 L/s Exótica", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Load and paste icons from existing icon folder
    ico_names = ['ico_rift_tear_cosmic_32.png', 'ico_harmonic_wave_cosmic_32.png', 'ico_anchor_pylon_cosmic_32.png', 'ico_exotic_matter_cosmic_32.png']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, iname)
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "RESSONÂNCIA R = 0.94", fill=(255, 215, 80, 255), font=FONT_TEXT)
    pbar_r_path = os.path.join(BAR_DIR, 'progressbar_cosmic_resonance.png')
    if os.path.exists(pbar_r_path):
        pbar_r = Image.open(pbar_r_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_r, (panel_x + 10, panel_y + 160), pbar_r)
        
    d.text((panel_x + 10, panel_y + 180), "ESTABILIDADE S = 88%", fill=(80, 255, 140, 255), font=FONT_TEXT)
    pbar_s_path = os.path.join(BAR_DIR, 'progressbar_cosmic_stability.png')
    if os.path.exists(pbar_s_path):
        pbar_s = Image.open(pbar_s_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_s, (panel_x + 10, panel_y + 196), pbar_s)
        
    d.text((panel_x + 10, panel_y + 220), "PROFUNDIDADE D: 23 (Manto)", fill=(240, 140, 255, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Multiplicador D^1.5: 110.3x", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Buttons
    btn_n_path = os.path.join(BTN_DIR, 'btn_cosmic_normal.png')
    btn_h_path = os.path.join(BTN_DIR, 'btn_cosmic_hover.png')
    btn_p_path = os.path.join(BTN_DIR, 'btn_cosmic_pressed.png')
    
    if os.path.exists(btn_n_path):
        btn_n = Image.open(btn_n_path).resize((74, 28), Image.NEAREST)
        canvas.paste(btn_n, (panel_x + 10, panel_y + 266), btn_n)
        d.text((panel_x + 22, panel_y + 274), "SONDA", fill=(255, 255, 255, 255), font=FONT_BTN)
        
    if os.path.exists(btn_h_path):
        btn_h = Image.open(btn_h_path).resize((74, 28), Image.NEAREST)
        canvas.paste(btn_h, (panel_x + 90, panel_y + 266), btn_h)
        d.text((panel_x + 100, panel_y + 274), "ÂNCORA", fill=(255, 255, 255, 255), font=FONT_BTN)
        
    if os.path.exists(btn_p_path):
        btn_p = Image.open(btn_p_path).resize((154, 32), Image.NEAREST)
        canvas.paste(btn_p, (panel_x + 10, panel_y + 306), btn_p)
        d.text((panel_x + 32, panel_y + 314), "[ SINTONIZAR ]", fill=(255, 220, 100, 255), font=FONT_BTN)
        
    # Footer
    d.text((16, 442), f"Estilo: {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho do Background: 512x512 (ou Wide 640x360) · Alta Densidade Textural Procedural", fill=(100, 110, 130, 255), font=FONT_TEXT)
    
    return canvas


# ===========================================================================
# 5. UNIFIED COMPARISON OVERVIEW
# ===========================================================================

def generate_comparison_sheet_hd(p1, p2, p3):
    """Combine the 3 HD previews into a single side-by-side comparison sheet."""
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    
    d.rectangle([0, 0, sheet.width, 60], fill=(20, 20, 30, 255), outline=(50, 55, 75, 255))
    d.text((30, 14), "GTNA · COMPARATIVO DE ALTA DILIGÊNCIA VISUAL — MULTIBLOCO 2: PORTÃO DE FENDA DIMENSIONAL", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "3 Variações Ricas em Detalhes 512x512 (Vórtice Volumétrico, Nebulosa da Fenda & Atlas, Matriz Sagrada dos 8 Pilones)", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    sheet.paste(p1, (10, 75))
    sheet.paste(p2, (sw + 20, 75))
    sheet.paste(p3, (sw * 2 + 30, 75))
    
    return sheet


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def main():
    print(">>> Gerando Variações de Alta Diligência (HD) para o Portão de Fenda...")
    
    print("  -> Gerando Background 1A: Vórtice Cósmico Volumétrico (512x512)...")
    bg_1a = generate_bg_1a_volumetric(512, 512)
    bg_1a.save(os.path.join(BG_DIR, 'bg_variation_1a_volumetric_512.png'))
    generate_bg_1a_volumetric(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1a_volumetric_wide.png'))
    
    print("  -> Gerando Background 1B: Nebulosa da Fenda & Atlas Celestial (512x512)...")
    bg_1b = generate_bg_1b_nebula_atlas(512, 512)
    bg_1b.save(os.path.join(BG_DIR, 'bg_variation_1b_nebula_atlas_512.png'))
    generate_bg_1b_nebula_atlas(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1b_nebula_atlas_wide.png'))
    
    print("  -> Gerando Background 1C: Matriz Rúnica dos 8 Pilones (512x512)...")
    bg_1c = generate_bg_1c_sacred_matrix(512, 512)
    bg_1c.save(os.path.join(BG_DIR, 'bg_variation_1c_sacred_matrix_512.png'))
    generate_bg_1c_sacred_matrix(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1c_sacred_matrix_wide.png'))

    print("  -> Montando Telas Completas de Preview...")
    prev_1a = compose_preview_hd(bg_1a, "Variação 1A: Vórtice Cósmico Volumétrico", "Singularidade de Acreção Fibrosa, Gaiola de Arcos Magnéticos & Osciloscópio CRT")
    prev_1a.save(os.path.join(PREV_DIR, 'preview_variation_1a_volumetric.png'))
    
    prev_1b = compose_preview_hd(bg_1b, "Variação 1B: Nebulosa da Fenda & Atlas", "Nuvens Cósmicas Volumétricas com Rim-Lighting, Rasgadura & Rede de Constelações")
    prev_1b.save(os.path.join(PREV_DIR, 'preview_variation_1b_nebula_atlas.png'))
    
    prev_1c = compose_preview_hd(bg_1c, "Variação 1C: Matriz Rúnica dos 8 Pilones", "Octagrama Dourado Sagrado de Confinamento, Escala Vernier & Pauta de Ressonância")
    prev_1c.save(os.path.join(PREV_DIR, 'preview_variation_1c_sacred_matrix.png'))

    print("  -> Gerando Prancha Comparativa Unificada HD...")
    sheet = generate_comparison_sheet_hd(prev_1a, prev_1b, prev_1c)
    sheet.save(os.path.join(OUT_DIR, 'comparison_overview.png'))
    
    print("\n[OK] Todos os assets de alta diligência foram gerados com sucesso em:")
    print(f"     {OUT_DIR}")

if __name__ == '__main__':
    main()
