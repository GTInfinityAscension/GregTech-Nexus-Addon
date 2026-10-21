"""Candidate animated icon sets for the originals' materials, three concepts per material (G-0272).

Same pipeline as tools/generate_material_set_textures.py (the Gemini sets: Awakened Draconium, White Dwarf
Matter...): Modernity-GTNH shapes (WhiteDwarfMatter CUSTOM set, ingots from a profile set), layered numpy effects
over 32 frames with interpolation, and a GTNA item effect loader (gtna:halo / gtna:glow_edge) on the item models.

Usage:
  python3 tools/design/originals_icon_variants.py <material> <out dir>             # showcase GIFs, 3 options
  python3 tools/design/originals_icon_variants.py <material> <out dir> --install N  # write option N to the mod
"""

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
MODERNITY = Path.home() / "Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures"
ICONSETS = MODERNITY / "items/materialicons"
CUSTOM = ICONSETS / "CUSTOM/WhiteDwarfMatter"
CUSTOM_BLOCK = MODERNITY / "blocks/materialicons/CUSTOM/WhiteDwarfMatter"
FRAMES = 32
EMPTY = Image.new("RGBA", (16, 16), (0, 0, 0, 0))

# GTCEu name -> Modernity name
FORMS = {"ingot": "ingot", "nugget": "nugget", "dust": "dust", "dust_small": "dustSmall", "dust_tiny": "dustTiny",
         "plate": "plate", "rod": "stick", "wire_fine": "wireFine", "gem": "gem", "block": "block"}


def base_of(name, ingot_profile=None):
    src = FORMS[name]
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


def overlay_of(name, ingot_profile=None):
    src = FORMS[name]
    folder = ICONSETS / ingot_profile if name in ("ingot", "nugget", "gem") and ingot_profile else CUSTOM
    p = folder / f"{src}_OVERLAY.png"
    return Image.open(p).convert("RGBA").crop((0, 0, 16, 16)) if p.exists() else EMPTY


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


# ---------------------------------------------------------------------------------------------- custom halos
# Animated halo textures (64x64, 32 frames) for gtna:halo. Drawn in their own colours: the model uses color -1.

HALO_SIZE = 64


def _halo_grid():
    y, x = np.mgrid[:HALO_SIZE, :HALO_SIZE].astype(np.float32)
    c = (HALO_SIZE - 1) / 2
    dx, dy = (x - c) / c, (y - c) / c
    return np.sqrt(dx ** 2 + dy ** 2), np.arctan2(dy, dx), dx, dy


def halo_nexium_field(f):
    # Field loops: dipole field lines round the item in a slow iridescent drift (teal -> blue -> violet).
    rr, ang, dx, dy = _halo_grid()
    t = f / FRAMES
    rot = ang + 2 * np.pi * t * 0.25
    psi = np.sin(rot) ** 2 / np.maximum(rr, 0.05)
    lines = np.exp(-((np.mod(psi * 1.2 - t, 1.0) - 0.5) / 0.12) ** 2)
    fade = np.clip((rr - 0.42) / 0.2, 0, 1) * np.clip((1 - rr) / 0.25, 0, 1)
    hue = np.mod(t + ang / (2 * np.pi), 1.0)
    r = np.interp(hue, [0, .33, .66, 1], [40, 60, 160, 40])
    g = np.interp(hue, [0, .33, .66, 1], [230, 140, 100, 230])
    b = np.interp(hue, [0, .33, .66, 1], [210, 255, 255, 210])
    glow = np.clip(1 - rr, 0, 1) ** 2 * 0.35
    alpha = np.clip(lines * fade * 0.9 + glow, 0, 1)
    return np.dstack([r, g, b, alpha * 255])


