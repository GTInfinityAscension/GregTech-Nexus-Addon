"""Master Generator for 36 Endgame Material Set Proposals (12 materials x 3 options).
Generates animated 32-frame previews, custom animated 64x64 halos, and slot composites without modifying any game code.
"""

import colorsys
import json
import math
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MODERNITY = Path.home() / "Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures"
ICONSETS = MODERNITY / "items/materialicons"
CUSTOM = ICONSETS / "CUSTOM/WhiteDwarfMatter"
CUSTOM_BLOCK = MODERNITY / "blocks/materialicons/CUSTOM/WhiteDwarfMatter"
PROPOSALS_DIR = ROOT / "docs/roadmap/design/proposals/originals_material_sets"
PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)

FRAMES = 32
HALO_SIZE = 64
CELL = 32
EMPTY = Image.new("RGBA", (16, 16), (0, 0, 0, 0))

FORMS = {
    "ingot": "ingot", "nugget": "nugget", "dust": "dust", "dust_small": "dustSmall", "dust_tiny": "dustTiny",
    "plate": "plate", "rod": "stick", "wire_fine": "wireFine", "gem": "gem", "block": "block"
}


def base_of(name, ingot_profile=None):
    src = FORMS.get(name, name)
    if name == "block":
        path = CUSTOM_BLOCK / "block1.png"
        if not path.exists():
            path = next(CUSTOM_BLOCK.glob("block*.png"))
    elif name in ("ingot", "nugget", "gem") and ingot_profile:
        path = ICONSETS / ingot_profile / f"{src}.png"
    else:
        path = CUSTOM / f"{src}.png"
    arr = np.array(Image.open(path).convert("RGBA"), dtype=np.float32)
    return arr[:arr.shape[1]]


def geometry(base):
    h, w = base.shape[:2]
    a = base[..., 3] > 0
    gray = base[..., :3].mean(axis=2) / 255.0
    y, x = np.mgrid[:h, :w].astype(np.float32)
    cy, cx = (y[a].mean(), x[a].mean()) if a.any() else (h / 2, w / 2)
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    rmax = max(1.0, r[a].max()) if a.any() else 8.0
    edge = a & (~np.roll(a, 1, 0) | ~np.roll(a, -1, 0) | ~np.roll(a, 1, 1) | ~np.roll(a, -1, 1))
    return a, gray, x, y, cx, cy, r / rmax, np.arctan2(y - cy, x - cx), edge


def finish(base, r, g, b):
    a = base[..., 3]
    out = np.zeros(base.shape, dtype=np.float32)
    out[..., 0] = np.where(a > 0, r, 0)
    out[..., 1] = np.where(a > 0, g, 0)
    out[..., 2] = np.where(a > 0, b, 0)
    out[..., 3] = a
    return np.clip(out, 0, 255).astype(np.uint8)


def ramp(v, stops):
    pos = [p for p, _ in stops]
    return [np.interp(v, pos, [c[k] for _, c in stops]) for k in range(3)]


def _halo_grid():
    y, x = np.mgrid[:HALO_SIZE, :HALO_SIZE].astype(np.float32)
    c = (HALO_SIZE - 1) / 2
    dx, dy = (x - c) / c, (y - c) / c
    return np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx), dx, dy


# ==============================================================================================
# 36 HALOS (Unique formulas for each option)
# ==============================================================================================

