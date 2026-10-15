#!/usr/bin/env python3
"""High-Detail UI Asset Generator for GTNA Multiblock 3: Anel Colisor de Antimatéria (Antimatter Collider Ring).

Outputs 3 Ultra-Detailed 512x512 Variations based on the user's preferred Godforge Cosmic Purple theme:
  - Variation 1: "Acelerador Relativístico & Ponto de Colisão" (Synchrotron Ring, Dipoles, Particle Collision Spikes & Invariant Mass Histogram)
  - Variation 2: "Câmara de Bolhas Quântica & Modelo Padrão" (Lorentz Spiral Tracks, Vertex Tracker, Holographic SM Grid & Luminosity HUD)
  - Variation 3: "Matriz de Contenção de Penning & Criogenia" (Quadrupole Penning Trap, Antiproton Cloud, Superconducting Coils & Quench Margin)

Outputs to: tools/design/ui_proposals/collider_ring/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'collider_ring')
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
# Procedural Noise & Color Ramps
# ---------------------------------------------------------------------------
def generate_fbm_noise(w, h, octaves=7, persistence=0.54, lacunarity=2.0, seed=42):
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
        out[mask] = np.array(c0, dtype=np.float32) + (np.array(c1, dtype=np.float32) - np.array(c0, dtype=np.float32)) * t
    out[values < stops[0][0]] = np.array(stops[0][1], dtype=np.float32)
    out[values > stops[-1][0]] = np.array(stops[-1][1], dtype=np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)


# ===========================================================================
# 1. BACKGROUND 1: ACELERADOR RELATIVÍSTICO & PONTO DE COLISÃO
# ===========================================================================

def generate_bg_variation_1_accelerator(w=512, h=512):
    """Circular Synchrotron Ring, Dipole Magnets, Collision Burst & Invariant Mass Histogram."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Base Cosmic FBM Noise
    n_base = generate_fbm_noise(w, h, octaves=7, persistence=0.55, seed=111)
    n_radial = generate_fbm_noise(w, h, octaves=4, persistence=0.6, seed=222)
    
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    
    # Synchrotron ring halo around r ~ 125px
    ring_dist = np.abs(r - 125.0) / 40.0
    synchrotron_glow = np.exp(-ring_dist * ring_dist * 2.5) * 0.95
    
    # Collision point intense glow at center
    core_dist = r / 35.0
    collision_core = np.exp(-core_dist * core_dist * 2.0) * 0.85
    
    lum = np.clip(n_base * 0.35 + synchrotron_glow + collision_core + n_radial * 0.15, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.18, (24, 8, 42)),
        (0.35, (60, 16, 88)),
        (0.55, (125, 30, 155)),
        (0.72, (195, 50, 210)),
        (0.85, (0, 230, 255)),
        (0.95, (255, 235, 160)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 2. Stars & Quantum Particles in Space
    rng = np.random.default_rng(1234)
    for _ in range(250):
        sx, sy = rng.integers(10, w - 10), rng.integers(10, h - 10)
        b = rng.uniform(0.2, 1.0)
        if b > 0.94:
            d.line([(sx - 3, sy), (sx + 3, sy)], fill=(255, 240, 180, 240), width=1)
            d.line([(sx, sy - 3), (sx, sy + 3)], fill=(255, 240, 180, 240), width=1)
            d.point((sx, sy), fill=(255, 255, 255, 255))
        else:
            d.point((sx, sy), fill=(160, 180, 230, int(180 * b)))
            
    # 3. Main Synchrotron Ring Structure (Vacuum Chamber & Dipole Magnets)
    r_ring = 125
    d.ellipse([cx - r_ring, cy - r_ring, cx + r_ring, cy + r_ring], outline=(180, 80, 255, 180), width=3)
    d.ellipse([cx - r_ring + 8, cy - r_ring + 8, cx + r_ring - 8, cy + r_ring - 8], outline=(0, 240, 255, 140), width=1)
    d.ellipse([cx - r_ring - 8, cy - r_ring - 8, cx + r_ring + 8, cy + r_ring + 8], outline=(100, 50, 160, 100), width=1)
    
    # Dipole Superconducting Magnet Blocks (16 sectors along ring)
    for i in range(16):
        ang = i * (360 / 16)
        rad = math.radians(ang)
        mx = cx + int(r_ring * math.cos(rad))
        my = cy + int(r_ring * math.sin(rad))
        # Magnet box
        d.rectangle([mx - 5, my - 5, mx + 5, my + 5], fill=(24, 16, 40, 255), outline=(255, 215, 80, 240), width=1)
        d.point((mx, my), fill=(0, 240, 255, 255))
        
    # Counter-rotating Beams (Opposing Arrows on the Ring)
    d.arc([cx - r_ring - 2, cy - r_ring - 2, cx + r_ring + 2, cy + r_ring + 2], 10, 80, fill=(0, 255, 255, 240), width=2)
    d.arc([cx - r_ring + 2, cy - r_ring + 2, cx + r_ring - 2, cy + r_ring - 2], 190, 260, fill=(255, 80, 220, 240), width=2)

    # 4. Interaction Point (IP) Collision Burst & Particle Decays (Center)
    # Hadron spray jets & spiral decay tracks
    for jet_angle in [25, 70, 140, 210, 290, 335]:
        rad_base = math.radians(jet_angle)
        # Logarithmic Lorentz spiral track: r = a * exp(b * theta)
        pts_track = []
        for step in range(25):
            dist_step = step * 3.5
            curve = math.radians(step * 14.0)
            tx = cx + int(dist_step * math.cos(rad_base + curve))
            ty = cy + int(dist_step * math.sin(rad_base + curve))
            pts_track.append((tx, ty))
        col_jet = (0, 240, 255, 180) if jet_angle % 2 == 0 else (255, 80, 200, 180)
        d.line(pts_track, fill=col_jet, width=1)
        
    # Central Collision Core Flare
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(255, 255, 255, 255), outline=(255, 215, 80, 255))
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 220, 255))

    # 5. Integrated Invariant Mass Histogram (Bottom 136px)
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(10, 6, 20, 240), outline=(75, 38, 120, 255), width=2)
    d.rectangle([16, box_y + 2, w - 16, box_y + box_h - 2], outline=(32, 16, 52, 255), width=1)
    
    # Histogram Grid & Axes
    hist_left, hist_right, hist_base = 28, w - 28, box_y + box_h - 24
    d.line([(hist_left, hist_base), (hist_right, hist_base)], fill=(85, 45, 140, 220), width=1)
    for gy in range(box_y + 16, hist_base, 20):
        d.line([(hist_left, gy), (hist_right, gy)], fill=(34, 20, 58, 100), width=1)
        
    # Real Invariant Mass Histogram Data: Exponential Background + Higgs Gaussian Peak (m = 125 GeV)
    rng_hist = np.random.default_rng(42)
    n_bins = 48
    bin_w = (hist_right - hist_left) / n_bins
    
    for i in range(n_bins):
        m_gev = 100 + i * (60.0 / n_bins)
        # Background: exp(-(m-100)/25)
        bg = 42.0 * math.exp(-(m_gev - 100.0) / 25.0)
        # Signal peak at 125 GeV (width sigma ~ 2.5 GeV)
        sig = 32.0 * math.exp(-((m_gev - 125.0) / 3.0) ** 2)
        noise_fluct = rng_hist.uniform(-2.5, 2.5)
        total_h = max(2, int(bg + sig + noise_fluct))
        
        bx = int(hist_left + i * bin_w)
        # Background bar (Dark slate-purple)
        d.rectangle([bx, hist_base - total_h, bx + int(bin_w) - 1, hist_base], fill=(55, 35, 85, 255), outline=(85, 55, 130, 200))
        # Signal component highlighted in Cyan
        if sig > 4.0:
            sig_h = int(sig)
            d.rectangle([bx, hist_base - total_h, bx + int(bin_w) - 1, hist_base - total_h + sig_h], fill=(0, 240, 255, 240))

    # Higgs Discovery Annotation Marker
    peak_x = int(hist_left + ((125.0 - 100.0) / 60.0) * (hist_right - hist_left))
    d.line([(peak_x, box_y + 16), (peak_x, hist_base)], fill=(255, 215, 80, 220), width=1)
    d.polygon([(peak_x, box_y + 24), (peak_x - 4, box_y + 16), (peak_x + 4, box_y + 16)], fill=(255, 215, 80, 255))
    
    d.text((peak_x - 38, box_y + 6), "BÓSON DE HIGGS (125 GeV)", fill=(255, 215, 80, 255), font=FONT_MICRO)
    d.text((26, box_y + 6), "EVENTOS / 1.25 GeV", fill=(160, 170, 190, 220), font=FONT_MICRO)
    d.text((hist_right - 140, box_y + 6), "SIGNIFICÂNCIA: 5.2σ [DESCOBERTA]", fill=(80, 255, 140, 255), font=FONT_MICRO)
    d.text((hist_left, hist_base + 6), "100 GeV", fill=(120, 130, 150, 220), font=FONT_MICRO)
    d.text((peak_x - 12, hist_base + 6), "125 GeV", fill=(255, 215, 80, 255), font=FONT_MICRO)
    d.text((hist_right - 40, hist_base + 6), "160 GeV", fill=(120, 130, 150, 220), font=FONT_MICRO)

    # 6. Deluxe Frame with Gold Corner Brackets
    for b in range(6):
        d.rectangle([b, b, w - 1 - b, h - 1 - b], outline=(14, 7, 26, int(255 * (1.0 - b / 6))))
    d.rectangle([5, 5, w - 6, h - 6], outline=(125, 55, 185, 255), width=2)
    d.rectangle([7, 7, w - 8, h - 8], outline=(55, 24, 90, 255), width=1)
    for bx, by, sx, sy in [(10, 10, 1, 1), (w - 10, 10, -1, 1), (10, h - 10, 1, -1), (w - 10, h - 10, -1, -1)]:
        d.line([(bx, by), (bx + sx * 20, by)], fill=(255, 215, 80, 255), width=2)
        d.line([(bx, by), (bx, by + sy * 20)], fill=(255, 215, 80, 255), width=2)
        d.point((bx, by), fill=(255, 255, 255, 255))
        
    return im


