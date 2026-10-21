#!/usr/bin/env python3
"""Generate all 3 tabs for GTNA Multiblock 4: Câmara de Contenção Estelar (Stellar Containment Chamber - MAX Tier):
  - Tab 1: Estrela de Nêutrons & Ergosfera (Neutron Star / Pulsar in normal state, with Kerr Black Hole post-collapse)
  - Tab 2: Diagrama Massa–Período (M-P Plane, TOV Limit 2.2 M☉ & Keplerian Breakup Curve matching OriginalsGui.massPeriod)
  - Tab 3: Sismograma dos Tremores da Crosta & Ejeção Degenerada (Starquake Glitch Detector matching OriginalsGui.quakes)

Buttons match StellarChamberMachine.java:
  - [-] (sp_sub) and [+] (sp_add) for setpoint adjustment (EU/t = 2^setpoint)
  - [CAMPO MAGNETAR: ATIVO / INATIVO] (magnetar)
  - NO "Disco ON" button.

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

# ===========================================================================
# TAB 1: ESTRELA DE NÊUTRONS / PULSAR (NORMAL STATE)
# ===========================================================================
def generate_bg_tab1_neutron_star(w=512, h=512, clean=False):
    """Incandescent Neutron Star / Pulsar (Normal State) with relativistic polar jets,
    magnetic dipole field loops, and 4 concentric containment bands."""
    cx, cy = w // 2, int(h * 0.44)
    
    n_base = generate_fbm_noise(w, h, octaves=7, persistence=0.55, seed=1001)
    n_corona = generate_fbm_noise(w, h, octaves=5, persistence=0.62, seed=1002)
    
    y, x = np.ogrid[:h, :w]
    dx = (x - cx).astype(np.float32)
    dy = (y - cy).astype(np.float32)
    r = np.sqrt(dx * dx + dy * dy)
    r_norm = r / (w * 0.5)
    theta = np.arctan2(dy, dx)
    
    # Blinding Stellar Core & Plasma Coronal Flames
    core_glow = np.exp(-(r / 36.0) ** 2) * 1.7
    
    # Magnetic Dipole Coronal Loops
    dipole_loops = np.abs(np.sin(theta)) ** 2 * np.exp(-r_norm * 2.0)
    
    # Polar Relativistic Jets (|dx| < 22)
    jet_width = np.abs(dx) / 22.0
    polar_jets = np.exp(-jet_width * jet_width) * np.exp(-np.abs(dy) / 240.0) * 1.3
    
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
    
    # Stars in background
    rng = np.random.default_rng(2026)
    for _ in range(240):
        sx = rng.integers(10, w - 10)
        sy = rng.integers(10, h - 10)
        if math.hypot(sx - cx, sy - cy) < 45: continue
        bright = rng.uniform(0.2, 1.0)
        if bright > 0.94:
            scol = (255, 240, 180, 240) if rng.random() > 0.5 else (160, 240, 255, 240)
            d.line([(sx - 4, sy), (sx + 4, sy)], fill=scol, width=1)
            d.line([(sx, sy - 4), (sx, sy + 4)], fill=scol, width=1)
            d.point((sx, sy), fill=(255, 255, 255, 255))
        else:
            d.point((sx, sy), fill=(160, 180, 230, int(180 * bright)))
            
    # 4 Concentric Neutronium Containment Bands
    band_radii = [60, 92, 124, 156]
    for b_idx, r_b in enumerate(band_radii):
        col_b = (255, 215, 80, 220) if b_idx == 3 else (160, 90, 240, 150)
        d.ellipse([cx - r_b, cy - r_b, cx + r_b, cy + r_b], outline=col_b, width=2)
        # Degree ticks
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            t_len = 5 if deg % 45 == 0 else 3
            x0 = cx + int(math.cos(rad) * (r_b - t_len))
            y0 = cy + int(math.sin(rad) * (r_b - t_len))
            x1 = cx + int(math.cos(rad) * (r_b + t_len))
            y1 = cy + int(math.sin(rad) * (r_b + t_len))
            d.line([(x0, y0), (x1, y1)], fill=col_b, width=1)
            
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "CÂMARA DE CONTENÇÃO ESTELAR · ESTADO NORMAL (PULSAR DE MILISSEGUNDO)", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 200, 26), "COLAPSO TOV: SE M > 2.20 M☉", fill=(255, 215, 80, 240), font=FONT_MICRO)
        
        # Bottom Telemetry Bar
        d.rectangle([28, h - 55, w - 28, h - 25], fill=(14, 8, 24, 230), outline=(75, 45, 105, 255))
        d.text((36, h - 48), "MASSA: 1.200 M☉ · PERÍODO: 33.0 ms · CAMPO MAGNETAR: ATIVO · BANDAS: 4/4 (100% CAMPO)", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((36, h - 36), "EXTRAÇÃO INDUZIDA: 2^50 EU/t (1.13e15 EU/t) · MATÉRIA DEGENERADA ESTÁVEL", fill=(0, 240, 255, 240), font=FONT_MICRO)
        
    return im

# ===========================================================================
# TAB 2: DIAGRAMA MASSA–PERÍODO (M-P PLANE & TOV BOUNDARY)
# ===========================================================================
def generate_bg_tab2_mass_period(w=512, h=512, clean=False):
    """Astrophysical Mass vs Rotation Period plane matching OriginalsGui.massPeriod:
    - log period 0.5 ms .. 1 s on X axis
    - mass 1.0 .. 2.6 M☉ on Y axis
    - TOV limit horizontal red line at 2.2 M☉
    - Kepler break-up golden curve: p = 7e-4 * sqrt(1.4 / mm)
    - Cyan trail and state dot."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=4202)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.35, (22, 10, 42)),
        (0.65, (52, 18, 86)),
        (0.85, (0, 210, 245)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "DIAGRAMA EVOLUTIVO MASSA–PERÍODO (PLANO M–P)", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 200, 26), "LIMITE TOV: 2.20 M☉ (COLAPSO EM BH)", fill=(255, 80, 80, 240), font=FONT_MICRO)

    # Main Graph Box
    gx0, gy0, gx1, gy1 = 45, 52, w - 35, h - 65
    gw, gh = gx1 - gx0, gy1 - gy0
    d.rectangle([gx0, gy0, gx1, gy1], fill=(12, 6, 22, 235), outline=(75, 45, 105, 255), width=2)
    
    # Grid lines for Mass: 1.0 to 2.6 M☉
    for mm_int in range(10, 27, 2):
        mm = mm_int / 10.0
        yy = gy1 - int((mm - 1.0) / 1.6 * gh)
        d.line([(gx0, yy), (gx1, yy)], fill=(45, 30, 65, 160), width=1)
        if not clean:
            d.text((gx0 - 24, yy - 5), f"{mm:.1f}", fill=(160, 170, 190, 200), font=FONT_MICRO)
            
    # TOV Collapse Boundary Line (Red Horizontal at M = 2.2 M☉)
    tov_y = gy1 - int((2.20 - 1.0) / 1.6 * gh)
    d.line([(gx0, tov_y), (gx1, tov_y)], fill=(255, 70, 70, 255), width=2)
    if not clean:
        d.text((gx1 - 75, tov_y - 12), "LIMITE TOV [2.2 M☉]", fill=(255, 80, 80, 255), font=FONT_MICRO)
        d.rectangle([gx0, gy0, gx1, tov_y], fill=(255, 40, 40, 20)) # Warning zone above TOV
        
    # Keplerian Centrifugal Breakup Curve: p = 7e-4 * sqrt(1.4 / mm)
    lo = math.log10(5e-4) # 0.5 ms
    hi = 0.0              # 1.0 s
    kepler_pts = []
    for px in range(gx0, gx1, 2):
        rel_x = (px - gx0) / float(gw)
        log_p = lo + rel_x * (hi - lo)
        p = 10 ** log_p
        # from p = 7e-4 * sqrt(1.4 / mm) => mm = 1.4 * (7e-4 / p)^2
        # or parameterize mm from 1.0 to 2.6:
        pass
    
    # Accurate Kepler curve from mm = 1.0 to 2.6
    kepler_pts = []
    for mm_step in np.linspace(1.0, 2.6, 120):
        p = 7e-4 * math.sqrt(1.4 / mm_step)
        if p >= 5e-4 and p <= 1.0:
            log_p = math.log10(p)
            xx = gx0 + int((log_p - lo) / (hi - lo) * gw)
            yy = gy1 - int((mm_step - 1.0) / 1.6 * gh)
            kepler_pts.append((xx, yy))
            
    for i in range(len(kepler_pts) - 1):
        d.line([kepler_pts[i], kepler_pts[i + 1]], fill=(255, 215, 80, 240), width=2)
        
    if not clean:
        d.text((gx0 + 10, gy1 - 25), "RUPTURA KEPLERIANA (LIMITE CENTRÍFUGO)", fill=(255, 215, 80, 220), font=FONT_MICRO)
        
        # Historical Trail of Star Evolution (Cyan Dots)
        trail_pts = [
            (1.15, 0.040), (1.16, 0.038), (1.18, 0.036), (1.19, 0.034), (1.20, 0.033)
        ]
        for t_idx, (tm, tp) in enumerate(trail_pts):
            log_p = math.log10(tp)
            tx = gx0 + int((log_p - lo) / (hi - lo) * gw)
            ty = gy1 - int((tm - 1.0) / 1.6 * gh)
            alpha = int(80 + 170 * (t_idx / len(trail_pts)))
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(0, 240, 255, alpha))
            
        # Current Operating State Dot (Cyan / Gold Pulsar)
        curr_m, curr_p = 1.20, 0.033
        curr_x = gx0 + int((math.log10(curr_p) - lo) / (hi - lo) * gw)
        curr_y = gy1 - int((curr_m - 1.0) / 1.6 * gh)
        d.ellipse([curr_x - 5, curr_y - 5, curr_x + 5, curr_y + 5], fill=(255, 255, 255, 255), outline=(0, 240, 255, 255), width=2)
        d.text((curr_x + 8, curr_y - 6), "ESTADO ATUAL (1.20 M☉, 33 ms)", fill=(0, 240, 255, 255), font=FONT_MICRO)
        
        # Axis Labels
        d.text((gx0, gy0 - 12), "M (Massas Solares M☉)", fill=(160, 170, 190, 255), font=FONT_MICRO)
        d.text((gx1 - 70, gy1 + 6), "P (Período em s)", fill=(160, 170, 190, 255), font=FONT_MICRO)
        
    return im

