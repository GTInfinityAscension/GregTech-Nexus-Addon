#!/usr/bin/env python3
"""Generate all 3 tabs for GTNA Multiblock 2: Portão de Fenda Dimensional (Dimensional Rift Gate - UIV):
  - Tab 1: Vórtice de Fenda & Horizonte (Volumetric Wormhole & Event Horizon - Approved Winner 1A)
  - Tab 2: Roda de Acordes & Pauta Harmônica (Chord Wheel & Harmonic Staff matching OriginalsGui.atlas & RiftCore.Harmonic - NO PHANTOM PYLONS)
  - Tab 3: Atlas de Sementes & Cartografia Dimensional (Deep Space Charted Rifts & Seed Coordinates)

Outputs to: tools/design/ui_proposals/rift_gate/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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

def generate_fbm_noise(w, h, octaves=7, persistence=0.55, lacunarity=2.0, seed=42):
    rng = np.random.default_rng(seed)
    grid = np.zeros((h, w), dtype=np.float32)
    amplitude, total_amp = 1.0, 0.0
    for oct_idx in range(octaves):
        freq = int(4 * (lacunarity ** oct_idx))
        if freq >= min(w, h): break
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
        if not np.any(mask): continue
        t = ((values[mask] - p0) / (p1 - p0))[:, np.newaxis]
        out[mask] = np.array(c0, dtype=np.float32) + (np.array(c1, dtype=np.float32) - np.array(c0, dtype=np.float32)) * t
    out[values < stops[0][0]] = np.array(stops[0][1], dtype=np.float32)
    out[values > stops[-1][0]] = np.array(stops[-1][1], dtype=np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)

# The 8 Harmonics from RiftCore.Harmonic
RIFT_HARMONICS = [
    ("OCTAVE", "Oitava", 2, 1, "2:1", True),
    ("FIFTH", "Quinta Justa", 3, 2, "3:2", True),
    ("FOURTH", "Quarta Justa", 4, 3, "4:3", True),
    ("MAJOR_THIRD", "Terça Maior", 5, 4, "5:4", True),
    ("MINOR_SIXTH", "Sexta Menor", 8, 5, "8:5", True),
    ("MINOR_SEVENTH", "Sétima Menor", 9, 5, "9:5", False),
    ("TRITONE", "Trítono", 45, 32, "45:32", False),
    ("MINOR_SECOND", "Segunda Menor", 16, 15, "16:15", False),
]

# ===========================================================================
# TAB 2: RODA DE ACORDES & PAUTA HARMÔNICA (CHORD WHEEL - NO PYLONS)
# ===========================================================================
def generate_bg_tab2_harmonic_score(w=512, h=512, clean=False):
    """Accurate Chord Wheel & Harmonic Staff matching OriginalsGui.atlas and RiftCore.Harmonic.
    NO phantom pylons. The 8 harmonic ratios form a circular chord wheel with loaded harmonies
    joined by resonant polygon lines, standing wave scope, and tuning slots."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.54, seed=2202)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.38 + 0.08, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 15)),
        (0.35, (26, 10, 48)),
        (0.65, (60, 20, 95)),
        (0.85, (0, 220, 255)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "PORTÃO DE FENDA · RODA DE ACORDES & HARMÔNICOS DE FENDA", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 210, 26), "SINTONIA: HATCH DE AFINAÇÃO (TUNING)", fill=(255, 215, 80, 240), font=FONT_MICRO)

    # Left Section: The Sacred Chord Wheel (Roda de Acordes)
    # Circle with the 8 Harmonics from RiftCore.Harmonic
    wheel_cx = 145
    wheel_cy = 165
    wheel_r = 95
    
    # Outer glowing compass circle
    d.ellipse([wheel_cx - wheel_r, wheel_cy - wheel_r, wheel_cx + wheel_r, wheel_cy + wheel_r],
              outline=(75, 45, 115, 255), width=2)
    d.ellipse([wheel_cx - wheel_r - 4, wheel_cy - wheel_r - 4, wheel_cx + wheel_r + 4, wheel_cy + wheel_r + 4],
              outline=(0, 240, 255, 60), width=1)
              
    # Harmonic node positions along circle
    pts = []
    loaded_pts = []
    for i, (hid, hname, p, q, ratio_str, loaded) in enumerate(RIFT_HARMONICS):
        ang = 2 * math.pi * i / len(RIFT_HARMONICS) - math.pi / 2
        nx = int(wheel_cx + math.cos(ang) * wheel_r)
        ny = int(wheel_cy + math.sin(ang) * wheel_r)
        pts.append((nx, ny))
        if loaded:
            loaded_pts.append((nx, ny))
            
    # Draw geometric resonance chord lines between loaded harmonics
    for i in range(len(loaded_pts)):
        p1 = loaded_pts[i]
        p2 = loaded_pts[(i + 1) % len(loaded_pts)]
        d.line([p1, p2], fill=(160, 60, 255, 220), width=2)
        # Cross diagonals
        p3 = loaded_pts[(i + 2) % len(loaded_pts)]
        d.line([p1, p3], fill=(0, 240, 255, 120), width=1)
        
    # Draw Harmonic Nodes on Circle
    for i, (hid, hname, p, q, ratio_str, loaded) in enumerate(RIFT_HARMONICS):
        nx, ny = pts[i]
        ncol = (0, 240, 255) if loaded else (140, 150, 170)
        d.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=ncol + (255,), outline=(255, 255, 255, 255))
        if not clean:
            # Text label offset
            dx_t = 12 if nx >= wheel_cx else -32
            dy_t = -6 if abs(ny - wheel_cy) < 20 else (10 if ny > wheel_cy else -16)
            d.text((nx + dx_t, ny + dy_t), ratio_str, fill=ncol + (255,), font=FONT_MICRO)

    # Right Section: Harmonic Staff & 5-Slot Loaded Score
    staff_x0 = 265
    staff_x1 = w - 28
    staff_y0 = 48
    staff_h = 230
    d.rectangle([staff_x0, staff_y0, staff_x1, staff_y0 + staff_h], fill=(12, 6, 22, 230), outline=(75, 38, 120, 255), width=2)
    
    if not clean:
        d.text((staff_x0 + 10, staff_y0 + 8), "PAUTA MUSICAL DE RESSONÂNCIA (5 SLOTS CARREGADOS)", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
    # 5 Horizontal Musical Staff Lines
    base_line_y = staff_y0 + 38
    spacing = 18
    for line_idx in range(5):
        ly = base_line_y + line_idx * spacing
        d.line([(staff_x0 + 15, ly), (staff_x1 - 15, ly)], fill=(255, 215, 80, 140), width=1)
        
    # Musical note markers for the loaded harmonics
    note_slots = [
        (staff_x0 + 40, base_line_y + 0 * spacing, "2:1", "Oitava", (0, 240, 255)),
        (staff_x0 + 78, base_line_y + 1 * spacing, "3:2", "Quinta", (80, 255, 140)),
        (staff_x0 + 116, base_line_y + 2 * spacing, "4:3", "Quarta", (0, 240, 255)),
        (staff_x0 + 154, base_line_y + 3 * spacing, "5:4", "Terça", (255, 215, 80)),
        (staff_x0 + 192, base_line_y + 4 * spacing, "8:5", "Sexta", (180, 100, 255)),
    ]
    for nx, ny, nratio, nname, ncol in note_slots:
        d.ellipse([nx - 6, ny - 6, nx + 6, ny + 6], fill=ncol + (255,), outline=(255, 255, 255, 255), width=2)
        d.line([(nx + 6, ny), (nx + 6, ny - 20)], fill=ncol + (255,), width=2)
        d.line([(nx + 6, ny - 20), (nx + 14, ny - 17)], fill=ncol + (255,), width=2)
        if not clean:
            d.text((nx - 10, ny + 8), nratio, fill=ncol + (255,), font=FONT_MICRO)
            
    # Standing Wave Scope below staff
    wave_y = staff_y0 + 160
    d.line([(staff_x0 + 15, wave_y), (staff_x1 - 15, wave_y)], fill=(60, 40, 85, 255), width=1)
    if not clean:
        d.text((staff_x0 + 15, wave_y - 14), "ONDA ESTACIONÁRIA INTERDIMENSIONAL (FASE TRAVADA 100%)", fill=(0, 240, 255, 200), font=FONT_MICRO)
        
    wave_pts = []
    for px in range(staff_x0 + 15, staff_x1 - 15):
        rad = (px - staff_x0) * 0.05
        wy = wave_y + int(math.sin(rad) * 18 * math.cos(rad * 0.3) + math.sin(rad * 2.5) * 5)
        wave_pts.append((px, wy))
    for i in range(len(wave_pts) - 1):
        d.line([wave_pts[i], wave_pts[i + 1]], fill=(0, 240, 255, 220), width=2)
        
    # Lower Section: Charted Rifts Atlas Star Map (from OriginalsGui.atlas)
    box_y = staff_y0 + staff_h + 12
    box_h = h - box_y - 20
    d.rectangle([28, box_y, w - 28, box_y + box_h], fill=(10, 6, 18, 240), outline=(75, 38, 120, 255), width=2)
    
    if not clean:
        d.text((38, box_y + 8), "FENDAS VISITADAS (ATLAS) · 24 SEMENTES", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
        # Deep space charted stars
        rng = np.random.default_rng(777)
        for _ in range(35):
            sx = rng.integers(38, w - 38)
            sy = rng.integers(box_y + 24, box_y + box_h - 15)
            depth = rng.integers(1, 4)
            bright = rng.integers(120, 255)
            scol = (bright // 2, bright, 255, 255) if rng.random() > 0.4 else (255, bright, 100, 255)
            d.ellipse([sx - depth, sy - depth, sx + depth, sy + depth], fill=scol)
            if depth >= 2:
                d.arc([sx - depth - 2, sy - depth - 2, sx + depth + 2, sy + depth + 2], start=0, end=360, fill=(0, 240, 255, 100))
                
        # Constellation connection lines
        d.line([(85, box_y + 50), (160, box_y + 80)], fill=(120, 60, 200, 160), width=1)
        d.line([(160, box_y + 80), (280, box_y + 45)], fill=(120, 60, 200, 160), width=1)
        d.line([(280, box_y + 45), (390, box_y + 90)], fill=(120, 60, 200, 160), width=1)
        d.text((45, box_y + box_h - 18), "CATÁLOGO DE PROFUNDIDADE: SONDAS RETORNARAM 100% TELEMETRIA ESTÁVEL", fill=(80, 255, 140, 255), font=FONT_MICRO)
        
    return im

# ===========================================================================
# TAB 3: ATLAS DE CONSTELAÇÕES (CONSTELLATION ATLAS & SEED MAP)
# ===========================================================================
def generate_bg_tab3_constellation_atlas(w=512, h=512, clean=False):
    """Deep space starfield with glowing constellation network, seed nodes & dimensional catalog."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=2303)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.08, 0.0, 1.0)
    
    stops = [
        (0.00, (4, 3, 12)),
        (0.35, (20, 8, 42)),
        (0.65, (50, 16, 85)),
        (0.85, (0, 200, 240)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "ATLAS CELESTIAL DE CONSTELAÇÕES · CARTOGRAFIA DE SEMENTES", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 180, 26), "ATLAS: 16 SEMENTES", fill=(255, 215, 80, 240), font=FONT_MICRO)

    # Star Map Chart Area
    map_y0 = 48
    map_h = int(h * 0.58)
    d.rectangle([28, map_y0, w - 28, map_y0 + map_h], fill=(8, 4, 16, 230), outline=(75, 38, 120, 255), width=2)
    
    # Celestial Coordinate Grid Lines (Polar concentric circles)
    mcx, mcy = w // 2, map_y0 + map_h // 2
    for cr in [40, 80, 120, 160]:
        d.ellipse([mcx - cr, mcy - cr, mcx + cr, mcy + cr], outline=(40, 25, 65, 120), width=1)
    d.line([(mcx, map_y0 + 5), (mcx, map_y0 + map_h - 5)], fill=(40, 25, 65, 120), width=1)
    d.line([(35, mcy), (w - 35, mcy)], fill=(40, 25, 65, 120), width=1)
    
    # Constellation Nodes (Rift Seeds)
    nodes = [
        (mcx - 110, mcy - 60, "S-01 [Nexus Alpha]", (0, 240, 255)),
        (mcx - 65, mcy - 85, "S-02 [Vórtice]", (180, 80, 255)),
        (mcx + 20, mcy - 100, "S-03 [Horizonte]", (255, 215, 80)),
        (mcx + 105, mcy - 40, "S-04 [Têmpora]", (80, 255, 140)),
        (mcx + 85, mcy + 45, "S-05 [Hiperespaço]", (0, 240, 255)),
        (mcx + 15, mcy + 95, "S-06 [Abismo]", (255, 80, 140)),
        (mcx - 70, mcy + 75, "S-07 [Cronos]", (255, 215, 80)),
        (mcx - 120, mcy + 20, "S-08 [Singular]", (80, 255, 140)),
    ]
    
    # Constellation Lines
    for i in range(len(nodes)):
        x0, y0, _, _ = nodes[i]
        x1, y1, _, _ = nodes[(i + 1) % len(nodes)]
        d.line([(x0, y0), (x1, y1)], fill=(120, 50, 180, 140), width=1)
    # Cross chords
    d.line([(nodes[0][0], nodes[0][1]), (nodes[4][0], nodes[4][1])], fill=(0, 240, 255, 80), width=1)
    d.line([(nodes[2][0], nodes[2][1]), (nodes[6][0], nodes[6][1])], fill=(255, 215, 80, 80), width=1)
    
    # Draw Nodes
    for nx, ny, nname, ncol in nodes:
        d.ellipse([nx - 5, ny - 5, nx + 5, ny + 5], fill=ncol + (255,), outline=(255, 255, 255, 255), width=2)
        d.ellipse([nx - 10, ny - 10, nx + 10, ny + 10], outline=ncol + (100,), width=1)
        if not clean:
            d.text((nx + 8, ny - 6), nname, fill=(255, 255, 255, 255), font=FONT_MICRO)

    # Lower Section: Dimensional Seed Catalog Table
    cat_y = map_y0 + map_h + 10
    cat_h = h - cat_y - 20
    d.rectangle([28, cat_y, w - 28, cat_y + cat_h], fill=(12, 6, 22, 240), outline=(75, 38, 120, 255), width=2)
    
    if not clean:
        d.text((38, cat_y + 8), "SEMENTES DO ATLAS · MELHOR RESSONÂNCIA E PROFUNDIDADE", fill=(255, 215, 80, 255), font=FONT_MICRO)
        th_y = cat_y + 24
        d.text((38, th_y), "SEMENTE", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((115, th_y), "BIOMA", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((250, th_y), "PROFUNDIDADE", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((350, th_y), "MELHOR R", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.line([(34, th_y + 12), (w - 34, th_y + 12)], fill=(60, 45, 85, 200), width=1)
        
        seeds_data = [
            # RiftCore.Biome; depth is the anchor count (Relic from 20, Void from 40)
            ("3F9A1C02", "Vazio", "40", "R 0,984", (80, 255, 140)),
            ("A07D55E1", "Relíquia de civilização", "22", "R 0,921", (80, 255, 140)),
            ("1B44C9F0", "Mundo-forja", "6", "R 0,847", (0, 240, 255)),
            ("7E02B3AA", "Oceano de mercúrio", "3", "R 0,612", (255, 215, 80)),
        ]
        row_gap = max(16, (cat_h - 44) // len(seeds_data))
        for r_idx, (sid, sdim, sdep, sres, scol) in enumerate(seeds_data):
            ry = th_y + 14 + r_idx * row_gap
            if ry + 12 < cat_y + cat_h:
                d.text((38, ry), sid, fill=(255, 255, 255, 255), font=FONT_MICRO)
                d.text((115, ry), sdim, fill=(255, 215, 80, 255), font=FONT_MICRO)
                d.text((250, ry), sdep, fill=(0, 240, 255, 255), font=FONT_MICRO)
                d.text((350, ry), sres, fill=scol + (255,), font=FONT_MICRO)
                
    return im

# ===========================================================================
# PREVIEWS & TAB OVERVIEW SHEET
# ===========================================================================
def compose_preview_rift(bg_img, active_tab_idx, title, palette_desc):
    canvas = Image.new('RGBA', (640, 480), (10, 8, 16, 255))
    d = ImageDraw.Draw(canvas)
    
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(75, 45, 105, 255), width=2)
    
    # Header with title
    d.rectangle([16, 12, 624, 40], fill=(24, 16, 36, 255), outline=(70, 45, 95, 255))
    d.text((24, 18), f"GTNA · PORTÃO DE FENDA DIMENSIONAL [UIV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 12, 28, 255), outline=(60, 40, 85, 255), width=2)
    
    d.text((panel_x + 10, panel_y + 12), "TELEMETRIA DE FENDA", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(65, 45, 90, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Estabilidade: 96,8 / 100", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Ressonância R: 0,924", fill=(255, 215, 80, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Profundidade: 9 / 12", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Acorde: 5 harmônicos", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['wormhole_vortex', 'harmonic_crystal', 'depth_anchor', 'dimension_atlas']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "RESSONÂNCIA (92%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_res_path = os.path.join(BAR_DIR, 'progressbar_resonance.png')
    if os.path.exists(pbar_res_path):
        pbar_r = Image.open(pbar_res_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_r, (panel_x + 10, panel_y + 160), pbar_r)
        
    d.text((panel_x + 10, panel_y + 180), "ESTABILIDADE (97%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_stab_path = os.path.join(BAR_DIR, 'progressbar_stability.png')
    if os.path.exists(pbar_stab_path):
        pbar_s = Image.open(pbar_stab_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_s, (panel_x + 10, panel_y + 196), pbar_s)
    
    d.text((panel_x + 10, panel_y + 220), "ESTADO: FENDA ABERTA", fill=(80, 255, 140, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "SpaceTime: 1,3 L/s", fill=(0, 240, 255, 255), font=FONT_TEXT)
    
    # Action buttons
    btn_n_path = os.path.join(BTN_DIR, 'btn_cosmic_normal.png')
    btn_p_path = os.path.join(BTN_DIR, 'btn_cosmic_pressed.png')
    if os.path.exists(btn_n_path):
        btn_n = Image.open(btn_n_path).resize((74, 28), Image.NEAREST)
        btn_p = Image.open(btn_p_path).resize((154, 32), Image.NEAREST)
        canvas.paste(btn_n, (panel_x + 10, panel_y + 266), btn_n)
        d.text((panel_x + 22, panel_y + 274), "FREQ −", fill=(255, 255, 255, 255), font=FONT_BTN)
        canvas.paste(btn_n, (panel_x + 90, panel_y + 266), btn_n)
        d.text((panel_x + 102, panel_y + 274), "FREQ +", fill=(255, 255, 255, 255), font=FONT_BTN)
        canvas.paste(btn_p, (panel_x + 10, panel_y + 306), btn_p)
        d.text((panel_x + 36, panel_y + 314), "[ FECHAR FENDA ]", fill=(255, 220, 100, 255), font=FONT_BTN)

    # Tab Bar on Bottom Left
    tab_labels = ["1. VÓRTICE & FENDA", "2. RODA DE ACORDES", "3. ATLAS CELESTIAL"]
    for i, tlab in enumerate(tab_labels):
        tx = 20 + i * 136
        ty = 390
        is_active = (i == active_tab_idx)
        btn_img = Image.open(btn_p_path if is_active else btn_n_path).resize((130, 26), Image.NEAREST)
        canvas.paste(btn_img, (tx, ty), btn_img)
        tcol = (255, 215, 80) if is_active else (180, 190, 210)
        d.text((tx + 6, ty + 6), tlab, fill=tcol + (255,), font=FONT_MICRO)

    d.text((16, 442), f"Aba Ativa: {title} · {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho Background: 512x512 · Fiel a RiftCore.java & OriginalsGui.atlas (controles: frequência/fase/amplitude ±, abrir/fechar)", fill=(100, 110, 130, 255), font=FONT_TEXT)
    return canvas

def main():
    print(">>> Gerando todas as 3 abas corrigidas para o Portão de Fenda Dimensional (UIV)...")
    
    # Load Tab 1 background
    bg_tab1_path = os.path.join(BG_DIR, 'bg_variation_1a_volumetric_512.png')
    bg_tab1 = Image.open(bg_tab1_path)
    
    print("  -> Gerando Aba 2: Roda de Acordes & Pauta Harmônica (512x512 & Clean - SEM PILONES)...")
    bg_tab2 = generate_bg_tab2_harmonic_score(512, 512, clean=False)
    bg_tab2.save(os.path.join(BG_DIR, 'bg_tab2_harmonic_score_512.png'))
    bg_tab2_clean = generate_bg_tab2_harmonic_score(512, 512, clean=True)
    bg_tab2_clean.save(os.path.join(BG_DIR, 'bg_tab2_harmonic_score_clean.png'))
    
    print("  -> Gerando Aba 3: Atlas de Sementes & Constelações (512x512 & Clean)...")
    bg_tab3 = generate_bg_tab3_constellation_atlas(512, 512, clean=False)
    bg_tab3.save(os.path.join(BG_DIR, 'bg_tab3_constellation_atlas_512.png'))
    bg_tab3_clean = generate_bg_tab3_constellation_atlas(512, 512, clean=True)
    bg_tab3_clean.save(os.path.join(BG_DIR, 'bg_tab3_constellation_atlas_clean.png'))
    
    print("  -> Montando Telas de Preview das 3 Abas...")
    prev_tab1 = compose_preview_rift(bg_tab1, 0, "Aba 1: Vórtice de Fenda", "Vórtice Volumétrico & Horizonte de Eventos")
    prev_tab1.save(os.path.join(PREV_DIR, 'preview_tab1_wormhole_vortex.png'))
    
    prev_tab2 = compose_preview_rift(bg_tab2, 1, "Aba 2: Roda de Acordes", "Roda de Acordes dos 8 Harmônicos & Pauta (OriginalsGui)")
    prev_tab2.save(os.path.join(PREV_DIR, 'preview_tab2_harmonic_score.png'))
    
    prev_tab3 = compose_preview_rift(bg_tab3, 2, "Aba 3: Atlas Celestial", "Cartografia de Constelações & Sementes de Fenda")
    prev_tab3.save(os.path.join(PREV_DIR, 'preview_tab3_constellation_atlas.png'))
    
    # Combined Tabs Overview Sheet
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 8, 18, 255))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, sheet.width, 60], fill=(24, 14, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 14), "GTNA · PORTÃO DE FENDA DIMENSIONAL [UIV] — VISÃO COMPLETA DAS 3 ABAS NAVEGÁVEIS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "Aba 1: Vórtice · Aba 2: Roda de Acordes (controles: frequência/fase/amplitude ±, abrir/fechar) · Aba 3: Atlas de Sementes (Backgrounds 512x512)", fill=(180, 190, 210, 255), font=FONT_SUB)
    sheet.paste(prev_tab1, (10, 75))
    sheet.paste(prev_tab2, (sw + 20, 75))
    sheet.paste(prev_tab3, (sw * 2 + 30, 75))
    sheet.save(os.path.join(OUT_DIR, 'tabs_overview.png'))
    print(f"[OK] Abas do Portão de Fenda geradas com sucesso em: {OUT_DIR}")

if __name__ == '__main__':
    main()
