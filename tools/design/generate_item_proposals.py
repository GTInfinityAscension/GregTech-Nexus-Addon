#!/usr/bin/env python3
"""Generate Design Proposals for GTNA Endgame Items:
  1. Target Cartridge (Cartucho de Alvo - Lança Cinética Orbital)
  2. Contained Particles (Armadilhas de Penning - Anel Colisor de Antimatéria)
  3. Rift Probe (Sonda de Fenda - Portão de Fenda Dimensional)
  4. Depth Anchor (Âncora de Profundidade - Portão de Fenda Dimensional)
  5. Rift Singularity (Singularidade de Fenda - Portão de Fenda Dimensional)

Outputs to: tools/design/item_proposals/
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(BASE_DIR, 'item_proposals')

CATEGORIES = ['target_cartridge', 'contained_particles', 'rift_probe', 'depth_anchor', 'rift_singularity']
for cat in CATEGORIES:
    os.makedirs(os.path.join(PROPOSALS_DIR, cat, '16x16'), exist_ok=True)
    os.makedirs(os.path.join(PROPOSALS_DIR, cat, '32x32'), exist_ok=True)
    os.makedirs(os.path.join(PROPOSALS_DIR, cat, 'previews'), exist_ok=True)

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

FONT_HEADER = get_font(18, bold=True)
FONT_SUB = get_font(13, bold=False)
FONT_TITLE = get_font(12, bold=True)
FONT_TEXT = get_font(10, bold=False)
FONT_MICRO = get_font(9, bold=False)

def put_pixel(im, x, y, col):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((x, y), col)

def draw_border_and_glow(im, outline_col=(20, 15, 30, 255)):
    """Add 1px outline around non-transparent pixels."""
    w, h = im.size
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    for y in range(h):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            if a > 30:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        if im.getpixel((nx, ny))[3] <= 30:
                            out.putpixel((nx, ny), outline_col)
    out.alpha_composite(im)
    return out

# ===========================================================================
# 1. TARGET CARTRIDGE (CARTUCHO DE ALVO)
# ===========================================================================
def create_target_cartridge_var_a(size=32):
    """Var A: Cosmic Optical Crystal Cartridge (Godforge Theme)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Gold naquadah body with chamfered top
    # Body bounds: x from 6 to 25, y from 4 to 28
    body_fill = (45, 30, 65, 255)
    gold_hi = (255, 220, 100, 255)
    gold_mid = (210, 160, 45, 255)
    gold_dark = (140, 95, 25, 255)
    casing_bg = (24, 16, 36, 255)
    
    # Main outer rectangle
    d.polygon([(9, 4), (22, 4), (25, 7), (25, 27), (6, 27), (6, 7)], fill=casing_bg, outline=gold_dark)
    # Highlight bevels
    d.line([(9, 4), (22, 4)], fill=gold_hi, width=1)
    d.line([(6, 7), (9, 4)], fill=gold_hi, width=1)
    d.line([(6, 7), (6, 27)], fill=gold_mid, width=1)
    d.line([(25, 7), (25, 27)], fill=gold_dark, width=1)
    d.line([(6, 27), (25, 27)], fill=gold_dark, width=1)
    
    # Golden AE2 Interface Pins at bottom
    for px in [9, 13, 17, 21]:
        d.rectangle([px, 28, px + 1, 30], fill=gold_hi)
        
    # Central Optical Crystal Window (Hexagonal)
    cx, cy = 15, 14
    d.polygon([(cx, cy - 7), (cx + 6, cy - 3), (cx + 6, cy + 4), (cx, cy + 8), (cx - 6, cy + 4), (cx - 6, cy - 3)],
              fill=(16, 8, 28, 255), outline=gold_mid)
              
    # Glowing Holographic Gem & Reticle
    gem_colors = [
        (180, 80, 255, 255),
        (0, 240, 255, 255),
        (255, 255, 255, 255),
    ]
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(120, 40, 200, 255))
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(0, 240, 255, 255))
    put_pixel(im, cx, cy, (255, 255, 255, 255))
    
    # Fine Crosshair targeting reticle
    d.line([(cx - 5, cy), (cx + 5, cy)], fill=(0, 240, 255, 180))
    d.line([(cx, cy - 5), (cx, cy + 5)], fill=(0, 240, 255, 180))
    
    # Top LED indicator
    d.rectangle([14, 5, 16, 6], fill=(80, 255, 140, 255))
    # Side telemetry grip grooves
    for gy in [10, 13, 16, 19]:
        d.line([(7, gy), (8, gy)], fill=gold_dark)
        d.line([(23, gy), (24, gy)], fill=gold_dark)
        
    return draw_border_and_glow(im)

