#!/usr/bin/env python3
"""Generate all 3 tabs for GTNA Multiblock 1: Lança Cinética Orbital (Kinetic Orbital Lance - UEV Tier):
  - Tab 1: Levantamento & Mira Orbital (Target Trajectory & Orbital Map - Approved Winner 1)
  - Tab 2: Bancada de Customização do Cano (Blueprint, Coils & Thermal Balance matching OriginalsGui.bench)
  - Tab 3: Fila de Cápsulas de Carga & Reentrada (Capsule Recovery Timeline & Suborbital Logistics)

Controls match LanceMachine.java (revised 2026-10-15 against the code):
  - [ALVO ▸] cycles the targetable bodies (in the text panel a body is picked by clicking it)
  - [AUTO: ON / OFF] auto-fire toggle; a shot fires the whole bank once it is full (there is no manual fire)
  - values below come from LanceCore with a full 4e12 EU bank, 4 CuNb rails (η 0.41), tungsten 50 kg.

Outputs to: tools/design/ui_proposals/lance/
"""

import math
import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'ui_proposals', 'lance')
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

# ===========================================================================
# TAB 2: BANCADA DE CUSTOMIZAÇÃO DO CANO (BLUEPRINT & BENCH)
# ===========================================================================
def generate_bg_tab2_cannon_bench(w=512, h=512, clean=False):
    """Heavy railgun barrel schematic, modular slot sockets matching OriginalsGui.bench."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=1202)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (8, 6, 16)),
        (0.35, (25, 12, 45)),
        (0.65, (55, 20, 85)),
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
        d.text((28, 26), "BANCADA DO CANO (ABA BENCH)", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 150, 26), "BANCADA VÁLIDA", fill=(80, 255, 140, 240), font=FONT_MICRO)

    # Upper Half: Longitudinal Section Blueprint of the Lance Barrel
    bp_y = 48
    bp_h = 190
    d.rectangle([28, bp_y, w - 28, bp_y + bp_h], fill=(12, 8, 22, 230), outline=(75, 40, 115, 255), width=2)
    
    # Grid lines inside blueprint
    for gy in range(bp_y + 20, bp_y + bp_h, 25):
        d.line([(30, gy), (w - 30, gy)], fill=(40, 25, 60, 140), width=1)
    for gx in range(48, w - 28, 40):
        d.line([(gx, bp_y + 2), (gx, bp_y + bp_h - 2)], fill=(40, 25, 60, 140), width=1)
        
    # Central Railgun Bore (Longitudinal)
    bore_cy = bp_y + bp_h // 2
    d.rectangle([35, bore_cy - 14, w - 35, bore_cy + 14], fill=(20, 15, 30, 255), outline=(130, 95, 175, 255), width=2)
    d.line([(35, bore_cy), (w - 35, bore_cy)], fill=(0, 240, 255, 200), width=1)
    
    # Superconducting Magnetic Acceleration Coils (Segments along barrel)
    coil_x_start = 55
    coil_w = 26
    coil_gap = 18
    for i in range(4):
        cx = coil_x_start + i * (coil_w + coil_gap)
        if cx + coil_w < w - 40:
            d.rectangle([cx, bore_cy - 36, cx + coil_w, bore_cy - 16], fill=(255, 215, 80, 220), outline=(255, 255, 255, 255))
            d.rectangle([cx, bore_cy + 16, cx + coil_w, bore_cy + 36], fill=(255, 215, 80, 220), outline=(255, 255, 255, 255))
            for ly in range(bore_cy - 34, bore_cy - 18, 4):
                d.line([(cx + 2, ly), (cx + coil_w - 2, ly)], fill=(140, 95, 25, 255), width=1)
            for ly in range(bore_cy + 18, bore_cy + 34, 4):
                d.line([(cx + 2, ly), (cx + coil_w - 2, ly)], fill=(140, 95, 25, 255), width=1)
                
    if not clean:
        d.text((45, bp_y + 10), "PERFIL DO CANO: 4× TRILHOS CuNb · LINER DE CARBETO DE TUNGSTÊNIO", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((45, bp_y + bp_h - 18), "MASSA 170/800 t · CALOR 14/60 · INDUTÂNCIA 4/8 · EF. 41%", fill=(80, 255, 140, 255), font=FONT_MICRO)

    # Lower Half: Modular Component Fitting Sockets matching LanceCore.Component
    box_y = bp_y + bp_h + 12
    box_h = h - box_y - 20
    d.rectangle([28, box_y, w - 28, box_y + box_h], fill=(12, 8, 22, 240), outline=(75, 40, 115, 255), width=2)
    
    if not clean:
        d.text((38, box_y + 8), "COMPONENTES INSTALADOS NO CANO (LANCECORE.COMPONENT)", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
        # LanceCore.Component: slot, effect, mass (t), heat; locked ones need the body surveyed first.
        components = [
            ("▣ RAIL_CU_NB ×4", "Trilho de cobre-nióbio", "ef. +2% · 40 t", (80, 255, 140)),
            ("▣ SENSOR_TELESCOPE", "Telescópio de mira (Lua)", "erro ×0,7 · 10 t", (80, 255, 140)),
            ("□ RAIL_SUPERCONDUCTOR", "Trilho supercondutor", "requer Fobos", (140, 150, 170)),
            ("□ COOLING_HELIUM", "Resfriamento a hélio", "requer Ceres", (140, 150, 170)),
            ("□ CAPSULE_ABLATIVE", "Cápsula ablativa (75%)", "requer Ceres", (140, 150, 170)),
            ("□ SALVO_SPLITTER", "Divisor de salva (×2)", "requer Vesta", (140, 150, 170)),
        ]
        
        row_gap = (box_h - 40) // 3
        col_w = (w - 76) // 2
        for idx, (cname, cdesc, cspec, ccol) in enumerate(components):
            r = idx % 3
            c = idx // 3
            cx = 38 + c * (col_w + 12)
            cy = box_y + 28 + r * row_gap
            d.rectangle([cx, cy, cx + col_w, cy + row_gap - 6], fill=(18, 12, 28, 240), outline=(60, 40, 85, 255))
            d.text((cx + 8, cy + 4), cname, fill=ccol + (255,), font=FONT_MICRO)
            d.text((cx + 8, cy + 18), cdesc, fill=(180, 190, 210, 255), font=FONT_MICRO)
            d.text((cx + col_w - 110, cy + 4), cspec, fill=(255, 215, 80, 255), font=FONT_MICRO)
            
    return im

# ===========================================================================
# TAB 3: FILA DE CÁPSULAS DE CARGA (REENTRY TIMELINE & CAPSULES)
# ===========================================================================
def generate_bg_tab3_capsule_queue(w=512, h=512, clean=False):
    """Suborbital capsule telemetry, re-entry timeline and ME extraction buffer."""
    n_base = generate_fbm_noise(w, h, octaves=6, persistence=0.55, seed=1303)
    y, x = np.ogrid[:h, :w]
    lum = np.clip(n_base * 0.35 + 0.1, 0.0, 1.0)
    
    stops = [
        (0.00, (8, 6, 16)),
        (0.35, (25, 12, 45)),
        (0.65, (55, 20, 85)),
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
        d.text((28, 26), "LOGÍSTICA DE REENTRADA · FILA DE CÁPSULAS RECUPERADAS", fill=(0, 240, 255, 240), font=FONT_MICRO)
        d.text((w - 160, 26), "SAÍDA: OUTPUT BUS", fill=(80, 255, 140, 240), font=FONT_MICRO)

    # Upper Section: Suborbital Trajectory & Re-Entry Corridor
    corridor_y = 48
    corridor_h = 160
    d.rectangle([28, corridor_y, w - 28, corridor_y + corridor_h], fill=(12, 8, 22, 230), outline=(75, 40, 115, 255), width=2)
    
    # Planetary Atmospheric Layers
    d.line([(30, corridor_y + 40), (w - 30, corridor_y + 40)], fill=(0, 240, 255, 100), width=1)
    d.line([(30, corridor_y + 90), (w - 30, corridor_y + 90)], fill=(80, 255, 140, 100), width=1)
    
    if not clean:
        d.text((36, corridor_y + 26), "EXOSFERA (VÁCUO ORBITAL)", fill=(160, 170, 190, 200), font=FONT_MICRO)
        d.text((36, corridor_y + 76), "MESOSFERA / CORREDOR DE REENTRADA HIPERSÔNICA", fill=(0, 240, 255, 200), font=FONT_MICRO)
        d.text((36, corridor_y + 126), "TROPOSFERA / ZONA DE POUSO AUTOMATIZADO", fill=(80, 255, 140, 200), font=FONT_MICRO)
        
    # Re-entry capsules along path
    capsule_pts = [
        (w - 70, corridor_y + 25, "CAP-04 (Vesta)", (255, 215, 80)),
        (w - 180, corridor_y + 55, "CAP-03 (Fobos)", (0, 240, 255)),
        (w - 290, corridor_y + 95, "CAP-02 (Lua)", (80, 255, 140)),
        (w - 410, corridor_y + 135, "CAP-01 (Lua)", (80, 255, 140)),
    ]
    for i in range(len(capsule_pts) - 1):
        d.line([(capsule_pts[i][0], capsule_pts[i][1]), (capsule_pts[i+1][0], capsule_pts[i+1][1])],
               fill=(255, 180, 50, 180), width=2)
    for cx, cy, ctag, ccol in capsule_pts:
        d.polygon([(cx - 6, cy - 4), (cx + 6, cy - 4), (cx + 4, cy + 5), (cx - 4, cy + 5)], fill=ccol + (255,))
        if not clean:
            d.text((cx - 24, cy - 14), ctag, fill=ccol + (255,), font=FONT_MICRO)

    # Lower Section: Cargo Manifest Table
    table_y = corridor_y + corridor_h + 12
    table_h = h - table_y - 20
    d.rectangle([28, table_y, w - 28, table_y + table_h], fill=(12, 8, 22, 240), outline=(75, 40, 115, 255), width=2)
    
    if not clean:
        d.text((38, table_y + 8), "CÁPSULAS EM VOO · 1 PÓ POR TONELADA AO POUSAR", fill=(255, 215, 80, 255), font=FONT_MICRO)
        
        th_y = table_y + 24
        d.text((38, th_y), "CÁPSULA", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((115, th_y), "CORPO CELESTE", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((230, th_y), "MASSA · CHEGA EM", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.text((345, th_y), "MINÉRIOS EXTRAÍDOS", fill=(140, 150, 170, 255), font=FONT_MICRO)
        d.line([(34, th_y + 12), (w - 34, th_y + 12)], fill=(60, 45, 85, 200), width=1)
        
        rows_data = [
            ("CAP-01", "Lua", "98.400 t · 12 s", "Ferro, Titânio, Alumínio, Hélio-3", (80, 255, 140)),
            ("CAP-02", "Lua", "98.400 t · 40 s", "Ferro, Titânio, Alumínio, Hélio-3", (80, 255, 140)),
            ("CAP-03", "Fobos", "164.000 t · 9 s", "Carbono, Níquel, Ferro", (0, 240, 255)),
            ("CAP-04", "Vesta", "56.200 t · 5 h 15 min", "Ferro, Magnésio, Crômio, Platina", (255, 215, 80)),
        ]
        row_gap = max(18, (table_h - 48) // len(rows_data))
        for r_idx, (cid, cbody, cweight, cores, ccol) in enumerate(rows_data):
            ry = th_y + 14 + r_idx * row_gap
            if ry + 12 < table_y + table_h:
                d.text((38, ry), cid, fill=(255, 255, 255, 255), font=FONT_MICRO)
                d.text((115, ry), cbody, fill=(255, 215, 80, 255), font=FONT_MICRO)
                d.text((230, ry), cweight, fill=(0, 240, 255, 255), font=FONT_MICRO)
                d.text((345, ry), cores, fill=ccol + (255,), font=FONT_MICRO)
                
    return im

# ===========================================================================
# PREVIEWS & TAB OVERVIEW SHEET
# ===========================================================================
def compose_preview_lance(bg_img, active_tab_idx, title, palette_desc):
    canvas = Image.new('RGBA', (640, 480), (10, 8, 16, 255))
    d = ImageDraw.Draw(canvas)
    
    vp_w, vp_h = 420, 380
    bg_cropped = bg_img.resize((vp_w, vp_h), Image.BICUBIC)
    canvas.paste(bg_cropped, (16, 50))
    d.rectangle([15, 49, 16 + vp_w, 50 + vp_h], outline=(75, 45, 105, 255), width=2)
    
    # Header with title
    d.rectangle([16, 12, 624, 40], fill=(24, 16, 36, 255), outline=(70, 45, 95, 255))
    d.text((24, 18), f"GTNA · LANÇA CINÉTICA ORBITAL [UEV] — {title.upper()}", fill=(255, 215, 80, 255), font=FONT_PANEL)
    
    # Side panel
    panel_x, panel_y, panel_w, panel_h = 446, 50, 178, 380
    d.rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], fill=(18, 12, 28, 255), outline=(60, 40, 85, 255), width=2)
    
    d.text((panel_x + 10, panel_y + 12), "STATUS DA LANÇA", fill=(200, 210, 230, 255), font=FONT_PANEL)
    d.line([(panel_x + 10, panel_y + 28), (panel_x + panel_w - 10, panel_y + 28)], fill=(65, 45, 90, 255))
    
    d.text((panel_x + 10, panel_y + 34), "Alvo: Lua (384 Mm) · 100%", fill=(255, 255, 255, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 48), "Projétil: tungstênio 50 kg", fill=(255, 215, 80, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 62), "Banco: 4,00e12 / 4,00e12 EU", fill=(160, 170, 190, 255), font=FONT_TEXT)
    d.text((panel_x + 10, panel_y + 76), "Ef. 41% · mira 1,00 · 16k CWU", fill=(80, 255, 140, 255), font=FONT_TEXT)
    
    # Load and paste icons
    ico_names = ['orbital_cannon', 'target_reticle', 'capacitor_bank', 'hypervelocity_bullet']
    for idx, iname in enumerate(ico_names):
        ipath = os.path.join(ICO_DIR, f'ico_{iname}_32.png')
        if os.path.exists(ipath):
            ico = Image.open(ipath)
            canvas.paste(ico, (panel_x + 10 + idx * 40, panel_y + 96), ico)
            
    # Progress bars
    d.text((panel_x + 10, panel_y + 144), "BANCO (100%)", fill=(200, 210, 230, 255), font=FONT_TEXT)
    pbar_path = os.path.join(BAR_DIR, 'progressbar_cosmic.png')
    if os.path.exists(pbar_path):
        pbar = Image.open(pbar_path).resize((panel_w - 20, 12), Image.NEAREST)
        canvas.paste(pbar, (panel_x + 10, panel_y + 160), pbar)
        
    d.text((panel_x + 10, panel_y + 180), "CANO 300 / 2500 K · LINER 0%", fill=(200, 210, 230, 255), font=FONT_TEXT)
    if os.path.exists(pbar_path):
        canvas.paste(pbar, (panel_x + 10, panel_y + 196), pbar)
    
    d.text((panel_x + 10, panel_y + 220), "REGIME: RELATIVÍSTICO", fill=(255, 200, 60, 255), font=FONT_PANEL)
    d.text((panel_x + 10, panel_y + 236), "v = 8.100 km/s (0,027c)", fill=(160, 220, 255, 255), font=FONT_TEXT)
    
    # Action buttons matching LanceMachine.java:
    # [MIRAR] (target cycle)
    # [AUTO: ON] (auto-fire toggle)
    # [DISPARAR] (manual fire)
    # NO "CALIBRAR"
    btn_n_path = os.path.join(BTN_DIR, 'btn_cosmic_normal.png')
    btn_p_path = os.path.join(BTN_DIR, 'btn_cosmic_pressed.png')
    if os.path.exists(btn_n_path):
        btn_n = Image.open(btn_n_path).resize((74, 28), Image.NEAREST)
        btn_p = Image.open(btn_p_path).resize((154, 32), Image.NEAREST)
        
        canvas.paste(btn_n, (panel_x + 10, panel_y + 266), btn_n)
        d.text((panel_x + 20, panel_y + 274), "ALVO ▸", fill=(255, 255, 255, 255), font=FONT_BTN)
        
        # Real auto-fire button from LanceMachine.java
        canvas.paste(btn_n, (panel_x + 90, panel_y + 266), btn_n)
        d.text((panel_x + 98, panel_y + 274), "AUTO: ON", fill=(80, 255, 140, 255), font=FONT_BTN)
        
        # No manual fire in the machine: the bank fires itself when full and auto-fire is on.
        d.text((panel_x + 10, panel_y + 310), "Dispara sozinho com o", fill=(140, 150, 170, 255), font=FONT_TEXT)
        d.text((panel_x + 10, panel_y + 324), "banco cheio (AUTO).", fill=(140, 150, 170, 255), font=FONT_TEXT)

    # Tab Bar on Bottom Left
    tab_labels = ["1. LEVANTAMENTO", "2. BANCADA DO CANO", "3. FILA DE CÁPSULAS"]
    for i, tlab in enumerate(tab_labels):
        tx = 20 + i * 136
        ty = 390
        is_active = (i == active_tab_idx)
        btn_img = Image.open(btn_p_path if is_active else btn_n_path).resize((130, 26), Image.NEAREST)
        canvas.paste(btn_img, (tx, ty), btn_img)
        tcol = (255, 215, 80) if is_active else (180, 190, 210)
        d.text((tx + 12, ty + 6), tlab, fill=tcol + (255,), font=FONT_MICRO)

    d.text((16, 442), f"Aba Ativa: {title} · {palette_desc}", fill=(140, 150, 170, 255), font=FONT_TEXT)
    d.text((16, 458), "Tamanho Background: 512x512 · Fiel a LanceMachine/LanceCore (ALVO, AUTO)", fill=(100, 110, 130, 255), font=FONT_TEXT)
    return canvas

def main():
    print(">>> Gerando todas as 3 abas corrigidas para a Lança Cinética Orbital (UEV)...")
    
    # Load Tab 1 background
    bg_tab1_path = os.path.join(BG_DIR, 'bg_variation_1_cosmic_512.png')
    bg_tab1 = Image.open(bg_tab1_path)
    
    print("  -> Gerando Aba 2: Bancada do Cano (512x512 & Clean)...")
    bg_tab2 = generate_bg_tab2_cannon_bench(512, 512, clean=False)
    bg_tab2.save(os.path.join(BG_DIR, 'bg_tab2_cannon_bench_512.png'))
    bg_tab2_clean = generate_bg_tab2_cannon_bench(512, 512, clean=True)
    bg_tab2_clean.save(os.path.join(BG_DIR, 'bg_tab2_cannon_bench_clean.png'))
    
    print("  -> Gerando Aba 3: Fila de Cápsulas (512x512 & Clean)...")
    bg_tab3 = generate_bg_tab3_capsule_queue(512, 512, clean=False)
    bg_tab3.save(os.path.join(BG_DIR, 'bg_tab3_capsule_queue_512.png'))
    bg_tab3_clean = generate_bg_tab3_capsule_queue(512, 512, clean=True)
    bg_tab3_clean.save(os.path.join(BG_DIR, 'bg_tab3_capsule_queue_clean.png'))
    
    print("  -> Montando Telas de Preview das 3 Abas...")
    prev_tab1 = compose_preview_lance(bg_tab1, 0, "Aba 1: Levantamento", "Mapa Orbital de Corpos Celestes & Trajetórias")
    prev_tab1.save(os.path.join(PREV_DIR, 'preview_tab1_orbital_survey.png'))
    
    prev_tab2 = compose_preview_lance(bg_tab2, 1, "Aba 2: Bancada do Cano", "Blueprint do Cano, Bobinas & Balanço Térmico")
    prev_tab2.save(os.path.join(PREV_DIR, 'preview_tab2_cannon_bench.png'))
    
    prev_tab3 = compose_preview_lance(bg_tab3, 2, "Aba 3: Fila de Cápsulas", "Cápsulas em voo e o que trazem")
    prev_tab3.save(os.path.join(PREV_DIR, 'preview_tab3_capsule_queue.png'))
    
    # Combined Tabs Overview Sheet
    sw, sh = 640, 480
    sheet = Image.new('RGBA', (sw * 3 + 40, sh + 90), (12, 10, 18, 255))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, sheet.width, 60], fill=(22, 16, 32, 255), outline=(65, 45, 95, 255), width=2)
    d.text((30, 14), "GTNA · LANÇA CINÉTICA ORBITAL [UEV] — VISÃO COMPLETA DAS 3 ABAS NAVEGÁVEIS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 36), "Aba 1: Levantamento · Aba 2: Bancada do Cano · Aba 3: Fila de Cápsulas (Controles ALVO e AUTO)", fill=(180, 190, 210, 255), font=FONT_SUB)
    sheet.paste(prev_tab1, (10, 75))
    sheet.paste(prev_tab2, (sw + 20, 75))
    sheet.paste(prev_tab3, (sw * 2 + 30, 75))
    sheet.save(os.path.join(OUT_DIR, 'tabs_overview.png'))
    print(f"[OK] Abas da Lança geradas com sucesso em: {OUT_DIR}")

if __name__ == '__main__':
    main()
