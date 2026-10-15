#!/usr/bin/env python3
"""Generate UI assets for GTNA Multiblock 2: Portão de Fenda Dimensional (Dimensional Rift Gate).

Outputs 3 visual variations:
  - Variation 1: "Vórtice Cósmico & Ondas Harmônicas" (Godforge Cosmic Purple, Harmonic Sine Waves & 8-Pylon Ring)
  - Variation 2: "Atlas de Constelações & Fenda Eterial" (Astrometric Emerald & Celestial Cyan Constellation Grid)
  - Variation 3: "Dissonância do Vazio & Fenda Singular" (Void Crimson, Spacetime Tear & High-Voltage Electric Blue)

Each variation includes:
  - 512x512 Backgrounds (and 640x360 wide versions)
  - 9-Sliceable Buttons (Normal, Hover, Pressed)
  - Status/Control Icons (32x32 and 64x64)
  - Progress Bars & Resonance Gauges
  - Complete Composed UI Mockups
  - A Unified Comparison Sheet
"""

import math
import os
import random
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
    """Variation 1: Vórtice Cósmico & Ondas Harmônicas (Godforge Cosmic Purple)."""
    im = Image.new('RGBA', (w, h), (14, 7, 28, 255))
    d = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2
    
    # 1. Swirling Cosmic Rift Vortex with Dithering
    col_deep = (14, 7, 28)
    col_mid = (56, 18, 88)
    col_bright = (130, 35, 160)
    col_core = (210, 80, 240)
    
    px = im.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)
            angle = math.atan2(dy, dx)
            # Spiral vortex twist
            spiral = math.sin(angle * 4.0 - dist * 0.04) * 0.18
            t = max(0.0, 1.0 - dist / (w * 0.52)) + spiral
            t = max(0.0, min(1.0, t))
            
            if t < 0.35:
                col = dither_pixel(x, y, col_deep, col_mid, t / 0.35)
            elif t < 0.7:
                col = dither_pixel(x, y, col_mid, col_bright, (t - 0.35) / 0.35)
            else:
                col = dither_pixel(x, y, col_bright, col_core, (t - 0.7) / 0.3)
                
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)

    # 2. Dual Harmonic Interference Sine Waves (Tuning Waveform)
    # Background wave chamber in middle
    wave_box_y = int(h * 0.62)
    wave_box_h = 100
    d.rectangle([20, wave_box_y, w - 20, wave_box_y + wave_box_h], fill=(8, 4, 16, 200), outline=(85, 45, 140, 240), width=2)
    
    # Wave grid lines
    for gy in range(wave_box_y + 10, wave_box_y + wave_box_h, 20):
        d.line([(22, gy), (w - 22, gy)], fill=(45, 25, 75, 140), width=1)
    d.line([(22, wave_box_y + wave_box_h // 2), (w - 22, wave_box_y + wave_box_h // 2)], fill=(120, 60, 190, 200), width=1)

    # Sine Wave 1 (Carrier frequency f - Cyan)
    pts_wave1 = []
    # Sine Wave 2 (Tuned harmonic p:q - Magenta)
    pts_wave2 = []
    for x in range(24, w - 24):
        rad = (x - 24) * 0.065
        y1 = wave_box_y + wave_box_h // 2 + int(32 * math.sin(rad))
        y2 = wave_box_y + wave_box_h // 2 + int(24 * math.sin(rad * 1.5 + 0.8))
        pts_wave1.append((x, y1))
        pts_wave2.append((x, y2))
        
    d.line(pts_wave2, fill=(255, 60, 220, 240), width=2)
    d.line(pts_wave1, fill=(0, 240, 255, 240), width=2)

    # 3. Octagonal 8-Pylon Anchor Ring with Celestial Nodes
    r_ring = 110
    d.ellipse([cx - r_ring, cy - 90 - r_ring, cx + r_ring, cy - 90 + r_ring], outline=(170, 90, 255, 120), width=2)
    d.ellipse([cx - r_ring + 14, cy - 90 - r_ring + 14, cx + r_ring - 14, cy - 90 + r_ring - 14], outline=(255, 215, 80, 140), width=1)
    
    # 8 Anchor Pylons placed around circle
    for i in range(8):
        ang = i * (360 / 8)
        rad = math.radians(ang)
        px_p = cx + int(r_ring * math.cos(rad))
        py_p = (cy - 90) + int(r_ring * math.sin(rad))
        # Beam towards center
        d.line([(px_p, py_p), (cx, cy - 90)], fill=(180, 100, 255, 80), width=1)
        # Pylon diamond node
        d.polygon([
            (px_p, py_p - 6), (px_p + 6, py_p), (px_p, py_p + 6), (px_p - 6, py_p)
        ], fill=(255, 215, 80, 255), outline=(255, 255, 255, 255))
        
    # Central Singularity Node
    d.ellipse([cx - 16, cy - 90 - 16, cx + 16, cy - 90 + 16], fill=(255, 255, 255, 255), outline=(255, 80, 240, 240))
    d.ellipse([cx - 8, cy - 90 - 8, cx + 8, cy - 90 + 8], fill=(18, 6, 32, 255))
    
    # Border Vignette
    for b in range(12):
        alpha = int(220 * (1.0 - b / 12))
        d.rectangle([b, b, w - 1 - b, h - 1 - b], outline=(8, 4, 16, alpha))
        
    return im


def generate_bg_variation_2_astrometric(w=512, h=512):
    """Variation 2: Atlas de Constelações & Fenda Eterial (Emerald & Celestial Cyan)."""
    im = Image.new('RGBA', (w, h), (6, 18, 22, 255))
    d = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2
    
    # 1. Ethereal Emerald & Deep Cyan Nebula
    col_deep = (6, 18, 22)
    col_mid = (12, 45, 52)
    col_bright = (18, 88, 92)
    col_hot = (40, 150, 145)
    
    px = im.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dx, dy = x - cx, y - cy
            dist = math.hypot(dx, dy)
            t = max(0.0, 1.0 - dist / (w * 0.58))
            angle = math.atan2(dy, dx)
            ripple = 0.12 * math.cos(angle * 5.0 + dist * 0.03)
            t = max(0.0, min(1.0, t + ripple))
            
            if t < 0.4:
                col = dither_pixel(x, y, col_deep, col_mid, t / 0.4)
            elif t < 0.75:
                col = dither_pixel(x, y, col_mid, col_bright, (t - 0.4) / 0.35)
            else:
                col = dither_pixel(x, y, col_bright, col_hot, (t - 0.75) / 0.25)
                
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)

    # 2. Astrolabe Coordinate Circles & Depth Rings (D1 to D80)
    for r in [50, 100, 150, 200]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(30, 110, 115, 90), width=1)
        # Degree tick marks
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            t1x, t1y = cx + int((r - 4) * math.cos(rad)), cy + int((r - 4) * math.sin(rad))
            t2x, t2y = cx + int((r + 4) * math.cos(rad)), cy + int((r + 4) * math.sin(rad))
            d.line([(t1x, t1y), (t2x, t2y)], fill=(80, 220, 200, 140), width=1)

    # 3. Constellation Seed Network (Linked procedural nodes)
    random.seed(108)
    constellation_stars = [
        (cx - 120, cy - 80, 'A3F-19'), (cx - 50, cy - 130, '7C2-04'), (cx + 60, cy - 120, '9D8-27'),
        (cx + 130, cy - 60, '1B4-09'), (cx + 80, cy + 50, 'E5K-88'), (cx - 30, cy + 90, 'Omega-0'),
        (cx - 110, cy + 40, 'V-404'), (cx, cy, 'CENTRAL')
    ]
    
    # Links
    links = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (1, 7), (4, 7), (6, 7)]
    for a, b in links:
        p1 = constellation_stars[a]
        p2 = constellation_stars[b]
        d.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=(0, 240, 220, 110), width=1)
        
    # Star nodes
    for sx, sy, label in constellation_stars:
        is_central = (label == 'CENTRAL')
        node_col = (255, 215, 80) if is_central else (140, 255, 240)
        d.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=node_col + (255,), outline=(255, 255, 255, 255))
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], outline=node_col + (120,), width=1)

    # 8 Anchor Pylon Symbols at perimeter
    for i in range(8):
        ang = i * (360 / 8) + 22.5
        rad = math.radians(ang)
        px_p = cx + int(215 * math.cos(rad))
        py_p = cy + int(215 * math.sin(rad))
        d.rectangle([px_p - 5, py_p - 5, px_p + 5, py_p + 5], fill=(15, 45, 55, 255), outline=(0, 255, 220, 220))
        
    return im


