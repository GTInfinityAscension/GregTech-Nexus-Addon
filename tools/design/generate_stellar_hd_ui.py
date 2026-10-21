#!/usr/bin/env python3
"""High-Detail UI Asset Generator for GTNA Multiblock 4: Câmara de Contenção Estelar (Stellar Containment Chamber).

Outputs 3 Ultra-Detailed 512x512 Variations based on the user's preferred Godforge Cosmic Purple theme:
  - Variation 1: "Pulsar de Milissegundo & Feixes Relativísticos" (Incandescent Neutron Star, Dipole Fields, Polar Jets & Seismogram)
  - Variation 2: "Diagrama Astrofísico M–P & Limite TOV" (Mass-Period Evolutionary Plane, Accretion Disk & TOV Boundary)
  - Variation 3: "Ergosfera do Buraco Negro & Processo de Penrose" (Extreme Kerr Black Hole, Photon Ring, Lensing & Penrose Extraction)

Outputs to: tools/design/ui_proposals/stellar_chamber/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'stellar_chamber')
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
def generate_fbm_noise(w, h, octaves=7, persistence=0.55, lacunarity=2.0, seed=42):
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
# 1. BACKGROUND 1: PULSAR DE MILISSEGUNDO & FEIXES RELATIVÍSTICOS
# ===========================================================================

def generate_bg_variation_1_pulsar(w=512, h=512):
    """Incandescent Neutron Star (Godforge background_star style), Relativistic Polar Jets & Seismogram."""
    cx, cy = w // 2, int(h * 0.44)
    
    # 1. Multi-octave FBM Base for Deep Cosmic Gas
    n_base = generate_fbm_noise(w, h, octaves=7, persistence=0.55, seed=1001)
    n_corona = generate_fbm_noise(w, h, octaves=5, persistence=0.62, seed=1002)
    
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    r_norm = r / (w * 0.5)
    theta = np.arctan2(dy, dx)
    
    # 2. Stellar Core & Plasma Coronal Flames (like background_star.png)
    core_glow = np.exp(-(r / 38.0) ** 2) * 1.6
    
    # Magnetic Dipole Coronal Loops: intensity along dipole field lines
    # Field line equation: r = L * sin^2(theta)
    dipole_loops = np.abs(np.sin(theta)) ** 2 * np.exp(-r_norm * 2.0)
    
    # Polar Jets: intense along vertical axis (|dx| < 20)
    jet_width = np.abs(dx) / 22.0
    polar_jets = np.exp(-jet_width * jet_width) * np.exp(-np.abs(dy) / 240.0) * 1.2
    
    # Coronal plasma filaments radiating outward
    rays = 0.5 + 0.5 * np.cos(theta * 16.0 + n_corona * 6.0)
    corona_filaments = rays * np.exp(-r_norm * 1.8) * 0.45
    
    lum = np.clip(n_base * 0.22 + core_glow + polar_jets + corona_filaments + dipole_loops * 0.35, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.18, (24, 8, 44)),
        (0.35, (65, 18, 92)),
        (0.55, (135, 32, 160)),
        (0.72, (205, 55, 215)),
        (0.85, (0, 225, 255)),
        (0.94, (255, 235, 160)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # 3. Dense Field of Stars
    rng = np.random.default_rng(2026)
    for _ in range(260):
        sx = rng.integers(10, w - 10)
        sy = rng.integers(10, h - 10)
        if math.hypot(sx - cx, sy - cy) < 42:
            continue
        bright = rng.uniform(0.2, 1.0)
        if bright > 0.94:
            scol = (255, 240, 180, 240) if rng.random() > 0.5 else (160, 240, 255, 240)
            d.line([(sx - 4, sy), (sx + 4, sy)], fill=scol, width=1)
            d.line([(sx, sy - 4), (sx, sy + 4)], fill=scol, width=1)
            d.point((sx, sy), fill=(255, 255, 255, 255))
        else:
            d.point((sx, sy), fill=(160, 180, 230, int(180 * bright)))
            
    # 4. 4 Concentric Neutronium Containment Bands
    band_radii = [60, 90, 120, 150]
    for b_idx, r_b in enumerate(band_radii):
        col_b = (255, 215, 80, 200) if b_idx == 3 else (160, 90, 240, 140)
        d.ellipse([cx - r_b, cy - r_b, cx + r_b, cy + r_b], outline=col_b, width=2)
        # Vernier degree ticks
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            p1 = (cx + int((r_b - 3) * math.cos(rad)), cy + int((r_b - 3) * math.sin(rad)))
            p2 = (cx + int((r_b + 3) * math.cos(rad)), cy + int((r_b + 3) * math.sin(rad)))
            d.line([p1, p2], fill=(0, 240, 255, 140), width=1)
            
    # Magnetic field dipole loop arches (golden and cyan)
    d.arc([cx - 100, cy - 80, cx + 100, cy + 80], -60, 60, fill=(0, 240, 255, 160), width=2)
    d.arc([cx - 100, cy - 80, cx + 100, cy + 80], 120, 240, fill=(0, 240, 255, 160), width=2)
    
    # Central Incandescent Neutron Star Core
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(255, 255, 255, 255), outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 240, 255))
    
    # 5. Integrated Crust Seismogram & Glitch Analyzer (Bottom 136px)
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(10, 6, 20, 240), outline=(75, 38, 120, 255), width=2)
    d.rectangle([16, box_y + 2, w - 16, box_y + box_h - 2], outline=(32, 16, 52, 255), width=1)
    
    seismo_zero = box_y + box_h // 2 - 8
    d.line([(22, seismo_zero), (w - 22, seismo_zero)], fill=(85, 45, 140, 180), width=1)
    for gy in range(box_y + 14, box_y + box_h - 10, 18):
        d.line([(22, gy), (w - 22, gy)], fill=(34, 20, 58, 100), width=1)
        
    # Real Pulsar Glitch Seismic Waveform (Vela-like crustquake trace)
    rng_seismo = np.random.default_rng(55)
    pts_seismo = []
    for x_pos in range(22, w - 22):
        dist_from_left = x_pos - 22
        # Baseline noise
        y_val = rng_seismo.uniform(-2.0, 2.0)
        # Giant Glitch Event at x = 160
        glitch1 = 26.0 * math.exp(-((dist_from_left - 138) / 8.0) ** 2) * math.sin(dist_from_left * 0.8)
        # Secondary Glitch at x = 320
        glitch2 = 18.0 * math.exp(-((dist_from_left - 298) / 6.0) ** 2) * math.sin(dist_from_left * 1.2)
        total_disp = int(seismo_zero - (y_val + glitch1 + glitch2))
        pts_seismo.append((x_pos, total_disp))
        
    # Draw glow & crisp line
    d.line(pts_seismo, fill=(0, 200, 255, 90), width=3)
    d.line(pts_seismo, fill=(0, 240, 255, 240), width=1)
    
    # Glitch Marker Annotations
    d.line([(160, box_y + 22), (160, box_y + box_h - 24)], fill=(255, 215, 80, 180), width=1)
    d.text((26, box_y + 6), "SISMOGRAMA (0–200 Hz)", fill=(160, 170, 190, 220), font=FONT_MICRO)
    d.text((164, box_y + 6), "GLITCH: ΔΩ/Ω = 1.1e-6 [VELA]", fill=(255, 215, 80, 255), font=FONT_MICRO)
    d.text((w - 150, box_y + 6), "EJEÇÃO: MAT. DEGENERADA", fill=(80, 255, 140, 255), font=FONT_MICRO)
    d.text((26, box_y + box_h - 18), "TENSÃO: σ = 0.64 [OK]", fill=(80, 255, 140, 255), font=FONT_MICRO)
    d.text((w - 146, box_y + box_h - 18), "BANDAS: 4/4 [TIER 4]", fill=(255, 215, 80, 255), font=FONT_MICRO)


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
# 2. BACKGROUND 2: DIAGRAMA ASTROFÍSICO M–P & LIMITE TOV
# ===========================================================================

def generate_bg_variation_2_mp_diagram(w=512, h=512):
    """2D Mass-Period Astrophysical Evolutionary Plane + Spiral Accretion Disk."""
    cx, cy = w // 2, int(h * 0.44)
    
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.56, seed=2001)
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    
    lum = np.clip(n_base * 0.35 + np.exp(-r / 180.0) * 0.45, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.22, (22, 10, 38)),
        (0.45, (55, 20, 80)),
        (0.70, (110, 35, 140)),
        (0.88, (0, 210, 230)),
        (1.00, (240, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Holographic Mass-Period Plane Chart
    chart_x0, chart_x1 = 36, w - 36
    chart_y0, chart_y1 = 28, int(h * 0.66)
    
    # Coordinate Axes
    d.rectangle([chart_x0, chart_y0, chart_x1, chart_y1], fill=(12, 8, 24, 210), outline=(85, 45, 140, 220), width=2)
    
    # Region shading
    # Pulsar Comum (P > 30 ms): Blue tint
    d.rectangle([chart_x0 + 2, chart_y0 + 2, chart_x1 - 2, chart_y0 + 45], fill=(30, 45, 90, 80))
    d.text((chart_x0 + 8, chart_y0 + 6), "PULSAR COMUM (P > 30 ms)", fill=(140, 180, 255, 220), font=FONT_MICRO)
    
    # Recente (10 < P < 30 ms): Green tint
    d.rectangle([chart_x0 + 2, chart_y0 + 46, chart_x1 - 2, chart_y0 + 95], fill=(20, 75, 60, 80))
    d.text((chart_x0 + 8, chart_y0 + 50), "PULSAR RECENTE (10–30 ms) [Crosta Acelerada]", fill=(80, 255, 180, 220), font=FONT_MICRO)
    
    # Milissegundo (P < 10 ms): Cyan/Gold tint
    d.rectangle([chart_x0 + 2, chart_y0 + 96, chart_x1 - 2, chart_y0 + 155], fill=(70, 60, 20, 90))
    d.text((chart_x0 + 8, chart_y0 + 100), "MILISSEGUNDO RECICLADO (P < 10 ms) [Potência Máxima]", fill=(255, 215, 80, 240), font=FONT_MICRO)

    # TOV Collapse Boundary (Vertical Red Line at M = 2.2 Msol)
    tov_x = chart_x0 + int((chart_x1 - chart_x0) * 0.78)
    for dy_pos in range(chart_y0, chart_y1, 6):
        d.line([(tov_x, dy_pos), (tov_x, dy_pos + 3)], fill=(255, 60, 60, 240), width=2)
    d.rectangle([tov_x + 1, chart_y0 + 2, chart_x1 - 2, chart_y1 - 2], fill=(60, 10, 20, 120))
    d.text((tov_x + 6, chart_y0 + 16), "LIMITE TOV (2.2 M☉)", fill=(255, 80, 80, 255), font=FONT_MICRO)
    d.text((tov_x + 6, chart_y0 + 28), "COLAPSO EM", fill=(255, 80, 80, 255), font=FONT_MICRO)
    d.text((tov_x + 6, chart_y0 + 40), "BURACO NEGRO", fill=(255, 80, 80, 255), font=FONT_MICRO)
    
    # Kepler Breakup Limit Curve (Lower boundary)
    pts_kepler = []
    for x_step in range(chart_x0 + 2, tov_x):
        t_frac = (x_step - chart_x0) / (chart_x1 - chart_x0)
        m_val = 1.0 + t_frac * 1.4
        p_kepler = 0.75 / math.sqrt(m_val)
        y_pos = chart_y1 - 12 - int(p_kepler * 18)
        pts_kepler.append((x_step, y_pos))
    d.line(pts_kepler, fill=(255, 120, 40, 220), width=2)
    d.text((chart_x0 + 8, chart_y1 - 20), "LIMITE DE QUEBRA DE KEPLER (P_min)", fill=(255, 140, 60, 220), font=FONT_MICRO)

    # Star's Evolutionary Trajectory (Dots and dashed vector)
    star_track = [
        (chart_x0 + 40, chart_y0 + 25),
        (chart_x0 + 75, chart_y0 + 55),
        (chart_x0 + 120, chart_y0 + 85),
        (chart_x0 + 180, chart_y0 + 115),
        (chart_x0 + 235, chart_y0 + 140)
    ]
    for i in range(len(star_track) - 1):
        d.line([star_track[i], star_track[i + 1]], fill=(255, 215, 80, 240), width=2)
        d.ellipse([star_track[i][0] - 3, star_track[i][1] - 3, star_track[i][0] + 3, star_track[i][1] + 3], fill=(0, 240, 255, 255))
        
    # Current Star Position (Glowing Pulsar Star at tip)
    cur_x, cur_y = star_track[-1]
    d.ellipse([cur_x - 8, cur_y - 8, cur_x + 8, cur_y + 8], fill=(255, 255, 255, 255), outline=(255, 215, 80, 255), width=2)
    d.text((cur_x - 30, cur_y - 18), "ATUAL: 1.62 M☉ · 3.8 ms", fill=(255, 255, 255, 255), font=FONT_MICRO)

    # Bottom Telemetry Box
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(8, 6, 18, 240), outline=(60, 75, 130, 255), width=2)
    d.text((26, box_y + 10), "ALIMENTAÇÃO & SPIN-UP DO DISCO DE ACREÇÃO", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 170, box_y + 10), "ENERGIA ROTACIONAL: 1.24e25 EU", fill=(255, 215, 80, 240), font=FONT_MICRO)
    
    d.rectangle([26, box_y + 36, w - 26, box_y + 54], fill=(14, 12, 24, 255), outline=(50, 60, 100, 255))
    d.rectangle([28, box_y + 38, 28 + int((w - 56) * 0.72), box_y + 52], fill=(240, 180, 40, 220))
    d.text((36, box_y + 40), "Massa Atual: 1.62 M☉ / 2.20 M☉ (Margem TOV: 0.58 M☉)", fill=(255, 255, 255, 255), font=FONT_MICRO)

    d.rectangle([5, 5, w - 6, h - 6], outline=(75, 100, 180, 255), width=2)
    return im


# ===========================================================================
# 3. BACKGROUND 3: ERGOSFERA DO BURACO NEGRO & PROCESSO DE PENROSE
# ===========================================================================

def generate_bg_variation_3_kerr_black_hole(w=512, h=512):
    """Post-Collapse Kerr Black Hole (a*=0.998), Oblate Ergosphere, Photon Ring & Penrose Extraction."""
    cx, cy = w // 2, int(h * 0.44)
    
    n_base = generate_fbm_noise(w, h, octaves=7, persistence=0.55, seed=3001)
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    
    # Gravitational Lensing & Oblate Ergosphere: r_ergo = M + sqrt(M^2 - a^2 * cos^2(theta))
    r = np.sqrt(dx * dx + (dy * 1.35) ** 2) # Oblate due to extreme spin
    
    # Accretion ring around r ~ 80px
    ring_dist = np.abs(r - 70.0) / 35.0
    accretion_glow = np.exp(-ring_dist * ring_dist * 2.2) * 1.1
    
    # Event horizon blackout in the very center
    horizon_mask = np.clip((r - 26.0) / 10.0, 0.0, 1.0)
    
    lum = np.clip((n_base * 0.35 + accretion_glow) * horizon_mask, 0.0, 1.0)
    
    stops = [
        (0.00, (4, 2, 8)),
        (0.20, (18, 6, 32)),
        (0.40, (50, 15, 75)),
        (0.65, (115, 30, 150)),
        (0.80, (200, 50, 215)),
        (0.92, (0, 240, 255)),
        (1.00, (255, 255, 255))
    ]
    
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Oblate Ergosphere Boundary (Ultraviolet & Gold)
    d.ellipse([cx - 85, cy - 65, cx + 85, cy + 65], outline=(255, 215, 80, 220), width=2)
    d.ellipse([cx - 95, cy - 75, cx + 95, cy + 75], outline=(0, 240, 255, 140), width=1)
    
    # Pure Black Hole Event Horizon in Center
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(0, 0, 0, 255), outline=(0, 240, 255, 255), width=2)
    # Photon sphere ring
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], outline=(255, 255, 255, 240), width=1)
    
    # Penrose Energy Extraction Spiral Flow Lines
    for angle_start in [0, 60, 120, 180, 240, 300]:
        rad_base = math.radians(angle_start)
        pts_penrose = []
        for step in range(30):
            dist_p = 34 + step * 4.5
            rot_drag = math.radians(step * 15.0) # Frame dragging
            px_p = cx + int(dist_p * math.cos(rad_base + rot_drag))
            py_p = cy + int((dist_p * 0.8) * math.sin(rad_base + rot_drag))
            pts_penrose.append((px_p, py_p))
        d.line(pts_penrose, fill=(0, 240, 255, 180), width=1)

    # Bottom Penrose Efficiency Monitor
    box_y = int(h * 0.70)
    box_h = 136
    d.rectangle([14, box_y, w - 14, box_y + box_h], fill=(8, 6, 18, 240), outline=(80, 45, 130, 255), width=2)
    d.text((26, box_y + 10), "EXTRAÇÃO DE ENERGIA DA ERGOSFERA · PROCESSO DE PENROSE", fill=(0, 240, 255, 240), font=FONT_MICRO)
    d.text((w - 170, box_y + 10), "SPIN KERR: a* = 0.998 [MÁXIMO]", fill=(255, 215, 80, 240), font=FONT_MICRO)
    
    d.rectangle([26, box_y + 36, w - 26, box_y + 54], fill=(14, 12, 24, 255), outline=(50, 60, 100, 255))
    d.rectangle([28, box_y + 38, 28 + int((w - 56) * 0.99), box_y + 52], fill=(160, 60, 220, 220))
    d.text((36, box_y + 40), "Eficiência de Extração: η = 27.1% · Potência: 4.61e18 EU/t (2^62)", fill=(255, 255, 255, 255), font=FONT_MICRO)

    d.rectangle([5, 5, w - 6, h - 6], outline=(125, 55, 185, 255), width=2)
    return im


# ===========================================================================
# 4. BUTTONS & ICONS & PROGRESS BARS
# ===========================================================================

def generate_button(theme, state='normal', w=64, h=32):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if state == 'normal':
        bg_top, bg_bot = (54, 26, 84), (32, 14, 52)
        border_outer, border_inner = (95, 45, 150), (145, 75, 220)
        glow_corner = (200, 140, 255)
    elif state == 'hover':
        bg_top, bg_bot = (78, 38, 118), (48, 22, 75)
        border_outer, border_inner = (130, 65, 200), (190, 110, 255)
        glow_corner = (235, 190, 255)
    else:
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

def generate_stellar_icons():
    icons = {}
    c = 32
    
    # 1. Neutron Star Pulsar
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.line([(c, 6), (c, 58)], fill=(0, 240, 255, 200), width=3)
    d.ellipse([c - 14, c - 14, c + 14, c + 14], fill=(255, 255, 255, 255), outline=(255, 215, 80, 255), width=2)
    d.arc([c - 22, c - 18, c + 22, c + 18], -50, 50, fill=(180, 80, 255, 240), width=2)
    d.arc([c - 22, c - 18, c + 22, c + 18], 130, 230, fill=(180, 80, 255, 240), width=2)
    icons['neutron_star'] = im

    # 2. Containment Band
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([10, 16, 54, 48], outline=(180, 80, 255, 240), width=3)
    d.ellipse([16, 22, 48, 42], outline=(255, 215, 80, 240), width=2)
    d.point((c, c), fill=(255, 255, 255, 255))
    icons['containment_band'] = im

    # 3. Stellar Seismogram Glitch
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([8, 14, 56, 50], fill=(16, 12, 26, 255), outline=(80, 45, 120, 255))
    ys = [32, 32, 30, 34, 18, 46, 24, 34, 32, 32]
    pts = [(10 + i * 4.4, ys[i]) for i in range(len(ys))]
    d.line(pts, fill=(0, 240, 255, 255), width=2)
    icons['stellar_seismogram'] = im

    # 4. Mass Injector Disc
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(c, 10), (48, 24), (c, 34), (16, 24)], fill=(180, 80, 255, 200), outline=(255, 215, 80, 255))
    d.line([(c, 34), (c, 54)], fill=(0, 240, 255, 240), width=3)
    icons['mass_injector'] = im

    # 5. Degenerate Matter Cell
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([14, 14, 50, 50], radius=6, fill=(20, 14, 32, 255), outline=(255, 215, 80, 255), width=2)
    d.polygon([(c, 20), (44, c), (c, 44), (20, c)], fill=(160, 60, 220, 240), outline=(255, 255, 255, 255))
    icons['degenerate_matter'] = im

    # 6. Ergosphere Penrose Vortex
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse([12, 16, 52, 48], outline=(255, 215, 80, 240), width=2)
    d.ellipse([22, 22, 42, 42], fill=(0, 0, 0, 255), outline=(0, 240, 255, 255), width=2)
    icons['ergosphere_penrose'] = im

    return icons

def generate_progressbar(w=256, h=16, frac=0.85, bar_type='energy'):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], fill=(12, 12, 18, 255), outline=(45, 45, 60, 255))
    d.rectangle([1, 1, w - 2, h - 2], outline=(20, 20, 28, 255))
    
    fill_w = max(0, min(w - 4, int((w - 4) * frac)))
    if fill_w > 0:
        c1, c2 = ((80, 30, 160), (255, 215, 80)) if bar_type == 'energy' else (((30, 140, 70), (0, 240, 255)) if bar_type == 'stress' else ((180, 50, 120), (255, 240, 180)))
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

def compose_preview_stellar(bg_img, title, palette_desc):
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
    d.text((24, 18), f"GTNA · CÂMARA DE CONTENÇÃO ESTELAR [MAX] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel contents
    d.text((panel_x + 10, panel_y + 12), "TELEMETRIA ESTELAR", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(60, 65, 85, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Massa: 1.62 M☉ (Pulsar)", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Período: 3.8 ms (263 Hz)", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Extração: 2^58 EU/t", fill=(255, 215, 80, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Bandas: 4/4 (Tier 4)", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['neutron_star', 'containment_band', 'stellar_seismogram', 'degenerate_matter']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "ENERGIA ROTACIONAL (1.24e25 EU)", fill=(255, 215, 80, 255), font=FONT_TEXT)
    pbar_e = generate_progressbar(panel_w - 20, 12, 0.88, 'energy')
    canvas.paste(pbar_e, (panel_x + 10, panel_y + 160), pbar_e)
    
    d.text((panel_x + 10, panel_y + 180), "TENSÃO DA CROSTA (σ = 0.64)", fill=(80, 255, 140, 255), font=FONT_TEXT)
    pbar_s = generate_progressbar(panel_w - 20, 12, 0.64, 'stress')
    canvas.paste(pbar_s, (panel_x + 10, panel_y + 196), pbar_s)
    
    d.text((panel_x + 10, panel_y + 218), "REGIME: MILISSEGUNDO", fill=(80, 255, 140, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 234), "Ejeção: Matéria Degenerada", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Buttons
    btn_n = generate_button('cosmic', 'normal', 74, 28)
    btn_h = generate_button('cosmic', 'hover', 74, 28)
    btn_p = generate_button('cosmic', 'pressed', 154, 32)
    
    canvas.paste(btn_n, (panel_x + 10, panel_y + 266), btn_n)
    d.text((panel_x + 18, panel_y + 274), "INJETAR", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_h, (panel_x + 90, panel_y + 266), btn_h)
    d.text((panel_x + 98, panel_y + 274), "EXTRAIR", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_p, (panel_x + 10, panel_y + 306), btn_p)
    d.text((panel_x + 36, panel_y + 314), "[ SPIN-UP ]", fill=(255, 220, 100, 255), font=FONT_BTN)
    
    # Footer
    d.text((16, 442), f"Estilo: {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho do Background: 512x512 (ou Wide 640x360) · Alta Densidade Textural Procedural", fill=(100, 110, 130, 255), font=FONT_TEXT)
    
    return canvas


# ===========================================================================
# 6. UNIFIED COMPARISON OVERVIEW
# ===========================================================================

def generate_comparison_sheet_stellar(p1, p2, p3):
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    
    d.rectangle([0, 0, sheet.width, 60], fill=(20, 20, 30, 255), outline=(50, 55, 75, 255))
    d.text((30, 14), "GTNA · COMPARATIVO DE ALTA DILIGÊNCIA VISUAL — MULTIBLOCO 4: CÂMARA DE CONTENÇÃO ESTELAR", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "3 Variações Ricas em Detalhes 512x512 (Pulsar & Feixes Relativísticos, Diagrama M-P & Limite TOV, Ergosfera Kerr)", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    sheet.paste(p1, (10, 75))
    sheet.paste(p2, (sw + 20, 75))
    sheet.paste(p3, (sw * 2 + 30, 75))
    return sheet


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print(">>> Gerando Variações de Alta Diligência (HD) para a Câmara de Contenção Estelar...")
    
    print("  -> Gerando Background 1: Pulsar de Milissegundo & Sismograma (512x512)...")
    bg_1 = generate_bg_variation_1_pulsar(512, 512)
    bg_1.save(os.path.join(BG_DIR, 'bg_variation_1_pulsar_512.png'))
    generate_bg_variation_1_pulsar(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1_pulsar_wide.png'))
    
    print("  -> Gerando Background 2: Diagrama Astrofísico M-P & Limite TOV (512x512)...")
    bg_2 = generate_bg_variation_2_mp_diagram(512, 512)
    bg_2.save(os.path.join(BG_DIR, 'bg_variation_2_mp_diagram_512.png'))
    generate_bg_variation_2_mp_diagram(640, 360).save(os.path.join(BG_DIR, 'bg_variation_2_mp_diagram_wide.png'))
    
    print("  -> Gerando Background 3: Ergosfera do Buraco Negro & Processo de Penrose (512x512)...")
    bg_3 = generate_bg_variation_3_kerr_black_hole(512, 512)
    bg_3.save(os.path.join(BG_DIR, 'bg_variation_3_kerr_black_hole_512.png'))
    generate_bg_variation_3_kerr_black_hole(640, 360).save(os.path.join(BG_DIR, 'bg_variation_3_kerr_black_hole_wide.png'))

    print("  -> Gerando Botões 9-Slice...")
    for state in ['normal', 'hover', 'pressed']:
        btn = generate_button('cosmic', state, 64, 32)
        btn.save(os.path.join(BTN_DIR, f'btn_cosmic_{state}.png'))

    print("  -> Gerando Ícones da Câmara Estelar...")
    icons = generate_stellar_icons()
    for name, img in icons.items():
        img.save(os.path.join(ICO_DIR, f'ico_{name}_64.png'))
        img_32 = img.resize((32, 32), Image.NEAREST)
        img_32.save(os.path.join(ICO_DIR, f'ico_{name}_32.png'))

    print("  -> Gerando Barras de Energia Rotacional e Tensão Sísmica...")
    generate_progressbar(256, 16, 0.88, 'energy').save(os.path.join(BAR_DIR, 'progressbar_rotational_energy.png'))
    generate_progressbar(256, 16, 0.64, 'stress').save(os.path.join(BAR_DIR, 'progressbar_crust_stress.png'))

    print("  -> Montando Telas Completas de Preview...")
    prev_1 = compose_preview_stellar(bg_1, "Variação 1: Pulsar de Milissegundo & Feixes", "Estrela Incandescente, Feixes Polares, 4 Bandas de Neutrônio & Sismograma Tipo Vela")
    prev_1.save(os.path.join(PREV_DIR, 'preview_variation_1_pulsar.png'))
    
    prev_2 = compose_preview_stellar(bg_2, "Variação 2: Diagrama M–P & Limite TOV", "Plano Evolutivo Massa-Período, Limite de Colapso TOV 2.2 M☉ & Trajetória de Spin-up")
    prev_2.save(os.path.join(PREV_DIR, 'preview_variation_2_mp_diagram.png'))
    
    prev_3 = compose_preview_stellar(bg_3, "Variação 3: Ergosfera Kerr & Processo de Penrose", "Buraco Negro em Rotação a*=0.998, Anel de Fótons & Extração de Penrose 4.61e18 EU/t")
    prev_3.save(os.path.join(PREV_DIR, 'preview_variation_3_kerr_black_hole.png'))

    print("  -> Gerando Prancha Comparativa Unificada HD...")
    sheet = generate_comparison_sheet_stellar(prev_1, prev_2, prev_3)
    sheet.save(os.path.join(OUT_DIR, 'comparison_overview.png'))
    
    print("\n[OK] Todos os assets da Câmara Estelar foram gerados com sucesso em:")
    print(f"     {OUT_DIR}")

if __name__ == '__main__':
    main()
