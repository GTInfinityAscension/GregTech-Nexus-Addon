"""Godforge-style mockups of the new progression screens, built from real GTNA/GTCEu textures."""
import math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcgui import *
from PIL import Image

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out'); os.makedirs(OUT, exist_ok=True)
PL = GTNA + '/block/eye_of_harmony/planet/'
IT = os.path.dirname(os.path.abspath(__file__)) + '/vanilla/assets/minecraft/textures/item/'
CAS = GTNA + '/block/casings/'
CC = GTCEU + '/block/casings/'
W, H = 320, 200


def frame(title):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); panel(im, 0, 0, W, H)
    text(im, 7, 6, title, DARK, shadow=False)
    return im


def tab_bar(im, labels, active):
    x = 7
    for i, l in enumerate(labels):
        w = FONT.width(l) + 12
        purple_button(im, x, H - 21, l, w=w, h=16, pressed=(i == active), color=GOLD if i == active else GRAY)
        x += w + 3


# ------------------------------------------------------------------ Lança: levantamento
def lance_survey():
    im = frame('Lança Cinética Orbital · Levantamento')
    background(im, GF + 'background_space.png', 6, 17, 196, 156)
    bodies = {'Lua': (22, 100, 'moon', 1.0), 'Fobos': (54, 100, 'mars', 1.0), 'Vesta': (88, 58, 'mercury', .72), 'Ceres': (88, 144, 'glacio', .41),
              'Psique': (126, 58, 'venus', .12), 'Europa': (126, 144, 'end', 0), 'Arrokoth': (160, 100, 'nether', 0), 'Nexus-1': (184, 58, None, 0)}
    edges = [('Lua', 'Fobos'), ('Fobos', 'Vesta'), ('Fobos', 'Ceres'), ('Vesta', 'Psique'), ('Ceres', 'Europa'), ('Europa', 'Arrokoth'), ('Psique', 'Arrokoth'), ('Arrokoth', 'Nexus-1')]
    for a, b in edges:
        A, B = bodies[a], bodies[b]
        lit = A[3] >= 1 and B[3] > 0
        (line if lit else dashed)(im, (A[0], A[1]), (B[0], B[1]), (120, 150, 255, 170) if lit else (150, 150, 170, 150), 2 if lit else 1)
    for n, (x, y, t, f) in bodies.items():
        locked = f == 0 and n not in ('Lua',)
        if t: blit(im, PL + t + '_front.png', x - 8, y - 8, 16, 16, alpha=110 if locked else 255)
        else: blit(im, GF + 'picture_rainbow_square.png', x - 8, y - 8, 16, 16, alpha=150)
        ring(im, x, y, 11, f, (85, 255, 255, 255) if f >= 1 else (255, 200, 40, 255), 2)
        if n == 'Vesta': blit(im, GF + 'picture_green_selector.png', x - 12, y - 12, 24, 24)
        text(im, x, y - 22, n, GOLD if n == 'Vesta' else WHITE, center=True)
        text(im, x, y + 14, f'{int(f * 100)}%' if not locked else 'bloq.', CYAN if f >= 1 else (GRAY if locked else GOLD), center=True)
    # detail
    display(im, 206, 17, 107, 156)
    blit(im, PL + 'mercury_front.png', 212, 23, 24, 24)
    text(im, 242, 25, 'Vesta', GOLD); text(im, 242, 36, '72%', WHITE)
    bar(im, 212, 52, 95, .72, 'blue')
    for k, m in enumerate((25, 50, 75)): rect(im, 212 + round(95 * m / 100), 51, 1, 9, (255, 200, 40, 255))
    rows = [('Fe', 'revelado', GREEN), ('Mg', 'revelado', GREEN), ('Cr', 'revelado', GREEN), ('Pt', '???', GRAY)]
    for i, (e, s, c) in enumerate(rows): text(im, 212, 66 + i * 10, e, WHITE); text(im, 238, 66 + i * 10, s, c)
    text(im, 212, 110, 'Dureza 3,5 MJ/kg', GRAY); text(im, 212, 120, 'Retorno 19 s', GRAY)
    purple_button(im, 230, 140, 'MIRAR', w=60, h=18)
    # capsule queue
    for i, t_ in enumerate((19, 34, 48, 61)):
        x = 8 + i * 48
        blit(im, GTCEU + '/gui/base/slot.png', x, 176, 18, 18); blit(im, IT + 'firework_rocket.png', x + 1, 177, 16, 16)
        text(im, x + 21, 181, f'{t_}s', WHITE)
    save(im, OUT + '/lance_survey.png')