def create_target_cartridge_var_b(size=32):
    """Var B: Aerospace Tactical Railgun ROM."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    steel_hi = (180, 190, 210, 255)
    steel_mid = (100, 110, 130, 255)
    steel_dark = (50, 55, 70, 255)
    casing_fill = (22, 26, 34, 255)
    
    # Heavy rectangular rugged casing
    d.rectangle([7, 3, 24, 27], fill=casing_fill, outline=steel_dark)
    d.line([(7, 3), (24, 3)], fill=steel_hi)
    d.line([(7, 3), (7, 27)], fill=steel_hi)
    d.line([(24, 3), (24, 27)], fill=steel_dark)
    d.line([(7, 27), (24, 27)], fill=steel_dark)
    
    # Top Tactical Warning Stripes (Yellow/Black)
    stripes = [(8, 4), (11, 4), (14, 4), (17, 4), (20, 4)]
    for sx, sy in stripes:
        d.line([(sx, sy), (sx + 2, sy + 3)], fill=(255, 200, 40, 255), width=1)
        
    # Center Microchip / Wafer Grid
    d.rectangle([10, 10, 21, 20], fill=(12, 14, 18, 255), outline=steel_mid)
    # Green circuit matrix traces
    for py in [12, 15, 18]:
        d.line([(12, py), (19, py)], fill=(0, 220, 140, 200))
    put_pixel(im, 15, 15, (255, 255, 255, 255))
    
    # Bottom Military Connector Terminals
    for px in [9, 11, 13, 15, 17, 19, 21]:
        d.rectangle([px, 27, px, 29], fill=(255, 215, 80, 255))
        
    # 3 Status LEDs on the left
    d.rectangle([8, 22, 9, 23], fill=(80, 255, 140, 255))   # Green: Lock
    d.rectangle([11, 22, 12, 23], fill=(0, 240, 255, 255))  # Cyan: Sync
    d.rectangle([14, 22, 15, 23], fill=(255, 160, 40, 255)) # Amber: Armed
    return draw_border_and_glow(im)

def create_target_cartridge_var_c(size=32):
    """Var C: Astrometric Cartridge with Holographic Celestial Body Dome."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    plat_hi = (220, 230, 255, 255)
    plat_mid = (130, 145, 180, 255)
    plat_dark = (60, 70, 95, 255)
    
    # Curved ergonomic body
    d.polygon([(9, 3), (22, 3), (26, 8), (26, 26), (22, 29), (9, 29), (5, 26), (5, 8)],
              fill=(18, 20, 32, 255), outline=plat_dark)
    d.line([(9, 3), (22, 3)], fill=plat_hi)
    d.line([(5, 8), (9, 3)], fill=plat_hi)
    d.line([(5, 8), (5, 26)], fill=plat_mid)
    
    # Holographic Observation Dome (Central Circle)
    cx, cy = 15, 16
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(10, 8, 24, 255), outline=(0, 240, 255, 220))
    
    # Mini Pixel Celestial Body inside (Cratered Asteroid / Moon)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(160, 170, 195, 255), outline=(210, 220, 240, 255))
    # Crater details
    put_pixel(im, cx - 2, cy - 2, (100, 110, 130, 255))
    put_pixel(im, cx + 2, cy + 1, (100, 110, 130, 255))
    put_pixel(im, cx - 1, cy + 2, (80, 90, 110, 255))
    
    # Astrometric Orbit Ring around the body
    d.arc([cx - 7, cy - 4, cx + 7, cy + 4], 30, 330, fill=(255, 215, 80, 240))
    
    # Bottom Data Pins
    d.rectangle([11, 29, 20, 30], fill=(255, 215, 80, 255))
    return draw_border_and_glow(im)

