"""Originals material sets, second pass: 32x32 animated items and 128x128 halos.

Takes the approach of the Cosmic Frontier material sets (studied in cosmiccore 0.8.5 / 0.21.5): high resolution
icons with long animations and frame events, and halos that read as a shape (vortex, tentacles, beams) instead of a
soft blur. Everything here is generated; nothing is copied from Cosmic Frontier.

    python3 originals_cf_style.py preview      # GIFs + sheet in the scratch dir given by --out
    python3 originals_cf_style.py install      # writes textures and models into the GTNA assets
"""

import colorsys
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from generate_all_originals_proposals import CUSTOM_BLOCK, ROOT, base_of
from install_winning_originals_materials import MATERIAL_SPECS, overlay_of

F = 48  # frames per loop, 2 ticks each = 4.8 s
HS = 128  # halo resolution
TAU = 2 * np.pi
HALO_FORMS = {"ingot", "gem", "dust", "plate", "rod", "wire_fine"}

TEX_ITEMS = ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets"
TEX_BLOCKS = ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets"
MODEL_ITEMS = ROOT / "src/main/resources/assets/gtceu/models/item/material_sets"
HALO_TEX = ROOT / "src/main/resources/assets/gtna/textures/item/effect"


# ---------------------------------------------------------------- helpers

def ramp(v, stops):
    v = np.clip(v, 0, 1)
    xs = [s[0] for s in stops]
    return np.stack([np.interp(v, xs, [s[1][c] / 255 for s in stops]) for c in range(3)], -1)


def hexs(*cols):
    out = []
    for i, c in enumerate(cols):
        c = c.lstrip("#")
        out.append((i / (len(cols) - 1), tuple(int(c[j:j + 2], 16) for j in (0, 2, 4))))
    return out


class Noise:
    """Tileable value noise on a period-n grid; sampling at (x + R cos t, y + R sin t) loops in time."""

    def __init__(self, seed, n=8):
        self.g = np.random.default_rng(seed).random((n, n))
        self.n = n

    def __call__(self, x, y):
        n = self.n
        x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
        fx, fy = x - x0, y - y0
        fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        g = self.g
        a = g[y0 % n, x0 % n] * (1 - fx) + g[y0 % n, (x0 + 1) % n] * fx
        b = g[(y0 + 1) % n, x0 % n] * (1 - fx) + g[(y0 + 1) % n, (x0 + 1) % n] * fx
        return a * (1 - fy) + b * fy

    def fbm(self, x, y, oct=3):
        s, amp, tot = 0, 1, 0
        for o in range(oct):
            s = s + amp * self(x * 2 ** o + o * 3.7, y * 2 ** o + o * 1.3)
            tot += amp
            amp *= 0.5
        return s / tot


def loop_noise(nz, x, y, t, radius=1.5, oct=3):
    return nz.fbm(x + radius * np.cos(TAU * t), y + radius * np.sin(TAU * t), oct)


def smooth(e0, e1, v):
    v = np.clip((v - e0) / (e1 - e0), 0, 1)
    return v * v * (3 - 2 * v)


def up2(a):
    return np.repeat(np.repeat(a, 2, 0), 2, 1)


def sparkle_field(seed, shape, count, mask):
    rng = np.random.default_rng(seed)
    ys, xs = np.nonzero(mask)
    if len(ys) == 0:
        return []
    idx = rng.choice(len(ys), size=min(count, len(ys)), replace=False)
    return [(ys[i], xs[i], rng.random(), 0.6 + 0.8 * rng.random()) for i in idx]


def twinkle(stars, shape, t, width=0.12, cross=True):
    out = np.zeros(shape, np.float32)
    for (y, x, ph, sp) in stars:
        d = ((t * sp + ph) % 1.0)
        v = max(0.0, 1 - abs(d - 0.5) / width) if abs(d - 0.5) < width else 0.0
        if v <= 0:
            continue
        out[y, x] = max(out[y, x], v)
        if cross and v > 0.5:
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                yy, xx = y + dy, x + dx
                if 0 <= yy < shape[0] and 0 <= xx < shape[1]:
                    out[yy, xx] = max(out[yy, xx], (v - 0.5) * 1.4)
    return out


