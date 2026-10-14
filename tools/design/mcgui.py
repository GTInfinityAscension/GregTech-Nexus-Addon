"""Tiny Minecraft-GUI compositor: real GTNA/GTCEu textures + the vanilla bitmap font, drawn at GUI pixel scale."""
import json, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
GTNA = '/home/raishxn/MineProjects/GregTech-Nexus-Addon/src/main/resources/assets/gtna/textures'
GTCEU = '/tmp/claude-1000/-home-raishxn/462c1290-9b24-46c2-ab31-8c8cd094341f/scratchpad/wiki/gtceu/assets/gtceu/textures'
GF = GTNA + '/gui/godforge/'

_tex = {}
def tex(path):
    if path not in _tex: _tex[path] = Image.open(path).convert('RGBA')
    return _tex[path]

# ---------------------------------------------------------------- font
class Font:
    def __init__(self):
        d = json.load(open(HERE + '/font/assets/minecraft/font/include/default.json'))
        self.glyph = {}
        for p in reversed(d['providers']):  # ascii last wins for latin
            img = tex(HERE + '/font/assets/minecraft/textures/' + p['file'].split(':')[1])
            rows = p['chars']; cw = img.width // len(rows[0]); ch = img.height // len(rows)
            h = p.get('height', 8); asc = p.get('ascent', 7)
            for r, row in enumerate(rows):
                for c, chr_ in enumerate(row):
                    if chr_ in ('\u0000', ' '): continue
                    g = img.crop((c * cw, r * ch, (c + 1) * cw, (r + 1) * ch))
                    if h != ch: g = g.resize((round(cw * h / ch), h), Image.NEAREST)
                    bb = g.getbbox(); w = (bb[2] if bb else 0)
                    self.glyph[chr_] = (g.crop((0, 0, max(w, 1), g.height)), w, asc)
    def width(self, s): return sum((4 if c == ' ' else self.glyph.get(c, (None, 5, 7))[1] + 1) for c in s)
    def draw(self, im, x, y, s, color=(255, 255, 255), shadow=True):
        cx = x
        for c in s:
            if c == ' ': cx += 4; continue
            g = self.glyph.get(c)
            if not g: cx += 6; continue
            img, w, asc = g; oy = y + 7 - asc
            mask = img.split()[3]
            if shadow:
                sc = tuple(v // 4 for v in color)
                im.paste(Image.new('RGBA', img.size, sc + (255,)), (cx + 1, oy + 1), mask)
            im.paste(Image.new('RGBA', img.size, tuple(color) + (255,)), (cx, oy), mask)
            cx += w + 1
        return cx
FONT = Font()

# ---------------------------------------------------------------- widgets
def nine(im, path, x, y, w, h, b=3):
    t = tex(path); W, H = t.size
    parts = [(0, 0, b, b, x, y, b, b), (W - b, 0, W, b, x + w - b, y, b, b), (0, H - b, b, H, x, y + h - b, b, b), (W - b, H - b, W, H, x + w - b, y + h - b, b, b),
             (b, 0, W - b, b, x + b, y, w - 2 * b, b), (b, H - b, W - b, H, x + b, y + h - b, w - 2 * b, b),
             (0, b, b, H - b, x, y + b, b, h - 2 * b), (W - b, b, W, H - b, x + w - b, y + b, b, h - 2 * b),
             (b, b, W - b, H - b, x + b, y + b, w - 2 * b, h - 2 * b)]
    for sx0, sy0, sx1, sy1, dx, dy, dw, dh in parts:
        if dw > 0 and dh > 0: im.alpha_composite(t.crop((sx0, sy0, sx1, sy1)).resize((dw, dh), Image.NEAREST), (dx, dy))

def panel(im, x, y, w, h): nine(im, GTCEU + '/gui/base/background.png', x, y, w, h, 4)
def display(im, x, y, w, h): nine(im, GTCEU + '/gui/base/display.png', x, y, w, h, 2)
def blit(im, path, x, y, w=None, h=None, alpha=255):
    t = tex(path)
    if w: t = t.resize((w, h or w), Image.NEAREST)
    if alpha < 255:
        t = t.copy(); a = t.split()[3].point(lambda v: v * alpha // 255); t.putalpha(a)
    im.alpha_composite(t, (x, y))
def text(im, x, y, s, color=(255, 255, 255), shadow=True, center=False):
    if center: x -= FONT.width(s) // 2
    return FONT.draw(im, x, y, s, color, shadow)
def purple_button(im, x, y, label, w=32, h=16, pressed=False, color=(255, 200, 40)):
    blit(im, GF + ('button_purple_pressed.png' if pressed else 'button_purple.png'), x, y, w, h)
    text(im, x + w // 2, y + 4, label, color, center=True)
def std_button(im, x, y, w, h, overlay=None, pressed=False):
    blit(im, GF + ('button_standard_pressed.png' if pressed else 'button_standard.png'), x, y, w, h)
    if overlay: blit(im, overlay, x + (w - 16) // 2, y + (h - 16) // 2)
def bar(im, x, y, w, frac, color='blue', h=7):
    blit(im, GF + 'progressbar_godforge_progressbar_background.png', x, y, w, h)
    f = tex(GF + f'progressbar_godforge_progressbar_{color}.png').resize((w, h), Image.NEAREST)
    n = max(0, min(w, round(w * frac)))
    if n: im.alpha_composite(f.crop((0, 0, n, h)), (x, y))
def line(im, a, b, rgba, width=4):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).line([a, b], fill=rgba, width=width); im.alpha_composite(lay)
def dashed(im, a, b, rgba, width=1, dash=3):
    import math
    L = math.dist(a, b); n = int(L // (dash * 2)) + 1
    for i in range(n):
        t0, t1 = i * 2 * dash / L, min(1, (i * 2 * dash + dash) / L)
        line(im, (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1), rgba, width)
def rect(im, x, y, w, h, rgba):
    if w <= 0 or h <= 0: return
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(lay).rectangle([x, y, x + w - 1, y + h - 1], fill=rgba); im.alpha_composite(lay)
def ring(im, cx, cy, r, frac, rgba, width=2, back=(60, 60, 80, 200)):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=back, width=width)
    if frac > 0: d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=rgba, width=width)
    im.alpha_composite(lay)
def background(im, path, x, y, w, h, alpha=255):
    t = tex(path).resize((w, h), Image.NEAREST)
    if alpha < 255: t = t.copy(); t.putalpha(t.split()[3].point(lambda v: v * alpha // 255))
    im.alpha_composite(t, (x, y))
def save(im, path, scale=3):
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(path)

# colours used by GTNH/GT GUIs
GOLD, WHITE, GRAY, CYAN, RED, GREEN, PURPLE, DARK = (255, 200, 40), (255, 255, 255), (170, 170, 170), (85, 255, 255), (255, 85, 85), (85, 255, 85), (255, 85, 255), (64, 64, 64)
