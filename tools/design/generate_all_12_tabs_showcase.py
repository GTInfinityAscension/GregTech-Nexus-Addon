#!/usr/bin/env python3
"""Generate the Complete 12-Tab Master Collage for all 4 GTNA Endgame Multiblocks:
  Row 1: Lança Cinética Orbital (UEV) -> Tab 1, Tab 2, Tab 3 (Buttons: MIRAR, AUTO, DISPARAR)
  Row 2: Portão de Fenda Dimensional (UIV) -> Tab 1, Tab 2, Tab 3 (Chord Wheel & Harmonic Staff - NO PYLONS)
  Row 3: Anel Colisor de Antimatéria (UIV) -> Tab 1, Tab 2, Tab 3 (The 10 Particles 5x2 & The 9 Proposals)
  Row 4: Câmara de Contenção Estelar (MAX) -> Tab 1, Tab 2, Tab 3 (Neutron Star / Pulsar in normal state, Buttons [-], [+], [MAGNETAR])

Outputs to: tools/design/ui_proposals/all_12_tabs_master_showcase.png
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

FONT_HEADER = get_font(20, bold=True)
FONT_SUB = get_font(13, bold=False)
FONT_ROW = get_font(12, bold=True)

def main():
    tabs = [
        # Row 1: Lança Cinética Orbital
        ("lance", [
            ("preview_tab1_orbital_survey.png", "Aba 1: Levantamento de Alvos & Órbitas"),
            ("preview_tab2_cannon_bench.png", "Aba 2: Bancada do Cano (Blueprint & Trilhos)"),
            ("preview_tab3_capsule_queue.png", "Aba 3: Fila de Cápsulas & Logística ME")
        ], "1. LANÇA CINÉTICA ORBITAL [UEV] — CONTROLES: [ALVO ▸], [AUTO: ON]"),
        
        # Row 2: Portão de Fenda Dimensional
        ("rift_gate", [
            ("preview_tab1_wormhole_vortex.png", "Aba 1: Vórtice Volumétrico & Horizonte"),
            ("preview_tab2_harmonic_score.png", "Aba 2: Roda de Acordes (OriginalsGui - Sem Pilones)"),
            ("preview_tab3_constellation_atlas.png", "Aba 3: Atlas de Sementes & Constelações")
        ], "2. PORTÃO DE FENDA DIMENSIONAL [UIV] — RODA DE ACORDES & HARMÔNICOS DE FENDA"),
        
        # Row 3: Anel Colisor de Antimatéria
        ("collider_ring", [
            ("preview_tab1_synchrotron_ring.png", "Aba 1: Anel Síncrotron de 3 km & Feixe"),
            ("preview_tab2_standard_model.png", "Aba 2: As 10 Partículas do ColliderCore (Grid 5x2)"),
            ("preview_tab3_beam_committee.png", "Aba 3: Comitê de Feixe (As 9 Propostas)")
        ], "3. ANEL COLISOR DE ANTIMATÉRIA [UIV] — 10 PARTÍCULAS EM GRID 5x2 & 9 PROPOSTAS DO CÓDIGO"),
        
        # Row 4: Câmara de Contenção Estelar
        ("stellar_chamber", [
            ("preview_tab1_neutron_star.png", "Aba 1: Estrela de Nêutrons / Pulsar (Estado Normal)"),
            ("preview_tab2_mass_period.png", "Aba 2: Diagrama Massa–Período (Limite TOV 2.2 M☉)"),
            ("preview_tab3_crust_seismograph.png", "Aba 3: Sismograma & Matéria Degenerada")
        ], "4. CÂMARA DE CONTENÇÃO ESTELAR [MAX] — ESTADO NORMAL: PULSAR · BOTÕES [-], [+], [MAGNETAR]"),
    ]

    card_w, card_h = 640, 480
    header_h = 75
    row_title_h = 28
    gap = 14
    
    total_w = gap * 4 + card_w * 3
    total_h = header_h + (row_title_h + card_h + gap) * 4 + gap
    
    canvas = Image.new('RGBA', (total_w, total_h), (12, 9, 18, 255))
    d = ImageDraw.Draw(canvas)
    
    # Master Header Banner
    d.rectangle([0, 0, total_w, header_h], fill=(24, 15, 36, 255), outline=(75, 45, 105, 255), width=2)
    d.text((32, 16), "GTNA · PAINEL GERAL DAS 12 ABAS NAVEGÁVEIS (100% CORRIGIDAS & ALINHADAS AO CÓDIGO JAVA)", fill=(255, 215, 80, 255), font=FONT_HEADER)
    d.text((32, 44), "Fiel a OriginalsGui.java, ColliderCore, StellarCore, RiftCore e LanceCore · Padrão Godforge Cosmic Purple (Backgrounds 512x512)", fill=(180, 190, 215, 255), font=FONT_SUB)
    
    cur_y = header_h + gap
    for row_idx, (mb_dir, row_tabs, mb_title) in enumerate(tabs):
        # Row Title Bar
        d.rectangle([gap, cur_y, total_w - gap, cur_y + row_title_h], fill=(20, 12, 30, 255), outline=(65, 40, 90, 255))
        d.text((gap + 12, cur_y + 6), mb_title, fill=(255, 215, 80, 255), font=FONT_ROW)
        cur_y += row_title_h + 6
        
        # 3 Preview Cards
        for col_idx, (pfilename, ptitle) in enumerate(row_tabs):
            ppath = os.path.join(PROPOSALS_DIR, mb_dir, 'previews', pfilename)
            card_x = gap + col_idx * (card_w + gap)
            if os.path.exists(ppath):
                im = Image.open(ppath)
                canvas.paste(im, (card_x, cur_y))
            else:
                d.rectangle([card_x, cur_y, card_x + card_w, cur_y + card_h], fill=(30, 20, 40, 255))
                d.text((card_x + 20, cur_y + 20), f"Falta: {pfilename}", fill=(255, 100, 100, 255))
                
        cur_y += card_h + gap
        
    out_file = os.path.join(PROPOSALS_DIR, 'all_12_tabs_master_showcase.png')
    canvas.save(out_file)
    print(f"[OK] Master collage gerada com sucesso em: {out_file}")

if __name__ == '__main__':
    main()
