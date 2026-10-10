#!/usr/bin/env python3
"""
Gera GIFs animados que combinam LADO A LADO todas as opções se mexendo juntas em tempo real!
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/bd675c79-98ee-419c-9725-13ae9cf612a0")
DOCS_DIR = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon/docs/visualization")

import sys
sys.path.append(str(Path(__file__).resolve().parent))
from build_fine_tuning_showcase_g1 import (
    render_dragonmetal_c1, render_dragonmetal_c2, render_dragonmetal_c3,
    render_mellion_c1, render_mellion_c2, render_mellion_c3,
    render_nitinol_c1, render_nitinol_c2, render_nitinol_c3,
    render_superconductor_c1, render_superconductor_c2, render_superconductor_c3,
    extract_old_texture_frames
)

def make_slot(sprite_arr, scale=6):
    size = 16 * scale
    im = Image.fromarray(sprite_arr.astype(np.uint8), mode="RGBA")
    im_scaled = im.resize((size, size), resample=Image.NEAREST)
    
    pad = 4
    w = size + pad * 2
    slot = Image.new("RGBA", (w, w), (139, 139, 139, 255))
    draw = ImageDraw.Draw(slot)
    draw.rectangle([0, 0, w - 1, 2], fill=(55, 55, 55, 255))
    draw.rectangle([0, 0, 2, w - 1], fill=(55, 55, 55, 255))
    draw.rectangle([0, w - 3, w - 1, w - 1], fill=(255, 255, 255, 255))
    draw.rectangle([w - 3, 0, w - 1, w - 1], fill=(255, 255, 255, 255))
    slot.paste(im_scaled, (pad, pad), im_scaled)
    return slot

def build_row_animated_gif(title, opt_list, out_name, n_frames=30, duration=66):
    # opt_list: [("ATUAL (RUIM)", frames, (248, 81, 73)), ("OPÇÃO 1", frames, (63, 185, 80)), ...]
    slot_w = 16 * 6 + 8 # 104px
    col_w = 140
    total_w = len(opt_list) * col_w + 20
    total_h = 175
    
    gif_frames = []
    for f in range(n_frames):
        canvas = Image.new("RGBA", (total_w, total_h), (22, 27, 34, 255))
        draw = ImageDraw.Draw(canvas)
        draw.text((15, 8), title, fill=(240, 246, 252, 255))
        
        for i, (label, frames, tag_color) in enumerate(opt_list):
            x = 10 + i * col_w
            y = 30
            # box
            draw.rectangle([x, y, x + col_w - 10, y + 135], outline=(48, 54, 61, 255), width=1)
            draw.text((x + 10, y + 6), label, fill=tag_color)
            
            f_idx = f % len(frames)
            slot = make_slot(frames[f_idx])
            canvas.paste(slot, (x + 12, y + 25), slot)
            
        p_frame = canvas.convert("P", palette=Image.ADAPTIVE, colors=256)
        gif_frames.append(p_frame)
        
    p1 = ARTIFACT_DIR / out_name
    p2 = DOCS_DIR / out_name
    gif_frames[0].save(
        p1,
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )
    gif_frames[0].save(
        p2,
        save_all=True,
        append_images=gif_frames[1:],
        duration=duration,
        loop=0,
        disposal=2
    )
    print(f"Gerado row GIF: {p1}")

# 1. Dragonmetal
old_dragon = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png")
build_row_animated_gif("Dragonmetal (Dragonblood Metal) — Animações Lado a Lado", [
    ("ATUAL (RUIM)", old_dragon, (248, 81, 73, 255)),
    ("OPÇÃO 1", render_dragonmetal_c1(), (63, 185, 80, 255)),
    ("OPÇÃO 2", render_dragonmetal_c2(), (88, 166, 255, 255)),
    ("OPÇÃO 3", render_dragonmetal_c3(), (210, 168, 255, 255)),
], "dragonmetal_anim_row.gif")

# 2. Mellion
old_mellion = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_mellion/ingot.png")
build_row_animated_gif("Mellion (Godforge UXV Catalyst) — Animações Lado a Lado", [
    ("ATUAL (RUIM)", old_mellion, (248, 81, 73, 255)),
    ("OPÇÃO 1", render_mellion_c1(), (63, 185, 80, 255)),
    ("OPÇÃO 2", render_mellion_c2(), (88, 166, 255, 255)),
    ("OPÇÃO 3", render_mellion_c3(), (210, 168, 255, 255)),
], "mellion_anim_row.gif")

# 3. Nitinol 60
old_nitinol = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_nitinol_60/ingot.png")
build_row_animated_gif("Nitinol 60 (Ni₄Ti₆ Superalloy) — Animações Lado a Lado", [
    ("ATUAL (RUIM)", old_nitinol, (248, 81, 73, 255)),
    ("OPÇÃO 1", render_nitinol_c1(), (63, 185, 80, 255)),
    ("OPÇÃO 2", render_nitinol_c2(), (88, 166, 255, 255)),
    ("OPÇÃO 3", render_nitinol_c3(), (210, 168, 255, 255)),
], "nitinol60_anim_row.gif")

# 4. Superconductor UIV
old_uiv = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_superconductor_uiv_base/ingot.png")
build_row_animated_gif("Superconductor UIV Base — Animações Lado a Lado", [
    ("ATUAL (RUIM)", old_uiv, (248, 81, 73, 255)),
    ("OPÇÃO 1", render_superconductor_c1(), (63, 185, 80, 255)),
    ("OPÇÃO 2", render_superconductor_c2(), (88, 166, 255, 255)),
    ("OPÇÃO 3", render_superconductor_c3(), (210, 168, 255, 255)),
], "superconductor_uiv_anim_row.gif")

print("Todos os row GIFs foram gerados!")