def generate_bg_variation_3_void(w=512, h=512):
    """Variation 3: Dissonância do Vazio & Fenda Singular (Void Crimson & Electric Blue)."""
    im = Image.new('RGBA', (w, h), (10, 5, 12, 255))
    d = ImageDraw.Draw(im)
    cx, cy = w // 2, h // 2
    
    # 1. Void Black & Spacetime Crimson Bleed
    col_void = (10, 5, 12)
    col_bleed = (45, 8, 22)
    col_crimson = (140, 18, 48)
    col_shock = (220, 30, 70)
    
    px = im.load()
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            dx, dy = x - cx, y - cy
            # Jagged diagonal spacetime tear
            tear_dist = abs(dy - 0.35 * dx)
            t = max(0.0, 1.0 - tear_dist / 140.0)
            
            if t < 0.4:
                col = dither_pixel(x, y, col_void, col_bleed, t / 0.4)
            elif t < 0.75:
                col = dither_pixel(x, y, col_bleed, col_crimson, (t - 0.4) / 0.35)
            else:
                col = dither_pixel(x, y, col_crimson, col_shock, (t - 0.75) / 0.25)
                
            for oy in range(2):
                for ox in range(2):
                    if x + ox < w and y + oy < h:
                        px[x + ox, y + oy] = col + (255,)

    # 2. Electric Blue Quantum Arcs bursting across the tear
    random.seed(77)
    for _ in range(16):
        x1 = random.randint(cx - 160, cx + 160)
        y1 = int(cy + 0.35 * (x1 - cx)) + random.randint(-15, 15)
        length = random.randint(30, 80)
        ang = random.uniform(-math.pi, math.pi)
        x2 = x1 + int(length * math.cos(ang))
        y2 = y1 + int(length * math.sin(ang))
        d.line([(x1, y1), (x2, y2)], fill=(80, 220, 255, 200), width=1)
        d.point(((x1 + x2)//2, (y1 + y2)//2), fill=(255, 255, 255, 255))

    # 3. Collapse Threshold Warning Rings & 8-Spike Tension Cage
    d.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], outline=(255, 40, 80, 180), width=2)
    d.ellipse([cx - 145, cy - 145, cx + 145, cy + 145], outline=(80, 200, 255, 140), width=1)
    
    # 8 Tension Spikes pointing inward
    for i in range(8):
        ang = i * (360 / 8)
        rad = math.radians(ang)
        p_outer = (cx + int(175 * math.cos(rad)), cy + int(175 * math.sin(rad)))
        p_inner = (cx + int(135 * math.cos(rad)), cy + int(135 * math.sin(rad)))
        d.line([p_outer, p_inner], fill=(255, 60, 90, 240), width=3)
        d.polygon([
            p_inner,
            (p_inner[0] + int(6 * math.cos(rad + 2.5)), p_inner[1] + int(6 * math.sin(rad + 2.5))),
            (p_inner[0] + int(6 * math.cos(rad - 2.5)), p_inner[1] + int(6 * math.sin(rad - 2.5)))
        ], fill=(255, 255, 255, 255))

    # Spacetime rip core
    d.polygon([
        (cx - 30, cy - 10), (cx, cy - 35), (cx + 30, cy + 10), (cx, cy + 35)
    ], fill=(255, 255, 255, 240), outline=(255, 30, 80, 255))
    
    return im