def halo_gen(mat, opt, f):
    t = f / FRAMES
    rr, ang, dx, dy = _halo_grid()
    
    if mat == "nexium":
        if opt == 1: # Dipole field lines
            rot = ang + 2 * np.pi * t * 0.25
            psi = np.sin(rot) ** 2 / np.maximum(rr, 0.05)
            lines = np.exp(-((np.mod(psi * 1.2 - t, 1.0) - 0.5) / 0.12) ** 2)
            fade = np.clip((rr - 0.42) / 0.2, 0, 1) * np.clip((1 - rr) / 0.25, 0, 1)
            hue = np.mod(t + ang / (2 * np.pi), 1.0)
            r = np.interp(hue, [0, .33, .66, 1], [40, 60, 160, 40])
            g = np.interp(hue, [0, .33, .66, 1], [230, 140, 100, 230])
            b = np.interp(hue, [0, .33, .66, 1], [210, 255, 255, 210])
            alpha = np.clip(lines * fade * 0.9 + np.clip(1 - rr, 0, 1) ** 2 * 0.35, 0, 1)
            return np.dstack([r, g, b, alpha * 255])
        elif opt == 2: # Flux rings expanding
            r_ring = (t * 0.8 + 0.2) % 0.8
            ring = np.exp(-((rr - r_ring) / 0.06) ** 2)
            alpha = ring * np.clip(1 - rr, 0, 1) * 0.9
            return np.dstack([50 + 100 * rr, 180 + 70 * np.sin(ang), 230 * np.ones_like(rr), alpha * 255])
        else: # Cryo aurora
            wisp = np.sin(ang * 4 + 2 * np.pi * t) * 0.15
            alpha = np.clip(1 - (rr + wisp) / 0.85, 0, 1) ** 2 * 0.7
            return np.dstack([30 * np.ones_like(rr), 240 * np.ones_like(rr), 220 * np.ones_like(rr), alpha * 255])

    elif mat == "primordial_tholin":
        if opt == 1: # Frost haze
            rng = np.random.default_rng(int(t * 10))
            specks = np.clip(1 - rr / 0.75, 0, 1) ** 3 * (0.4 + 0.6 * np.sin(ang * 3 + t * 4))
            return np.dstack([210 * np.ones_like(rr), 120 * np.ones_like(rr), 80 * np.ones_like(rr), specks * 180])
        elif opt == 2: # Amber corona
            pulse = 0.5 + 0.5 * np.sin(2 * np.pi * t)
            alpha = np.clip(1 - rr / 0.8, 0, 1) ** 2 * (0.3 + 0.4 * pulse)
            return np.dstack([240 * np.ones_like(rr), 130 * np.ones_like(rr), 30 * np.ones_like(rr), alpha * 255])
        else: # Comet tail
            tail = np.exp(-((dx - 0.2) / 0.3) ** 2) * np.clip(-dy, 0, 1) * np.clip(1 - rr, 0, 1)
            return np.dstack([220 * np.ones_like(rr), 90 * np.ones_like(rr), 50 * np.ones_like(rr), tail * 200])

    elif mat == "magnetar_crystal":
        if opt == 1: # Pulsar beams
            turn = np.mod(ang / (2 * np.pi) - t, 0.5)
            beam = np.exp(-((turn - 0.25) / 0.032) ** 2) * np.clip(rr - 0.25, 0, 1) * 2.6
            trail = np.where((turn > 0.25) & (turn < 0.4), np.exp(-(turn - 0.25) / 0.04), 0) * 0.9 * np.clip(rr - 0.25, 0, 1)
            flare = np.cos(2 * np.pi * t * 2) ** 12
            disc = np.clip(1 - rr, 0, 1) ** 1.8 * (0.45 + 0.45 * flare)
            alpha = np.clip(beam + trail + disc, 0, 1) * np.clip((1 - rr) / 0.15, 0, 1)
            return np.dstack([160 * np.ones_like(rr), 90 * np.ones_like(rr), 255 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Relativistic spiral
            spiral = np.sin(ang * 2 - rr * 8 + 2 * np.pi * t * 2) * 0.5 + 0.5
            alpha = spiral * np.clip(1 - rr / 0.85, 0, 1) ** 1.5 * 0.8
            return np.dstack([120 * np.ones_like(rr), 50 * np.ones_like(rr), 240 * np.ones_like(rr), alpha * 255])
        else: # Magnetic cage
            grid = (np.abs(np.sin(dx * 12 + t * 4)) < 0.2) | (np.abs(np.sin(dy * 12 - t * 4)) < 0.2)
            alpha = grid * np.clip(1 - rr / 0.75, 0, 1) * 0.65
            return np.dstack([190 * np.ones_like(rr), 120 * np.ones_like(rr), 255 * np.ones_like(rr), alpha * 255])

    elif mat == "degenerate_core_matter":
        if opt == 1: # Inward compression rings
            rings = sum(np.exp(-((rr - (1.0 - ((t + k / 3) % 1.0) * 0.6)) / 0.05) ** 2) * (1 - (t + k / 3) % 1.0) ** 0.6 for k in range(3))
            core = np.clip(1 - rr, 0, 1) ** 2 * 0.6
            alpha = np.clip(rings * 1.3 + core, 0, 1) * np.clip((1 - rr) / 0.12, 0, 1)
            return np.dstack([170 * np.ones_like(rr), 190 * np.ones_like(rr), 255 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Graviton lens
            ring = np.exp(-((rr - 0.55) / 0.04) ** 2) * 0.9
            halo = np.clip(1 - rr / 0.9, 0, 1) ** 3 * 0.4
            return np.dstack([210 * np.ones_like(rr), 230 * np.ones_like(rr), 255 * np.ones_like(rr), (ring + halo) * 255])
        else: # Subatomic cloud
            flicker = np.sin(rr * 14 - 2 * np.pi * t * 3) * 0.5 + 0.5
            alpha = flicker * np.clip(1 - rr / 0.8, 0, 1) ** 2 * 0.8
            return np.dstack([240 * np.ones_like(rr), 245 * np.ones_like(rr), 255 * np.ones_like(rr), alpha * 255])

    elif mat == "magnetarium":
        if opt == 1: # Dipole torus
            torus = np.exp(-((rr - 0.5) / 0.12) ** 2) * (np.sin(ang * 2 + 2 * np.pi * t) * 0.3 + 0.7)
            return np.dstack([90 * np.ones_like(rr), 70 * np.ones_like(rr), 230 * np.ones_like(rr), torus * 220])
        elif opt == 2: # Flux cage
            lines = (np.abs(np.sin(ang * 6 + 2 * np.pi * t)) < 0.25) * np.clip(1 - rr, 0, 1)
            return np.dstack([140 * np.ones_like(rr), 100 * np.ones_like(rr), 255 * np.ones_like(rr), lines * 200])
        else: # Meissner field
            shell = np.exp(-((rr - 0.65) / 0.03) ** 2) * (0.8 + 0.2 * np.sin(t * 8))
            return np.dstack([70 * np.ones_like(rr), 150 * np.ones_like(rr), 255 * np.ones_like(rr), shell * 240])

    elif mat == "prismatium":
        if opt == 1: # Rainbow corona
            hue = np.mod(ang / (2 * np.pi) + t, 1.0)
            r = np.interp(hue, [0, .17, .33, .5, .67, .83, 1], [255, 255, 0, 0, 0, 255, 255])
            g = np.interp(hue, [0, .17, .33, .5, .67, .83, 1], [0, 255, 255, 255, 0, 0, 0])
            b = np.interp(hue, [0, .17, .33, .5, .67, .83, 1], [0, 0, 0, 255, 255, 255, 0])
            alpha = np.clip(1 - rr / 0.85, 0, 1) ** 2 * 0.75
            return np.dstack([r, g, b, alpha * 255])
        elif opt == 2: # Caustic star flare
            star = np.exp(-((np.abs(dx * dy) - 0.02) / 0.03) ** 2) * np.clip(1 - rr, 0, 1)
            return np.dstack([220 * np.ones_like(rr), 240 * np.ones_like(rr), 255 * np.ones_like(rr), star * 230])
        else: # Newton rings
            rings = (np.sin(rr * 22 - 2 * np.pi * t * 2) * 0.5 + 0.5) * np.clip(1 - rr / 0.8, 0, 1)
            return np.dstack([190 * np.ones_like(rr), 210 * np.ones_like(rr), 255 * np.ones_like(rr), rings * 190])

    elif mat == "chronomercury":
        if opt == 1: # Hourglass vortex
            swirl = np.sin(ang * 3 + rr * 6 - 2 * np.pi * t * 2) * 0.5 + 0.5
            alpha = swirl * np.clip(1 - rr / 0.8, 0, 1) * 0.8
            return np.dstack([190 * np.ones_like(rr), 200 * np.ones_like(rr), 220 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Dilation rings
            d_ring = np.exp(-((rr - (0.7 - t * 0.5)) / 0.05) ** 2)
            return np.dstack([160 * np.ones_like(rr), 180 * np.ones_like(rr), 210 * np.ones_like(rr), d_ring * 220])
        else: # Tachyon wave
            tach = (np.sin(dx * 16 - 2 * np.pi * t * 3) * 0.5 + 0.5) * np.clip(1 - rr, 0, 1)
            return np.dstack([210 * np.ones_like(rr), 220 * np.ones_like(rr), 240 * np.ones_like(rr), tach * 180])

    elif mat == "forgecore":
        if opt == 1: # Coronal loops
            loops = np.sin(ang * 4 + np.sin(rr * 6) * 2 + 2 * np.pi * t) * 0.5 + 0.5
            alpha = loops * np.clip(1 - rr / 0.85, 0, 1) ** 1.5 * 0.85
            return np.dstack([255 * np.ones_like(rr), 90 * np.ones_like(rr), 20 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Heat shimmer
            shimmer = np.clip(1 - rr / 0.8, 0, 1) ** 2 * (0.5 + 0.5 * np.sin(dy * 10 + t * 8))
            return np.dstack([255 * np.ones_like(rr), 140 * np.ones_like(rr), 30 * np.ones_like(rr), shimmer * 220])
        else: # Crucible flare
            burst = np.exp(-((rr - 0.45) / 0.1) ** 2) * (0.6 + 0.4 * np.sin(2 * np.pi * t * 2))
            return np.dstack([255 * np.ones_like(rr), 180 * np.ones_like(rr), 50 * np.ones_like(rr), burst * 240])

    elif mat == "vivispore":
        if opt == 1: # Spore drift
            drift = np.sin(dx * 8 + dy * 6 + 2 * np.pi * t) * 0.5 + 0.5
            alpha = drift * np.clip(1 - rr / 0.8, 0, 1) ** 2 * 0.75
            return np.dstack([90 * np.ones_like(rr), 220 * np.ones_like(rr), 40 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Bio aura
            pulse = np.sin(2 * np.pi * t) * 0.1
            alpha = np.clip(1 - (rr + pulse) / 0.75, 0, 1) ** 2 * 0.65
            return np.dstack([60 * np.ones_like(rr), 190 * np.ones_like(rr), 50 * np.ones_like(rr), alpha * 255])
        else: # Toxic phosphor
            toxic = (np.sin(ang * 5 - rr * 6 + t * 4) * 0.5 + 0.5) * np.clip(1 - rr / 0.85, 0, 1)
            return np.dstack([140 * np.ones_like(rr), 255 * np.ones_like(rr), 60 * np.ones_like(rr), toxic * 210])

    elif mat == "abyssal_antimatter":
        if opt == 1: # Hawking radiation
            glow = np.clip(1 - rr / 0.85, 0, 1) ** 2.5 * 0.8
            return np.dstack([160 * np.ones_like(rr), 40 * np.ones_like(rr), 230 * np.ones_like(rr), glow * 255])
        elif opt == 2: # Cherenkov burst
            burst = np.exp(-((rr - 0.4) / 0.08) ** 2) * (0.6 + 0.4 * np.cos(2 * np.pi * t * 3) ** 4)
            return np.dstack([100 * np.ones_like(rr), 60 * np.ones_like(rr), 255 * np.ones_like(rr), burst * 240])
        else: # Event horizon
            ring = np.exp(-((rr - 0.58) / 0.025) ** 2) * 0.95
            return np.dstack([210 * np.ones_like(rr), 120 * np.ones_like(rr), 255 * np.ones_like(rr), ring * 255])

    elif mat == "precursor_residue":
        if opt == 1: # Schematic grid
            grid = (np.abs(np.sin(dx * 14)) < 0.18) | (np.abs(np.sin(dy * 14)) < 0.18)
            alpha = grid * np.clip(1 - rr / 0.8, 0, 1) * 0.6
            return np.dstack([220 * np.ones_like(rr), 180 * np.ones_like(rr), 80 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Glyph circle
            circle = np.exp(-((rr - 0.55) / 0.03) ** 2) * (np.sin(ang * 12 + 2 * np.pi * t) * 0.4 + 0.6)
            return np.dstack([230 * np.ones_like(rr), 190 * np.ones_like(rr), 90 * np.ones_like(rr), circle * 230])
        else: # Nanite swarm
            swarm = (np.sin(dx * 10 - t * 6) * np.sin(dy * 10 + t * 6) > 0.4) * np.clip(1 - rr, 0, 1)
            return np.dstack([240 * np.ones_like(rr), 200 * np.ones_like(rr), 110 * np.ones_like(rr), swarm * 210])

    elif mat == "void_ash":
        if opt == 1: # Rising cinders
            cinder = np.sin(dx * 8 + (dy - t * 2) * 8) * 0.5 + 0.5
            alpha = cinder ** 3 * np.clip(1 - rr / 0.8, 0, 1) * 0.6
            return np.dstack([120 * np.ones_like(rr), 120 * np.ones_like(rr), 150 * np.ones_like(rr), alpha * 255])
        elif opt == 2: # Entropy sink
            sink = np.clip(rr / 0.8, 0, 1) * (1 - np.clip(rr / 0.8, 0, 1)) * 3.5 * (np.sin(ang * 2 - rr * 5 + t * 4) * 0.3 + 0.7)
            return np.dstack([80 * np.ones_like(rr), 80 * np.ones_like(rr), 110 * np.ones_like(rr), sink * 200])
        else: # Dark energy fracture
            fissure = (np.abs(dx + np.sin(dy * 5) * 0.2) < 0.12) * np.clip(1 - rr / 0.8, 0, 1)
            return np.dstack([100 * np.ones_like(rr), 100 * np.ones_like(rr), 140 * np.ones_like(rr), fissure * 210])

    return np.zeros((HALO_SIZE, HALO_SIZE, 4), dtype=np.uint8)


# ==============================================================================================
# 36 TEXTURE OPTIONS (12 Materials x 3 Concepts)
# ==============================================================================================

# Palettes
P_NEXIUM = [(0.0, (3, 22, 26)), (0.28, (8, 70, 72)), (0.55, (24, 160, 150)), (0.8, (96, 232, 214)), (1.0, (226, 255, 250))]
P_THOLIN = [(0.0, (28, 5, 6)), (0.3, (88, 18, 16)), (0.55, (146, 40, 30)), (0.8, (194, 92, 68)), (1.0, (236, 178, 148))]
P_MAGNETAR = [(0.0, (12, 4, 36)), (0.28, (46, 18, 120)), (0.55, (104, 66, 226)), (0.8, (176, 150, 255)), (1.0, (244, 238, 255))]
P_DEGENERATE = [(0.0, (10, 12, 32)), (0.3, (40, 50, 108)), (0.55, (110, 128, 200)), (0.8, (196, 210, 252)), (1.0, (255, 255, 255))]
P_MAGNETARIUM = [(0.0, (14, 9, 38)), (0.28, (45, 32, 110)), (0.55, (95, 75, 210)), (0.8, (165, 150, 255)), (1.0, (240, 235, 255))]
P_PRISMATIUM = [(0.0, (20, 25, 45)), (0.3, (65, 90, 145)), (0.6, (140, 180, 230)), (0.85, (215, 235, 255)), (1.0, (255, 255, 255))]
P_CHRONOMERCURY = [(0.0, (22, 25, 32)), (0.28, (65, 75, 92)), (0.55, (128, 142, 165)), (0.8, (195, 208, 225)), (1.0, (255, 255, 255))]
P_FORGECORE = [(0.0, (38, 6, 0)), (0.28, (130, 32, 0)), (0.55, (235, 85, 10)), (0.8, (255, 180, 60)), (1.0, (255, 245, 180))]
P_VIVISPORE = [(0.0, (12, 26, 6)), (0.28, (45, 90, 20)), (0.55, (105, 180, 45)), (0.8, (185, 238, 100)), (1.0, (235, 255, 190))]
P_ABYSSAL = [(0.0, (4, 1, 8)), (0.28, (24, 10, 44)), (0.55, (68, 28, 115)), (0.8, (155, 75, 235)), (1.0, (235, 180, 255))]
P_PRECURSOR = [(0.0, (38, 25, 8)), (0.28, (95, 68, 24)), (0.55, (170, 132, 58)), (0.8, (228, 195, 115)), (1.0, (252, 240, 192))]
P_VOID_ASH = [(0.0, (3, 3, 5)), (0.28, (16, 16, 24)), (0.55, (38, 38, 50)), (0.8, (88, 88, 110)), (1.0, (155, 155, 185))]


def render_material_frame(mat, opt, base, f):
    a, gray, x, y, cx, cy, nd, ang, edge = geometry(base)
    t = f / FRAMES
    
    if mat == "nexium":
        r, g, b = ramp(gray, P_NEXIUM)
        if opt == 1: # Current sweep
            band = np.exp(-(((x + y) - (t * 44 - 10)) / 2.2) ** 2) * np.clip(gray - 0.35, 0, 1) * 1.6
            spark = edge * np.where(((t - (ang / (2 * np.pi)) % 1.0) % 1.0) < 0.08, 1, 0)
            r, g, b = r + band * 120 + spark * 90, g + band * 160 + spark * 200, b + band * 150 + spark * 190
        elif opt == 2: # Field memory iridescence
            phase = (t + (x + y) / 48.0) % 1.0
            r = r + np.sin(2 * np.pi * phase) * 30
            g = g + np.sin(2 * np.pi * (phase + 0.33)) * 30
            b = b + np.sin(2 * np.pi * (phase + 0.66)) * 40
        else: # Cryo glint
            glint = np.maximum(0.0, np.cos(2 * np.pi * (t - nd * 1.5))) ** 12 * np.clip(gray - 0.3, 0, 1) * 200
            r, g, b = r + glint * 0.7, g + glint * 0.9, b + glint

    elif mat == "primordial_tholin":
        r, g, b = ramp(gray, P_THOLIN)
        if opt == 1: # Frost glints
            glint = np.maximum(0.0, np.cos(2 * np.pi * (t * 2 + (x * 3 + y * 7) / 16))) ** 16 * (gray > 0.4) * 220
            r, g, b = r + glint * 0.7, g + glint * 0.85, b + glint
        elif opt == 2: # Polymerizing veins
            vein = (np.abs(np.sin(x * 1.2 + y * 0.8)) < 0.25) * (0.5 + 0.5 * np.sin(2 * np.pi * t))
            r, g, b = r + vein * 160, g + vein * 100, b + vein * 20
        else: # Sublimation wisp
            wisp = np.sin((y + t * 16) * 0.8 + x) * 0.5 + 0.5
            haze = wisp ** 3 * (1 - y / 16) * 70
            r, g, b = r + haze * 1.1, g + haze * 0.8, b + haze * 0.7

    elif mat == "magnetar_crystal":
        r, g, b = ramp(gray, P_MAGNETAR)
        if opt == 1: # Inverted dipole wave
            wave = (np.sin(2 * np.pi * (nd * 2.0 - t * 2)) * 0.5 + 0.5) ** 3 * (0.3 + 0.7 * gray)
            r, g, b = r + wave * 130, g + wave * 100, b + wave * 80
        elif opt == 2: # Lighthouse beam
            turn = np.mod(ang / (2 * np.pi) - t * 2, 0.5)
            beam = np.exp(-((turn - 0.25) / 0.035) ** 2) * (0.3 + 0.7 * gray)
            r, g, b = r + beam * 150, g + beam * 140, b + beam * 110
        else: # Fracture discharge
            crack = (np.abs(np.sin(x * 1.2 - y * 1.5)) < 0.2) * (np.sin(2 * np.pi * (t * 3 + x * 0.2)) > 0.7)
            r, g, b = r + crack * 160, g + crack * 200, b + crack * 240

    elif mat == "degenerate_core_matter":
        r, g, b = ramp(gray ** 1.2, P_DEGENERATE)
        if opt == 1: # Fermi shimmer & inward flash
            front = np.exp(-((nd - (1 - t)) / 0.09) ** 2) * 80
            flash = np.exp(-nd * 5) * max(0.0, 1 - abs(t - 0.95) * 12) * 120
            r, g, b = r + front + flash, g + front + flash, b + front + flash
        elif opt == 2: # Einstein lens ring
            ring = np.exp(-((nd - 0.45) / 0.08) ** 2) * 100
            r, g, b = r + ring * 0.8, g + ring * 0.9, b + ring
        else: # Subatomic charge wander
            px = cx + np.cos(2 * np.pi * t) * 4
            py = cy + np.sin(2 * np.pi * t) * 4
            spot = np.exp(-((x - px) ** 2 + (y - py) ** 2) / 2.0) * a * 120
            r, g, b = r + spot * 0.8, g + spot * 0.9, b + spot

    elif mat == "magnetarium":
        r, g, b = ramp(gray, P_MAGNETARIUM)
        if opt == 1: # Lorentz force wave
            lorentz = (np.sin((x - y) * 0.8 + 2 * np.pi * t * 2) * 0.5 + 0.5) ** 2 * 90
            r, g, b = r + lorentz * 0.5, g + lorentz * 0.4, b + lorentz
        elif opt == 2: # Ferrofluid spike
            spike = (np.sin(x * 1.5) * np.sin(y * 1.5) * np.sin(2 * np.pi * t)) > 0.4
            r, g, b = r + spike * 80, g + spike * 70, b + spike * 140
        else: # Meissner edge glow
            repulse = edge * (0.6 + 0.4 * np.sin(2 * np.pi * t * 2)) * 120
            r, g, b = r + repulse * 0.4, g + repulse * 0.7, b + repulse

    elif mat == "prismatium":
        if opt == 1: # Full rainbow cycle
            hue = (t + (x + y) / 32.0) % 1.0
            pr, pg, pb = [np.array(c) for c in zip(*[colorsys.hls_to_rgb(h, max(0.2, min(0.8, g)), 0.75) for h, g in zip(hue.flat, gray.flat)])]
            r, g, b = pr.reshape(gray.shape) * 255, pg.reshape(gray.shape) * 255, pb.reshape(gray.shape) * 255
        elif opt == 2: # Caustic star flare
            r, g, b = ramp(gray, P_PRISMATIUM)
            flare = np.maximum(0.0, np.cos(2 * np.pi * (t - nd))) ** 8 * 140
            r, g, b = r + flare * 0.9, g + flare, b + flare
        else: # Chirality interference
            r, g, b = ramp(gray, P_PRISMATIUM)
            interf = (np.sin(nd * 12 - 2 * np.pi * t * 2) * 0.5 + 0.5) * 80
            r, g, b = r + interf * 0.7, g + interf * 0.8, b + interf

    elif mat == "chronomercury":
        r, g, b = ramp(gray, P_CHRONOMERCURY)
        if opt == 1: # Reverse time sweep
            sweep = np.exp(-(((x - y) - ((1 - t) * 40 - 20)) / 2.0) ** 2) * 120
            r, g, b = r + sweep, g + sweep, b + sweep
        elif opt == 2: # Temporal ghost echo
            echo = np.sin(nd * 8 + 2 * np.pi * t * 2) * 35
            r, g, b = r + echo, g + echo, b + echo
        else: # Tachyon phase shift
            phase = (np.sin(2 * np.pi * (t * 2 + x * 0.2)) > 0) * 45
            r, g, b = r + phase * 0.9, g + phase, b + phase

    elif mat == "forgecore":
        r, g, b = ramp(gray, P_FORGECORE)
        if opt == 1: # Solar granulation boil
            boil = (np.sin(x * 1.4 + t * 6) * np.sin(y * 1.4 - t * 6)) * 40
            r, g, b = r + boil * 1.2, g + boil * 0.8, b + boil * 0.2
        elif opt == 2: # Thermonuclear core pulse
            pulse = (0.5 + 0.5 * np.sin(2 * np.pi * t * 2)) * (1 - nd) * 110
            r, g, b = r + pulse * 1.2, g + pulse * 0.9, b + pulse * 0.4
        else: # Crucible flame spark
            spark = edge * (np.sin(2 * np.pi * (t * 3 + y * 0.3)) > 0.6) * 130
            r, g, b = r + spark * 1.2, g + spark * 0.8, b + spark * 0.1

    elif mat == "vivispore":
        r, g, b = ramp(gray, P_VIVISPORE)
        if opt == 1: # Mycelial respiration
            breath = (0.5 + 0.5 * np.sin(2 * np.pi * t)) * (gray > 0.35) * 75
            r, g, b = r + breath * 0.3, g + breath, b + breath * 0.4
        elif opt == 2: # Bioluminescent cascade
            casc = (np.sin(x * 1.1 + y * 1.3 - 2 * np.pi * t * 2) > 0.5) * 80
            r, g, b = r + casc * 0.4, g + casc, b + casc * 0.5
        else: # Toxic phosphor flash
            flash = (np.sin(2 * np.pi * (t * 3 + (x * 5 + y * 11) / 16)) > 0.8) * 110
            r, g, b = r + flash * 0.6, g + flash, b + flash * 0.2

    elif mat == "abyssal_antimatter":
        r, g, b = ramp(gray, P_ABYSSAL)
        if opt == 1: # Vacuum void & gamma spark
            spark = (np.sin(2 * np.pi * (t * 4 + x * 0.7 + y * 1.1)) > 0.85) * 150
            r, g, b = r + spark * 0.7, g + spark * 0.4, b + spark
        elif opt == 2: # Cherenkov radiation burst
            burst = (0.5 + 0.5 * np.sin(2 * np.pi * (t * 2 - nd * 2))) * 70
            r, g, b = r + burst * 0.5, g + burst * 0.3, b + burst
        else: # Event horizon shadow
            edge_l = edge * 90
            r, g, b = r + edge_l * 0.8, g + edge_l * 0.5, b + edge_l

    elif mat == "precursor_residue":
        r, g, b = ramp(gray, P_PRECURSOR)
        if opt == 1: # Nano-bus logic trace
            trace = ((np.abs(np.sin(x * 1.5)) < 0.2) | (np.abs(np.sin(y * 1.5)) < 0.2)) * (np.sin(2 * np.pi * (t * 2 + x * 0.1)) > 0.3) * 90
            r, g, b = r + trace * 1.1, g + trace * 0.9, b + trace * 0.4
        elif opt == 2: # Runic scan line
            scan = np.exp(-((y - ((t * 20) % 18)) / 1.5) ** 2) * 100
            r, g, b = r + scan * 1.1, g + scan * 0.95, b + scan * 0.5
        else: # Nanite cube shimmer
            cube = ((x.astype(int) + y.astype(int) + int(t * 8)) % 3 == 0) * 60
            r, g, b = r + cube * 1.1, g + cube * 0.9, b + cube * 0.4

    elif mat == "void_ash":
        r, g, b = ramp(gray, P_VOID_ASH)
        if opt == 1: # Cold cinder rise
            rise = (np.sin(x * 1.5 + (y - t * 16) * 1.2) > 0.6) * 60
            r, g, b = r + rise * 0.8, g + rise * 0.8, b + rise
        elif opt == 2: # Entropy dissolution
            diss = (np.sin(2 * np.pi * t) * 0.5 + 0.5) * (gray < 0.5) * 45
            r, g, b = r + diss * 0.9, g + diss * 0.9, b + diss * 1.1
        else: # Dark energy fracture
            fiss = (np.abs(x - y) < 1.2) * (np.sin(2 * np.pi * t * 2) * 0.5 + 0.5) * 70
            r, g, b = r + fiss * 0.7, g + fiss * 0.7, b + fiss

    return finish(base, r, g, b)


# ==============================================================================================
# PREVIEW COMPOSITOR (Slot + Halo + Icon + Glow Edge)
# ==============================================================================================

def make_slot_preview(icon_frame, halo_frame, opt, glow_color=None):
    cell = Image.new("RGBA", (CELL, CELL), (198, 198, 198, 255))
    slot = Image.new("RGBA", (18, 18), (139, 139, 139, 255))
    cell.alpha_composite(slot, (7, 7))
    
    # 1. Halo behind (scaled to fit slot)
    halo_img = Image.fromarray(halo_frame, "RGBA").resize((28, 28), Image.BILINEAR)
    cell.alpha_composite(halo_img, (2, 2))
    
    # 2. Icon in center
    icon = Image.fromarray(icon_frame, "RGBA")
    cell.alpha_composite(icon, (8, 8))
    
    # 3. Optional glow edge
    if glow_color:
        edge_img = icon.resize((18, 18), Image.NEAREST)
        # Tint glow edge
        arr = np.array(edge_img, dtype=np.float32)
        arr[..., 0] *= (glow_color >> 16 & 255) / 255
        arr[..., 1] *= (glow_color >> 8 & 255) / 255
        arr[..., 2] *= (glow_color & 255) / 255
        arr[..., 3] *= 0.45
        edge_tinted = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
        cell.alpha_composite(edge_tinted, (7, 7))
        cell.alpha_composite(icon, (8, 8)) # Re-paste icon on top
        
    return cell


# ==============================================================================================
# SPECIFICATIONS & METADATA
# ==============================================================================================

PROPOSALS = {
    "nexium": {
        "title": "Nexium (Nx)",
        "machine": "Kinetic Orbital Lance (Nexus-1)",
        "lore": "Metal supercondutor que preserva o vetor de todo campo magnético ou elétrico já atravessado.",
        "profile": "SHINY",
        "primary_form": "ingot",
        "options": [
            {
                "name": "Current Sweep (Varredura de Corrente)",
                "desc": "Teal metálico frio com feixe de corrente contínua varrendo em diagonal e faíscas azuis nas bordas.",
                "halo_name": "nexium_field",
                "halo_desc": "Linhas de dipolo magnético em rotação contínua ao redor do item.",
                "glow_color": 0x24d4c4,
                "accent": "#167a76"
            },
            {
                "name": "Field Memory (Memória de Campo)",
                "desc": "Filme fino iridescente com transição espectral suave ondulando na superfície do metal.",
                "halo_name": "nexium_flux_ring",
                "halo_desc": "Anéis concêntricos de fluxo magnético que expandem suavemente.",
                "glow_color": 0x38bdf8,
                "accent": "#0284c7"
            },
            {
                "name": "Cryo Glint (Cintilação Criogênica)",
                "desc": "Ciano profundo com lentes de difração térmicas e 5 estrelas de glint que acendem em cascata.",
                "halo_name": "nexium_aurora",
                "halo_desc": "Névoa de plasma eletrostático pulsante em tom ciano-celeste.",
                "glow_color": 0x67e8f9,
                "accent": "#0891b2"
            }
        ]
    },
    "primordial_tholin": {
        "title": "Primordial Tholin",
        "machine": "Kinetic Orbital Lance (Arrokoth)",
        "lore": "Polímeros orgânicos complexos criados por radiação solar sobre gelos voláteis do Cinturão de Kuiper.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Methane Frost (Gelos de Metano)",
                "desc": "Crosta vermelho-tijolo escura com micro-cristais de gelo que reluzem em branco-azulado.",
                "halo_name": "tholin_frost_haze",
                "halo_desc": "Poeira estelar fria dispersa em micro-partículas.",
                "glow_color": 0xecb294,
                "accent": "#a8432a"
            },
            {
                "name": "Polymerizing Veins (Veios em Cadeia)",
                "desc": "Veios de carbono e nitrogênio que pulsam em âmbar profundo simulando fotoquímica ativa.",
                "halo_name": "tholin_amber_corona",
                "halo_desc": "Corona difusa de calor âmbar pulsando suavemente.",
                "glow_color": 0xf59e0b,
                "accent": "#b45309"
            },
            {
                "name": "Sublimation Jets (Jatos de Sublimação)",
                "desc": "Filamentos tênues de vapor de nitrogênio e metano subindo verticalmente dos grãos.",
                "halo_name": "tholin_comet_tail",
                "halo_desc": "Cauda cometária assimétrica projetada para cima.",
                "glow_color": 0xfb7185,
                "accent": "#e11d48"
            }
        ]
    },
    "magnetar_crystal": {
        "title": "Magnetar Crystal",
        "machine": "Stellar Containment Chamber (Starquake)",
        "lore": "Gema ferro-cristalina sintetizada sob as forças gravitacionais e magnéticas de um terremoto estelar.",
        "profile": "GEM_HORIZONTAL",
        "primary_form": "gem",
        "options": [
            {
                "name": "Inverted Dipole (Dipolo Invertido)",
                "desc": "Púrpura cósmico profundo com ondas de choque magnéticas que viajam do núcleo para os ápices.",
                "halo_name": "magnetar_pulsar",
                "halo_desc": "Dois jatos relativísticos de pulsar girando em 180°.",
                "glow_color": 0xa855f7,
                "accent": "#6b21a8"
            },
            {
                "name": "Lighthouse Beam (Farol Relativístico)",
                "desc": "Dois feixes de alta energia varrendo a linha de visão do jogador com flash intenso no topo.",
                "halo_name": "magnetar_relativistic_jets",
                "halo_desc": "Espirais relativísticas projetadas com disco de acreção.",
                "glow_color": 0xc084fc,
                "accent": "#7e22ce"
            },
            {
                "name": "Starquake Fracture (Fratura de Tensão)",
                "desc": "Trincas de choque cristalino liberando descargas e centelhas violeta de altíssima tensão.",
                "halo_name": "magnetar_magnetic_cage",
                "halo_desc": "Gaiola geométrica de linhas de força magnética entrelaçadas.",
                "glow_color": 0x818cf8,
                "accent": "#4338ca"
            }
        ]
    },
    "degenerate_core_matter": {
        "title": "Degenerate Core Matter (nₙ)",
        "machine": "Stellar Containment Chamber (Collapse)",
        "lore": "Matéria colapsada em densidade nuclear máxima, mantida por pressão de degenerescência de nêutrons.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Fermi Sea (Mar de Fermi)",
                "desc": "Branco-chumbo frio com cintilação quântica contínua e frente de compressão esférica.",
                "halo_name": "degenerate_compression",
                "halo_desc": "Anéis concêntricos de luz gravitacional caindo para o centro.",
                "glow_color": 0xe2e8f0,
                "accent": "#64748b"
            },
            {
                "name": "Einstein Ring (Anel Gravitacional)",
                "desc": "Lente gravitacional simulada com anel de curvatura de luz respirando ao redor do centro.",
                "halo_name": "degenerate_graviton_lens",
                "halo_desc": "Distorção ótica com arco estelar curvado no horizonte.",
                "glow_color": 0x93c5fd,
                "accent": "#2563eb"
            },
            {
                "name": "Quark Soup (Sopa de Quarks)",
                "desc": "Cores de carga quântica orbitando o centro denso e colidindo em flashes brancos.",
                "halo_name": "degenerate_subatomic_cloud",
                "halo_desc": "Nuvem de probabilidade quântica com micro-faíscas subatômicas.",
                "glow_color": 0xa5b4fc,
                "accent": "#4f46e5"
            }
        ]
    },
    "magnetarium": {
        "title": "Magnetarium",
        "machine": "Stellar Containment Chamber & Lance Slug",
        "lore": "Superliga ferromagnética densa projetada para projéteis de canhão orbital e armaduras extremas.",
        "profile": "SHINY",
        "primary_form": "ingot",
        "options": [
            {
                "name": "Lorentz Wave (Ondas de Lorentz)",
                "desc": "Índigo metálico escuro com faixas de fluxo de força de Lorentz varrendo longitudinalmente.",
                "halo_name": "magnetarium_dipole_torus",
                "halo_desc": "Toro magnético fechado oscilando suavemente.",
                "glow_color": 0x818cf8,
                "accent": "#3730a3"
            },
            {
                "name": "Ferrofluid Spikes (Picos Magnéticos)",
                "desc": "Picos espiculados de tensão ferromagnética erguendo-se e retraindo nas facetas.",
                "halo_name": "magnetarium_flux_cage",
                "halo_desc": "Gaiola geométrica de contenção com linhas de campo magnético.",
                "glow_color": 0x6366f1,
                "accent": "#312e81"
            },
            {
                "name": "Meissner Shield (Blindagem Diamagnética)",
                "desc": "Bordas em azul elétrico resplandecente com repulsão diamagnética perfeita.",
                "halo_name": "magnetarium_meissner_field",
                "halo_desc": "Escudo polar esférico translúcido com reflexo polar.",
                "glow_color": 0x38bdf8,
                "accent": "#0369a1"
            }
        ]
    },
    "prismatium": {
        "title": "Prismatium",
        "machine": "Dimensional Rift Gate",
        "lore": "Cristal hiperdimensional que decompõe a radiação local em dispersão cromática perpétua.",
        "profile": "DIAMOND",
        "primary_form": "gem",
        "options": [
            {
                "name": "Spectral Cycle (Dispersão Espectral)",
                "desc": "Cristal lapidado com ciclo completo de arco-íris refrativo girando pelas facetas internas.",
                "halo_name": "prismatium_rainbow_corona",
                "halo_desc": "Coroa iridescente de arco-íris circular em rotação contínua.",
                "glow_color": 0x38bdf8,
                "accent": "#0284c7"
            },
            {
                "name": "Caustic Flare (Cáusticas Prismáticas)",
                "desc": "Padrão de cáusticas de alta intensidade convergindo para os vértices do cristal.",
                "halo_name": "prismatium_caustic_flare",
                "halo_desc": "Raios de difração em cruz com separação de cores.",
                "glow_color": 0xa7f3d0,
                "accent": "#059669"
            },
            {
                "name": "Chirality Waves (Ondas Quirais)",
                "desc": "Interferência harmônica de polarização circular esquerda e direita nas facetas.",
                "halo_name": "prismatium_interference_rings",
                "halo_desc": "Anéis concêntricos de interferência de Newton.",
                "glow_color": 0xf472b6,
                "accent": "#db2777"
            }
        ]
    },
    "chronomercury": {
        "title": "Chronomercury (Hg⧖)",
        "machine": "Dimensional Rift Gate",
        "lore": "Metal líquido de entropia invertida cujas propriedades físicas reagem contra o fluxo do tempo.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Retrograde Sweep (Varredura Retrógrada)",
                "desc": "Prata cromada pura com reflexos especulares correndo no sentido anti-horário (tempo reverso).",
                "halo_name": "chronomercury_hourglass_vortex",
                "halo_desc": "Espiral temporal em contração contínua em direção ao centro.",
                "glow_color": 0xe2e8f0,
                "accent": "#475569"
            },
            {
                "name": "Temporal Ghosting (Ecos Temporais)",
                "desc": "Réplicas translúcidas de frames anteriores convergindo e se unificando no corpo do grão.",
                "halo_name": "chronomercury_dilation_rings",
                "halo_desc": "Anéis de dilatação temporal com pulso de atraso de fase.",
                "glow_color": 0x94a3b8,
                "accent": "#334155"
            },
            {
                "name": "Tachyon Quicksilver (Mercúrio Taquiônico)",
                "desc": "Alternância rápida de fase entre líquido espelhado e estrias temporais de taquiões.",
                "halo_name": "chronomercury_tachyon_halo",
                "halo_desc": "Ondulações taquiônicas lineares com distorção de fase.",
                "glow_color": 0xcb99c9,
                "accent": "#70587c"
            }
        ]
    },
    "forgecore": {
        "title": "Forgecore",
        "machine": "Dimensional Rift Gate & Stellar Armour",
        "lore": "Matriz metálica hiper-termonuclear alimentada pelo plasma de forja dimensional.",
        "profile": "SHINY",
        "primary_form": "ingot",
        "options": [
            {
                "name": "Solar Granulation (Granulação Solar)",
                "desc": "Magma incandescente com células de convecção térmica fervendo nas facetas.",
                "halo_name": "forgecore_coronal_loops",
                "halo_desc": "Alças coronais de plasma que se projetam e reconectam.",
                "glow_color": 0xf97316,
                "accent": "#ea580c"
            },
            {
                "name": "Thermonuclear Core (Ignição Nuclear)",
                "desc": "Pulsação radiativa em branco-amarelo vivo emanando de blindagem de aço escuro.",
                "halo_name": "forgecore_heat_shimmer",
                "halo_desc": "Distorção térmica por convecção de ar e calor radiativo.",
                "glow_color": 0xfacc15,
                "accent": "#ca8a04"
            },
            {
                "name": "Crucible Flare (Cadinho de Plasma)",
                "desc": "Erupções de faíscas incandescentes canalizadas pelas ranhuras do metal.",
                "halo_name": "forgecore_crucible_flare",
                "halo_desc": "Coroa de chamas de plasma estelar de alta energia.",
                "glow_color": 0xef4444,
                "accent": "#dc2626"
            }
        ]
    },
    "vivispore": {
        "title": "Vivispore",
        "machine": "Dimensional Rift Gate",
        "lore": "Esporos xenobiológicos luminescentes colhidos em ecossistemas de micro-gravidade da fenda.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Mycelial Breath (Respiração Micelial)",
                "desc": "Verde musgo alienígena profundo com filamentos de micélio que respiram ritmicamente.",
                "halo_name": "vivispore_spore_drift",
                "halo_desc": "Nuvem viva de micro-esporos fosforescentes flutuando.",
                "glow_color": 0x84cc16,
                "accent": "#4d7c0f"
            },
            {
                "name": "Bio Bloom (Eflorescência Simbiótica)",
                "desc": "Centros de fluorescência biológica que acendem em cascata pelos grãos.",
                "halo_name": "vivispore_bio_aura",
                "halo_desc": "Aura orgânica ondulante com pulso biológico suave.",
                "glow_color": 0x22c55e,
                "accent": "#15803d"
            },
            {
                "name": "Toxic Phosphor (Fósforo Tóxico)",
                "desc": "Bioluminescência verde-limão com estalos químicos rápidos e centelhas enzimáticas.",
                "halo_name": "vivispore_toxic_phosphor",
                "halo_desc": "Anéis de descarga enzimática luminescente.",
                "glow_color": 0xa3e635,
                "accent": "#65a30d"
            }
        ]
    },
    "abyssal_antimatter": {
        "title": "Abyssal Antimatter (p̄ē)",
        "machine": "Dimensional Rift Gate",
        "lore": "Antimatéria barionicamente estável em vácuo abissal, com assinaturas de radiação gama.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Vacuum & Gamma (Vácuo e Raios Gama)",
                "desc": "Preto-vácuo absoluto com micro-flashes pontuais de aniquilação gama ultravioleta.",
                "halo_name": "abyssal_hawking_glow",
                "halo_desc": "Halo de radiação Hawking em violeta escuro ao redor do vácuo.",
                "glow_color": 0xa855f7,
                "accent": "#581c87"
            },
            {
                "name": "Cherenkov Burst (Cascata Cherenkov)",
                "desc": "Brilho penetrante azul-violeta emitido do núcleo para as extremidades dos grãos.",
                "halo_name": "abyssal_cherenkov_burst",
                "halo_desc": "Feixes de radiação Cherenkov com decaimento exponencial.",
                "glow_color": 0x6366f1,
                "accent": "#3730a3"
            },
            {
                "name": "Event Horizon (Horizonte de Eventos)",
                "desc": "Anel de contorno ultrafino hiperbrilhante contornando uma silhueta de escuridão total.",
                "halo_name": "abyssal_event_horizon",
                "halo_desc": "Anel hiperbrilhante fino contornando uma sombra escura.",
                "glow_color": 0xd8b4fe,
                "accent": "#7e22ce"
            }
        ]
    },
    "precursor_residue": {
        "title": "Precursor Residue (?)",
        "machine": "Dimensional Rift Gate",
        "lore": "Resíduos fossilizados de nano-máquinas e circuitos computacionais de civilizações precursoras.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Nano-Bus Traces (Barramento de Circuitos)",
                "desc": "Bronze dourado ancestral com trilhas lógicas de nanocircuitos que acendem em pulso.",
                "halo_name": "precursor_schematic_grid",
                "halo_desc": "Grade holográfica sutil de blueprint tecnológico flutuando.",
                "glow_color": 0xfacc15,
                "accent": "#a16207"
            },
            {
                "name": "Runic Decoding (Decodificação Rúnica)",
                "desc": "Micro-glifos horizontais que são lidos e iluminados sequencialmente em linhas de dados.",
                "halo_name": "precursor_glyph_circle",
                "halo_desc": "Anel de glifos ancestrais em rotação lenta.",
                "glow_color": 0xfde047,
                "accent": "#854d0e"
            },
            {
                "name": "Nanite Swarm (Enxame de Nanites)",
                "desc": "Poeira que se reorganiza periodicamente em micro-matrizes cúbicas ordenadas.",
                "halo_name": "precursor_nanite_swarm",
                "halo_desc": "Partículas cúbicas microscópicas orbitando o item.",
                "glow_color": 0xd97706,
                "accent": "#78350f"
            }
        ]
    },
    "void_ash": {
        "title": "Void Ash (∅)",
        "machine": "Dimensional Rift Gate",
        "lore": "Cinzas entrópicas sem massa restante, geradas após a evaporação completa de anomalias da fenda.",
        "profile": None,
        "primary_form": "dust",
        "options": [
            {
                "name": "Cold Cinders (Fuligem Ascendente)",
                "desc": "Cinza carvão fosco absoluto com micro-partículas subindo lentamente em gravidade zero.",
                "halo_name": "void_cold_cinder_aura",
                "halo_desc": "Motas pálidas e escuras flutuando em turbulência lenta.",
                "glow_color": 0x94a3b8,
                "accent": "#1e293b"
            },
            {
                "name": "Entropy Dissolution (Dissolução Entrópica)",
                "desc": "Bordas dos grãos que se dissolvem no vácuo e retornam em oscilação contínua.",
                "halo_name": "void_entropy_sink",
                "halo_desc": "Espiral de distorção de sucção de luz.",
                "glow_color": 0x64748b,
                "accent": "#0f172a"
            },
            {
                "name": "Dark Fracture (Fratura de Energia Escura)",
                "desc": "Fissuras dimensionais que cortam as cinzas com pulsação de energia escura fria.",
                "halo_name": "void_dark_fracture_halo",
                "halo_desc": "Rachaduras espaciais estáticas com pulsação de energia escura.",
                "glow_color": 0x475569,
                "accent": "#020617"
            }
        ]
    }
}


