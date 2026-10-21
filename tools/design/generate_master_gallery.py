#!/usr/bin/env python3
"""Master showcase generator combining the 4 chosen winners for the GTNA Unique Endgame Multiblocks:
  1. Lança Cinética Orbital (UEV) -> Aba 1 (Levantamento Orbital & Trajetórias, Botões MIRAR/AUTO/DISPARAR)
  2. Portão de Fenda Dimensional (UIV) -> Aba 1 (Vórtice Cósmico Volumétrico & Horizonte)
  3. Anel Colisor de Antimatéria (UIV) -> Aba 1 (Anel Síncrotron de 3 km & Diagnóstico do Feixe)
  4. Câmara de Contenção Estelar (MAX) -> Aba 1 (Pulsar de Milissegundo em Estado Normal, Botões [-]/[+]/[MAGNETAR])
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROPOSALS_DIR = os.path.join(BASE_DIR, 'ui_proposals')

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

def main():
    p1_path = os.path.join(PROPOSALS_DIR, 'lance', 'previews', 'preview_tab1_orbital_survey.png')
    p2_path = os.path.join(PROPOSALS_DIR, 'rift_gate', 'previews', 'preview_tab1_wormhole_vortex.png')
    p3_path = os.path.join(PROPOSALS_DIR, 'collider_ring', 'previews', 'preview_tab1_synchrotron_ring.png')
    p4_path = os.path.join(PROPOSALS_DIR, 'stellar_chamber', 'previews', 'preview_tab1_neutron_star.png')

    im1 = Image.open(p1_path)
    im2 = Image.open(p2_path)
    im3 = Image.open(p3_path)
    im4 = Image.open(p4_path)

    w, h = 640, 480
    header_h = 75
    gap = 16
    
    total_w = w * 2 + gap * 3
    total_h = header_h + h * 2 + gap * 3
    
    master = Image.new('RGBA', (total_w, total_h), (12, 10, 18, 255))
    d = ImageDraw.Draw(master)
    
    # Header Banner
    d.rectangle([0, 0, total_w, header_h], fill=(22, 16, 32, 255), outline=(65, 45, 95, 255), width=2)
    d.text((32, 16), "GTNA · GALERIA MASTER DOS 4 MULTIBLOCOS ÚNICOS — TELAS PRINCIPAIS ATUALIZADAS", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((32, 44), "Estética Godforge Cosmic Purple 100% alinhada à mecânica real do código Java (Backgrounds 512x512, Telas 640x480)", fill=(180, 190, 215, 255), font=FONT_SUB)
    
    # 2x2 Grid Placement
    # Top-Left: Lança Cinética Orbital
    x1, y1 = gap, header_h + gap
    master.paste(im1, (x1, y1))
    
    # Top-Right: Portão de Fenda Dimensional
    x2, y2 = gap * 2 + w, header_h + gap
    master.paste(im2, (x2, y2))
    
    # Bottom-Left: Anel Colisor de Antimatéria
    x3, y3 = gap, header_h + gap * 2 + h
    master.paste(im3, (x3, y3))
    
    # Bottom-Right: Câmara de Contenção Estelar
    x4, y4 = gap * 2 + w, header_h + gap * 2 + h
    master.paste(im4, (x4, y4))
    
    out_file = os.path.join(PROPOSALS_DIR, 'master_winners_showcase.png')
    master.save(out_file)
    print(f"[OK] Master gallery saved to: {out_file}")

if __name__ == '__main__':
    main()