# ===========================================================================
# 2. CONTAINED PARTICLES (ARMADILHAS DE PENNING COM PARTÍCULAS)
# ===========================================================================
def create_contained_particle(particle_type="higgs", variant="a", size=32):
    """Contained Particle in Cryogenic Penning Trap Capsule.
    Types: 'higgs', 'antiproton', 'qgp', 'lambda', 'positron'
    Variants: 'a' (Quadrupole Cylinder), 'b' (Hexagonal Monolith), 'c' (Triradial Flask)
    """
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Palette per particle
    p_palettes = {
        'higgs': {
            'glow': (255, 215, 80, 255),
            'core': (255, 255, 255, 255),
            'field': (255, 235, 140, 180),
            'label': 'H0'
        },
        'antiproton': {
            'glow': (0, 240, 255, 255),
            'core': (180, 80, 255, 255),
            'field': (0, 200, 255, 180),
            'label': 'p-'
        },
        'qgp': {
            'glow': (255, 60, 100, 255),
            'core': (255, 200, 40, 255),
            'field': (255, 120, 40, 180),
            'label': 'QGP'
        },
        'lambda': {
            'glow': (80, 255, 140, 255),
            'core': (200, 255, 120, 255),
            'field': (0, 220, 100, 180),
            'label': 'Lam'
        },
        'positron': {
            'glow': (0, 200, 255, 255),
            'core': (255, 255, 255, 255),
            'field': (120, 160, 255, 180),
            'label': 'e+'
        }
    }
    pinfo = p_palettes.get(particle_type, p_palettes['higgs'])
    
    if variant == "a":
        # Variant A: Quadrupole Penning Cylinder (Classic High-Tech Vacuum Tube)
        gold_hi = (255, 225, 120, 255)
        gold_mid = (210, 165, 45, 255)
        gold_dark = (120, 85, 20, 255)
        glass_tint = (16, 24, 38, 200)
        
        # Top Superconducting Magnet Cap
        d.rectangle([9, 2, 22, 6], fill=gold_mid, outline=gold_dark)
        d.line([(9, 2), (22, 2)], fill=gold_hi)
        # Top cryo valve
        d.rectangle([14, 0, 17, 2], fill=(180, 190, 210, 255))
        
        # Bottom Magnet Cap & Connector
        d.rectangle([9, 25, 22, 29], fill=gold_mid, outline=gold_dark)
        d.line([(9, 25), (22, 25)], fill=gold_hi)
        d.rectangle([13, 29, 18, 31], fill=(255, 215, 80, 255))
        
        # Transparent Vacuum Glass Tube Body
        d.rectangle([9, 6, 22, 25], fill=glass_tint, outline=(70, 95, 130, 255))
        # Glass reflections on left and right
        d.line([(10, 7), (10, 24)], fill=(255, 255, 255, 90))
        d.line([(11, 7), (11, 24)], fill=(255, 255, 255, 50))
        d.line([(21, 7), (21, 24)], fill=(255, 255, 255, 40))
        
        # 4 Quadrupole Needle Electrodes
        d.line([(10, 8), (12, 11)], fill=gold_hi)
        d.line([(21, 8), (19, 11)], fill=gold_hi)
        d.line([(10, 23), (12, 20)], fill=gold_hi)
        d.line([(21, 23), (19, 20)], fill=gold_hi)
        
        # Central Trapped Particle Core
        cx, cy = 15, 15
        # Soft magnetic field rings
        d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], outline=pinfo['field'])
        d.ellipse([cx - 3, cy - 5, cx + 3, cy + 5], outline=pinfo['field'])
        # Glowing Particle Cluster
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=pinfo['glow'])
        d.ellipse([cx - 1, cy - 1, cx + 1, cy + 1], fill=pinfo['core'])
        put_pixel(im, cx, cy, (255, 255, 255, 255))
        
    elif variant == "b":
        # Variant B: Hexagonal Monolith Cell
        neut_hi = (160, 175, 200, 255)
        neut_mid = (70, 80, 100, 255)
        neut_dark = (35, 40, 55, 255)
        
        # Heavy Hexagonal Body
        d.polygon([(9, 3), (22, 3), (27, 10), (27, 21), (22, 28), (9, 28), (4, 21), (4, 10)],
                  fill=(20, 22, 32, 255), outline=neut_dark)
        d.line([(9, 3), (22, 3)], fill=neut_hi)
        d.line([(4, 10), (9, 3)], fill=neut_hi)
        d.line([(4, 10), (4, 21)], fill=neut_mid)
        
        # Circular Flange with Gold Bolts
        cx, cy = 15, 15
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(12, 14, 20, 255), outline=(255, 215, 80, 240))
        # 4 bolts
        for bx, by in [(cx - 6, cy - 6), (cx + 6, cy - 6), (cx - 6, cy + 6), (cx + 6, cy + 6)]:
            put_pixel(im, bx, by, (255, 220, 100, 255))
            
        # Interior Particle Core
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=pinfo['glow'])
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=pinfo['core'])
        put_pixel(im, cx, cy, (255, 255, 255, 255))
        
        # Side Cryo Level Gauges
        d.rectangle([2, 12, 3, 19], fill=(0, 240, 255, 220))
        d.rectangle([28, 12, 29, 19], fill=(0, 240, 255, 220))
        
    elif variant == "c":
        # Variant C: Triradial Field-Suspension Flask
        cx, cy = 15, 15
        # Spherical glass orb
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(15, 20, 35, 220), outline=(0, 240, 255, 180))
        
        # 3 Curved Magnetic Claws / Pylons (Top, Bottom-Left, Bottom-Right)
        gold_hi = (255, 220, 90, 255)
        # Top pylon
        d.polygon([(13, 2), (18, 2), (16, 7), (15, 7)], fill=gold_hi)
        # Bottom left
        d.polygon([(4, 23), (8, 27), (11, 23), (7, 19)], fill=gold_hi)
        # Bottom right
        d.polygon([(27, 23), (23, 27), (20, 23), (24, 19)], fill=gold_hi)
        
        # Central Energetic Plasma Singularity
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=pinfo['glow'])
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=pinfo['core'])
        put_pixel(im, cx, cy, (255, 255, 255, 255))
        
        # Cross magnetic field lines
        d.arc([cx - 8, cy - 5, cx + 8, cy + 5], 0, 360, fill=(255, 255, 255, 100))
        
    return draw_border_and_glow(im)

# ===========================================================================
# 3. RIFT PROBE (SONDA DE FENDA)
# ===========================================================================
def create_rift_probe_var_a(size=32):
    """Var A: Tachyon Needle Dart (Hypersonic Sub-Space Dart)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Diagonal orientation (pointing top-right or vertical pointing up)
    # Let's make it vertical pointing up for crisp symmetry and distinct silhouette
    # Piercing Needle Tip (y from 2 to 9)
    d.line([(15, 2), (15, 9)], fill=(0, 240, 255, 255), width=1)
    put_pixel(im, 15, 2, (255, 255, 255, 255))
    put_pixel(im, 14, 5, (0, 240, 255, 200))
    put_pixel(im, 16, 5, (0, 240, 255, 200))
    
    # Sensor Module & Naquadah Fuselage
    d.polygon([(15, 8), (19, 13), (19, 23), (15, 27), (11, 23), (11, 13)],
              fill=(35, 18, 55, 255), outline=(140, 70, 210, 255))
    d.line([(15, 8), (19, 13)], fill=(255, 215, 80, 255))
    d.line([(15, 8), (11, 13)], fill=(255, 215, 80, 255))
    
    # 4 Swept Phase Stabilizer Wings
    # Left wing
    d.polygon([(11, 15), (4, 21), (5, 26), (11, 23)], fill=(20, 10, 35, 255), outline=(0, 240, 255, 220))
    # Right wing
    d.polygon([(19, 15), (26, 21), (25, 26), (19, 23)], fill=(20, 10, 35, 255), outline=(0, 240, 255, 220))
    
    # Central Resonance Capacitor Core (Pulsing Diamond)
    d.polygon([(15, 14), (18, 17), (15, 20), (12, 17)], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255))
    put_pixel(im, 15, 17, (255, 255, 255, 255))
    
    # Rear Stabilizer Ion Thruster
    d.rectangle([13, 27, 17, 29], fill=(255, 215, 80, 255))
    d.line([(14, 30), (16, 30)], fill=(0, 240, 255, 220))
    put_pixel(im, 15, 31, (0, 240, 255, 180))
    return draw_border_and_glow(im)

def create_rift_probe_var_b(size=32):
    """Var B: Octahedral Harmonic Astrolabe (Resonant Gyro Probe)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 15, 15
    
    gold_hi = (255, 220, 90, 255)
    gold_dark = (140, 95, 25, 255)
    
    # Outer Gimbal Ring (Gold)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=gold_dark, width=1)
    d.arc([cx - 12, cy - 12, cx + 12, cy + 12], 135, 315, fill=gold_hi)
    
    # Inner Tilted Ring (Cosmic Cyan/Violet)
    d.ellipse([cx - 9, cy - 6, cx + 9, cy + 6], outline=(0, 240, 255, 220), width=1)
    
    # Central Octahedral Resonator Crystal
    d.polygon([(cx, cy - 9), (cx + 6, cy), (cx, cy + 9), (cx - 6, cy)],
              fill=(160, 60, 240, 255), outline=(255, 255, 255, 255))
    # Facet split
    d.line([(cx, cy - 9), (cx, cy + 9)], fill=(255, 255, 255, 200))
    d.line([(cx - 6, cy), (cx + 6, cy)], fill=(200, 100, 255, 220))
    
    # 4 Harmonic tuning emitter antennae extending along axes
    for ax, ay in [(cx, 1), (cx, 29), (1, cy), (29, cy)]:
        put_pixel(im, ax, ay, (0, 240, 255, 255))
    d.line([(cx, 3), (cx, cy - 9)], fill=gold_hi)
    d.line([(cx, 27), (cx, cy + 9)], fill=gold_dark)
    return draw_border_and_glow(im)

