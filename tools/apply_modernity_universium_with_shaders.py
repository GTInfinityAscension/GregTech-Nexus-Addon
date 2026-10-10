"""Restore Modernity Universium silhouettes with live RenderBlender cosmic rendering.

Source: Modernity-GTNH (CC BY-NC-SA 4.0), documented in THIRD_PARTY_NOTICES.md.
Preserves all existing GTCEu model aliases instead of deleting the asset directories.
"""
import json
import shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures')


def apply():
    from generate_material_set_textures import STANDARD_ITEMS
    src = SOURCE / 'items/materialicons/CUSTOM/universium'
    if not src.is_dir():
        raise FileNotFoundError(src)
    models = ROOT / 'src/main/resources/assets/gtceu/models/item/material_sets/gtna_universium'
    textures = ROOT / 'src/main/resources/assets/gtceu/textures/item/material_sets/gtna_universium'
    aliases = {v: k for k, v in STANDARD_ITEMS.items()}
    aliases.update({'rodLong': 'stickLong', 'rod': 'stick', 'gearSmall': 'gearGtSmall',
                    'singularity': 'gem', 'gear': 'gearGt', 'turbineBlade': 'TURBINE_BLADE', 'turbine_blade': 'TURBINE_BLADE'})
    count = 0
    for path in sorted(models.glob('*.json')):
        name = path.stem
        source_name = aliases.get(name, name)
        base = src / f'{source_name}.png'
        if not base.exists():
            base = src / f'{name}.png'
        if not base.exists():
            raise FileNotFoundError(f'No original Universium texture for {path}')
        overlay = base.with_name(base.stem + '_OVERLAY.png')
        shutil.copyfile(base, textures / f'{name}.png')
        for suffix in ('', '_overlay', '_secondary', '_cosmic_mask'):
            (textures / f'{name}{suffix}.png.mcmeta').unlink(missing_ok=True)
        image = Image.open(base).convert('RGBA')
        blank = Image.new('RGBA', image.size, (0, 0, 0, 0))
        if overlay.exists():
            shutil.copyfile(overlay, textures / f'{name}_overlay.png')
        else:
            blank.save(textures / f'{name}_overlay.png')
        blank.save(textures / f'{name}_secondary.png')
        # The cosmic shader samples red as opacity; preserve the original item's silhouette.
        alpha = image.getchannel('A')
        mask = Image.merge('RGBA', (alpha, alpha, alpha, alpha))
        mask.save(textures / f'{name}_cosmic_mask.png')
        data = json.loads(path.read_text())
        data['loader'] = 'renderblender:cosmic'
        data['cosmic'] = {'mask': f'gtceu:item/material_sets/gtna_universium/{name}_cosmic_mask'}
        path.write_text(json.dumps(data, indent=2) + '\n')
        count += 1
    print(f'Restored {count} Universium models with original silhouettes and live cosmic shader')


if __name__ == '__main__':
    apply()