# ===========================================================================
# 2. BUTTONS (9-Sliceable, 64x32)
# ===========================================================================

def generate_button(theme, state='normal', w=64, h=32):
    """Generate 9-sliceable themed button for Rift Gate."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    if theme == 'cosmic':
        # Godforge-inspired Cosmic Purple / Magenta
        if state == 'normal':
            bg_top, bg_bot = (55, 26, 85), (32, 14, 52)
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
            
    elif theme == 'astrometric':
        # Astrometric Emerald & Celestial Cyan
        if state == 'normal':
            bg_top, bg_bot = (16, 48, 48), (8, 28, 30)
            border_outer, border_inner = (15, 110, 105), (35, 175, 160)
            glow_corner = (120, 255, 240)
        elif state == 'hover':
            bg_top, bg_bot = (25, 68, 68), (14, 40, 42)
            border_outer, border_inner = (25, 145, 135), (60, 215, 195)
            glow_corner = (180, 255, 250)
        else: # pressed
            bg_top, bg_bot = (8, 22, 24), (18, 44, 45)
            border_outer, border_inner = (10, 75, 70), (20, 120, 110)
            glow_corner = (70, 180, 170)
            
    else: # void
        # Void Crimson & Spacetime Overload
        if state == 'normal':
            bg_top, bg_bot = (54, 16, 26), (32, 8, 16)
            border_outer, border_inner = (160, 30, 65), (220, 50, 95)
            glow_corner = (255, 140, 175)
        elif state == 'hover':
            bg_top, bg_bot = (75, 24, 38), (45, 12, 24)
            border_outer = (200, 45, 85)
            border_inner = (255, 80, 130)
            glow_corner = (255, 190, 215)
        else: # pressed
            bg_top, bg_bot = (22, 6, 12), (42, 12, 20)
            border_outer = (105, 20, 45)
            border_inner = (145, 30, 65)
            glow_corner = (180, 50, 90)
            
    for y in range(h):
        t = y / (h - 1)
        row_col = lerp_color(bg_top, bg_bot, t)
        d.line([(2, y), (w - 3, y)], fill=row_col + (255,))
        
    d.rectangle([1, 1, w - 2, h - 2], outline=border_outer + (255,))
    d.rectangle([2, 2, w - 3, h - 3], outline=border_inner + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=(8, 8, 12, 255))
    
    # Corner notches
    d.point((2, 2), fill=glow_corner + (255,))
    d.point((w - 3, 2), fill=glow_corner + (255,))
    d.point((2, h - 3), fill=glow_corner + (255,))
    d.point((w - 3, h - 3), fill=glow_corner + (255,))
    
    return im


# ===========================================================================
# 3. STATUS & CONTROL ICONS (64x64, downsampled to 32x32)
# ===========================================================================

def generate_icon_rift_tear(theme, size=64):
    """Dimensional rift vortex opening."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    col_tear = (190, 80, 255) if theme == 'cosmic' else ((0, 255, 220) if theme == 'astrometric' else (255, 40, 80))
    col_core = (255, 215, 80) if theme == 'cosmic' else ((255, 255, 255) if theme == 'astrometric' else (80, 220, 255))
    
    # Outer swirling vortex petals
    for i in range(6):
        ang = i * (360 / 6)
        rad = math.radians(ang)
        p1 = (c + int(12 * math.cos(rad)), c + int(12 * math.sin(rad)))
        p2 = (c + int(26 * math.cos(rad + 0.8)), c + int(26 * math.sin(rad + 0.8)))
        d.line([p1, p2], fill=col_tear + (190,), width=2)
        
    # Central eye of rift
    d.ellipse([c - 14, c - 14, c + 14, c + 14], fill=(12, 6, 20, 255), outline=col_tear + (240,), width=2)
    d.polygon([(c, c - 8), (c + 6, c), (c, c + 8), (c - 6, c)], fill=col_core + (255,))
    return im