# ===========================================================================
# 2. BACKGROUND 2: CÂMARA DE BOLHAS QUÂNTICA & TABELA DO MODELO PADRÃO
# ===========================================================================

def generate_bg_variation_2_bubble_chamber(w=512, h=512):
    """Dense Quantum Bubble Chamber Particle Spirals + Holographic Standard Model Grid."""
    cx, cy = w // 2, int(h * 0.44)
    
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.56, seed=333)
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    
    lum = np.clip(n_base * 0.45 + np.exp(-r / 160.0) * 0.4, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.25, (22, 10, 38)),
        (0.50, (55, 20, 80)),
        (0.75, (110, 35, 140)),
        (0.90, (0, 210, 230)),
        (1.00, (240, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Bubble chamber tracks (Hundreds of spiraling micro-particles under Lorentz magnetic force)
    rng = np.random.default_rng(888)
    for _ in range(40):
        track_cx = rng.integers(cx - 140, cx + 140)
        track_cy = rng.integers(cy - 120, cy + 120)
        direction = 1 if rng.random() > 0.5 else -1
        max_r_track = rng.uniform(15.0, 60.0)
        pts = []
        for step in range(35):
            t_rad = step * 0.25 * direction
            curr_r = max_r_track * (1.0 - step / 36.0)
            px_t = track_cx + int(curr_r * math.cos(t_rad))
            py_t = track_cy + int(curr_r * math.sin(t_rad))
            pts.append((px_t, py_t))
        alpha = rng.integers(60, 200)
        col = (0, 240, 255, alpha) if rng.random() > 0.4 else (255, 90, 220, alpha)
        d.line(pts, fill=col, width=1)
        
    # Concentric Silicon Vertex Detector Layers
    for r_layer in [40, 75, 110, 145]:
        d.ellipse([cx - r_layer, cy - r_layer, cx + r_layer, cy + r_layer], outline=(70, 90, 150, 90), width=1)
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            p1 = (cx + int((r_layer - 2) * math.cos(rad)), cy + int((r_layer - 2) * math.sin(rad)))
            p2 = (cx + int((r_layer + 2) * math.cos(rad)), cy + int((r_layer + 2) * math.sin(rad)))
            d.line([p1, p2], fill=(0, 240, 255, 120), width=1)

    # Holographic Standard Model Sector Cells (Floating upper-center)
    sm_particles = [
        ('u', 0, 0), ('c', 1, 0), ('t', 2, 0), ('γ', 3, 0),
        ('d', 0, 1), ('s', 1, 1), ('b', 2, 1), ('g', 3, 1),
        ('e', 0, 2), ('μ', 1, 2), ('τ', 2, 2), ('Z', 3, 2),
        ('νe', 0, 3), ('νμ', 1, 3), ('ντ', 2, 3), ('W', 3, 3)
    ]
    grid_ox, grid_oy = cx - 120, cy - 80
    for sym, col_idx, row_idx in sm_particles:
        gx = grid_ox + col_idx * 26
        gy = grid_oy + row_idx * 26
        d.rectangle([gx, gy, gx + 22, gy + 22], fill=(16, 12, 28, 200), outline=(120, 60, 180, 220))
        d.text((gx + 6, gy + 4), sym, fill=(255, 215, 80, 255) if col_idx == 2 and row_idx == 0 else (220, 230, 255, 220), font=FONT_MICRO)

    # Higgs Boson Special Cell (Centered to the right)
    hx, hy = cx + 20, cy - 50
    d.rectangle([hx, hy, hx + 36, hy + 36], fill=(45, 18, 70, 240), outline=(255, 215, 80, 255), width=2)
    d.text((hx + 12, hy + 8), "H", fill=(255, 255, 255, 255), font=FONT_PANEL)
    d.text((hx + 4, hy + 22), "125 GeV", fill=(255, 215, 80, 255), font=FONT_MICRO)
    
    # 4. Integrated Luminosity Telemetry Box
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(8, 6, 18, 240), outline=(60, 75, 130, 255), width=2)
    d.text((26, box_y + 10), "TELEMETRIA DE LUMINOSIDADE INTEGRADA: L = 1.84e34 cm⁻² s⁻¹", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 160, box_y + 10), "FEIXE: 108 TeV (CM 216 TeV)", fill=(255, 215, 80, 240), font=FONT_MICRO)
    
    # Luminosity fill gauge
    d.rectangle([26, box_y + 36, w - 26, box_y + 54], fill=(14, 12, 24, 255), outline=(50, 60, 100, 255))
    d.rectangle([28, box_y + 38, 28 + int((w - 56) * 0.78), box_y + 52], fill=(0, 200, 240, 220))
    d.text((36, box_y + 40), "L_int: 3.906 / 5.000 fb⁻¹ (Modo Top & Higgs)", fill=(255, 255, 255, 255), font=FONT_MICRO)

    d.rectangle([5, 5, w - 6, h - 6], outline=(75, 100, 180, 255), width=2)
    return im


