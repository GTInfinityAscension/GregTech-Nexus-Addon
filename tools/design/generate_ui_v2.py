#!/usr/bin/env python3
"""UI v2 mockups for the four original multiblocks: a wide main window in the spirit of the Forge of Gods screen
(status display on top, player inventory bottom-left, a grid of chamfered buttons to its right) whose tabs open as
panels over the display instead of new screens, plus a new information panel.

Drawn in GUI pixels and scaled 3x, like the game at GUI scale 3. Values shown are what the machines compute.

    python3 tools/design/generate_ui_v2.py      ->  tools/design/ui_v2/
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 3
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_v2')
os.makedirs(OUT, exist_ok=True)


def font(px, bold=False):
    for p in ([f'/usr/share/fonts/TTF/DejaVuSans{"-Bold" if bold else ""}.ttf'] +
              ['/usr/share/fonts/TTF/DejaVuSans.ttf']):
        if os.path.exists(p): return ImageFont.truetype(p, px * S)
    return ImageFont.load_default()


F8, F7, F6, F9B = font(8), font(7), font(6), font(9, True)
F7B = font(7, True)

THEMES = {
    'lance': dict(name='Kinetic Orbital Lance', accent=(255, 176, 64), glow=(255, 214, 140), base=(24, 20, 28),
                  panel=(34, 28, 38), line=(92, 72, 56), dim=(150, 130, 110)),
    'stellar': dict(name='Stellar Containment Chamber', accent=(120, 190, 255), glow=(210, 235, 255),
                    base=(14, 18, 32), panel=(22, 28, 48), line=(60, 80, 130), dim=(120, 140, 180)),
    'collider': dict(name='Antimatter Collider Ring', accent=(80, 240, 220), glow=(200, 255, 245),
                     base=(12, 22, 26), panel=(18, 32, 38), line=(50, 110, 110), dim=(110, 160, 160)),
    'rift': dict(name='Dimensional Rift Gate', accent=(196, 120, 255), glow=(235, 210, 255),
                 base=(20, 14, 30), panel=(30, 22, 44), line=(90, 60, 130), dim=(150, 125, 180)),
}


class Canvas:
    def __init__(self, w, h, bg=(0, 0, 0, 0)):
        self.im = Image.new('RGBA', (w * S, h * S), bg)
        self.d = ImageDraw.Draw(self.im)

    def r(self, *box):
        return [v * S for v in box]

    def rect(self, x, y, w, h, fill=None, outline=None, width=1):
        if w <= 0 or h <= 0: return
        self.d.rectangle(self.r(x, y, max(x, x + w - 1), max(y, y + h - 1)), fill=fill, outline=outline, width=width * S)

    def chamfer(self, x, y, w, h, c, fill, outline=None, width=1):
        pts = [(x + c, y), (x + w - c, y), (x + w, y + c), (x + w, y + h - c), (x + w - c, y + h), (x + c, y + h),
               (x, y + h - c), (x, y + c)]
        self.d.polygon([(px * S, py * S) for px, py in pts], fill=fill, outline=outline, width=width * S)

    def text(self, x, y, s, fill, f=F7, anchor='la'):
        self.d.text((x * S, y * S), s, fill=fill, font=f, anchor=anchor)

    def line(self, pts, fill, width=1):
        self.d.line([(px * S, py * S) for px, py in pts], fill=fill, width=width * S)

    def ellipse(self, x, y, w, h, fill=None, outline=None, width=1):
        self.d.ellipse(self.r(x, y, x + w, y + h), fill=fill, outline=outline, width=width * S)

    def paste(self, img, x, y):
        self.im.alpha_composite(img, (x * S, y * S))


def mc_frame(c, x, y, w, h):
    """Vanilla-style raised GUI frame (light top-left, dark bottom-right) in dark tones."""
    c.rect(x, y, w, h, fill=(198, 198, 198))
    c.rect(x, y, w - 1, 1, fill=(255, 255, 255)); c.rect(x, y, 1, h - 1, fill=(255, 255, 255))
    c.rect(x + 1, y + h - 1, w - 1, 1, fill=(85, 85, 85)); c.rect(x + w - 1, y + 1, 1, h - 1, fill=(85, 85, 85))


def slot(c, x, y):
    c.rect(x, y, 18, 18, fill=(139, 139, 139))
    c.rect(x, y, 17, 1, fill=(55, 55, 55)); c.rect(x, y, 1, 17, fill=(55, 55, 55))
    c.rect(x + 1, y + 17, 17, 1, fill=(255, 255, 255)); c.rect(x + 17, y + 1, 1, 17, fill=(255, 255, 255))


def inventory(c, x, y):
    for r in range(3):
        for k in range(9): slot(c, x + k * 18, y + r * 18)
    for k in range(9): slot(c, x + k * 18, y + 58)


def starfield(w, h, seed, tint=(255, 255, 255), density=0.004):
    rng = np.random.default_rng(seed)
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for _ in range(int(w * h * density)):
        x, y = rng.random() * w * S, rng.random() * h * S
        b = int(90 + 165 * rng.random() ** 3)
        r = 0.6 * S if rng.random() < 0.9 else 1.0 * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=tint + (b,))
    return im


def glow(img, radius):
    return img.filter(ImageFilter.GaussianBlur(radius * S))


def display(c, t, x, y, w, h):
    """The machine's status display: dark glass with a thin accent frame and corner ticks."""
    c.chamfer(x, y, w, h, 4, fill=t['base'] + (255,), outline=t['line'] + (255,))
    c.paste(starfield(w - 4, h - 4, hash(t['name']) % 997, density=0.0025), x + 2, y + 2)
    for (cx, cy, dx, dy) in ((x + 3, y + 3, 1, 1), (x + w - 3, y + 3, -1, 1), (x + 3, y + h - 3, 1, -1),
                             (x + w - 3, y + h - 3, -1, -1)):
        c.line([(cx, cy + 6 * dy), (cx, cy), (cx + 6 * dx, cy)], t['accent'] + (255,))


