#!/usr/bin/env python3
"""Generate High-Definition 64x64 (HD) Item Textures & Showcases for GTNA Endgame:
  1. Target Cartridge (Cartucho de Alvo - Lança Cinética Orbital):
     - Var 1: Cartucho de Memória Tática Orbital (Tactical Military ROM)
     - Var 2: Cartucho Óptico Quântico de Coordenadas (Cosmic Optical Lens / Godforge Gold)
     - Var 3: Cartucho Holo-Domo de Astrometria (Astrometric Holo-Core / Data Crystal)
     - Bonus: All 8 target body cartridges (Moon, Phobos, Vesta, Ceres, Psyche, Europa, Arrokoth, Nexus-1)
  2. Contained Particles (Armadilhas de Penning - Anel Colisor de Antimatéria):
     - High-detail 64x64 Penning Traps for all 10 ColliderCore particles:
       Antiproton, Kaon, Lambda, Charm, Bottom, W-Boson, Z-Boson, Higgs, Top, X-Nexus
     - Bonus: Antiproton Penning Cell (Superconducting Cryogenic Cell)
  3. Rift Probe (Sonda de Fenda - Portão de Fenda Dimensional):
     - Var 1: Agulha de Táctons Quântica (Tachyon Quantum Needle)
     - Var 2: Astrolábio Octaédrico Dimensional (Dimensional Octahedral Astrolabe)
     - Var 3: Batíscafo de Vácuo Profundo (Deep Void Bathyscaphe)
  4. Depth Anchor (Âncora de Profundidade - Portão de Fenda Dimensional):
     - Var 1: Estaca Gravitacional de Singularidade (Gravitational Singularity Stake)
     - Var 2: Âncora de Fenda Fluke (Dimensional Fluke Anchor)
     - Var 3: Pilone Trípode de Fixação Subespacial (Subspace Tripod Pylon)
  5. Rift Singularity (Singularidade de Fenda - Portão de Fenda Dimensional):
     - Var 1: Horizonte de Eventos Vórtice de Fenda (Swirling Event Horizon)
     - Var 2: Hipercubo Tesseract 4D (4D Tesseract Core)
     - Var 3: Olho do Vazio Cósmico (Cosmic Void Eye)

Outputs to: tools/design/item_proposals/<category>/64x64/ and previews.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(BASE_DIR, 'item_proposals')

CATEGORIES = ['target_cartridge', 'contained_particles', 'rift_probe', 'depth_anchor', 'rift_singularity']
for cat in CATEGORIES:
    os.makedirs(os.path.join(PROPOSALS_DIR, cat, '64x64'), exist_ok=True)
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

def apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=None, glow_radius=2):
    """Adds a clean outer shadow/outline and optional bloom glow to the item."""
    w, h = im.size
    glow_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if glow_col is not None:
        gd = ImageDraw.Draw(glow_layer)
        for y in range(h):
            for x in range(w):
                if im.getpixel((x, y))[3] > 60:
                    for dx in range(-glow_radius, glow_radius + 1):
                        for dy in range(-glow_radius, glow_radius + 1):
                            dist = math.sqrt(dx*dx + dy*dy)
                            if 0 < dist <= glow_radius:
                                nx, ny = x + dx, y + dy
                                if 0 <= nx < w and 0 <= ny < h and im.getpixel((nx, ny))[3] <= 40:
                                    alpha = int(glow_col[3] * (1.0 - dist / (glow_radius + 0.5)))
                                    cur = glow_layer.getpixel((nx, ny))
                                    if alpha > cur[3]:
                                        glow_layer.putpixel((nx, ny), (glow_col[0], glow_col[1], glow_col[2], alpha))
    
    outline_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            if im.getpixel((x, y))[3] > 40:
                for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and im.getpixel((nx, ny))[3] <= 20:
                        outline_layer.putpixel((nx, ny), outline_col)
                        
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if glow_col is not None:
        out.alpha_composite(glow_layer)
    out.alpha_composite(outline_layer)
    out.alpha_composite(im)
    return out

# ===========================================================================
# 1. TARGET CARTRIDGE (64x64 HD)
# ===========================================================================

def generate_cartridge_var1_tactical_rom(size=64):
    """Var 1: Cartucho de Memória Tática Orbital (Tactical ROM Cartridge).
    Heavy reinforced titanium/tungsten case, gold edge connector bus, status LEDs, targeting reticle."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Outer casing bounds: x from 12 to 51, y from 8 to 56
    # Chamfered upper corners
    casing_pts = [(18, 8), (45, 8), (51, 14), (51, 54), (12, 54), (12, 14)]
    d.polygon(casing_pts, fill=(30, 24, 42, 255), outline=(75, 55, 95, 255))
    
    # Metallic shading gradient across casing
    for y in range(9, 54):
        shade = int(28 + (y - 9) * 0.4)
        d.line([(13, y), (50, y)], fill=(shade, shade - 6, shade + 10, 255))
        
    # Bevel highlights
    d.line([(18, 8), (45, 8)], fill=(160, 140, 200, 255), width=1)
    d.line([(12, 14), (18, 8)], fill=(160, 140, 200, 255), width=1)
    d.line([(12, 14), (12, 53)], fill=(140, 120, 180, 255), width=1)
    d.line([(51, 14), (51, 54)], fill=(20, 15, 30, 255), width=1)
    d.line([(12, 54), (51, 54)], fill=(20, 15, 30, 255), width=1)
    
    # Gold PCB Connector Pins at bottom
    for px in range(16, 48, 4):
        d.rectangle([px, 54, px + 2, 59], fill=(255, 215, 80, 255), outline=(160, 110, 25, 255))
        d.line([(px, 54), (px, 59)], fill=(255, 240, 160, 255))
        
    # Recessed Display / Targeting Matrix Window
    d.rectangle([18, 16, 45, 42], fill=(10, 8, 18, 255), outline=(90, 60, 130, 255), width=1)
    d.rectangle([19, 17, 44, 41], fill=(16, 12, 26, 255))
    
    # Grid lines inside screen
    for gy in range(20, 41, 5):
        d.line([(20, gy), (43, gy)], fill=(35, 25, 55, 255))
    for gx in range(23, 44, 5):
        d.line([(gx, 18), (gx, 40)], fill=(35, 25, 55, 255))
        
    # Holographic Targeting Reticle (Cyan & Gold)
    rcx, rcy = 31, 29
    d.ellipse([rcx - 8, rcy - 8, rcx + 8, rcy + 8], outline=(0, 240, 255, 200), width=1)
    d.ellipse([rcx - 4, rcy - 4, rcx + 4, rcy + 4], outline=(255, 215, 80, 240), width=1)
    d.ellipse([rcx - 1, rcy - 1, rcx + 1, rcy + 1], fill=(255, 255, 255, 255))
    d.line([(rcx - 10, rcy), (rcx - 5, rcy)], fill=(0, 240, 255, 255))
    d.line([(rcx + 5, rcy), (rcx + 10, rcy)], fill=(0, 240, 255, 255))
    d.line([(rcx, rcy - 10), (rcx, rcy - 5)], fill=(0, 240, 255, 255))
    d.line([(rcx, rcy + 5), (rcx, rcy + 10)], fill=(0, 240, 255, 255))
    
    # Status LED cluster on right
    led_colors = [(80, 255, 140), (0, 240, 255), (255, 215, 80)]
    for i, col in enumerate(led_colors):
        d.rectangle([47, 20 + i * 8, 49, 23 + i * 8], fill=col + (255,), outline=(255, 255, 255, 255))
        
    # Laser-etched ROM designation
    d.rectangle([20, 46, 43, 50], fill=(22, 16, 32, 255), outline=(50, 35, 75, 255))
    d.line([(22, 48), (41, 48)], fill=(120, 100, 160, 255))
    
    return apply_glow_and_outline(im, outline_col=(14, 10, 20, 255), glow_col=(0, 220, 255, 80))