# ===========================================================================
# 3. BACKGROUND 3: MATRIZ DE CONTENÇÃO DE PENNING & CRIOGENIA
# ===========================================================================

def generate_bg_variation_3_penning_cryo(w=512, h=512):
    """Quadrupole Hyperbolic Penning Trap, Antiproton Core & Liquid Helium Quench Margin."""
    cx, cy = w // 2, int(h * 0.44)
    
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=555)
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    
    # Quadrupole potential field: V = (x^2 + y^2 - 2z^2) -> hyperbolas
    quad_field = np.abs(dx * dx - dy * dy) / (w * 80.0)
    quad_glow = np.exp(-quad_field * 2.0) * 0.8
    
    r = np.sqrt(dx * dx + dy * dy)
    antiproton_cloud = np.exp(-(r / 25.0) ** 2) * 1.2
    
    lum = np.clip(n_base * 0.35 + quad_glow * 0.6 + antiproton_cloud, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.20, (20, 8, 38)),
        (0.40, (55, 18, 85)),
        (0.65, (120, 32, 160)),
        (0.80, (200, 50, 215)),
        (0.92, (0, 240, 255)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Hyperbolic Electrode Boundaries of the Penning Trap
    d.arc([cx - 100, cy - 80, cx + 100, cy + 80], 30, 150, fill=(255, 215, 80, 220), width=3)
    d.arc([cx - 100, cy - 80, cx + 100, cy + 80], 210, 330, fill=(255, 215, 80, 220), width=3)
    d.line([(cx - 70, cy - 90), (cx + 70, cy - 90)], fill=(0, 240, 255, 200), width=2)
    d.line([(cx - 70, cy + 90), (cx + 70, cy + 90)], fill=(0, 240, 255, 200), width=2)

    # Glowing Antiproton Cloud in Center
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(255, 255, 255, 240), outline=(0, 240, 255, 255), width=2)
    d.text((cx - 36, cy - 36), "1e13 p̄ (ANTIPRÓTONS)", fill=(0, 240, 255, 255), font=FONT_MICRO)

    # Cryogenic Helium & Quench Margin Monitor
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(8, 6, 18, 240), outline=(80, 45, 130, 255), width=2)
    d.text((26, box_y + 10), "SISTEMA CRIOGÊNICO DE HÉLIO LÍQUIDO · 1.9 K (SUPERFLUIDO)", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 160, box_y + 10), "STATUS: ESTÁVEL [SEM QUENCH]", fill=(80, 255, 140, 255), font=FONT_MICRO)
    
    # 8 Cryo Sectors status
    for s_idx in range(8):
        sx = 28 + s_idx * 58
        d.rectangle([sx, box_y + 36, sx + 50, box_y + 60], fill=(18, 24, 45, 255), outline=(0, 200, 240, 200))
        d.text((sx + 6, box_y + 40), f"SEC {s_idx+1}", fill=(200, 220, 255, 255), font=FONT_MICRO)
        d.text((sx + 6, box_y + 50), "1.88 K", fill=(80, 255, 140, 255), font=FONT_MICRO)

    d.rectangle([5, 5, w - 6, h - 6], outline=(125, 55, 185, 255), width=2)
    return im