def generate_icon_harmonic_wave(theme, size=64):
    """Interference waveform / harmonic resonance."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    w1_col = (0, 240, 255) if theme == 'cosmic' else ((80, 255, 220) if theme == 'astrometric' else (255, 60, 90))
    w2_col = (255, 80, 220) if theme == 'cosmic' else ((255, 215, 80) if theme == 'astrometric' else (80, 220, 255))
    
    # Outer gauge frame
    d.rectangle([8, 14, size - 9, size - 15], outline=(60, 60, 85, 255), fill=(12, 12, 18, 255))
    d.line([(8, c), (size - 9, c)], fill=(40, 40, 60, 255), width=1)
    
    # Two interfering waves
    pts1, pts2 = [], []
    for x in range(10, size - 10):
        t = (x - 10) * 0.22
        pts1.append((x, c + int(10 * math.sin(t))))
        pts2.append((x, c + int(8 * math.sin(t * 1.5 + 1.2))))
        
    d.line(pts1, fill=w1_col + (255,), width=2)
    d.line(pts2, fill=w2_col + (255,), width=2)
    return im


def generate_icon_anchor_pylon(theme, size=64):
    """Stabilization anchor pylon with energetic vertical beam."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    beam_col = (170, 90, 255) if theme == 'cosmic' else ((0, 255, 220) if theme == 'astrometric' else (255, 40, 80))
    pylon_metal = (180, 190, 210)
    
    # Vertical stabilization beam
    d.line([(c, 6), (c, 58)], fill=beam_col + (140,), width=5)
    d.line([(c, 6), (c, 58)], fill=(255, 255, 255, 240), width=1)
    
    # Pylon spike structure
    pts_pylon = [(c, 10), (c + 9, 36), (c + 6, 52), (c - 6, 52), (c - 9, 36)]
    d.polygon(pts_pylon, fill=(40, 45, 60, 255), outline=pylon_metal + (255,))
    
    # Focus rings around pylon
    d.arc([c - 14, 22, c + 14, 30], 0, 180, fill=beam_col + (240,), width=2)
    d.arc([c - 16, 38, c + 16, 46], 0, 180, fill=beam_col + (240,), width=2)
    return im