def halo_magnetar_pulsar(f):
    # Pulsar: two opposite beams sweep round the item over a faint violet disc; the beams flare as they pass the top.
    rr, ang, dx, dy = _halo_grid()
    t = f / FRAMES
    turn = np.mod(ang / (2 * np.pi) - t, 0.5)
    beam = np.exp(-((turn - 0.25) / 0.032) ** 2) * np.clip(rr - 0.25, 0, 1) * 2.6
    trail = np.where((turn > 0.25) & (turn < 0.4), np.exp(-(turn - 0.25) / 0.04), 0) * 0.9 * np.clip(rr - 0.25, 0, 1)
    flare = np.cos(2 * np.pi * t * 2) ** 12
    disc = np.clip(1 - rr, 0, 1) ** 1.8 * (0.45 + 0.45 * flare)
    alpha = np.clip(beam + trail + disc, 0, 1) * np.clip((1 - rr) / 0.15, 0, 1)
    white = np.clip(beam - 0.6, 0, 1)
    r = 120 + white * 135
    g = 70 + white * 185
    b = 255 + white * 0
    return np.dstack([r * np.ones_like(rr), g * np.ones_like(rr), b * np.ones_like(rr), alpha * 255])


def halo_degenerate_compression(f):
    # Compression: rings of light fall inward onto the item and vanish into it; faint lensed specks orbit.
    rr, ang, dx, dy = _halo_grid()
    t = f / FRAMES
    rings = np.zeros_like(rr)
    for k in range(3):
        rad = 1.0 - ((t + k / 3) % 1.0) * 0.6
        rings += np.exp(-((rr - rad) / 0.05) ** 2) * (1 - (t + k / 3) % 1.0) ** 0.6
    rng = np.random.default_rng(3)
    specks = np.zeros_like(rr)
    for k in range(10):
        a0, r0 = rng.random() * 2 * np.pi + 2 * np.pi * t * (0.5 + rng.random()), 0.55 + rng.random() * 0.4
        sx, sy = np.cos(a0) * r0, np.sin(a0) * r0
        specks += np.exp(-((dx - sx) ** 2 + (dy - sy) ** 2) / 0.0015)
    core = np.clip(1 - rr, 0, 1) ** 2 * 0.6
    alpha = np.clip(rings * 1.3 + specks + core, 0, 1) * np.clip((1 - rr) / 0.12, 0, 1)
    bright = np.clip(rings, 0, 1)
    return np.dstack([70 + bright * 170, 100 + bright * 150, 255 + 0 * rr, alpha * 255])


HALOS = {"nexium_field": halo_nexium_field, "magnetar_pulsar": halo_magnetar_pulsar,
         "degenerate_compression": halo_degenerate_compression}


def halo_frames(name):
    return [np.clip(HALOS[name](f), 0, 255).astype(np.uint8) for f in range(FRAMES)]


def install_halo(name):
    d = ROOT / "src/main/resources/assets/gtna/textures/item/effect"
    strip = np.concatenate(halo_frames(name), axis=0)
    Image.fromarray(strip, "RGBA").save(d / f"{name}.png")
    (d / f"{name}.png.mcmeta").write_text(
        json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=2) + "\n")


# ------------------------------------------------------------------------------------------- effect preview
# Approximates ItemEffectRenderer on a 32 px slot cell: halo quad behind (size px each side, tinted ARGB), the
# icon, the glow edge (tinted copy scaled 1 + width * 0.05, translucent) and the pulse (jittering 60 % copy).

CELL = 32
_DEFAULT_HALO = None


def _tint(img, argb):
    if argb in (None, 0, -1):
        return img
    c = argb & 0xFFFFFFFF
    a, r, g, b = (c >> 24) & 255, (c >> 16) & 255, (c >> 8) & 255, c & 255
    arr = np.array(img, dtype=np.float32)
    arr[..., 0] *= r / 255
    arr[..., 1] *= g / 255
    arr[..., 2] *= b / 255
    arr[..., 3] *= a / 255
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")