def generate_cartridge_var2_cosmic_optical(size=64, body_color=(255, 215, 80), body_symbol="MOON"):
    """Var 2: Cartucho Óptico Quântico de Coordenadas (Cosmic Optical Lens / Godforge Gold).
    Radiant Naquadah Gold frame, deep cosmic purple casing, hexagonal optical lens with celestial prism."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Frame points (Octagonal tech profile)
    frame_pts = [(20, 6), (43, 6), (53, 16), (53, 49), (46, 56), (17, 56), (10, 49), (10, 16)]
    d.polygon(frame_pts, fill=(24, 14, 38, 255), outline=(180, 130, 40, 255))
    
    # Inner gold border bevel
    inner_gold = [(21, 8), (42, 8), (51, 17), (51, 48), (45, 54), (18, 54), (12, 48), (12, 17)]
    d.polygon(inner_gold, outline=(255, 225, 100, 255), width=2)
    
    # Deep royal purple plate
    d.polygon([(22, 10), (41, 10), (49, 18), (49, 46), (43, 52), (20, 52), (14, 46), (14, 18)],
              fill=(38, 20, 60, 255))
              
    # Gold Connector Teeth at bottom
    for px in [19, 24, 29, 34, 39, 44]:
        d.rectangle([px, 55, px + 2, 60], fill=(255, 220, 90, 255), outline=(130, 90, 20, 255))
        d.line([(px, 55), (px, 60)], fill=(255, 255, 180, 255))
        
    # Central Hexagonal Optical Prism Lens
    lcx, lcy = 31, 30
    lr = 15
    hex_pts = []
    for a in range(6):
        rad = math.radians(a * 60 - 30)
        hex_pts.append((int(lcx + math.cos(rad) * lr), int(lcy + math.sin(rad) * lr)))
    d.polygon(hex_pts, fill=(10, 5, 20, 255), outline=(255, 215, 80, 255), width=2)
    
    # Lens Glass Gradient (Multi-radial cyan to magenta)
    for r_step in range(lr - 2, 0, -2):
        frac = r_step / (lr - 2)
        col = (int(body_color[0] * (1 - frac) + 20 * frac),
               int(body_color[1] * (1 - frac) + 180 * frac),
               int(body_color[2] * (1 - frac) + 255 * frac), 255)
        sub_pts = []
        for a in range(6):
            rad = math.radians(a * 60 - 30)
            sub_pts.append((int(lcx + math.cos(rad) * r_step), int(lcy + math.sin(rad) * r_step)))
        d.polygon(sub_pts, fill=col)
        
    # Diagonal Specular Glass Reflection
    d.line([(lcx - 10, lcy - 8), (lcx + 4, lcy - 12)], fill=(255, 255, 255, 200), width=2)
    d.line([(lcx - 6, lcy + 8), (lcx + 8, lcy + 2)], fill=(255, 255, 255, 140), width=1)
    
    # Center Quantum Focal Core (Glow)
    d.ellipse([lcx - 4, lcy - 4, lcx + 4, lcy + 4], fill=(255, 255, 255, 255), outline=body_color + (255,))
    
    # Arcane Data Glyphs around lens
    for a in range(4):
        ang = math.radians(a * 90 + 45)
        gx = int(lcx + math.cos(ang) * 19)
        gy = int(lcy + math.sin(ang) * 19)
        d.rectangle([gx - 1, gy - 1, gx + 1, gy + 1], fill=(255, 215, 80, 255))
        
    return apply_glow_and_outline(im, outline_col=(18, 10, 28, 255), glow_col=body_color + (100,))

def generate_cartridge_var3_holo_dome(size=64):
    """Var 3: Cartucho Holo-Domo de Astrometria (Astrometric Holo-Core / Data Crystal).
    Translucent cyber-glass housing with spherical astrometric holo-dome showing planetary orbits."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Base Chassis
    d.polygon([(14, 20), (50, 20), (54, 26), (54, 54), (10, 54), (10, 26)], fill=(26, 20, 38, 255), outline=(90, 70, 120, 255))
    
    # Metallic Base Shading
    for y in range(21, 54):
        val = int(24 + (y - 21) * 0.5)
        d.line([(11, y), (53, y)], fill=(val, val - 4, val + 12, 255))
        
    # Gold Connector at base
    for px in range(15, 48, 5):
        d.rectangle([px, 54, px + 3, 59], fill=(255, 215, 80, 255), outline=(140, 100, 25, 255))
        
    # Glass Cylindrical Holo-Dome (Upper portion)
    dome_cx, dome_cy = 32, 24
    dome_r = 18
    # Outer dome arc
    d.ellipse([dome_cx - dome_r, dome_cy - dome_r + 4, dome_cx + dome_r, dome_cy + dome_r + 4],
              fill=(15, 10, 30, 220), outline=(0, 230, 255, 220), width=2)
              
    # Translucent Glass Highlight
    d.arc([dome_cx - dome_r + 2, dome_cy - dome_r + 6, dome_cx + dome_r - 2, dome_cy + dome_r + 2],
          start=190, end=350, fill=(255, 255, 255, 200), width=2)
          
    # 3D Orbital Rings inside Holo-Dome (Cyan & Neon Violet)
    d.ellipse([dome_cx - 13, dome_cy - 4, dome_cx + 13, dome_cy + 12], outline=(0, 240, 255, 220), width=1)
    d.ellipse([dome_cx - 9, dome_cy - 7, dome_cx + 9, dome_cy + 15], outline=(180, 80, 255, 200), width=1)
    
    # Central Celestial Body (Glowing Emerald or Gold Sphere)
    d.ellipse([dome_cx - 4, dome_cy + 2, dome_cx + 4, dome_cy + 8], fill=(255, 255, 255, 255), outline=(0, 255, 200, 255))
    
    # Orbiting Target Satellite
    d.rectangle([dome_cx + 10, dome_cy + 1, dome_cx + 12, dome_cy + 3], fill=(255, 215, 80, 255))
    
    # Micro circuit bus in lower section
    d.rectangle([16, 38, 48, 48], fill=(12, 8, 20, 255), outline=(60, 45, 85, 255))
    for cx in range(19, 47, 4):
        d.line([(cx, 40), (cx, 46)], fill=(0, 240, 255, 180))
        
    return apply_glow_and_outline(im, outline_col=(15, 10, 22, 255), glow_col=(0, 230, 255, 90))

# Target Cartridges for the 8 Celestial Bodies (LanceCore.Body)
BODY_DATA = [
    ("moon", "Lua", (220, 225, 235), "Luna / Fe-Ti"),
    ("phobos", "Fobos", (180, 140, 120), "Carbonáceo / C-Ni"),
    ("vesta", "Vesta", (210, 180, 110), "Basáltico / Mg-Pt"),
    ("ceres", "Ceres", (160, 200, 210), "Gelo & Sais / Na-NH3"),
    ("psyche", "Psique", (230, 200, 90), "Núcleo Metálico / Ir-Os-Au"),
    ("europa", "Europa", (140, 230, 255), "Oceano Subsuperfície / D-S"),
    ("arrokoth", "Arrokoth", (215, 110, 90), "Tholin Kuiper / CH4-N"),
    ("nexus_1", "Nexus-1", (180, 80, 255), "Singularidade / Spacetime"),
]

# ===========================================================================
# 2. CONTAINED PARTICLES & PENNING CELLS (64x64 HD)
# ===========================================================================

PARTICLE_PROFILES = [
    ("antiproton", "Antipróton", "5.6 GeV", (0, 240, 255), "Aniquilação Antimatéria"),
    ("kaon", "Káon", "1.0 GeV", (190, 80, 255), "Méson Estranho (s-d)"),
    ("lambda", "Lambda", "2.5 GeV", (80, 255, 140), "Bárion Estranho (uds)"),
    ("charm", "Charm", "10.0 GeV", (255, 200, 50), "Méson Encantado (c-c)"),
    ("bottom", "Bottom", "40.0 GeV", (255, 60, 100), "Quark Beauty (b-b)"),
    ("w_boson", "Bóson W", "161 GeV", (50, 160, 255), "Bóson Vetorial Carregado"),
    ("z_boson", "Bóson Z", "182 GeV", (220, 235, 255), "Bóson Vetorial Neutro"),
    ("higgs", "Bóson Higgs", "250 GeV", (255, 230, 80), "Bóson Escalar Fundamental"),
    ("top", "Quark Top", "346 GeV", (255, 140, 30), "Quark Mais Pesado (t)"),
    ("x_nexus", "X-Nexus", "4800 GeV", (170, 40, 255), "Grande Unificação GUT"),
]