def create_rift_probe_var_c(size=32):
    """Var C: Deep Horizon Bathyscaphe (Armored Spherical Explorer)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 15, 16
    
    # Heavy armored sphere body
    d.ellipse([cx - 10, cy - 9, cx + 10, cy + 9], fill=(24, 18, 36, 255), outline=(130, 65, 195, 255))
    # Top highlight
    d.arc([cx - 9, cy - 8, cx + 9, cy + 8], 190, 350, fill=(200, 140, 255, 255))
    
    # Tri-Spectrum Central Sensor Eye
    d.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(10, 8, 18, 255), outline=(0, 240, 255, 255))
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 80, 160, 255))
    put_pixel(im, cx, cy, (255, 255, 255, 255))
    
    # Top Dimensional Anchor Eyelet & Antenna Array
    d.ellipse([cx - 3, 2, cx + 3, 7], outline=(255, 215, 80, 255))
    d.line([(cx - 7, 6), (cx - 7, 2)], fill=(0, 240, 255, 240))
    d.line([(cx + 7, 6), (cx + 7, 2)], fill=(0, 240, 255, 240))
    
    # Dual Lateral Ion Maneuvering Thrusters
    d.rectangle([2, cy - 3, 5, cy + 3], fill=(255, 215, 80, 255))
    d.rectangle([25, cy - 3, 28, cy + 3], fill=(255, 215, 80, 255))
    return draw_border_and_glow(im)

# ===========================================================================
# 4. DEPTH ANCHOR (ÂNCORA DE PROFUNDIDADE)
# ===========================================================================
def create_depth_anchor_var_a(size=32):
    """Var A: Spacetime Gravity Stake / Spike (Barbed Mooring Peg)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    gold_hi = (255, 225, 100, 255)
    gold_dark = (140, 95, 25, 255)
    body_fill = (26, 16, 40, 255)
    
    # Top Gravitational Anvil Head & Ring
    d.ellipse([11, 2, 19, 8], fill=None, outline=gold_hi, width=1)
    d.rectangle([8, 7, 22, 11], fill=(45, 28, 65, 255), outline=gold_hi)
    # Compression rune mark in head
    d.line([(12, 9), (18, 9)], fill=(0, 240, 255, 255))
    
    # Stepped Barbed Shaft penetrating downward
    # Upper shaft
    d.polygon([(11, 11), (19, 11), (21, 16), (19, 17), (11, 17), (9, 16)], fill=body_fill, outline=gold_dark)
    # Middle barbed teeth
    d.polygon([(11, 17), (19, 17), (23, 22), (18, 23), (12, 23), (7, 22)], fill=body_fill, outline=gold_dark)
    # Lower penetration spike
    d.polygon([(12, 23), (18, 23), (15, 30)], fill=(0, 240, 255, 200), outline=gold_hi)
    put_pixel(im, 15, 30, (255, 255, 255, 255))
    
    # Glowing Spacetime Phase Channels along center line
    d.line([(15, 11), (15, 27)], fill=(0, 240, 255, 255), width=1)
    for ry in [13, 19, 25]:
        d.line([(13, ry), (17, ry)], fill=(180, 80, 255, 240))
        
    return draw_border_and_glow(im)