def generate_icon_exotic_matter(theme, size=64):
    """Exotic matter containment vial / stabilization fluid."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    fluid_col = (210, 60, 240) if theme == 'cosmic' else ((20, 220, 180) if theme == 'astrometric' else (255, 60, 60))
    
    # Vial container
    pts_flask = [
        (c - 6, 12), (c + 6, 12), (c + 6, 22), (c + 18, 48), (c - 18, 48), (c - 6, 22)
    ]
    d.polygon(pts_flask, fill=(20, 25, 38, 255), outline=(130, 140, 165, 255))
    
    # Liquid fill inside
    pts_liquid = [(c + 4, 26), (c + 15, 46), (c - 15, 46), (c - 4, 26)]
    d.polygon(pts_liquid, fill=fluid_col + (200,))
    # Meniscus
    d.line([(c - 4, 26), (c + 4, 26)], fill=(255, 255, 255, 220), width=2)
    
    # Bubbles / sparkle
    d.point((c, 36), fill=(255, 255, 255, 255))
    d.point((c + 5, 42), fill=(255, 255, 255, 255))
    return im


def generate_icon_rift_probe(theme, size=64):
    """Rift probe / dimensional scanner."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    accent = (255, 215, 80) if theme == 'cosmic' else ((0, 240, 220) if theme == 'astrometric' else (80, 220, 255))
    
    # Probe octahedron satellite
    pts_sat = [(c, 12), (c + 14, c), (c, 52), (c - 14, c)]
    d.polygon(pts_sat, fill=(45, 50, 68, 255), outline=(140, 150, 175, 255))
    d.line([(c - 14, c), (c + 14, c)], fill=(180, 190, 215, 255), width=1)
    d.line([(c, 12), (c, 52)], fill=(255, 255, 255, 220), width=1)
    
    # Sensor dish / laser beam emission
    d.ellipse([c - 5, c - 5, c + 5, c + 5], fill=accent + (255,))
    d.line([(c, 52), (c, 60)], fill=accent + (220,), width=2)
    return im


