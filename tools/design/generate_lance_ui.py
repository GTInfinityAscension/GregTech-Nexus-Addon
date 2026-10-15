#!/usr/bin/env python3
"""Generate UI assets for GTNA Multiblock 1: Lança Cinética Orbital (Orbital Kinetic Lance).

Outputs 3 visual variations:
  - Variation 1: "Cosmic Abyss / Deep Godforge" (Deep purple, nebula dithering, gold & cyan celestial accents)
  - Variation 2: "Tactical Railgun / High-Voltage HUD" (Dark cyan-slate, electric cyan vector lines, tech HUD)
  - Variation 3: "Kinetic Hazard / Relativistic Amber" (Dark gunmetal, thermal amber/crimson plasma, industrial warning)

Each variation includes:
  - 512x512 Backgrounds (and 640x360 wide versions)
  - 9-Sliceable Buttons (Normal, Hover, Pressed)
  - Status/Control Icons (32x32 and 64x64)
  - Progress Bars & Gauges
  - Complete Composed UI Mockups
  - A Unified Comparison Sheet
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'lance')
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
# Bayer Dithering Matrix 4x4
# ---------------------------------------------------------------------------
BAYER_4X4 = [
    [ 0/16,  8/16,  2/16, 10/16],
    [12/16,  4/16, 14/16,  6/16],
    [ 3/16, 11/16,  1/16,  9/16],
    [15/16,  7/16, 13/16,  5/16]
]

def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(len(c1)))

def dither_pixel(x, y, c1, c2, t):
    thresh = BAYER_4X4[y % 4][x % 4]
    return c2 if t > thresh else c1


# ===========================================================================
# 1. BACKGROUND GENERATORS (512x512)
# ===========================================================================

def generate_bg_variation_1_cosmic(w=512, h=512):
    """Variation 1: Cosmic Abyss / Deep Godforge."""
    im = Image.new('RGBA', (w, h), (11, 7, 22, 255))
    d = ImageDraw.Draw(im)
    
    # 1. Radial Nebula Glow with dithering
    cx, cy = int(w * 0.45), int(h * 0.48)
    max_r = int(math.hypot(w, h) * 0.65)
    nebula_dark = (11, 7, 22)
    nebula_mid = (45, 18, 70)
    nebula_hot = (95, 30, 115)
    nebula_core = (140, 50, 150)
    
    px = im.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dx, dy = (x - cx) / 1.1, (y - cy) * 1.2
            dist = math.hypot(dx, dy)
            t = max(0.0, 1.0 - dist / (max_r * 0.75))
            
            # Swirl turbulence
            angle = math.atan2(dy, dx)
            swirl = 0.15 * math.sin(angle * 3.0 + dist * 0.02)
            t = max(0.0, min(1.0, t + swirl))
            
            if t < 0.35:
                col = dither_pixel(x, y, nebula_dark, nebula_mid, t / 0.35)
            elif t < 0.7:
                col = dither_pixel(x, y, nebula_mid, nebula_hot, (t - 0.35) / 0.35)
            else:
                col = dither_pixel(x, y, nebula_hot, nebula_core, (t - 0.7) / 0.3)
            
            # Write 2x2 pixel blocks for crisp pixelart feel
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)

    # 2. Starfield with Bayer distribution
    random.seed(42)
    for _ in range(160):
        sx, sy = random.randint(4, w - 5), random.randint(4, h - 5)
        bright = random.random()
        if bright > 0.92:
            # Diamond cross star
            scol = (255, 235, 170, 240) if random.random() > 0.5 else (180, 240, 255, 240)
            d.point((sx, sy), fill=(255, 255, 255, 255))
            d.point((sx-1, sy), fill=scol); d.point((sx+1, sy), fill=scol)
            d.point((sx, sy-1), fill=scol); d.point((sx, sy+1), fill=scol)
        elif bright > 0.6:
            scol = (200, 210, 255, 200)
            d.point((sx, sy), fill=scol)
            d.point((sx+1, sy), fill=(scol[0], scol[1], scol[2], 120))
        else:
            d.point((sx, sy), fill=(160, 160, 200, 140))

    # 3. Godforge-style Celestial Vector Grid & Capacitor Orbit Ring
    grid_col = (100, 80, 160, 50)
    for gy in range(32, h, 32):
        d.line([(0, gy), (w, gy)], fill=grid_col, width=1)
    for gx in range(32, w, 32):
        d.line([(gx, 0), (gx, h)], fill=grid_col, width=1)
        
    # Concentric targeting / capacitor rings
    ring_col1 = (130, 210, 255, 80)
    ring_col2 = (220, 150, 255, 90)
    gold_notch = (255, 215, 80, 200)
    
    for r, col in [(90, ring_col1), (160, ring_col2), (220, ring_col1)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=2)
        # Cardinal notches
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            nx1 = cx + int((r - 6) * math.cos(rad))
            ny1 = cy + int((r - 6) * math.sin(rad))
            nx2 = cx + int((r + 6) * math.cos(rad))
            ny2 = cy + int((r + 6) * math.sin(rad))
            d.line([(nx1, ny1), (nx2, ny2)], fill=gold_notch, width=2)

    # Crosshair through center
    d.line([(cx - 40, cy), (cx - 10, cy)], fill=(255, 215, 80, 220), width=2)
    d.line([(cx + 10, cy), (cx + 40, cy)], fill=(255, 215, 80, 220), width=2)
    d.line([(cx, cy - 40), (cx, cy - 10)], fill=(255, 215, 80, 220), width=2)
    d.line([(cx, cy + 10), (cx, cy + 40)], fill=(255, 215, 80, 220), width=2)
    d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255, 255))
    
    # Border vignette
    for b in range(12):
        alpha = int(220 * (1.0 - b / 12))
        d.rectangle([b, b, w - 1 - b, h - 1 - b], outline=(5, 3, 10, alpha))
        
    return im


def generate_bg_variation_2_tactical(w=512, h=512):
    """Variation 2: Tactical Railgun / High-Voltage HUD."""
    im = Image.new('RGBA', (w, h), (7, 13, 20, 255))
    d = ImageDraw.Draw(im)
    
    # 1. Dark high-voltage cyan gradient & scanlines
    px = im.load()
    dark_cyan = (7, 13, 20)
    mid_cyan = (12, 32, 48)
    pulse_cyan = (18, 55, 78)
    
    cx, cy = int(w * 0.5), int(h * 0.5)
    max_d = math.hypot(cx, cy)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dist = math.hypot(x - cx, y - cy)
            t = max(0.0, 1.0 - dist / max_d)
            col = dither_pixel(x, y, dark_cyan, mid_cyan if t < 0.6 else pulse_cyan, t)
            # Scanline darkening
            if (y // 2) % 2 == 1:
                col = tuple(max(0, c - 4) for c in col)
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)
                        
    # 2. Millimeter Grid & Coordinate Markings
    grid_fine = (20, 60, 85, 55)
    grid_bold = (35, 110, 145, 90)
    for gy in range(16, h, 16):
        d.line([(0, gy), (w, gy)], fill=grid_bold if gy % 64 == 0 else grid_fine, width=1)
    for gx in range(16, w, 16):
        d.line([(gx, 0), (gx, h)], fill=grid_bold if gx % 64 == 0 else grid_fine, width=1)

    # 3. High-Voltage Railgun Barrel Vector (Orthographic top-down gun representation)
    rail_col = (0, 240, 255, 160)
    accel_glow = (180, 255, 255, 220)
    
    # Central acceleration axis (dashed line)
    for y in range(32, h - 32, 12):
        d.line([(cx, y), (cx, y + 6)], fill=(0, 240, 255, 180), width=2)
        
    # Rail pair
    d.line([(cx - 36, 40), (cx - 36, h - 40)], fill=rail_col, width=3)
    d.line([(cx + 36, 40), (cx + 36, h - 40)], fill=rail_col, width=3)
    
    # Coil stages (transverse pulses along the rails)
    for coil_y in range(70, h - 70, 48):
        d.rectangle([cx - 48, coil_y, cx - 36, coil_y + 12], outline=(0, 200, 240, 220), fill=(10, 40, 60, 180))
        d.rectangle([cx + 36, coil_y, cx + 48, coil_y + 12], outline=(0, 200, 240, 220), fill=(10, 40, 60, 180))
        d.line([(cx - 36, coil_y + 6), (cx + 36, coil_y + 6)], fill=(0, 255, 255, 70), width=1)
        
    # Tactical Reticle & Angular Sector
    d.ellipse([cx - 120, cy - 120, cx + 120, cy + 120], outline=(0, 220, 255, 120), width=2)
    d.arc([cx - 140, cy - 140, cx + 140, cy + 140], -45, 45, fill=(0, 255, 255, 200), width=3)
    d.arc([cx - 140, cy - 140, cx + 140, cy + 140], 135, 225, fill=(0, 255, 255, 200), width=3)
    
    # Corner HUD brackets
    bracket_col = (0, 240, 255, 220)
    for bx, by, sx, sy in [(20, 20, 1, 1), (w - 20, 20, -1, 1), (20, h - 20, 1, -1), (w - 20, h - 20, -1, -1)]:
        d.line([(bx, by), (bx + sx * 24, by)], fill=bracket_col, width=3)
        d.line([(bx, by), (bx, by + sy * 24)], fill=bracket_col, width=3)
        
    return im


def generate_bg_variation_3_kinetic(w=512, h=512):
    """Variation 3: Kinetic Hazard / Relativistic Amber."""
    im = Image.new('RGBA', (w, h), (18, 14, 16, 255))
    d = ImageDraw.Draw(im)
    
    # 1. Warm gunmetal & thermal glow
    px = im.load()
    dark_metal = (18, 14, 16)
    warm_metal = (42, 26, 24)
    plasma_amber = (90, 45, 20)
    core_hot = (150, 75, 25)
    
    cx, cy = int(w * 0.5), int(h * 0.5)
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dist = math.hypot(x - cx, (y - cy) * 1.1)
            t = max(0.0, 1.0 - dist / 280.0)
            if t < 0.4:
                col = dither_pixel(x, y, dark_metal, warm_metal, t / 0.4)
            elif t < 0.8:
                col = dither_pixel(x, y, warm_metal, plasma_amber, (t - 0.4) / 0.4)
            else:
                col = dither_pixel(x, y, plasma_amber, core_hot, (t - 0.8) / 0.2)
                
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)

    # 2. Heavy Industrial Hazard Crosshatch & Hexagonal Grid
    hex_col = (180, 100, 30, 45)
    r_hex = 28
    h_hex = int(r_hex * math.sqrt(3))
    for row in range(-1, h // h_hex + 2):
        for col in range(-1, w // (3 * r_hex) + 2):
            x_mid = col * 3 * r_hex + ((row % 2) * 1.5 * r_hex)
            y_mid = row * h_hex
            pts = []
            for a in range(0, 360, 60):
                rad = math.radians(a)
                pts.append((x_mid + r_hex * math.cos(rad), y_mid + r_hex * math.sin(rad)))
            d.polygon(pts, outline=hex_col)

    # 3. Kinetic Impact Blast Rings & Trajectory Vector
    hazard_amber = (255, 165, 0, 180)
    hazard_crimson = (255, 60, 40, 200)
    hazard_yellow = (255, 220, 50, 220)
    
    # Impact shockwave rings
    for r, col, wd in [(60, hazard_yellow, 2), (120, hazard_amber, 2), (190, hazard_crimson, 3), (250, (255, 100, 40, 80), 1)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=wd)
        
    # Segmented hazard perimeter ring (hazard stripes)
    n_seg = 32
    r_in, r_out = 205, 217
    for i in range(n_seg):
        if i % 2 == 0:
            a1, a2 = i * (360 / n_seg), (i + 1) * (360 / n_seg)
            d.arc([cx - r_out, cy - r_out, cx + r_out, cy + r_out], a1, a2, fill=hazard_amber, width=12)
            
    # Trajectory Arrow / Reticle
    d.line([(cx, cy - 80), (cx, cy + 80)], fill=hazard_yellow, width=2)
    d.line([(cx - 80, cy), (cx + 80, cy)], fill=hazard_yellow, width=2)
    d.polygon([(cx, cy - 14), (cx - 10, cy + 10), (cx, cy + 5), (cx + 10, cy + 10)], fill=(255, 255, 255, 240))
    
    return im


# ===========================================================================
# 2. BUTTONS (9-Sliceable, 32x16 & 64x32)
# ===========================================================================

def generate_button(theme, state='normal', w=64, h=32):
    """Generate 9-sliceable themed button."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    if theme == 'cosmic':
        # Godforge-inspired Cosmic Purple
        if state == 'normal':
            bg_top = (52, 28, 88)
            bg_bot = (32, 16, 56)
            border_outer = (85, 45, 140)
            border_inner = (130, 80, 205)
            glow_corner = (180, 130, 255)
        elif state == 'hover':
            bg_top = (75, 40, 120)
            bg_bot = (48, 25, 80)
            border_outer = (120, 70, 190)
            border_inner = (175, 120, 255)
            glow_corner = (220, 190, 255)
        else: # pressed
            bg_top = (22, 12, 40)
            bg_bot = (38, 20, 65)
            border_outer = (45, 25, 75)
            border_inner = (75, 45, 120)
            glow_corner = (110, 70, 170)
            
    elif theme == 'tactical':
        # High-Voltage Tactical Railgun
        if state == 'normal':
            bg_top = (22, 40, 55)
            bg_bot = (12, 24, 35)
            border_outer = (0, 150, 190)
            border_inner = (0, 210, 255)
            glow_corner = (160, 245, 255)
        elif state == 'hover':
            bg_top = (32, 60, 80)
            bg_bot = (18, 36, 52)
            border_outer = (0, 200, 240)
            border_inner = (80, 235, 255)
            glow_corner = (220, 255, 255)
        else: # pressed
            bg_top = (10, 20, 30)
            bg_bot = (18, 34, 48)
            border_outer = (0, 110, 140)
            border_inner = (0, 160, 200)
            glow_corner = (100, 210, 240)
            
    else: # kinetic
        # Industrial Amber / Relativistic Warning
        if state == 'normal':
            bg_top = (50, 32, 18)
            bg_bot = (30, 18, 10)
            border_outer = (180, 95, 20)
            border_inner = (245, 150, 30)
            glow_corner = (255, 215, 100)
        elif state == 'hover':
            bg_top = (75, 48, 25)
            bg_bot = (45, 28, 14)
            border_outer = (220, 125, 30)
            border_inner = (255, 185, 60)
            glow_corner = (255, 240, 160)
        else: # pressed
            bg_top = (22, 14, 8)
            bg_bot = (40, 25, 14)
            border_outer = (130, 65, 15)
            border_inner = (175, 95, 20)
            glow_corner = (210, 135, 50)
            
    # Draw beveled background
    for y in range(h):
        t = y / (h - 1)
        row_col = lerp_color(bg_top, bg_bot, t)
        d.line([(2, y), (w - 3, y)], fill=row_col + (255,))
        
    # Borders
    d.rectangle([1, 1, w - 2, h - 2], outline=border_outer + (255,))
    d.rectangle([2, 2, w - 3, h - 3], outline=border_inner + (255,))
    
    # Outer dark shadow
    d.rectangle([0, 0, w - 1, h - 1], outline=(10, 10, 14, 255))
    
    # Corner glowing notches (Godforge high-tech hallmark)
    d.point((2, 2), fill=glow_corner + (255,))
    d.point((w - 3, 2), fill=glow_corner + (255,))
    d.point((2, h - 3), fill=glow_corner + (255,))
    d.point((w - 3, h - 3), fill=glow_corner + (255,))
    
    return im