def create_depth_anchor_var_b(size=32):
    """Var B: Tethered Spatial Fluke Anchor (Nautical High-Tech)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    plat_hi = (220, 230, 255, 255)
    plat_mid = (130, 140, 170, 255)
    plat_dark = (60, 65, 85, 255)
    
    # Top Mooring Ring
    d.ellipse([12, 2, 18, 8], outline=plat_hi, width=1)
    
    # Central Shaft / Stock
    d.rectangle([13, 8, 17, 24], fill=(28, 20, 42, 255), outline=plat_mid)
    d.line([(14, 8), (14, 24)], fill=(0, 240, 255, 220)) # Energy Conduit
    
    # Cross Stock bar
    d.rectangle([7, 10, 23, 12], fill=plat_mid, outline=plat_dark)
    d.line([(7, 10), (23, 10)], fill=plat_hi)
    
    # Dual Swept Flukes (Curved heavy arms at bottom)
    d.arc([5, 15, 25, 29], 30, 150, fill=plat_mid, width=3)
    # Sharp Fluke Tips pointing upward
    d.polygon([(5, 18), (8, 22), (2, 20)], fill=(255, 215, 80, 255))
    d.polygon([(25, 18), (22, 22), (28, 20)], fill=(255, 215, 80, 255))
    
    # Bottom Crown
    d.polygon([(11, 24), (19, 24), (15, 29)], fill=(0, 240, 255, 255), outline=plat_hi)
    put_pixel(im, 15, 29, (255, 255, 255, 255))
    return draw_border_and_glow(im)

def create_depth_anchor_var_c(size=32):
    """Var C: Sub-Dimensional Resonant Pylon (Tripod Deployment)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Heavy Pylon Body
    d.rectangle([11, 4, 19, 22], fill=(22, 14, 34, 255), outline=(140, 70, 210, 255))
    # Glowing Depth Level Notch Rings
    d.line([(11, 8), (19, 8)], fill=(255, 215, 80, 255))   # Level 1
    d.line([(11, 12), (19, 12)], fill=(255, 160, 40, 255)) # Level 2
    d.line([(11, 16), (19, 16)], fill=(0, 240, 255, 255))  # Level 3
    d.line([(11, 20), (19, 20)], fill=(180, 80, 255, 255)) # Level 4
    
    # Central Core Crystal Window
    d.rectangle([13, 9, 17, 19], fill=(0, 240, 255, 220))
    put_pixel(im, 15, 14, (255, 255, 255, 255))
    
    # 3 Deployable Hydraulic Claw Feet
    d.line([(11, 22), (5, 29)], fill=(255, 215, 80, 255), width=2)
    d.line([(19, 22), (25, 29)], fill=(255, 215, 80, 255), width=2)
    d.line([(15, 22), (15, 30)], fill=(0, 240, 255, 255), width=2)
    put_pixel(im, 15, 30, (255, 255, 255, 255))
    
    # Top Cap
    d.polygon([(11, 4), (19, 4), (15, 1)], fill=(255, 215, 80, 255))
    return draw_border_and_glow(im)

# ===========================================================================
# 5. RIFT SINGULARITY (SINGULARIDADE DE FENDA)
# ===========================================================================
def create_rift_singularity_var_a(size=32):
    """Var A: Swirling Event Horizon Tear (Lensed Singularity)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 15, 15
    
    # Swirling Outer Gravitational Distortion Halo
    halo_colors = [
        (40, 15, 70, 90),
        (80, 25, 130, 140),
        (140, 45, 200, 180),
        (0, 240, 255, 220),
    ]
    for r in range(13, 7, -2):
        col = halo_colors[(13 - r) // 2]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=1)
        
    # Accretion Swirl Spiral Arms
    for angle_deg in range(0, 360, 45):
        rad = math.radians(angle_deg)
        for step in range(6):
            cur_r = 7 + step
            cur_ang = rad + step * 0.35
            px = int(cx + cur_r * math.cos(cur_ang))
            py = int(cy + cur_r * math.sin(cur_ang))
            col = (255, 215, 80, 240) if step % 2 == 0 else (0, 240, 255, 220)
            put_pixel(im, px, py, col)
            
    # Relativistic Photon Ring
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=(255, 255, 255, 255), width=1)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(0, 240, 255, 240), width=1)
    
    # Absolute Void Horizon Core (Pure Black Hole Kernel)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(4, 2, 8, 255))
    
    # Escaping Hawking Micro-Sparks
    sparks = [(cx - 9, cy - 8), (cx + 10, cy - 7), (cx + 8, cy + 9), (cx - 10, cy + 8)]
    for sx, sy in sparks:
        put_pixel(im, sx, sy, (255, 255, 255, 255))
        
    return draw_border_and_glow(im)

def create_rift_singularity_var_b(size=32):
    """Var B: Caged Hypercube Tesseract (Magnetic Containment Lattice)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 15, 15
    
    gold_hi = (255, 225, 90, 255)
    gold_dark = (140, 95, 20, 255)
    
    # Outer Tesseract Cube Box
    d.rectangle([5, 5, 25, 25], outline=gold_dark, width=1)
    d.line([(5, 5), (25, 5)], fill=gold_hi)
    d.line([(5, 5), (5, 25)], fill=gold_hi)
    
    # Inner Projected Cube
    d.rectangle([10, 10, 20, 20], outline=(0, 240, 255, 220), width=1)
    
    # Connecting 4D Projection Lines
    d.line([(5, 5), (10, 10)], fill=gold_hi)
    d.line([(25, 5), (20, 10)], fill=gold_hi)
    d.line([(5, 25), (10, 20)], fill=gold_dark)
    d.line([(25, 25), (20, 20)], fill=gold_dark)
    
    # Trapped Reality Fracture inside Inner Cube
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(16, 6, 28, 255), outline=(255, 80, 160, 255))
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255, 255))
    put_pixel(im, cx, cy, (4, 2, 8, 255)) # Micro black center
    return draw_border_and_glow(im)