def generate_icon_depth_anchor(theme, size=64):
    """Depth anchor / harmonic resonance chord token."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = size // 2
    
    anchor_col = (180, 100, 255) if theme == 'cosmic' else ((0, 230, 200) if theme == 'astrometric' else (255, 60, 90))
    
    # Heavy triangular dimensional anchor symbol
    pts_tri = [(c, 12), (c + 20, 48), (c - 20, 48)]
    d.polygon(pts_tri, fill=(24, 24, 34, 255), outline=(120, 130, 150, 255))
    
    # Inner energy triangle
    pts_inner = [(c, 24), (c + 10, 42), (c - 10, 42)]
    d.polygon(pts_inner, fill=anchor_col + (220,), outline=(255, 255, 255, 255))
    return im


# ===========================================================================
# 4. PROGRESS BARS & GAUGES
# ===========================================================================

def generate_progressbar(theme, w=256, h=16, frac=0.94, bar_type='resonance'):
    """Resonance (R), Stability (S), or Depth (D) progress bar."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    d.rectangle([0, 0, w - 1, h - 1], fill=(12, 12, 18, 255), outline=(45, 45, 60, 255))
    d.rectangle([1, 1, w - 2, h - 2], outline=(20, 20, 28, 255))
    
    fill_w = max(0, min(w - 4, int((w - 4) * frac)))
    if fill_w > 0:
        if bar_type == 'resonance':
            # Resonance: Cyan to Gold or Pink
            c1, c2 = (0, 180, 220), (255, 215, 80)
        elif bar_type == 'stability':
            # Stability: Green to Emerald
            c1, c2 = (30, 140, 70), (80, 255, 140)
        else: # depth
            # Depth: Purple to Magenta
            c1, c2 = (80, 30, 140), (240, 70, 210)
            
        for x in range(fill_w):
            t = x / (w - 4)
            col = lerp_color(c1, c2, t)
            d.line([(2 + x, 2), (2 + x, h - 3)], fill=col + (255,))
            d.point((2 + x, 2), fill=(255, 255, 255, 180))
            
    # Milestone threshold markers (e.g. R=0.9, R=0.98)
    for m in [0.5, 0.9, 0.98]:
        mx = 2 + int((w - 4) * m)
        d.line([(mx, 0), (mx, h - 1)], fill=(255, 255, 255, 200), width=1)
        
    return im


# ===========================================================================
# 5. COMPOSED UI PREVIEW (640x480 Mockup for each Variation)
# ===========================================================================