def preview(icon_frame, effect, f, rng):
    global _DEFAULT_HALO
    cell = Image.new("RGBA", (CELL, CELL), (198, 198, 198, 255))
    slot = Image.new("RGBA", (18, 18), (139, 139, 139, 255))
    cell.alpha_composite(slot, (7, 7))
    icon = Image.fromarray(icon_frame, "RGBA")
    loader = effect.get("loader") if effect else None
    off = (CELL - 16) // 2
    if loader == "gtna:halo":
        h = effect["halo"]
        if "custom" in h:
            tex = Image.fromarray(halo_frames(h["custom"])[f], "RGBA")
        else:
            src = ROOT / "src/main/resources/assets/gtna/textures/item/effect" / (h["texture"].split("/")[-1] + ".png")
            tex = Image.open(src).convert("RGBA").crop((0, 0, 64, 64))
        px = 16 + 2 * h["size"]
        tex = _tint(tex.resize((px, px), Image.BILINEAR), h.get("color", -1))
        cell.alpha_composite(tex, ((CELL - px) // 2, (CELL - px) // 2))
    cell.alpha_composite(icon, (off, off))
    if loader == "gtna:halo" and effect["halo"].get("pulse"):
        sc = rng.random() * 0.15 + 0.95
        px = max(1, round(16 * sc))
        cp = icon.resize((px, px), Image.NEAREST)
        cp.putalpha(cp.getchannel("A").point(lambda v: int(v * 0.6)))
        cell.alpha_composite(cp, ((CELL - px) // 2, (CELL - px) // 2))
    if loader == "gtna:glow_edge":
        w = max(0.5, effect["glow_edge"]["width"])
        px = round(16 * (1 + w * 0.05)) + 1
        cp = _tint(icon.resize((px, px), Image.NEAREST), effect["glow_edge"]["color"] | 0xFF000000)
        cp.putalpha(cp.getchannel("A").point(lambda v: int(v * 0.55)))
        cell.alpha_composite(cp, ((CELL - px) // 2, (CELL - px) // 2 - 1))
    return cell


# ----------------------------------------------------------------------------------------------------- Nexium
# Lance, Nexus-1. A metal that carries current without heat and keeps the shape of every field it has crossed.

def ramp(v, stops):
    """Palette ramp over the Modernity relief: stops are (position, (r, g, b))."""
    pos = [p for p, _ in stops]
    return [np.interp(v, pos, [c[k] for _, c in stops]) for k in range(3)]


NEXIUM_TEAL = [(0.0, (3, 22, 26)), (0.28, (8, 70, 72)), (0.55, (24, 160, 150)), (0.8, (96, 232, 214)),
               (1.0, (226, 255, 250))]
NEXIUM_AZURE = [(0.0, (4, 14, 34)), (0.28, (14, 52, 110)), (0.55, (36, 120, 210)), (0.8, (120, 200, 255)),
                (1.0, (232, 246, 255))]
NEXIUM_VIOLET = [(0.0, (14, 6, 34)), (0.28, (48, 22, 110)), (0.55, (112, 72, 220)), (0.8, (188, 160, 255)),
                 (1.0, (246, 240, 255))]


def nexium(opt, base, f):
    a, gray, x, y, cx, cy, nd, ang, edge = geometry(base)
    t = f / FRAMES
    if opt == 1:
        # Superconductor: cold teal metal; a soft current glint sweeps diagonally across the bright facets and a
        # few cyan sparks run along the outline. Calm, no pattern on the body.
        r, g, b = ramp(gray, NEXIUM_TEAL)
        band = np.exp(-(((x + y) - (t * 44 - 10)) / 2.2) ** 2) * np.clip(gray - 0.35, 0, 1) * 1.6
        r, g, b = r + band * 120, g + band * 160, b + band * 150
        for k in range(3):
            head = (t + k / 3) % 1.0
            lag = (head - (ang / (2 * np.pi)) % 1.0) % 1.0
            spark = edge * np.where(lag < 0.06, 1 - lag / 0.06, 0)
            r, g, b = r + spark * 90, g + spark * 200, b + spark * 190
    elif opt == 2:
        # Field memory: the whole piece slowly shifts teal -> azure -> violet and back, offset across the surface
        # like a thin film, so the colour runs over the relief instead of sitting on it.
        phase = (t + (x + y) / 48.0) % 1.0
        pals = (NEXIUM_TEAL, NEXIUM_AZURE, NEXIUM_VIOLET, NEXIUM_TEAL)
        seg = np.minimum((phase * 3).astype(int), 2)
        w = phase * 3 - seg
        cols = [ramp(gray, pal) for pal in pals]
        r = np.zeros_like(gray); g = np.zeros_like(gray); b = np.zeros_like(gray)
        for i in range(3):
            m = seg == i
            for ch, out in enumerate((r, g, b)):
                out[m] = (cols[i][ch] * (1 - w) + cols[i + 1][ch] * w)[m]
    else:
        # Cold crystal: a deeper teal with slow lensing ripples and five cold star glints that flare in turn.
        r, g, b = ramp(gray * 0.92, NEXIUM_TEAL)
        lens = np.sin(2 * np.pi * (t * 1.5 + nd * 2.5)) * 10
        r, g, b = r + lens * 0.4, g + lens * 0.9, b + lens
        pts = np.argwhere(a & (gray > 0.45))
        if len(pts):
            for k, idx in enumerate((3, 17, 29, 41, 53)):
                sy, sx = pts[(idx * 7) % len(pts)]
                glint = max(0.0, np.cos(((t - k / 5) % 1.0) * 2 * np.pi)) ** 10
                for dy, dx, wgt in ((0, 0, 1.0), (0, 1, 0.45), (0, -1, 0.45), (1, 0, 0.45), (-1, 0, 0.45)):
                    ny, nx = sy + dy, sx + dx
                    if 0 <= ny < 16 and 0 <= nx < 16 and a[ny, nx]:
                        r[ny, nx] += glint * wgt * 200
                        g[ny, nx] += glint * wgt * 255
                        b[ny, nx] += glint * wgt * 255
    return finish(base, r, g, b)


NEXIUM_EFFECTS = {
    1: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo", "color": -12597560, "size": 3,
                                         "pulse": True}},
    2: {"loader": "gtna:glow_edge", "glow_edge": {"color": 4183752, "width": 1.5}},
    3: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo_noise", "color": -12597560, "size": 2,
                                         "pulse": False}},
}

# ------------------------------------------------------------------------------------------ Primordial Tholin
# Lance, Arrokoth. The red organic crust of a cold Kuiper-belt body: polymers made by sunlight on methane ice.

THOLIN = [(0.0, (28, 5, 6)), (0.3, (88, 18, 16)), (0.55, (146, 40, 30)), (0.8, (194, 92, 68)),
          (1.0, (236, 178, 148))]


def tholin(opt, base, f):
    a, gray, x, y, cx, cy, nd, ang, edge = geometry(base)
    t = f / FRAMES
    r, g, b = ramp(gray, THOLIN)
    if opt == 1:
        # Arrokoth frost: methane-ice crystals in the red dust catch the light one after another (pale blue-white).
        pts = np.argwhere(a & (gray > 0.4))
        if len(pts):
            for k, idx in enumerate((2, 11, 19, 27, 36, 44)):
                sy, sx = pts[(idx * 5) % len(pts)]
                glint = max(0.0, np.cos(((t - k / 6) % 1.0) * 2 * np.pi)) ** 12
                for dy, dx, wgt in ((0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)):
                    ny, nx = sy + dy, sx + dx
                    if 0 <= ny < 16 and 0 <= nx < 16 and a[ny, nx]:
                        r[ny, nx] += glint * wgt * 170
                        g[ny, nx] += glint * wgt * 210
                        b[ny, nx] += glint * wgt * 255
    elif opt == 2:
        # Polymerising: amber veins in the dark grains slowly brighten and fade as the chains grow.
        veins = np.abs(np.sin(x * 1.3 + np.sin(y * 0.9) * 2.0)) < 0.25
        pulse = (np.sin(2 * np.pi * (t - nd * 0.6)) * 0.5 + 0.5) ** 2
        glow = veins * (gray < 0.7) * a * (0.25 + 0.75 * pulse)
        r, g, b = r + glow * 190, g + glow * 120, b + glow * 25
    else:
        # Sublimation haze: pale wisps rise off the grains and thin out, as on a comet's surface.
        wisp = np.sin(x * 0.8 + np.sin((y + t * 16) * 0.5) * 1.5 + 2 * np.pi * t) * 0.5 + 0.5
        rise = np.clip(1 - y / 16, 0, 1)
        haze = wisp ** 3 * rise * 0.7
        r, g, b = r + haze * 120, g + haze * 100, b + haze * 95
    return finish(base, r, g, b)


THOLIN_EFFECTS = {
    1: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo_noise", "color": -5154236, "size": 2,
                                         "pulse": False}},
    2: {"loader": "gtna:glow_edge", "glow_edge": {"color": 13924919, "width": 1.0}},
    3: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo", "color": -3049610, "size": 3,
                                         "pulse": True}},
}