def generate_penning_trap_64(p_col=(0, 240, 255), p_name="antiproton", is_dewar_cell=False):
    """Generate 64x64 HD Penning Trap Containment Capsule:
    - Superconducting magnetic endcap coils (top and bottom)
    - Quadrupole hyperbolic ring electrodes (center)
    - Ultra-clear cylindrical vacuum quartz tube with double reflections
    - Quantum particle trapped in central harmonic potential well."""
    im = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Bounds: tube x from 18 to 45, y from 8 to 55
    tx0, tx1 = 18, 45
    ty0, ty1 = 8, 55
    tcx = (tx0 + tx1) // 2
    
    # 1. Top Superconducting Endcap & Cryo Valve
    d.rectangle([tx0 - 2, ty0, tx1 + 2, ty0 + 7], fill=(50, 40, 65, 255), outline=(130, 105, 160, 255))
    d.line([(tx0 - 1, ty0), (tx1 + 1, ty0)], fill=(200, 180, 230, 255), width=1)
    # Pole piece tip (Upper electrode)
    d.polygon([(tcx - 6, ty0 + 7), (tcx + 6, ty0 + 7), (tcx + 3, ty0 + 13), (tcx - 3, ty0 + 13)],
              fill=(220, 180, 80, 255), outline=(140, 100, 30, 255))
              
    # 2. Bottom Superconducting Endcap & Terminals
    d.rectangle([tx0 - 2, ty1 - 7, tx1 + 2, ty1], fill=(50, 40, 65, 255), outline=(130, 105, 160, 255))
    d.line([(tx0 - 1, ty1 - 7), (tx1 + 1, ty1 - 7)], fill=(160, 140, 190, 255), width=1)
    d.line([(tx0 - 2, ty1), (tx1 + 2, ty1)], fill=(20, 15, 30, 255), width=1)
    # Pole piece tip (Lower electrode)
    d.polygon([(tcx - 3, ty1 - 13), (tcx + 3, ty1 - 13), (tcx + 6, ty1 - 7), (tcx - 6, ty1 - 7)],
              fill=(220, 180, 80, 255), outline=(140, 100, 30, 255))
              
    # Base Contact Prongs
    for px in [tx0 + 4, tcx - 1, tx1 - 5]:
        d.rectangle([px, ty1, px + 2, ty1 + 4], fill=(255, 215, 80, 255), outline=(140, 100, 20, 255))
        
    # 3. Transparent Vacuum Quartz Tube Cylinder
    d.rectangle([tx0, ty0 + 7, tx1, ty1 - 7], fill=(12, 8, 24, 180), outline=(80, 60, 110, 200))
    
    # 4. Central Quadrupole Ring Electrode (Hyperbolic Torus)
    mcy = 31
    d.ellipse([tx0 - 1, mcy - 6, tx0 + 7, mcy + 6], fill=(220, 180, 80, 255), outline=(150, 110, 30, 255))
    d.ellipse([tx1 - 7, mcy - 6, tx1 + 1, mcy + 6], fill=(220, 180, 80, 255), outline=(150, 110, 30, 255))
    d.line([(tx0 + 5, mcy), (tx1 - 5, mcy)], fill=(255, 215, 80, 80), width=1)
    
    # 5. Trapped Particle Quantum Core & Harmonic Potential Well
    # Outer Emission Halo
    for r_glow in range(12, 2, -2):
        alpha = int(140 * (1.0 - r_glow / 12.0))
        d.ellipse([tcx - r_glow, mcy - r_glow, tcx + r_glow, mcy + r_glow],
                  fill=p_col + (alpha,))
                  
    # Ionization / Orbital Sparkles
    for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle_deg)
        dist = 7 if (angle_deg % 90 == 0) else 5
        sx = int(tcx + math.cos(rad) * dist)
        sy = int(mcy + math.sin(rad) * dist)
        d.point((sx, sy), fill=(255, 255, 255, 230))
        
    # White-Hot Particle Center
    d.ellipse([tcx - 3, mcy - 3, tcx + 3, mcy + 3], fill=(255, 255, 255, 255), outline=p_col + (255,))
    
    # 6. Specular Reflections on Quartz Tube (Glass Bevel)
    # Left bright vertical streak
    d.line([(tx0 + 2, ty0 + 10), (tx0 + 2, ty1 - 10)], fill=(255, 255, 255, 160), width=1)
    d.line([(tx0 + 4, ty0 + 12), (tx0 + 4, ty1 - 12)], fill=(255, 255, 255, 80), width=1)
    # Right soft reflection
    d.line([(tx1 - 3, ty0 + 10), (tx1 - 3, ty1 - 10)], fill=(180, 210, 255, 90), width=1)
    
    # Special Dewar Cage for Antiproton Cell
    if is_dewar_cell:
        # Reinforced outer cryogenic exo-ribs
        for ry in [ty0 + 14, ty1 - 14]:
            d.line([(tx0 - 3, ry), (tx1 + 3, ry)], fill=(0, 240, 255, 255), width=2)
            d.line([(tx0 - 3, ry - 1), (tx1 + 3, ry - 1)], fill=(255, 255, 255, 200), width=1)
            
    return apply_glow_and_outline(im, outline_col=(16, 10, 25, 255), glow_col=p_col + (120,))

# ===========================================================================
# 3. RIFT PROBE (64x64 HD)
# ===========================================================================

def generate_rift_probe_var1_needle(size=64):
    """Var 1: Agulha de Táctons Quântica (Tachyon Quantum Needle).
    Needle-like chrono-probe with tachyon emitter needle tip, stabilization vanes, and glowing chronon core."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    # Oriented along diagonal: Tip at (52, 11), Base at (13, 50)
    # Central fuselage
    fuse_pts = [(45, 18), (49, 14), (52, 11), (49, 17), (25, 41), (18, 43), (13, 50), (20, 45), (22, 38)]
    
    # Main needle body
    d.line([(15, 48), (51, 12)], fill=(120, 100, 160, 255), width=5)
    d.line([(15, 48), (51, 12)], fill=(200, 190, 230, 255), width=3)
    d.line([(15, 48), (51, 12)], fill=(255, 255, 255, 255), width=1)
    
    # Needle Emitter Tip (Ultra-sharp tachyon spark)
    d.line([(48, 15), (55, 8)], fill=(0, 240, 255, 255), width=2)
    d.point((56, 7), fill=(255, 255, 255, 255))
    d.ellipse([51, 6, 57, 12], outline=(0, 240, 255, 200))
    
    # Central Stabilization Vanes (Delta wings)
    # Top-right vane
    d.polygon([(34, 29), (42, 21), (38, 17), (30, 25)], fill=(45, 30, 70, 255), outline=(255, 215, 80, 255))
    # Bottom-left vane
    d.polygon([(29, 34), (21, 42), (17, 38), (25, 30)], fill=(45, 30, 70, 255), outline=(255, 215, 80, 255))
    
    # Glowing Chronon Core in the center
    ccx, ccy = 32, 31
    d.ellipse([ccx - 5, ccy - 5, ccx + 5, ccy + 5], fill=(0, 240, 255, 240), outline=(255, 255, 255, 255))
    d.ellipse([ccx - 2, ccy - 2, ccx + 2, ccy + 2], fill=(255, 255, 255, 255))
    
    # Dimensional Stabilizer Fin & Thruster Bells
    d.polygon([(15, 48), (11, 44), (16, 39)], fill=(60, 45, 85, 255), outline=(140, 110, 190, 255))
    d.polygon([(15, 48), (19, 52), (24, 47)], fill=(60, 45, 85, 255), outline=(140, 110, 190, 255))
    
    # Ion Thruster Plumes
    d.line([(13, 50), (7, 56)], fill=(0, 240, 255, 255), width=2)
    d.point((6, 57), fill=(255, 255, 255, 255))
    
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(0, 230, 255, 100))

def generate_rift_probe_var2_astrolabe(size=64):
    """Var 2: Astrolábio Octaédrico Dimensional (Dimensional Octahedral Astrolabe).
    Nested gyroscope gimbal rings, sacred geometry octahedron core, runic spatial compass."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx, cy = 32, 32
    
    # Outer Gold Gyroscope Ring
    r_outer = 24
    d.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - r_outer + 1, cy - r_outer + 1, cx + r_outer - 1, cy + r_outer - 1], outline=(140, 95, 25, 255), width=1)
    
    # Intermediate Tilted Ring (Cyan phase ring)
    d.ellipse([cx - 20, cy - 10, cx + 20, cy + 10], outline=(0, 240, 255, 220), width=2)
    # Vertical Tilted Ring (Purple resonance ring)
    d.ellipse([cx - 10, cy - 20, cx + 10, cy + 20], outline=(180, 80, 255, 220), width=2)
    
    # Cardinal Calibration Prongs
    for ang in [0, 90, 180, 270]:
        rad = math.radians(ang)
        px0 = int(cx + math.cos(rad) * (r_outer - 3))
        py0 = int(cy + math.sin(rad) * (r_outer - 3))
        px1 = int(cx + math.cos(rad) * (r_outer + 4))
        py1 = int(cy + math.sin(rad) * (r_outer + 4))
        d.line([(px0, py0), (px1, py1)], fill=(255, 255, 255, 255), width=2)
        d.rectangle([px1 - 1, py1 - 1, px1 + 1, py1 + 1], fill=(255, 215, 80, 255))
        
    # Central Glowing Octahedron Crystal
    oct_r = 10
    top_pt = (cx, cy - oct_r)
    bot_pt = (cx, cy + oct_r)
    left_pt = (cx - oct_r, cy)
    right_pt = (cx + oct_r, cy)
    
    # Upper left facet
    d.polygon([top_pt, left_pt, (cx, cy)], fill=(0, 220, 255, 230), outline=(255, 255, 255, 255))
    # Upper right facet (specular highlight)
    d.polygon([top_pt, right_pt, (cx, cy)], fill=(180, 245, 255, 255), outline=(255, 255, 255, 255))
    # Lower left facet
    d.polygon([bot_pt, left_pt, (cx, cy)], fill=(0, 140, 220, 230), outline=(255, 255, 255, 255))
    # Lower right facet
    d.polygon([bot_pt, right_pt, (cx, cy)], fill=(0, 180, 240, 230), outline=(255, 255, 255, 255))
    
    # Pulsing Center
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255, 255))
    
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(0, 220, 255, 90))