def main():
    print(f"Generating all 36 proposals across 12 materials into {PROPOSALS_DIR}...")
    manifest = {}

    for mat_id, meta in PROPOSALS.items():
        mat_dir = PROPOSALS_DIR / mat_id
        mat_dir.mkdir(parents=True, exist_ok=True)
        primary_name = meta["primary_form"]
        profile = meta["profile"]
        base = base_of(primary_name, profile)
        
        manifest[mat_id] = {
            "title": meta["title"],
            "machine": meta["machine"],
            "lore": meta["lore"],
            "primary_form": primary_name,
            "options": []
        }

        print(f"  [{mat_id}] Rendering 3 options for {primary_name}...")

        for opt_idx, opt_info in enumerate(meta["options"], 1):
            # 1. Render 32 frames of icon & halo
            icon_frames = [render_material_frame(mat_id, opt_idx, base, f) for f in range(FRAMES)]
            halo_frames = [
                np.clip(halo_gen(mat_id, opt_idx, f), 0, 255).astype(np.uint8)
                for f in range(FRAMES)
            ]
            
            # 2. Render slot composites (6x scale = 192x192 px)
            slot_frames = [
                make_slot_preview(icon_frames[f], halo_frames[f], opt_idx, opt_info["glow_color"])
                .resize((CELL * 6, CELL * 6), Image.NEAREST)
                for f in range(FRAMES)
            ]
            slot_gif_path = mat_dir / f"opt{opt_idx}_slot.gif"
            slot_frames[0].save(
                slot_gif_path, save_all=True, append_images=slot_frames[1:],
                duration=60, loop=0, disposal=2
            )
            
            # 3. Render icon-only GIF (6x scale = 96x96 px)
            icon_gif_frames = [
                Image.fromarray(fr, "RGBA").resize((96, 96), Image.NEAREST)
                for fr in icon_frames
            ]
            icon_gif_path = mat_dir / f"opt{opt_idx}_icon.gif"
            icon_gif_frames[0].save(
                icon_gif_path, save_all=True, append_images=icon_gif_frames[1:],
                duration=60, loop=0, disposal=2
            )

            # 4. Render halo-only GIF on dark background (2x scale = 128x128 px)
            halo_gif_frames = []
            for hf in halo_frames:
                bg = Image.new("RGBA", (HALO_SIZE, HALO_SIZE), (20, 20, 26, 255))
                bg.alpha_composite(Image.fromarray(hf, "RGBA"))
                halo_gif_frames.append(bg.resize((128, 128), Image.BILINEAR))
            halo_gif_path = mat_dir / f"opt{opt_idx}_halo.gif"
            halo_gif_frames[0].save(
                halo_gif_path, save_all=True, append_images=halo_gif_frames[1:],
                duration=60, loop=0, disposal=2
            )

            manifest[mat_id]["options"].append({
                "option": opt_idx,
                "name": opt_info["name"],
                "desc": opt_info["desc"],
                "halo_name": opt_info["halo_name"],
                "halo_desc": opt_info["halo_desc"],
                "accent": opt_info["accent"],
                "slot_gif": f"{mat_id}/opt{opt_idx}_slot.gif",
                "icon_gif": f"{mat_id}/opt{opt_idx}_icon.gif",
                "halo_gif": f"{mat_id}/opt{opt_idx}_halo.gif",
            })

    # Save manifest
    manifest_path = PROPOSALS_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Done! Manifest saved to {manifest_path}")


if __name__ == "__main__":
    main()