def bar(c, t, x, y, w, label, value, frac, colour=None):
    colour = colour or t['accent']
    c.text(x, y, label, t['dim'] + (255,), F6)
    c.text(x + w, y, value, t['glow'] + (255,), F6, anchor='ra')
    c.rect(x, y + 8, w, 4, fill=(0, 0, 0, 160), outline=t['line'] + (255,))
    if frac > 0: c.rect(x + 1, y + 9, max(1, int((w - 2) * frac)), 2, fill=colour + (255,))


def button(c, t, x, y, w, h, icon, label=None, active=False, shape='chamfer'):
    """Non-vanilla button: chamfered metal plate (or diamond) with an accent-lit icon."""
    fill = (t['panel'][0] + 14, t['panel'][1] + 14, t['panel'][2] + 14, 255)
    edge = (t['accent'] if active else t['line']) + (255,)
    if shape == 'diamond':
        cx, cy = x + w / 2, y + h / 2
        pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
        c.d.polygon([(px * S, py * S) for px, py in pts], fill=fill, outline=edge, width=S)
    else:
        c.chamfer(x, y, w, h, 3, fill=fill, outline=edge)
    if active:
        c.rect(x + 3, y + h - 2, w - 6, 1, fill=t['accent'] + (255,))
    c.text(x + w / 2, y + h / 2 - (3 if label else 0), icon, (t['glow'] if active else t['dim']) + (255,), F8,
           anchor='mm')
    if label: c.text(x + w / 2, y + h - 5, label, t['dim'] + (255,), F6, anchor='mm')


def window(t, title):
    """Main window 300 x 226: display, status chip row, inventory, button grid. Returns (canvas, inner origin)."""
    W, H = 300, 226
    c = Canvas(W + 8, H + 18)
    # Title tab, like the fancy UI's, with the machine name.
    c.chamfer(4, 0, 150, 14, 3, fill=t['panel'] + (255,), outline=t['line'] + (255,))
    c.text(12, 3, title, t['glow'] + (255,), F7B)
    c.chamfer(0, 12, W + 8, H + 4, 5, fill=t['panel'] + (255,), outline=t['line'] + (255,))
    return c, 4, 16


def chip(c, t, x, y, w, text, colour):
    c.chamfer(x, y, w, 12, 2, fill=(0, 0, 0, 140), outline=colour + (180,))
    c.text(x + w / 2, y + 2, text, colour + (255,), F6, anchor='ma')


def right_grid(c, t, ox, oy, buttons):
    """3 x 4 grid of 36 x 18 plates right of the inventory (x 174..292)."""
    for i, b in enumerate(buttons):
        col, row = i % 3, i // 3
        button(c, t, ox + 174 + col * 39, oy + 118 + row * 21, 36, 18, *b)


