#!/usr/bin/env python3
"""
Gera imagens PNG diretas com comparativos visuais ampliados (8x, pixelated)
para visualização imediata no chat e nos artefatos.
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ARTIFACT_DIR = Path("/home/raishxn/.gemini/antigravity/brain/bd675c79-98ee-419c-9725-13ae9cf612a0")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

DOCS_DIR = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon/docs/visualization")
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Import renderers from showcase builder
import sys
sys.path.append(str(Path(__file__).resolve().parent))
from build_fine_tuning_showcase_g1 import (
    render_dragonmetal_c1, render_dragonmetal_c2, render_dragonmetal_c3,
    render_mellion_c1, render_mellion_c2, render_mellion_c3,
    render_nitinol_c1, render_nitinol_c2, render_nitinol_c3,
    render_superconductor_c1, render_superconductor_c2, render_superconductor_c3,
    extract_old_texture_frames
)

SCALE = 8 # 16x16 -> 128x128
SLOT_SIZE = 128
PADDING = 24
BOX_WIDTH = 180
BOX_HEIGHT = 230

def create_jei_slot(inner_im):
    # inner_im is 128x128
    slot = Image.new("RGBA", (140, 140), (139, 139, 139, 255))
    draw = ImageDraw.Draw(slot)
    # Dark bevel top & left
    draw.rectangle([0, 0, 139, 3], fill=(55, 55, 55, 255))
    draw.rectangle([0, 0, 3, 139], fill=(55, 55, 55, 255))
    # Light bevel bottom & right
    draw.rectangle([0, 136, 139, 139], fill=(255, 255, 255, 255))
    draw.rectangle([136, 0, 139, 139], fill=(255, 255, 255, 255))
    
    # Paste centered
    slot.paste(inner_im, (6, 6), inner_im)
    return slot

def build_comparison_sheet(title, old_frames, c1_frames, c2_frames, c3_frames, out_name):
    # 4 columns: Old, C1, C2, C3
    total_w = 4 * 180 + 5 * 20
    total_h = 280
    sheet = Image.new("RGBA", (total_w, total_h), (22, 27, 34, 255))
    draw = ImageDraw.Draw(sheet)
    
    # Header
    draw.text((20, 12), title, fill=(240, 246, 252, 255))
    
    candidates = [
        ("ATUAL (RUIM)", old_frames[0] if old_frames else None, (248, 81, 73, 255)),
        ("OPÇÃO 1", c1_frames[0], (63, 185, 80, 255)),
        ("OPÇÃO 2", c2_frames[0], (88, 166, 255, 255)),
        ("OPÇÃO 3", c3_frames[0], (210, 168, 255, 255)),
    ]
    
    for i, (label, arr, tag_color) in enumerate(candidates):
        x_offset = 20 + i * (180 + 20)
        y_offset = 45
        
        # Border box
        draw.rectangle([x_offset, y_offset, x_offset + 180, y_offset + 220], outline=(48, 54, 61, 255), width=1)
        
        # Tag
        draw.text((x_offset + 10, y_offset + 8), label, fill=tag_color)
        
        if arr is not None:
            # Sprite
            im = Image.fromarray(arr.astype(np.uint8), mode="RGBA")
            im_scaled = im.resize((128, 128), resample=Image.NEAREST)
            slot = create_jei_slot(im_scaled)
            sheet.paste(slot, (x_offset + 20, y_offset + 35), slot)
        else:
            draw.text((x_offset + 30, y_offset + 80), "Sem Imagem", fill=(139, 148, 158, 255))
            
    # Save both to ARTIFACT_DIR and DOCS_DIR
    p1 = ARTIFACT_DIR / out_name
    p2 = DOCS_DIR / out_name
    sheet.save(p1)
    sheet.save(p2)
    print(f"Salvo: {p1}")

# 1. Dragonmetal
old_dragon = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_dragon_metal/ingot.png")
build_comparison_sheet("Dragonmetal (Dragonblood Metal) — Comparativo Visual", old_dragon, render_dragonmetal_c1(), render_dragonmetal_c2(), render_dragonmetal_c3(), "dragonmetal_sheet.png")

# 2. Mellion
old_mellion = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_mellion/ingot.png")
build_comparison_sheet("Mellion (Godforge UXV Catalyst) — Comparativo Visual", old_mellion, render_mellion_c1(), render_mellion_c2(), render_mellion_c3(), "mellion_sheet.png")

# 3. Nitinol 60
old_nitinol = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_nitinol_60/ingot.png")
build_comparison_sheet("Nitinol 60 (Ni₄Ti₆ Superalloy) — Comparativo Visual", old_nitinol, render_nitinol_c1(), render_nitinol_c2(), render_nitinol_c3(), "nitinol60_sheet.png")

# 4. Superconductor UIV
old_uiv = extract_old_texture_frames("src/main/resources/assets/gtceu/textures/item/material_sets/gtna_superconductor_uiv_base/ingot.png")
build_comparison_sheet("Superconductor UIV Base — Comparativo Visual", old_uiv, render_superconductor_c1(), render_superconductor_c2(), render_superconductor_c3(), "superconductor_uiv_sheet.png")

print("Todas as pranchas visuais geradas!")
