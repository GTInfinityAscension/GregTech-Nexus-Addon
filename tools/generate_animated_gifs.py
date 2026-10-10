#!/usr/bin/env python3
"""
Gera GIFs animados ampliados (8x, NEAREST, com moldura de slot JEI)
para que o usuário possa ver as animações em loop contínuo direto no markdown.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/bd675c79-98ee-419c-9725-13ae9cf612a0")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from build_fine_tuning_showcase_g1 import (
    render_dragonmetal_c1, render_dragonmetal_c2, render_dragonmetal_c3,
    render_mellion_c1, render_mellion_c2, render_mellion_c3,
    render_nitinol_c1, render_nitinol_c2, render_nitinol_c3,
    render_superconductor_c1, render_superconductor_c2, render_superconductor_c3,
    extract_old_texture_frames
)

def make_jei_slot_frame(frame_arr, scale=6):
    # 16x16 -> 96x96
    size = 16 * scale
    im = Image.fromarray(frame_arr.astype(np.uint8), mode="RGBA")
    im_scaled = im.resize((size, size), resample=Image.NEAREST)
    
    pad = 6
    slot_w = size + pad * 2
    slot = Image.new("RGBA", (slot_w, slot_w), (139, 139, 139, 255))
    draw = ImageDraw.Draw(slot)
    
    # 3D JEI bevel
    draw.rectangle([0, 0, slot_w - 1, 2], fill=(55, 55, 55, 255))
    draw.rectangle([0, 0, 2, slot_w - 1], fill=(55, 55, 55, 255))
    draw.rectangle([0, slot_w - 3, slot_w - 1, slot_w - 1], fill=(255, 255, 255, 255))
    draw.rectangle([slot_w - 3, 0, slot_w - 1, slot_w - 1], fill=(255, 255, 255, 255))
    
    slot.paste(im_scaled, (pad, pad), im_scaled)
    return slot

def save_scaled_gif(frames, out_path, scale=6, duration=66):
    p_frames = []
    for f in frames:
        slot = make_jei_slot_frame(f, scale=scale)
        p_frame = slot.convert("P", palette=Image.ADAPTIVE, colors=256)
        p_frames.append(p_frame)
        
    p_frames[0].save(
        out_path,
        save_all=True,
        append_images=p_frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )
    print(f"Gerado: {out_path}")

# Materiais
targets = [
    ("dragonmetal", [
        ("atual", extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png")),
        ("op1", render_dragonmetal_c1()),
        ("op2", render_dragonmetal_c2()),
        ("op3", render_dragonmetal_c3())
    ]),
    ("mellion", [
        ("atual", extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_mellion/ingot.png")),
        ("op1", render_mellion_c1()),
        ("op2", render_mellion_c2()),
        ("op3", render_mellion_c3())
    ]),
    ("nitinol60", [
        ("atual", extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_nitinol_60/ingot.png")),
        ("op1", render_nitinol_c1()),
        ("op2", render_nitinol_c2()),
        ("op3", render_nitinol_c3())
    ]),
    ("superconductor_uiv", [
        ("atual", extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_superconductor_uiv_base/ingot.png")),
        ("op1", render_superconductor_c1()),
        ("op2", render_superconductor_c2()),
        ("op3", render_superconductor_c3())
    ])
]

for mat_name, options in targets:
    for opt_name, frames in options:
        if frames:
            out_file = ARTIFACT_DIR / f"{mat_name}_{opt_name}.gif"
            save_scaled_gif(frames, out_file)

print("Todos os GIFs animados foram gerados com sucesso!")