# ------------------------------------------------------------------ Lança: bancada
def lance_bench():
    im = frame('Lança Cinética Orbital · Bancada do Cano')
    display(im, 6, 17, 210, 110)
    # blueprint of the cannon in side view
    for gx in range(10, 214, 8): rect(im, gx, 19, 1, 106, (60, 110, 160, 90))
    for gy in range(21, 125, 8): rect(im, 8, gy, 206, 1, (60, 110, 160, 90))
    rect(im, 40, 92, 60, 26, (85, 170, 255, 60)); rect(im, 30, 118, 80, 4, (85, 170, 255, 120))
    rect(im, 60, 60, 150, 26, (85, 170, 255, 50))
    rails = ['rail_cu'] * 5 + ['rail_sc'] * 3
    for i, r in enumerate(rails):
        x = 66 + i * 17
        blit(im, GTCEU + '/gui/base/slot.png', x, 64, 18, 18)
        blit(im, (CC + 'coils/machine_coil_cupronickel.png') if r == 'rail_cu' else (CC + 'coils/machine_coil_superconductor.png'), x + 1, 65, 16, 16)
    text(im, 66, 54, 'Trilhos 8/8', CYAN)
    slots = [('Revest.', CAS + 'neutronium_stable_casing.png', 14, 26), ('Arref.', CAS + 'cold_ice_casing.png', 14, 96), ('Sensor', IT + 'spyglass.png', 110, 96),
             ('Cápsula', IT + 'firework_rocket.png', 150, 96), ('Salva', None, 190, 96)]
    for n, t, x, y in slots:
        blit(im, GTCEU + '/gui/base/slot.png', x, y, 18, 18)
        if t: blit(im, t, x + 1, y + 1, 16, 16)
        else: blit(im, GF + 'picture_unselected_option.png', x, y, 18, 18)
        text(im, x + 9, y + 20, n, WHITE, center=True)
    # budgets
    display(im, 220, 17, 93, 110)
    for i, (n, v, f, c) in enumerate((('Massa', '820/1000 t', .82, 'purple'), ('Calor', '64/80', .8, 'red'), ('Indutância', '0,71 L', .71, 'blue'))):
        text(im, 225, 22 + i * 26, n, GOLD); text(im, 309, 22 + i * 26, v, WHITE, center=False) if False else text(im, 225, 31 + i * 26 + 8, v, GRAY)
        bar(im, 225, 31 + i * 26, 82, f, c)
    text(im, 225, 104, 'η = 0,52', CYAN); text(im, 225, 114, 'v = 4.521 km/s', CYAN)
    # inventory of components
    comps = [CC + 'coils/machine_coil_cupronickel.png', CC + 'coils/machine_coil_superconductor.png', CAS + 'neutronium_stable_casing.png', CAS + 'cold_ice_casing.png',
             IT + 'spyglass.png', IT + 'firework_rocket.png', IT + 'ender_eye.png', IT + 'nether_star.png']
    text(im, 7, 131, 'Componentes', DARK, shadow=False)
    for i, t in enumerate(comps):
        x = 7 + i * 19; blit(im, GTCEU + '/gui/base/slot.png', x, 141, 18, 18); blit(im, t, x + 1, 142, 16, 16, alpha=255 if i < 6 else 90)
        if i >= 6: text(im, x + 5, 146, '?', RED)
    text(im, 7, 162, 'Bloqueado: planta no veio-mãe de Psique', GRAY)
    purple_button(im, 240, 140, 'MONTAR', w=70, h=18)
    tab_bar(im, ['Levantamento', 'Bancada', 'Fila'], 1)
    save(im, OUT + '/lance_bench.png')