# ------------------------------------------------------------------------------------------- Magnetar Crystal
# Stellar Containment Chamber, magnetar starquake. A crystal that still carries the inverted field.

MAGNETAR = [(0.0, (12, 4, 36)), (0.28, (46, 18, 120)), (0.55, (104, 66, 226)), (0.8, (176, 150, 255)),
            (1.0, (244, 238, 255))]


def magnetar(opt, base, f):
    a, gray, x, y, cx, cy, nd, ang, edge = geometry(base)
    t = f / FRAMES
    r, g, b = ramp(gray, MAGNETAR)
    if opt == 1:
        # Inverted field: dipole field lines inside the crystal glow in waves that travel outward from the core.
        rr = np.maximum(nd, 0.08)
        psi = np.sin(ang) ** 2 / rr
        line = np.exp(-((np.mod(psi * 1.4, 1.0) - 0.5) / 0.14) ** 2)
        wave = (np.sin(2 * np.pi * (nd * 2.0 - t * 2)) * 0.5 + 0.5) ** 3
        glow = line * wave * (0.3 + 0.7 * gray)
        r, g, b = r + glow * 150, g + glow * 120, b + glow * 90
    elif opt == 2:
        # Pulsar: two opposite beams sweep round the core like a lighthouse, each with a fading trail; the core
        # flashes as a beam crosses the line of sight (top), and the outline sparks where the beam leaves the crystal.
        turn = np.mod(ang / (2 * np.pi) - t * 2, 0.5)          # 0..0.5, two beams per turn
        lead = np.exp(-((turn - 0.25) / 0.035) ** 2)
        trail = np.where((turn > 0.25) & (turn < 0.42), np.exp(-(turn - 0.25) / 0.05), 0) * 0.55
        beam = (lead + trail) * (0.3 + 0.7 * gray) * np.clip(1.25 - nd, 0, 1)
        sight = np.cos(2 * np.pi * t * 4) ** 16                    # beam crossing the viewer, twice per turn
        core = np.exp(-nd * 3.5) * (0.35 + 1.2 * sight)
        spark = edge * lead * 1.4
        r = r + beam * 150 + core * 110 + spark * 160
        g = g + beam * 140 + core * 95 + spark * 150
        b = b + beam * 110 + core * 70 + spark * 120
        white = np.clip(beam + core - 1.0, 0, 1)
        r, g, b = r + white * 60, g + white * 60, b + white * 60
    else:
        # Starquake lattice: fracture lines in the crystal flicker with discharge, and prismatic glints run over
        # the facets.
        crack = (np.abs(np.sin(x * 0.9 - y * 1.3 + np.sin(y * 0.6) * 2)) < 0.22) & a
        flick = np.clip(np.sin(2 * np.pi * (t * 3 + x * 0.17)), 0, 1) ** 2
        r, g, b = r + crack * flick * 150, g + crack * flick * 200, b + crack * flick * 230
        glint = np.exp(-(((x - y) - (t * 40 - 20)) / 1.6) ** 2) * np.clip(gray - 0.4, 0, 1) * 2
        hue = np.mod(x / 16 + t, 1.0)
        r = r + glint * np.interp(hue, [0, 0.33, 0.66, 1], [255, 120, 140, 255])
        g = g + glint * np.interp(hue, [0, 0.33, 0.66, 1], [120, 255, 160, 120])
        b = b + glint * np.interp(hue, [0, 0.33, 0.66, 1], [200, 220, 255, 200])
    return finish(base, r, g, b)