# ===========================================================================
# 3. STATUS & CONTROL ICONS (64x64, can downsample to 32x32)
# ===========================================================================

def generate_icon_crosshair(theme, size=64):
    """Orbital targeting reticle / crosshair."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    col_main = (140, 90, 255) if theme == 'cosmic' else ((0, 240, 255) if theme == 'tactical' else (255, 160, 20))
    col_accent = (255, 215, 80) if theme == 'cosmic' else ((200, 255, 255) if theme == 'tactical' else (255, 60, 40))
    
    # Outer circle & arcs
    d.ellipse([c - 24, c - 24, c + 24, c + 24], outline=col_main + (140,), width=2)
    d.arc([c - 28, c - 28, c + 28, c + 28], -30, 30, fill=col_accent + (255,), width=3)
    d.arc([c - 28, c - 28, c + 28, c + 28], 150, 210, fill=col_accent + (255,), width=3)
    
    # Cross lines with center gap
    d.line([(c - 20, c), (c - 6, c)], fill=col_main + (255,), width=2)
    d.line([(c + 6, c), (c + 20, c)], fill=col_main + (255,), width=2)
    d.line([(c, c - 20), (c, c - 6)], fill=col_main + (255,), width=2)
    d.line([(c, c + 6), (c, c + 20)], fill=col_main + (255,), width=2)
    
    # Diamond core
    d.polygon([(c, c - 3), (c - 3, c), (c, c + 3), (c + 3, c)], fill=col_accent + (255,))
    return im


def generate_icon_sabot(theme, size=64):
    """Kinetic hypervelocity sabot projectile with plasma shockwave."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    plasma_col = (180, 80, 255) if theme == 'cosmic' else ((0, 240, 255) if theme == 'tactical' else (255, 80, 20))
    metal_body = (220, 230, 245)
    metal_dark = (120, 130, 145)
    
    # Trailing plasma shockwave cone
    pts_shock = [(c, 8), (c - 16, 52), (c - 8, 48), (c, 56), (c + 8, 48), (c + 16, 52)]
    d.polygon(pts_shock, fill=plasma_col + (90,))
    
    # Sabot dart projectile
    pts_dart = [(c, 10), (c + 5, 24), (c + 4, 46), (c + 8, 50), (c - 8, 50), (c - 4, 46), (c - 5, 24)]
    d.polygon(pts_dart, fill=metal_body + (255,), outline=metal_dark + (255,))
    # Shading line
    d.line([(c, 10), (c, 48)], fill=(255, 255, 255, 220), width=1)
    
    # Kinetic energy rings around dart
    d.arc([c - 10, 22, c + 10, 32], 0, 180, fill=plasma_col + (240,), width=2)
    d.arc([c - 12, 34, c + 12, 44], 0, 180, fill=plasma_col + (240,), width=2)
    return im