# ------------------------------------------------------------------ Portão: partitura
def rift_score():
    im = frame('Portão de Fenda · Partitura de Ressonância')
    display(im, 6, 17, 210, 70)
    for x in range(8, 214):
        t = (x - 8) / 206 * 6 * math.pi
        for k, (amp, ph, col) in enumerate(((22, 0, (85, 255, 255, 255)), (18, 0.6, (255, 85, 255, 255)))):
            y = 52 + amp * math.sin(t + ph)
            rect(im, x, round(y), 1, 2, col)
    rect(im, 160, 19, 54, 14, (0, 0, 0, 200)); text(im, 187, 22, 'R = 0,94', GREEN, center=True)
    for i, (n, v) in enumerate((('Freq.', '412,7 THz'), ('Fase', '128°'), ('Ampl.', '63%'))):
        x = 6 + i * 71
        display(im, x, 90, 68, 26); text(im, x + 4, 93, n, GOLD); text(im, x + 4, 104, v.split(' ')[0], WHITE)
        std_button(im, x + 50, 92, 14, 10); text(im, x + 54, 93, '+', WHITE); std_button(im, x + 50, 104, 14, 10); text(im, x + 54, 105, '-', WHITE)
    # staff
    display(im, 6, 119, 210, 54)
    for k in range(5): rect(im, 12, 127 + k * 8, 198, 1, (170, 170, 220, 200))
    for i, (t, n, c, y) in enumerate(((IT + 'diamond.png', '3:2', CYAN, 134), (IT + 'glowstone_dust.png', '2:1', GOLD, 126), (IT + 'redstone.png', '45:32', RED, 142))):
        x = 40 + i * 60; blit(im, t, x, y - 8, 16, 16); text(im, x + 8, 160, n, c, center=True)
    # analysis
    display(im, 220, 17, 93, 156)
    text(im, 225, 22, 'Acorde', GOLD)
    for i, (n, v, c) in enumerate((('C', '0,40', WHITE), ('λ₀', '× 0,90', GREEN), ('Prof.', '× 0,70', RED))):
        text(im, 225, 36 + i * 11, n, GRAY); text(im, 260, 36 + i * 11, v, c)
    blit(im, GF + 'picture_overlay_green.png', 225, 74, 83, 12); text(im, 266, 76, 'Estável', WHITE, center=True)
    text(im, 225, 94, 'Gemas', GOLD)
    for i, (t, n) in enumerate(((IT + 'diamond.png', 'Quinta'), (IT + 'glowstone_dust.png', 'Oitava'), (IT + 'redstone.png', 'Trítono'), (IT + 'emerald.png', 'Terça'))):
        blit(im, GTCEU + '/gui/base/slot.png', 225, 104 + i * 17, 18, 18); blit(im, t, 226, 105 + i * 17, 16, 16); text(im, 247, 109 + i * 17, n, WHITE)
    tab_bar(im, ['Sintonia', 'Partitura', 'Atlas'], 1)
    save(im, OUT + '/rift_score.png')


# ------------------------------------------------------------------ Portão: atlas
def rift_atlas():
    im = frame('Portão de Fenda · Atlas de Constelações')
    background(im, GF + 'background_purple_glow.png', 6, 17, 210, 156)
    random.seed(4)
    for _ in range(90): rect(im, random.randint(8, 214), random.randint(19, 170), 1, 1, (255, 255, 255, random.randint(80, 220)))
    crown = [(30, 40), (52, 30), (74, 42), (64, 64), (40, 64)]
    for i in range(len(crown)): line(im, crown[i], crown[(i + 1) % len(crown)], (255, 200, 40, 230), 2)
    other = [(120, 40), (150, 52), (182, 36), (170, 80)]
    for a, b in ((0, 1), (1, 2), (1, 3)): line(im, other[a], other[b], (120, 150, 255, 200), 2)
    open_ = [(110, 120), (140, 110), (168, 128), (196, 150), (140, 150)]
    for a, b, d in ((0, 1, False), (1, 2, False), (2, 3, True), (1, 4, True)): (dashed if d else line)(im, open_[a], open_[b], (170, 170, 200, 200), 1 if d else 2)
    for pts, col in ((crown, GOLD), (other, CYAN), (open_, WHITE)):
        for p in pts: blit(im, GF + 'button_celestial.png', p[0] - 4, p[1] - 4, 8, 8)
    text(im, 12, 76, 'Coroa de Mercúrio', GOLD)
    labels = ['A3F-19', '7C2-04', '9D8-27', '1B4-09']
    for p, l in zip(other, labels): text(im, p[0], p[1] + 6, l, WHITE, center=True)
    blit(im, GF + 'picture_green_selector.png', 131, 101, 18, 18)
    display(im, 220, 17, 93, 156)
    text(im, 225, 22, 'Semente A3F-19', GOLD)
    for i, (n, v) in enumerate((('Bioma', 'Hg'), ('Prof.', '23'), ('R máx', '0,987'), ('Harm.', '5:4'), ('Const.', '3/5'))):
        text(im, 225, 36 + i * 11, n, GRAY); text(im, 270, 36 + i * 11, v, WHITE)
    blit(im, PL + 'mercury_front.png', 250, 96, 32, 32)
    purple_button(im, 228, 140, 'REABRIR', w=78, h=18)
    tab_bar(im, ['Sintonia', 'Partitura', 'Atlas'], 2)
    save(im, OUT + '/rift_atlas.png')