def generate_rift_probe_var3_bathyscaphe(size=64):
    """Var 3: Batíscafo de Vácuo Profundo (Deep Void Bathyscaphe).
    Armored spherical deep-space exploration capsule, reinforced viewports, sensor antennae and thrusters."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx, cy = 32, 33
    r = 18
    
    # Heavy Hull Sphere
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(35, 25, 48, 255), outline=(90, 70, 120, 255), width=2)
    
    # Metallic Hull Shading
    for y in range(cy - r + 1, cy + r):
        dy = y - cy
        half_w = int(math.sqrt(max(0, r*r - dy*dy)))
        val = int(30 + (y - (cy - r)) * 0.6)
        d.line([(cx - half_w + 1, y), (cx + half_w - 1, y)], fill=(val, val - 6, val + 14, 255))
        
    # Armored Ring Belts (Latitude lines)
    d.arc([cx - r, cy - 8, cx + r, cy + 8], start=0, end=180, fill=(255, 215, 80, 200), width=2)
    
    # Reinforced Center Viewport Dome (Incandescent Cyan/Violet)
    vr = 9
    d.ellipse([cx - vr, cy - vr, cx + vr, cy + vr], fill=(12, 6, 24, 255), outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - vr + 2, cy - vr + 2, cx + vr - 2, cy + vr - 2], fill=(0, 240, 255, 240))
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    # Glass glare
    d.arc([cx - vr + 3, cy - vr + 3, cx + vr - 3, cy + vr - 3], start=200, end=300, fill=(255, 255, 255, 255), width=1)
    
    # Sub-Space Sensor Antenna at Top
    d.line([(cx, cy - r), (cx, 8)], fill=(180, 160, 210, 255), width=2)
    d.ellipse([cx - 3, 5, cx + 3, 11], fill=(255, 215, 80, 255), outline=(255, 255, 255, 255))
    d.line([(cx - 7, 8), (cx + 7, 8)], fill=(255, 215, 80, 255), width=1)
    
    # Lateral Thruster Pods
    for tx in [cx - r - 4, cx + r - 1]:
        d.rectangle([tx, cy - 5, tx + 5, cy + 5], fill=(50, 40, 70, 255), outline=(140, 110, 180, 255))
        d.line([(tx + 1, cy + 5), (tx + 1, cy + 9)], fill=(0, 240, 255, 255), width=2)
        
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(0, 240, 255, 80))

# ===========================================================================
# 4. DEPTH ANCHOR (64x64 HD)
# ===========================================================================

def generate_depth_anchor_var1_grav_stake(size=64):
    """Var 1: Estaca Gravitacional de Singularidade (Gravitational Singularity Stake).
    Dense gravimetric spearhead, dark matter containment tether rings, dimensional anchor prongs."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx = 32
    # Vertical Stake Spire: from y=6 to y=57
    # Top Eyelet / Shackle Ring
    d.ellipse([cx - 8, 6, cx + 8, 20], fill=(25, 18, 38, 255), outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - 4, 10, cx + 4, 16], fill=(0, 0, 0, 0), outline=(140, 100, 30, 255), width=1)
    
    # Main Shaft (Heavy Beveled Tungsten-Naquadah Column)
    d.polygon([(cx - 4, 19), (cx + 4, 19), (cx + 5, 42), (cx - 5, 42)], fill=(40, 30, 55, 255), outline=(130, 105, 165, 255))
    d.line([(cx, 19), (cx, 42)], fill=(200, 180, 230, 255), width=1)
    
    # Pulsing Gravitational Wave Rings (Horizontal Ribs)
    for ry in [24, 30, 36]:
        d.ellipse([cx - 11, ry - 3, cx + 11, ry + 3], outline=(0, 240, 255, 220), width=1)
        d.line([(cx - 7, ry), (cx + 7, ry)], fill=(255, 215, 80, 255), width=2)
        
    # Singularity Ground Spike Point (Wedge)
    d.polygon([(cx - 7, 42), (cx + 7, 42), (cx, 58)], fill=(22, 14, 34, 255), outline=(255, 215, 80, 255), width=2)
    d.line([(cx, 42), (cx, 57)], fill=(0, 240, 255, 255), width=2)
    d.point((cx, 58), fill=(255, 255, 255, 255))
    
    # Gravitational Barbs / Anchoring Fins (Lateral Wings)
    # Left fin
    d.polygon([(cx - 5, 34), (cx - 18, 44), (cx - 15, 48), (cx - 5, 41)], fill=(32, 22, 48, 255), outline=(0, 240, 255, 255))
    # Right fin
    d.polygon([(cx + 5, 34), (cx + 18, 44), (cx + 15, 48), (cx + 5, 41)], fill=(32, 22, 48, 255), outline=(0, 240, 255, 255))
    
    # Central Black-Hole Micro Singularity
    d.ellipse([cx - 3, 29, cx + 3, 35], fill=(0, 0, 0, 255), outline=(180, 80, 255, 255), width=1)
    d.point((cx, 32), fill=(255, 255, 255, 255))
    
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(0, 240, 255, 80))

def generate_depth_anchor_var2_fluke(size=64):
    """Var 2: Âncora de Fenda Fluke (Dimensional Fluke Anchor).
    Classical heavy nautical anchor forged in radiant Godforge naquadah with quantum phase-shifting flukes."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx = 32
    # Top Hoist Ring
    d.ellipse([cx - 8, 6, cx + 8, 20], fill=(20, 14, 30, 255), outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - 4, 10, cx + 4, 16], fill=(0, 0, 0, 0))
    
    # Cross Stock (Horizontal Beam)
    d.rectangle([13, 20, 51, 25], fill=(38, 28, 52, 255), outline=(255, 215, 80, 255), width=1)
    d.line([(14, 21), (50, 21)], fill=(255, 240, 160, 255), width=1)
    # Stock terminal balls
    d.ellipse([10, 19, 14, 26], fill=(255, 215, 80, 255))
    d.ellipse([50, 19, 54, 26], fill=(255, 215, 80, 255))
    
    # Central Shank
    d.rectangle([cx - 4, 24, cx + 4, 46], fill=(30, 22, 44, 255), outline=(140, 110, 175, 255))
    d.line([(cx, 25), (cx, 45)], fill=(200, 180, 230, 255), width=1)
    
    # Curved Anchor Arms / Crown (Arc from left fluke to right fluke)
    arm_pts_left = [(cx - 4, 45), (cx - 16, 48), (cx - 23, 40), (cx - 24, 31)]
    arm_pts_right = [(cx + 4, 45), (cx + 16, 48), (cx + 23, 40), (cx + 24, 31)]
    
    # Broad Crown Base
    d.polygon([(cx - 7, 44), (cx + 7, 44), (cx + 5, 53), (cx - 5, 53)], fill=(255, 215, 80, 255), outline=(140, 95, 25, 255))
    d.ellipse([cx - 3, 51, cx + 3, 56], fill=(0, 240, 255, 255))
    
    # Fluke Left Spade (Dimensional Blade)
    d.polygon([(8, 30), (13, 19), (17, 34)], fill=(0, 220, 255, 240), outline=(255, 255, 255, 255), width=1)
    d.line([(10, 31), (cx - 4, 48)], fill=(40, 30, 58, 255), width=5)
    d.line([(10, 31), (cx - 4, 48)], fill=(255, 215, 80, 255), width=2)
    
    # Fluke Right Spade (Dimensional Blade)
    d.polygon([(56, 30), (51, 19), (47, 34)], fill=(0, 220, 255, 240), outline=(255, 255, 255, 255), width=1)
    d.line([(54, 31), (cx + 4, 48)], fill=(40, 30, 58, 255), width=5)
    d.line([(54, 31), (cx + 4, 48)], fill=(255, 215, 80, 255), width=2)
    
    # Tachyon energy arcs leaping between flukes and shank
    d.line([(14, 28), (cx - 5, 34)], fill=(180, 80, 255, 200), width=1)
    d.line([(50, 28), (cx + 5, 34)], fill=(180, 80, 255, 200), width=1)
    
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(255, 215, 80, 90))

def generate_depth_anchor_var3_tripod(size=64):
    """Var 3: Pilone Trípode de Fixação Subespacial (Subspace Tripod Pylon).
    Industrial heavy-duty anchoring apparatus with deployable hydraulic ground claws, flux spire, and spatial lock."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx = 32
    # Top Spatial Mooring Emitter
    d.polygon([(cx - 7, 10), (cx + 7, 10), (cx, 5)], fill=(0, 240, 255, 255), outline=(255, 255, 255, 255))
    d.ellipse([cx - 4, 9, cx + 4, 17], fill=(255, 215, 80, 255), outline=(140, 95, 25, 255))
    
    # Central Pylon Spire
    d.rectangle([cx - 5, 17, cx + 5, 41], fill=(32, 24, 46, 255), outline=(130, 100, 170, 255), width=1)
    for y in range(18, 41):
        d.line([(cx - 4, y), (cx + 4, y)], fill=(38 + (y%4)*6, 28 + (y%4)*5, 52 + (y%4)*8, 255))
    d.line([(cx, 18), (cx, 40)], fill=(0, 240, 255, 255), width=1)
    
    # Massive Tripod Legs
    # Left Leg
    d.polygon([(cx - 5, 35), (cx - 24, 53), (cx - 19, 56), (cx - 3, 40)], fill=(45, 32, 62, 255), outline=(255, 215, 80, 255))
    # Right Leg
    d.polygon([(cx + 5, 35), (cx + 24, 53), (cx + 19, 56), (cx + 3, 40)], fill=(45, 32, 62, 255), outline=(255, 215, 80, 255))
    # Center Front Leg
    d.polygon([(cx - 4, 38), (cx + 4, 38), (cx + 3, 57), (cx - 3, 57)], fill=(55, 40, 75, 255), outline=(180, 150, 220, 255))
    
    # Heavy Footpads & Ground Claws
    d.rectangle([cx - 26, 52, cx - 17, 57], fill=(255, 215, 80, 255), outline=(120, 80, 20, 255))
    d.rectangle([cx + 17, 52, cx + 26, 57], fill=(255, 215, 80, 255), outline=(120, 80, 20, 255))
    d.rectangle([cx - 6, 56, cx + 6, 60], fill=(255, 215, 80, 255), outline=(120, 80, 20, 255))
    
    # Hydraulic Pistons (Piston rods in steel highlight)
    d.line([(cx - 4, 28), (cx - 16, 44)], fill=(220, 225, 240, 255), width=2)
    d.line([(cx + 4, 28), (cx + 16, 44)], fill=(220, 225, 240, 255), width=2)
    
    # Subspace Lock Field (Hexagonal Shield Glow)
    d.ellipse([cx - 8, 23, cx + 8, 35], outline=(0, 240, 255, 240), width=1)
    d.ellipse([cx - 3, 26, cx + 3, 32], fill=(255, 255, 255, 255))
    
    return apply_glow_and_outline(im, outline_col=(18, 12, 28, 255), glow_col=(0, 240, 255, 80))