def generate_icon_capacitor(theme, size=64):
    """Capacitor ring cell / high-energy storage bank."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    col_core = (160, 100, 255) if theme == 'cosmic' else ((0, 255, 240) if theme == 'tactical' else (255, 170, 30))
    casing = (70, 75, 88)
    
    # Outer octagonal cell
    pts_oct = []
    for a in range(22, 382, 45):
        rad = math.radians(a)
        pts_oct.append((c + 24 * math.cos(rad), c + 24 * math.sin(rad)))
    d.polygon(pts_oct, fill=casing + (255,), outline=(130, 140, 160, 255))
    
    # Glowing capacitor plate gap
    d.ellipse([c - 16, c - 16, c + 16, c + 16], fill=(15, 15, 22, 255), outline=col_core + (180,))
    # Energy arc inside
    d.line([(c - 10, c - 6), (c - 2, c), (c + 2, c - 4), (c + 10, c + 4)], fill=col_core + (255,), width=3)
    d.line([(c - 8, c + 6), (c - 1, c + 2), (c + 3, c + 6), (c + 8, c)], fill=(255, 255, 255, 240), width=1)
    return im


def generate_icon_thermal(theme, size=64):
    """Barrel temperature & cryogenic heat radiator."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    heat_col = (255, 70, 50)
    cold_col = (100, 210, 255)
    
    # Radiator fins on left, flame/plasma on right
    # Thermometer / gauge stem
    d.rounded_rectangle([c - 5, 12, c + 5, 42], radius=4, fill=(30, 35, 45, 255), outline=(100, 110, 130, 255))
    d.ellipse([c - 10, 38, c + 10, 54], fill=(30, 35, 45, 255), outline=(100, 110, 130, 255))
    
    # Mercury fill (glowing)
    d.rounded_rectangle([c - 2, 22, c + 2, 42], radius=2, fill=heat_col + (255,))
    d.ellipse([c - 7, 41, c + 7, 51], fill=heat_col + (255,))
    
    # Frost flakes / thermal radiation waves
    d.arc([c + 10, 18, c + 22, 30], -60, 60, fill=heat_col + (200,), width=2)
    d.arc([c + 14, 14, c + 28, 34], -60, 60, fill=(255, 180, 50, 180), width=2)
    d.arc([c - 22, 26, c - 10, 38], 120, 240, fill=cold_col + (200,), width=2)
    return im