# ===========================================================================
# 4. BUTTONS & ICONS & PROGRESS BARS
# ===========================================================================

def generate_button(theme, state='normal', w=64, h=32):
    """9-Sliceable themed button for Collider Ring."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    if state == 'normal':
        bg_top, bg_bot = (54, 26, 84), (32, 14, 52)
        border_outer, border_inner = (95, 45, 150), (145, 75, 220)
        glow_corner = (200, 140, 255)
    elif state == 'hover':
        bg_top, bg_bot = (78, 38, 118), (48, 22, 75)
        border_outer, border_inner = (130, 65, 200), (190, 110, 255)
        glow_corner = (235, 190, 255)
    else: # pressed
        bg_top, bg_bot = (25, 10, 42), (40, 18, 65)
        border_outer, border_inner = (55, 25, 85), (85, 40, 130)
        glow_corner = (120, 60, 180)
        
    for y in range(h):
        t = y / (h - 1)
        row_col = tuple(int(bg_top[i] + (bg_bot[i] - bg_top[i]) * t) for i in range(3))
        d.line([(2, y), (w - 3, y)], fill=row_col + (255,))
        
    d.rectangle([1, 1, w - 2, h - 2], outline=border_outer + (255,))
    d.rectangle([2, 2, w - 3, h - 3], outline=border_inner + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(8, 8, 12, 255))
    d.point((2, 2), fill=glow_corner + (255,))
    d.point((w - 3, 2), fill=glow_corner + (255,))
    d.point((2, h - 3), fill=glow_corner + (255,))
    d.point((w - 3, h - 3), fill=glow_corner + (255,))
    return im

def generate_collider_icons():
    """Generate 6 icons for the Collider Ring (64x64 and 32x32)."""
    icons = {}
    
    # 1. Particle Collision Burst
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = 32
    d.ellipse([c - 16, c - 16, c + 16, c + 16], outline=(180, 80, 255, 180), width=2)
    for ang in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(ang)
        d.line([(c, c), (c + int(24 * math.cos(rad)), c + int(24 * math.sin(rad)))], fill=(0, 240, 255, 240), width=2)
    d.ellipse([c - 6, c - 6, c + 6, c + 6], fill=(255, 255, 255, 255), outline=(255, 215, 80, 255))
    icons['particle_collision'] = im

    # 2. Penning Trap
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.arc([14, 12, 50, 28], 0, 180, fill=(255, 215, 80, 255), width=2)
    d.arc([14, 36, 50, 52], 180, 360, fill=(255, 215, 80, 255), width=2)
    d.ellipse([c - 10, c - 10, c + 10, c + 10], fill=(0, 240, 255, 220), outline=(255, 255, 255, 255))
    icons['penning_trap'] = im

    # 3. Superconducting Dipole Magnet
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([12, 16, 52, 48], radius=6, fill=(35, 20, 55, 255), outline=(180, 90, 255, 255), width=2)
    d.ellipse([22, 22, 42, 42], fill=(10, 6, 16, 255), outline=(0, 240, 255, 240), width=2)
    d.point((c, c), fill=(255, 255, 255, 255))
    icons['superconducting_magnet'] = im

    # 4. Higgs Boson Discovery
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([c - 22, c - 22, c + 22, c + 22], outline=(255, 215, 80, 240), width=2)
    d.polygon([(c, 16), (46, c), (c, 48), (18, c)], outline=(0, 240, 255, 255), fill=(45, 18, 70, 200))
    d.text((c - 5, c - 7), "H", fill=(255, 255, 255, 255), font=FONT_PANEL)
    icons['higgs_boson'] = im

    # 5. Cryo Liquid Helium
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([18, 14, 46, 50], radius=4, fill=(20, 30, 50, 255), outline=(0, 240, 255, 255), width=2)
    d.rectangle([20, 32, 44, 48], fill=(0, 200, 240, 220)) # Liquid level
    d.text((c - 6, 18), "He", fill=(255, 215, 80, 255), font=FONT_MICRO)
    icons['cryo_helium'] = im

    # 6. Linac RF Cavity Injector
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(3):
        x_cav = 16 + i * 14
        d.ellipse([x_cav, 20, x_cav + 12, 44], fill=(35, 18, 55, 255), outline=(180, 80, 255, 255), width=2)
    d.line([(8, c), (56, c)], fill=(255, 255, 255, 240), width=2)
    icons['beam_injector'] = im

    return icons

def generate_progressbar(w=256, h=16, frac=0.85, bar_type='energy'):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(12, 12, 18, 255), outline=(45, 45, 60, 255))
    d.rectangle([1, 1, w - 2, h - 2], outline=(20, 20, 28, 255))
    
    fill_w = max(0, min(w - 4, int((w - 4) * frac)))
    if fill_w > 0:
        c1, c2 = ((80, 30, 160), (0, 230, 255)) if bar_type == 'energy' else (((30, 140, 70), (80, 255, 140)) if bar_type == 'quench' else ((180, 50, 120), (255, 215, 80)))
        for x in range(fill_w):
            t = x / (w - 4)
            col = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
            d.line([(2 + x, 2), (2 + x, h - 3)], fill=col + (255,))
            d.point((2 + x, 2), fill=(255, 255, 255, 180))
            
    for m in [0.33, 0.66]:
        mx = 2 + int((w - 4) * m)
        d.line([(mx, 0), (mx, h - 1)], fill=(255, 255, 255, 180), width=1)
    return im


# ===========================================================================
# 5. COMPOSED FULL UI PREVIEW (640x480)
# ===========================================================================

def compose_preview_collider(bg_img, title, palette_desc):
    canvas = Image.new('RGBA', (640, 480), (10, 10, 15, 255))
    d = ImageDraw.Draw(canvas)
    
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(70, 75, 95, 255), width=2)
    
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 18, 26, 255), outline=(50, 55, 75, 255), width=2)
    
    # Header
    d.rectangle([16, 12, 624, 40], fill=(24, 24, 34, 255), outline=(60, 65, 85, 255))
    d.text((24, 18), f"GTNA · ANEL COLISOR DE ANTIMATÉRIA [UIV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel contents
    d.text((panel_x + 10, panel_y + 12), "TELEMETRIA DO ANEL", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(60, 65, 85, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Ímãs: Nb₃Sn (12 Tesla)", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "E_feixe: 10.8 TeV (CM 21.6 TeV)", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Luminosidade: 2.1e34 cm⁻²s⁻¹", fill=(80, 255, 140, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Hélio Líquido: 1.0 L/s (1.9 K)", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['particle_collision', 'penning_trap', 'superconducting_magnet', 'higgs_boson']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "ENERGIA DO FEIXE (10.8 TeV)", fill=(255, 215, 80, 255), font=FONT_TEXT)
    pbar_e = generate_progressbar(panel_w - 20, 12, 0.85, 'energy')
    canvas.paste(pbar_e, (panel_x + 10, panel_y + 160), pbar_e)
    
    d.text((panel_x + 10, panel_y + 180), "MARGEM DE QUENCH (84%)", fill=(80, 255, 140, 255), font=FONT_TEXT)
    pbar_q = generate_progressbar(panel_w - 20, 12, 0.84, 'quench')
    canvas.paste(pbar_q, (panel_x + 10, panel_y + 196), pbar_q)
    
    d.text((panel_x + 10, panel_y + 220), "STATUS: HIGGS DESCOBERTO (5.2σ)", fill=(80, 255, 140, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Armadilha Penning: 4.0e12 p̄", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Buttons
    btn_n = generate_button('cosmic', 'normal', 74, 28)
    btn_h = generate_button('cosmic', 'hover', 74, 28)
    btn_p = generate_button('cosmic', 'pressed', 154, 32)
    
    canvas.paste(btn_n, (panel_x + 10, panel_y + 266), btn_n)
    d.text((panel_x + 18, panel_y + 274), "PROPOSTA", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_h, (panel_x + 90, panel_y + 266), btn_h)
    d.text((panel_x + 98, panel_y + 274), "PENNING", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_p, (panel_x + 10, panel_y + 306), btn_p)
    d.text((panel_x + 40, panel_y + 314), "[ COLIDIR ]", fill=(255, 220, 100, 255), font=FONT_BTN)
    
    # Footer
    d.text((16, 442), f"Estilo: {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho do Background: 512x512 (ou Wide 640x360) · Alta Densidade Textural Procedural", fill=(100, 110, 130, 255), font=FONT_TEXT)
    
    return canvas


# ===========================================================================
# 6. UNIFIED COMPARISON OVERVIEW
# ===========================================================================

def generate_comparison_sheet_collider(p1, p2, p3):
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    
    d.rectangle([0, 0, sheet.width, 60], fill=(20, 20, 30, 255), outline=(50, 55, 75, 255))
    d.text((30, 14), "GTNA · COMPARATIVO DE ALTA DILIGÊNCIA VISUAL — MULTIBLOCO 3: ANEL COLISOR DE ANTIMATÉRIA", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "3 Variações Ricas em Detalhes 512x512 (Acelerador & Histograma, Câmara de Bolhas & Modelo Padrão, Matriz Penning)", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    sheet.paste(p1, (10, 75))
    sheet.paste(p2, (sw + 20, 75))
    sheet.paste(p3, (sw * 2 + 30, 75))
    return sheet


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print(">>> Gerando Variações de Alta Diligência (HD) para o Anel Colisor...")
    
    print("  -> Gerando Background 1: Acelerador Relativístico & Histograma (512x512)...")
    bg_1 = generate_bg_variation_1_accelerator(512, 512)
    bg_1.save(os.path.join(BG_DIR, 'bg_variation_1_accelerator_512.png'))
    generate_bg_variation_1_accelerator(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1_accelerator_wide.png'))
    
    print("  -> Gerando Background 2: Câmara de Bolhas Quântica & Modelo Padrão (512x512)...")
    bg_2 = generate_bg_variation_2_bubble_chamber(512, 512)
    bg_2.save(os.path.join(BG_DIR, 'bg_variation_2_bubble_chamber_512.png'))
    generate_bg_variation_2_bubble_chamber(640, 360).save(os.path.join(BG_DIR, 'bg_variation_2_bubble_chamber_wide.png'))
    
    print("  -> Gerando Background 3: Matriz de Contenção de Penning & Criogenia (512x512)...")
    bg_3 = generate_bg_variation_3_penning_cryo(512, 512)
    bg_3.save(os.path.join(BG_DIR, 'bg_variation_3_penning_cryo_512.png'))
    generate_bg_variation_3_penning_cryo(640, 360).save(os.path.join(BG_DIR, 'bg_variation_3_penning_cryo_wide.png'))

    print("  -> Gerando Botões 9-Slice...")
    for state in ['normal', 'hover', 'pressed']:
        btn = generate_button('cosmic', state, 64, 32)
        btn.save(os.path.join(BTN_DIR, f'btn_cosmic_{state}.png'))

    print("  -> Gerando Ícones do Colisor...")
    icons = generate_collider_icons()
    for name, img in icons.items():
        img.save(os.path.join(ICO_DIR, f'ico_{name}_64.png'))
        img_32 = img.resize((32, 32), Image.NEAREST)
        img_32.save(os.path.join(ICO_DIR, f'ico_{name}_32.png'))

    print("  -> Gerando Barras de Energia e Margem de Quench...")
    generate_progressbar(256, 16, 0.85, 'energy').save(os.path.join(BAR_DIR, 'progressbar_beam_energy.png'))
    generate_progressbar(256, 16, 0.84, 'quench').save(os.path.join(BAR_DIR, 'progressbar_quench_margin.png'))

    print("  -> Montando Telas Completas de Preview...")
    prev_1 = compose_preview_collider(bg_1, "Variação 1: Acelerador Relativístico & Histograma", "Anel Síncrotron, Dipolos de Nb₃Sn, Ponto de Colisão & Histograma Invariante 5σ")
    prev_1.save(os.path.join(PREV_DIR, 'preview_variation_1_accelerator.png'))
    
    prev_2 = compose_preview_collider(bg_2, "Variação 2: Câmara de Bolhas & Modelo Padrão", "Espirais de Trajetórias de Lorentz, Detector de Vértice, Setores SM & Higgs 125 GeV")
    prev_2.save(os.path.join(PREV_DIR, 'preview_variation_2_bubble_chamber.png'))
    
    prev_3 = compose_preview_collider(bg_3, "Variação 3: Matriz de Penning & Criogenia", "Armadilha Hiperbólica Quadrupolar, Nuvem de Antiprótons & 8 Setores Criogênicos 1.9 K")
    prev_3.save(os.path.join(PREV_DIR, 'preview_variation_3_penning_cryo.png'))

    print("  -> Gerando Prancha Comparativa Unificada HD...")
    sheet = generate_comparison_sheet_collider(prev_1, prev_2, prev_3)
    sheet.save(os.path.join(OUT_DIR, 'comparison_overview.png'))
    
    print("\n[OK] Todos os assets do Anel Colisor foram gerados com sucesso em:")
    print(f"     {OUT_DIR}")

if __name__ == '__main__':
    main()