# ===========================================================================
# 5. RIFT SINGULARITY (64x64 HD)
# ===========================================================================

def generate_rift_singularity_var1_vortex(size=64):
    """Var 1: Horizonte de Eventos Vórtice de Fenda (Swirling Event Horizon).
    Hypnotic accretion vortex of distorted spacetime spiraling into a pure void black hole with relativistic jets."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx, cy = 32, 32
    
    # Multi-arm spiral accretion vortex
    num_arms = 4
    for arm in range(num_arms):
        arm_offset = arm * (2 * math.pi / num_arms)
        for step in range(50):
            theta = step * 0.16 + arm_offset
            r = step * 0.5 + 4
            if r > 28: break
            x = int(cx + math.cos(theta) * r)
            y = int(cy + math.sin(theta) * r * 0.75) # Slight tilt
            frac = step / 50.0
            col = (int(180 * frac + 0 * (1 - frac)),
                   int(60 * frac + 240 * (1 - frac)),
                   int(255 * frac + 255 * (1 - frac)),
                   int(220 * (1 - frac*0.5)))
            dot_r = 1 if step < 20 else 2
            d.ellipse([x - dot_r, y - dot_r, x + dot_r, y + dot_r], fill=col)
            
    # Relativistic Polar Jets (Vertical luminous beam)
    for jy in range(6, 58):
        dist_y = abs(jy - cy)
        if dist_y > 8:
            jet_alpha = int(220 * (1.0 - (dist_y - 8) / 26.0))
            d.line([(cx - 1, jy), (cx + 1, jy)], fill=(0, 240, 255, jet_alpha), width=1)
            d.point((cx, jy), fill=(255, 255, 255, jet_alpha))
            
    # Glowing Photon Sphere Ring (Gold & Cyan)
    d.ellipse([cx - 11, cy - 8, cx + 11, cy + 8], outline=(255, 215, 80, 255), width=2)
    d.ellipse([cx - 12, cy - 9, cx + 12, cy + 9], outline=(0, 240, 255, 180), width=1)
    
    # Pure Void Event Horizon Core
    d.ellipse([cx - 8, cy - 6, cx + 8, cy + 6], fill=(5, 2, 10, 255), outline=(140, 40, 220, 255), width=1)
    
    return apply_glow_and_outline(im, outline_col=(18, 10, 28, 255), glow_col=(180, 60, 255, 120))

def generate_rift_singularity_var2_tesseract(size=64):
    """Var 2: Hipercubo Tesseract 4D (4D Tesseract Core).
    Multi-dimensional rotating wireframe hypercube with inner singularity core and spatial rift cracks."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx, cy = 32, 32
    
    # Outer 3D Cube Projection vertices
    orad = 22
    out_verts = [
        (cx - orad, cy - int(orad * 0.6)), # 0: Top-left
        (cx + orad, cy - int(orad * 0.6)), # 1: Top-right
        (cx + orad, cy + int(orad * 0.6)), # 2: Bot-right
        (cx - orad, cy + int(orad * 0.6)), # 3: Bot-left
        (cx, cy - orad),                   # 4: Apex Top
        (cx, cy + orad),                   # 5: Apex Bot
    ]
    
    # Inner 4D Hypercube Vertices
    irad = 9
    in_verts = [
        (cx - irad, cy - int(irad * 0.6)), # 0
        (cx + irad, cy - int(irad * 0.6)), # 1
        (cx + irad, cy + int(irad * 0.6)), # 2
        (cx - irad, cy + int(irad * 0.6)), # 3
        (cx, cy - irad),                   # 4
        (cx, cy + irad),                   # 5
    ]
    
    # Outer Cube Edges (Gold & Cosmic Purple Wireframe)
    outer_edges = [(4, 0), (4, 1), (0, 3), (1, 2), (3, 5), (2, 5)]
    for u, v in outer_edges:
        d.line([out_verts[u], out_verts[v]], fill=(255, 215, 80, 240), width=2)
        
    # Inner Cube Edges (Cyan Wireframe)
    inner_edges = [(4, 0), (4, 1), (0, 3), (1, 2), (3, 5), (2, 5)]
    for u, v in inner_edges:
        d.line([in_verts[u], in_verts[v]], fill=(0, 240, 255, 255), width=2)
        
    # 4D Trans-dimensional Connecting Struts (Outer to Inner)
    for i in range(6):
        d.line([out_verts[i], in_verts[i]], fill=(180, 80, 255, 200), width=1)
        # Glowing vertex nodes
        d.ellipse([out_verts[i][0] - 2, out_verts[i][1] - 2, out_verts[i][0] + 2, out_verts[i][1] + 2],
                  fill=(255, 255, 255, 255), outline=(255, 215, 80, 255))
        d.ellipse([in_verts[i][0] - 1, in_verts[i][1] - 1, in_verts[i][0] + 1, in_verts[i][1] + 1],
                  fill=(255, 255, 255, 255), outline=(0, 240, 255, 255))
                  
    # Central 4D Singularity Point (Ultra-bright white/magenta)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255), outline=(180, 40, 255, 255), width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255, 255))
    
    # Spacetime Rift Energy Cracks
    d.line([(cx - 7, cy - 1), (cx - 16, cy + 3)], fill=(0, 240, 255, 200), width=1)
    d.line([(cx + 6, cy + 2), (cx + 17, cy - 4)], fill=(0, 240, 255, 200), width=1)
    
    return apply_glow_and_outline(im, outline_col=(18, 10, 28, 255), glow_col=(0, 240, 255, 90))

