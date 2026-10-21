#!/usr/bin/env python3
"""Clean up tools/design/ui_proposals to keep ONLY the selected winning assets."""

import os
import glob

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_proposals')

# Allowed patterns for each multiblock:
KEEP = {
    'lance': [
        'backgrounds/bg_variation_1_cosmic_*.png',
        'backgrounds/bg_tab2_cannon_bench_*.png',
        'backgrounds/bg_tab3_capsule_queue_*.png',
        'buttons/btn_cosmic_*.png',
        'icons/*_cosmic_*.png',
        'progressbars/progressbar_cosmic.png',
        'previews/preview_tab*.png',
        'tabs_overview.png',
    ],
    'rift_gate': [
        'backgrounds/bg_variation_1a_volumetric_*.png',
        'backgrounds/bg_tab2_harmonic_score_*.png',
        'backgrounds/bg_tab3_constellation_atlas_*.png',
        'buttons/btn_cosmic_*.png',
        'icons/*_cosmic_*.png',
        'progressbars/progressbar_cosmic_*.png',
        'previews/preview_tab*.png',
        'tabs_overview.png',
    ],
    'collider_ring': [
        'backgrounds/bg_variation_1_accelerator_*.png',
        'backgrounds/bg_tab2_standard_model_*.png',
        'backgrounds/bg_tab3_beam_committee_*.png',
        'buttons/btn_cosmic_*.png',
        'icons/*.png',
        'progressbars/*.png',
        'previews/preview_tab*.png',
        'tabs_overview.png',
    ],
    'stellar_chamber': [
        'backgrounds/bg_variation_3_kerr_black_hole_*.png',
        'backgrounds/bg_tab2_mass_period_*.png',
        'backgrounds/bg_tab3_crust_seismograph_*.png',
        'buttons/btn_cosmic_*.png',
        'icons/*.png',
        'progressbars/*.png',
        'previews/preview_tab*.png',
        'tabs_overview.png',
    ]
}

def main():
    print(">>> Limpando ui_proposals para manter EXCLUSIVAMENTE os vencedores...")
    removed_count = 0
    
    for mb, patterns in KEEP.items():
        mb_dir = os.path.join(BASE, mb)
        if not os.path.exists(mb_dir):
            continue
            
        allowed_files = set()
        for pat in patterns:
            for f in glob.glob(os.path.join(mb_dir, pat)):
                allowed_files.add(os.path.abspath(f))
                
        # Walk and delete any file in subdirs not in allowed_files (except comparison_overview if desired, or remove comparison_overview as well)
        for root, dirs, files in os.walk(mb_dir):
            for f in files:
                full_path = os.path.abspath(os.path.join(root, f))
                # Remove non-winning previews, backgrounds, buttons, and old comparison sheets
                if full_path not in allowed_files:
                    os.remove(full_path)
                    removed_count += 1
                    
    # Clean up scratch test script if present
    test_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_rift_hd.py')
    if os.path.exists(test_script):
        os.remove(test_script)
        
    print(f"[OK] Removidos {removed_count} arquivos descartados.")
    print("Agora a pasta contém APENAS os assets oficiais vencedores!")

if __name__ == '__main__':
    main()
