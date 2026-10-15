#!/usr/bin/env python3
"""UI v2 mockups drawn the way Minecraft draws a GUI: every element on whole GUI pixels, no anti-aliasing, the
vanilla bitmap font (assets/minecraft/textures/font/ascii.png from the client jar) with its 1 px drop shadow, glows
dithered instead of blurred, 9x9 pixel-art icons; then scaled 3x nearest-neighbour like GUI scale 3.

    python3 tools/design/generate_ui_v2_pixel.py <ascii.png>   ->  tools/design/ui_v2_pixel/
"""
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

SCALE = 3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_v2_pixel')
os.makedirs(OUT, exist_ok=True)

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


# ----------------------------------------------------------------------------------------------- vanilla font
class MCFont:
    def __init__(self, path):
        sheet = Image.open(path).convert('RGBA')
        self.cell = sheet.width // 16
        self.glyphs, self.widths = {}, {}
        a = np.asarray(sheet)[..., 3]
        for code in range(256):
            gx, gy = (code % 16) * self.cell, (code // 16) * self.cell
            cell = a[gy:gy + self.cell, gx:gx + self.cell]
            cols = np.where(cell.max(axis=0) > 0)[0]
            self.widths[code] = 4 if code == 32 else (cols.max() + 2 if len(cols) else 0)
            self.glyphs[code] = sheet.crop((gx, gy, gx + self.cell, gy + self.cell))

    def width(self, s):
        return sum(self.widths.get(ord(ch), 6) for ch in s) - 1

    def draw(self, img, x, y, s, colour, shadow=True):
        if shadow: self._draw(img, x + 1, y + 1, s, tuple(int(c * 0.25) for c in colour[:3]))
        self._draw(img, x, y, s, colour[:3])

    def _draw(self, img, x, y, s, rgb):
        for ch in s:
            code = ord(ch)
            if code < 256 and self.widths.get(code):
                g = self.glyphs[code]
                tinted = Image.new('RGBA', g.size, rgb + (255,))
                tinted.putalpha(g.getchannel('A'))
                img.alpha_composite(tinted, (x, y))
            x += self.widths.get(code, 6)


FONT = None

# ----------------------------------------------------------------------------------------------- icons (9x9)
ICONS = {
    'left': ["....#....", "...##....", "..###....", ".####....", "#####....", ".####....", "..###....", "...##....",
             "....#...."],
    'right': ["....#....", "....##...", "....###..", "....####.", "....#####", "....####.", "....###..",
              "....##...", "....#...."],
    'auto': [".#######.", "#.......#", "#..###..#", "#.#...#.#", "#.#####.#", "#.#...#.#", "#.#...#.#",
             "#.......#", ".#######."],
    'orbit': ["..#####..", ".#.....#.", "#...#...#", "#..###..#", "#.#####.#", "#..###..#", "#...#...#",
              ".#.....#.", "..#####.."],
    'gear': ["...#.#...", ".#.###.#.", "..#####..", "###...###", ".##.#.##.", "###...###", "..#####..",
             ".#.###.#.", "...#.#..."],
    'capsule': ["...###...", "..#####..", "..#####..", "..#####..", "..#####..", ".#######.", ".#.###.#.",
                "#...#...#", "........."],
    'info': ["...###...", "...###...", ".........", "..####...", "...###...", "...###...", "...###...",
             "..#####..", "........."],
    'power': ["....#....", ".#..#..#.", "#...#...#", "#...#...#", "#.......#", "#.......#", "#.......#",
              ".#.....#.", "..#####.."],
    'minus': [".........", ".........", ".........", ".........", "#########", ".........", ".........",
              ".........", "........."],
    'plus': ["....#....", "....#....", "....#....", "....#....", "#########", "....#....", "....#....",
             "....#....", "....#...."],
    'bolt': ["....###..", "...###...", "..###....", ".#######.", "....###..", "...###...", "..###....",
             ".##......", "#........"],
    'chart': ["#........", "#......#.", "#.....#..", "#..#.#...", "#.#.#....", "##.......", "#........",
              "#########", "........."],
    'wave': [".........", ".........", "....#....", "...#.#...", "#.#...#.#", ".#.....#.", ".........",
             ".........", "........."],
    'star': ["....#....", "....#....", "...###...", "#########", ".#######.", "..#####..", ".###.###.",
             ".##...##.", "#.......#"],
    'swap': ["..#......", ".##......", "#########", ".##......", "..#...#..", "......##.", "#########",
             "......##.", "......#.."],
    'atom': ["#.......#", ".#.....#.", "..#####..", "..#.#.#..", "..##.##..", "..#.#.#..", "..#####..",
             ".#.....#.", "#.......#"],
    'list': ["##.######", ".........", "##.######", ".........", "##.######", ".........", "##.######",
             ".........", "........."],
    'snow': ["....#....", ".#..#..#.", "..#.#.#..", "...###...", "#########", "...###...", "..#.#.#..",
             ".#..#..#.", "....#...."],
    'ring': ["..#####..", ".#.....#.", "#.......#", "#.......#", "#.......#", "#.......#", "#.......#",
             ".#.....#.", "..#####.."],
    'open': ["..#####..", ".#.....#.", "#..###..#", "#.#...#.#", "#.#.#.#.#", "#.#...#.#", "#..###..#",
             ".#.....#.", "..#####.."],
    'close': ["#.......#", ".#.....#.", "..#...#..", "...#.#...", "....#....", "...#.#...", "..#...#..",
              ".#.....#.", "#.......#"],
    'note': ["....####.", "....#..#.", "....#..#.", "....#..#.", "....#..#.", "..###.##.", ".####.##.",
             ".###.....", "........."],
    'map': ["#...#...#", "#..##..##", "#.#.#.#.#", "##..##..#", "#...#...#", "#...#...#", "#...#...#",
            "#...#...#", "........."],
    'down': ["....#....", "....#....", "....#....", "....#....", "#...#...#", ".#..#..#.", "..#.#.#..",
             "...###...", "....#...."],
    'io': ["#########", "#.......#", "#.#####.#", "#.#...#.#", "#.#...#.#", "#.#...#.#", "#.#####.#",
           "#.......#", "#########"],
}


def icon(img, x, y, name, colour):
    px = img.load()
    for j, row in enumerate(ICONS[name]):
        for i, ch in enumerate(row):
            if ch == '#':
                px[x + i, y + j] = colour + (255,)
                if x + i + 1 < img.width and y + j + 1 < img.height and \
                        (j + 1 >= 9 or ICONS[name][j + 1][i] != '#'):
                    pass


# ----------------------------------------------------------------------------------------------- palette
THEMES = {
    'lance': dict(name='Kinetic Orbital Lance', accent=(255, 170, 40), glow=(255, 226, 160), base=(20, 17, 24),
                  panel=(46, 40, 48), hi=(92, 82, 92), lo=(18, 14, 20), line=(110, 84, 52), dim=(168, 150, 128)),
    'stellar': dict(name='Stellar Containment Chamber', accent=(96, 176, 255), glow=(214, 236, 255),
                    base=(10, 14, 28), panel=(36, 44, 66), hi=(78, 92, 124), lo=(12, 14, 24), line=(58, 84, 140),
                    dim=(132, 152, 196)),
    'collider': dict(name='Antimatter Collider Ring', accent=(64, 236, 214), glow=(204, 255, 248),
                     base=(8, 20, 24), panel=(30, 48, 54), hi=(70, 104, 110), lo=(10, 16, 18), line=(44, 120, 116),
                     dim=(120, 170, 170)),
    'rift': dict(name='Dimensional Rift Gate', accent=(196, 112, 255), glow=(236, 214, 255), base=(18, 10, 28),
                 panel=(44, 32, 62), hi=(88, 70, 118), lo=(14, 10, 22), line=(100, 64, 150), dim=(160, 136, 192)),
}
GREEN, YELLOW, RED, VIOLET = (85, 255, 85), (255, 255, 85), (255, 85, 85), (200, 140, 255)


class Px:
    def __init__(self, w, h, bg=(0, 0, 0, 0)):
        self.im = Image.new('RGBA', (w, h), bg)
        self.d = ImageDraw.Draw(self.im)
        self.w, self.h = w, h

    def rect(self, x, y, w, h, c):
        if w > 0 and h > 0: self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=c)

    def hline(self, x, y, w, c):
        self.rect(x, y, w, 1, c)

    def vline(self, x, y, h, c):
        self.rect(x, y, 1, h, c)

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.im.putpixel((int(x), int(y)), c)

    def text(self, x, y, s, c, shadow=True, align='l'):
        w = FONT.width(s)
        if align == 'r': x -= w
        elif align == 'c': x -= w // 2
        FONT.draw(self.im, int(x), int(y), s, c, shadow)
        return w