# ---------------------------------------------------------------- item frames (32x32)

def item_layers(base16, overlay16):
    base = up2(base16)
    ov = up2(np.array(overlay16, dtype=np.float32)) / 255
    a = base[..., 3] > 0
    gray = base[..., :3].mean(-1) / 255
    h, w = a.shape
    y, x = np.mgrid[:h, :w].astype(np.float32)
    cy, cx = (y[a].mean(), x[a].mean()) if a.any() else (h / 2, w / 2)
    r = np.hypot(x - cx, y - cy)
    r = r / max(1.0, r[a].max() if a.any() else 16)
    edge = a & (~np.roll(a, 1, 0) | ~np.roll(a, -1, 0) | ~np.roll(a, 1, 1) | ~np.roll(a, -1, 1))
    return dict(a=a, gray=gray, x=x, y=y, r=r, th=np.arctan2(y - cy, x - cx), edge=edge, ov=ov)


def hsv_img(h, s, v):
    f = np.vectorize(colorsys.hsv_to_rgb)
    return np.stack(f(h % 1.0, np.clip(s, 0, 1), np.clip(v, 0, 1)), -1)


def item_frame(mat, L, k):
    t = k / F
    a, g, x, y, r, th, edge = L["a"], L["gray"], L["x"], L["y"], L["r"], L["th"], L["edge"]
    nz = NOISE[mat]
    tex = loop_noise(nz, x / 6, y / 6, t, 1.0, 2)  # fine grain, keeps the 32 px detail alive
    v = g * 0.85 + (tex - 0.5) * 0.18
    add = np.zeros(a.shape + (3,), np.float32)
    interp = True
    S = SPARKS[mat]

    if mat == "nexium":
        band = np.exp(-(((x + y) / 64 - (t * 1.6 % 1.6 - 0.3)) / 0.06) ** 2)
        col = ramp(v + band * 0.35, PAL[mat])
        arc = twinkle(S, a.shape, t * 3, 0.05)
        add += arc[..., None] * np.array([0.6, 1.0, 1.0]) + band[..., None] * np.array([0.1, 0.35, 0.35])
    elif mat == "primordial_tholin":
        drift = loop_noise(nz, x / 10, y / 10 + t * 2, t, 0.6, 3)
        col = ramp(v * 0.75 + drift * 0.3, PAL[mat])
        add += twinkle(S, a.shape, t, 0.08)[..., None] * np.array([0.75, 0.9, 1.0])
    elif mat == "magnetar_crystal":
        beam = np.cos(th - TAU * t) ** 16 + np.cos(th - TAU * t + np.pi) ** 16
        col = ramp(v + beam * 0.3 * (0.4 + r), PAL[mat])
        add += twinkle(S, a.shape, t * 2, 0.07)[..., None] * np.array([1.0, 0.85, 1.0])
        add += (beam * (r > 0.3))[..., None] * np.array([0.25, 0.15, 0.4])
    elif mat == "degenerate_core_matter":
        wave = 0.5 + 0.5 * np.sin(r * 18 + TAU * t * 3)
        col = ramp(v * 0.8 + wave * 0.25, PAL[mat])
        add += (smooth(0.85, 1, wave) * (1 - r))[..., None] * np.array([0.35, 0.4, 0.55])
    elif mat == "magnetarium":
        lines = 0.5 + 0.5 * np.sin(np.sin(th) ** 2 / np.maximum(r, 0.08) * 3 - TAU * t * 2)
        col = ramp(v * 0.8 + lines * 0.25, PAL[mat])
        add += twinkle(S, a.shape, t, 0.06)[..., None] * np.array([0.7, 0.6, 1.0])
    elif mat == "prismatium":
        hue = g * 0.35 + (x + y) / 80 + t
        col = hsv_img(hue, 0.55 - g * 0.25, 0.35 + v * 0.75)
        add += twinkle(S, a.shape, t * 2, 0.06)[..., None] * 1.0
    elif mat == "chronomercury":
        flow = loop_noise(nz, x / 9 + t * 3, y / 9, t, 0.8, 3)
        col = ramp(v * 0.6 + flow * 0.45, PAL[mat])
        # the rewind: a short glitch where the colour channels slip apart, like time catching up
        if 34 <= k <= 38:
            interp = False
            sh = 2 if k % 2 else -2
            col = np.stack([np.roll(col[..., 0], sh, 1), col[..., 1], np.roll(col[..., 2], -sh, 1)], -1)
            col = col * 0.7 + np.array([0.15, 0.25, 0.35])
    elif mat == "forgecore":
        heat = loop_noise(nz, x / 7, y / 7 + t * 4, t, 0.5, 3)
        cracks = smooth(0.62, 0.75, heat)
        col = ramp(v * 0.65 + heat * 0.3, PAL[mat])
        add += cracks[..., None] * np.array([0.5, 0.35, 0.05])
        add += twinkle(S, a.shape, t * 2, 0.05)[..., None] * np.array([1.0, 0.8, 0.3])
    elif mat == "vivispore":
        cells = np.zeros(a.shape, np.float32)
        for i, (cy_, cx_, ph, sp) in enumerate(S):
            p = 0.5 + 0.5 * np.sin(TAU * (t * 2 + ph))
            cells += p * np.exp(-((x - cx_) ** 2 + (y - cy_) ** 2) / 5)
        col = ramp(v * 0.75 + cells * 0.25, PAL[mat])
        add += np.clip(cells, 0, 1)[..., None] * np.array([0.3, 0.55, 0.05])
    elif mat == "abyssal_antimatter":
        col = ramp(v * 0.7, PAL[mat])
        add += twinkle(S, a.shape, t, 0.1, cross=False)[..., None] * np.array([0.85, 0.7, 1.0])
        if k in (20, 21, 22):  # annihilation flash: the whole grain flips to its own negative for a beat
            interp = False
            col = 1 - col * np.array([0.6, 1.0, 0.4])
    elif mat == "precursor_residue":
        hx = (np.abs(((x + (y // 6 % 2) * 3) % 6) - 3) < 0.6) | (y % 6 < 0.6)
        scan = np.exp(-((y / 32 - (t * 1.4 % 1.4 - 0.2)) / 0.05) ** 2)
        col = ramp(v * 0.85, PAL[mat])
        add += (hx * scan)[..., None] * np.array([0.9, 0.75, 0.3])
        add += twinkle(S, a.shape, t * 2, 0.05)[..., None] * np.array([1.0, 0.95, 0.6])
    elif mat == "void_ash":
        col = ramp(v * 0.55, PAL[mat])
        for (sy, sx, ph, sp) in S:  # embers rising and dying out
            p = (t * sp + ph) % 1.0
            yy = int(sy - p * 10) % a.shape[0]
            if a[yy, sx]:
                add[yy, sx] += np.array([0.55, 0.35, 0.7]) * (1 - p)
    rgb = np.clip(col + add, 0, 1)
    # original outline darkening + the Modernity highlight overlay
    rgb = rgb * np.where(edge, 0.72, 1.0)[..., None]
    ov = L["ov"]
    rgb = rgb * (1 - ov[..., 3:]) + ov[..., :3] * ov[..., 3:]
    out = np.zeros(a.shape + (4,), np.uint8)
    out[..., :3] = (rgb * 255).astype(np.uint8)
    out[..., 3] = (a * 255).astype(np.uint8)
    return out, interp


# ---------------------------------------------------------------- halos (128x128)

_y, _x = (np.mgrid[:HS, :HS].astype(np.float32) + 0.5) / HS * 2 - 1
HR = np.hypot(_x, _y)
HT = np.arctan2(_y, _x)


def angdist(a, b):
    return np.abs((a - b + np.pi) % TAU - np.pi)


def halo(mat, k):
    t = k / F
    r, th, x, y = HR, HT, _x, _y
    nz = NOISE[mat]
    rgb = np.zeros((HS, HS, 3), np.float32)
    al = np.zeros((HS, HS), np.float32)

    def put(c, a):
        nonlocal rgb, al
        a = np.clip(a, 0, 1)
        rgb = rgb * (1 - a[..., None]) + np.array(c, np.float32) * a[..., None]
        al = al + a * (1 - al)

    glow = np.exp(-((r - 0.5) / 0.22) ** 2)
    if mat == "nexium":
        put((0.05, 0.6, 0.6), glow * 0.35)
        rot = th - TAU * t / 2
        s2 = np.sin(rot) ** 2
        Lp = r / np.maximum(s2, 1e-3)
        for i, L0 in enumerate((0.62, 0.8, 1.05, 1.4)):
            line = np.exp(-((Lp - L0) / (0.025 + 0.012 * i)) ** 2) * (r > 0.38) * (r < 0.97)
            flow = 0.55 + 0.45 * np.sin(rot * 6 - TAU * t * 4 + i)
            put((0.55, 1.0, 0.95), line * flow)
    elif mat == "primordial_tholin":
        haze = loop_noise(nz, x * 3, y * 3, t, 0.8, 4)
        put((0.55, 0.17, 0.09), np.clip(glow * (0.4 + haze) * 1.3, 0, 0.85))
        head = TAU * t
        trail = angdist(th, head)
        behind = ((head - th) % TAU) < 2.4
        tail = np.exp(-((r - 0.74) / (0.07 + 0.08 * trail)) ** 2) * np.exp(-trail * 0.9) * 1.3 * behind
        put((0.86, 0.45, 0.28), tail)
        coma = np.exp(-((x - 0.74 * np.cos(head)) ** 2 + (y - 0.74 * np.sin(head)) ** 2) / 0.01)
        put((0.95, 0.98, 1.0), coma * 1.5)
        ice = twinkle(SPARKS_H[mat], (HS, HS), t * 2, 0.08)
        put((0.8, 0.92, 1.0), ice)
    elif mat == "magnetar_crystal":
        put((0.35, 0.15, 0.75), glow * 0.45)
        ang = TAU * t
        for off in (0, np.pi):
            d = angdist(th, ang + off)
            beam = np.exp(-(d * (2 + 6 * r) / 0.16) ** 2) * smooth(0.3, 0.5, r) * (1 - smooth(0.8, 1, r))
            flash = 1 + 1.5 * np.exp(-(angdist(ang + off, -np.pi / 2) / 0.25) ** 2)
            put((0.82, 0.7, 1.0), beam * 0.8 * flash)
        put((0.95, 0.9, 1.0), np.exp(-((r - 0.48) / 0.015) ** 2) * 0.6)
    elif mat == "degenerate_core_matter":
        arms = 0.5 + 0.5 * np.sin(4 * th + 7 * np.log(np.maximum(r, 0.05)) + TAU * t * 2)
        body = smooth(0.25, 0.45, r) * (1 - smooth(0.75, 1, r))
        put((0.12, 0.15, 0.32), body * 0.45)
        put((0.75, 0.82, 1.0), body * smooth(0.55, 0.95, arms))
        for i in range(3):
            rr = 0.95 - ((t * 3 + i / 3) % 1) * 0.5
            put((0.9, 0.95, 1.0), np.exp(-((r - rr) / 0.012) ** 2) * (rr - 0.4) * 1.6)
    elif mat == "magnetarium":
        put((0.3, 0.2, 0.75), glow * 0.55)
        gx, gy = (x * 9 + 0.5) % 1 - 0.5, (y * 9 + 0.5) % 1 - 0.5
        bx = 3 * x * y
        by = 2 * y * y - x * x
        n = np.maximum(np.hypot(bx, by), 1e-4)
        ux, uy = bx / n, by / n
        along = gx * ux + gy * uy
        perp = np.abs(-gx * uy + gy * ux)
        dash = (np.abs(along) < 0.32) * np.exp(-(perp / 0.07) ** 2)
        wave = 0.35 + 0.65 * smooth(0.6, 1, np.sin(r * 14 - TAU * t * 3))
        put((0.82, 0.74, 1.0), 1.7 * dash * wave * smooth(0.38, 0.5, r) * (1 - smooth(0.85, 1, r)))
    elif mat == "prismatium":
        n_rays = 12
        ph = th * n_rays / TAU - t * 2
        ray = np.exp(-(((ph + 0.5) % 1 - 0.5) / 0.12) ** 2) * smooth(0.35, 0.5, r) * (1 - smooth(0.7, 1.0, r))
        tw = 0.6 + 0.4 * np.sin(np.floor(ph) * 2.3 + TAU * t * 3)
        hue = (th / TAU + t) % 1
        col = hsv_img(hue, np.full_like(r, 0.85), np.ones_like(r))
        a = ray * tw
        rgb = rgb * (1 - a[..., None]) + col * a[..., None]
        al = al + a * (1 - al)
        ring = np.exp(-((r - 0.55) / 0.03) ** 2) * 0.7
        rgb = rgb * (1 - ring[..., None]) + hsv_img(hue + 0.5, np.full_like(r, 0.6), np.ones_like(r)) * ring[..., None]
        al = al + ring * (1 - al)
    elif mat == "chronomercury":
        put((0.5, 0.56, 0.66), glow * 0.3)
        put((0.9, 0.94, 1.0), np.exp(-((r - 0.8) / 0.018) ** 2) * 0.9)
        tick = np.exp(-(((th * 12 / TAU + 0.5) % 1 - 0.5) / 0.06) ** 2) * (r > 0.84) * (r < 0.94)
        put((0.95, 0.97, 1.0), tick)
        for speed, length, wdt in ((1, 0.76, 0.05), (-4, 0.66, 0.035)):
            ang = TAU * t * speed - np.pi / 2
            d = np.abs(-x * np.sin(ang) + y * np.cos(ang))
            along = x * np.cos(ang) + y * np.sin(ang)
            hand = np.exp(-(d / wdt) ** 2) * (along > 0.42) * (along < length)
            put((0.82, 0.88, 1.0), hand)
        runes = 0.5 + 0.5 * np.sin(th * 24 + TAU * t * 2)
        put((0.6, 0.7, 0.85), np.exp(-((r - 0.62) / 0.02) ** 2) * smooth(0.7, 1, runes))
    elif mat == "forgecore":
        flame = loop_noise(nz, th * 3 / np.pi * 2, r * 4 - t * 6, t, 0.7, 4)
        reach = 0.5 + 0.38 * flame
        fire = smooth(0.38, 0.48, r) * (1 - smooth(reach - 0.08, reach, r))
        put((0.9, 0.3, 0.02), fire * 0.9)
        put((1.0, 0.75, 0.25), fire * smooth(0.55, 0.85, flame))
        for i in range(3):
            c = TAU * (i / 3 + t / 3)
            px, py = 0.66 * np.cos(c), 0.66 * np.sin(c)
            d = np.hypot(x - px, y - py)
            loop = np.exp(-((d - 0.17) / 0.02) ** 2) * (r > 0.5)
            put((1.0, 0.85, 0.45), loop * (0.6 + 0.4 * np.sin(TAU * t * 4 + i)))
    elif mat == "vivispore":
        put((0.15, 0.4, 0.05), glow * 0.35)
        n_t = 7
        wob = th + 0.25 * np.sin(r * 9 - TAU * t * 2)
        arm = np.exp(-(((wob * n_t / TAU + 0.5) % 1 - 0.5) / (0.16 * (1.1 - r))) ** 2)
        put((0.45, 0.85, 0.1), arm * smooth(0.35, 0.5, r) * (1 - smooth(0.7, 0.95, r)))
        for (sy, sx, ph, sp) in SPARKS_H[mat]:
            p = (t * sp + ph) % 1
            ang = np.arctan2(sy - 64, sx - 64)
            rr = 0.45 + 0.5 * p
            d = (x - rr * np.cos(ang)) ** 2 + (y - rr * np.sin(ang)) ** 2
            put((0.85, 1.0, 0.5), np.exp(-d / 0.0012) * (1 - p))
    elif mat == "abyssal_antimatter":
        n_t = 9
        wob = th + 0.35 * np.sin(r * 8 - TAU * t * 2 + th * 2)
        arm = np.exp(-(((wob * n_t / TAU + 0.5) % 1 - 0.5) / (0.2 * (1.05 - r))) ** 2)
        shape = np.clip(arm * (1 - smooth(0.6, 0.98, r)) + (1 - smooth(0.4, 0.55, r)), 0, 1)
        put((0.02, 0.0, 0.05), shape * 0.95)
        rim = np.clip(shape - np.roll(shape, 2, 0) * 0.5 - np.roll(shape, -2, 1) * 0.5, 0, 1)
        put((0.6, 0.25, 1.0), rim * 0.8)
        acc = np.exp(-((r - 0.56) / 0.02) ** 2) * (0.4 + 0.6 * smooth(0.5, 1, np.sin(th * 5 - TAU * t * 3)))
        put((0.85, 0.6, 1.0), acc)
    elif mat == "precursor_residue":
        put((0.4, 0.3, 0.08), glow * 0.25)
        q = (x * 2 / 3) * 5.5
        rr_ = (-x / 3 + y / np.sqrt(3)) * 5.5
        cq, cr = np.round(q), np.round(rr_)
        cs = np.round(-q - rr_)
        dq, dr, ds = np.abs(cq - q), np.abs(cr - rr_), np.abs(cs + q + rr_)
        cq = np.where((dq > dr) & (dq > ds), -cr - cs, cq)
        cr = np.where(~((dq > dr) & (dq > ds)) & (dr > ds), -cq - cs, cr)
        edgeh = np.maximum(np.maximum(dq, dr), ds)
        cell_id = (cq * 7.13 + cr * 3.71) % 1
        on = smooth(0.35, 0.6, np.sin(TAU * (cell_id * 3 + t * 2)) * 0.5 + 0.5)
        band = smooth(0.42, 0.52, r) * (1 - smooth(0.8, 0.95, r))
        orbit = 0.5 + 0.5 * np.cos(th - TAU * t)
        put((0.95, 0.78, 0.3), smooth(0.36, 0.48, edgeh) * band * (0.25 + 0.75 * on) * (0.4 + 0.6 * orbit))
        put((1.0, 0.92, 0.6), (edgeh < 0.2) * band * on * orbit * 0.6)
    elif mat == "void_ash":
        swirl = loop_noise(nz, (th / TAU + t * 0.25) * 8, np.log(np.maximum(r, 0.05)) * 3 + t * 4, 0, 0, 3)
        disk = smooth(0.3, 0.45, r) * (1 - smooth(0.7, 1.0, r))
        put((0.02, 0.02, 0.03), disk * (0.55 + 0.45 * swirl))
        for (sy, sx, ph, sp) in SPARKS_H[mat]:
            p = (t * sp + ph) % 1
            ang = np.arctan2(sy - 64, sx - 64) + p * 2.5
            rr = 0.95 - 0.5 * p
            d = (x - rr * np.cos(ang)) ** 2 + (y - rr * np.sin(ang)) ** 2
            put((0.7, 0.62, 0.85), np.exp(-d / 0.0009) * p)
    al = al * (1 - smooth(0.9, 1.0, r)) * 0.85
    out = np.zeros((HS, HS, 4), np.uint8)
    out[..., :3] = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    out[..., 3] = (np.clip(al, 0, 1) * 255).astype(np.uint8)
    return out


# ---------------------------------------------------------------- per-material data

PAL = {
    "nexium": hexs("031a1e", "0b4f52", "169e94", "5fe6d2", "e6fffb"),
    "primordial_tholin": hexs("1a0504", "4e120d", "8d2a1c", "c25d40", "f0b494"),
    "magnetar_crystal": hexs("0c0424", "301276", "6a42e2", "b49aff", "f6f0ff"),
    "degenerate_core_matter": hexs("06081c", "222c66", "5f74c4", "c4d2fc", "ffffff"),
    "magnetarium": hexs("0e0926", "2e2070", "5f4bd2", "a596ff", "f0ebff"),
    "prismatium": hexs("101828", "41608f", "8cb4e6", "d7ebff", "ffffff"),
    "chronomercury": hexs("12151c", "3e4858", "7f8ea6", "c5d2e3", "ffffff"),
    "forgecore": hexs("260500", "841f00", "e8550a", "ffb43c", "fff5b4"),
    "vivispore": hexs("0a1a04", "2b5a12", "69b42d", "b9ee64", "ebffbe"),
    "abyssal_antimatter": hexs("040108", "180a2c", "441c73", "9b4beb", "ebb4ff"),
    "precursor_residue": hexs("261908", "5f4418", "aa843a", "e4c373", "fcf0c0"),
    "void_ash": hexs("030305", "0e0e16", "24242f", "4f4f63", "8d8da6"),
}
HALO_SIZE = {"nexium": 5, "primordial_tholin": 5, "magnetar_crystal": 5, "degenerate_core_matter": 4,
             "magnetarium": 5, "prismatium": 5, "chronomercury": 5, "forgecore": 5, "vivispore": 5,
             "abyssal_antimatter": 5, "precursor_residue": 5, "void_ash": 5}
HALO_NAME = {"nexium": "nexium_field", "primordial_tholin": "tholin_comet_tail",
             "magnetar_crystal": "magnetar_pulsar", "degenerate_core_matter": "degenerate_compression",
             "magnetarium": "magnetarium_dipole_torus", "prismatium": "prismatium_rainbow_corona",
             "chronomercury": "chronomercury_hourglass_vortex", "forgecore": "forgecore_coronal_loops",
             "vivispore": "vivispore_toxic_phosphor", "abyssal_antimatter": "abyssal_hawking_glow",
             "precursor_residue": "precursor_nanite_swarm", "void_ash": "void_entropy_sink"}
MATS = list(PAL)
NOISE = {m: Noise(i * 31 + 7) for i, m in enumerate(MATS)}
_full32 = np.ones((32, 32), bool)
SPARKS = {m: sparkle_field(i + 100, (32, 32), 9, _full32) for i, m in enumerate(MATS)}
_ring = (HR > 0.45) & (HR < 0.9)
SPARKS_H = {m: sparkle_field(i + 200, (HS, HS), 14, _ring) for i, m in enumerate(MATS)}


def mask_sparks(mat, a):
    """Sparks only on the icon's own pixels."""
    return [s for s in sparkle_field(MATS.index(mat) + 100, a.shape, 12, a)]


def item_strip(mat, form, profile):
    if form == "block" or form == "frame_gt":
        src = CUSTOM_BLOCK / ("frameGt.png" if form == "frame_gt" else "block1.png")
        base16 = np.array(Image.open(src).convert("RGBA"), dtype=np.float32)[:16]
        overlay = Image.new("RGBA", (16, 16))
    else:
        base16 = base_of(form, profile)
        overlay = overlay_of(form, profile)
    L = item_layers(base16, overlay)
    SPARKS[mat] = mask_sparks(mat, L["a"] & ~L["edge"])
    frames, interps = zip(*(item_frame(mat, L, k) for k in range(F)))
    return np.concatenate(frames, 0), all(interps)


def halo_strip(mat):
    return np.concatenate([halo(mat, k) for k in range(F)], 0)


def mcmeta(interp):
    return json.dumps({"animation": {"frametime": 2, "interpolate": interp}}, indent=2) + "\n"


def primary(mat):
    items = MATERIAL_SPECS[mat]["items"]
    return next(f for f in ("ingot", "gem", "dust") if f in items)


def composite(icon, halo_img, size, scale=4, bg=(54, 54, 66)):
    """Slot view: the halo quad spans 16 + 2*size pixels around the 16 px slot."""
    span = 16 + 2 * size
    cell = Image.new("RGBA", (span * scale, span * scale), bg + (255,))
    cell.alpha_composite(Image.fromarray(halo_img).resize((span * scale, span * scale), Image.BILINEAR))
    ic = Image.fromarray(icon).resize((16 * scale, 16 * scale), Image.NEAREST)
    cell.alpha_composite(ic, (size * scale, size * scale))
    return cell


def preview(out):
    out.mkdir(parents=True, exist_ok=True)
    cells = []
    for mat in MATS:
        prof = MATERIAL_SPECS[mat]["profile"]
        strip, _ = item_strip(mat, primary(mat), prof)
        hstrip = halo_strip(mat)
        s = HALO_SIZE[mat]
        frames = [composite(strip[k * 32:(k + 1) * 32], hstrip[k * HS:(k + 1) * HS], s) for k in range(F)]
        frames[0].save(out / f"{mat}.gif", save_all=True, append_images=frames[1:], duration=100, loop=0,
                       disposal=2)
        cells.append([frames[k].resize((184, 184)) for k in (0, 12, 24, 36)])
        print("preview", mat)
    sheet = Image.new("RGBA", (len(cells) * 190, 4 * 190), (30, 30, 38, 255))
    for i, col in enumerate(cells):
        for j, c in enumerate(col):
            sheet.alpha_composite(c, (i * 190 + 3, j * 190 + 3))
    sheet.save(out / "sheet.png")


def install():
    HALO_TEX.mkdir(parents=True, exist_ok=True)
    for mat in MATS:
        spec = MATERIAL_SPECS[mat]
        folder = f"gtna_{mat}"
        halo_name = HALO_NAME[mat]
        Image.fromarray(halo_strip(mat)).save(HALO_TEX / f"{halo_name}.png")
        (HALO_TEX / f"{halo_name}.png.mcmeta").write_text(mcmeta(True))
        for form in spec["items"]:
            strip, interp = item_strip(mat, form, spec["profile"])
            d = TEX_ITEMS / folder
            Image.fromarray(strip).save(d / f"{form}.png")
            (d / f"{form}.png.mcmeta").write_text(mcmeta(interp))
            for extra in ("overlay", "secondary"):
                Image.new("RGBA", (32, 32)).save(d / f"{form}_{extra}.png")
            model = {"parent": "item/generated",
                     "textures": {"layer0": f"gtceu:item/material_sets/{folder}/{form}"}}
            if form in HALO_FORMS:
                model["textures"]["halo"] = f"gtna:item/effect/{halo_name}"
                model["loader"] = "gtna:halo"
                model["halo"] = {"texture": "#halo", "color": -1, "size": HALO_SIZE[mat], "pulse": False}
            (MODEL_ITEMS / folder / f"{form}.json").write_text(json.dumps(model, indent=2) + "\n")
        for block in spec["blocks"]:
            strip, interp = item_strip(mat, block, None)
            d = TEX_BLOCKS / folder
            Image.fromarray(strip).save(d / f"{block}.png")
            (d / f"{block}.png.mcmeta").write_text(mcmeta(interp))
        print("installed", mat)


if __name__ == "__main__":
    if sys.argv[1] == "preview":
        preview(Path(sys.argv[2]))
    else:
        install()