# ============================================================================ machine screens
def lance_main():
    t = THEMES['lance']
    c, ox, oy = window(t, t['name'])
    display(c, t, ox + 2, oy + 2, 292, 108)
    # Left: orbit sketch with the target and the shot arc.
    vx, vy = ox + 10, oy + 10
    sky = Canvas(96, 92)
    sky.ellipse(38, 36, 20, 20, fill=(70, 120, 200, 255))             # Earth
    for r in (30, 42):
        sky.ellipse(48 - r, 46 - r, 2 * r, 2 * r, outline=t['line'] + (180,))
    mx, my = 48 + 42 * math.cos(-0.8), 46 + 42 * math.sin(-0.8)
    sky.ellipse(mx - 5, my - 5, 10, 10, fill=(200, 200, 205, 255))
    sky.line([(58, 44), (70, 30), (mx - 3, my + 3)], t['accent'] + (255,))
    sky.ellipse(mx - 9, my - 9, 18, 18, outline=t['accent'] + (255,))
    c.paste(sky.im, vx, vy)
    c.text(vx + 48, vy + 92, 'MOON · 384 Mm', t['accent'] + (255,), F6, anchor='ma')
    # Right: readouts.
    x0 = ox + 112
    c.text(x0, oy + 8, 'TARGET  Moon   survey 100%', t['glow'] + (255,), F7)
    c.text(x0, oy + 18, 'Neutronium slug · 400 kg', t['dim'] + (255,), F6)
    bar(c, t, x0, oy + 28, 172, 'CAPACITOR BANK', '4.00e12 / 4.00e12 EU', 1.0)
    bar(c, t, x0, oy + 44, 172, 'BARREL', '300 / 2500 K', 0.0, (255, 110, 70))
    bar(c, t, x0, oy + 60, 172, 'LINER (naquadah alloy)', '12% worn', 0.12, (255, 210, 90))
    bar(c, t, x0, oy + 76, 172, 'AIM COMPUTATION', '16 000 CWU/t', 1.0, (120, 220, 255))
    c.text(x0, oy + 94, 'Regime: relativistic · v 4 400 km/s · 2 capsules returning', t['dim'] + (255,), F6)
    # Chip row.
    chip(c, t, ox + 2, oy + 114, 60, 'FORMED', (110, 230, 130))
    chip(c, t, ox + 66, oy + 114, 60, 'AUTO-FIRE', t['accent'])
    chip(c, t, ox + 130, oy + 114, 40, 'NEXUS', (190, 140, 255))
    inventory(c, ox + 2, oy + 132)
    right_grid(c, t, ox, oy, [('◀', 'TARGET'), ('▶', 'TARGET'), ('A', 'AUTO', True),
                              ('◎', 'ORBIT'), ('⚙', 'BENCH'), ('⇪', 'CAPSULE'),
                              ('ℹ', 'INFO'), ('◍', 'POWER', True), ('▣', 'IO')])
    return c


def stellar_main():
    t = THEMES['stellar']
    c, ox, oy = window(t, t['name'])
    display(c, t, ox + 2, oy + 2, 292, 108)
    # Star with corona and beams.
    star = Canvas(100, 100)
    g = Canvas(100, 100)
    g.ellipse(26, 26, 48, 48, fill=(120, 180, 255, 140))
    star.paste(glow(g.im, 6), 0, 0)
    star.line([(50, 50), (82, 4)], (200, 230, 255, 200), 3)
    star.line([(50, 50), (18, 96)], (200, 230, 255, 200), 3)
    star.ellipse(40, 40, 20, 20, fill=(235, 245, 255, 255))
    star.ellipse(14, 44, 72, 12, outline=(255, 160, 70, 200))
    c.paste(star.im, ox + 6, oy + 6)
    x0 = ox + 112
    c.text(x0, oy + 8, 'NEUTRON STAR · millisecond pulsar', t['glow'] + (255,), F7)
    c.text(x0, oy + 18, 'M 1.4210 M☉  ·  P 1.612 ms  ·  break-up 0.606 ms', t['dim'] + (255,), F6)
    bar(c, t, x0, oy + 28, 172, 'EXTRACTION', '2^58 EU/t', 0.7)
    bar(c, t, x0, oy + 44, 172, 'CRUST STRESS', '0.42', 0.42, (255, 200, 100))
    bar(c, t, x0, oy + 60, 172, 'CONTAINMENT DAMAGE', '0.0%', 0.0, (255, 90, 90))
    bar(c, t, x0, oy + 76, 172, 'BAND TIER', '3 / 4', 0.75, (170, 140, 255))
    c.text(x0, oy + 94, 'Output 2.88e17 EU/t · quakes decoded: micro, crab, Vela', t['dim'] + (255,), F6)
    chip(c, t, ox + 2, oy + 114, 60, 'STAR LIT', (255, 240, 170))
    chip(c, t, ox + 66, oy + 114, 60, 'PROBE OK', (110, 230, 130))
    chip(c, t, ox + 130, oy + 114, 40, 'NEXUS', (190, 140, 255))
    inventory(c, ox + 2, oy + 132)
    right_grid(c, t, ox, oy, [('−', 'EXTRACT'), ('+', 'EXTRACT'), ('ϟ', 'MAGNETAR'),
                              ('◷', 'M–P'), ('∿', 'SEISMO'), ('◉', 'STAR'),
                              ('ℹ', 'INFO'), ('◍', 'POWER', True), ('▣', 'IO')])
    return c


