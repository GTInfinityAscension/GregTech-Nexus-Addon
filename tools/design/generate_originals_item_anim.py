#!/usr/bin/env python3
"""Animated item texture proposals for the original multiblocks (Rift Singularity, Antiproton Penning Cell,
Moon target cartridge) at 64x and 128x.

Each frame is drawn at 4x supersampling and downscaled, then the frames are stacked vertically like a vanilla
animated texture (with a .mcmeta). Also writes a GIF per item and a comparison sheet.

    python3 tools/design/generate_originals_item_anim.py

Output: tools/design/item_proposals/originals/
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'item_proposals', 'originals')
os.makedirs(OUT, exist_ok=True)
SS = 4  # supersampling


def noise2(w, h, scale, seed, octaves=4):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp, total = 1.0, 0.0
    for o in range(octaves):
        gs = max(2, int(scale * 2 ** o))
        g = rng.random((gs + 1, gs + 1))
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(img, float) / 255 * amp
        total += amp
        amp *= 0.5
    return out / total


def to_img(rgba):
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), 'RGBA')


def finish(big, size):
    """Downscale, then a light unsharp pass so edges stay crisp at item size."""
    im = big.resize((size, size), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=0.6, percent=60, threshold=1))


# --------------------------------------------------------------------- rift singularity
def rift_singularity(size, t, frames):
    s = size * SS
    y, x = np.mgrid[0:s, 0:s].astype(float)
    cx = cy = s / 2
    dx, dy = (x - cx) / (s / 2) * 1.12, (y - cy) / (s / 2) * 1.12
    r = np.hypot(dx, dy)
    a = np.arctan2(dy, dx)
    ph = 2 * math.pi * t / frames
    # Spiral accretion arms, turning; lensed (pulled inward near the horizon).
    rl = r + 0.08 / np.maximum(r, 0.05)
    arms = 0.5 + 0.5 * np.sin(3 * a - 9 * rl + ph * 3)
    dust = noise2(s, s, 3, 7)
    disk = np.clip(1 - np.abs(r - 0.55) / 0.33, 0, 1) ** 1.5 * (0.45 + 0.55 * arms) * (0.6 + 0.6 * dust)
    ring = np.exp(-((r - 0.30) / 0.035) ** 2) * (0.8 + 0.2 * math.sin(ph * 2))   # photon ring
    horizon = r < 0.26
    col = np.zeros((s, s, 4))
    hot = np.clip(disk * 1.4, 0, 1)
    col[..., 0] = 120 * disk + 255 * ring * 0.7 + 255 * hot ** 3 * 0.6
    col[..., 1] = 40 * disk + 230 * ring + 200 * hot ** 3 * 0.5
    col[..., 2] = 230 * disk + 255 * ring + 120 * hot ** 2
    alpha = np.clip(disk * 1.6 + ring * 1.5, 0, 1) * 255
    col[..., 3] = np.where(r < 0.97, alpha, 0)
    col[horizon] = [4, 2, 10, 255]
    im = to_img(col)
    d = ImageDraw.Draw(im)
    # Sparks infalling on spiral paths.
    rng = np.random.default_rng(11)
    for k in range(18):
        a0 = rng.random() * 2 * math.pi
        life = (t / frames + rng.random()) % 1
        rr = 0.92 - 0.62 * life
        aa = a0 + life * 4.5
        px, py = cx + math.cos(aa) * rr * s / 2, cy + math.sin(aa) * rr * s / 2
        rad = s * 0.012 * (1.2 - life)
        d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=(190, 240, 255, int(255 * (1 - life * 0.6))))
    return finish(im, size)


# --------------------------------------------------------------------- antiproton penning cell
def penning_cell(size, t, frames, core=(255, 60, 220), spark=(255, 200, 255), count=40, seed=5):
    s = size * SS
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w0, w1 = s * 0.26, s * 0.74        # body
    top, bot = s * 0.08, s * 0.92
    cap = s * 0.11
    ph = 2 * math.pi * t / frames
    # Glass body with a dark inner vacuum.
    d.rounded_rectangle([w0, top + cap * 0.6, w1, bot - cap * 0.6], radius=s * 0.06, fill=(18, 14, 38, 235),
                        outline=(150, 200, 255, 200), width=max(1, s // 64))
    # Magnetic field lines (Penning trap): ellipses that breathe.
    cxm, cym = s / 2, s / 2
    for k in range(4):
        e = 0.10 + 0.05 * k + 0.01 * math.sin(ph + k)
        d.ellipse([cxm - s * e, cym - s * (0.26 - 0.02 * k), cxm + s * e, cym + s * (0.26 - 0.02 * k)],
                  outline=(60, 200, 255, 90 + 30 * k), width=max(1, s // 160))
    # Antiproton cloud: magenta orbiting particles with glow.
    glow = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    rng = np.random.default_rng(seed)
    for k in range(count):
        rr = 0.03 + rng.random() * 0.09
        sp = 1 + rng.random() * 2
        aa = rng.random() * 2 * math.pi + ph * sp
        z = math.sin(ph * 2 + k) * 0.18
        px, py = cxm + math.cos(aa) * rr * s, cym + z * s + math.sin(aa) * rr * s * 0.35
        rad = s * (0.008 + 0.006 * rng.random())
        gd.ellipse([px - rad * 3, py - rad * 3, px + rad * 3, py + rad * 3], fill=core + (70,))
        gd.ellipse([px - rad, py - rad, px + rad, py + rad], fill=spark + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(s * 0.008))
    im.alpha_composite(glow)
    # Glass highlight.
    d = ImageDraw.Draw(im)
    d.rectangle([w0 + s * 0.04, top + cap, w0 + s * 0.07, bot - cap], fill=(255, 255, 255, 50))
    # Metal end caps with coil rings and status LED.
    for y0 in (top, bot - cap):
        d.rounded_rectangle([w0 - s * 0.04, y0, w1 + s * 0.04, y0 + cap], radius=s * 0.02, fill=(70, 74, 92, 255),
                            outline=(30, 30, 40, 255), width=max(1, s // 96))
        for k in range(3):
            yy = y0 + cap * (0.25 + 0.25 * k)
            d.line([w0 - s * 0.03, yy, w1 + s * 0.03, yy], fill=(200, 140, 60, 255), width=max(1, s // 128))
    led = 0.5 + 0.5 * math.sin(ph * 2)
    d.ellipse([w1 - s * 0.05, top + cap * 0.3, w1 - s * 0.01, top + cap * 0.7],
              fill=(80 + int(175 * led), 255, 120, 255))
    return finish(im, size)


# --------------------------------------------------------------------- moon target cartridge
_MAPS = {}

# Body surfaces: (seed, base albedo, maria strength, crater count, bands/streaks, tint rgb, glow)
BODIES = {
    'moon': (21, 0.62, 1.1, 140, 0.0, (170, 225, 255), 0.0),
    'phobos': (5, 0.45, 0.4, 90, 0.0, (205, 185, 160), 0.0),
    'vesta': (8, 0.55, 0.6, 60, 0.0, (215, 200, 175), 0.0),
    'ceres': (13, 0.40, 0.3, 80, 0.0, (180, 185, 200), 0.0),
    'psyche': (17, 0.70, 0.2, 50, 0.0, (230, 225, 210), 0.0),
    'europa': (29, 0.85, 0.0, 6, 1.0, (225, 235, 255), 0.0),
    'arrokoth': (31, 0.55, 0.5, 20, 0.0, (240, 140, 110), 0.0),
    'nexus_1': (41, 0.50, 0.8, 40, 0.5, (210, 120, 255), 0.6),
}


def moon_map(body='moon'):
    """Equirectangular albedo: maria (dark patches), craters with bright rims, optional streaks (Europa's lineae)."""
    if body in _MAPS: return _MAPS[body]
    seed, alb, mar, ncr, streak, _, _ = BODIES[body]
    w, h = 512, 256
    base = alb + 0.18 * noise2(w, h, 8, seed, 5)
    maria = noise2(w, h, 2, seed + 12, 3)
    base -= np.clip(maria - 0.55, 0, 1) * mar
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    rng = np.random.default_rng(seed)
    if streak:
        yy0, xx0 = np.mgrid[0:h, 0:w].astype(float)
        for _ in range(14):
            a, b, c = rng.random() * 6, rng.random() * 0.06, rng.random() * w
            line = np.abs(np.sin((xx0 - c) / w * a * math.pi + yy0 / h * 9 * b) )
            base -= 0.35 * streak * np.exp(-(line / 0.02) ** 2)
    for _ in range(ncr):
        cx, cy, r = rng.random() * w, rng.random() * h, 2 + rng.random() ** 3 * 22
        dxw = np.minimum(np.abs(xx - cx), w - np.abs(xx - cx))
        d = np.hypot(dxw, yy - cy) / r
        base -= 0.22 * np.clip(1 - d, 0, 1) ** 0.7 * (d < 1)
        base += 0.18 * np.exp(-((d - 1.0) / 0.18) ** 2)
    _MAPS[body] = np.clip(base, 0, 1)
    return _MAPS[body]
def moon_cartridge(size, t, frames, body='moon'):
    s = size * SS
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ph = 2 * math.pi * t / frames
    # Cartridge plate: angled dark steel with brass rails.
    plate = [(s * 0.16, s * 0.22), (s * 0.84, s * 0.22), (s * 0.84, s * 0.78), (s * 0.16, s * 0.78)]
    d.rounded_rectangle([s * 0.14, s * 0.18, s * 0.86, s * 0.82], radius=s * 0.06, fill=(44, 46, 60, 255),
                        outline=(20, 20, 28, 255), width=max(1, s // 64))
    d.rectangle([s * 0.14, s * 0.18, s * 0.86, s * 0.25], fill=(190, 140, 60, 255))
    d.rectangle([s * 0.14, s * 0.75, s * 0.86, s * 0.82], fill=(190, 140, 60, 255))
    for k in range(5):
        xx = s * (0.22 + 0.14 * k)
        d.rectangle([xx, s * 0.76, xx + s * 0.06, s * 0.81], fill=(60, 50, 30, 255))
    # Holographic moon: rotating cratered sphere (texture scrolls in longitude).
    r = s * 0.235
    cx, cy = s / 2, s / 2
    yy, xx = np.mgrid[0:s, 0:s].astype(float)
    nx, ny = (xx - cx) / r, (yy - cy) / r
    rr = nx ** 2 + ny ** 2
    inside = rr <= 1
    nz = np.sqrt(np.clip(1 - rr, 0, 1))
    lon = np.arctan2(nx, nz) + ph
    lat = np.arcsin(np.clip(ny, -1, 1))
    tex = moon_map(body)
    tint, glowk = BODIES[body][5], BODIES[body][6]
    u = ((lon / (2 * math.pi)) % 1 * 255).astype(int)
    u = ((lon / (2 * math.pi)) % 1 * 511).astype(int)
    v = ((lat / math.pi + 0.5) * 255).clip(0, 255).astype(int)
    craters = tex[v, u]
    light = np.clip(0.25 + 0.75 * (nx * -0.5 + ny * -0.3 + nz * 0.8), 0, 1)
    shade = craters * light
    holo = np.zeros((s, s, 4))
    rim = np.clip(1 - nz, 0, 1) ** 3 * glowk
    holo[..., 0] = tint[0] * shade + 20 + 200 * rim
    holo[..., 1] = tint[1] * shade + 25 + 80 * rim
    holo[..., 2] = tint[2] * shade + 40 + 255 * rim
    scan = 0.95 + 0.05 * np.sin(yy / s * 160 - ph * 6)
    holo[..., 3] = np.where(inside, 230 * scan, 0)
    im.alpha_composite(to_img(holo))
    # Targeting reticle sweeping.
    d = ImageDraw.Draw(im)
    lw = max(1, s // 96)
    d.ellipse([cx - r * 1.25, cy - r * 1.25, cx + r * 1.25, cy + r * 1.25], outline=(80, 255, 200, 200), width=lw)
    for k in range(4):
        a = ph + k * math.pi / 2
        x0, y0 = cx + math.cos(a) * r * 1.1, cy + math.sin(a) * r * 1.1
        x1, y1 = cx + math.cos(a) * r * 1.45, cy + math.sin(a) * r * 1.45
        d.line([x0, y0, x1, y1], fill=(255, 220, 90, 255), width=lw * 2)
    return finish(im, size)


# --------------------------------------------------------------------- rift probe
def rift_probe(size, t, frames):
    s = size * SS
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ph = 2 * math.pi * t / frames
    lw = max(1, s // 96)
    # Diagonal dart: hull, fins and a lens at the tip.
    def rot(pts, a=-math.pi / 4):
        c, sn = math.cos(a), math.sin(a)
        return [(s / 2 + (x * c - y * sn) * s, s / 2 + (x * sn + y * c) * s) for x, y in pts]
    d.polygon(rot([(-0.06, -0.36), (0.06, -0.36), (0.09, 0.22), (0, 0.33), (-0.09, 0.22)]), fill=(70, 74, 96, 255),
              outline=(25, 25, 35, 255))
    for side in (-1, 1):
        d.polygon(rot([(0.06 * side, -0.30), (0.17 * side, -0.40), (0.15 * side, -0.18), (0.06 * side, -0.14)]),
                  fill=(190, 140, 60, 255), outline=(60, 45, 20, 255))
    d.polygon(rot([(-0.05, 0.05), (0.05, 0.05), (0.05, 0.12), (-0.05, 0.12)]), fill=(40, 220, 255, 255))
    # Scanning cone from the lens, sweeping.
    glow = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    sweep = math.sin(ph) * 0.25
    tip = rot([(0, 0.33)])[0]
    a0 = -math.pi / 4 + math.pi / 2 + sweep
    for k in range(10):
        f = k / 10
        aa = a0 + (f - 0.5) * 0.5
        gd.line([tip, (tip[0] + math.cos(aa) * s * 0.35, tip[1] + math.sin(aa) * s * 0.35)],
                fill=(80, 255, 230, 60), width=lw * 2)
    glow = glow.filter(ImageFilter.GaussianBlur(s * 0.01))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    led = 0.5 + 0.5 * math.sin(ph * 3)
    c = rot([(0, -0.25)])[0]
    d.ellipse([c[0] - s * 0.02, c[1] - s * 0.02, c[0] + s * 0.02, c[1] + s * 0.02],
              fill=(255, int(80 + 150 * led), 80, 255))
    return finish(im, size)


# --------------------------------------------------------------------- depth anchor
def depth_anchor(size, t, frames):
    s = size * SS
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ph = 2 * math.pi * t / frames
    cx = s / 2
    # Heavy spike pointing down.
    d.polygon([(cx - s * 0.12, s * 0.16), (cx + s * 0.12, s * 0.16), (cx + s * 0.08, s * 0.62), (cx, s * 0.92),
               (cx - s * 0.08, s * 0.62)], fill=(58, 52, 78, 255), outline=(22, 20, 30, 255))
    d.rectangle([cx - s * 0.2, s * 0.08, cx + s * 0.2, s * 0.18], fill=(95, 90, 120, 255), outline=(22, 20, 30, 255))
    d.line([cx, s * 0.2, cx, s * 0.86], fill=(160, 90, 255, 255), width=max(1, s // 64))
    # Tilted rings orbiting the spike, phase-shifted.
    glow = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for k in range(3):
        yc = s * (0.32 + 0.16 * k) + math.sin(ph + k * 2) * s * 0.02
        rw = s * (0.30 - 0.05 * k)
        gd.ellipse([cx - rw, yc - rw * 0.25, cx + rw, yc + rw * 0.25], outline=(190, 120, 255, 220),
                   width=max(1, s // 80))
        a = ph * (1 + 0.3 * k) + k
        px, py = cx + math.cos(a) * rw, yc + math.sin(a) * rw * 0.25
        gd.ellipse([px - s * 0.025, py - s * 0.025, px + s * 0.025, py + s * 0.025], fill=(255, 230, 255, 255))
    glow2 = glow.filter(ImageFilter.GaussianBlur(s * 0.012))
    im.alpha_composite(glow2)
    im.alpha_composite(glow)
    return finish(im, size)


PARTICLES = {
    'antiproton': ((255, 60, 220), (255, 200, 255), 40), 'kaon': ((60, 200, 255), (200, 240, 255), 30),
    'lambda': ((120, 255, 140), (220, 255, 220), 26), 'charm': ((255, 200, 60), (255, 245, 200), 22),
    'bottom': ((255, 120, 40), (255, 220, 180), 18), 'w_boson': ((90, 140, 255), (210, 225, 255), 14),
    'z_boson': ((40, 255, 220), (210, 255, 245), 14), 'higgs': ((255, 230, 120), (255, 255, 240), 10),
    'top': ((255, 70, 70), (255, 210, 210), 10), 'x_nexus': ((190, 80, 255), (255, 240, 255), 8),
}

ITEMS = [('rift_singularity', rift_singularity, 32, 2), ('antiproton_cell', penning_cell, 24, 2),
         ('target_cartridge_moon', moon_cartridge, 32, 2)]


MOD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'main', 'resources', 'assets',
                   'gtna', 'textures', 'item', 'originals')


def write_strip(path, imgs, frametime):
    size = imgs[0].width
    strip = Image.new('RGBA', (size, size * len(imgs)))
    for i, im in enumerate(imgs): strip.paste(im, (0, i * size))
    strip.save(path, optimize=True)
    with open(path + '.mcmeta', 'w') as f:
        f.write('{\n  "animation": {\n    "frametime": %d\n  }\n}\n' % frametime)


def mod_textures():
    """The approved 64x set, written into the mod (2026-10-15: the author picked 64x)."""
    jobs = [('rift_singularity', lambda t: rift_singularity(64, t, 32), 32),
            ('antiproton_cell', lambda t: penning_cell(64, t, 24), 24),
            ('rift_probe', lambda t: rift_probe(64, t, 24), 24),
            ('depth_anchor', lambda t: depth_anchor(64, t, 32), 32)]
    for body in BODIES:
        jobs.append((f'target_cartridge_{body}', lambda t, b=body: moon_cartridge(64, t, 32, b), 32))
    for i, (p, (core, spark, n)) in enumerate(PARTICLES.items()):
        jobs.append((f'contained_{p}', lambda t, c=core, sp=spark, n=n, i=i: penning_cell(64, t, 24, c, sp, n, 50 + i), 24))
    sheet = []
    for name, fn, frames in jobs:
        imgs = [fn(t) for t in range(frames)]
        write_strip(os.path.join(MOD, name + '.png'), imgs, 2)
        sheet.append((name, imgs))
        print('mod', name)
    # Sheet of the whole set (first frame) for review.
    cols = 6
    rows = (len(sheet) + cols - 1) // cols
    out = Image.new('RGBA', (cols * 160, rows * 176), (24, 22, 32, 255))
    for i, (name, imgs) in enumerate(sheet):
        bg = Image.new('RGBA', (64, 64), (40, 40, 48, 255))
        bg.alpha_composite(imgs[len(imgs) // 4])
        out.paste(bg.resize((128, 128), Image.NEAREST), ((i % cols) * 160 + 16, (i // cols) * 176 + 8))
        ImageDraw.Draw(out).text(((i % cols) * 160 + 16, (i // cols) * 176 + 142), name[:22], fill=(200, 200, 220))
    out.save(os.path.join(OUT, 'mod_set_64.png'))


def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--mod':
        mod_textures()
        return
    sheet_tiles = []
    for name, fn, frames, frametime in ITEMS:
        for size in (64, 128):
            imgs = [fn(size, t, frames) for t in range(frames)]
            strip = Image.new('RGBA', (size, size * frames))
            for i, im in enumerate(imgs): strip.paste(im, (0, i * size))
            base = os.path.join(OUT, f'{name}_{size}')
            strip.save(base + '.png', optimize=True)
            with open(base + '.png.mcmeta', 'w') as f:
                f.write('{\n  "animation": {\n    "frametime": %d\n  }\n}\n' % frametime)
            # Preview GIF on a dark slot background, scaled up for viewing.
            view = []
            for im in imgs:
                bg = Image.new('RGBA', (size, size), (40, 40, 48, 255))
                bg.alpha_composite(im)
                view.append(bg.resize((256, 256), Image.NEAREST).convert('P', palette=Image.ADAPTIVE))
            view[0].save(base + '.gif', save_all=True, append_images=view[1:], duration=frametime * 50, loop=0)
            sheet_tiles.append((name, size, imgs[0], imgs[frames // 3]))
            print(f'{name} {size}x: {frames} frames')
    # Comparison sheet: each item at 64x and 128x, two frames, plus the 16x look of the 128x art.
    cell = 256
    sheet = Image.new('RGBA', (cell * 5, cell * len(ITEMS)), (24, 22, 32, 255))
    for row, (name, _, _, _) in enumerate(ITEMS):
        tiles = [t for t in sheet_tiles if t[0] == name]
        col = 0
        for _, size, f0, f1 in tiles:
            for f in (f0, f1):
                bg = Image.new('RGBA', (size, size), (40, 40, 48, 255))
                bg.alpha_composite(f)
                sheet.paste(bg.resize((cell, cell), Image.NEAREST), (col * cell, row * cell))
                col += 1
        small = tiles[-1][2].resize((16, 16), Image.LANCZOS)
        bg = Image.new('RGBA', (16, 16), (40, 40, 48, 255))
        bg.alpha_composite(small)
        sheet.paste(bg.resize((cell, cell), Image.NEAREST), (col * cell, row * cell))
    sheet.save(os.path.join(OUT, 'comparison.png'))


if __name__ == '__main__':
    main()