MAGNETAR_EFFECTS = {
    1: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo", "color": -7643905, "size": 4,
                                         "pulse": True}},
    2: {"loader": "gtna:glow_edge", "glow_edge": {"color": 10057471, "width": 1.5}},
    3: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo_noise", "color": -7643905, "size": 3,
                                         "pulse": False}},
}

# ------------------------------------------------------------------------------------- Degenerate Core Matter
# Stellar Containment Chamber, star collapse. Neutron-degenerate matter: white-hot, unbearably dense.

DEGENERATE = [(0.0, (10, 12, 32)), (0.3, (40, 50, 108)), (0.55, (110, 128, 200)), (0.8, (196, 210, 252)),
              (1.0, (255, 255, 255))]


def degenerate(opt, base, f):
    a, gray, x, y, cx, cy, nd, ang, edge = geometry(base)
    t = f / FRAMES
    r, g, b = ramp(gray ** 1.25, DEGENERATE)
    rng = np.random.default_rng(7)
    noise = rng.random((FRAMES, 16, 16))
    if opt == 1:
        # Fermi sea: the grains shimmer as degenerate neutrons fill every state (fine flicker), and a compression
        # front sweeps inward to the core, where it flashes white.
        fl = (noise[f, :gray.shape[0], :gray.shape[1]] - 0.5) * 34 * gray
        front = np.exp(-((nd - (1 - t)) / 0.09) ** 2) * (0.4 + 0.6 * gray)
        flash = np.exp(-nd * 5) * max(0.0, 1 - abs(t - 0.97) * 12)
        r, g, b = r + fl + front * 70 + flash * 120, g + fl + front * 90 + flash * 120, b + fl + front * 130 + flash * 120
    elif opt == 2:
        # Lensing core: space bends round the dense centre; a ring of light (Einstein ring) breathes and the
        # surrounding grains swirl inward.
        swirl = np.sin(ang * 3 + nd * 9 - 2 * np.pi * t * 2) * 0.5 + 0.5
        ring_r = 0.45 + 0.08 * np.sin(2 * np.pi * t)
        ring = np.exp(-((nd - ring_r) / 0.07) ** 2)
        dark = np.exp(-(nd / 0.18) ** 2)
        r = r * (1 - dark * 0.7) + swirl * 22 * gray + ring * 120
        g = g * (1 - dark * 0.7) + swirl * 30 * gray + ring * 140
        b = b * (1 - dark * 0.6) + swirl * 50 * gray + ring * 180
    else:
        # Quark soup: colour-charge sparks (red, green, blue) wander through the grains and merge white at the core.
        cols = ((255, 70, 90), (90, 255, 120), (90, 140, 255))
        for k, (cr, cg, cb) in enumerate(cols):
            ph = 2 * np.pi * (t + k / 3)
            px = cx + np.cos(ph) * 4.5 * (1 - 0.5 * np.sin(ph * 2) ** 2)
            py = cy + np.sin(ph) * 4.0
            spot = np.exp(-((x - px) ** 2 + (y - py) ** 2) / 2.2) * a
            r, g, b = r * (1 - spot * 0.4) + spot * cr, g * (1 - spot * 0.4) + spot * cg, b * (1 - spot * 0.4) + spot * cb
        core = np.exp(-nd * 4) * (0.6 + 0.4 * np.sin(2 * np.pi * t * 3) ** 2)
        r, g, b = r + core * 90, g + core * 90, b + core * 90
    return finish(base, r, g, b)