def collider_main():
    t = THEMES['collider']
    c, ox, oy = window(t, t['name'])
    display(c, t, ox + 2, oy + 2, 292, 108)
    ring = Canvas(100, 100)
    ring.ellipse(10, 10, 80, 80, outline=t['accent'] + (255,), width=3)
    for k in range(16):
        a = k * math.pi / 8
        ring.rect(50 + 40 * math.cos(a) - 2, 50 + 40 * math.sin(a) - 2, 4, 4, fill=(255, 255, 255, 220))
    ring.ellipse(44, 44, 12, 12, fill=(255, 90, 220, 255))
    ring.line([(10, 50), (44, 50)], (255, 90, 220, 220), 1)
    c.paste(ring.im, ox + 6, oy + 6)
    x0 = ox + 112
    c.text(x0, oy + 8, 'PHYSICS RUN · Nb3Sn 12 T · E_cm 21.6 TeV', t['glow'] + (255,), F7)
    c.text(x0, oy + 18, 'L = 1.45e34 cm⁻²s⁻¹ · active proposal: vertex detector', t['dim'] + (255,), F6)
    bar(c, t, x0, oy + 28, 172, 'RAMP', '100%', 1.0)
    bar(c, t, x0, oy + 44, 172, 'LIQUID HELIUM', '1.0 / 1.0 L/s', 1.0, (150, 220, 255))
    bar(c, t, x0, oy + 60, 172, 'PENNING TRAPS', '8.4e11 / 1e12 p̄', 0.84, (255, 90, 220))
    bar(c, t, x0, oy + 76, 172, 'CHARM SIGNIFICANCE', '3.4σ / 5σ', 0.68, (255, 210, 90))
    c.text(x0, oy + 94, 'Beam Dump ✓ · Detector ✓ · quench recovery 0 s', t['dim'] + (255,), F6)
    chip(c, t, ox + 2, oy + 114, 60, 'BEAM ON', (110, 230, 130))
    chip(c, t, ox + 66, oy + 114, 60, 'PHYSICS', t['accent'])
    chip(c, t, ox + 130, oy + 114, 40, 'NEXUS', (190, 140, 255))
    inventory(c, ox + 2, oy + 132)
    right_grid(c, t, ox, oy, [('⇄', 'MODE', True), ('⚛', 'MODEL'), ('☰', 'COMMITTEE'),
                              ('◌', 'TRAPS'), ('❄', 'CRYO'), ('◎', 'RING'),
                              ('ℹ', 'INFO'), ('◍', 'POWER', True), ('▣', 'IO')])
    return c


def rift_main():
    t = THEMES['rift']
    c, ox, oy = window(t, t['name'])
    display(c, t, ox + 2, oy + 2, 292, 108)
    vort = Canvas(100, 100)
    for k in range(5):
        r = 40 - k * 7
        vort.ellipse(50 - r, 50 - r, 2 * r, 2 * r, outline=(200 - k * 20, 120 + k * 20, 255, 200), width=2)
    vort.ellipse(42, 42, 16, 16, fill=(10, 0, 20, 255), outline=(255, 255, 255, 255))
    c.paste(glow(vort.im, 1.2), ox + 6, oy + 6)
    c.paste(vort.im, ox + 6, oy + 6)
    x0 = ox + 112
    c.text(x0, oy + 8, 'RIFT OPEN · seed 3F9A1C02 · Forge world', t['glow'] + (255,), F7)
    c.text(x0, oy + 18, 'depth 6 / 12 · chord 3 harmonics · SpaceTime 31 L/s', t['dim'] + (255,), F6)
    bar(c, t, x0, oy + 28, 172, 'RESONANCE', '0.86', 0.86)
    bar(c, t, x0, oy + 44, 172, 'STABILITY', '72 / 100', 0.72, (120, 230, 160))
    # Knobs with hot/cold.
    for i, (lab, val, close) in enumerate((('FREQ', '612.0 THz', 0.9), ('PHASE', '144°', 0.7),
                                           ('AMPL', '55%', 0.95))):
        y = oy + 62 + i * 13
        c.text(x0, y, lab, t['dim'] + (255,), F6)
        c.text(x0 + 30, y, val, t['glow'] + (255,), F6)
        for k in range(5):
            on = k < round(close * 5)
            col = (110, 230, 130) if close > 0.8 else (255, 210, 90)
            c.rect(x0 + 90 + k * 7, y + 1, 5, 6, fill=(col if on else (50, 40, 60)) + (255,))
        button(c, t, x0 + 132, y - 2, 18, 11, '−')
        button(c, t, x0 + 154, y - 2, 18, 11, '+')
    chip(c, t, ox + 2, oy + 114, 60, 'RIFT OPEN', (110, 230, 130))
    chip(c, t, ox + 66, oy + 114, 60, 'TUNING HATCH', t['accent'])
    chip(c, t, ox + 130, oy + 114, 40, 'NEXUS', (190, 140, 255))
    inventory(c, ox + 2, oy + 132)
    right_grid(c, t, ox, oy, [('◉', 'OPEN', True), ('✕', 'CLOSE'), ('♪', 'CHORD'),
                              ('✦', 'ATLAS'), ('∿', 'SEISMO'), ('⇣', 'DEPTH'),
                              ('ℹ', 'INFO'), ('◍', 'POWER', True), ('▣', 'IO')])
    return c