# ------------------------------------------------------------------ Colisor: modelo padrão
def collider_sm():
    im = frame('Anel Colisor · Modelo Padrão')
    display(im, 6, 17, 150, 156)
    grid = [['u', 'c', 't', 'γ'], ['d', 's', 'b', 'g'], ['e', 'μ', 'τ', 'Z'], ['νe', 'νμ', 'ντ', 'W']]
    known = {'u', 'c', 'γ', 'd', 's', 'b', 'g', 'e', 'μ', 'τ', 'Z', 'νe', 'νμ', 'ντ', 'W'}
    cols = [(255, 85, 255), (255, 85, 255), (85, 255, 85), (255, 200, 40)]
    for r, row in enumerate(grid):
        for c, p in enumerate(row):
            x, y = 12 + c * 28, 24 + r * 28
            std_button(im, x, y, 24, 24, pressed=p not in known)
            text(im, x + 12, y + 8, p if p in known else '?', cols[c if r < 2 else (2 if c < 3 else 3)] if p in known else DARK, center=True)
    std_button(im, 124, 24, 24, 52); text(im, 136, 46, '?', DARK, center=True); text(im, 136, 80, 'H', GRAY, center=True)
    text(im, 12, 140, 'Além do Modelo Padrão', GOLD); std_button(im, 12, 150, 20, 20, pressed=True); text(im, 22, 156, '?', DARK, center=True)
    # histogram
    display(im, 160, 17, 153, 110)
    text(im, 165, 21, 'Massa invariante (GeV)', GRAY)
    random.seed(7)
    for i in range(36):
        m = 100 + i * 1.4; bg = 70 * math.exp(-(m - 100) / 40); sig = 26 * math.exp(-((m - 125) / 3) ** 2)
        h = int(bg + sig + random.uniform(-3, 3)); x = 166 + i * 4
        rect(im, x, 120 - h, 3, h, (110, 110, 140, 255)); rect(im, x, 120 - h, 3, int(sig), (85, 255, 255, 255))
    text(im, 236, 34, 'Higgs 3,4σ', CYAN)
    text(im, 160, 131, 'Significância até 5σ', GOLD); bar(im, 160, 141, 153, 3.4 / 5, 'blue')
    text(im, 160, 151, 'L_int 1.502 / 3.906 fb⁻¹', WHITE)
    for i, (n, v, c) in enumerate((('<3σ', '10%', GRAY), ('3σ', '40%', GOLD), ('5σ', '100%', GREEN))):
        text(im, 160 + i * 52, 163, f'{n} {v}', c)
    tab_bar(im, ['Anel', 'Modelo Padrão', 'Comitê'], 1)
    save(im, OUT + '/collider_sm.png')


