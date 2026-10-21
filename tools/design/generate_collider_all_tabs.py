#!/usr/bin/env python3
"""Generate all 3 tabs for GTNA Multiblock 3: Anel Colisor de Antimatéria (Antimatter Collider Ring - UIV):
  - Tab 1: Anel de Feixe & Colisão (Synchrotron Ring, RF Cavities & Luminosity)
  - Tab 2: Quadro de Partículas do Colisor (EXACTLY the 10 particles from ColliderCore.java in 5x2 grid matching OriginalsGui.standardModel)
  - Tab 3: Comitê de Tempo de Feixe (EXACTLY the 9 proposals from ColliderCore.Proposal matching OriginalsGui.committee)

Buttons match ColliderRingMachine.java:
  - [MODO: FÍSICA / PRODUÇÃO] (mode)

Outputs to: tools/design/ui_proposals/collider_ring/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'collider_ring')
BG_DIR = os.path.join(OUT_DIR, 'backgrounds')
BTN_DIR = os.path.join(OUT_DIR, 'buttons')
ICO_DIR = os.path.join(OUT_DIR, 'icons')
BAR_DIR = os.path.join(OUT_DIR, 'progressbars')
PREV_DIR = os.path.join(OUT_DIR, 'previews')

os.makedirs(BG_DIR, exist_ok=True)
os.makedirs(BTN_DIR, exist_ok=True)
os.makedirs(ICO_DIR, exist_ok=True)
os.makedirs(BAR_DIR, exist_ok=True)
os.makedirs(PREV_DIR, exist_ok=True)

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

FONT_HEADER = get_font(15, bold=True)
FONT_SUB = get_font(12, bold=False)
FONT_PANEL = get_font(11, bold=True)
FONT_TEXT = get_font(10, bold=False)
FONT_BTN = get_font(10, bold=True)
FONT_MICRO = get_font(9, bold=False)

def generate_fbm_noise(w, h, octaves=7, persistence=0.55, lacunarity=2.0, seed=42):
    rng = np.random.default_rng(seed)
    grid = np.zeros((h, w), dtype=np.float32)
    amplitude, total_amp = 1.0, 0.0
    for oct_idx in range(octaves):
        freq = int(4 * (lacunarity ** oct_idx))
        if freq >= min(w, h): break
        sub_h = max(3, int(h / (lacunarity ** (octaves - 1 - oct_idx))))
        sub_w = max(3, int(w / (lacunarity ** (octaves - 1 - oct_idx))))
        noise_small = rng.uniform(0.0, 1.0, (sub_h, sub_w)).astype(np.float32)
        im_noise = Image.fromarray(noise_small).resize((w, h), Image.BICUBIC)
        grid += np.array(im_noise) * amplitude
        total_amp += amplitude
        amplitude *= persistence
    return grid / total_amp

def color_ramp(values, stops):
    h, w = values.shape
    out = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        mask = (values >= p0) & (values <= p1)
        if not np.any(mask): continue
        t = ((values[mask] - p0) / (p1 - p0))[:, np.newaxis]
        out[mask] = np.array(c0, dtype=np.float32) + (np.array(c1, dtype=np.float32) - np.array(c0, dtype=np.float32)) * t
    out[values < stops[0][0]] = np.array(stops[0][1], dtype=np.float32)
    out[values > stops[-1][0]] = np.array(stops[-1][1], dtype=np.float32)
    return np.clip(out, 0, 255).astype(np.uint8)

# The 10 particles from ColliderCore.Particle
COLLIDER_PARTICLES = [
    ("ANTIPROTON", "Antipróton", 5.6, 50.0, 5.0, (80, 255, 140)),     # Discovered
    ("KAON", "Káon", 1.0, 30.0, 5.0, (80, 255, 140)),                # Discovered
    ("LAMBDA", "Lambda", 2.5, 8.0, 5.0, (80, 255, 140)),              # Discovered
    ("CHARM", "Quark Charm", 10.0, 4.0, 5.0, (80, 255, 140)),         # Discovered
    ("BOTTOM", "Quark Bottom", 40.0, 1.5, 5.0, (80, 255, 140)),       # Discovered
    ("W_BOSON", "Bóson W", 161.0, 0.6, 5.0, (80, 255, 140)),          # Discovered
    ("Z_BOSON", "Bóson Z", 182.0, 0.8, 5.0, (80, 255, 140)),          # Discovered
    ("HIGGS", "Bóson Higgs", 250.0, 0.08, 4.8, (255, 215, 80)),       # Evidence 4.8 sigma
    ("TOP", "Quark Top", 346.0, 0.15, 3.2, (255, 215, 80)),           # Evidence 3.2 sigma
    ("X_NEXUS", "X-Nexus", 4800.0, 0.02, 1.4, (140, 150, 170)),       # Search 1.4 sigma
]

# The 9 proposals from ColliderCore.Proposal
COLLIDER_PROPOSALS = [
    # ColliderCore.proposalMet: what each one asks for (shown instead of a fb⁻¹ total)
    ("NB3SN_MAGNET", "Ímã Nb3Sn (12 T)", "CONCLUÍDA", "5 fb⁻¹ e 7 TeV", 1.0, (80, 255, 140)),
    ("VERTEX_DETECTOR", "Detector de vértice", "CONCLUÍDA", "charm 5σ", 1.0, (80, 255, 140)),
    ("STOCHASTIC_COOLING", "Resfriamento estocástico", "CONCLUÍDA", "20 fb⁻¹", 1.0, (80, 255, 140)),
    ("CRYO_PENNING", "Armadilhas Penning criogênicas", "ATIVA", "1e13 p̄ ou 40 fb⁻¹", 0.71, (255, 215, 80)),
    ("REBCO_MAGNET", "Ímã REBCO (20 T)", "NA FILA", "W e Z 5σ", 0.0, (0, 240, 255)),
    ("LEPTON_COLLIDER", "Colisor de léptons", "NA FILA", "bottom 5σ", 0.0, (0, 240, 255)),
    ("HEAVY_IONS", "Íons pesados", "NA FILA", "top 5σ", 0.0, (140, 150, 170)),
    ("NEUTRONIUM_MAGNET", "Ímã de neutrônio (45 T)", "NA FILA", "Higgs 5σ", 0.0, (140, 150, 170)),
    ("BEYOND_STANDARD_MODEL", "Além do Modelo Padrão", "NA FILA", "X-Nexus 3σ", 0.0, (140, 150, 170)),
]

# ===========================================================================
# TAB 2: QUADRO DE PARTÍCULAS DO COLISOR (5x2 GRID MATCHING ORIGINAL CODE)
# ===========================================================================
def generate_bg_tab2_standard_model(w=512, h=512, clean=False):
    """5x2 Grid showing EXACTLY the 10 GTNA ColliderCore particles matching OriginalsGui.standardModel:
    Antiproton, Kaon, Lambda, Charm, Bottom, W-Boson, Z-Boson, Higgs, Top, X-Nexus.
    Shows threshold GeV, sigma discovery bar (up to 5.0 sigma) and golden status."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=3202)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 4, 16)),
        (0.35, (24, 10, 44)),
        (0.65, (55, 18, 88)),
        (0.85, (0, 210, 245)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "ANEL COLISOR · MATRIZ DAS 10 PARTÍCULAS (ORIGINALSGUI)", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 190, 26), "LIMIAR: 5.0 σ (DESCOBERTA DOURADA)", fill=(255, 215, 80, 240), font=FONT_MICRO)

    # 5 Columns x 2 Rows Grid matching OriginalsGui.standardModel
    grid_y = 48
    grid_h = h - grid_y - 30
    cols = 5
    rows = 2
    cw = (w - 56) // cols
    rh = (grid_h - 10) // rows
    
    for idx, (p_id, p_name, p_gev, p_sec, p_sig, p_col) in enumerate(COLLIDER_PARTICLES):
        c = idx % cols
        r = idx // cols
        px = 28 + c * cw + 2
        py = grid_y + r * rh + 2
        box_w = cw - 4
        box_h = rh - 4
        
        # Particle Box Container
        bg_alpha = 40 if p_sig >= 5.0 else 25
        d.rectangle([px, py, px + box_w, py + box_h], fill=(p_col[0] // 5, p_col[1] // 5, p_col[2] // 5, 230),
                    outline=p_col + (220,), width=1 if p_sig < 5.0 else 2)
                    
        # Header strip inside box
        d.rectangle([px + 1, py + 1, px + box_w - 1, py + 22], fill=(22, 14, 36, 255))
        
        if not clean:
            # Particle Name
            d.text((px + 6, py + 4), p_name, fill=(255, 255, 255, 255), font=FONT_MICRO)
            # Energy Threshold
            d.text((px + 6, py + 26), f"{p_gev:.1f} GeV" if p_gev < 1000 else f"{p_gev/1000:.1f} TeV",
                   fill=(180, 190, 210, 255), font=FONT_MICRO)
            # Cross Section
            d.text((px + 6, py + 38), f"σ: {p_sec} pb", fill=(140, 150, 170, 255), font=FONT_MICRO)
            
            # Significance text and bar (up to 5.0 sigma)
            sig_col = (80, 255, 140) if p_sig >= 5.0 else (255, 215, 80) if p_sig >= 3.0 else (140, 150, 170)
            d.text((px + 6, py + box_h - 26), f"{p_sig:.2f} σ", fill=sig_col + (255,), font=FONT_MICRO)
            
            # Progress bar
            bar_y = py + box_h - 14
            bar_w = box_w - 12
            d.rectangle([px + 6, bar_y, px + 6 + bar_w, bar_y + 6], fill=(12, 8, 20, 255), outline=(50, 40, 70, 255))
            filled_w = int(bar_w * (min(5.0, p_sig) / 5.0))
            if filled_w > 0:
                d.rectangle([px + 7, bar_y + 1, px + 6 + filled_w, bar_y + 5], fill=sig_col + (255,))
                
            # Discovered Badge if >= 5.0 sigma
            if p_sig >= 5.0:
                d.text((px + box_w - 20, py + 4), "★", fill=(255, 215, 80, 255), font=FONT_MICRO)
                
    return im

# ===========================================================================
# TAB 3: COMITÊ DE TEMPO DE FEIXE (9 PROPOSALS MATCHING ORIGINAL CODE)
# ===========================================================================
def generate_bg_tab3_beam_committee(w=512, h=512, clean=False):
    """9 Beam-Time Committee Proposals matching ColliderCore.Proposal:
    Nb3Sn Magnet, Vertex Detector, Stochastic Cooling, Cryo Penning, REBCO Magnet,
    Lepton Collider, Heavy Ions, Neutronium Magnet, Beyond Standard Model.
    Shows progress bars, approval state, and beam delivery fb^-1."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=3303)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (6, 4, 16)),
        (0.35, (24, 10, 44)),
        (0.65, (55, 18, 88)),
        (0.85, (0, 210, 245)),
        (1.00, (255, 255, 255))
    ]
    rgb = color_ramp(lum, stops)
    im = Image.fromarray(rgb, 'RGB').convert('RGBA')
    d = ImageDraw.Draw(im)
    
    # Outer Tech Frame
    d.rectangle([20, 20, w - 20, h - 20], outline=(140, 70, 210, 140), width=1)
    d.rectangle([22, 22, w - 22, h - 22], outline=(0, 240, 255, 60), width=1)
    
    if not clean:
        d.text((28, 26), "COMITÊ DE TEMPO DE FEIXE · AS 9 PROPOSTAS (COLLIDERCORE)", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 190, 26), "PROPOSTA ATIVA: 4/9", fill=(255, 215, 80, 240), font=FONT_MICRO)

    # Upper Section: 4 Cryogenic Penning Traps Status
    traps_y = 48
    trap_w = (w - 68) // 4
    trap_h = 75
    
    trap_data = [
        # One Penning trap pool (ColliderCore.antiprotons / trapCapacity), its upkeep and the helium plant.
        ("PENNING T1", "Antiprótons", "8,4e11 / 1e12", 0.84, (80, 255, 140)),
        ("CÉLULAS", "Saída 1e11 cada", "12 no bus", 0.60, (0, 240, 255)),
        ("MANUTENÇÃO", "Armadilhas", "2^21 EU/t", 1.00, (255, 215, 80)),
        ("HÉLIO", "Líquido 1 L/s", "100%", 1.00, (80, 255, 140)),
    ]
    for idx, (tname, tcontent, tfill_txt, tfill_val, tcol) in enumerate(trap_data):
        tx = 28 + idx * (trap_w + 4)
        d.rectangle([tx, traps_y, tx + trap_w, traps_y + trap_h], fill=(12, 8, 22, 230), outline=(75, 40, 115, 255), width=1)
        d.rectangle([tx + 1, traps_y + 1, tx + trap_w - 1, traps_y + 18], fill=(22, 14, 36, 255))
        if not clean:
            d.text((tx + 6, traps_y + 4), tname, fill=(255, 215, 80, 255), font=FONT_MICRO)
            d.text((tx + 6, traps_y + 24), tcontent, fill=(255, 255, 255, 255), font=FONT_MICRO)
            d.text((tx + 6, traps_y + 38), tfill_txt, fill=tcol + (255,), font=FONT_MICRO)
            
            # Progress bar
            bar_y_pos = traps_y + trap_h - 14
            d.rectangle([tx + 6, bar_y_pos, tx + trap_w - 6, bar_y_pos + 6], fill=(18, 12, 28, 255), outline=(50, 40, 70, 255))
            d.rectangle([tx + 7, bar_y_pos + 1, tx + 7 + int((trap_w - 14) * tfill_val), bar_y_pos + 5], fill=tcol + (255,))

    # Lower Section: 9 Proposals Table matching ColliderCore.Proposal
    sched_y = traps_y + trap_h + 10
    sched_h = h - sched_y - 25
    d.rectangle([28, sched_y, w - 28, sched_y + sched_h], fill=(12, 8, 22, 240), outline=(75, 40, 115, 255), width=2)
    
    if not clean:
        d.text((38, sched_y + 8), "COMITÊ DE TEMPO DE FEIXE · 9 PROPOSTAS", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
        # Table Header
        th_y = sched_y + 24
        d.text((38, th_y), "#", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((60, th_y), "PROPOSTA DE FEIXE", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((230, th_y), "PEDE", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((395, th_y), "ESTADO", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.line([(34, th_y + 12), (w - 34, th_y + 12)], fill=(60, 45, 85, 200), width=1)
        
        row_gap = (sched_h - 48) // len(COLLIDER_PROPOSALS)
        for r_idx, (pid, pname, pstat, pprog, pmax, pcol) in enumerate(COLLIDER_PROPOSALS):
            ry = th_y + 14 + r_idx * row_gap
            if ry + 12 < sched_y + sched_h:
                d.text((38, ry), f"{r_idx + 1}", fill=(255, 215, 80, 255), font=FONT_MICRO)
                d.text((60, ry), pname, fill=(255, 255, 255, 255) if pmax > 0 else (160, 170, 190, 255), font=FONT_MICRO)
                
                # Progress bar & numbers
                d.text((230, ry), pprog, fill=(0, 240, 255, 255), font=FONT_MICRO)
                bar_x = 330
                bar_w = 55
                d.rectangle([bar_x, ry + 2, bar_x + bar_w, ry + 8], fill=(16, 10, 25, 255), outline=(50, 35, 70, 255))
                if pmax > 0:
                    fill_w = int(bar_w * min(1.0, pmax))
                    d.rectangle([bar_x + 1, ry + 3, bar_x + fill_w, ry + 7], fill=pcol + (255,))
                    
                d.text((395, ry), pstat, fill=pcol + (255,), font=FONT_MICRO)
                
    return im

# ===========================================================================
# PREVIEWS & TAB OVERVIEW SHEET
# ===========================================================================
def compose_preview_collider(bg_img, active_tab_idx, title, palette_desc):
    canvas = Image.new('RGBA', (640, 480), (10, 8, 16, 255))
    d = ImageDraw.Draw(canvas)
    
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(75, 45, 105, 255), width=2)
    
    # Header with title
    d.rectangle([16, 12, 624, 40], fill=(24, 16, 36, 255), outline=(70, 45, 95, 255))
    d.text((24, 18), f"GTNA · ANEL COLISOR DE ANTIMATÉRIA [UIV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 12, 28, 255), outline=(60, 40, 85, 255), width=2)
    
    d.text((panel_x + 10, panel_y + 12), "DIAGNÓSTICO DO FEIXE", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(65, 45, 90, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Ímã: Nb3Sn (12.0 T)", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Energia E_cm: 21.6 TeV", fill=(255, 215, 80, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Luminosidade: 1.45e34", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Hélio Líquido: 100% [OK]", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['synchrotron_ring', 'particle_detector', 'penning_trap', 'beam_dump']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "RAMP DE ENERGIA (100%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_lumi_path = os.path.join(BAR_DIR, 'progressbar_luminosity.png')
    if os.path.exists(pbar_lumi_path):
        pbar_l = Image.open(pbar_lumi_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_l, (panel_x + 10, panel_y + 160), pbar_l)
        
    d.text((panel_x + 10, panel_y + 180), "ARMADILHAS PENNING (84%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_trap_path = os.path.join(BAR_DIR, 'progressbar_penning_storage.png')
    if os.path.exists(pbar_trap_path):
        pbar_t = Image.open(pbar_trap_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar_t, (panel_x + 10, panel_y + 196), pbar_t)
    
    d.text((panel_x + 10, panel_y + 220), "ESTADO: FEIXE ESTÁVEL", fill=(80, 255, 140, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "Detector: instalado", fill=(0, 240, 255, 255), font=FONT_TEXT)
    
    # Action buttons matching ColliderRingMachine.java:
    # [MODO: FÍSICA] or [MODO: PRODUÇÃO]
    btn_n_path = os.path.join(BTN_DIR, 'btn_cosmic_normal.png')
    btn_p_path = os.path.join(BTN_DIR, 'btn_cosmic_pressed.png')
    if os.path.exists(btn_n_path):
        btn_n = Image.open(btn_n_path).resize((74, 28), Image.NEAREST)
        btn_p = Image.open(btn_p_path).resize((154, 32), Image.NEAREST)
        
        # Mode switch button
        canvas.paste(btn_p, (panel_x + 10, panel_y + 266), btn_p)
        d.text((panel_x + 22, panel_y + 274), "[MODO: FÍSICA]", fill=(255, 220, 100, 255), font=FONT_BTN)
        
        # Beam dump and helium are status chips (not buttons): installed / supplied
        canvas.paste(btn_n, (panel_x + 10, panel_y + 306), btn_n)
        d.text((panel_x + 16, panel_y + 314), "DUMP ✓", fill=(80, 255, 140, 255), font=FONT_BTN)
        canvas.paste(btn_n, (panel_x + 90, panel_y + 306), btn_n)
        d.text((panel_x + 96, panel_y + 314), "HÉLIO OK", fill=(0, 240, 255, 255), font=FONT_BTN)

    # Tab Bar on Bottom Left
    tab_labels = ["1. FEIXE & ANEL", "2. AS 10 PARTÍCULAS", "3. COMITÊ (9 PROPOSTAS)"]
    for i, tlab in enumerate(tab_labels):
        tx = 20 + i * 136
        ty = 390
        is_active = (i == active_tab_idx)
        btn_img = Image.open(btn_p_path if is_active else btn_n_path).resize((130, 26), Image.NEAREST)
        canvas.paste(btn_img, (tx, ty), btn_img)
        tcol = (255, 215, 80) if is_active else (180, 190, 210)
        d.text((tx + 4, ty + 6), tlab, fill=tcol + (255,), font=FONT_MICRO)

    d.text((16, 442), f"Aba Ativa: {title} · {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho Background: 512x512 · Fiel a ColliderCore.java & OriginalsGui.java", fill=(100, 110, 130, 255), font=FONT_TEXT)
    return canvas

def main():
    print(">>> Gerando todas as 3 abas corrigidas para o Anel Colisor de Antimatéria (UIV)...")
    
    # Load Tab 1 background
    bg_tab1_path = os.path.join(BG_DIR, 'bg_variation_1_accelerator_512.png')
    bg_tab1 = Image.open(bg_tab1_path)
    
    print("  -> Gerando Aba 2: Quadro das 10 Partículas do ColliderCore (512x512 & Clean)...")
    bg_tab2 = generate_bg_tab2_standard_model(512, 512, clean=False)
    bg_tab2.save(os.path.join(BG_DIR, 'bg_tab2_standard_model_512.png'))
    bg_tab2_clean = generate_bg_tab2_standard_model(512, 512, clean=True)
    bg_tab2_clean.save(os.path.join(BG_DIR, 'bg_tab2_standard_model_clean.png'))
    
    print("  -> Gerando Aba 3: Comitê de Feixe com as 9 Propostas (512x512 & Clean)...")
    bg_tab3 = generate_bg_tab3_beam_committee(512, 512, clean=False)
    bg_tab3.save(os.path.join(BG_DIR, 'bg_tab3_beam_committee_512.png'))
    bg_tab3_clean = generate_bg_tab3_beam_committee(512, 512, clean=True)
    bg_tab3_clean.save(os.path.join(BG_DIR, 'bg_tab3_beam_committee_clean.png'))
    
    print("  -> Montando Telas de Preview das 3 Abas...")
    prev_tab1 = compose_preview_collider(bg_tab1, 0, "Aba 1: Feixe & Anel", "Anel Síncrotron de 3 km, Cavidades RF & Luminosidade")
    prev_tab1.save(os.path.join(PREV_DIR, 'preview_tab1_synchrotron_ring.png'))
    
    prev_tab2 = compose_preview_collider(bg_tab2, 1, "Aba 2: As 10 Partículas", "As 10 Partículas de ColliderCore.java em Grid 5x2 (5.0σ)")
    prev_tab2.save(os.path.join(PREV_DIR, 'preview_tab2_standard_model.png'))
    
    prev_tab3 = compose_preview_collider(bg_tab3, 2, "Aba 3: Comitê de Feixe", "As 9 Propostas de ColliderCore.Proposal & Cronograma")
    prev_tab3.save(os.path.join(PREV_DIR, 'preview_tab3_beam_committee.png'))
    
    # Combined Tabs Overview Sheet
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 8, 18, 255))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, sheet.width, 60], fill=(24, 14, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 14), "GTNA · ANEL COLISOR DE ANTIMATÉRIA [UIV] — VISÃO COMPLETA DAS 3 ABAS NAVEGÁVEIS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "Aba 1: Feixe & Anel · Aba 2: As 10 Partículas (Grid 5x2) · Aba 3: As 9 Propostas (Botão [MODO])", fill=(180, 190, 210, 255), font=FONT_SUB)
    sheet.paste(prev_tab1, (10, 75))
    sheet.paste(prev_tab2, (sw + 20, 75))
    sheet.paste(prev_tab3, (sw * 2 + 30, 75))
    sheet.save(os.path.join(OUT_DIR, 'tabs_overview.png'))
    print(f"[OK] Abas do Colisor geradas com sucesso em: {OUT_DIR}")

if __name__ == '__main__':
    main()
