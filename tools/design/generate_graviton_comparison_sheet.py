#!/usr/bin/env python3
"""Generate a Side-by-Side Benchmark Poster comparing 'graviton_anomaly' with the 5 newly created Graviton-Tier Endgame Items:
  0. Graviton Anomaly (Reference Baseline from Mod)
  1. Target Cartridge (Avionics Tactical Module & Laser Reticle)
  2. Contained Particle (Cryogenic Penning Trap & Quantum Wave Rings)
  3. Rift Probe (Supersonic Needle & Rotating 3D Astrolabe Gimbals)
  4. Depth Anchor (Gravimetric Mooring Apparatus & Spacetime Ripples)
  5. Rift Singularity (Relativistic Accretion Vortex & Doppler Beaming)

Outputs to: tools/design/item_proposals/graviton_tier_comparison_benchmark.png
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(BASE_DIR, 'item_proposals')

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

FONT_HEADER = get_font(18, bold=True)
FONT_SUB = get_font(13, bold=False)
FONT_TITLE = get_font(12, bold=True)
FONT_TEXT = get_font(10, bold=False)
FONT_MICRO = get_font(9, bold=False)

def get_first_frame(path):
    im = Image.open(path)
    if getattr(im, "is_animated", False):
        im.seek(0)
    return im.convert('RGBA')

def main():
    # 0. Reference Graviton Anomaly
    grav_path = os.path.join(BASE_DIR, '../../src/main/resources/assets/gtna/textures/item/graviton_anomaly.png')
    grav_strip = Image.open(grav_path)
    grav_f0 = grav_strip.crop((0, 0, 64, 64))
    
    # 1. Target Cartridge
    tc_path = os.path.join(PROPOSALS_DIR, 'target_cartridge', 'target_cartridge_64.gif')
    tc_f0 = get_first_frame(tc_path)
    
    # 2. Contained Antiproton & Higgs
    anti_path = os.path.join(PROPOSALS_DIR, 'contained_particles', 'contained_antiproton_64.gif')
    anti_f0 = get_first_frame(anti_path)
    
    higgs_path = os.path.join(PROPOSALS_DIR, 'contained_particles', 'contained_higgs_64.gif')
    higgs_f0 = get_first_frame(higgs_path)
    
    # 3. Rift Probe
    rp_path = os.path.join(PROPOSALS_DIR, 'rift_probe', 'rift_probe_64.gif')
    rp_f0 = get_first_frame(rp_path)
    
    # 4. Depth Anchor
    da_path = os.path.join(PROPOSALS_DIR, 'depth_anchor', 'depth_anchor_64.gif')
    da_f0 = get_first_frame(da_path)
    
    # 5. Rift Singularity
    rs_path = os.path.join(PROPOSALS_DIR, 'rift_singularity', 'rift_singularity_64.gif')
    rs_f0 = get_first_frame(rs_path)

    items_data = [
        ("0. GRAVITON ANOMALY", "REFERÊNCIA DO MOD", grav_f0, (245, 120, 25), [
            "Shaders de campo de distância NumPy",
            "Disco de acreção logarítmico 3D",
            "Beaming relativístico Doppler",
            "Esfera de fótons & ondas gravitacionais",
            "16 frames animados fluidos"
        ]),
        ("1. TARGET CARTRIDGE", "LANÇA CINÉTICA (UEV)", tc_f0, (0, 240, 255), [
            "Chassi Duranium com iluminação Phong",
            "Retículo holográfico rotativo ciano",
            "Varredura radar contínua 360°",
            "Contatos dourados PCB & LEDs de status",
            "Vidro especular curvado com glare"
        ]),
        ("2. CONTAINED PARTICLE", "ANEL COLISOR (UIV)", anti_f0, (0, 240, 255), [
            "Eletrodo quadrupolo toroidal usinado",
            "Tubo de quartzo a vácuo com duplo glare",
            "Anéis giroscópicos de onda quântica",
            "Descargas de arco elétrico nos polos",
            "Núcleo subatômico incandescente"
        ]),
        ("3. RIFT PROBE", "PORTÃO DE FENDA (UIV)", rp_f0, (180, 80, 255), [
            "Fuselagem supersônica agulha cônica",
            "Anéis cardânicos de astrolábio 3D",
            "Ondas de choque de fase taquiônica",
            "Pluma de propulsão iônica turbulenta",
            "Núcleo cronon ultravioleta pulsante"
        ]),
        ("4. DEPTH ANCHOR", "PORTÃO DE FENDA (UIV)", da_f0, (255, 215, 80), [
            "Haste pesada com chanfros especulares",
            "Ondas gravitacionais irradiando da coroa",
            "Pás de fenda com corte de fase taquion",
            "Micro-singularidade de trava espacial",
            "Anéis de fluxo quântico pulsantes"
        ]),
        ("5. RIFT SINGULARITY", "PORTÃO DE FENDA (UIV/MAX)", rs_f0, (220, 50, 255), [
            "Rival direto do Graviton Anomaly",
            "Espiral de acreção com micro-turbulência",
            "Beaming relativístico assimétrico",
            "Fissuras de relâmpago dimensional",
            "Horizonte de eventos negro absoluto"
        ]),
    ]

    sw, sh = 1260, 680
    sheet = Image.new('RGBA', (sw, sh), (12, 8, 20, 255))
    d = ImageDraw.Draw(sheet)
    
    # Top Header
    d.rectangle([0, 0, sw, 75], fill=(22, 14, 34, 255), outline=(75, 45, 105, 255), width=2)
    d.text((30, 16), "GTNA · BENCHMARK DE QUALIDADE: GRAVITON ANOMALY vs ITENS ENDGAME RECRIADOS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((30, 44), "Todos os 5 itens recriados com o mesmo motor matemático de shaders NumPy, iluminação Phong e física relativística (64x64 HD, 16 frames)", fill=(180, 190, 215, 255), font=FONT_SUB)
    
    col_w = (sw - 40) // 6
    for idx, (iname, isub, if0, icol, ispecs) in enumerate(items_data):
        cx = 20 + idx * col_w
        cy = 90
        cw = col_w - 10
        ch = sh - 110
        
        # Container
        is_ref = (idx == 0)
        border_col = (255, 120, 30, 255) if is_ref else (65, 45, 90, 255)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=(18, 12, 28, 255), outline=border_col, width=2 if is_ref else 1)
        
        # Header strip
        d.rectangle([cx + 2, cy + 2, cx + cw - 2, cy + 34], fill=(28, 16, 44, 255))
        d.text((cx + 6, cy + 6), iname, fill=(255, 215, 80, 255) if not is_ref else (255, 160, 50, 255), font=FONT_MICRO)
        d.text((cx + 6, cy + 20), isub, fill=icol + (255,), font=FONT_MICRO)
        
        # 2.5x enlarged preview box (160x160)
        box_size = 160
        bx = cx + (cw - box_size) // 2
        by = cy + 44
        d.rectangle([bx, by, bx + box_size, by + box_size], fill=(8, 5, 14, 255), outline=(50, 35, 70, 255), width=2)
        
        # Resize nearest neighbor (pixel-perfect 2.5x)
        enlarged = if0.resize((150, 150), Image.NEAREST)
        sheet.paste(enlarged, (bx + 5, by + 5), enlarged)
        
        # 1x native 64x64 preview box
        nat_y = by + box_size + 14
        d.rectangle([bx, nat_y, bx + 68, nat_y + 68], fill=(8, 5, 14, 255), outline=(50, 35, 70, 255))
        sheet.paste(if0, (bx + 2, nat_y + 2), if0)
        
        d.text((bx + 74, nat_y + 4), "64x64 HD", fill=(0, 240, 255, 255), font=FONT_MICRO)
        d.text((bx + 74, nat_y + 18), "16 Frames", fill=(255, 215, 80, 255), font=FONT_MICRO)
        d.text((bx + 74, nat_y + 32), "NumPy Shaders", fill=(180, 190, 210, 255), font=FONT_MICRO)
        d.text((bx + 74, nat_y + 46), "Doppler/SDF", fill=(80, 255, 140, 255), font=FONT_MICRO)
        
        # Specs list
        spec_y = nat_y + 76
        d.line([(cx + 8, spec_y), (cx + cw - 8, spec_y)], fill=(50, 35, 70, 255))
        for s_idx, spec in enumerate(ispecs):
            sy = spec_y + 8 + s_idx * 16
            if sy + 14 < cy + ch:
                d.text((cx + 6, sy), f"• {spec}", fill=(200, 210, 230, 255), font=FONT_MICRO)
                
    out_file = os.path.join(PROPOSALS_DIR, 'graviton_tier_comparison_benchmark.png')
    sheet.save(out_file)
    print(f"[OK] Benchmark sheet saved to: {out_file}")

if __name__ == '__main__':
    main()