def bevel(p, x, y, w, h, t, raised=True, cut=2):
    """Chamfered plate with a 1 px light/dark bevel, the corners cut by `cut` pixels."""
    hi, lo = (t['hi'], t['lo']) if raised else (t['lo'], t['hi'])
    p.rect(x + cut, y, w - 2 * cut, h, t['panel'])
    p.rect(x, y + cut, w, h - 2 * cut, t['panel'])
    for k in range(cut):
        p.rect(x + cut - k, y + k, w - 2 * (cut - k), 1, t['panel'])
        p.rect(x + cut - k, y + h - 1 - k, w - 2 * (cut - k), 1, t['panel'])
    p.hline(x + cut, y, w - 2 * cut, hi); p.vline(x, y + cut, h - 2 * cut, hi)
    p.hline(x + cut, y + h - 1, w - 2 * cut, lo); p.vline(x + w - 1, y + cut, h - 2 * cut, lo)
    for k in range(1, cut + 1):
        p.px(x + cut - k, y + k, hi); p.px(x + w - 1 - cut + k, y + k, hi)
        p.px(x + cut - k, y + h - 1 - k, lo); p.px(x + w - 1 - cut + k, y + h - 1 - k, lo)


def glass(p, x, y, w, h, t, seed):
    """The status display: dark glass, every other row a shade darker, single-pixel stars, accent corner ticks."""
    p.rect(x, y, w, h, t['lo'])
    p.rect(x + 1, y + 1, w - 2, h - 2, t['base'])
    for yy in range(y + 2, y + h - 1, 2):
        p.hline(x + 1, yy, w - 2, tuple(max(0, v - 4) for v in t['base']))
    rng = np.random.default_rng(seed)
    for _ in range(w * h // 120):
        sx, sy = x + 2 + int(rng.random() * (w - 4)), y + 2 + int(rng.random() * (h - 4))
        v = int(80 + 140 * rng.random() ** 2)
        p.px(sx, sy, (v, v, min(255, v + 20), 255))
    for cx, cy, dx, dy in ((x + 2, y + 2, 1, 1), (x + w - 3, y + 2, -1, 1), (x + 2, y + h - 3, 1, -1),
                           (x + w - 3, y + h - 3, -1, -1)):
        for k in range(4):
            p.px(cx + k * dx, cy, t['accent']); p.px(cx, cy + k * dy, t['accent'])


def dither_disc(p, cx, cy, r, colour, strength=1.0):
    """A soft glow as an ordered-dither falloff: pixel-art light without blur."""
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            d = math.hypot(xx - cx, yy - cy) / r
            if d >= 1: continue
            if (1 - d) ** 1.6 * strength > BAYER[yy % 4][xx % 4]:
                p.px(xx, yy, colour)


def disc(p, cx, cy, r, colour):
    for yy in range(int(cy - r), int(cy + r) + 1):
        for xx in range(int(cx - r), int(cx + r) + 1):
            if math.hypot(xx - cx + 0.5, yy - cy + 0.5) <= r: p.px(xx, yy, colour)


def circle(p, cx, cy, r, colour, step=1):
    n = int(2 * math.pi * r * 1.5)
    for k in range(0, n, step):
        a = 2 * math.pi * k / n
        p.px(round(cx + r * math.cos(a)), round(cy + r * math.sin(a)), colour)


def ellipse_pts(p, cx, cy, rx, ry, colour, dotted=0):
    n = int(2 * math.pi * max(rx, ry) * 1.5)
    for k in range(n):
        if dotted and (k // dotted) % 2: continue
        a = 2 * math.pi * k / n
        p.px(round(cx + rx * math.cos(a)), round(cy + ry * math.sin(a)), colour)


def line(p, x0, y0, x1, y1, c):
    p.d.line([x0, y0, x1, y1], fill=c, width=1)


def bar(p, t, x, y, w, label, value, frac, colour=None):
    colour = colour or t['accent']
    p.text(x, y, label, t['dim'], shadow=False)
    p.text(x + w, y, value, t['glow'], shadow=False, align='r')
    p.rect(x, y + 9, w, 4, t['lo'])
    p.rect(x + 1, y + 10, w - 2, 2, (10, 10, 12, 255))
    f = int((w - 2) * max(0.0, min(1.0, frac)))
    if f:
        p.rect(x + 1, y + 10, f, 2, colour)
        p.hline(x + 1, y + 10, f, tuple(min(255, v + 60) for v in colour[:3]))


def chip(p, t, x, y, w, s, colour):
    p.rect(x, y, w, 13, t['lo'])
    p.rect(x + 1, y + 1, w - 2, 11, (0, 0, 0, 255))
    p.vline(x + 1, y + 1, 11, colour + (255,) if len(colour) == 3 else colour)
    p.text(x + w // 2 + 1, y + 3, s, colour, shadow=False, align='c')


def button(p, t, x, y, w, h, ico, label=None, active=False):
    bevel(p, x, y, w, h, t, raised=not active)
    col = t['accent'] if active else t['dim']
    if label:
        icon(p.im, x + 4, y + (h - 9) // 2, ico, col)
        p.text(x + 16, y + (h - 8) // 2 + 1, label, t['glow'] if active else t['dim'])
    else:
        icon(p.im, x + (w - 9) // 2, y + (h - 9) // 2, ico, col)
    if active: p.hline(x + 3, y + h - 3, w - 6, t['accent'])


def slot(p, x, y):
    p.rect(x, y, 18, 18, (139, 139, 139, 255))
    p.hline(x, y, 17, (55, 55, 55, 255)); p.vline(x, y, 17, (55, 55, 55, 255))
    p.hline(x + 1, y + 17, 17, (255, 255, 255, 255)); p.vline(x + 17, y + 1, 17, (255, 255, 255, 255))


def inventory(p, x, y):
    for r in range(3):
        for k in range(9): slot(p, x + k * 18, y + r * 18)
    for k in range(9): slot(p, x + k * 18, y + 58)


# ----------------------------------------------------------------------------------------------- window
W, H = 300, 226


def window(t):
    """Main window: a title tab, the window plate, the display, a chip row, the inventory and 2 x 4 buttons."""
    p = Px(W, H + 14)
    bevel(p, 0, 0, FONT.width(t['name']) + 16, 16, t, cut=2)
    p.text(8, 4, t['name'], t['glow'])
    bevel(p, 0, 13, W, H + 1, t, cut=3)
    return p, 0, 14


def right_buttons(p, t, ox, oy, items):
    for i, it in enumerate(items):
        col, row = i % 2, i // 2
        button(p, t, ox + 172 + col * 62, oy + 120 + row * 21, 60, 19, *it)


def lance_main():
    t = THEMES['lance']
    p, ox, oy = window(t)
    glass(p, ox + 4, oy + 4, 292, 108, t, 3)
    # Orbit sketch: Earth, Moon on its orbit, the shot arc.
    cx, cy = ox + 52, oy + 56
    ellipse_pts(p, cx, cy, 34, 34, t['line'] + (255,), dotted=2)
    ellipse_pts(p, cx, cy, 24, 24, t['line'] + (255,), dotted=2)
    dither_disc(p, cx, cy, 14, (40, 90, 170, 255), 0.6)
    disc(p, cx, cy, 8, (60, 120, 210, 255))
    for k in range(3): p.px(cx - 3 + k, cy - 4, (110, 190, 110, 255))
    mx, my = cx + 24, cy - 24
    disc(p, mx, my, 5, (190, 190, 196, 255))
    p.px(mx - 1, my - 1, (150, 150, 156, 255)); p.px(mx + 2, my + 1, (150, 150, 156, 255))
    circle(p, mx, my, 9, t['accent'] + (255,), 2)
    for k in range(20):
        a = k / 19
        p.px(round(cx + 8 + (mx - cx - 8) * a), round(cy - 6 - (cy - 6 - my) * a - 10 * math.sin(math.pi * a)),
             t['accent'] + (255,))
    p.text(cx, oy + 98, 'Moon 384 Mm', t['accent'], align='c')
    x0 = ox + 104
    p.text(x0, oy + 8, 'Target: Moon', t['glow'])
    p.text(ox + 290, oy + 8, 'survey 100%', GREEN, align='r')
    bar(p, t, x0, oy + 20, 186, 'Bank', '4.00e12 EU', 1.0)
    bar(p, t, x0, oy + 37, 186, 'Barrel', '300 K', 0.0, (255, 100, 60))
    bar(p, t, x0, oy + 54, 186, 'Liner', '12% worn', 0.12, (255, 210, 70))
    bar(p, t, x0, oy + 71, 186, 'Aim', '16000 CWU/t', 1.0, (110, 210, 255))
    p.text(x0, oy + 90, 'Neutronium slug, 2 capsules', t['dim'], shadow=False)
    p.text(x0, oy + 100, 'Regime: relativistic', t['dim'], shadow=False)
    chip(p, t, ox + 4, oy + 116, 52, 'FORMED', GREEN)
    chip(p, t, ox + 60, oy + 116, 52, 'AUTO', t['accent'])
    chip(p, t, ox + 116, oy + 116, 50, 'NEXUS', VIOLET)
    inventory(p, ox + 4, oy + 134)
    right_buttons(p, t, ox, oy, [('left', 'Prev'), ('right', 'Next'), ('auto', 'Auto', True), ('orbit', 'Orbit'),
                                 ('gear', 'Bench'), ('capsule', 'Pods'), ('info', 'Info'), ('power', 'Power', True)])
    return p


def stellar_main():
    t = THEMES['stellar']
    p, ox, oy = window(t)
    glass(p, ox + 4, oy + 4, 292, 108, t, 5)
    cx, cy = ox + 52, oy + 54
    for k in range(-40, 41):
        p.px(cx + k * 0.6, cy - k, (180, 210, 255, 255) if abs(k) > 8 else (0, 0, 0, 0))
    dither_disc(p, cx, cy, 22, (60, 120, 230, 255), 0.7)
    dither_disc(p, cx, cy, 14, (150, 200, 255, 255), 0.9)
    disc(p, cx, cy, 7, (236, 246, 255, 255))
    ellipse_pts(p, cx, cy, 28, 6, (255, 150, 60, 255))
    x0 = ox + 104
    p.text(x0, oy + 8, 'Millisecond pulsar', t['glow'])
    p.text(ox + 290, oy + 8, 'lit', GREEN, align='r')
    p.text(x0, oy + 18, 'M 1.421  P 1.61ms  Pk 0.61ms', t['dim'], shadow=False)
    bar(p, t, x0, oy + 29, 186, 'Extraction', '2^58 EU/t', 0.7)
    bar(p, t, x0, oy + 46, 186, 'Crust stress', '0.42', 0.42, (255, 200, 90))
    bar(p, t, x0, oy + 63, 186, 'Damage', '0.0%', 0.0, RED)
    bar(p, t, x0, oy + 80, 186, 'Band tier', '3 / 4', 0.75, (170, 130, 255))
    p.text(x0, oy + 99, 'Output 2.88e17 EU/t', t['dim'], shadow=False)
    chip(p, t, ox + 4, oy + 116, 52, 'STAR', (255, 236, 160))
    chip(p, t, ox + 60, oy + 116, 52, 'PROBE', GREEN)
    chip(p, t, ox + 116, oy + 116, 50, 'NEXUS', VIOLET)
    inventory(p, ox + 4, oy + 134)
    right_buttons(p, t, ox, oy, [('minus', 'Less'), ('plus', 'More'), ('bolt', 'Field'), ('chart', 'M-P'),
                                 ('wave', 'Quake'), ('star', 'Star'), ('info', 'Info'), ('power', 'Power', True)])
    return p


def collider_main():
    t = THEMES['collider']
    p, ox, oy = window(t)
    glass(p, ox + 4, oy + 4, 292, 108, t, 7)
    cx, cy = ox + 52, oy + 56
    circle(p, cx, cy, 34, t['accent'] + (255,))
    circle(p, cx, cy, 33, tuple(v // 2 for v in t['accent']) + (255,))
    for k in range(16):
        a = k * math.pi / 8
        p.rect(round(cx + 34 * math.cos(a)) - 1, round(cy + 34 * math.sin(a)) - 1, 3, 3, (230, 255, 250, 255))
    dither_disc(p, cx, cy, 9, (255, 80, 220, 255), 0.9)
    disc(p, cx, cy, 3, (255, 220, 250, 255))
    x0 = ox + 104
    p.text(x0, oy + 8, 'Physics run', t['glow'])
    p.text(ox + 290, oy + 8, '21.6 TeV', t['accent'], align='r')
    p.text(x0, oy + 18, 'Nb3Sn 12 T  L 1.45e34', t['dim'], shadow=False)
    bar(p, t, x0, oy + 29, 186, 'Ramp', '100%', 1.0)
    bar(p, t, x0, oy + 46, 186, 'Helium', '1.0 L/s', 1.0, (150, 220, 255))
    bar(p, t, x0, oy + 63, 186, 'Traps', '8.4e11', 0.84, (255, 80, 220))
    bar(p, t, x0, oy + 80, 186, 'Charm', '3.4 / 5', 0.68, YELLOW)
    p.text(x0, oy + 99, 'Proposal: vertex detector', t['dim'], shadow=False)
    chip(p, t, ox + 4, oy + 116, 52, 'BEAM', GREEN)
    chip(p, t, ox + 60, oy + 116, 52, 'DUMP', GREEN)
    chip(p, t, ox + 116, oy + 116, 50, 'NEXUS', VIOLET)
    inventory(p, ox + 4, oy + 134)
    right_buttons(p, t, ox, oy, [('swap', 'Mode', True), ('atom', 'Model'), ('list', 'Board'), ('ring', 'Traps'),
                                 ('snow', 'Cryo'), ('orbit', 'Ring'), ('info', 'Info'), ('power', 'Power', True)])
    return p


def rift_main():
    t = THEMES['rift']
    p, ox, oy = window(t)
    glass(p, ox + 4, oy + 4, 292, 108, t, 9)
    cx, cy = ox + 52, oy + 54
    cols = [(150, 60, 220), (170, 90, 240), (120, 140, 255), (90, 190, 255), (220, 200, 255)]
    for k in range(5):
        circle(p, cx, cy, 34 - k * 6, cols[k] + (255,), 1 if k % 2 == 0 else 2)
    disc(p, cx, cy, 6, (6, 0, 14, 255))
    circle(p, cx, cy, 6, (255, 255, 255, 255))
    x0 = ox + 104
    p.text(x0, oy + 8, 'Rift open', t['glow'])
    p.text(ox + 290, oy + 8, 'Forge world', t['accent'], align='r')
    bar(p, t, x0, oy + 20, 186, 'Resonance', '0.86', 0.86)
    bar(p, t, x0, oy + 37, 186, 'Stability', '72 / 100', 0.72, (110, 230, 150))
    for i, (lab, val, close) in enumerate((('Freq', '612.0', 0.9), ('Phase', '144', 0.7), ('Ampl', '55', 0.95))):
        y = oy + 56 + i * 15
        p.text(x0, y + 2, lab, t['dim'], shadow=False)
        p.text(x0 + 34, y + 2, val, t['glow'], shadow=False)
        for k in range(5):
            on = k < round(close * 5)
            c = (GREEN if close > 0.8 else YELLOW) if on else (60, 48, 76)
            p.rect(x0 + 74 + k * 7, y + 3, 5, 6, c + (255,) if len(c) == 3 else c)
        button(p, t, x0 + 128, y, 14, 13, 'minus')
        button(p, t, x0 + 146, y, 14, 13, 'plus')
        button(p, t, x0 + 164, y, 22, 13, 'right')
    p.text(x0, oy + 101, 'SpaceTime 31 L/s, depth 6', t['dim'], shadow=False)
    chip(p, t, ox + 4, oy + 116, 52, 'OPEN', GREEN)
    chip(p, t, ox + 60, oy + 116, 52, 'TUNING', t['accent'])
    chip(p, t, ox + 116, oy + 116, 50, 'NEXUS', VIOLET)
    inventory(p, ox + 4, oy + 134)
    right_buttons(p, t, ox, oy, [('open', 'Open', True), ('close', 'Close'), ('note', 'Chord'), ('map', 'Atlas'),
                                 ('wave', 'Seismo'), ('down', 'Depth'), ('info', 'Info'), ('power', 'Power', True)])
    return p


# ----------------------------------------------------------------------------------------------- panels
def panel(t, title, w=292, h=150):
    p = Px(w, h)
    bevel(p, 0, 0, w, h, t, cut=3)
    glass(p, 4, 15, w - 8, h - 19, t, len(title))
    p.text(6, 4, title, t['accent'])
    button(p, t, w - 15, 2, 12, 11, 'close')
    return p


def lance_orbit():
    t = THEMES['lance']
    p = panel(t, 'Orbital Map')
    cx, cy = 98, 82
    dither_disc(p, cx, cy, 12, (255, 200, 80, 255), 0.8)
    disc(p, cx, cy, 5, (255, 240, 170, 255))
    bodies = [('Moon', 14, 0.5, (196, 196, 202), True), ('Phobos', 24, 2.4, (150, 120, 100), True),
              ('Vesta', 34, 3.7, (186, 170, 146), True), ('Ceres', 44, 5.3, (150, 150, 160), True),
              ('Psyche', 52, 1.2, (210, 204, 186), False), ('Europa', 58, 4.4, (226, 232, 244), False),
              ('Arrokoth', 64, 2.9, (226, 136, 106), False)]
    for name, r, a, col, ok in bodies:
        ellipse_pts(p, cx, cy, r * 1.35, r * 0.85, t['line'] + (255,), dotted=1)
    for name, r, a, col, ok in bodies:
        bx, by = round(cx + r * 1.35 * math.cos(a)), round(cy + r * 0.85 * math.sin(a))
        c = col if ok else tuple(v // 3 for v in col)
        p.rect(bx - 2, by - 2, 5, 5, c + (255,))
        p.rect(bx - 1, by - 1, 3, 1, tuple(min(255, v + 40) for v in c) + (255,))
        if name == 'Vesta':
            for k in range(-4, 5): p.px(bx + k, by - 5, t['accent'] + (255,)); p.px(bx + k, by + 5, t['accent'] + (255,))
            for k in range(-4, 5): p.px(bx - 5, by + k, t['accent'] + (255,)); p.px(bx + 5, by + k, t['accent'] + (255,))
        p.text(bx + 6, by - 4, name, t['glow'] if ok else t['dim'], shadow=ok)
    bevel(p, 196, 18, 92, 128, t, raised=False)
    p.text(201, 23, 'Vesta', t['accent'])
    rows = [('Survey', '64%'), ('Dist', '1.7e5 Mm'), ('Hard', '3.5'), ('Back', '5h15'), ('Gives', 'Fe Mg Cr')]
    for i, (k, v) in enumerate(rows):
        p.text(201, 37 + i * 11, k, t['dim'], shadow=False)
        p.text(285, 37 + i * 11, v, t['glow'], shadow=False, align='r')
    button(p, t, 200, 126, 84, 16, 'orbit', 'Target', True)
    return p


def lance_bench():
    t = THEMES['lance']
    p = panel(t, 'Barrel Bench')
    p.rect(12, 34, 268, 10, (70, 60, 60, 255))
    p.hline(12, 34, 268, (110, 100, 100, 255))
    for k in range(8):
        c = (255, 180, 60, 255) if k < 4 else (54, 46, 50, 255)
        p.rect(18 + k * 33, 24, 24, 7, c); p.rect(18 + k * 33, 47, 24, 7, c)
        if k < 4: p.hline(18 + k * 33, 24, 24, (255, 230, 150, 255)); p.hline(18 + k * 33, 47, 24, (255, 230, 150, 255))
    p.text(146, 58, '4/8 rails  eff 41%', t['dim'], shadow=False, align='c')
    slots = [('gear', 'Rail', True), ('snow', 'Cool', False), ('orbit', 'Aim', True), ('capsule', 'Pod', False),
             ('swap', 'Salvo', False)]
    for i, (ico, s, on) in enumerate(slots):
        button(p, t, 10 + i * 55, 72, 52, 19, ico, s, on)
    bar(p, t, 12, 98, 128, 'Mass', '170/800t', 170 / 800)
    bar(p, t, 152, 98, 128, 'Heat', '14/60', 14 / 60, (255, 100, 60))
    p.text(146, 124, 'Bench valid', GREEN, align='c')
    return p


def stellar_mp():
    t = THEMES['stellar']
    p = panel(t, 'Mass-Period Diagram')
    x0, y0, w, h = 30, 20, 250, 110
    p.rect(x0, y0, w, h, (6, 8, 16, 255))
    tov = y0 + int(h * (1 - 1.2 / 1.6))
    for yy in range(y0, tov):
        for xx in range(x0, x0 + w):
            if (xx + yy) % 3 == 0: p.px(xx, yy, (90, 20, 30, 255))
    p.hline(x0, tov, w, RED + (255,))
    p.text(x0 + w - 2, tov - 9, 'TOV', RED, align='r')
    for k in range(40):
        p.px(x0 + 4 + int(k ** 1.5 / 1.6), y0 + h - 2 - int(k * 2.6), YELLOW + (255,))
    pts = [(x0 + 210, y0 + 96), (x0 + 170, y0 + 90), (x0 + 130, y0 + 78), (x0 + 100, y0 + 70)]
    for a, b in zip(pts, pts[1:]): line(p, *a, *b, t['accent'] + (255,))
    disc(p, pts[-1][0], pts[-1][1], 2, t['glow'] + (255,))
    for i, v in enumerate(('1.0', '1.4', '1.8', '2.2', '2.6')):
        p.text(x0 - 3, y0 + h - 4 - i * 27, v, t['dim'], shadow=False, align='r')
    p.text(x0 + w // 2, y0 + h + 3, 'spin period (ms)', t['dim'], shadow=False, align='c')
    return p


def stellar_seismo():
    t = THEMES['stellar']
    p = panel(t, 'Seismogram')
    p.rect(10, 20, 272, 54, (4, 10, 8, 255))
    rng = np.random.default_rng(2)
    prev = None
    for x in range(12, 280):
        a = 1.5 + (12 * math.exp(-((x - 110) / 6) ** 2) + 20 * math.exp(-((x - 210) / 5) ** 2)) * math.sin(x * 1.7)
        y = int(47 + a + rng.normal() * 0.6)
        if prev: line(p, x - 1, prev, x, y, GREEN + (255,))
        prev = y
    p.text(110, 22, 'Crab', t['accent'], align='c')
    p.text(210, 22, 'Vela', t['accent'], align='c')
    rows = [('Micro', 'bands 2', True), ('Crab', 'decoded', True), ('Vela', 'bands 3', True),
            ('Anti', 'magnetar', False), ('Collapse', 'TOV edge', False)]
    for i, (q, s, ok) in enumerate(rows):
        p.text(12, 80 + i * 13, q, t['glow'])
        p.text(110, 80 + i * 13, s, GREEN if ok else t['dim'], shadow=ok)
    return p


def collider_model():
    t = THEMES['collider']
    p = panel(t, 'Standard Model')
    parts = [('p', 5.0), ('K', 5.0), ('L', 5.0), ('c', 3.4), ('b', 1.2), ('W', 0.4), ('Z', 0.3), ('H', 0), ('t', 0),
             ('X', 0)]
    names = ['Antiproton', 'Kaon', 'Lambda', 'Charm', 'Bottom', 'W boson', 'Z boson', 'Higgs', 'Top', 'X-Nexus']
    for i, ((sym, z), name) in enumerate(zip(parts, names)):
        x, y = 8 + (i % 5) * 56, 18 + (i // 5) * 64
        col = GREEN if z >= 5 else YELLOW if z >= 3 else t['dim']
        bevel(p, x, y, 52, 60, t, raised=False)
        big = Px(12, 10)
        big.text(1, 1, sym, col)
        p.im.alpha_composite(big.im.resize((24, 20), Image.NEAREST), (x + 14, y + 4))
        p.text(x + 26, y + 28, name[:8], t['glow'], shadow=False, align='c')
        p.text(x + 26, y + 39, f'{z:.1f}s', col, shadow=False, align='c')
        p.rect(x + 6, y + 51, 40, 3, (20, 20, 20, 255))
        p.rect(x + 6, y + 51, int(40 * min(1, z / 5)), 3, col + (255,) if len(col) == 3 else col)
    return p


def collider_board():
    t = THEMES['collider']
    p = panel(t, 'Beam-Time Committee')
    rows = [('Nb3Sn magnet', '7 TeV', 1, 'done'), ('Vertex detector', 'charm 5s', 0.68, 'active'),
            ('Stoch. cooling', '20 fb', 0, ''), ('Cryo Penning', '1e13 p', 0, ''), ('REBCO magnet', 'W+Z 5s', 0, ''),
            ('Lepton collider', 'b 5s', 0, ''), ('Heavy ions', 'top 5s', 0, ''), ('Neutronium mag.', 'H 5s', 0, ''),
            ('Beyond the SM', 'X 3s', 0, '')]
    for i, (n, req, f, st) in enumerate(rows):
        y = 18 + i * 14
        col = GREEN if st == 'done' else t['accent'] if st == 'active' else t['dim']
        p.rect(8, y, 276, 12, (0, 0, 0, 255) if i % 2 else (12, 22, 24, 255))
        p.text(12, y + 2, n, col, shadow=st != '')
        p.text(130, y + 2, req, t['dim'], shadow=False)
        p.rect(196, y + 4, 50, 4, (30, 30, 30, 255))
        p.rect(196, y + 4, int(50 * f), 4, col + (255,) if len(col) == 3 else col)
        p.text(282, y + 2, st, col, shadow=False, align='r')
    return p


def rift_chord():
    t = THEMES['rift']
    p = panel(t, 'Harmonic Chord')
    cx, cy, r = 74, 82, 50
    names = ['2:1', '3:2', '4:3', '5:4', '8:5', '9:5', '45:32', '16:15']
    pts = []
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * math.pi / 4
        x, y = round(cx + r * math.cos(a)), round(cy + r * math.sin(a))
        pts.append((x, y))
    for a, b in ((0, 1), (1, 4), (4, 0)): line(p, *pts[a], *pts[b], (110, 210, 255, 255))
    for i, (x, y) in enumerate(pts):
        rec, load = i in (0, 1, 2, 4), i in (0, 1, 4)
        disc(p, x, y, 4, (255, 255, 255, 255) if load else t['panel'] if rec else (40, 30, 54, 255))
        circle(p, x, y, 4, t['accent'] + (255,))
        p.text(x + (7 if x >= cx else -7), y - 4, names[i], t['glow'] if rec else t['dim'],
               shadow=rec, align='l' if x >= cx else 'r')
    bevel(p, 150, 18, 138, 128, t, raised=False)
    for i, (k, v) in enumerate((('Loaded', '2:1 3:2 8:5'), ('Consonance', '0.42'), ('Loss', '1.32/s'),
                                ('Max depth', '12'), ('Recorded', '4 of 8'))):
        p.text(155, 24 + i * 12, k, t['dim'], shadow=False)
        p.text(284, 24 + i * 12, v, t['glow'], shadow=False, align='r')
    p.text(219, 96, 'Click a harmonic', t['dim'], shadow=False, align='c')
    p.text(219, 106, 'to load it (max 5)', t['dim'], shadow=False, align='c')
    return p


def rift_atlas():
    t = THEMES['rift']
    p = panel(t, 'Seed Atlas')
    rng = np.random.default_rng(12)
    pts = [(int(14 + rng.random() * 160), int(22 + rng.random() * 118)) for _ in range(14)]
    for i in range(len(pts) - 1):
        if rng.random() < 0.55: line(p, *pts[i], *pts[i + 1], t['line'] + (255,))
    for i, (x, y) in enumerate(pts):
        col = [GREEN, YELLOW, VIOLET][i % 3]
        p.rect(x - 1, y - 1, 3, 3, col + (255,))
    circle(p, pts[3][0], pts[3][1], 5, (255, 255, 255, 255))
    bevel(p, 190, 18, 98, 128, t, raised=False)
    p.text(195, 23, '1B44C9F0', t['accent'])
    for i, (k, v) in enumerate((('Biome', 'Forge'), ('Best R', '0.847'), ('Depth', '6'), ('Note', '4:3'),
                                ('Gives', 'W Os Ir'))):
        p.text(195, 37 + i * 11, k, t['dim'], shadow=False)
        p.text(284, 37 + i * 11, v, t['glow'], shadow=False, align='r')
    button(p, t, 194, 126, 90, 16, 'open', 'Reopen', True)
    return p


def info_panel():
    """Field manual: steel slate, hazard stripe, chapter tabs on the left, page on the right."""
    t = dict(THEMES['lance'])
    t.update(panel=(40, 42, 46), hi=(96, 100, 106), lo=(14, 14, 16), base=(22, 24, 28), accent=(240, 186, 40),
             glow=(232, 232, 236), dim=(150, 154, 160))
    w, h = 292, 200
    p = Px(w, h)
    bevel(p, 0, 0, w, h, t, cut=3)
    for x in (4, w - 6):
        for y in (4, h - 6):
            p.rect(x, y, 2, 2, (130, 134, 140, 255)); p.px(x, y, (190, 194, 200, 255))
    for k in range(0, w - 16, 6):
        for j in range(4):
            p.px(8 + k + j, 10 + j, t['accent'] + (255,)); p.px(9 + k + j, 10 + j, t['accent'] + (255,))
            p.px(10 + k + j, 10 + j, t['accent'] + (255,))
    p.text(8, 18, 'FIELD MANUAL - ORBITAL LANCE', t['glow'])
    chapters = ['Overview', 'Structure', 'Bank', 'Targets', 'Bench', 'Yields']
    for i, ch in enumerate(chapters):
        on = i == 2
        y = 32 + i * 18
        if on:
            p.rect(6, y, 66, 15, t['accent'] + (255,))
            p.text(10, y + 4, f'{i + 1} {ch}', (24, 20, 10), shadow=False)
        else:
            bevel(p, 6, y, 66, 15, t)
            p.text(10, y + 4, f'{i + 1} {ch}', t['dim'])
    bevel(p, 76, 30, 210, 164, t, raised=False)
    p.text(82, 35, 'Bank & firing', t['accent'])
    for i, l in enumerate(['The bank charges from the', 'Nexus network. With Auto on,',
                           'a full bank fires one slug', 'from the input bus.']):
        p.text(82, 49 + i * 10, l, t['glow'], shadow=False)
    p.rect(82, 92, 198, 24, (10, 26, 14, 255))
    p.hline(82, 92, 198, GREEN + (255,)); p.hline(82, 115, 198, GREEN + (255,))
    p.text(87, 96, 'v = sqrt(2 eff E / m)', GREEN, shadow=False)
    p.text(87, 106, 'bank = 4e12 x 2^(rings-1)', GREEN, shadow=False)
    for i, l in enumerate(['Slugs: naquadah alloy, trinium,', 'neutronium, cosmic neutronium,',
                           'white dwarf matter.']):
        p.text(82, 122 + i * 10, l, t['glow'], shadow=False)
    p.text(82, 180, '< prev', t['dim'], shadow=False)
    p.text(280, 180, 'next >', t['accent'], align='r')
    return p


def big(p):
    return p.im.resize((p.im.width * SCALE, p.im.height * SCALE), Image.NEAREST)


def sheet(name, main, panels):
    pad = 12
    mw, mh = main.im.size
    pw = max(x.im.size[0] for x in panels)
    W2 = mw + pw + pad * 3
    H2 = max(mh, sum(x.im.size[1] for x in panels) + pad * (len(panels) - 1)) + pad * 2
    out = Px(W2, H2, (38, 38, 42, 255))
    out.im.alpha_composite(main.im, (pad, pad))
    y = pad
    for x in panels:
        out.im.alpha_composite(x.im, (mw + pad * 2, y))
        y += x.im.size[1] + pad
    big(out).save(os.path.join(OUT, f'{name}.png'))
    print(name)


def main():
    global FONT
    FONT = MCFont(sys.argv[1])
    sheet('lance', lance_main(), [lance_orbit(), lance_bench()])
    sheet('stellar', stellar_main(), [stellar_mp(), stellar_seismo()])
    sheet('collider', collider_main(), [collider_model(), collider_board()])
    sheet('rift', rift_main(), [rift_chord(), rift_atlas()])
    big(info_panel()).save(os.path.join(OUT, 'info_panel.png'))
    m = lance_main()
    m.im.alpha_composite(lance_orbit().im, (4, 18))
    big(m).save(os.path.join(OUT, 'lance_panel_open.png'))


if __name__ == '__main__' and len(sys.argv) == 2:
    main()


# ----------------------------------------------------------------------------------------------- mod textures
def export_textures(root):
    """Static backgrounds for the in-game screens (assets/gtna/textures/gui/originals_v2/<theme>/): the window plate
    with its display glass, a panel plate, plate buttons; the manual slate. Text, icons, bars and drawings are drawn
    by the game over them."""
    for key, t in THEMES.items():
        d = os.path.join(root, key)
        os.makedirs(d, exist_ok=True)
        # Window: 300 x 240, title tab on top (name drawn by the game), display glass at (4, 18) 292 x 108.
        p = Px(W, H + 14)
        bevel(p, 0, 0, 170, 16, t, cut=2)
        bevel(p, 0, 13, W, H + 1, t, cut=3)
        glass(p, 4, 18, 292, 108, t, len(key))
        p.im.save(os.path.join(d, 'window.png'))
        # Panel: 292 x 150 over the display, title drawn by the game.
        q = Px(292, 150)
        bevel(q, 0, 0, 292, 150, t, cut=3)
        glass(q, 4, 15, 284, 131, t, len(key) * 7)
        q.im.save(os.path.join(d, 'panel.png'))
        r = Px(380, 170)
        bevel(r, 0, 0, 380, 170, t, cut=3)
        glass(r, 4, 15, 372, 151, t, len(key) * 11)
        r.im.save(os.path.join(d, 'panel_wide.png'))
        k = Px(130, 148)
        bevel(k, 0, 0, 130, 148, t, raised=False)
        k.im.save(os.path.join(d, 'card_wide.png'))
        for name, raised, w, h in (('plate', True, 60, 19), ('plate_on', False, 60, 19), ('small', True, 14, 13),
                                   ('small_on', False, 14, 13), ('wide', True, 22, 13), ('card', False, 92, 128)):
            b = Px(w, h)
            bevel(b, 0, 0, w, h, t, raised=raised)
            if not raised and name != 'card': b.hline(3, h - 3, w - 6, t['accent'])
            b.im.save(os.path.join(d, name + '.png'))
        # Inventory slot in the theme's tones: a mid plate light enough for items, sunk into the window.
        mid = tuple((a + b) // 2 for a, b in zip(t['hi'], t['dim']))
        sl = Px(18, 18)
        sl.rect(0, 0, 18, 18, mid + (255,))
        sl.hline(0, 0, 17, t['lo'] + (255,)); sl.vline(0, 0, 17, t['lo'] + (255,))
        light = tuple(min(255, c + 50) for c in t['dim'])
        sl.hline(1, 17, 17, light + (255,)); sl.vline(17, 1, 17, light + (255,))
        sl.im.save(os.path.join(d, 'slot.png'))
        # The field manual slate in the theme's colours.
        m = Px(292, 200)
        bevel(m, 0, 0, 292, 200, t, cut=3)
        for x in (4, 286):
            for y in (4, 194):
                m.rect(x, y, 2, 2, t['hi'] + (255,)); m.px(x, y, light + (255,))
        for k in range(0, 276, 6):
            for j in range(4):
                for o in range(3): m.px(8 + k + j + o, 10 + j, t['accent'] + (255,))
        bevel(m, 76, 30, 210, 164, t, raised=False)
        m.im.save(os.path.join(d, 'slate.png'))
        for name, on in (('tab', False), ('tab_on', True)):
            b = Px(66, 15)
            if on: b.rect(0, 0, 66, 15, t['accent'] + (255,))
            else: bevel(b, 0, 0, 66, 15, t)
            b.im.save(os.path.join(d, name + '.png'))

if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[2] == '--textures':
    FONT = MCFont(sys.argv[1])
    export_textures(sys.argv[3])