# ============================================================================ panels (open over the display)
def panel(t, title, w=292, h=170):
    c = Canvas(w, h)
    c.chamfer(0, 0, w, h, 6, fill=t['base'] + (250,), outline=t['accent'] + (255,))
    c.paste(starfield(w - 6, h - 6, len(title) * 13, density=0.003), 3, 3)
    c.chamfer(8, 4, len(title) * 5 + 20, 11, 3, fill=t['panel'] + (255,), outline=t['line'] + (255,))
    c.text(16, 6, title.upper(), t['accent'] + (255,), F6)
    button(c, t, w - 18, 4, 12, 11, '✕')
    return c


def lance_orbital_map():
    """Solar-system map in the spirit of GTO Dev 15's: Sun in the middle, dotted orbits, body tiles, a card."""
    t = THEMES['lance']
    c = panel(t, 'Orbital map')
    cx, cy = 110, 92
    sun = Canvas(40, 40)
    sun.ellipse(10, 10, 20, 20, fill=(255, 220, 120, 255))
    c.paste(glow(sun.im, 3), cx - 20, cy - 20)
    c.ellipse(cx - 6, cy - 6, 12, 12, fill=(255, 240, 180, 255))
    bodies = [('Moon', 18, 0.4, (200, 200, 205), True, '100%'), ('Phobos', 30, 2.2, (160, 130, 110), True, '100%'),
              ('Vesta', 44, 3.6, (190, 175, 150), True, '64%'), ('Ceres', 54, 5.2, (150, 150, 160), True, '12%'),
              ('Psyche', 64, 1.2, (210, 205, 190), False, '—'), ('Europa', 72, 4.4, (230, 235, 245), False, '—'),
              ('Arrokoth', 80, 0.0, (230, 140, 110), False, '—')]
    for name, r, a, col, ok, sv in bodies:
        for k in range(0, 360, 6):
            ang = math.radians(k)
            c.ellipse(cx + r * math.cos(ang) * 1.3 - 0.6, cy + r * math.sin(ang) * 0.85 - 0.6, 1.2, 1.2,
                      fill=t['dim'] + (200,))
        bx, by = cx + r * math.cos(a) * 1.3, cy + r * math.sin(a) * 0.85
        c.rect(bx - 3, by - 3, 7, 7, fill=col + (255 if ok else 110,), outline=(0, 0, 0, 255))
        c.text(bx + 6, by - 4, name, (t['glow'] if ok else t['dim']) + (255,), F6)
    # Selected body card (right), like GTO's side card.
    c.chamfer(196, 20, 88, 140, 4, fill=(0, 0, 0, 170), outline=t['line'] + (255,))
    c.text(202, 24, 'Vesta', t['accent'] + (255,), F8)
    c.text(202, 36, '170 000 Mm', t['dim'] + (255,), F6)
    for i, (k, v) in enumerate((('Survey', '64%'), ('Hardness', '3.5 MJ/kg'), ('Return', '5 h 15 min'),
                                ('Yields', 'Fe Mg Cr Pt'), ('Unlocks', 'salvo splitter'))):
        c.text(202, 50 + i * 12, k, t['dim'] + (255,), F6)
        c.text(280, 50 + i * 12, v, t['glow'] + (255,), F6, anchor='ra')
    button(c, t, 202, 124, 76, 14, '◎ SET TARGET', active=True)
    return c


def lance_bench():
    t = THEMES['lance']
    c = panel(t, 'Barrel bench')
    # Barrel schematic with rail sockets.
    c.chamfer(10, 20, 272, 40, 3, fill=(0, 0, 0, 150), outline=t['line'] + (255,))
    c.rect(18, 36, 256, 8, fill=(60, 50, 50, 255), outline=t['dim'] + (255,))
    for k in range(8):
        on = k < 4
        c.rect(24 + k * 31, 26, 22, 6, fill=((255, 190, 80) if on else (50, 44, 48)) + (255,))
        c.rect(24 + k * 31, 48, 22, 6, fill=((255, 190, 80) if on else (50, 44, 48)) + (255,))
    c.text(146, 62, '4 / 8 rails · inductance 50% · efficiency 41%', t['dim'] + (255,), F6, anchor='ma')
    slots = [('RAIL', 'CuNb ×4', True), ('COOLING', 'helium', False), ('SENSOR', 'telescope', True),
             ('CAPSULE', 'ablative', False), ('SALVO', 'locked: Vesta', False)]
    for i, (s_, v, on) in enumerate(slots):
        x = 10 + i * 55
        button(c, t, x, 76, 51, 30, s_[0], s_, active=on)
        c.text(x + 25, 108, v, (t['glow'] if on else t['dim']) + (255,), F6, anchor='ma')
    bar(c, t, 10, 124, 130, 'MASS', '170 / 800 t', 170 / 800)
    bar(c, t, 152, 124, 130, 'HEAT', '14 / 60', 14 / 60, (255, 120, 70))
    c.text(146, 146, 'Bench valid · click a socket to change its part', (110, 230, 130, 255), F6, anchor='ma')
    return c