DEGENERATE_EFFECTS = {
    1: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo", "color": -2104065, "size": 4,
                                         "pulse": True}},
    2: {"loader": "gtna:halo", "halo": {"texture": "gtna:item/effect/halo_noise", "color": -6250241, "size": 5,
                                         "pulse": True}},
    3: {"loader": "gtna:glow_edge", "glow_edge": {"color": 15791359, "width": 1.5}},
}

MATERIALS = {
    # material: (effect fn, ingot profile, item forms, showcase forms, item effects per option)
    "nexium": (nexium, "SHINY", ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod", "wire_fine"],
               ["ingot", "plate", "rod", "wire_fine", "dust", "block"], NEXIUM_EFFECTS),
    "primordial_tholin": (tholin, None, ["dust", "dust_small", "dust_tiny"],
                          ["dust", "dust_small", "dust_tiny", "block"], THOLIN_EFFECTS),
    "magnetar_crystal": (magnetar, "GEM_HORIZONTAL", ["gem", "dust", "dust_small", "dust_tiny"],
                         ["gem", "dust", "dust_small", "dust_tiny", "block"], MAGNETAR_EFFECTS),
    "degenerate_core_matter": (degenerate, None, ["dust", "dust_small", "dust_tiny"],
                               ["dust", "dust_small", "dust_tiny", "block"], DEGENERATE_EFFECTS),
}