def compose_preview(theme_name, bg_img, title, palette_desc):
    """Compose full GUI mockup at 640x480."""
    canvas = Image.new('RGBA', (640, 480), (10, 10, 15, 255))
    d = ImageDraw.Draw(canvas)
    
    # 1. Main Viewport
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(70, 75, 95, 255), width=2)
    
    # 2. Side Panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 18, 26, 255), outline=(50, 55, 75, 255), width=2)
    
    # Title Header
    d.rectangle([16, 12, 624, 40], fill=(24, 24, 34, 255), outline=(60, 65, 85, 255))
    d.text((24, 18), f"GTNA · PORTÃO DE FENDA DIMENSIONAL [UIV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel contents
    d.text((panel_x + 10, panel_y + 12), "SINTONIA DIMENSIONAL", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(60, 65, 85, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Semente: A3F-19", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Bioma: Planície Cristalina", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Pilones Ativos: 8/8", fill=(80, 255, 140, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Consumo: 0.03 L/s Exótica", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Icons row
    ico_tear = generate_icon_rift_tear(theme_name, 36)
    ico_wave = generate_icon_harmonic_wave(theme_name, 36)
    ico_pylon = generate_icon_anchor_pylon(theme_name, 36)
    ico_fluid = generate_icon_exotic_matter(theme_name, 36)
    
    canvas.paste(ico_tear, (panel_x + 10, panel_y + 96), ico_tear)
    canvas.paste(ico_wave, (panel_x + 50, panel_y + 96), ico_wave)
    canvas.paste(ico_pylon, (panel_x + 90, panel_y + 96), ico_pylon)
    canvas.paste(ico_fluid, (panel_x + 130, panel_y + 96), ico_fluid)
    
    # Bars
    d.text((panel_x + 10, panel_y + 144), "RESSONÂNCIA R = 0.94", fill=(255, 215, 80, 255), font=FONT_TEXT)
    bar_r = generate_progressbar(theme_name, panel_w - 20, 12, 0.94, 'resonance')
    canvas.paste(bar_r, (panel_x + 10, panel_y + 160), bar_r)
    
    d.text((panel_x + 10, panel_y + 180), "ESTABILIDADE S = 88%", fill=(80, 255, 140, 255), font=FONT_TEXT)
    bar_s = generate_progressbar(theme_name, panel_w - 20, 12, 0.88, 'stability')
    canvas.paste(bar_s, (panel_x + 10, panel_y + 196), bar_s)
    
    d.text((panel_x + 10, panel_y + 220), "PROFUNDIDADE D: 23 (Manto)", fill=(240, 140, 255, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Multiplicador D^1.5: 110.3x", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Buttons
    btn_normal = generate_button(theme_name, 'normal', 74, 28)
    btn_hover = generate_button(theme_name, 'hover', 74, 28)
    btn_main = generate_button(theme_name, 'pressed', 154, 32)
    
    canvas.paste(btn_normal, (panel_x + 10, panel_y + 266), btn_normal)
    d.text((panel_x + 22, panel_y + 274), "SONDA", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_hover, (panel_x + 90, panel_y + 266), btn_hover)
    d.text((panel_x + 100, panel_y + 274), "ÂNCORA", fill=(255, 255, 255, 255), font=FONT_BTN)
    
    canvas.paste(btn_main, (panel_x + 10, panel_y + 306), btn_main)
    d.text((panel_x + 32, panel_y + 314), "[ SINTONIZAR ]", fill=(255, 220, 100, 255), font=FONT_BTN)
    
    # Harmonics staff in viewport bottom
    d.rectangle([26, 380, 426, 420], fill=(12, 12, 18, 220), outline=(50, 55, 75, 200))
    d.text((36, 392), "PARTITURA:", fill=(180, 190, 210, 255), font=FONT_PANEL)
    d.text((120, 392), "Quinta (3:2)  ·  Oitava (2:1)  ·  Terça (5:4)", fill=(255, 215, 80, 255), font=FONT_TEXT)
    
    # Footer
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
    
    d.rectangle([0, 0, sheet.width, 60], fill=(20, 20, 30, 255), outline=(50, 55, 75, 255))
    d.text((30, 14), "GTNA · COMPARATIVO DE DESIGN DE UI — MULTIBLOCO 2: PORTÃO DE FENDA DIMENSIONAL", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "3 Variações de Estilo Visual (Vórtice Harmônico, Atlas Astrométrico e Vazio Dissonante)", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    sheet.paste(p1, (10, 75))
    sheet.paste(p2, (sw + 20, 75))
    sheet.paste(p3, (sw * 2 + 30, 75))
    
    return sheet


# ===========================================================================
# MAIN PIPELINE
# ===========================================================================

def main():
    print(">>> Gerando Variações de UI para o Portão de Fenda Dimensional...")
    
    # 1. Backgrounds
    print("  -> Gerando Backgrounds (512x512 & Wide)...")
    bg1 = generate_bg_variation_1_cosmic(512, 512)
    bg1.save(os.path.join(BG_DIR, 'bg_variation_1_cosmic_512.png'))
    generate_bg_variation_1_cosmic(640, 360).save(os.path.join(BG_DIR, 'bg_variation_1_cosmic_wide.png'))
    
    bg2 = generate_bg_variation_2_astrometric(512, 512)
    bg2.save(os.path.join(BG_DIR, 'bg_variation_2_astrometric_512.png'))
    generate_bg_variation_2_astrometric(640, 360).save(os.path.join(BG_DIR, 'bg_variation_2_astrometric_wide.png'))
    
    bg3 = generate_bg_variation_3_void(512, 512)
    bg3.save(os.path.join(BG_DIR, 'bg_variation_3_void_512.png'))
    generate_bg_variation_3_void(640, 360).save(os.path.join(BG_DIR, 'bg_variation_3_void_wide.png'))

    # 2. Buttons
    print("  -> Gerando Botões 9-Slice...")
    for theme in ['cosmic', 'astrometric', 'void']:
        for state in ['normal', 'hover', 'pressed']:
            btn = generate_button(theme, state, 64, 32)
            btn.save(os.path.join(BTN_DIR, f'btn_{theme}_{state}.png'))

    # 3. Icons
    print("  -> Gerando Ícones de Sintonia e Fenda...")
    icon_generators = [
        ('rift_tear', generate_icon_rift_tear),
        ('harmonic_wave', generate_icon_harmonic_wave),
        ('anchor_pylon', generate_icon_anchor_pylon),
        ('exotic_matter', generate_icon_exotic_matter),
        ('rift_probe', generate_icon_rift_probe),
        ('depth_anchor', generate_icon_depth_anchor)
    ]
    for theme in ['cosmic', 'astrometric', 'void']:
        for name, gen_fn in icon_generators:
            ico64 = gen_fn(theme, 64)
            ico64.save(os.path.join(ICO_DIR, f'ico_{name}_{theme}_64.png'))
            ico32 = ico64.resize((32, 32), Image.NEAREST)
            ico32.save(os.path.join(ICO_DIR, f'ico_{name}_{theme}_32.png'))

    # 4. Progress Bars
    print("  -> Gerando Barras de Ressonância e Estabilidade...")
    for theme in ['cosmic', 'astrometric', 'void']:
        bar_r = generate_progressbar(theme, 256, 16, 0.94, 'resonance')
        bar_r.save(os.path.join(BAR_DIR, f'progressbar_{theme}_resonance.png'))
        bar_s = generate_progressbar(theme, 256, 16, 0.88, 'stability')
        bar_s.save(os.path.join(BAR_DIR, f'progressbar_{theme}_stability.png'))

    # 5. Full Composed Previews
    print("  -> Montando Telas Completas de Preview...")
    prev1 = compose_preview('cosmic', bg1, "Variação 1: Vórtice Cósmico & Ondas Harmônicas", "Púrpura Profundo, Ondas Senoidais Ciano/Fúcsia, 8 Pilones Celestiais")
    prev1.save(os.path.join(PREV_DIR, 'preview_variation_1_cosmic.png'))
    
    prev2 = compose_preview('astrometric', bg2, "Variação 2: Atlas Astrométrico & Fenda Eterial", "Verde-Esmeralda Abissal, Rede de Constelações, Astrolábio de Sementes")
    prev2.save(os.path.join(PREV_DIR, 'preview_variation_2_astrometric.png'))
    
    prev3 = compose_preview('void', bg3, "Variação 3: Dissonância do Vazio & Fenda Singular", "Vazio Negro, Rasgadura Carmesim, Arcos Quânticos Azul-Elétrico")
    prev3.save(os.path.join(PREV_DIR, 'preview_variation_3_void.png'))

    # 6. Combined Comparison Sheet
    print("  -> Gerando Prancha Comparativa Unificada...")
    sheet = generate_comparison_sheet(prev1, prev2, prev3)
    sheet.save(os.path.join(OUT_DIR, 'comparison_overview.png'))
    
    print("\n[OK] Todos os assets do Portão de Fenda foram gerados com sucesso em:")
    print(f"     {OUT_DIR}")

if __name__ == '__main__':
    main()