def create_rift_singularity_var_c(size=32):
    """Var C: Cosmic Eye of the Void (Elliptical Spacetime Rip)."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy = 15, 15
    
    # Diagonal Elliptical Slit (Cosmic Eye)
    # Violent Coronal Plasma Flare
    for r in range(12, 5, -2):
        d.arc([cx - r - 2, cy - r, cx + r + 2, cy + r], 0, 360, fill=(180, 60, 240, 140))
        
    # Pupil Contour
    d.polygon([(cx - 10, cy), (cx, cy - 7), (cx + 10, cy), (cx, cy + 7)],
              fill=(8, 4, 16, 255), outline=(255, 215, 80, 255))
    # Inner Coronal rim
    d.polygon([(cx - 7, cy), (cx, cy - 4), (cx + 7, cy), (cx, cy + 4)],
              fill=(0, 0, 0, 255), outline=(0, 240, 255, 240))
              
    # Absolute Void Pupil Center
    d.line([(cx - 4, cy), (cx + 4, cy)], fill=(255, 255, 255, 255), width=1)
    put_pixel(im, cx, cy, (0, 240, 255, 255))
    
    # Dimensional Discharge Lightning Arcs
    d.line([(cx - 10, cy), (cx - 13, cy - 3)], fill=(0, 240, 255, 255))
    d.line([(cx + 10, cy), (cx + 13, cy + 3)], fill=(0, 240, 255, 255))
    d.line([(cx, cy - 7), (cx + 2, cy - 11)], fill=(255, 215, 80, 255))
    d.line([(cx, cy + 7), (cx - 2, cy + 11)], fill=(255, 215, 80, 255))
    return draw_border_and_glow(im)

# ===========================================================================
# PREVIEW CARD COMPOSITOR (128x128 & COMPARISON SHEETS)
# ===========================================================================
def compose_item_card(im32, name, var_id, desc, tags):
    """Create a 210x246 dark preview card showing the item scaled up 4x with details."""
    card = Image.new('RGBA', (210, 246), (16, 12, 24, 255))
    d = ImageDraw.Draw(card)
    
    # Outer Card Border
    d.rectangle([0, 0, 209, 245], outline=(65, 40, 95, 255), width=2)
    d.rectangle([2, 2, 207, 26], fill=(26, 18, 38, 255))
    d.text((10, 6), f"VARIAÇÃO {var_id}", fill=(255, 215, 80, 255), font=FONT_TITLE)
    
    # Item Display Box (128x128 area)
    box_x, box_y = 41, 34
    d.rectangle([box_x - 1, box_y - 1, box_x + 128, box_y + 128], fill=(8, 6, 14, 255), outline=(50, 35, 75, 255))
    
    # Checkerboard background for transparency
    for cy in range(0, 128, 16):
        for cx in range(0, 128, 16):
            if ((cx // 16) + (cy // 16)) % 2 == 1:
                d.rectangle([box_x + cx, box_y + cy, box_x + cx + 15, box_y + cy + 15], fill=(14, 10, 22, 255))
                
    # Scale up item 4x (32 -> 128) using Nearest Neighbor
    im128 = im32.resize((128, 128), Image.NEAREST)
    card.alpha_composite(im128, (box_x, box_y))
    
    # Item Name
    d.text((10, 172), name, fill=(255, 255, 255, 255), font=FONT_TITLE)
    # Description
    d.text((10, 192), desc, fill=(180, 190, 215, 255), font=FONT_MICRO)
    # Tags / Lore
    d.text((10, 210), tags, fill=(0, 240, 255, 255), font=FONT_MICRO)
    d.text((10, 226), "Pixel Art: 32x32 & 16x16 HD", fill=(140, 150, 170, 255), font=FONT_MICRO)
    return card

def create_comparison_sheet(title, subtitle, cards, out_path):
    card_w, card_h = 210, 246
    n = len(cards)
    gap = 16
    total_w = max(780, gap * (n + 1) + card_w * n)
    header_h = 68
    total_h = header_h + card_h + gap * 2
    
    sheet = Image.new('RGBA', (total_w, total_h), (12, 8, 18, 255))
    d = ImageDraw.Draw(sheet)
    
    # Header Banner
    d.rectangle([0, 0, total_w, header_h], fill=(22, 14, 34, 255), outline=(75, 45, 105, 255), width=2)
    d.text((24, 14), title, fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((24, 40), subtitle, fill=(180, 190, 215, 255), font=FONT_SUB)
    
    start_x = (total_w - (n * card_w + (n - 1) * gap)) // 2
    for idx, card in enumerate(cards):
        cx = start_x + idx * (card_w + gap)
        cy = header_h + gap
        sheet.alpha_composite(card, (cx, cy))
        
    sheet.save(out_path)
    print(f"[OK] Comparison sheet saved to: {out_path}")

def main():
    print(">>> Gerando Propostas de Design para os Itens do GTNA Endgame...")
    
    # -----------------------------------------------------------------------
    # 1. Target Cartridge
    # -----------------------------------------------------------------------
    print("  -> Criando variações para Target Cartridge...")
    tc_a = create_target_cartridge_var_a(32)
    tc_b = create_target_cartridge_var_b(32)
    tc_c = create_target_cartridge_var_c(32)
    
    p = os.path.join(PROPOSALS_DIR, 'target_cartridge')
    tc_a.save(os.path.join(p, '32x32', 'target_cartridge_var_a.png'))
    tc_b.save(os.path.join(p, '32x32', 'target_cartridge_var_b.png'))
    tc_c.save(os.path.join(p, '32x32', 'target_cartridge_var_c.png'))
    
    tc_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'target_cartridge_var_a.png'))
    tc_b.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'target_cartridge_var_b.png'))
    tc_c.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'target_cartridge_var_c.png'))
    
    card_tc_a = compose_item_card(tc_a, "Cartucho Óptico Cósmico", "1", "Cristal hexagonal & retículo ouro", "Tema: Godforge Cosmic Purple")
    card_tc_b = compose_item_card(tc_b, "ROM Tática Aeroespacial", "2", "Carcaça militar & LEDs de mira", "Tema: Blindagem Tungstênio-Aço")
    card_tc_c = compose_item_card(tc_c, "Domo Astrométrico Holo", "3", "Miniatura 3D do corpo celeste", "Tema: Radiant Naquadah & Vidro")
    
    create_comparison_sheet(
        "GTNA · PROPOSTAS DE DESIGN: CARTUCHO DE ALVO (TARGET CARTRIDGE)",
        "Item da Lança Cinética Orbital [UEV] · Define corpo celeste, efemérides e rotação AE2",
        [card_tc_a, card_tc_b, card_tc_c],
        os.path.join(p, 'previews', 'comparison_target_cartridge.png')
    )

    # -----------------------------------------------------------------------
    # 2. Contained Particles
    # -----------------------------------------------------------------------
    print("  -> Criando variações para Contained Particles (Penning Traps)...")
    cp_higgs_a = create_contained_particle('higgs', 'a', 32)
    cp_antiproton_a = create_contained_particle('antiproton', 'a', 32)
    cp_qgp_a = create_contained_particle('qgp', 'a', 32)
    cp_lambda_a = create_contained_particle('lambda', 'a', 32)
    
    cp_higgs_b = create_contained_particle('higgs', 'b', 32)
    cp_higgs_c = create_contained_particle('higgs', 'c', 32)
    
    p = os.path.join(PROPOSALS_DIR, 'contained_particles')
    cp_higgs_a.save(os.path.join(p, '32x32', 'contained_higgs_var_a.png'))
    cp_antiproton_a.save(os.path.join(p, '32x32', 'contained_antiproton_var_a.png'))
    cp_qgp_a.save(os.path.join(p, '32x32', 'contained_qgp_var_a.png'))
    cp_lambda_a.save(os.path.join(p, '32x32', 'contained_lambda_var_a.png'))
    cp_higgs_b.save(os.path.join(p, '32x32', 'contained_higgs_var_b.png'))
    cp_higgs_c.save(os.path.join(p, '32x32', 'contained_higgs_var_c.png'))
    
    cp_higgs_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'contained_higgs_var_a.png'))
    cp_antiproton_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'contained_antiproton_var_a.png'))
    cp_qgp_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'contained_qgp_var_a.png'))
    cp_lambda_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'contained_lambda_var_a.png'))
    
    card_cp_a = compose_item_card(cp_higgs_a, "Célula Penning Quadrupolo", "1", "Tubo borossilicato & bobinas ouro", "Partícula: Bóson de Higgs (125 GeV)")
    card_cp_anti = compose_item_card(cp_antiproton_a, "Célula Penning Antimatéria", "1B", "Confinamento B=18.5T criogênico", "Partícula: Antiprótons (938 MeV)")
    card_cp_qgp = compose_item_card(cp_qgp_a, "Célula Penning QGP", "1C", "Fluido de Quarks & Glúons 5 TeV", "Partícula: QGP Relativístico")
    card_cp_b = compose_item_card(cp_higgs_b, "Monólito Hexagonal Blindado", "2", "Neutrônio maciço & parafusos ouro", "Proteção extrema contra vazamento")
    card_cp_c = compose_item_card(cp_higgs_c, "Frasco Trirradial em Levitação", "3", "3 garras magnéticas em suspensão", "Alta mobilidade para rede Nexus")
    
    create_comparison_sheet(
        "GTNA · PROPOSTAS DE DESIGN: PARTÍCULAS CONTIDAS (CONTAINED PARTICLES)",
        "Itens do Anel Colisor [UIV] · Armadilhas de Penning portáteis contendo produtos de alta energia",
        [card_cp_a, card_cp_anti, card_cp_qgp, card_cp_b, card_cp_c],
        os.path.join(p, 'previews', 'comparison_contained_particles.png')
    )

    # -----------------------------------------------------------------------
    # 3. Rift Probe
    # -----------------------------------------------------------------------
    print("  -> Criando variações para Rift Probe...")
    rp_a = create_rift_probe_var_a(32)
    rp_b = create_rift_probe_var_b(32)
    rp_c = create_rift_probe_var_c(32)
    
    p = os.path.join(PROPOSALS_DIR, 'rift_probe')
    rp_a.save(os.path.join(p, '32x32', 'rift_probe_var_a.png'))
    rp_b.save(os.path.join(p, '32x32', 'rift_probe_var_b.png'))
    rp_c.save(os.path.join(p, '32x32', 'rift_probe_var_c.png'))
    
    rp_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_probe_var_a.png'))
    rp_b.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_probe_var_b.png'))
    rp_c.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_probe_var_c.png'))
    
    card_rp_a = compose_item_card(rp_a, "Dardo de Agulha Táquion", "1", "Agulha sub-espacial & 4 asas de fase", "Estreita tolerâncias sigma em 20%")
    card_rp_b = compose_item_card(rp_b, "Astrolábio Octaédrico", "2", "Anéis giroscópicos & cristal central", "Ressonador harmônico para 8 pilones")
    card_rp_c = compose_item_card(rp_c, "Batiscafo do Vazio", "3", "Domo esférico & olho multi-espectral", "Blindagem térmica para fendas profundas")
    
    create_comparison_sheet(
        "GTNA · PROPOSTAS DE DESIGN: SONDA DE FENDA (RIFT PROBE)",
        "Item do Portão de Fenda [UIV] · Lançada na fenda para sintonizar a frequência ótima",
        [card_rp_a, card_rp_b, card_rp_c],
        os.path.join(p, 'previews', 'comparison_rift_probe.png')
    )

    # -----------------------------------------------------------------------
    # 4. Depth Anchor
    # -----------------------------------------------------------------------
    print("  -> Criando variações para Depth Anchor...")
    da_a = create_depth_anchor_var_a(32)
    da_b = create_depth_anchor_var_b(32)
    da_c = create_depth_anchor_var_c(32)
    
    p = os.path.join(PROPOSALS_DIR, 'depth_anchor')
    da_a.save(os.path.join(p, '32x32', 'depth_anchor_var_a.png'))
    da_b.save(os.path.join(p, '32x32', 'depth_anchor_var_b.png'))
    da_c.save(os.path.join(p, '32x32', 'depth_anchor_var_c.png'))
    
    da_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'depth_anchor_var_a.png'))
    da_b.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'depth_anchor_var_b.png'))
    da_c.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'depth_anchor_var_c.png'))
    
    card_da_a = compose_item_card(da_a, "Estaca Gravitacional Farpada", "1", "Dentes de fixação & runa de fase", "Aprofunda D e libera camadas do bioma")
    card_da_b = compose_item_card(da_b, "Âncora Náutica Espacial", "2", "Braços duplos curvados & elo táquion", "Fixação robusta contra colapso")
    card_da_c = compose_item_card(da_c, "Pilone Tripé de Fixação", "3", "Garras hidráulicas & anéis de nível", "Indicador visual de profundidade I..XX")
    
    create_comparison_sheet(
        "GTNA · PROPOSTAS DE DESIGN: ÂNCORA DE PROFUNDIDADE (DEPTH ANCHOR)",
        "Item do Portão de Fenda [UIV] · Consumível que ancora a fenda nas camadas mais ricas (D^1.5)",
        [card_da_a, card_da_b, card_da_c],
        os.path.join(p, 'previews', 'comparison_depth_anchor.png')
    )

    # -----------------------------------------------------------------------
    # 5. Rift Singularity
    # -----------------------------------------------------------------------
    print("  -> Criando variações para Rift Singularity...")
    rs_a = create_rift_singularity_var_a(32)
    rs_b = create_rift_singularity_var_b(32)
    rs_c = create_rift_singularity_var_c(32)
    
    p = os.path.join(PROPOSALS_DIR, 'rift_singularity')
    rs_a.save(os.path.join(p, '32x32', 'rift_singularity_var_a.png'))
    rs_b.save(os.path.join(p, '32x32', 'rift_singularity_var_b.png'))
    rs_c.save(os.path.join(p, '32x32', 'rift_singularity_var_c.png'))
    
    rs_a.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_singularity_var_a.png'))
    rs_b.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_singularity_var_b.png'))
    rs_c.resize((16, 16), Image.BOX).save(os.path.join(p, '16x16', 'rift_singularity_var_c.png'))
    
    card_rs_a = compose_item_card(rs_a, "Vórtice do Horizonte de Eventos", "1", "Buraco negro micro & lente gravitacional", "Gotícula pura de espaço-tempo fraturado")
    card_rs_b = compose_item_card(rs_b, "Tesseract Confinado 4D", "2", "Hipercubo ouro/ciano contendo o rasgo", "Gaiola geométrica de alta estabilidade")
    card_rs_c = compose_item_card(rs_c, "Olho Cósmico do Vazio", "3", "Fenda elíptica com arcos coronais", "Emissão violenta de radiação exótica")
    
    create_comparison_sheet(
        "GTNA · PROPOSTAS DE DESIGN: SINGULARIDADE DE FENDA (RIFT SINGULARITY)",
        "Item Raro do Portão de Fenda [UIV] · Drop de 5%/min em Ressonância em Cascata (R >= 0.98)",
        [card_rs_a, card_rs_b, card_rs_c],
        os.path.join(p, 'previews', 'comparison_rift_singularity.png')
    )

    # -----------------------------------------------------------------------
    # MASTER SHOWCASE OF ALL 5 ITEMS
    # -----------------------------------------------------------------------
    print("  -> Montando Galeria Master dos 5 Itens...")
    master_w = 1160
    master_h = 1680
    master = Image.new('RGBA', (master_w, master_h), (12, 8, 18, 255))
    d = ImageDraw.Draw(master)
    
    # Master Header
    d.rectangle([0, 0, master_w, 75], fill=(24, 15, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 16), "GTNA · GALERIA DE PROPOSTAS DE DESIGN DE ITENS ENDGAME", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 44), "Pixel Art 32x32 & 16x16 HD · Padrão Estético Godforge Cosmic Purple, Aeroespacial & Alta Energia", fill=(180, 190, 215, 255), font=FONT_SUB)
    
    # 5 Rows for the 5 categories
    item_rows = [
        ("1. CARTUCHOS DE ALVO (TARGET CARTRIDGES) — LANÇA CINÉTICA [UEV]", [card_tc_a, card_tc_b, card_tc_c]),
        ("2. PARTÍCULAS CONTIDAS (PENNING TRAPS) — ANEL COLISOR [UIV]", [card_cp_a, card_cp_anti, card_cp_qgp, card_cp_b, card_cp_c]),
        ("3. SONDA DE FENDA (RIFT PROBE) — PORTÃO DE FENDA [UIV]", [card_rp_a, card_rp_b, card_rp_c]),
        ("4. ÂNCORA DE PROFUNDIDADE (DEPTH ANCHOR) — PORTÃO DE FENDA [UIV]", [card_da_a, card_da_b, card_da_c]),
        ("5. SINGULARIDADE DE FENDA (RIFT SINGULARITY) — PORTÃO DE FENDA [UIV]", [card_rs_a, card_rs_b, card_rs_c]),
    ]
    
    cur_y = 85
    for row_title, cards in item_rows:
        d.rectangle([15, cur_y, master_w - 15, cur_y + 24], fill=(20, 12, 30, 255), outline=(65, 40, 90, 255))
        d.text((25, cur_y + 4), row_title, fill=(255, 215, 80, 255), font=FONT_TITLE)
        cur_y += 30
        
        # Draw cards centered or spaced
        card_gap = 14
        total_row_w = len(cards) * 210 + (len(cards) - 1) * card_gap
        start_x = (master_w - total_row_w) // 2
        for c_idx, card in enumerate(cards):
            cx = start_x + c_idx * (card.width + card_gap)
            master.alpha_composite(card, (cx, cur_y))
        cur_y += 246 + 18
        
    master_path = os.path.join(PROPOSALS_DIR, 'all_items_master_showcase.png')
    master.save(master_path)
    print(f"[OK] Master Items Showcase salvo em: {master_path}")

if __name__ == '__main__':
    main()