def generate_rift_singularity_var3_void_eye(size=64):
    """Var 3: Olho do Vazio Cósmico (Cosmic Void Eye).
    Horrific and awe-inspiring dimensional fissure opening like an all-seeing celestial eye into the abyss."""
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    
    cx, cy = 32, 32
    
    # Outer Energy Tendrils / Corona
    for ang in range(0, 360, 20):
        rad = math.radians(ang)
        r0 = 16
        r1 = 26 + (ang % 40) // 10 * 3
        px0 = int(cx + math.cos(rad) * r0)
        py0 = int(cy + math.sin(rad) * r0 * 0.6)
        px1 = int(cx + math.cos(rad) * r1)
        py1 = int(cy + math.sin(rad) * r1 * 0.6)
        d.line([(px0, py0), (px1, py1)], fill=(160, 40, 255, 140), width=1)
        d.point((px1, py1), fill=(0, 240, 255, 200))
        
    # The Celestial Eye Fissure Shape (Curved top and bottom eyelids)
    # Upper lid arc, lower lid arc
    eye_w = 26
    eye_h = 16
    eye_pts_top = []
    eye_pts_bot = []
    for x in range(cx - eye_w, cx + eye_w + 1):
        rel = (x - cx) / float(eye_w)
        if abs(rel) <= 1.0:
            curve = math.sqrt(max(0, 1.0 - rel * rel))
            eye_pts_top.append((x, int(cy - curve * eye_h)))
            eye_pts_bot.append((x, int(cy + curve * eye_h)))
            
    eye_poly = eye_pts_top + eye_pts_bot[::-1]
    d.polygon(eye_poly, fill=(15, 6, 28, 255), outline=(255, 215, 80, 255), width=2)
    
    # Glowing Eyelid Ribbons (Gold & Cyan)
    for p in eye_pts_top:
        d.point((p[0], p[1] - 1), fill=(255, 240, 160, 255))
    for p in eye_pts_bot:
        d.point((p[0], p[1] + 1), fill=(0, 240, 255, 255))
        
    # Glowing Amethyst Iris
    iris_r = 11
    d.ellipse([cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r], fill=(120, 20, 200, 255), outline=(0, 240, 255, 255), width=2)
    d.ellipse([cx - iris_r + 2, cy - iris_r + 2, cx + iris_r - 2, cy + iris_r - 2], fill=(180, 50, 255, 255))
    
    # Pure Abyss Pupil (Vertical Cat/Void Slit)
    d.polygon([(cx - 2, cy - 10), (cx + 2, cy - 10), (cx + 4, cy), (cx + 2, cy + 10), (cx - 2, cy + 10), (cx - 4, cy)],
              fill=(0, 0, 0, 255), outline=(255, 255, 255, 255), width=1)
              
    # Blinding Starlight Glint
    d.ellipse([cx - 4, cy - 5, cx - 1, cy - 2], fill=(255, 255, 255, 255))
    
    return apply_glow_and_outline(im, outline_col=(18, 10, 28, 255), glow_col=(180, 40, 255, 110))

# ===========================================================================
# GENERATION & COMPARISON SHEETS
# ===========================================================================