def stellar_mp():
    t = THEMES['stellar']
    c = panel(t, 'Mass–period diagram')
    x0, y0, w, h = 24, 22, 250, 120
    c.rect(x0, y0, w, h, fill=(0, 0, 0, 140), outline=t['line'] + (255,))
    tov = y0 + h * (1 - (2.2 - 1.0) / 1.6)
    c.rect(x0 + 1, y0 + 1, w - 2, tov - y0 - 1, fill=(255, 70, 70, 40))
    c.line([(x0, tov), (x0 + w, tov)], (255, 90, 90, 255))
    c.text(x0 + w - 2, tov - 8, 'TOV 2.2 M☉', (255, 120, 120, 255), F6, anchor='ra')
    pts = [(x0 + 6 + 4 * k ** 0.5 * 4, y0 + h - k * 7) for k in range(18)]
    c.line(pts, (255, 200, 90, 255))
    c.text(x0 + 30, y0 + h - 10, 'Kepler break-up', (255, 200, 90, 255), F6)
    track = [(x0 + 200, y0 + 108), (x0 + 160, y0 + 100), (x0 + 120, y0 + 88), (x0 + 90, y0 + 80)]
    c.line(track, t['accent'] + (255,))
    c.ellipse(track[-1][0] - 3, track[-1][1] - 3, 6, 6, fill=t['glow'] + (255,))
    for i, v in enumerate(('1.0', '1.4', '1.8', '2.2', '2.6')):
        c.text(x0 - 4, y0 + h - i * 30 - 3, v, t['dim'] + (255,), F6, anchor='ra')
    c.text(x0 + w / 2, y0 + h + 6, 'spin period (ms, log)', t['dim'] + (255,), F6, anchor='ma')
    return c


def stellar_seismo():
    t = THEMES['stellar']
    c = panel(t, 'Seismogram')
    c.rect(12, 22, 268, 62, fill=(0, 0, 0, 150), outline=t['line'] + (255,))
    rng = np.random.default_rng(3)
    pts = []
    for x in range(14, 278):
        a = 2 + (14 * math.exp(-((x - 120) / 6) ** 2) + 22 * math.exp(-((x - 210) / 5) ** 2)) * math.sin(x * 1.7)
        pts.append((x, 53 + a + rng.normal() * 0.8))
    c.line(pts, (120, 255, 170, 255))
    c.text(120, 26, 'Crab', t['accent'] + (255,), F6, anchor='ma')
    c.text(210, 26, 'Vela', t['accent'] + (255,), F6, anchor='ma')
    for i, (q, s_, st) in enumerate((('Micro', '1e-9', 'decoded → bands 2'), ('Crab', '5e-8', 'decoded'),
                                     ('Vela', '1.1e-6', 'decoded → bands 3'), ('Anti', '—', 'magnetar only'),
                                     ('Collapse', '—', 'cross the TOV edge'))):
        y = 92 + i * 14
        c.text(14, y, q, t['glow'] + (255,), F7)
        c.text(90, y, s_, t['dim'] + (255,), F7)
        c.text(160, y, st, ((110, 230, 130) if 'decoded' in st else t['dim']) + (255,), F7)
    return c