def generate_icon_celestial_body(theme, size=64):
    """Target asteroid / planetary body with scan ring."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    # Asteroid craggy body
    pts_rock = [
        (c - 16, c - 12), (c - 8, c - 20), (c + 6, c - 18), (c + 18, c - 8),
        (c + 16, c + 12), (c + 4, c + 20), (c - 12, c + 18), (c - 20, c + 4)
    ]
    d.polygon(pts_rock, fill=(70, 65, 80, 255), outline=(120, 115, 135, 255))
    
    # Craters
    d.ellipse([c - 8, c - 10, c - 2, c - 4], outline=(40, 35, 50, 255), fill=(50, 45, 60, 255))
    d.ellipse([c + 2, c + 2, c + 10, c + 10], outline=(40, 35, 50, 255), fill=(50, 45, 60, 255))
    d.ellipse([c - 10, c + 6, c - 4, c + 12], outline=(40, 35, 50, 255), fill=(50, 45, 60, 255))
    
    # Scanning orbital ring around it
    scan_col = (130, 220, 255) if theme == 'tactical' else ((255, 215, 80) if theme == 'cosmic' else (255, 120, 40))
    d.ellipse([c - 26, c - 12, c + 26, c + 12], outline=scan_col + (190,), width=2)
    return im


def generate_icon_capsule(theme, size=64):
    """Recovery capsule with deceleration thruster / shield."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    col_flame = (255, 120, 30)
    # Capsule heat shield cone
    pts_cap = [(c, 14), (c + 14, 38), (c + 12, 44), (c - 12, 44), (c - 14, 38)]
    d.polygon(pts_cap, fill=(180, 190, 205, 255), outline=(100, 110, 125, 255))
    
    # Porthole / scanner
    d.ellipse([c - 4, 26, c + 4, 34], fill=(40, 120, 200, 255), outline=(200, 220, 255, 255))
    
    # Heatshield base
    d.rounded_rectangle([c - 15, 42, c + 15, 47], radius=2, fill=(60, 60, 65, 255), outline=(220, 120, 40, 255))
    
    # Retro thruster burn
    d.polygon([(c - 8, 48), (c, 60), (c + 8, 48)], fill=col_flame + (230,))
    d.polygon([(c - 4, 48), (c, 56), (c + 4, 48)], fill=(255, 255, 200, 255))
    return im