def generate_item_comparison_sheet(cat_name, title, desc, variations, out_file):
    """Build a professional showcase sheet for 3 item variations in HD:
    - 64x64 native
    - 128x128 preview (2x pixel-perfect)
    - 256x256 showcase (4x pixel-perfect)
    - Descriptions, specs and rationale."""
    sw, sh = 880, 580
    sheet = Image.new('RGBA', (sw, sh), (14, 10, 22, 255))
    d = ImageDraw.Draw(sheet)
    
    # Top Header
    d.rectangle([0, 0, sw, 70], fill=(24, 16, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((25, 14), f"GTNA ITEM PROPOSALS · {title.upper()} (RESOLUÇÃO 64x64 HD)", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((25, 42), desc, fill=(180, 190, 210, 255), font=FONT_SUB)
    
    col_w = (sw - 40) // 3
    for idx, (v_name, v_subtitle, v_img, v_specs) in enumerate(variations):
        cx = 20 + idx * col_w
        cy = 85
        cw = col_w - 12
        ch = sh - 100
        
        # Panel container
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(18, 12, 28, 255), outline=(65, 45, 90, 255), width=2)
        d.rectangle([cx + 2, cy + 2, cx + cw - 2, cy + 32], fill=(28, 18, 44, 255))
        d.text((cx + 10, cy + 8), v_name, fill=(255, 215, 80, 255), font=FONT_TITLE)
        d.text((cx + 10, cy + 36), v_subtitle, fill=(0, 240, 255, 255), font=FONT_MICRO)
        
        # Display Box for 256x256 enlarged pixel-perfect preview
        box_y = cy + 54
        box_size = 200
        box_x = cx + (cw - box_size) // 2
        d.rectangle([box_x, box_y, box_x + box_size, box_y + box_size], fill=(10, 6, 16, 255), outline=(55, 38, 75, 255), width=2)
        
        # Subtitle inside preview box
        d.text((box_x + 6, box_y + 6), "64x64 HD (AMPLIADO 4X)", fill=(100, 110, 130, 200), font=FONT_MICRO)
        
        # Paste 4x enlarged (256x256)
        v_256 = v_img.resize((192, 192), Image.NEAREST)
        sheet.paste(v_256, (box_x + 4, box_y + 4), v_256)
        
        # Native 64x64 preview box beside specs
        nat_y = box_y + box_size + 14
        d.rectangle([box_x, nat_y, box_x + 68, nat_y + 68], fill=(10, 6, 16, 255), outline=(55, 38, 75, 255))
        d.text((box_x + 2, nat_y - 12), "1X NATIVO (64x64)", fill=(140, 150, 170, 255), font=FONT_MICRO)
        sheet.paste(v_img, (box_x + 2, nat_y + 2), v_img)
        
        # Specs & Design Highlights
        spec_x = box_x + 78
        for s_idx, spec in enumerate(v_specs):
            sy = nat_y + s_idx * 15
            d.text((spec_x, sy), f"• {spec}", fill=(200, 210, 230, 255), font=FONT_MICRO)
            
        # Selection Indicator
        btn_y = cy + ch - 34
        d.rectangle([cx + 12, btn_y, cx + cw - 12, btn_y + 24], fill=(35, 24, 52, 255), outline=(255, 215, 80, 200))
        d.text((cx + cw // 2 - 40, btn_y + 5), f"[ PROPOSTA {idx + 1} ]", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
    sheet.save(out_file)
    print(f"  [+] Salvo Showcase: {out_file}")

def generate_contained_particles_master_sheet(particles_list, out_file):
    """Build a master showcase sheet for all 10 Contained Particles + Antiproton Cell in 64x64 HD."""
    sw, sh = 960, 640
    sheet = Image.new('RGBA', (sw, sh), (12, 8, 20, 255))
    d = ImageDraw.Draw(sheet)
    
    # Header
    d.rectangle([0, 0, sw, 70], fill=(22, 14, 34, 255), outline=(75, 45, 105, 255), width=2)
    d.text((25, 14), "GTNA · AS 10 PARTÍCULAS DO ANEL COLISOR & ARMADILHAS DE PENNING (64x64 HD)", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((25, 42), "Modeladas fielmente ao ColliderCore.java · Células de Confinamento Criogênico com Quadrupolo Eletrostático", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    # 5 columns x 2 rows grid for the 10 particles
    cols, rows = 5, 2
    cell_w = (sw - 40) // cols
    cell_h = 220
    
    for idx, (p_id, p_name, p_gev, p_col, p_desc, p_img) in enumerate(particles_list[:10]):
        c = idx % cols
        r = idx // cols
        px = 20 + c * cell_w
        py = 85 + r * (cell_h + 10)
        cw = cell_w - 8
        
        d.rectangle([px, py, px + cw, py + cell_h], fill=(18, 12, 28, 255), outline=(65, 45, 90, 255), width=1)
        d.rectangle([px + 1, py + 1, px + cw - 1, py + 22], fill=(26, 16, 40, 255))
        d.text((px + 6, py + 4), f"{idx + 1}. {p_name}", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((px + cw - 48, py + 4), p_gev, fill=p_col + (255,), font=FONT_MICRO)
        
        # 128x128 enlarged Penning trap (pixel-perfect)
        box_size = 110
        bx = px + (cw - box_size) // 2
        by = py + 26
        d.rectangle([bx, by, bx + box_size, by + box_size], fill=(8, 5, 14, 255), outline=(50, 35, 70, 255))
        
        p_enlarged = p_img.resize((102, 102), Image.NEAREST)
        sheet.paste(p_enlarged, (bx + 4, by + 4), p_enlarged)
        
        # Description & details
        d.text((px + 6, py + 144), p_desc, fill=(200, 210, 230, 255), font=FONT_MICRO)
        d.text((px + 6, py + 160), f"ID: contained_{p_id}", fill=(130, 140, 160, 255), font=FONT_MICRO)
        
        # 5-sigma discovery bar preview
        d.rectangle([px + 6, py + 180, px + cw - 6, py + 188], fill=(10, 6, 16, 255), outline=(50, 40, 70, 255))
        d.rectangle([px + 7, py + 181, px + cw - 7, py + 187], fill=p_col + (255,))
        d.text((px + 6, py + 194), "Nível de Descoberta: 5.0 σ", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
    # Bottom Strip: Antiproton Penning Cell (Dewar Storage)
    strip_y = sh - 85
    d.rectangle([20, strip_y, sw - 20, sh - 15], fill=(24, 16, 38, 255), outline=(255, 215, 80, 255), width=2)
    # Paste Antiproton Cell icon
    dewar_img = particles_list[10][5]
    dewar_enlarged = dewar_img.resize((60, 60), Image.NEAREST)
    sheet.paste(dewar_enlarged, (30, strip_y + 5), dewar_enlarged)
    
    d.text((105, strip_y + 12), "CÉLULA PENNING DE ANTIPRÓTONS (DEWAR DE ALTA CAPACIDADE · 1e11 p⁻)", fill=(255, 215, 80, 255), font=FONT_TITLE)
    d.text((105, strip_y + 32), "Item: 'antiproton_cell' · Usado para evacuar as armadilhas cheias do colisor e alimentar a Lança e a Câmara Estelar.", fill=(200, 210, 230, 255), font=FONT_MICRO)
    d.text((105, strip_y + 48), "Blindagem criogênica reforçada com exo-nervuras de naquadah radiante e vácuo ultra-profundo.", fill=(0, 240, 255, 255), font=FONT_MICRO)
    
    sheet.save(out_file)
    print(f"  [+] Salvo Showcase Master de Partículas: {out_file}")

def generate_target_cartridges_bodies_sheet(bodies_list, out_file):
    """Build a showcase sheet for the 8 Target Cartridges (Moon to Nexus-1) in 64x64 HD."""
    sw, sh = 920, 520
    sheet = Image.new('RGBA', (sw, sh), (12, 8, 20, 255))
    d = ImageDraw.Draw(sheet)
    
    # Header
    d.rectangle([0, 0, sw, 70], fill=(22, 14, 34, 255), outline=(75, 45, 105, 255), width=2)
    d.text((25, 14), "GTNA · OS 8 CARTUCHOS DE ALVO DA LANÇA CINÉTICA (64x64 HD)", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((25, 42), "Modelados fielmente a LanceCore.Body · Cartuchos Ópticos com Coordenadas Planetárias Laser", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    cols, rows = 4, 2
    cell_w = (sw - 40) // cols
    cell_h = 195
    
    for idx, (b_id, b_name, b_col, b_desc, b_img) in enumerate(bodies_list):
        c = idx % cols
        r = idx // cols
        px = 20 + c * cell_w
        py = 85 + r * (cell_h + 10)
        cw = cell_w - 8
        
        d.rectangle([px, py, px + cw, py + cell_h], fill=(18, 12, 28, 255), outline=(65, 45, 90, 255), width=1)
        d.rectangle([px + 1, py + 1, px + cw - 1, py + 22], fill=(26, 16, 40, 255))
        d.text((px + 6, py + 4), f"{idx + 1}. {b_name.upper()}", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((px + cw - 52, py + 4), f"ALVO #{idx+1}", fill=b_col + (255,), font=FONT_MICRO)
        
        # 128x128 enlarged
        box_size = 96
        bx = px + (cw - box_size) // 2
        by = py + 26
        d.rectangle([bx, by, bx + box_size, by + box_size], fill=(8, 5, 14, 255), outline=(50, 35, 70, 255))
        
        b_enlarged = b_img.resize((90, 90), Image.NEAREST)
        sheet.paste(b_enlarged, (bx + 3, by + 3), b_enlarged)
        
        # Description & details
        d.text((px + 6, py + 130), b_desc, fill=(200, 210, 230, 255), font=FONT_MICRO)
        d.text((px + 6, py + 146), f"ID: target_cartridge_{b_id}", fill=(130, 140, 160, 255), font=FONT_MICRO)
        d.text((px + 6, py + 164), "Óptica: Prisma Quântico 64x HD", fill=(0, 240, 255, 255), font=FONT_MICRO)
        
    sheet.save(out_file)
    print(f"  [+] Salvo Showcase de Cartuchos por Corpo Celeste: {out_file}")

def generate_master_all_items_hd_poster(all_categories_data, out_file):
    """Poster assembling all 5 Endgame Item categories in 64x64 HD."""
    sw, sh = 1080, 720
    poster = Image.new('RGBA', (sw, sh), (10, 6, 16, 255))
    d = ImageDraw.Draw(poster)
    
    # Outer Tech Frame
    d.rectangle([0, 0, sw, 80], fill=(20, 12, 32, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 16), "GTNA · GALERIA MASTER DE ITENS ENDGAME (64x64 HD PIXEL ART)", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 46), "Resolução HD 64x64 com Iluminação Emissiva, Chanfros Metálicos, Vidro Refletivo & Cores do Código", fill=(180, 190, 210, 255), font=FONT_SUB)
    
    # 5 Rows/Columns for the 5 Categories
    cat_y = 95
    row_h = 115
    for idx, (cat_title, cat_items, cat_desc) in enumerate(all_categories_data):
        cy = cat_y + idx * (row_h + 8)
        d.rectangle([20, cy, sw - 20, cy + row_h], fill=(16, 10, 25, 255), outline=(60, 40, 85, 255), width=1)
        
        # Category Label
        d.rectangle([22, cy + 2, 220, cy + 24], fill=(28, 18, 44, 255))
        d.text((28, cy + 5), f"{idx + 1}. {cat_title.upper()}", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((28, cy + 32), cat_desc, fill=(160, 170, 190, 255), font=FONT_MICRO)
        
        # Display items on row
        ix_start = 240
        item_gap = 135
        for i_idx, (it_name, it_img, it_tag) in enumerate(cat_items):
            ix = ix_start + i_idx * item_gap
            if ix + 120 < sw:
                # Small item frame
                d.rectangle([ix, cy + 8, ix + 125, cy + row_h - 8], fill=(10, 6, 16, 255), outline=(50, 35, 70, 255))
                # 64x64 native
                poster.paste(it_img, (ix + 6, cy + 18), it_img)
                # Label
                d.text((ix + 76, cy + 24), it_tag, fill=(0, 240, 255, 255), font=FONT_MICRO)
                d.text((ix + 76, cy + 44), it_name, fill=(255, 215, 80, 255), font=FONT_MICRO)
                
    poster.save(out_file)
    print(f"  [+] Salvo Poster Master de Todos os Itens HD: {out_file}")

def main():
    print(">>> Gerando todas as texturas de itens em 64x64 HD e Showcases...")
    
    # -----------------------------------------------------------------------
    # 1. TARGET CARTRIDGE
    # -----------------------------------------------------------------------
    tc_dir = os.path.join(PROPOSALS_DIR, 'target_cartridge', '64x64')
    tc_v1 = generate_cartridge_var1_tactical_rom(64)
    tc_v2 = generate_cartridge_var2_cosmic_optical(64, (255, 215, 80), "MOON")
    tc_v3 = generate_cartridge_var3_holo_dome(64)
    
    tc_v1.save(os.path.join(tc_dir, 'target_cartridge_var1_tactical_rom_64.png'))
    tc_v2.save(os.path.join(tc_dir, 'target_cartridge_var2_cosmic_optical_64.png'))
    tc_v3.save(os.path.join(tc_dir, 'target_cartridge_var3_holo_dome_64.png'))
    
    tc_variations = [
        ("VARIAÇÃO 1: ROM TÁTICA", "Chassi Militar de Tungstênio / LEDs / AE2", tc_v1,
         ["Blindagem de grau militar", "Barramento ouro estilo AE2", "Cluster de LEDs de telemetria", "Retículo de mira a laser"]),
        ("VARIAÇÃO 2: ÓPTICA QUÂNTICA", "Godforge Gold / Prisma Hexagonal / Lente", tc_v2,
         ["Estrutura em Naquadah Radiante", "Prisma óptico hexagonal", "Foco quântico estelar", "Reflexo especular multicamada"]),
        ("VARIAÇÃO 3: HOLO-DOMO", "Domo Transtranslúcido / Trajetória Orbital", tc_v3,
         ["Domo de cyber-vidro curvo", "Órbitas 3D holográficas", "Micro-barramento de dados", "Núcleo celestial de precisão"]),
    ]
    generate_item_comparison_sheet('target_cartridge', "Cartucho de Alvo (Target Cartridge)",
                                   "Módulo de mira e navegação orbital para a Lança Cinética Orbital (UEV)",
                                   tc_variations,
                                   os.path.join(PROPOSALS_DIR, 'target_cartridge', 'previews', 'showcase_target_cartridge_64.png'))
                                   
    # 8 Bodies Target Cartridges
    bodies_list = []
    for b_id, b_name, b_col, b_desc in BODY_DATA:
        b_im = generate_cartridge_var2_cosmic_optical(64, b_col, b_name)
        b_im.save(os.path.join(tc_dir, f'target_cartridge_{b_id}_64.png'))
        bodies_list.append((b_id, b_name, b_col, b_desc, b_im))
        
    generate_target_cartridges_bodies_sheet(bodies_list,
                                           os.path.join(PROPOSALS_DIR, 'target_cartridge', 'previews', 'showcase_all_8_bodies_cartridges_64.png'))

    # -----------------------------------------------------------------------
    # 2. CONTAINED PARTICLES
    # -----------------------------------------------------------------------
    part_dir = os.path.join(PROPOSALS_DIR, 'contained_particles', '64x64')
    particles_list = []
    for p_id, p_name, p_gev, p_col, p_desc in PARTICLE_PROFILES:
        p_im = generate_penning_trap_64(p_col, p_id, is_dewar_cell=False)
        p_im.save(os.path.join(part_dir, f'contained_{p_id}_64.png'))
        particles_list.append((p_id, p_name, p_gev, p_col, p_desc, p_im))
        
    # Antiproton Penning Cell (Dewar)
    dewar_im = generate_penning_trap_64((0, 240, 255), "antiproton", is_dewar_cell=True)
    dewar_im.save(os.path.join(part_dir, 'antiproton_cell_64.png'))
    particles_list.append(("antiproton_cell", "Célula Dewar", "1e11 p⁻", (0, 240, 255), "Dewar Criogênico", dewar_im))
    
    generate_contained_particles_master_sheet(particles_list,
                                             os.path.join(PROPOSALS_DIR, 'contained_particles', 'previews', 'showcase_contained_particles_64.png'))

    # -----------------------------------------------------------------------
    # 3. RIFT PROBE
    # -----------------------------------------------------------------------
    rp_dir = os.path.join(PROPOSALS_DIR, 'rift_probe', '64x64')
    rp_v1 = generate_rift_probe_var1_needle(64)
    rp_v2 = generate_rift_probe_var2_astrolabe(64)
    rp_v3 = generate_rift_probe_var3_bathyscaphe(64)
    
    rp_v1.save(os.path.join(rp_dir, 'rift_probe_var1_needle_64.png'))
    rp_v2.save(os.path.join(rp_dir, 'rift_probe_var2_astrolabe_64.png'))
    rp_v3.save(os.path.join(rp_dir, 'rift_probe_var3_bathyscaphe_64.png'))
    
    rp_variations = [
        ("VARIAÇÃO 1: AGULHA DE TÁCTONS", "Aerodinâmica Temporal / Emissor / Aletas", rp_v1,
         ["Agulha de penetração cronal", "Aletas estabilizadoras em delta", "Núcleo de tácton pulsante", "Propulsor de íons de fase"]),
        ("VARIAÇÃO 2: ASTROLÁBIO", "Giroscópio / Geometria Sagrada / Bússola", rp_v2,
         ["Anéis cardânicos de ouro", "Octaedro cristalino central", "Prongos de calibração cósmica", "Sensor de ressonância 3D"]),
        ("VARIAÇÃO 3: BATÍSCAFO", "Esfera Blindada / Domo / Antenas", rp_v3,
         ["Casco esférico reforçado", "Visor em cyber-vidro ciano", "Antena de telemetria subespaço", "Propulsores omnidirecionais"]),
    ]
    generate_item_comparison_sheet('rift_probe', "Sonda de Fenda (Rift Probe)",
                                   "Sonda de reconhecimento enviada através da fenda dimensional (UIV)",
                                   rp_variations,
                                   os.path.join(PROPOSALS_DIR, 'rift_probe', 'previews', 'showcase_rift_probe_64.png'))

    # -----------------------------------------------------------------------
    # 4. DEPTH ANCHOR
    # -----------------------------------------------------------------------
    da_dir = os.path.join(PROPOSALS_DIR, 'depth_anchor', '64x64')
    da_v1 = generate_depth_anchor_var1_grav_stake(64)
    da_v2 = generate_depth_anchor_var2_fluke(64)
    da_v3 = generate_depth_anchor_var3_tripod(64)
    
    da_v1.save(os.path.join(da_dir, 'depth_anchor_var1_grav_stake_64.png'))
    da_v2.save(os.path.join(da_dir, 'depth_anchor_var2_fluke_64.png'))
    da_v3.save(os.path.join(da_dir, 'depth_anchor_var3_tripod_64.png'))
    
    da_variations = [
        ("VARIAÇÃO 1: ESTACA GRAVITACIONAL", "Haste Pesada / Nervuras de Fluxo / Espigão", da_v1,
         ["Olhal de ancoragem pesada", "Nervuras de pulso gravitacional", "Farpas laterais de fixação", "Micro-singularidade no núcleo"]),
        ("VARIAÇÃO 2: ÂNCORA FLUKE", "Âncora Náutica Cósmica / Pás de Fenda", da_v2,
         ["Cepo horizontal com terminais", "Pás de fenda com corte de fase", "Coroa pesada em ouro naquadah", "Arcos de energia taquiônica"]),
        ("VARIAÇÃO 3: PILONE TRÍPODE", "Trípode Industrial / Garras Hidráulicas", da_v3,
         ["Pistões hidráulicos duplos", "Sapatas de solo auto-cravantes", "Torre de confinamento de fluxo", "Campo de trava hexagonal"]),
    ]
    generate_item_comparison_sheet('depth_anchor', "Âncora de Profundidade (Depth Anchor)",
                                   "Fixador gravitacional de horizontes de fenda dimensional (UIV)",
                                   da_variations,
                                   os.path.join(PROPOSALS_DIR, 'depth_anchor', 'previews', 'showcase_depth_anchor_64.png'))

    # -----------------------------------------------------------------------
    # 5. RIFT SINGULARITY
    # -----------------------------------------------------------------------
    rs_dir = os.path.join(PROPOSALS_DIR, 'rift_singularity', '64x64')
    rs_v1 = generate_rift_singularity_var1_vortex(64)
    rs_v2 = generate_rift_singularity_var2_tesseract(64)
    rs_v3 = generate_rift_singularity_var3_void_eye(64)
    
    rs_v1.save(os.path.join(rs_dir, 'rift_singularity_var1_vortex_64.png'))
    rs_v2.save(os.path.join(rs_dir, 'rift_singularity_var2_tesseract_64.png'))
    rs_v3.save(os.path.join(rs_dir, 'rift_singularity_var3_void_eye_64.png'))
    
    rs_variations = [
        ("VARIAÇÃO 1: VÓRTICE HORIZONTE", "Espiral de Acreção / Jatos Relativísticos", rs_v1,
         ["Braços espirais de acreção", "Esfera de fótons brilhante", "Horizonte de eventos puro breu", "Jatos polares relativísticos"]),
        ("VARIAÇÃO 2: TESSERACT 4D", "Hipercubo Wireframe / Fendas de Espaço-Tempo", rs_v2,
         ["Projeção de hipercubo 4D", "Vértices estelares dourados", "Nervuras trans-dimensionais", "Fissuras de ruptura quântica"]),
        ("VARIAÇÃO 3: OLHO DO VAZIO", "Fissura Abissal / Íris Ametista / Pupila Fenda", rs_v3,
         ["Bordas de fenda com fitas de luz", "Íris de ametista cósmica", "Pupila em fenda vertical negra", "Glint estelar ofuscante"]),
    ]
    generate_item_comparison_sheet('rift_singularity', "Singularidade de Fenda (Rift Singularity)",
                                   "Artefato primordial colapsado no centro do Portão de Fenda (UIV/MAX)",
                                   rs_variations,
                                   os.path.join(PROPOSALS_DIR, 'rift_singularity', 'previews', 'showcase_rift_singularity_64.png'))

    # -----------------------------------------------------------------------
    # MASTER POSTER OF ALL ITEMS
    # -----------------------------------------------------------------------
    all_categories_data = [
        ("Cartucho de Alvo", [
            ("ROM Tática", tc_v1, "VAR 1"),
            ("Óptica Quântica", tc_v2, "VAR 2"),
            ("Holo-Domo", tc_v3, "VAR 3"),
            ("Lua", bodies_list[0][4], "CORPO"),
            ("Nexus-1", bodies_list[7][4], "FINAL"),
        ], "Módulo de mira e navegação orbital para a Lança Cinética."),
        ("Partículas & Células", [
            ("Antipróton", particles_list[0][5], "5.6 GeV"),
            ("Bóson W", particles_list[5][5], "161 GeV"),
            ("Higgs", particles_list[7][5], "250 GeV"),
            ("X-Nexus", particles_list[9][5], "4.8 TeV"),
            ("Célula Dewar", dewar_im, "1e11 p⁻"),
        ], "Armadilhas de Penning do Anel Colisor (10 partículas do código)."),
        ("Sonda de Fenda", [
            ("Agulha Tácton", rp_v1, "VAR 1"),
            ("Astrolábio", rp_v2, "VAR 2"),
            ("Batíscafo", rp_v3, "VAR 3"),
        ], "Sonda de prospecção e telemetria dimensional do Portão."),
        ("Âncora de Profundidade", [
            ("Estaca Grav.", da_v1, "VAR 1"),
            ("Âncora Fluke", da_v2, "VAR 2"),
            ("Pilone Trípode", da_v3, "VAR 3"),
        ], "Fixador e estabilizador de horizontes de fenda."),
        ("Singularidade de Fenda", [
            ("Vórtice Acreção", rs_v1, "VAR 1"),
            ("Tesseract 4D", rs_v2, "VAR 2"),
            ("Olho do Vazio", rs_v3, "VAR 3"),
        ], "Artefato dimensional de distorção de horizonte e vácuo."),
    ]
    generate_master_all_items_hd_poster(all_categories_data,
                                        os.path.join(PROPOSALS_DIR, 'all_items_master_showcase_64.png'))
    print(">>> [SUCESSO] Todos os itens 64x64 HD foram gerados com perfeição!")

if __name__ == '__main__':
    main()