def frames_of(material, opt, name):
    fn, profile, _, _, _ = MATERIALS[material]
    base = base_of(name, profile)
    return [fn(opt, base, f) for f in range(FRAMES)]


def install(material, opt, effect_spec=None):
    _, profile, items, _, effects = MATERIALS[material]
    folder = f"gtna_{material}"
    tex = ROOT / "src/main/resources/assets/gtceu/textures"
    models = ROOT / "src/main/resources/assets/gtceu/models"
    meta = json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=2) + "\n"
    for kind, names in (("item", items), ("block", ["block"])):
        d = tex / kind / "material_sets" / folder
        md = models / kind / "material_sets" / folder
        d.mkdir(parents=True, exist_ok=True)
        md.mkdir(parents=True, exist_ok=True)
        for name in names:
            strip = np.concatenate(frames_of(material, opt, name), axis=0)
            Image.fromarray(strip, "RGBA").save(d / f"{name}.png")
            (d / f"{name}.png.mcmeta").write_text(meta)
            if kind == "item":
                overlay_of(name, profile).save(d / f"{name}_overlay.png")
                EMPTY.save(d / f"{name}_secondary.png")
                model = {"parent": "item/generated", "textures": {
                    "layer0": f"gtceu:item/material_sets/{folder}/{name}",
                    "layer1": "gtceu:item/material_sets/gtna_creon/gem_overlay",
                    "layer2": f"gtceu:item/material_sets/{folder}/{name}_overlay"}}
                effect = json.loads(json.dumps(effect_spec or effects[opt]))
                custom = effect.get("halo", {}).pop("custom", None)
                if custom:
                    install_halo(custom)
                    effect["halo"]["texture"] = f"gtna:item/effect/{custom}"
                model["loader"] = effect.pop("loader")
                for key, value in effect.items():
                    if "texture" in value:
                        model["textures"]["halo"] = value["texture"]
                        value = {**value, "texture": "#halo"}
                    model[key] = value
            else:
                model = {"parent": "block/block", "loader": "forge:composite",
                         "textures": {"particle": f"gtceu:block/material_sets/{folder}/block"},
                         "children": {"base": {"parent": "gtceu:block/cube/tinted/all_0", "render_type": "solid",
                                               "textures": {"all": f"gtceu:block/material_sets/{folder}/block"}}},
                         "item_render_order": ["base"]}
            (md / f"{name}.json").write_text(json.dumps(model, indent=2) + "\n")
    print(f"installed option {opt} for {material}")


def showcase(material, out, effects=None):
    _, _, _, shapes, default_effects = MATERIALS[material]
    effects = effects or default_effects
    out.mkdir(parents=True, exist_ok=True)
    for opt in (1, 2, 3):
        for name in shapes:
            frames = frames_of(material, opt, name)
            rng = np.random.default_rng(opt)
            effect = effects[opt] if name != "block" else None
            cells = [preview(fr, effect, i, rng).resize((CELL * 6, CELL * 6), Image.NEAREST)
                     for i, fr in enumerate(frames)]
            cells[0].save(out / f"{material}_opt{opt}_{name}.gif", save_all=True, append_images=cells[1:],
                          duration=100, loop=0, disposal=2)
    print(f"wrote {material} options to {out}")


if __name__ == "__main__":
    mat, out_dir = sys.argv[1], Path(sys.argv[2])
    if "--install" in sys.argv:
        spec = None
        if "--effect" in sys.argv:  # an effect spec file overrides the option's own effect
            spec = json.loads(Path(sys.argv[sys.argv.index("--effect") + 1]).read_text())
        install(mat, int(sys.argv[sys.argv.index("--install") + 1]), spec)
    else:
        showcase(mat, out_dir)