# ===========================================================================
# 4. PROGRESS BARS & GAUGES
# ===========================================================================

def generate_progressbar(theme, w=256, h=16, frac=0.72):
    """Progress bar with Godforge-style beveled frame and glowing plasma fill."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Background frame
    d.rectangle([0, 0, w - 1, h - 1], fill=(14, 14, 20, 255), outline=(45, 45, 60, 255))
    d.rectangle([1, 1, w - 2, h - 2], outline=(20, 20, 30, 255))
    
    fill_w = max(0, min(w - 4, int((w - 4) * frac)))
    if fill_w > 0:
        if theme == 'cosmic':
            c_left, c_right = (80, 30, 160), (220, 140, 255)
        elif theme == 'tactical':
            c_left, c_right = (0, 140, 180), (120, 255, 255)
        else:
            c_left, c_right = (180, 50, 10), (255, 210, 40)
            
        for x in range(fill_w):
            t = x / (w - 4)
            col = lerp_color(c_left, c_right, t)
            d.line([(2 + x, 2), (2 + x, h - 3)], fill=col + (255,))
            # Top highlight
            d.point((2 + x, 2), fill=(255, 255, 255, 180))
            
    # Milestones marks (Fragmentação, Fusão, Vaporização, Relativístico)
    for m in [0.25, 0.50, 0.75]:
        mx = 2 + int((w - 4) * m)
        d.line([(mx, 0), (mx, h - 1)], fill=(255, 215, 80, 240), width=1)
        
    return im


# ---------------------------------------------------------------------------
# Font Helper (JetBrainsMono or DejaVuSans for crisp UTF-8 text)
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


def compose_preview(theme_name, bg_img, title, palette_desc):
    """Compose full GUI mockup at 640x480 with panels, buttons, icons, and gauges."""
    canvas = Image.new('RGBA', (640, 480), (10, 10, 15, 255))
    d = ImageDraw.Draw(canvas)
    
    # 1. Background centered in main viewport
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    # Viewport border
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(70, 75, 95, 255), width=2)
    
    # 2. Side Control Panel (Right)
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 18, 26, 255), outline=(50, 55, 75, 255), width=2)
    
    # Title Header
    d.rectangle([16, 12, 624, 40], fill=(24, 24, 34, 255), outline=(60, 65, 85, 255))
    d.text((24, 18), f"GTNA · LANÇA CINÉTICA ORBITAL [UEV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel contents
    d.text((panel_x + 10, panel_y + 12), "TELEMETRIA DE MIRA", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(60, 65, 85, 255))
    
    # Target info
    d.text((panel_x + 10, panel_y + 34), "Alvo: Vesta (Asteroide)", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Distância: 170.000 Mm", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Dureza H: 3.5 MJ/kg", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Precisão A: 98.4%", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Icons row on side panel
    ico_body = generate_icon_celestial_body(theme_name, 36)
    ico_cross = generate_icon_crosshair(theme_name, 36)
    ico_dart = generate_icon_sabot(theme_name, 36)
    ico_cap = generate_icon_capacitor(theme_name, 36)
    
    canvas.paste(ico_body, (panel_x + 10, panel_y + 96), ico_body)
    canvas.paste(ico_cross, (panel_x + 50, panel_y + 96), ico_cross)
    canvas.paste(ico_dart, (panel_x + 90, panel_y + 96), ico_dart)
    canvas.paste(ico_cap, (panel_x + 130, panel_y + 96), ico_cap)
    
    # Progress bars in side panel
    d.text((panel_x + 10, panel_y + 144), "CARGA CAPACITOR (1e12 EU)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    bar_cap = generate_progressbar(theme_name, panel_w - 20, 12, 0.82)
    canvas.paste(bar_cap, (panel_x + 10, panel_y + 160), bar_cap)
    
    d.text((panel_x + 10, panel_y + 180), "CALOR DO CANO (64/80 K)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    bar_heat = generate_progressbar(theme_name, panel_w - 20, 12, 0.45)
    canvas.paste(bar_heat, (panel_x + 10, panel_y + 196), bar_heat)
    
    d.text((panel_x + 10, panel_y + 220), "REGIME: VAPORIZAÇÃO", fill=(255, 200, 60, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Velocidade: 3.742 km/s (0.0125c)", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Buttons
    btn_normal = generate_button(theme_name, 'normal', 74, 28)
    btn_hover = generate_button(theme_name, 'hover', 74, 28)
    btn_fire = generate_button(theme_name, 'pressed', 154, 32)
    
    canvas.paste(btn_normal, (panel_x + 10, panel_y + 266), btn_normal)
    d.text((panel_x + 24, panel_y + 274), "MIRAR", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_hover, (panel_x + 90, panel_y + 266), btn_hover)
    d.text((panel_x + 98, panel_y + 274), "AJUSTAR", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_fire, (panel_x + 10, panel_y + 306), btn_fire)
    d.text((panel_x + 36, panel_y + 314), "[ DISPARAR ]", fill=(255, 220, 100, 255), font=FONT_BTN)
    
    # Bottom capsule queue representation inside viewport
    d.rectangle([26, 380, 426, 420], fill=(12, 12, 18, 220), outline=(50, 55, 75, 200))
    d.text((36, 392), "FILA DE CÁPSULAS:", fill=(180, 190, 210, 255), font=FONT_PANEL)
    ico_capsule = generate_icon_capsule(theme_name, 28)
    for i, t_sec in enumerate([19, 34, 48]):
        bx = 170 + i * 85
        canvas.paste(ico_capsule, (bx, 386), ico_capsule)
        d.text((bx + 32, 392), f"#{i+1}: {t_sec}s", fill=(255, 255, 255, 255), font=FONT_TEXT)
        
    # Footer info
    d.text((16, 442), f"Estilo: {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho do Background: 512x512 (ou Wide 640x360) · 9-Slice & Pixel Art", fill=(100, 110, 130, 255), font=FONT_TEXT)
    
    return canvas



# ===========================================================================
# 6. UNIFIED COMPARISON OVERVIEW
# ===========================================================================

def generate_comparison_sheet(p1, p2, p3):
    """Combine the 3 previews into a single side-by-side comparison sheet."""
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    
    # Header banner
    d.rectangle([0, 0, sheet.width, 60], fill=(20, 20, 30, 255), outline=(50, 55, 75, 255))
    d.text((30, 14), "GTNA · COMPARATIVO DE DESIGN DE UI — MULTIBLOCO 1: LANÇA CINÉTICA ORBITAL", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "3 Variações de Estilo Visual (Backgrounds 512x512, Botões 9-Slice, Ícones de Status e Barras de Energia)", fill=(180, 190, 210, 255), font=FONT_SUB)

    
    # Paste the 3 previews
    sheet.paste(p1, (10, 75))
    sheet.paste(p2, (sw + 20, 75))
    sheet.paste(p3, (sw * 2 + 30, 75))
    
    return sheet


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def main():
    print(">>> Gerando Variações de UI para a Lança Cinética Orbital...")
    
    # 1. Backgrounds
    print("  -> Gerando Backgrounds (512x512)...")
    bg1 = generate_bg_variation_1_cosmic(512, 512)
    bg1.save(os.path.join(BG_DIR, 'bg_variation_1_cosmic_512.png'))
    
    bg2 = generate_bg_variation_2_tactical(512, 512)
    bg2.save(os.path.join(BG_DIR, 'bg_variation_2_tactical_512.png'))
    
    bg3 = generate_bg_variation_3_kinetic(512, 512)
    bg3.save(os.path.join(BG_DIR, 'bg_variation_3_kinetic_512.png'))

    # Wide versions (640x360)
    generate_bg_variation_1_cosmic(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1_cosmic_wide.png'))
    generate_bg_variation_2_tactical(640, 360).save(os.path.join(BG_DIR, 'bg_variation_2_tactical_wide.png'))
    generate_bg_variation_3_kinetic(640, 360).save(os.path.join(BG_DIR, 'bg_variation_3_kinetic_wide.png'))

    # 2. Buttons
    print("  -> Gerando Botões 9-Slice...")
    for theme in ['cosmic', 'tactical', 'kinetic']:
        for state in ['normal', 'hover', 'pressed']:
            btn = generate_button(theme, state, 64, 32)
            btn.save(os.path.join(BTN_DIR, f'btn_{theme}_{state}.png'))

    # 3. Icons
    print("  -> Gerando Ícones de Controle e Telemetria...")
    icon_generators = [
        ('orbital_crosshair', generate_icon_crosshair),
        ('kinetic_sabot', generate_icon_sabot),
        ('capacitor_bank', generate_icon_capacitor),
        ('barrel_thermal', generate_icon_thermal),
        ('celestial_body', generate_icon_celestial_body),
        ('return_capsule', generate_icon_capsule)
    ]
    for theme in ['cosmic', 'tactical', 'kinetic']:
        for name, gen_fn in icon_generators:
            ico64 = gen_fn(theme, 64)
            ico64.save(os.path.join(ICO_DIR, f'ico_{name}_{theme}_64.png'))
            ico32 = ico64.resize((32, 32), Image.NEAREST)
            ico32.save(os.path.join(ICO_DIR, f'ico_{name}_{theme}_32.png'))

    # 4. Progress Bars
    print("  -> Gerando Barras de Energia e Calor...")
    for theme in ['cosmic', 'tactical', 'kinetic']:
        pbar = generate_progressbar(theme, 256, 16, 0.75)
        pbar.save(os.path.join(BAR_DIR, f'progressbar_{theme}.png'))

    # 5. Full Composed Previews
    print("  -> Montando Telas Completas de Preview...")
    prev1 = compose_preview('cosmic', bg1, "Variação 1: Abismo Cósmico (Godforge Style)", "Púrpura Profundo, Nebulosa Dithered, Acentos Dourados & Ciano")
    prev1.save(os.path.join(PREV_DIR, 'preview_variation_1_cosmic.png'))
    
    prev2 = compose_preview('tactical', bg2, "Variação 2: Railgun Tático de Alta Voltagem", "Aço Escuro, Vetores HUD Ciano-Elétrico, Bobinas Lineares")
    prev2.save(os.path.join(PREV_DIR, 'preview_variation_2_tactical.png'))
    
    prev3 = compose_preview('kinetic', bg3, "Variação 3: Alerta Cinético & Âmbar Relativístico", "Gunmetal, Grade Hexagonal, Plasma Térmico Âmbar e Carmesim")
    prev3.save(os.path.join(PREV_DIR, 'preview_variation_3_kinetic.png'))

    # 6. Combined Comparison Sheet
    print("  -> Gerando Prancha Comparativa Unificada...")
    sheet = generate_comparison_sheet(prev1, prev2, prev3)
    sheet.save(os.path.join(OUT_DIR, 'comparison_overview.png'))
    
    print("\n[OK] Todos os assets foram gerados com sucesso em:")
    print(f"     {OUT_DIR}")

if __name__ == '__main__':
    main()