def collider_model():
    t = THEMES['collider']
    c = panel(t, 'Standard Model board')
    parts = [('p̄', 'Antiproton', 5.0), ('K', 'Kaon', 5.0), ('Λ', 'Lambda', 5.0), ('c', 'Charm', 3.4), ('b', 'Bottom', 1.2),
             ('W', 'W boson', 0.4), ('Z', 'Z boson', 0.3), ('H', 'Higgs', 0), ('t', 'Top', 0), ('X', 'X-Nexus', 0)]
    for i, (sym, name, z) in enumerate(parts):
        x, y = 10 + (i % 5) * 55, 22 + (i // 5) * 70
        col = (110, 230, 130) if z >= 5 else (255, 210, 90) if z >= 3 else t['dim']
        c.chamfer(x, y, 50, 64, 4, fill=(0, 0, 0, 160), outline=col + (255,))
        c.text(x + 25, y + 6, sym, col + (255,), font(14, True), anchor='ma')
        c.text(x + 25, y + 30, name, t['glow'] + (255,), F6, anchor='ma')
        c.text(x + 25, y + 40, f'{z:.1f}σ', col + (255,), F7, anchor='ma')
        c.rect(x + 6, y + 54, 38, 3, fill=(40, 40, 40, 255))
        c.rect(x + 6, y + 54, int(38 * min(1, z / 5)), 3, fill=col + (255,))
    return c


def collider_committee():
    t = THEMES['collider']
    c = panel(t, 'Beam-time committee')
    rows = [('Nb3Sn magnet', '5 fb⁻¹ and 7 TeV', 1, 'done'), ('Vertex detector', 'charm 5σ', 0.68, 'active'),
            ('Stochastic cooling', '20 fb⁻¹', 0, 'queued'), ('Cryogenic Penning', '1e13 p̄ or 40 fb⁻¹', 0, 'queued'),
            ('REBCO magnet', 'W and Z 5σ', 0, 'queued'), ('Lepton collider', 'bottom 5σ', 0, 'queued'),
            ('Heavy ions', 'top 5σ', 0, 'queued'), ('Neutronium magnet', 'Higgs 5σ', 0, 'queued'),
            ('Beyond the SM', 'X-Nexus 3σ', 0, 'queued')]
    for i, (n, req, f, st) in enumerate(rows):
        y = 20 + i * 16
        col = (110, 230, 130) if st == 'done' else t['accent'] if st == 'active' else t['dim']
        c.chamfer(10, y, 272, 14, 2, fill=(0, 0, 0, 140), outline=col + (160,))
        c.text(16, y + 3, n, col + (255,), F7)
        c.text(130, y + 3, req, t['dim'] + (255,), F6)
        c.rect(214, y + 5, 40, 4, fill=(40, 40, 40, 255))
        c.rect(214, y + 5, int(40 * f), 4, fill=col + (255,))
        c.text(276, y + 3, st, col + (255,), F6, anchor='ra')
    return c


def rift_chord():
    t = THEMES['rift']
    c = panel(t, 'Harmonic chord')
    cx, cy, r = 80, 92, 56
    names = ['2:1', '3:2', '4:3', '5:4', '8:5', '9:5', '45:32', '16:15']
    pts = []
    for i, n in enumerate(names):
        a = -math.pi / 2 + i * 2 * math.pi / 8
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pts.append((x, y))
        rec = i in (0, 1, 2, 4)
        load = i in (0, 1, 4)
        c.ellipse(x - 5, y - 5, 10, 10, fill=((255, 255, 255) if load else t['panel'] if rec else (40, 30, 50)) + (255,),
                  outline=t['accent'] + (255,))
        c.text(x + (10 if x >= cx else -10), y - 4, n, (t['glow'] if rec else t['dim']) + (255,), F6,
               anchor='la' if x >= cx else 'ra')
    for a_, b_ in ((0, 1), (1, 4), (4, 0)):
        c.line([pts[a_], pts[b_]], (120, 220, 255, 220))
    c.chamfer(160, 26, 122, 130, 4, fill=(0, 0, 0, 160), outline=t['line'] + (255,))
    for i, (k, v) in enumerate((('Loaded', '2:1  3:2  8:5'), ('Consonance', '0.42'), ('Stability λ', '1.32 /s'),
                                ('Max depth', '12'), ('Recorded', '4 of 8'))):
        c.text(166, 32 + i * 14, k, t['dim'] + (255,), F6)
        c.text(276, 32 + i * 14, v, t['glow'] + (255,), F6, anchor='ra')
    c.text(221, 110, 'Click a recorded harmonic', t['dim'] + (255,), F6, anchor='ma')
    c.text(221, 120, 'to load or unload it (max 5)', t['dim'] + (255,), F6, anchor='ma')
    return c


def rift_atlas():
    t = THEMES['rift']
    c = panel(t, 'Seed atlas')
    rng = np.random.default_rng(12)
    pts = [(20 + rng.random() * 160, 24 + rng.random() * 130) for _ in range(14)]
    for i in range(len(pts) - 1):
        if rng.random() < 0.5: c.line([pts[i], pts[i + 1]], t['line'] + (200,))
    for i, (x, y) in enumerate(pts):
        col = [(110, 230, 130), (255, 210, 90), (196, 120, 255)][i % 3]
        c.ellipse(x - 3, y - 3, 6, 6, fill=col + (255,))
    c.ellipse(pts[3][0] - 7, pts[3][1] - 7, 14, 14, outline=(255, 255, 255, 255))
    c.chamfer(190, 22, 92, 136, 4, fill=(0, 0, 0, 160), outline=t['line'] + (255,))
    c.text(196, 26, '1B44C9F0', t['accent'] + (255,), F8)
    for i, (k, v) in enumerate((('Biome', 'Forge world'), ('Best R', '0.847'), ('Depth', '6'), ('Harmonic', '4:3'),
                                ('Yields', 'W Os Ir'))):
        c.text(196, 42 + i * 12, k, t['dim'] + (255,), F6)
        c.text(278, 42 + i * 12, v, t['glow'] + (255,), F6, anchor='ra')
    button(c, t, 196, 132, 80, 14, '◉ REOPEN SEED', active=True)
    return c


def info_panel():
    """New information panel: a field manual on a slate, chapter rail on the left, page on the right."""
    t = dict(THEMES['lance'])
    w, h = 292, 200
    c = Canvas(w, h)
    c.chamfer(0, 0, w, h, 6, fill=(16, 18, 22, 252), outline=(150, 160, 170, 255))
    # Rivets and a hazard strip, a technical manual rather than a cosmic panel.
    for x in (6, w - 8):
        for y in (6, h - 8): c.ellipse(x - 1, y - 1, 3, 3, fill=(120, 125, 130, 255))
    for k in range(0, w - 20, 8):
        c.d.polygon([((10 + k) * S, 14 * S), ((14 + k) * S, 14 * S), ((10 + k) * S, 18 * S), ((6 + k) * S, 18 * S)],
                    fill=(230, 180, 40, 255))
    c.text(12, 22, 'FIELD MANUAL · KINETIC ORBITAL LANCE', (230, 230, 235, 255), F8)
    c.text(w - 12, 22, 'rev. GTNA', (130, 135, 140, 255), F6, anchor='ra')
    chapters = ['Overview', 'Structure', 'Bank & firing', 'Targets & aim', 'Bench & wear', 'Yields']
    for i, ch in enumerate(chapters):
        y = 38 + i * 18
        on = i == 2
        c.chamfer(10, y, 70, 15, 2, fill=((230, 180, 40) if on else (32, 34, 40)) + (255,),
                  outline=(80, 84, 92, 255))
        c.text(16, y + 4, f'{i + 1}. {ch}', ((20, 20, 20) if on else (190, 195, 200)) + (255,), F6)
    c.chamfer(86, 36, 196, 156, 3, fill=(24, 26, 30, 255), outline=(80, 84, 92, 255))
    c.text(92, 40, '3. Bank & firing', (230, 180, 40, 255), F8)
    lines = ['The bank charges from the Nexus network',
             'at up to 2^36 EU/t. With AUTO on, a full',
             'bank fires one slug from the input bus.', '']
    for i, l in enumerate(lines): c.text(92, 54 + i * 10, l, (210, 212, 216, 255), F6)
    c.chamfer(92, 96, 184, 24, 2, fill=(14, 30, 18, 255), outline=(90, 180, 110, 255))
    c.text(98, 100, 'v = √(2·η·E / m)', (130, 240, 150, 255), F7)
    c.text(98, 110, 'bank = 4e12 · 2^(rings−1) EU', (130, 240, 150, 255), F6)
    for i, l in enumerate(['Slugs: naquadah alloy, trinium, neutronium,',
                           'cosmic neutronium, white dwarf matter.',
                           'Heavier slugs are slower but hit harder.']):
        c.text(92, 126 + i * 10, l, (210, 212, 216, 255), F6)
    c.text(92, 170, '◀ prev', (130, 135, 140, 255), F6)
    c.text(276, 170, 'next ▶', (230, 180, 40, 255), F6, anchor='ra')
    return c


def sheet(name, main, panels):
    """Main window, then its panels; panels show where they sit over the display."""
    pad = 12 * S
    mw, mh = main.im.size
    pw = max(p.im.size[0] for p in panels)
    W = mw + pw + pad * 3
    H = max(mh, sum(p.im.size[1] for p in panels) + pad * (len(panels) - 1)) + pad * 2
    out = Image.new('RGBA', (W, H), (36, 36, 40, 255))
    out.alpha_composite(main.im, (pad, pad))
    y = pad
    for p in panels:
        out.alpha_composite(p.im, (mw + pad * 2, y))
        y += p.im.size[1] + pad
    out.save(os.path.join(OUT, f'{name}.png'))
    print(name, out.size)


def main():
    sheet('lance', lance_main(), [lance_orbital_map(), lance_bench()])
    sheet('stellar', stellar_main(), [stellar_mp(), stellar_seismo()])
    sheet('collider', collider_main(), [collider_model(), collider_committee()])
    sheet('rift', rift_main(), [rift_chord(), rift_atlas()])
    ip = info_panel()
    ip.im.save(os.path.join(OUT, 'info_panel.png'))
    # Overlay example: a panel opened over the lance display, as it would appear in game.
    m = lance_main()
    m.paste(lance_orbital_map().im.resize((292 * S, 170 * S)), 6, 2)
    m.im.save(os.path.join(OUT, 'lance_panel_open.png'))


if __name__ == '__main__':
    main()