# ===========================================================================
# TAB 3: SISMOGRAMA DOS TREMORES DA CROSTA (STARQUAKE GLITCH SEISMOGRAPH)
# ===========================================================================
def generate_bg_tab3_crust_seismograph(w=512, h=512, clean=False):
    """Starquake seismogram & degenerate matter ejection history matching OriginalsGui.quakes."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=4303)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 3, 14)),
        (0.35, (22, 10, 42)),
        (0.65, (52, 18, 86)),
        (0.85, (0, 210, 245)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "SISMOGRAMA DA CROSTA ESTELAR & MATÉRIA DEGENERADA", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 180, 26), "SONDA SÍSMICA: ACOPLADA [OK]", fill=(80, 255, 140, 240), font=FONT_MICRO)

    # Upper Half: Seismograph Waveform Scope
    seis_y0 = 48
    seis_h = 200
    seis_x0 = 28
    seis_x1 = w - 28
    seis_w = seis_x1 - seis_x0
    d.rectangle([seis_x0, seis_y0, seis_x1, seis_y0 + seis_h], fill=(12, 6, 22, 230), outline=(75, 40, 115, 255), width=2)
    
    # Grid lines
    mid_y = seis_y0 + seis_h // 2
    for k in range(1, 5):
        gy = seis_y0 + k * (seis_h // 5)
        d.line([(seis_x0, gy), (seis_x1, gy)], fill=(45, 30, 65, 150), width=1)
    d.line([(seis_x0, mid_y), (seis_x1, mid_y)], fill=(80, 50, 120, 200), width=1)
    
    # Dynamic Seismogram Waveform with Starquake Glitch Spikes
    glitch_1_x = seis_x0 + int(seis_w * 0.35)
    glitch_2_x = seis_x0 + int(seis_w * 0.72)
    
    wave_pts = []
    for px in range(seis_x0 + 2, seis_x1 - 2):
        rel_x = px - seis_x0
        jitter = math.sin(rel_x * 0.12) * 4 + math.sin(rel_x * 0.45) * 2 + math.sin(rel_x * 1.8) * 1.5
        
        dist1 = abs(px - glitch_1_x)
        spike1 = math.exp(-dist1 / 7.0) * math.sin(dist1 * 0.7) * 45 if dist1 < 35 else 0.0
        
        dist2 = abs(px - glitch_2_x)
        spike2 = math.exp(-dist2 / 10.0) * math.sin(dist2 * 0.5) * 65 if dist2 < 45 else 0.0
        
        wy = int(mid_y + jitter - spike1 - spike2)
        wy = max(seis_y0 + 4, min(seis_y0 + seis_h - 4, wy))
        wave_pts.append((px, wy))
        
    for i in range(len(wave_pts) - 1):
        d.line([wave_pts[i], wave_pts[i + 1]], fill=(80, 255, 140, 240), width=2)
        
    if not clean:
        d.text((glitch_1_x - 30, seis_y0 + 15), "★ GLITCH #41 [TREMOR VORTEX]", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.line([(glitch_1_x, seis_y0 + 26), (glitch_1_x, mid_y - 25)], fill=(255, 215, 80, 160), width=1)
        
        d.text((glitch_2_x - 30, seis_y0 + 15), "★ GLITCH #42 [FRATURA CROSTA]", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.line([(glitch_2_x, seis_y0 + 26), (glitch_2_x, mid_y - 45)], fill=(255, 215, 80, 160), width=1)

    # Lower Section: Degenerate Matter Ejection Collector Table
    box_y = seis_y0 + seis_h + 12
    box_h = h - box_y - 20
    d.rectangle([24, box_y, w - 24, box_y + box_h], fill=(12, 8, 22, 240), outline=(75, 40, 115, 255), width=2)
    
    if not clean:
        d.text((36, box_y + 8), "HISTÓRICO DE TREMORES E COLETA DE MATÉRIA DEGENERADA (ME EJECTION BUS)", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
        th_y = box_y + 24
        d.text((36, th_y), "EVENTO", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((95, th_y), "TIPO DE TREMOR", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((250, th_y), "ENERGIA DO TREMOR", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((365, th_y), "MATÉRIA DEGENERADA", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.line([(34, th_y + 12), (w - 34, th_y + 12)], fill=(60, 45, 85, 200), width=1)
        
        events = [
            ("GLITCH #42", "Desprendimento de Vórtices", "3.2e15 EU (Absorvido)", "1.400 kg [COLETADO]", (80, 255, 140)),
            ("GLITCH #41", "Fratura da Crosta Estelar", "1.5e15 EU (Absorvido)", "650 kg [COLETADO]", (80, 255, 140)),
            ("GLITCH #40", "Tremor Gigante (Vela-type)", "6.8e15 EU (Absorvido)", "3.100 kg [COLETADO]", (255, 215, 80)),
            ("GLITCH #39", "Micro-ajuste Rotacional", "1.1e15 EU (Absorvido)", "420 kg [COLETADO]", (80, 255, 140)),
        ]
        row_gap = max(18, (box_h - 44) // len(events))
        for r_idx, (eid, eomega, enrg, emat, ecol) in enumerate(events):
            ry = th_y + 14 + r_idx * row_gap
            if ry + 12 < box_y + box_h:
                d.text((36, ry), eid, fill=(255, 255, 255, 255), font=FONT_MICRO)
                d.text((95, ry), eomega, fill=(255, 215, 80, 255), font=FONT_MICRO)
                d.text((250, ry), enrg, fill=(0, 240, 255, 255), font=FONT_MICRO)
                d.text((365, ry), emat, fill=ecol + (255,), font=FONT_MICRO)
                
    return im

# ===========================================================================
# PREVIEWS & TAB OVERVIEW SHEET
# ===========================================================================
def compose_preview_stellar(bg_img, active_tab_idx, title, palette_desc):
    canvas = Image.new('RGBA', (640, 480), (10, 8, 16, 255))
    d = ImageDraw.Draw(canvas)
    
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(75, 45, 105, 255), width=2)
    
    # Header with title
    d.rectangle([16, 12, 624, 40], fill=(24, 16, 36, 255), outline=(70, 45, 95, 255))
    d.text((24, 18), f"GTNA · CÂMARA DE CONTENÇÃO ESTELAR [MAX] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 12, 28, 255), outline=(60, 40, 85, 255), width=2)
    
    d.text((panel_x + 10, panel_y + 12), "TELEMETRIA ESTELAR", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(65, 45, 90, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Massa: 1.200 M☉ (TOV: 2.2)", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Período: 33.0 ms (30.3 Hz)", fill=(255, 215, 80, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Ruptura (Kepler): 0,654 ms", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Bandas: tier 1 / 4", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['neutron_star', 'ergosphere_penrose', 'containment_band', 'stellar_seismogram']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "ENERGIA ROTACIONAL (88%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_rot_path = os.path.join(BAR_DIR, 'progressbar_rotational_energy.png')
    if os.path.exists(pbar_rot_path):
        pbar_r = Image.open(pbar_rot_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_r, (panel_x + 10, panel_y + 160), pbar_r)
        
    d.text((panel_x + 10, panel_y + 180), "TENSÃO DA CROSTA σ (42%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_str_path = os.path.join(BAR_DIR, 'progressbar_crust_stress.png')
    if os.path.exists(pbar_str_path):
        pbar_s = Image.open(pbar_str_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_s, (panel_x + 10, panel_y + 196), pbar_s)
    
    d.text((panel_x + 10, panel_y + 220), "ESTADO: ESTRELA NÊUTRONS", fill=(80, 255, 140, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Saída: 2^50 (1.13e15 EU/t)", fill=(0, 240, 255, 255), font=FONT_TEXT)
    
    # Action buttons matching StellarChamberMachine.java:
    # Setpoint adjustments: [-] and [+]
    # Magnetar Toggle: [CAMPO MAGNETAR: ATIVO]
    btn_n_path = os.path.join(BTN_DIR, 'btn_cosmic_normal.png')
    btn_p_path = os.path.join(BTN_DIR, 'btn_cosmic_pressed.png')
    if os.path.exists(btn_n_path):
        btn_n = Image.open(btn_n_path)
        btn_p = Image.open(btn_p_path)
        
        # Setpoint row
        d.text((panel_x + 10, panel_y + 258), "SETPOINT: 50", fill=(255, 215, 80, 255), font=FONT_PANEL)
        btn_sub = btn_n.resize((34, 24), Image.NEAREST)
        btn_add = btn_n.resize((34, 24), Image.NEAREST)
        canvas.paste(btn_sub, (panel_x + 95, panel_y + 255), btn_sub)
        d.text((panel_x + 107, panel_y + 261), "[-]", fill=(255, 100, 100, 255), font=FONT_BTN)
        canvas.paste(btn_add, (panel_x + 135, panel_y + 255), btn_add)
        d.text((panel_x + 147, panel_y + 261), "[+]", fill=(80, 255, 140, 255), font=FONT_BTN)
        
        # Magnetar toggle button
        btn_mag = btn_p.resize((154, 30), Image.NEAREST)
        canvas.paste(btn_mag, (panel_x + 10, panel_y + 292), btn_mag)
        d.text((panel_x + 18, panel_y + 300), "[MAGNETAR: ATIVO]", fill=(255, 220, 100, 255), font=FONT_BTN)
        
        # Ingestion indicator
        d.text((panel_x + 10, panel_y + 332), "Mass Injector: 1 · Input Hatch: 2", fill=(160, 170, 190, 255), font=FONT_MICRO)
        d.text((panel_x + 10, panel_y + 346), "Sonda Sísmica: Acoplada [OK]", fill=(80, 255, 140, 255), font=FONT_MICRO)

    # Tab Bar on Bottom Left
    tab_labels = ["1. ESTRELA NÊUTRONS", "2. DIAGRAMA M-P", "3. SISMOGRAMA"]
    for i, tlab in enumerate(tab_labels):
        tx = 20 + i * 136
        ty = 390
        is_active = (i == active_tab_idx)
        btn_img = Image.open(btn_p_path if is_active else btn_n_path).resize((130, 26), Image.NEAREST)
        canvas.paste(btn_img, (tx, ty), btn_img)
        tcol = (255, 215, 80) if is_active else (180, 190, 210)
        d.text((tx + 6, ty + 6), tlab, fill=tcol + (255,), font=FONT_MICRO)

    d.text((16, 442), f"Aba Ativa: {title} · {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho Background: 512x512 · Fiel a StellarChamberMachine.java & OriginalsGui.java", fill=(100, 110, 130, 255), font=FONT_TEXT)
    return canvas

def main():
    print(">>> Gerando todas as 3 abas corrigidas para a Câmara de Contenção Estelar (MAX)...")
    
    print("  -> Gerando Aba 1: Estrela de Nêutrons / Pulsar (Estado Normal 512x512 & Clean)...")
    bg_tab1 = generate_bg_tab1_neutron_star(512, 512, clean=False)
    bg_tab1.save(os.path.join(BG_DIR, 'bg_tab1_neutron_star_512.png'))
    bg_tab1_clean = generate_bg_tab1_neutron_star(512, 512, clean=True)
    bg_tab1_clean.save(os.path.join(BG_DIR, 'bg_tab1_neutron_star_clean.png'))
    
    print("  -> Gerando Aba 2: Diagrama Massa–Período M–P (512x512 & Clean)...")
    bg_tab2 = generate_bg_tab2_mass_period(512, 512, clean=False)
    bg_tab2.save(os.path.join(BG_DIR, 'bg_tab2_mass_period_512.png'))
    bg_tab2_clean = generate_bg_tab2_mass_period(512, 512, clean=True)
    bg_tab2_clean.save(os.path.join(BG_DIR, 'bg_tab2_mass_period_clean.png'))
    
    print("  -> Gerando Aba 3: Sismograma dos Tremores da Crosta (512x512 & Clean)...")
    bg_tab3 = generate_bg_tab3_crust_seismograph(512, 512, clean=False)
    bg_tab3.save(os.path.join(BG_DIR, 'bg_tab3_crust_seismograph_512.png'))
    bg_tab3_clean = generate_bg_tab3_crust_seismograph(512, 512, clean=True)
    bg_tab3_clean.save(os.path.join(BG_DIR, 'bg_tab3_crust_seismograph_clean.png'))
    
    print("  -> Montando Telas de Preview das 3 Abas...")
    prev_tab1 = compose_preview_stellar(bg_tab1, 0, "Aba 1: Estrela Nêutrons", "Pulsar de Milissegundo (Normal) · Colapso TOV se M > 2.2 M☉")
    prev_tab1.save(os.path.join(PREV_DIR, 'preview_tab1_neutron_star.png'))
    
    prev_tab2 = compose_preview_stellar(bg_tab2, 1, "Aba 2: Diagrama M–P", "Plano Massa-Período, Limite TOV & Ruptura Centrífuga")
    prev_tab2.save(os.path.join(PREV_DIR, 'preview_tab2_mass_period.png'))
    
    prev_tab3 = compose_preview_stellar(bg_tab3, 2, "Aba 3: Sismograma", "Sismógrafo de Tremores, Glitches & Matéria Degenerada")
    prev_tab3.save(os.path.join(PREV_DIR, 'preview_tab3_crust_seismograph.png'))
    
    # Combined Tabs Overview Sheet
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 8, 18, 255))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, sheet.width, 60], fill=(24, 14, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 14), "GTNA · CÂMARA DE CONTENÇÃO ESTELAR [MAX] — VISÃO COMPLETA DAS 3 ABAS NAVEGÁVEIS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "Aba 1: Estrela Nêutrons (Normal) · Aba 2: Diagrama M-P · Aba 3: Sismograma (Botões [-], [+], [MAGNETAR])", fill=(180, 190, 210, 255), font=FONT_SUB)
    sheet.paste(prev_tab1, (10, 75))
    sheet.paste(prev_tab2, (sw + 20, 75))
    sheet.paste(prev_tab3, (sw * 2 + 30, 75))
    sheet.save(os.path.join(OUT_DIR, 'tabs_overview.png'))
    print(f"[OK] Abas da Câmara Estelar geradas com sucesso em: {OUT_DIR}")

if __name__ == '__main__':
    main()