# ------------------------------------------------------------------ Colisor: comitê
def collider_beam():
    im = frame('Anel Colisor · Comitê de Tempo de Feixe')
    display(im, 6, 17, 307, 34)
    text(im, 10, 20, '24 h do anel', GRAY)
    blocks = [(0, 7, 'green', 'Produção'), (7, 13, 'blue', 'REBCO'), (13, 19, 'purple', 'X(Nexus)'), (19, 20, 'red', 'Q'), (20, 24, 'green', 'Produção')]
    for a, b, c, l in blocks:
        x0, x1 = 10 + a * 12.4, 10 + b * 12.4
        background(im, GF + f'picture_overlay_{c}.png', int(x0), 31, int(x1 - x0) - 1, 14); text(im, int((x0 + x1) / 2), 34, l, WHITE, center=True)
    cards = [('Ímã de Nb₃Sn', 'APROVADA', GREEN, 1.0, 'blue'), ('Detector de vértice', 'EM CURSO 62%', GOLD, .62, 'purple'), ('Íons pesados', 'requer Top', RED, 0, 'red')]
    for i, (n, s, c, f, bc) in enumerate(cards):
        y = 56 + i * 39
        panel(im, 6, y, 196, 36); blit(im, CC + ('coils/machine_coil_superconductor.png' if i == 0 else 'solid/machine_casing_clean_stainless_steel.png' if i == 1 else 'solid/machine_casing_robust_tungstensteel.png'), 11, y + 9, 18, 18)
        text(im, 34, y + 6, n, DARK, shadow=False); text(im, 34, y + 17, s, c)
        bar(im, 120, y + 18, 76, f, bc)
        if i == 2: blit(im, GF + 'button_boxed_exclamation_point.png', 180, y + 4, 14, 14)
    display(im, 206, 56, 107, 115)
    for i, (n, v) in enumerate((('E feixe', '10,8 TeV'), ('B', '12 T'), ('Hélio', '84%'), ('Lumin.', '2,1e34'))):
        text(im, 211, 61 + i * 11, n, GRAY); text(im, 260, 61 + i * 11, v, WHITE)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); import PIL.ImageDraw as D_; d = D_.Draw(lay)
    d.ellipse([224, 112, 296, 164], outline=(255, 85, 255, 220), width=2); d.ellipse([230, 117, 290, 159], outline=(85, 255, 255, 220), width=2)
    im.alpha_composite(lay)
    tab_bar(im, ['Anel', 'Modelo Padrão', 'Comitê'], 2)
    save(im, OUT + '/collider_beam.png')


# ------------------------------------------------------------------ Câmara: diagrama M–P
def star_mp():
    im = frame('Câmara Estelar · Diagrama M–P')
    background(im, GF + 'background_star.png', 6, 17, 210, 120, alpha=255)
    rect(im, 6, 17, 210, 120, (0, 0, 20, 150))
    x0, x1, y0, y1 = 24, 212, 21, 128
    def X(m): return x0 + (m - 1.0) / 1.4 * (x1 - x0)
    def Y(p_ms): return y0 + (math.log10(1000) - math.log10(p_ms)) / (math.log10(1000) - math.log10(0.4)) * (y1 - y0)
    regions = [(1000, 30, (85, 120, 255, 50), 'Pulsar comum'), (30, 10, (85, 255, 120, 50), 'Recente'), (10, 1.4, (85, 200, 255, 60), 'Milissegundo'), (1.4, 0.6, (255, 200, 40, 70), 'Recordista')]
    for a, b, c, n in regions:
        rect(im, x0, int(Y(a)), int(X(2.2) - x0), int(Y(b) - Y(a)), c); text(im, x0 + 3, int(Y(a)) + 2, n, WHITE)
    rect(im, int(X(2.2)), y0, x1 - int(X(2.2)), y1 - y0, (0, 0, 0, 200)); dashed(im, (X(2.2), y0), (X(2.2), y1), (255, 85, 85, 255), 1)
    text(im, int(X(2.2)) + 3, y0 + 2, 'TOV', RED)
    pts = [(1.30, 600), (1.34, 180), (1.40, 60), (1.47, 20), (1.55, 7), (1.62, 3.8)]
    for (m1, p1), (m2, p2) in zip(pts, pts[1:]): dashed(im, (X(m1), Y(p1)), (X(m2), Y(p2)), (200, 220, 255, 220), 1, 2)
    blit(im, GF + 'button_celestial.png', int(X(1.62)) - 5, int(Y(3.8)) - 5, 10, 10)
    for m in (1.0, 1.4, 1.8, 2.2): text(im, int(X(m)), 129, f'{m:.1f}'.replace('.', ','), GRAY, center=True)
    text(im, 8, 21, 'ms', GRAY)
    # seismogram
    display(im, 6, 140, 307, 33)
    random.seed(3)
    for x in range(8, 311):
        a = random.uniform(-2, 2); a += 13 * math.exp(-((x - 120) / 4) ** 2) * math.sin(x * 2) + 5 * math.exp(-((x - 230) / 3) ** 2) * math.sin(x * 3)
        rect(im, x, int(156 - a), 1, max(1, int(abs(a) / 3)), (85, 255, 255, 255))
    text(im, 130, 143, 'Tipo Vela  ΔΩ/Ω 1,1e-6  decifrado', GOLD)
    # telemetry
    display(im, 220, 17, 93, 120)
    for i, (n, v, c) in enumerate((('M', '1,62 Msol', WHITE), ('P', '3,8 ms', WHITE), ('Erot', '1,1e25', CYAN), ('Extr.', '2^58 EU/t', GOLD), ('Bandas', '3/4', GREEN))):
        text(im, 225, 22 + i * 14, n, GRAY); text(im, 256, 22 + i * 14, v, c)
    std_button(im, 225, 96, 18, 18, GF + 'overlay_button_battery_on.png'); std_button(im, 247, 96, 18, 18, GF + 'overlay_button_heat_on.png'); std_button(im, 269, 96, 18, 18, GF + 'overlay_button_statistics.png')
    tab_bar(im, ['Estrela', 'Diagrama', 'Sismograma'], 1)
    save(im, OUT + '/star_mp.png')


# ------------------------------------------------------------------ PWR: sala de controle
def pwr_control():
    im = frame('Reator PWR · Sala de Controle')
    display(im, 6, 17, 110, 110)
    text(im, 10, 20, 'Núcleo · queima', GRAY)
    random.seed(11)
    cols = [(85, 255, 85), (170, 255, 85), (255, 255, 85), (255, 170, 40), (255, 85, 85)]
    for r in range(7):
        for c in range(7):
            if math.hypot(r - 3, c - 3) > 3.4: continue
            b = min(4, int(abs(r - 3) + abs(c - 3) + random.randint(-1, 1))) if (r + c) % 2 else random.randint(0, 2)
            x, y = 14 + c * 13, 31 + r * 13
            rect(im, x, y, 12, 12, cols[4 - max(0, min(4, b))] + (255,))
            if r % 2 and c % 2: text(im, x + 6, y + 2, '+', DARK, shadow=False, center=True)
    gauges = [('Potência', '98,2%', GREEN), ('ρ', '+4 pcm', WHITE), ('Período', '∞', WHITE), ('Pressão', '155 bar', WHITE), ('T quente', '324 °C', WHITE),
              ('DNBR', '2,05', GREEN), ('Boro', '1.180 ppm', CYAN), ('Xe', '-2.790 pcm', PURPLE)]
    for i, (n, v, c) in enumerate(gauges):
        x, y = 120 + (i % 2) * 64, 17 + (i // 2) * 27
        display(im, x, y, 62, 25); text(im, x + 3, y + 3, n, GRAY); text(im, x + 3, y + 14, v, c)
    display(im, 248, 17, 65, 110)
    text(im, 252, 20, 'Alarmes', GOLD)
    alarms = [('SCRAM', False), ('PRZ baixo', True), ('Pressão', False), ('DNBR', False), ('Bombas', False), ('Contenção', False)]
    for i, (n, on) in enumerate(alarms):
        background(im, GF + ('picture_overlay_orange.png' if on else 'picture_overlay_blue.png'), 252, 31 + i * 15, 57, 12, alpha=255 if on else 70)
        text(im, 280, 33 + i * 15, n, WHITE if on else GRAY, center=True)
    display(im, 6, 130, 200, 43)
    text(im, 10, 133, 'Bancos de barras', GRAY)
    for i, (n, v) in enumerate((('A', .12), ('B', .24), ('C', .38), ('D', .52), ('P', .68))):
        x = 12 + i * 38; text(im, x, 146, n, GOLD); rect(im, x + 8, 145, 24, 24, (40, 40, 50, 255)); rect(im, x + 8, 145, 24, int(24 * v), (255, 170, 40, 255))
        text(im, x + 20, 162, f'{int(v * 100)}%', WHITE, center=True)
    purple_button(im, 212, 132, 'AUTO', w=48, h=18, pressed=True, color=GREEN)
    purple_button(im, 263, 132, 'RECARGA', w=50, h=18)
    purple_button(im, 212, 154, 'SCRAM', w=101, h=19, color=RED)
    tab_bar(im, ['Controle', 'Núcleo', 'Química', 'Ciclo'], 0)
    save(im, OUT + '/pwr_control.png')


for fn in (lance_survey, lance_bench, rift_score, rift_atlas, collider_sm, collider_beam, star_mp, pwr_control):
    fn(); print(fn.__name__)
