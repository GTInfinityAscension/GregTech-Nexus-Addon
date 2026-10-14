"""Gerador de Material Sets Animados do GregTech Nexus Addon (GTNA).

Converte sprites base modernos (16x16) em strips verticais animados (16x480, 30 frames)
com arquivos .mcmeta (frametime 2, interpolate true) e modelos composite JSON do GTCEu.

Uso:
    python3 tools/generate_material_set_textures.py --material white_dwarf
    python3 tools/generate_material_set_textures.py --material black_dwarf --style obsidian
    python3 tools/generate_material_set_textures.py --material hypogen
    python3 tools/generate_material_set_textures.py --material dragon_metal
    python3 tools/generate_material_set_textures.py --material chromatic_glass
    python3 tools/generate_material_set_textures.py --material celestial_tungsten
"""

import argparse
import json
import sys
import math
import colorsys
from pathlib import Path
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MODERNITY_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_ICONSETS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons")
GTCEU_DULL_BLOCKS = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/block/material_sets/dull")
GTCEU_DULL_ITEMS = ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/dull"

# Variação estrutural de silhuetas de ingots (Gordinhos vs Pequenininhos vs Padrão)
INGOT_TEMPLATES = {
    # Gordinhos (Ultimet / Shiny profile - superligas pesadas e refratárias)
    "mar_m_200_steel": "SHINY",
    "stellite": "SHINY",
    "hastelloy_n_75": "SHINY",
    "trinaquadalloy": "SHINY",
    "stellar_alloy": "SHINY",
    
    # Pequenininhos (Battery Alloy / Dull profile - ligas fusíveis, macias e delicadas)
    "indalloy_140": "DULL",
    "advanced_nitinol": "DULL",
    "shijima": "DULL",
}

STANDARD_ITEMS = {
    # Barras e Fundição
    "ingot": "ingot",
    "ingotHot": "ingot_hot",
    "ingotDouble": "ingot_double",
    "ingotTriple": "ingot_triple",
    "ingotQuadruple": "ingot_quadruple",
    "ingotQuintuple": "ingot_quintuple",
    "nugget": "nugget",
    
    # Placas
    "plate": "plate",
    "plateDouble": "plate_double",
    "plateTriple": "plate_triple",
    "plateQuadruple": "plate_quadruple",
    "plateQuintuple": "plate_quintuple",
    "plateDense": "plate_dense",
    "plateSuperdense": "plate_superdense",
    "foil": "foil",
    
    # Hastes e Fixadores
    "stick": "rod",
    "stickLong": "rod_long",
    "bolt": "bolt",
    "screw": "screw",
    "round": "round",
    "ring": "ring",
    
    # Engrenagens e Rotação
    "gearGt": "gear",
    "gearGtSmall": "gear_small",
    "rotor": "rotor",
    "spring": "spring",
    "springSmall": "spring_small",
    
    # Fios, Lâminas e Outros
    "wireFine": "wire_fine",
    "turbineBlade": "turbine_blade",
    "gem": "gem",
    
    # Pós
    "dust": "dust",
    "dustSmall": "dust_small",
    "dustTiny": "dust_tiny"
}

STANDARD_BLOCKS = {
    "block1": "block",
    "frameGt": "frame_gt"
}

PIPE_BLOCKS = {
    "pipeSide": "pipe_side",
    "pipeTiny": "pipe_tiny",
    "pipeSmall": "pipe_small",
    "pipeMedium": "pipe_medium",
    "pipeLarge": "pipe_large",
    "pipeHuge": "pipe_huge",
    "pipeQuadruple": "pipe_quadruple",
    "pipeNonuple": "pipe_nonuple"
}

EMPTY_16 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
MCMETA_CONTENT = json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=2) + "\n"


def palette_white_dwarf(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 60 + s_low * (208 - 60)
    g_low = 64 + s_low * (222 - 64)
    b_low = 92 + s_low * (240 - 92)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 208 + s_high * (255 - 208)
    g_high = 222 + s_high * (255 - 222)
    b_high = 240 + s_high * (255 - 240)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_black_dwarf(gray_val, style="obsidian"):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    
    if style == "crimson":
        r_low, g_low, b_low = 14 + s_low * 24, 10 + s_low * 12, 14 + s_low * 14
        r_high, g_high, b_high = 38 + s_high * 77, 22 + s_high * 43, 28 + s_high * 52
    elif style == "obsidian":
        r_low, g_low, b_low = 14 + s_low * 22, 14 + s_low * 22, 18 + s_low * 26
        r_high, g_high, b_high = 36 + s_high * 69, 36 + s_high * 72, 44 + s_high * 81
    else:  # void
        r_low, g_low, b_low = 12 + s_low * 20, 10 + s_low * 16, 18 + s_low * 28
        r_high, g_high, b_high = 32 + s_high * 63, 26 + s_high * 54, 46 + s_high * 89
        
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_hypogen_bronze(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 62 + s_low * (184 - 62)
    g_low = 30 + s_low * (96 - 30)
    b_low = 16 + s_low * (44 - 16)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 184 + s_high * (255 - 184)
    g_high = 96 + s_high * (205 - 96)
    b_high = 44 + s_high * (125 - 44)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_dragonblood(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.42
    s_low = np.clip(t / 0.42, 0, 1)
    # Sombra: granada dracônica profunda e sangue escuro (#320814)
    r_low = 50 + s_low * (180 - 50)
    g_low = 8 + s_low * (24 - 8)
    b_low = 18 + s_low * (42 - 18)
    
    s_high = np.clip((t - 0.42) / 0.58, 0, 1)
    # Corpo: rubi dracônico vivo -> highlights de fogo e escama âmbar incandescente
    r_high = 180 + s_high * (255 - 180)
    g_high = 24 + (s_high ** 1.6) * (185 - 24)
    b_high = 42 + (s_high ** 1.8) * (110 - 42)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])



def palette_celestial_tungsten(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 24 + s_low * (64 - 24)
    g_low = 25 + s_low * (68 - 25)
    b_low = 34 + s_low * (86 - 34)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 64 + s_high * (142 - 64)
    g_high = 68 + s_high * (150 - 68)
    b_high = 86 + s_high * (182 - 86)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_astral_titanium(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 68 + s_low * (185 - 68)
    g_low = 28 + s_low * (125 - 28)
    b_low = 105 + s_low * (225 - 105)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 185 + s_high * (255 - 185)
    g_high = 125 + s_high * (245 - 125)
    b_high = 225 + s_high * (255 - 225)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_six_phased_copper(gray_val, mode="copper"):
    t = gray_val / 255.0
    if mode == "copper":
        r = 75 + t * (238 - 75)
        g = 25 + t * (125 - 25)
        b = 8 + t * (30 - 8)
    elif mode == "flash":
        r = 90 + t * (255 - 90)
        g = 35 + t * (155 - 35)
        b = 12 + t * (50 - 12)
    elif mode == "green":
        r = 45 + t * (180 - 45)
        g = 52 + t * (165 - 52)
        b = 22 + t * (118 - 22)
    return np.dstack([r, g, b])


def palette_rhugnor(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 60 + s_low * (180 - 60)
    g_low = 0 + s_low * (20 - 0)
    b_low = 90 + s_low * (245 - 90)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 180 + s_high * (255 - 180)
    g_high = 20 + s_high * (180 - 20)
    b_high = 245 + s_high * (255 - 245)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_shirabon(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.45
    s_low = np.clip(t / 0.45, 0, 1)
    # Deep velvety ruby/plum shadow to canon tuning magenta #c61361 (198, 19, 97)
    r_low = 48 + s_low * (198 - 48)
    g_low = 4 + s_low * (19 - 4)
    b_low = 24 + s_low * (97 - 24)
    
    s_high = np.clip((t - 0.45) / 0.55, 0, 1)
    # Vibrant #c61361 to radiant rose-fuchsia glow
    r_high = 198 + s_high * (248 - 198)
    g_high = 19 + s_high * (42 - 19)
    b_high = 97 + s_high * (158 - 97)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_quantum(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 18 + s_low * (110 - 18)
    g_low = 55 + s_low * (200 - 55)
    b_low = 65 + s_low * (200 - 65)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 110 + s_high * (240 - 110)
    g_high = 200 + s_high * (255 - 200)
    b_high = 200 + s_high * (255 - 200)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_metastable_oganesson(gray_val):
    t = gray_val / 255.0
    mask_low = t < 0.42
    s_low = np.clip(t / 0.42, 0, 1)
    r_low = 10 + s_low * (20 - 10)
    g_low = 18 + s_low * (57 - 18)
    b_low = 52 + s_low * (127 - 52)
    
    s_high = np.clip((t - 0.42) / 0.58, 0, 1)
    r_high = 20 + s_high * (70 - 20)
    g_high = 57 + s_high * (130 - 57)
    b_high = 127 + s_high * (225 - 127)
    
    r = np.where(mask_low, r_low, r_high)
    g = np.where(mask_low, g_low, g_high)
    b = np.where(mask_low, b_low, b_high)
    return np.dstack([r, g, b])


def palette_transcendent_metal(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.5
    s1 = t / 0.5
    r[mask1] = 20 + s1[mask1] * (46 - 20)
    g[mask1] = 21 + s1[mask1] * (48 - 21)
    b[mask1] = 26 + s1[mask1] * (58 - 26)
    mask2 = (t >= 0.5) & (t < 0.85)
    s2 = (t - 0.5) / 0.35
    r[mask2] = 46 + s2[mask2] * (82 - 46)
    g[mask2] = 48 + s2[mask2] * (86 - 48)
    b[mask2] = 58 + s2[mask2] * (104 - 58)
    mask3 = t >= 0.85
    s3 = (t - 0.85) / 0.15
    r[mask3] = 82 + s3[mask3] * (130 - 82)
    g[mask3] = 86 + s3[mask3] * (136 - 86)
    b[mask3] = 104 + s3[mask3] * (162 - 104)
    return np.dstack([r, g, b])


def palette_creon(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 22 + s1[mask1] * (70 - 22)
    g[mask1] = 0 + s1[mask1] * (4 - 0)
    b[mask1] = 26 + s1[mask1] * (70 - 26)
    
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 70 + s2[mask2] * (145 - 70)
    g[mask2] = 4 + s2[mask2] * (32 - 4)
    b[mask2] = 70 + s2[mask2] * (155 - 70)
    
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 145 + s3[mask3] * (235 - 145)
    g[mask3] = 32 + s3[mask3] * (140 - 32)
    b[mask3] = 155 + s3[mask3] * (245 - 155)
    
    return np.dstack([r, g, b])


def palette_mellion(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    
    # Sombra: Ametista abissal profunda (#200c2c)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 32 + s1[mask1] * (96 - 32)
    g[mask1] = 12 + s1[mask1] * (24 - 12)
    b[mask1] = 44 + s1[mask1] * (68 - 44)
    
    # Meio: Carmesim imperial nobre e veludo cósmico (#9c1b48)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 96 + s2[mask2] * (185 - 96)
    g[mask2] = 24 + s2[mask2] * (55 - 24)
    b[mask2] = 68 + s2[mask2] * (115 - 68)
    
    # Realce: Ouro rosado acetinado e platina pura (#f8a4bc -> #fff0f5)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 185 + s3[mask3] * (255 - 185)
    g[mask3] = 55 + (s3[mask3] ** 1.3) * (240 - 55)
    b[mask3] = 115 + (s3[mask3] ** 1.2) * (245 - 115)
    
    return np.dstack([r, g, b])



def palette_echoite(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 9 + s1[mask1] * (22 - 9)
    g[mask1] = 34 + s1[mask1] * (72 - 34)
    b[mask1] = 30 + s1[mask1] * (65 - 30)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 22 + s2[mask2] * (38 - 22)
    g[mask2] = 72 + s2[mask2] * (145 - 72)
    b[mask2] = 65 + s2[mask2] * (115 - 65)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 38 + s3[mask3] * (110 - 38)
    g[mask3] = 145 + s3[mask3] * (235 - 145)
    b[mask3] = 115 + s3[mask3] * (210 - 115)
    return np.dstack([r, g, b])


def palette_universium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 24 + s1[mask1] * (62 - 24)
    g[mask1] = 16 + s1[mask1] * (42 - 16)
    b[mask1] = 52 + s1[mask1] * (115 - 52)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 62 + s2[mask2] * (145 - 62)
    g[mask2] = 42 + s2[mask2] * (82 - 42)
    b[mask2] = 115 + s2[mask2] * (200 - 115)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 145 + s3[mask3] * (245 - 145)
    g[mask3] = 82 + s3[mask3] * (215 - 82)
    b[mask3] = 200 + s3[mask3] * (255 - 200)
    return np.dstack([r, g, b])


def palette_ichorium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 90 + s1[mask1] * (165 - 90)
    g[mask1] = 36 + s1[mask1] * (82 - 36)
    b[mask1] = 6 + s1[mask1] * (16 - 6)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 165 + s2[mask2] * (228 - 165)
    g[mask2] = 82 + s2[mask2] * (145 - 82)
    b[mask2] = 16 + s2[mask2] * (32 - 16)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 228 + s3[mask3] * (255 - 228)
    g[mask3] = 145 + s3[mask3] * (235 - 145)
    b[mask3] = 32 + s3[mask3] * (140 - 32)
    return np.dstack([r, g, b])


def palette_tengam_purified(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 52 + s1[mask1] * (115 - 52)
    g[mask1] = 82 + s1[mask1] * (165 - 82)
    b[mask1] = 26 + s1[mask1] * (65 - 26)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 115 + s2[mask2] * (195 - 115)
    g[mask2] = 165 + s2[mask2] * (232 - 165)
    b[mask2] = 65 + s2[mask2] * (115 - 65)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 195 + s3[mask3] * (242 - 195)
    g[mask3] = 232 + s3[mask3] * (255 - 232)
    b[mask3] = 115 + s3[mask3] * (195 - 115)
    return np.dstack([r, g, b])


def palette_tengam_attuned(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 65 + s1[mask1] * (145 - 65)
    g[mask1] = 105 + s1[mask1] * (205 - 105)
    b[mask1] = 30 + s1[mask1] * (78 - 30)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 145 + s2[mask2] * (220 - 145)
    g[mask2] = 205 + s2[mask2] * (255 - 205)
    b[mask2] = 78 + s2[mask2] * (135 - 78)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 220 + s3[mask3] * (255 - 220)
    g[mask3] = 255
    b[mask3] = 135 + s3[mask3] * (235 - 135)
    return np.dstack([r, g, b])


def palette_fallking(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 95 + s1[mask1] * (185 - 95)
    g[mask1] = 72 + s1[mask1] * (145 - 72)
    b[mask1] = 32 + s1[mask1] * (68 - 32)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 185 + s2[mask2] * (255 - 185)
    g[mask2] = 145 + s2[mask2] * (212 - 145)
    b[mask2] = 68 + s2[mask2] * (115 - 68)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 255
    g[mask3] = 212 + s3[mask3] * (250 - 212)
    b[mask3] = 115 + s3[mask3] * (210 - 115)
    return np.dstack([r, g, b])


def palette_odyssey(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 26 + s1[mask1] * (48 - 26)
    g[mask1] = 48 + s1[mask1] * (88 - 48)
    b[mask1] = 42 + s1[mask1] * (78 - 42)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 48 + s2[mask2] * (88 - 48)
    g[mask2] = 88 + s2[mask2] * (148 - 88)
    b[mask2] = 78 + s2[mask2] * (132 - 78)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 88 + s3[mask3] * (165 - 88)
    g[mask3] = 148 + s3[mask3] * (225 - 148)
    b[mask3] = 132 + s3[mask3] * (210 - 132)
    return np.dstack([r, g, b])


def palette_draconium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 35 + s1[mask1] * (85 - 35)
    g[mask1] = 10 + s1[mask1] * (28 - 10)
    b[mask1] = 55 + s1[mask1] * (125 - 55)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 85 + s2[mask2] * (165 - 85)
    g[mask2] = 28 + s2[mask2] * (58 - 28)
    b[mask2] = 125 + s2[mask2] * (225 - 125)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 165 + s3[mask3] * (245 - 165)
    g[mask3] = 58 + s3[mask3] * (195 - 58)
    b[mask3] = 225 + s3[mask3] * (255 - 225)
    return np.dstack([r, g, b])


def palette_awakened_draconium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.4
    s1 = np.clip(t / 0.4, 0, 1)
    r[mask1] = 95 + s1[mask1] * (185 - 95)
    g[mask1] = 16 + s1[mask1] * (52 - 16)
    b[mask1] = 0 + s1[mask1] * (8 - 0)
    mask2 = (t >= 0.4) & (t < 0.75)
    s2 = np.clip((t - 0.4) / 0.35, 0, 1)
    r[mask2] = 185 + s2[mask2] * (255 - 185)
    g[mask2] = 52 + s2[mask2] * (135 - 52)
    b[mask2] = 8 + s2[mask2] * (18 - 8)
    mask3 = t >= 0.75
    s3 = np.clip((t - 0.75) / 0.25, 0, 1)
    r[mask3] = 255
    g[mask3] = 135 + s3[mask3] * (250 - 135)
    b[mask3] = 18 + s3[mask3] * (180 - 18)
    return np.dstack([r, g, b])


def palette_cosmic_neutronium(gray_val):
    t = gray_val / 255.0
    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)
    mask1 = t < 0.5
    s1 = np.clip(t / 0.5, 0, 1)
    r[mask1] = 4 + s1[mask1] * (18 - 4)
    g[mask1] = 8 + s1[mask1] * (24 - 8)
    b[mask1] = 18 + s1[mask1] * (48 - 18)
    mask2 = t >= 0.5
    s2 = np.clip((t - 0.5) / 0.5, 0, 1)
    r[mask2] = 18 + s2[mask2] * (42 - 18)
    g[mask2] = 24 + s2[mask2] * (54 - 24)
    b[mask2] = 48 + s2[mask2] * (92 - 48)
    return np.dstack([r, g, b])



def animate(base_im, material_type="white_dwarf", bd_style="obsidian", n_frames=30):
    base_arr = np.array(base_im.convert("RGBA"), dtype=np.float32)
    h_orig, w_orig = base_arr.shape[:2]
    if h_orig > w_orig:
        base_arr = base_arr[:w_orig, :, :]
    
    h, w = base_arr.shape[:2]
    gray = base_arr[:, :, 0]
    alpha = base_arr[:, :, 3] > 0
    t_base = gray / 255.0
    
    y_coords, x_coords = np.ogrid[:h, :w]
    stacked_frames = []
    
    if material_type == "quantum":
        colored_rgb = palette_quantum(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            psi_a = np.cos(2 * np.pi * (t * 2.0 + (x_coords + y_coords) / 7.0))
            psi_b = np.cos(2 * np.pi * (-t * 3.0 + (x_coords - y_coords) / 6.0))
            
            prob_density = ((psi_a + psi_b) * 0.5) ** 2
            collapse = np.sin(2 * np.pi * t * 4.0) ** 6 * 20.0
            
            intensity = prob_density * 65.0 + collapse
            
            frame[:, :, 0] += intensity * 0.70
            frame[:, :, 1] += intensity * 1.15
            frame[:, :, 2] += intensity * 1.25
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "metastable_oganesson":
        colored_rgb = palette_metastable_oganesson(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        # Center of mass of the item
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist_from_core = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            # Concentric relativistic electron shells expanding outward and breathing
            wavelength = 4.5
            shell_phase = 2 * np.pi * (dist_from_core / wavelength - t)
            
            shell_val = np.sin(shell_phase) * 0.6 + np.sin(shell_phase * 2.0 - t * 2 * np.pi) * 0.4
            shell_glow = np.clip((shell_val + 0.3) / 1.3, 0, 1) ** 2
            
            boundary_modulation = np.cos(2 * np.pi * (t + dist_from_core / 10.0)) * 0.25 + 0.75
            effective_glow = shell_glow * boundary_modulation * (0.35 + 0.65 * t_base)
            
            frame[:, :, 0] += effective_glow * 35.0
            frame[:, :, 1] += effective_glow * 90.0
            frame[:, :, 2] += effective_glow * 145.0
            
            rim_pulse = np.sin(2 * np.pi * t) * 12.0 * (t_base > 0.65)
            frame[:, :, 2] += rim_pulse
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "transcendent_metal":
        colored_rgb = palette_transcendent_metal(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]

        vertices_4d = []
        for vx in [-1, 1]:
            for vy in [-1, 1]:
                for vz in [-1, 1]:
                    for vw in [-1, 1]:
                        vertices_4d.append(np.array([vx, vy, vz, vw], dtype=float))

        edges = []
        for i in range(16):
            for j in range(i + 1, 16):
                if np.isclose(np.sum(np.abs(vertices_4d[i] - vertices_4d[j])), 2.0):
                    edges.append((i, j))

        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames

            theta = 2 * np.pi * t
            phi = 2 * np.pi * t * 0.5
            c1, s1 = np.cos(theta), np.sin(theta)
            c2, s2 = np.cos(phi), np.sin(phi)
            verts_proj = []
            for vx, vy, vz, vw in vertices_4d:
                rx = vx * c1 - vw * s1
                rw = vx * s1 + vw * c1
                ry = vy * c2 - vz * s2
                rz = vy * s2 + vz * c2
                d4 = 2.8
                s4 = 1.0 / (d4 - rw * 0.6)
                d3 = 3.5
                s3 = 1.0 / (d3 - (rz * s4) * 0.5)
                px = 7.5 + (rx * s4 * s3) * 32.0
                py = 7.5 + (ry * s4 * s3) * 32.0
                verts_proj.append((px, py, s4))

            grid = np.zeros((h, w), dtype=float)
            for (i, j) in edges:
                p1 = np.array([verts_proj[i][0], verts_proj[i][1]])
                p2 = np.array([verts_proj[j][0], verts_proj[j][1]])
                v = p2 - p1
                v_len_sq = np.sum(v**2) + 1e-6
                u_x = x_coords - p1[0]
                u_y = y_coords - p1[1]
                h_val = np.clip((u_x * v[0] + u_y * v[1]) / v_len_sq, 0.0, 1.0)
                dist_sq = (u_x - h_val * v[0])**2 + (u_y - h_val * v[1])**2
                intensity = np.exp(-dist_sq / 0.75)
                depth_w = (verts_proj[i][2] + verts_proj[j][2]) * 1.4
                grid += intensity * depth_w

            for (px, py, s4) in verts_proj:
                dist_sq = (x_coords - px)**2 + (y_coords - py)**2
                grid += np.exp(-dist_sq / 0.6) * s4 * 2.2

            wf_glow = np.clip(grid / 3.8, 0.0, 1.0)
            wf_effective = wf_glow * (0.35 + 0.65 * t_base)
            frame[:, :, 0] += wf_effective * 135.0 * 0.92
            frame[:, :, 1] += wf_effective * 135.0 * 0.94
            frame[:, :, 2] += wf_effective * 135.0 * 1.08

            facet_coord = (0.35 * x_coords + 0.55 * y_coords - t * 14.0) % 10.0
            facet_sweep = np.exp(-((facet_coord - 5.0) / 1.1)**2) * (t_base > 0.35)
            frame[:, :, 0] += facet_sweep * 110.0 * 0.94
            frame[:, :, 1] += facet_sweep * 110.0 * 0.96
            frame[:, :, 2] += facet_sweep * 110.0 * 1.04

            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)

            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "creon":
        colored_rgb = palette_creon(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]

        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        r = np.sqrt((x_coords - cx) ** 2 + (y_coords - cy) ** 2)

        for f in range(n_frames):
            phi = (f / n_frames) * 2 * np.pi
            frame = colored.copy()

            # Expanding gravitational ripple
            ripple = np.sin(phi - r * 0.85)
            ripple_pos = np.maximum(0, ripple) ** 2

            # Core breathing flare
            core_breath = np.exp(-r / 3.8) * (np.sin(phi) ** 2 * 1.2)

            # Total energetic intensity
            flare = (ripple_pos * 0.65 + core_breath * 0.75) * np.clip(t_base + 0.3, 0.4, 1.2)

            # Color shift towards vivid magenta / violet-white
            frame[:, :, 0] += flare * 85.0
            frame[:, :, 1] += flare * 28.0
            frame[:, :, 2] += flare * 105.0

            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)

            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "mellion":
        # Opção 1: Carmesim Imperial com Ouro Rosado Acetinado e Glint Especular
        colored_rgb = palette_mellion(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]

        for f in range(n_frames):
            phase = f / n_frames
            frame = colored.copy()

            # Glint suave e elegante deslizando pela faceta chanfrada em 30 frames
            sweep = (phase * 24.0) - 4.0
            diag = (x_coords * 0.7 + y_coords * 0.5)
            glint = np.exp(-((diag - sweep) / 1.4)**2) * (t_base > 0.5)

            frame[:, :, 0] += glint * 60.0
            frame[:, :, 1] += glint * 50.0
            frame[:, :, 2] += glint * 55.0

            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)

            stacked_frames.append(frame.astype(np.uint8))

            
    elif material_type == "shirabon":
        colored_rgb = palette_shirabon(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            wave_y1 = 7.5 + 4.5 * np.sin(x_coords * (2 * np.pi / 8.0) + t * 2 * np.pi)
            wave_y2 = 7.5 - 3.0 * np.sin(x_coords * (2 * np.pi / 5.0) - t * 4 * np.pi)
            
            line1 = np.exp(-((y_coords - wave_y1) / 1.1)**2)
            line2 = np.exp(-((y_coords - wave_y2) / 1.1)**2) * 0.7
            
            oscilloscope_glow = (line1 + line2) * 65.0
            hum = 8.0 * np.sin(2 * np.pi * t * 3.0)
            
            total_add = oscilloscope_glow + hum
            
            frame[:, :, 0] += total_add * 1.10
            frame[:, :, 1] += total_add * 0.15
            frame[:, :, 2] += total_add * 0.60
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "rhugnor":
        colored_rgb = palette_rhugnor(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        grid1 = (x_coords % 4 == 0) | (y_coords % 4 == 0)
        grid2 = ((x_coords + y_coords) % 4 == 0)
        grid_lines = grid1 | grid2
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            wave_pos = (x_coords + y_coords - t * 16.0) % 8.0
            wave_glow = np.exp(-((wave_pos - 4.0) / 1.5)**2)
            
            cell_pulse = np.sin(2 * np.pi * t * 2.0 + (x_coords // 4) + (y_coords // 4)) * 18.0
            grid_flare = np.where(grid_lines, wave_glow * 70.0 + 15.0, 0.0)
            
            total_add = grid_flare + cell_pulse
            
            frame[:, :, 0] += total_add * 0.90
            frame[:, :, 1] += total_add * 0.35
            frame[:, :, 2] += total_add * 1.30
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "six_phased_copper":
        col_copper = palette_six_phased_copper(gray, mode="copper")
        col_flash = palette_six_phased_copper(gray, mode="flash")
        col_green = palette_six_phased_copper(gray, mode="green")
        
        for f in range(n_frames):
            frame = np.zeros_like(base_arr)
            frame[:, :, 3] = base_arr[:, :, 3]
            
            if f < 24:
                hum = 4.0 * np.sin(2 * np.pi * (f / 24.0))
                frame[:, :, :3] = col_copper + hum
            elif f == 24:
                frame[:, :, :3] = col_green
            elif f == 25:
                frame[:, :, :3] = col_flash
            elif f == 26:
                frame[:, :, :3] = col_green
            elif f == 27:
                frame[:, :, :3] = col_flash
            elif f == 28:
                frame[:, :, :3] = col_green
            elif f == 29:
                frame[:, :, :3] = col_flash
                
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "astral_titanium":
        colored_rgb = palette_astral_titanium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        valid_coords = np.argwhere((alpha) & (t_base > 0.45))
        np.random.seed(1337)
        star_indices = [2, 14, 27, 42, 60, 78] if len(valid_coords) > 85 else [0, min(4, len(valid_coords)-1), min(8, len(valid_coords)-1)]
        star_pts = [valid_coords[i % len(valid_coords)] for i in star_indices]
        star_phases = [0.0, 0.18, 0.35, 0.52, 0.70, 0.86]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            ambient = 12.0 * np.sin(2 * np.pi * (t + (x_coords + y_coords) / 22.0))
            for c, boost in enumerate([0.95, 0.85, 1.15]):
                frame[:, :, c] += ambient * boost
                
            for (sy, sx), s_phase in zip(star_pts, star_phases):
                phase_diff = (t - s_phase) % 1.0
                glint = max(0.0, np.cos(phase_diff * 2 * np.pi)) ** 12
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            val_add = glint * weight * 170.0
                            frame[ny, nx, 0] += val_add * 0.95
                            frame[ny, nx, 1] += val_add * 0.90
                            frame[ny, nx, 2] += val_add * 1.00
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "celestial_tungsten":
        colored_rgb = palette_celestial_tungsten(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        np.random.seed(42)
        valid_coords = np.argwhere((alpha) & (t_base > 0.35))
        star_indices = [3, 15, 28, 45, 62, 80] if len(valid_coords) > 85 else [0, min(5, len(valid_coords)-1), min(10, len(valid_coords)-1)]
        star_pts = [valid_coords[i % len(valid_coords)] for i in star_indices]
        star_phases = [0.0, 0.2, 0.35, 0.55, 0.7, 0.85]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            ambient = 12.0 * np.sin(2 * np.pi * (t + (x_coords + y_coords) / 20.0))
            for c, boost in enumerate([0.9, 0.95, 1.15]):
                frame[:, :, c] += ambient * boost
                
            for (sy, sx), s_phase in zip(star_pts, star_phases):
                phase_diff = (t - s_phase) % 1.0
                glint = max(0.0, np.cos(phase_diff * 2 * np.pi)) ** 12
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            val_add = glint * weight * 160.0
                            frame[ny, nx, 0] += val_add * 0.85
                            frame[ny, nx, 1] += val_add * 0.92
                            frame[ny, nx, 2] += val_add * 1.00
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
            
    elif material_type == "chromatic_glass":
        for f in range(n_frames):
            hue = (f / n_frames) % 1.0
            r_map = np.zeros((h, w), dtype=np.float32)
            g_map = np.zeros((h, w), dtype=np.float32)
            b_map = np.zeros((h, w), dtype=np.float32)
            
            for y in range(h):
                for x in range(w):
                    v_val = 0.25 + 0.75 * t_base[y, x]
                    s_val = 0.85 if t_base[y, x] < 0.88 else 0.35
                    rgb = colorsys.hsv_to_rgb(hue, s_val, v_val)
                    r_map[y, x] = rgb[0] * 255.0
                    g_map[y, x] = rgb[1] * 255.0
                    b_map[y, x] = rgb[2] * 255.0
                    
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.where(alpha, np.clip(r_map, 0, 255), 0)
            frame[:, :, 1] = np.where(alpha, np.clip(g_map, 0, 255), 0)
            frame[:, :, 2] = np.where(alpha, np.clip(b_map, 0, 255), 0)
            frame[:, :, 3] = base_arr[:, :, 3].astype(np.uint8)
            stacked_frames.append(frame)
            
    elif material_type == "dragon_metal":
        # Opção 1: Escama Dracônica Iridescente & Pulso de Brasa
        colored_rgb = palette_dragonblood(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        bevel_mask = (y_coords <= x_coords + 2) & (t_base > 0.6)
        
        for f in range(n_frames):
            phase = f / n_frames
            tau = 2 * math.pi * phase
            frame = colored.copy()
            
            # Onda de calor dracônica que corre na diagonal top-left
            wave = np.sin((x_coords + y_coords) * 0.45 - tau) * 0.5 + 0.5
            ember = (wave ** 3.0) * (t_base > 0.4)
            
            # Chanfros superiores recebem glint dourado de escama
            scale_glint = np.sin(x_coords * 0.8 - tau) * 0.5 + 0.5
            scale_boost = (scale_glint ** 4.0) * bevel_mask
            
            frame[:, :, 0] += ember * 60.0 + scale_boost * 90.0
            frame[:, :, 1] += ember * 35.0 + scale_boost * 80.0
            frame[:, :, 2] += ember * 5.0 + scale_boost * 30.0
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))


    elif material_type == "echoite":
        # Opção 2 aprovada: Sonic Boom Resonance & Frequência Acústica
        colored_rgb = palette_echoite(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            wave1 = np.sin(2 * np.pi * (dist / 3.2 - t * 2.0))
            wave2 = np.sin(2 * np.pi * (dist / 2.0 - t * 3.0))
            acoustic_interf = ((wave1 * 0.65 + wave2 * 0.35) + 0.2) ** 2
            acoustic_wave = np.clip(acoustic_interf, 0, 1.2) * (t_base > 0.3) * 68.0
            
            boom = (np.sin(2 * np.pi * t) ** 14) * np.exp(-dist / 4.5) * 105.0
            spark = (np.sin(2 * np.pi * (t * 4.0 + (x_coords + y_coords) * 0.8)) ** 12) * 55.0 * (t_base > 0.5)
            
            total_sonic = acoustic_wave + boom + spark
            frame[:, :, 0] += total_sonic * 0.25
            frame[:, :, 1] += total_sonic * 1.15
            frame[:, :, 2] += total_sonic * 1.10
            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "universium":
        colored_rgb = palette_universium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        valid_coords = np.argwhere((alpha) & (t_base > 0.4))
        np.random.seed(777)
        star_pts = [valid_coords[i % len(valid_coords)] for i in [5, 18, 33, 52, 70]] if len(valid_coords) > 75 else []
        star_phases = [0.0, 0.22, 0.45, 0.68, 0.88]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            band_phase = (x_coords * 0.7 - y_coords * 0.7 - t * 16.0) % 14.0
            band_glow = np.exp(-((band_phase - 7.0) / 1.6)**2) * (t_base > 0.3)
            nebula = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 16.0)) * 15.0
            
            frame[:, :, 0] += band_glow * 95.0 + nebula * 0.9
            frame[:, :, 1] += band_glow * 65.0 + nebula * 0.5
            frame[:, :, 2] += band_glow * 135.0 + nebula * 1.3
            
            for (sy, sx), sp in zip(star_pts, star_phases):
                glint = max(0.0, np.cos(((t - sp) % 1.0) * 2 * np.pi)) ** 10
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.35), (0, -1, 0.35), (1, 0, 0.35), (-1, 0, 0.35)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            v = glint * weight * 165.0
                            frame[ny, nx, 0] += v * 0.95
                            frame[ny, nx, 1] += v * 0.90
                            frame[ny, nx, 2] += v * 1.00
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "ichorium":
        # Opção 3 aprovada pelo autor: Ichor Divine Crucible (Ascensão de Gotas do Sangue dos Deuses)
        drop_x_seeds = [4.0, 7.5, 11.5, 5.5, 9.5]
        drop_phases = [0.0, 0.2, 0.45, 0.65, 0.85]

        for f in range(n_frames):
            frame = np.zeros_like(base_arr)
            t = f / n_frames
            
            # Paleta Base: âmbar mel rubi profundo
            r = 52.0 + t_base * 170.0
            g = 16.0 + (t_base ** 1.4) * 100.0
            b = 2.0 + (t_base ** 2.2) * 10.0
            
            # Ascensão de micro-gotas de Ichor flutuando para cima (contra a gravidade)
            total_drops = np.zeros((h, w), dtype=np.float32)
            for i, (seed_x, phase) in enumerate(zip(drop_x_seeds, drop_phases)):
                cur_t = (t + phase) % 1.0
                cur_y = 15.0 - cur_t * 15.0
                cur_x = seed_x + np.sin(2 * np.pi * (cur_t * 2.0 + i)) * 1.0
                d = np.sqrt((x_coords - cur_x)**2 + (y_coords - cur_y)**2)
                
                drop = np.exp(-(d / 1.1)**2) * (1.2 - cur_t * 0.4)
                total_drops += drop
                
            drops_fx = total_drops * (t_base > 0.25)
            
            # Dissolução na borda superior (detonação de luz suave)
            top_dissolve = np.exp(-((y_coords - 2.5) / 1.5)**2) * (np.sin(2 * np.pi * t * 2.0) * 0.5 + 0.5) * 0.6 * (t_base > 0.4)
            
            # Efervescência de fundo no metal líquido
            simmer = (np.sin(2 * np.pi * (t * 3.0 + x_coords * 0.7 + y_coords * 0.5)) ** 10) * 0.45 * (t_base > 0.35)
            
            total_fx = drops_fx + top_dissolve + simmer
            
            # Cores: ouro solar celestial incandescente
            r += total_fx * 175.0
            g += total_fx * 135.0
            b += total_fx * 30.0
            
            # Centros das gotas em branco puro
            white_drop = np.clip(total_fx - 0.9, 0, 1.2) * 105.0
            r += white_drop * 0.95
            g += white_drop * 0.95
            b += white_drop * 0.85
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type in ("tengam_purified", "tengam_attuned"):
        # Opção 3 aprovada pelo autor: Superconducting Meissner Vortex (Vórtices de Abrikosov & Efeito Meissner)
        is_attuned = (material_type == "tengam_attuned")
        vortices = [
            (4.0, 4.0), (12.0, 4.0), (8.0, 8.0), (4.0, 12.0), (12.0, 12.0)
        ]
        gy, gx = np.gradient(gray)
        edge_mag = np.sqrt(gx**2 + gy**2)
        norm_edge = edge_mag / max(1.0, np.max(edge_mag))

        for f in range(n_frames):
            frame = np.zeros_like(base_arr)
            t = f / n_frames
            
            # Paleta Base:
            if is_attuned:
                # Sintonizado: incandescente verde-elétrico puro (#d5ff80)
                r = 20.0 + t_base * 95.0
                g = 42.0 + t_base * 175.0
                b = 10.0 + (t_base ** 1.6) * 45.0
            else:
                # Purificado: verde-oliva supercondutor elegante (#badf70)
                r = 16.0 + t_base * 85.0
                g = 35.0 + t_base * 165.0
                b = 8.0 + (t_base ** 1.8) * 40.0
                
            # Vórtices de fluxo quântico girando orbitalmente
            total_vortex = np.zeros((h, w), dtype=np.float32)
            rot_mult = 1.5 if is_attuned else 1.0
            for i, (vx, vy) in enumerate(vortices):
                rot_vx = vx + np.cos(2 * np.pi * (t * rot_mult + i / 5.0)) * 1.2
                rot_vy = vy + np.sin(2 * np.pi * (t * rot_mult + i / 5.0)) * 1.2
                d = np.sqrt((x_coords - rot_vx)**2 + (y_coords - rot_vy)**2)
                
                vortex_field = np.exp(-d / 1.6) * (0.6 + 0.4 * np.sin(2 * np.pi * (t * 2.0 * rot_mult - d * 0.8)))
                total_vortex += vortex_field
                
            vortex_fx = total_vortex * (t_base > 0.26)
            
            # Efeito Meissner: repulsão do fluxo para as bordas exteriores
            meissner_freq = 2.0 if is_attuned else 1.5
            meissner_edge = (norm_edge ** 1.5) * (np.sin(2 * np.pi * (t * meissner_freq + (x_coords + y_coords) * 0.2)) * 0.4 + 0.6) * (t_base > 0.3)
            
            total_fx = vortex_fx * 1.1 + meissner_edge * (0.9 if is_attuned else 0.7)
            
            # Adição de cor
            if is_attuned:
                r += total_fx * 170.0
                g += total_fx * 210.0
                b += total_fx * 45.0
                vortex_core = np.clip(total_fx - 0.75, 0, 1.2) * 125.0
            else:
                r += total_fx * 155.0
                g += total_fx * 195.0
                b += total_fx * 25.0
                vortex_core = np.clip(total_fx - 0.85, 0, 1.2) * 115.0
                
            r += vortex_core * 0.95
            g += vortex_core * 1.00
            b += vortex_core * 0.75
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "fallking":
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        for f in range(n_frames):
            frame = np.zeros((h, w, 4), dtype=np.float32)
            t = f / n_frames
            
            # Paleta Base: ouro-champanhe aeroespacial
            r = 60.0 + t_base * 175.0
            g = 45.0 + (t_base ** 1.3) * 140.0
            b = 14.0 + (t_base ** 2.0) * 60.0
            
            # Giroscópio 1: elipse inclinada precessando a velocidade 1.0
            rot1 = 2 * np.pi * t
            rx1 = (x_coords - cx) * np.cos(rot1) - (y_coords - cy) * np.sin(rot1)
            ry1 = (x_coords - cx) * np.sin(rot1) + (y_coords - cy) * np.cos(rot1)
            el1 = np.sqrt((rx1 / 1.0)**2 + (ry1 / 2.5)**2)
            gyro1 = np.exp(-((el1 - 4.5) / 0.8)**2)
            
            # Giroscópio 2: elipse perpendicular precessando em contra-rotação
            rot2 = -2 * np.pi * (t * 1.5)
            rx2 = (x_coords - cx) * np.cos(rot2) - (y_coords - cy) * np.sin(rot2)
            ry2 = (x_coords - cx) * np.sin(rot2) + (y_coords - cy) * np.cos(rot2)
            el2 = np.sqrt((rx2 / 2.5)**2 + (ry2 / 1.0)**2)
            gyro2 = np.exp(-((el2 - 4.0) / 0.8)**2)
            
            # Picos nos nós de gimbal lock
            nodes = (gyro1 * gyro2) * 2.0
            total_gyro = (gyro1 * 0.7 + gyro2 * 0.7 + nodes) * (t_base > 0.28)
            
            r += total_gyro * 165.0
            g += total_gyro * 135.0
            b += total_gyro * 50.0
            
            node_flash = np.clip(nodes - 0.6, 0, 1.2) * 110.0
            r += node_flash * 0.95
            g += node_flash * 0.95
            b += node_flash * 0.85
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "odyssey":
        # Opção 2 aprovada pelo autor: Nanite Swarm Self-Assembly (Enxame de Nanorrobôs em Auto-Montagem)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        for f in range(n_frames):
            frame = np.zeros((h, w, 4), dtype=np.float32)
            t = f / n_frames
            
            # Paleta Base: Superliga metalizada densa ciano-esmeralda
            r = 16.0 + t_base * 78.0
            g = 34.0 + (t_base ** 1.2) * 125.0
            b = 28.0 + (t_base ** 1.3) * 105.0
            
            # 4 núcleos móveis de enxame de nanites em órbitas Lissajous
            nanite_field = np.zeros((h, w), dtype=np.float32)
            
            attractors = [
                (cx + 4.2 * np.cos(2 * np.pi * t), cy + 4.2 * np.sin(2 * np.pi * t)),
                (cx + 4.5 * np.cos(-2 * np.pi * t * 1.5 + 1.2), cy + 3.2 * np.sin(-2 * np.pi * t * 1.5 + 1.2)),
                (cx + 3.0 * np.sin(2 * np.pi * t * 2.0), cy + 4.0 * np.cos(2 * np.pi * t * 2.0)),
                (cx + 3.8 * np.cos(2 * np.pi * t + np.pi), cy + 3.8 * np.sin(2 * np.pi * t + np.pi))
            ]
            
            for ax, ay in attractors:
                d = np.sqrt((x_coords - ax)**2 + (y_coords - ay)**2)
                nanite_field += np.exp(-((d / 1.6)**2)) * 1.1
                
            # Filamentos de montagem conectando os nanites
            interf = np.sin(nanite_field * 4.0 - 2 * np.pi * t * 2.0)
            assembly_mesh = (nanite_field * 0.8 + np.maximum(0, interf) * 0.6) * (t_base > 0.3)
            
            # Picos de solda a frio / sinterização nanotecnológica
            weld_flash = np.clip(assembly_mesh - 1.1, 0, 1.4) * 140.0
            
            # Cores: verde-menta elétrico e ciano brilhante
            r += assembly_mesh * 40.0 + weld_flash * 0.85
            g += assembly_mesh * 195.0 + weld_flash * 1.00
            b += assembly_mesh * 160.0 + weld_flash * 0.95
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "shijima":
        # Opção 2 aprovada pelo autor: Zen Silence Lotus Ripple (Ondulações do Vazio de Lótus Zen)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        angle = np.arctan2(y_coords - cy, x_coords - cx)
        
        for f in range(n_frames):
            frame = np.zeros((h, w, 4), dtype=np.float32)
            t = f / n_frames
            
            # Paleta Base: Prata pura celestial acetinada
            r = 40.0 + t_base * 190.0
            g = 48.0 + (t_base ** 1.1) * 192.0
            b = 68.0 + (t_base ** 1.15) * 187.0
            
            # Simetria de pétalas de lótus de 8 dobras
            lotus_mod = np.cos(8.0 * angle)
            r_lotus = dist * (1.0 + 0.22 * lotus_mod)
            
            # Onda de silêncio meditativo se expandindo suavemente
            wave = np.sin(2 * np.pi * (r_lotus / 4.2 - t * 1.5))
            ripple = np.exp(-((wave - 0.7) / 0.4)**2) * (t_base > 0.28)
            
            # Nós de quietude absoluta no centro
            zen_core = np.exp(-((dist / 3.2)**2)) * (0.6 + 0.4 * np.cos(2 * np.pi * t)) * (t_base > 0.35)
            
            total_zen = (ripple * 0.9 + zen_core * 1.1) * (t_base > 0.25)
            
            # Cores: azul-celeste translúcido e brilho prateado divino
            r += total_zen * 50.0
            g += total_zen * 110.0
            b += total_zen * 175.0
            
            zen_white = np.clip(total_zen - 0.7, 0, 1.2) * 120.0
            r += zen_white * 0.96
            g += zen_white * 0.98
            b += zen_white * 1.00
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "churitsu":
        # Opção 1 aprovada pelo autor: Neutral Dipole Yin-Yang Precession (Precessão de Dipolo Yin-Yang)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        angle = np.arctan2(y_coords - cy, x_coords - cx)
        
        for f in range(n_frames):
            t = f / n_frames
            
            # Paleta Base: Grafite monocromático metálico neutro (#828282)
            base_gray = 32.0 + t_base * 145.0
            r = base_gray.copy()
            g = base_gray.copy()
            b = base_gray.copy()
            
            # Dipolo rotativo Yin-Yang no plano da peça
            rot_angle = angle - 2 * np.pi * t
            dipole_wave = np.sin(rot_angle) * np.exp(-((dist - 4.5) / 2.5)**2)
            
            # Lóbulo positivo (platina brilhante) e lóbulo negativo (grafite denso)
            pos_lobe = np.maximum(0, dipole_wave) * (t_base > 0.28)
            neg_lobe = np.maximum(0, -dipole_wave) * (t_base > 0.28)
            
            # Ponto de aniquilação/equilíbrio central
            neutral_core = np.exp(-((dist / 2.2)**2)) * (0.5 + 0.5 * np.cos(4 * np.pi * t)) * (t_base > 0.35)
            
            total_fx = (pos_lobe * 1.5 - neg_lobe * 0.45 + neutral_core * 1.2)
            
            # Brilho neutro monocromático
            boost = total_fx * 95.0
            r += boost
            g += boost
            b += boost
            
            # Picos de equilíbrio supercrítico branco
            flash = np.clip(pos_lobe * 1.5 + neutral_core - 0.7, 0, 1.2) * 115.0
            r += flash
            g += flash
            b += flash
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "advanced_nitinol":
        # Opção 2 aprovada pelo autor: Shape-Memory Hysteresis Pulse (Pulso de Histerese com Memória de Forma)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        
        for f in range(n_frames):
            t = f / n_frames
            
            # Paleta Base: Ouro-bronze champanhe acetinado (#D2B48C)
            r = 48.0 + t_base * 162.0
            g = 35.0 + (t_base ** 1.2) * 145.0
            b = 18.0 + (t_base ** 1.4) * 122.0
            
            # Ciclo assimétrico de histerese: compressão lenta de estresse (70%) e disparo elástico (30%)
            if t < 0.7:
                phase_t = t / 0.7
                wave_rad = 7.0 * (1.0 - phase_t)
                hysteresis = np.exp(-((dist - wave_rad) / 1.5)**2) * 0.65
                shock = 0.0
            else:
                phase_t = (t - 0.7) / 0.3
                wave_rad = phase_t * 9.0
                hysteresis = 0.0
                shock = np.exp(-((dist - wave_rad) / 1.2)**2) * 1.5
                
            total_mem = (hysteresis + shock) * (t_base > 0.25)
            
            r += total_mem * 160.0
            g += total_mem * 130.0
            b += total_mem * 50.0
            
            flash = np.clip(shock - 0.8, 0, 1.4) * 120.0
            r += flash * 0.98
            g += flash * 0.95
            b += flash * 0.88
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "nitinol_60":
        # Opção 1: Cromo-Titânio Espelhado Anisotrópico (Hue Shift frio aeroespacial + Glint Estelar)
        for f in range(n_frames):
            phase = f / n_frames
            
            # Paleta com Hue Shift aeroespacial:
            # Sombra: Grafite cobalto frio (#202634)
            # Meio: Aço níquel polido límpido (#8898aa)
            # Destaque: Cromo espelhado puro (#e6edf5 -> #ffffff)
            r = 32.0 + t_base * 205.0
            g = 38.0 + (t_base ** 1.05) * 202.0
            b = 52.0 + (t_base ** 1.1) * 198.0
            
            # Glint anisotrópico nítido de superliga polida que varre a aresta
            sweep = (phase * 22.0) - 3.0
            diag = (x_coords + y_coords) * 0.5
            glint = np.exp(-((diag - sweep) / 1.0)**2) * (t_base > 0.6)
            
            # Glint estrela pontual no canto top-left
            star = 0.0
            if 8 <= f <= 11:
                st_dist = np.sqrt((x_coords - 3.0)**2 + (y_coords - 3.0)**2)
                star = np.exp(-(st_dist / 0.85)**2) * math.sin((f - 8) / 3.0 * math.pi)
                
            r += glint * 65.0 + star * 95.0
            g += glint * 70.0 + star * 95.0
            b += glint * 80.0 + star * 105.0
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))


    elif material_type == "superconductor_uiv_base":
        # Opção 1: Filamentos Quânticos de Supercorrente em Clusters (Zero-Resistance Neon)
        filaments = np.zeros((h, w), dtype=bool)
        filaments[4, 4:12] = True
        filaments[5:9, 7] = True
        filaments[8, 7:13] = True
        filaments[9:13, 10] = True
        filaments = filaments & alpha
        
        for f in range(n_frames):
            phase = f / n_frames
            tau = 2 * math.pi * phase
            
            # Paleta com Hue Shift:
            # Sombra: Índigo-violeta abissal (#1c0a2c)
            # Meio: Magenta cósmico puro (#b82294)
            # Destaque: Neon supercondutor (#ffa8f0 -> #ffffff)
            r = 35.0 + t_base * 195.0
            g = 10.0 + (t_base ** 1.8) * 115.0
            b = 55.0 + (t_base ** 1.3) * 165.0
            
            # Pulso ultra-rápido de supercorrente fluindo pelos filamentos
            pulse_pos = (phase * 18.0) % 12.0
            track_dist = (x_coords + y_coords * 0.8)
            current = np.exp(-((track_dist - (pulse_pos + 4.0)) / 1.2)**2) * filaments
            
            r += current * 125.0
            g += current * 115.0
            b += current * 135.0
            
            # Brilho chanfrado
            bevel = (y_coords <= x_coords) & (t_base > 0.65)
            glow = np.sin(tau) * 0.5 + 0.5
            r += bevel * (glow * 35.0 + 20.0)
            g += bevel * (glow * 15.0 + 10.0)
            b += bevel * (glow * 30.0 + 20.0)
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))


    elif material_type == "superconductor_umv_base":
        # Opção 1 aprovada pelo autor: Calabi-Yau Manifold Wormhole Tunneling (Micro-Buracos de Minhoca)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        dx = x_coords - cx
        dy = y_coords - cy
        r_dist = np.sqrt(dx**2 + dy**2)
        theta = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Púrpura/Violeta abissal multiversal (#B526CD)
            r = 38.0 + t_base * 145.0
            g = 8.0 + (t_base ** 1.35) * 32.0
            b = 48.0 + (t_base ** 1.05) * 162.0
            
            # Projeção 2D de micro-variedade de Calabi-Yau com 5 lóbulos dimensionais
            manifold = np.sin(5.0 * theta + tau) * np.cos(r_dist * 1.2 - tau * 0.7)
            wormhole_throat = np.exp(-((r_dist - (2.5 + 2.0 * np.sin(tau)))**2) / 1.2)
            
            tunnel_flux = np.abs(manifold) * (t_base > 0.25) * 1.3 + wormhole_throat * 1.5 * (t_base > 0.22)
            
            # Supercorrentes multiversais em trânsito instantâneo
            tunnel_flash = np.clip(tunnel_flux - 0.75, 0, 1.4) * (t_base > 0.3)
            
            total_fx = tunnel_flux * 0.85 + tunnel_flash * 1.1
            
            # Brilho violeta-choque neon e magenta dimensional
            r += total_fx * 78.0
            g += total_fx * 24.0
            b += total_fx * 92.0
            
            # Flashes singulares de tunelamento multiversal branco-estrela
            flash = np.clip(tunnel_flash - 0.4, 0, 1.5) * 105.0
            r += flash * 0.98
            g += flash * 0.92
            b += flash * 1.00
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "atomic_separation_catalyst":
        # Opção 2 aprovada pelo autor: Quark-Gluon Plasma Deconfinement (Plasma de Quarks e Glúons)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        dx = x_coords - cx
        dy = y_coords - cy
        r_dist = np.sqrt(dx**2 + dy**2)
        theta = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Fogo atômico de plasma de quarks (#e85e0c)
            r = 50.0 + t_base * 195.0
            g = 16.0 + (t_base ** 1.35) * 118.0
            b = 3.0 + (t_base ** 1.9) * 32.0
            
            # Vórtice elíptico relativístico SU(3) de viscosidade nula
            # 3 fluxos de carga de cor que giram em contra-fase no QGP
            flow1 = np.sin(3.0 * theta + r_dist * 0.9 - tau * 2.0)
            flow2 = np.cos(3.0 * theta - r_dist * 1.1 + tau * 2.0)
            gluon_vortex = np.exp(-((flow1 * flow2 - 0.3) / 0.35)**2) * (t_base > 0.25)
            
            # Núcleo de desconfinamento assintótico
            qgp_core = np.exp(-((r_dist / 2.8)**2)) * (1.0 + 0.6 * np.cos(tau * 3.0)) * (t_base > 0.3)
            
            total_qgp = (gluon_vortex * 1.1 + qgp_core * 1.3) * (t_base > 0.22)
            
            # Brilho de fogo cromodinâmico laranja-ouro
            r += total_qgp * 78.0
            g += total_qgp * 60.0
            b += total_qgp * 15.0
            
            # Flashes brancos de liberdade assintótica
            flash = np.clip(total_qgp - 1.1, 0, 1.4) * 105.0
            r += flash * 1.00
            g += flash * 0.98
            b += flash * 0.85
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "platinum_manganese_antimony_heusler_alloy":
        # Opção 2 aprovada pelo autor: Topological Chiral Skyrmion Lattice Drift & Hall Precession
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        # 3 vórtices de Skyrmion em coordenadas relativas com precessão de Hall em órbita elíptica
        skyrmion_radii = [4.2, 5.0, 4.6]
        skyrmion_phases = [0.0, 2.094, 4.188]  # 120° apart
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Prata-Manganês Magnética com gradiente quiral (#b0bcc8 / #e6e6e6)
            r = 28.0 + t_base * 150.0
            g = 32.0 + t_base * 160.0
            b = 44.0 + t_base * 178.0
            
            skyrmion_field = 0.0
            core_sparks = 0.0
            
            for sr, phase in zip(skyrmion_radii, skyrmion_phases):
                # Trajetória girotópica com ângulo de Hall de Skyrmion
                sk_x = cx + sr * np.cos(tau + phase)
                sk_y = cy + (sr * 0.72) * np.sin(tau + phase)
                
                dx = x_coords - sk_x
                dy = y_coords - sk_y
                dist = np.sqrt(dx**2 + dy**2)
                angle = np.arctan2(dy, dx)
                
                # Vórtice espiral quiral (Dzyaloshinskii-Moriya) com torção dextrogira
                chiral_spiral = np.sin(angle * 2.0 - dist * 1.45 + tau * 2.5) * np.exp(-dist / 3.4)
                
                # Núcleo magnético condensado (perpendicular ao plano)
                core = np.exp(-((dist / 1.15)**2)) * (1.2 + 0.65 * np.sin(tau * 3.0 + phase))
                
                skyrmion_field += np.clip(chiral_spiral, 0, 1.0) * 1.15 + core * 1.4
                core_sparks += core
                
            total_sk = skyrmion_field * (t_base > 0.2)
            
            # Luminescência de vórtice quiral em platina-aço
            r += total_sk * 62.0
            g += total_sk * 72.0
            b += total_sk * 90.0
            
            # Picos de energia topológica no núcleo do skyrmion
            flash = np.clip(core_sparks - 0.9, 0, 1.5) * 110.0
            r += flash * 1.00
            g += flash * 0.98
            b += flash * 1.00
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "stellar_alloy":
        # Opção 1 aprovada pelo autor: Photospheric Magnetoconvection & Solar Flares (Células Fotosféricas & Flares)
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Platina Estelar com tons de titânio (#c5ced8)
            # Núcleo denso metálico, relevo prateado
            r = 35.0 + t_base * 165.0
            g = 38.0 + t_base * 170.0
            b = 48.0 + t_base * 182.0
            
            # Rede de convecção de Bénard em padrão trigonal/hexagonal dinâmico
            c1 = np.sin(x_coords * 0.9 + tau) * np.cos(y_coords * 0.9 - tau * 0.5)
            c2 = np.sin((x_coords * 0.7 - y_coords * 0.7) + tau * 0.8)
            c3 = np.cos((x_coords * 0.5 + y_coords * 0.8) - tau * 1.2)
            granulation = (c1 + c2 + c3) / 3.0
            
            # Células de subida convectiva (quentes/ouro-estelar) vs bordas frias
            granules = np.exp(-((granulation - 0.4)**2) / 0.18) * (t_base > 0.22)
            
            # Reconexões magnéticas aleatórias ejetando micro-flares (relâmpagos solares)
            flare_trigger = np.sin(tau * 3.0) * np.cos(x_coords * 1.2 + y_coords * 0.6 + tau)
            flare = np.clip(flare_trigger - 0.7, 0, 1.0) * 2.5 * (t_base > 0.3)
            
            total_mhd = granules * 1.1 + flare * 1.4
            
            # Fulgor de ouro estelar e platina ionizada (#ffe164)
            r += total_mhd * 78.0
            g += total_mhd * 72.0
            b += total_mhd * 42.0
            
            # Picos incandescentes branco-solares nos flares
            flash = np.clip(total_mhd - 1.1, 0, 1.5) * 105.0
            r += flash * 1.00
            g += flash * 0.98
            b += flash * 0.90
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "trinaquadalloy":
        # Opção 2 aprovada pelo autor com paleta escurecida (quase preto puxado pro roxo):
        # Helical Fluxon Supercurrent Vortices (Hélice Dupla de Fluxons de Trinium e Naquadah)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        
        dx = x_coords - cx
        dy = y_coords - cy
        dist = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta "Quase preto puxado pro roxo" (#08040c a #251034)
            r = 5.0 + (t_base ** 1.3) * 32.0
            g = 2.0 + (t_base ** 1.5) * 14.0
            b = 8.0 + (t_base ** 1.2) * 44.0
            
            # Hélice dupla de supercorrentes girando em contra-fase ao redor do baricentro
            helix1 = np.sin(2.0 * angle + dist * 1.2 - tau * 2.5)
            helix2 = np.cos(2.0 * angle - dist * 1.2 + tau * 2.5)
            
            flux_violet = np.clip(helix1, 0, 1.0) * np.exp(-dist / 5.5) * (t_base > 0.25)
            flux_green = np.clip(helix2, 0, 1.0) * np.exp(-dist / 5.5) * (t_base > 0.25)
            
            # Filamentos sutis de Trinium (violeta escuro) e Naquadah (esmeralda radioativa)
            r += flux_violet * 45.0
            g += flux_violet * 8.0
            b += flux_violet * 65.0
            
            r += flux_green * 4.0
            g += flux_green * 50.0
            b += flux_green * 28.0
            
            # Ponto de ancoramento quântico central
            core_flux = np.exp(-((dist / 1.3)**2)) * (0.8 + 0.5 * np.sin(tau * 3.0)) * (t_base > 0.3)
            flash = np.clip(core_flux - 0.7, 0, 1.2) * 75.0
            r += flash * 0.85
            g += flash * 0.95
            b += flash * 0.90
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "mar_m_200_steel":
        # Opção 3 aprovada pelo autor:
        # Adiabatic Shear Banding & Dislocation Avalanches
        shear_lines = [
            (0.707, 0.707, 0.0),
            (0.866, -0.500, 2.09),
            (0.500, 0.866, 4.18)
        ]
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Aço-Carbono e Nióbio escuro (#515151)
            r = 23.0 + t_base * 104.0
            g = 24.0 + t_base * 107.0
            b = 26.0 + t_base * 112.0
            
            asb_total = 0.0
            for cos_a, sin_a, phase in shear_lines:
                proj = x_coords * cos_a + y_coords * sin_a
                # Onda de cisalhamento adiabático com disparo rápido e relaxamento térmico
                asb_wave = np.sin(proj * 1.4 - tau * 3.0 + phase)
                burst = np.exp(-((asb_wave - 0.85)**2) / 0.08)
                asb_total += burst
                
            total_shear = asb_total * (t_base > 0.22)
            
            # Brilho de fricção mecânica ultra-rápida em platina-aço
            r += total_shear * 68.0
            g += total_shear * 72.0
            b += total_shear * 85.0
            
            # Picos de temperatura localizada nos planos de escorregamento
            flash = np.clip(total_shear - 1.1, 0, 1.6) * 105.0
            r += flash * 1.00
            g += flash * 0.98
            b += flash * 0.96
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "hastelloy_n_75":
        # Opção 2 aprovada pelo autor:
        # Intergranular M₂₃C₆ Carbide Pinning & Laves Phase Network
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Olive-khaki greenish-gray matching casing ([89, 90, 66])
            r = 20.0 + t_base * 75.0
            g = 21.0 + t_base * 77.0
            b = 15.0 + t_base * 54.0
            
            # Rede celular intergranular de carbetos secundários M₂₃C₆ (tripla família de planos)
            w1 = np.sin(x_coords * 0.95 + y_coords * 0.55 - tau * 1.5)
            w2 = np.sin(-x_coords * 0.55 + y_coords * 0.95 + tau * 1.5)
            w3 = np.sin(x_coords * 0.70 - y_coords * 0.70 - tau * 1.0)
            
            carbide_net = np.abs(w1 * w2 + w2 * w3 + w3 * w1)
            carbides = np.clip(carbide_net * 0.8, 0, 1.2) * (t_base > 0.22)
            
            # Nós intermetálicos de fase de Laves (Ni₂Er / Fe₂Mo) nas junções triplas
            laves_nodes = np.exp(-((w1**2 + w2**2 + w3**2) / 0.55)) * (t_base > 0.25)
            
            # Khaki-sage / olive luster ao longo dos carbetos
            r += carbides * 36.0
            g += carbides * 40.0
            b += carbides * 28.0
            
            # Nós de ancoramento de fase de Laves em verde-oliva metálico iluminado
            r += laves_nodes * 48.0
            g += laves_nodes * 52.0
            b += laves_nodes * 38.0
            
            # Flashes pontuais nos nós de bloqueio de cisalhamento
            flash = np.clip(laves_nodes - 0.7, 0, 1.6) * 50.0
            r += flash * 0.92
            g += flash * 0.96
            b += flash * 0.75
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "stellite":
        # Opção 3 aprovada pelo autor:
        # High-Entropy Self-Healing Tribofilm & Haynes Stellar Gleam
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Cinza-Cobalto Estelar (#888192)
            r = 29.0 + t_base * 109.0
            g = 27.0 + t_base * 104.0
            b = 33.0 + t_base * 116.0
            
            # Fluxo laminar do tribofilme vítreo auto-regenerativo deslizando pela diagonal
            diag_flow = (x_coords * 0.707 + y_coords * 0.707) - tau * 2.8
            flow_wave = np.sin(diag_flow)
            tribofilm = np.clip(flow_wave, 0, 1.0) * (t_base > 0.22)
            
            # Brilho estelar pontual itinerante ("Haynes Stellar Gleam")
            pos_x = 4.0 + 8.0 * (0.5 + 0.5 * np.cos(tau))
            pos_y = 4.0 + 8.0 * (0.5 + 0.5 * np.sin(tau))
            d_gleam = np.sqrt((x_coords - pos_x)**2 + (y_coords - pos_y)**2)
            
            # Difração estelar cruciforme (+)
            gleam_core = np.exp(-(d_gleam**2) / 1.5)
            gleam_cross_x = np.exp(-((x_coords - pos_x)**2) / 0.6) * np.exp(-((y_coords - pos_y)**2) / 8.0)
            gleam_cross_y = np.exp(-((y_coords - pos_y)**2) / 0.6) * np.exp(-((x_coords - pos_x)**2) / 8.0)
            stellar_gleam = (gleam_core * 1.2 + (gleam_cross_x + gleam_cross_y) * 0.8) * (t_base > 0.25)
            
            # Realce lilás-prateado do tribofilme vítreo
            r += tribofilm * 55.0
            g += tribofilm * 52.0
            b += tribofilm * 75.0
            
            # Brilho estelar incandescente puro nos raios de difração
            r += stellar_gleam * 110.0
            g += stellar_gleam * 110.0
            b += stellar_gleam * 125.0
            
            flash = np.clip(stellar_gleam - 0.7, 0, 1.5) * 85.0
            r += flash * 1.00
            g += flash * 1.00
            b += flash * 1.00
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "indalloy_140":
        # Opção 1 aprovada pelo autor:
        # Eutectic Capillary Marangoni Convection & Wetting Fronts
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dx = x_coords - cx
        dy = y_coords - cy
        dist = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Azul-Ardósia Slate Blue (#6a5acd)
            r = 22.0 + t_base * 84.0
            g = 18.0 + t_base * 72.0
            b = 42.0 + t_base * 163.0
            
            # Frentes capilares com instabilidade de Saffman-Taylor (dedos de Marangoni)
            fingering = np.cos(5.0 * angle + np.sin(dist * 0.8 - tau * 2.0)) * 1.2
            marangoni_wave = np.sin(dist * 1.3 - tau * 2.5 + fingering)
            wetting = np.clip(marangoni_wave, 0, 1.0) * (t_base > 0.22)
            
            # Meniscos capilares de alta tensão superficial nos pontos de contato
            meniscus = np.exp(-((marangoni_wave - 0.75)**2) / 0.08) * (t_base > 0.25)
            
            # Realce azul-ciano elétrico de molhamento
            r += wetting * 45.0
            g += wetting * 75.0
            b += wetting * 85.0
            
            # Brilho de menisco em prata-índio pura
            r += meniscus * 85.0
            g += meniscus * 92.0
            b += meniscus * 98.0
            
            # Flashes nos vértices do menisco capilar
            flash = np.clip(meniscus - 0.72, 0, 1.5) * 100.0
            r += flash * 0.95
            g += flash * 0.98
            b += flash * 1.00
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "end_steel":
        # Opção 2 aprovada pelo autor:
        # Non-Euclidean Hyperbolic Poincaré Tessellation & Ender Resonances
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dx = (x_coords - cx) / 7.5
        dy = (y_coords - cy) / 7.5
        r_sq = dx**2 + dy**2
        # Métrica de Poincaré conformada
        r_hyp = 2.0 * np.sqrt(r_sq) / np.maximum(0.1, 1.0 - r_sq * 0.6)
        theta = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base: Amarelo-Verde Pálido (#d6d980)
            r = 40.0 + t_base * 174.0
            g = 43.0 + t_base * 174.0
            b = 18.0 + t_base * 110.0
            
            # Tesselação hiperbólica {7,3} deformada derivando angularmente
            tess = np.sin(7.0 * theta + r_hyp * 2.0 - tau * 2.5) * np.cos(r_hyp * 1.5 + tau * 1.5)
            hyp_rings = np.clip(tess, 0, 1.2) * (t_base > 0.22)
            
            # Vórtices de ressonância de Poincaré
            poincare_core = np.exp(-((r_hyp - 1.2 - 0.5 * np.sin(tau * 2.0))**2) / 0.15) * (t_base > 0.25)
            
            # Realce ouro-espectral
            r += hyp_rings * 50.0
            g += hyp_rings * 52.0
            b += hyp_rings * 20.0
            
            # Vórtices violeta-obsidiana hiperbólicos
            r += poincare_core * 60.0
            g += poincare_core * 30.0
            b += poincare_core * 90.0
            
            # Flashes estelares nos nós de Poincaré
            flash = np.clip(hyp_rings * poincare_core - 0.35, 0, 1.6) * 110.0
            r += flash * 1.00
            g += flash * 1.00
            b += flash * 0.90
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "dark_steel":
        # Opção 3 aprovada pelo autor:
        # Void-Absorbing Obsidian Acoustic Resonance & Gravitational Shadow
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dx = x_coords - cx
        dy = y_coords - cy
        r_dist = np.sqrt(dx**2 + dy**2)
        theta = np.arctan2(dy, dx)
        
        for f in range(n_frames):
            t = f / n_frames
            tau = 2 * np.pi * t
            
            # Paleta Base Dark Steel: Grafite-Vácuo com Matriz de Absorção
            r = 14.0 + t_base * 74.0
            g = 15.0 + t_base * 78.0
            b = 20.0 + t_base * 92.0
            
            # 1. Ondas acústicas centrípetas de absorção (sugadas em espiral para o centro)
            centripetal_radius = (r_dist + tau * 1.8) % 8.0
            absorption_ring = np.exp(-((centripetal_radius - 4.0)**2) / 0.8) * (t_base > 0.20)
            
            # 2. Modulação em espiral de momento angular óptico (vórtice de Casimir)
            spiral_phase = np.sin(3.0 * theta + r_dist * 1.5 - tau * 2.5)
            spiral_trap = np.clip(spiral_phase, 0, 1.2) * (t_base > 0.22)
            
            # 3. Gradiente de absorção de luz (escurecimento por armadilha de fótons)
            shadow_dip = np.clip(1.0 - 0.35 * spiral_trap, 0.4, 1.0)
            r *= shadow_dip
            g *= shadow_dip
            b *= shadow_dip
            
            # 4. Emissão Cherenkov ressonante em violeta-obsidiana profundo nas bordas de escape
            cherenkov_ring = absorption_ring * (t_base > 0.25)
            r += cherenkov_ring * 42.0
            g += cherenkov_ring * 16.0
            b += cherenkov_ring * 68.0
            
            # 5. Reflexos nos limites do horizonte de escape em violeta elétrico e prata
            violet_glow = spiral_trap * 0.7
            r += violet_glow * 32.0
            g += violet_glow * 14.0
            b += violet_glow * 55.0
            
            # 6. Micro-flashes de horizonte de eventos
            flash = np.clip(cherenkov_ring * spiral_trap - 0.45, 0, 1.5) * 110.0
            r += flash * 0.95
            g += flash * 0.92
            b += flash * 1.05
            
            frame = np.zeros((h, w, 4), dtype=np.uint8)
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "draconium":
        # Opção 3 aprovada pelo autor: Draconic Rune Pulse & Lattice (Batimento Cardíaco Bio-Mecânico)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        
        # Linhas de rede hexagonal / rúnica
        hex1 = np.abs((x_coords * 1.0 + y_coords * 0.577) % 3.6 - 1.8)
        hex2 = np.abs((x_coords * 1.0 - y_coords * 0.577) % 3.6 - 1.8)
        hex3 = np.abs((y_coords * 1.155) % 3.6 - 1.8)
        lattice_lines = np.exp(-np.minimum(np.minimum(hex1, hex2), hex3) * 2.5) * (t_base > 0.28)
        
        for f in range(n_frames):
            frame = np.zeros_like(base_arr)
            t = f / n_frames
            
            # Paleta Base: grafite-ametista temperado
            r = 16.0 + t_base * 70.0
            g = 4.0 + (t_base ** 1.3) * 18.0
            b = 30.0 + t_base * 115.0
            
            # Função de batimento cardíaco biológico (sístole + diástole rápida)
            t_phase = (t - dist / 16.0) % 1.0
            beat1 = np.exp(-((t_phase - 0.22) / 0.05)**2) * 1.2
            beat2 = np.exp(-((t_phase - 0.38) / 0.045)**2) * 0.85
            heartbeat = beat1 + beat2
            
            # Pulso na rede hexagonal
            lattice_glow = lattice_lines * (0.35 + 0.85 * heartbeat)
            
            # Choque no núcleo central durante o batimento
            core_shock = np.exp(-dist / 3.0) * heartbeat * 1.1
            
            # Picos de arco elétrico nos nós da rede
            nodes = (lattice_lines > 0.5) * heartbeat * 0.9
            
            total_beat = lattice_glow + core_shock + nodes
            
            # Cores: violeta elétrico incandescente
            r += total_beat * 145.0
            g += total_beat * 30.0
            b += total_beat * 215.0
            
            # Picos de choque lilás-branco
            white_shock = np.clip(total_beat - 0.8, 0, 1.2) * 95.0
            r += white_shock * 0.9
            g += white_shock * 0.85
            b += white_shock * 1.0
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "awakened_draconium":
        # Opção 1 aprovada pelo autor: Draconic Core Fusion (Fusão Solar & Arcos Coronais)
        cy = np.sum(np.where(alpha, y_coords, 0)) / max(1, np.sum(alpha))
        cx = np.sum(np.where(alpha, x_coords, 0)) / max(1, np.sum(alpha))
        dist = np.sqrt((x_coords - cx)**2 + (y_coords - cy)**2)
        max_d = max(1.0, np.max(dist[alpha])) if np.sum(alpha) > 0 else 8.0
        norm_dist = dist / max_d

        for f in range(n_frames):
            frame = np.zeros_like(base_arr)
            t = f / n_frames
            
            # Base de metal dracônico bronze/âmbar incandescente
            r = 56.0 + t_base * 170.0
            g = 12.0 + (t_base ** 1.4) * 85.0
            b = 2.0 + (t_base ** 2.2) * 20.0
            
            # 1. Pulso do núcleo térmico central (respiração térmica solar)
            pulse = (np.sin(2 * np.pi * t) * 0.5 + 0.5) ** 1.8
            core_heat = np.exp(-norm_dist * 2.8) * (0.65 + 0.45 * pulse) * (t_base > 0.25)
            
            # 2. Arcos coronais giratórios (loops magnéticos de plasma)
            angle = np.arctan2(y_coords - cy, x_coords - cx)
            coronal_wave1 = np.sin(angle * 2.0 - 2 * np.pi * t * 1.5 + norm_dist * 4.0)
            coronal_loop1 = np.exp(-((coronal_wave1 - 0.7) / 0.35) ** 2) * (norm_dist > 0.2) * (norm_dist < 0.85)
            
            coronal_wave2 = np.cos(angle * 3.0 + 2 * np.pi * t * 2.0 - norm_dist * 3.0)
            coronal_loop2 = np.exp(-((coronal_wave2 - 0.6) / 0.4) ** 2) * (norm_dist > 0.3) * (norm_dist < 0.9)
            
            loops = (coronal_loop1 * 0.6 + coronal_loop2 * 0.4) * (0.5 + 0.5 * t_base)
            
            # 3. Flare estelar transitório
            flare_t = (t * 2.0) % 1.0
            flare_int = (np.sin(np.pi * flare_t) ** 12) * np.exp(-norm_dist * 1.5) * 1.2
            
            total_plasma = core_heat * 1.3 + loops * 0.85 + flare_int * 0.95
            
            r += total_plasma * 180.0
            g += total_plasma * 140.0
            b += total_plasma * 65.0
            
            white_core = np.clip(total_plasma - 0.9, 0, 1.5) * 120.0
            r += white_core * 0.9
            g += white_core * 0.95
            b += white_core * 0.85
            
            frame[:, :, 0] = np.clip(np.where(alpha, r, 0), 0, 255)
            frame[:, :, 1] = np.clip(np.where(alpha, g, 0), 0, 255)
            frame[:, :, 2] = np.clip(np.where(alpha, b, 0), 0, 255)
            frame[:, :, 3] = base_arr[:, :, 3]
            stacked_frames.append(frame.astype(np.uint8))

    elif material_type == "cosmic_neutronium":
        colored_rgb = palette_cosmic_neutronium(gray)
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        valid_coords = np.argwhere((alpha) & (t_base > 0.35))
        np.random.seed(999)
        star_pts = [valid_coords[i % len(valid_coords)] for i in [3, 14, 25, 41, 58, 72, 85]] if len(valid_coords) > 90 else []
        star_phases = [0.0, 0.15, 0.32, 0.48, 0.65, 0.80, 0.92]
        star_colors = [
            (255, 120, 180),
            (120, 220, 255),
            (255, 230, 140),
            (180, 140, 255),
            (140, 255, 200),
            (255, 255, 255),
            (255, 160, 120)
        ]
        r_c = np.sqrt((x_coords - 7.5)**2 + (y_coords - 7.5)**2)
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            lensing = np.sin(2 * np.pi * (t * 1.5 + r_c / 5.0)) * 12.0
            frame[:, :, 0] += lensing * 0.6
            frame[:, :, 1] += lensing * 0.8
            frame[:, :, 2] += lensing * 1.2
            
            for (sy, sx), sp, scol in zip(star_pts, star_phases, star_colors):
                glint = max(0.0, np.cos(((t - sp) % 1.0) * 2 * np.pi)) ** 8
                if glint > 0.05:
                    for dy, dx, weight in [(0, 0, 1.0), (0, 1, 0.4), (0, -1, 0.4), (1, 0, 0.4), (-1, 0, 0.4)]:
                        ny, nx = sy + dy, sx + dx
                        if 0 <= ny < h and 0 <= nx < w and alpha[ny, nx]:
                            v = glint * weight
                            frame[ny, nx, 0] += v * scol[0]
                            frame[ny, nx, 1] += v * scol[1]
                            frame[ny, nx, 2] += v * scol[2]
                            
            for c in range(3):
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            stacked_frames.append(frame.astype(np.uint8))

    else:
        if material_type == "white_dwarf":
            colored_rgb = palette_white_dwarf(gray)
            edge_mask = np.clip((gray / 255.0 - 0.22) / 0.78, 0, 1)
            direction = 1.0
            boost_rgb = (0.85, 0.95, 1.15)
            amp = 45.0
        elif material_type == "hypogen":
            colored_rgb = palette_hypogen_bronze(gray)
            edge_mask = np.clip((gray / 255.0 - 0.20) / 0.80, 0, 1)
            direction = 1.0
            boost_rgb = (1.15, 0.95, 0.50)
            amp = 42.0
        else:  # black_dwarf
            colored_rgb = palette_black_dwarf(gray, style=bd_style)
            edge_mask = np.clip((gray / 255.0 - 0.18) / 0.82, 0, 1)
            direction = -1.0
            amp = 40.0
            boost_rgb = (0.95, 1.00, 1.15) if bd_style == "obsidian" else (0.90, 0.70, 1.40)
                
        colored = np.zeros_like(base_arr)
        colored[:, :, :3] = colored_rgb
        colored[:, :, 3] = base_arr[:, :, 3]
        
        for f in range(n_frames):
            frame = colored.copy()
            t = f / n_frames
            
            wave1 = np.sin(2 * np.pi * (direction * t + (x_coords + y_coords) / 18.0))
            wave2 = np.cos(2 * np.pi * (direction * t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
            interf = (wave1 + wave2) * 0.5
            
            intensity = interf * amp * edge_mask
            
            for c in range(3):
                frame[:, :, c] += intensity * boost_rgb[c]
                frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
                
            stacked_frames.append(frame.astype(np.uint8))
        
    full_strip = np.vstack(stacked_frames)
    return Image.fromarray(full_strip, mode="RGBA")


def apply_item_shader(model_json, material_type, item_name=""):
    if material_type in ("awakened_draconium", "ichorium"):
        model_json["loader"] = "gtna:halo"
        model_json["textures"]["halo"] = "gtna:item/effect/halo"
        model_json["halo"] = {"texture": "#halo", "color": -1, "size": 4, "pulse": False}
    elif material_type == "draconium":
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 11546879,
            "width": 1.5
        }
    elif material_type in ("tengam_purified", "tengam_attuned"):
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 14024576 if material_type == "tengam_attuned" else 12513904,
            "width": 1.5
        }
    elif material_type == "fallking":
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 16764779,
            "width": 1.5
        }
    elif material_type == "odyssey":
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 2999487,
            "width": 1.5
        }
    elif material_type == "shijima":
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 12900082,
            "width": 1.5
        }
    elif material_type == "churitsu":
        model_json["loader"] = "gtna:glow_edge"
        model_json["glow_edge"] = {
            "color": 15066597,
            "width": 1.5
        }
    elif material_type in (
        "advanced_nitinol", "nitinol_60", "superconductor_uiv_base",
        "superconductor_umv_base", "atomic_separation_catalyst",
        "platinum_manganese_antimony_heusler_alloy", "stellar_alloy",
        "trinaquadalloy", "mar_m_200_steel", "hastelloy_n_75",
        "stellite", "indalloy_140", "end_steel", "dark_steel"
    ):
        model_json["loader"] = "gtna:halo"
        model_json["textures"]["halo"] = "gtna:item/effect/halo_noise"
        model_json["halo"] = {"texture": "#halo", "color": -1, "size": 4, "pulse": False}


    profiles = json.loads((ROOT / "tools/material_effect_profiles.json").read_text())
    if material_type in profiles:
        profile = profiles[material_type]
        model_json["textures"]["halo"] = profile["texture"]
        model_json["halo"] = {**profile, "texture": "#halo"}

def generate_set(set_name, material_type="white_dwarf", bd_style="obsidian"):
    if material_type == "universium":
        from apply_modernity_universium_with_shaders import apply
        apply()
        return
    if not set_name.startswith("gtna_"):
        set_name = f"gtna_{set_name}"
    out_items = ROOT / f"src/main/resources/assets/gtceu/textures/item/material_sets/{set_name}"
    out_blocks = ROOT / f"src/main/resources/assets/gtceu/textures/block/material_sets/{set_name}"
    model_items = ROOT / f"src/main/resources/assets/gtceu/models/item/material_sets/{set_name}"
    model_blocks = ROOT / f"src/main/resources/assets/gtceu/models/block/material_sets/{set_name}"
    
    out_items.mkdir(parents=True, exist_ok=True)
    out_blocks.mkdir(parents=True, exist_ok=True)
    model_items.mkdir(parents=True, exist_ok=True)
    model_blocks.mkdir(parents=True, exist_ok=True)
    
    print(f"Gerando material set '{set_name}' (tipo: {material_type})...")
    
    mcmeta_content = json.dumps({"animation": {"frametime": 2, "interpolate": False if material_type == "six_phased_copper" else True}}, indent=2) + "\n"
    
    # Itens
    for src_name, dst_name in STANDARD_ITEMS.items():
        src_file = MODERNITY_ITEMS / f"{src_name}.png"
        custom_ov = None
        
        if dst_name.startswith("ingot") and material_type in INGOT_TEMPLATES:
            profile = INGOT_TEMPLATES[material_type]
            profile_file = MODERNITY_ICONSETS / profile / f"{src_name}.png"
            if profile_file.exists():
                src_file = profile_file
                profile_ov = MODERNITY_ICONSETS / profile / f"{src_name}_OVERLAY.png"
                if profile_ov.exists():
                    custom_ov = profile_ov
                    
        if not src_file.exists():
            print(f"  [AVISO] Arquivo ausente: {src_file}")
            continue
            
        base_im = Image.open(src_file)
        anim_strip = animate(base_im, material_type=material_type, bd_style=bd_style)
        
        # Determinar todos os nomes (camelCase e snake_case)
        names_to_save = {dst_name, src_name}
        if dst_name == "gear_small":
            names_to_save.update(["gearSmall", "gearGtSmall"])
        elif dst_name == "gear":
            names_to_save.add("gearGt")
        elif dst_name == "rod_long":
            names_to_save.update(["rodLong", "stickLong"])
        elif dst_name == "rod":
            names_to_save.add("stick")
        elif dst_name == "spring_small":
            names_to_save.add("springSmall")
        elif dst_name == "turbine_blade":
            names_to_save.add("turbineBlade")
        elif dst_name == "dust_small":
            names_to_save.add("dustSmall")
        elif dst_name == "dust_tiny":
            names_to_save.add("dustTiny")
        elif dst_name == "ingot_hot":
            names_to_save.add("ingotHot")
        elif dst_name == "wire_fine":
            names_to_save.add("wireFine")

        # Overlay apropriado
        if dst_name == "wire_fine" or src_name == "wireFine":
            ov_file = MODERNITY_ITEMS / "wireFine_OVERLAY.png"
            if ov_file.exists():
                ov_im = Image.open(ov_file).convert("RGBA")
            else:
                ov_im = Image.open(GTCEU_DULL_ITEMS / "wire_fine_overlay.png").convert("RGBA")
        elif custom_ov and custom_ov.exists():
            ov_im = Image.open(custom_ov).convert("RGBA")
        else:
            ov_im = EMPTY_16
            
        for alias in names_to_save:
            anim_strip.save(out_items / f"{alias}.png")
            (out_items / f"{alias}.png.mcmeta").write_text(mcmeta_content)
            EMPTY_16.save(out_items / f"{alias}_secondary.png")
            ov_im.save(out_items / f"{alias}_overlay.png")
            
            model_json = {
                "parent": "item/generated",
                "textures": {
                    "layer0": f"gtceu:item/material_sets/{set_name}/{alias}",
                    "layer1": f"gtceu:item/material_sets/{set_name}/{alias}_secondary",
                    "layer2": f"gtceu:item/material_sets/{set_name}/{alias}_overlay"
                }
            }
            apply_item_shader(model_json, material_type, alias)
            (model_items / f"{alias}.json").write_text(json.dumps(model_json, indent=2) + "\n")
        
    # Singularity
    dull_sing = GTCEU_DULL_ITEMS / "singularity.png"
    dull_sing_ov = GTCEU_DULL_ITEMS / "singularity_overlay.png"
    if dull_sing.exists() and dull_sing_ov.exists():
        c_core = Image.open(dull_sing).convert("RGBA").crop((0, 0, 16, 16))
        c_ring = Image.open(dull_sing_ov).convert("RGBA").crop((0, 0, 16, 16))
        sing_base = Image.alpha_composite(c_core, c_ring)
        sing_strip = animate(sing_base, material_type=material_type, bd_style=bd_style)
        sing_strip.save(out_items / "singularity.png")
        (out_items / "singularity.png.mcmeta").write_text(mcmeta_content)
        EMPTY_16.save(out_items / "singularity_secondary.png")
        EMPTY_16.save(out_items / "singularity_overlay.png")
        
        s_model = {
            "parent": "item/generated",
            "textures": {
                "layer0": f"gtceu:item/material_sets/{set_name}/singularity",
                "layer1": f"gtceu:item/material_sets/{set_name}/singularity_secondary",
                "layer2": f"gtceu:item/material_sets/{set_name}/singularity_overlay"
            }
        }
        apply_item_shader(s_model, material_type, "singularity")
        (model_items / "singularity.json").write_text(json.dumps(s_model, indent=2) + "\n")
        
    print(f"  ✓ Itens gerados (incluindo singularity e variantes camelCase).")
    
    # Blocos padrão (cubo e frame)
    for src_name, dst_name in STANDARD_BLOCKS.items():
        src_file = MODERNITY_BLOCKS / f"{src_name}.png"
        if not src_file.exists():
            print(f"  [AVISO] Bloco ausente: {src_file}")
            continue
            
        base_im = Image.open(src_file)
        anim_strip = animate(base_im, material_type=material_type, bd_style=bd_style)
        
        block_aliases = {dst_name, src_name}
        if dst_name == "frame_gt":
            block_aliases.add("frameGt")
            
        for b_name in block_aliases:
            anim_strip.save(out_blocks / f"{b_name}.png")
            (out_blocks / f"{b_name}.png.mcmeta").write_text(mcmeta_content)
            EMPTY_16.save(out_blocks / f"{b_name}_secondary.png")
            
            icon = f"gtceu:block/material_sets/{set_name}/{b_name}"
            model_json = {
                "parent": "block/block",
                "loader": "forge:composite",
                "textures": {"particle": icon},
                "children": {
                    "base": {
                        "parent": "gtceu:block/cube/tinted/all_0",
                        "render_type": "cutout" if "frame" in b_name else "solid",
                        "textures": {"all": icon}
                    },
                    "secondary": {
                        "parent": "gtceu:block/cube/tinted/all",
                        "render_type": "translucent",
                        "textures": {"all": icon + "_secondary"}
                    }
                },
                "item_render_order": ["base", "secondary"]
            }
            (model_blocks / f"{b_name}.json").write_text(json.dumps(model_json, indent=2) + "\n")
        
    # Tubulações de Fluido (Pipes)
    pipe_count = 0
    for src_pipe, dst_pipe in PIPE_BLOCKS.items():
        p_src = MODERNITY_BLOCKS / f"{src_pipe}.png"
        if p_src.exists():
            p_base = Image.open(p_src).convert("RGBA")
            p_strip = animate(p_base, material_type=material_type, bd_style=bd_style)
            for p_alias in (dst_pipe, src_pipe):
                p_strip.save(out_blocks / f"{p_alias}.png")
                (out_blocks / f"{p_alias}.png.mcmeta").write_text(mcmeta_content)
            pipe_count += 1
            
    # Cabos / Fios (Wires)
    wire_count = 0
    for wire_file in ("wire_side", "wire_end"):
        w_src = GTCEU_DULL_BLOCKS / f"{wire_file}.png"
        if w_src.exists():
            w_base = Image.open(w_src).convert("RGBA").crop((0, 0, 16, 16))
            w_strip = animate(w_base, material_type=material_type, bd_style=bd_style)
            camel_wire = "wireSide" if wire_file == "wire_side" else "wireEnd"
            for w_alias in (wire_file, camel_wire):
                w_strip.save(out_blocks / f"{w_alias}.png")
                (out_blocks / f"{w_alias}.png.mcmeta").write_text(mcmeta_content)
                EMPTY_16.save(out_blocks / f"{w_alias}_overlay.png")
            wire_count += 1
            
    # Fluidos (Liquid / Molten)
    fluid_count = 0
    for fluid_file in ("liquid", "molten"):
        fl_src = GTCEU_DULL_BLOCKS / f"{fluid_file}.png"
        if fl_src.exists():
            fl_base = Image.open(fl_src).convert("RGBA").crop((0, 0, 16, 16))
            fl_strip = animate(fl_base, material_type=material_type, bd_style=bd_style)
            fl_strip.save(out_blocks / f"{fluid_file}.png")
            (out_blocks / f"{fluid_file}.png.mcmeta").write_text(mcmeta_content)
            fluid_count += 1
            
    print(f"  ✓ Blocos gerados: {len(STANDARD_BLOCKS)} base, {pipe_count} pipes, {wire_count} wires, {fluid_count} fluidos.")
    print(f"Concluído com sucesso para '{set_name}'!")


if __name__ == "__main__":
    ALL_CHOICES = [
        "white_dwarf", "black_dwarf", "hypogen", "dragon_metal", "chromatic_glass",
        "celestial_tungsten", "astral_titanium", "six_phased_copper", "rhugnor",
        "shirabon", "quantum", "metastable_oganesson", "transcendent_metal", "creon", "mellion",
        "echoite", "universium", "ichorium", "tengam_purified", "tengam_attuned",
        "fallking", "odyssey", "draconium", "awakened_draconium", "cosmic_neutronium",
        "shijima", "churitsu", "advanced_nitinol", "nitinol_60", "superconductor_uiv_base",
        "superconductor_umv_base", "atomic_separation_catalyst",
        "platinum_manganese_antimony_heusler_alloy", "stellar_alloy", "trinaquadalloy",
        "mar_m_200_steel", "hastelloy_n_75", "stellite", "indalloy_140", "end_steel",
        "dark_steel", "all_new", "all"
    ]
    parser = argparse.ArgumentParser(description="Gerador de Material Sets Animados do GTNA")
    parser.add_argument("--material", choices=ALL_CHOICES, required=True,
                        help="Material a gerar (ou 'all' / 'all_new')")
    parser.add_argument("--style", choices=["void", "crimson", "obsidian"], default="obsidian",
                        help="Estilo visual (para black_dwarf)")
    args = parser.parse_args()
    
    name_map = {
        "white_dwarf": "gtna_white_dwarf_matter",
        "black_dwarf": "gtna_black_dwarf_matter",
        "hypogen": "gtna_hypogen",
        "dragon_metal": "gtna_dragon_metal",
        "chromatic_glass": "gtna_chromatic_glass",
        "celestial_tungsten": "gtna_celestial_tungsten",
        "astral_titanium": "gtna_astral_titanium",
        "six_phased_copper": "gtna_six_phased_copper",
        "rhugnor": "gtna_rhugnor",
        "shirabon": "gtna_shirabon",
        "quantum": "gtna_quantum",
        "metastable_oganesson": "gtna_metastable_oganesson",
        "transcendent_metal": "gtna_transcendent_metal",
        "creon": "gtna_creon",
        "mellion": "gtna_mellion",
        "echoite": "gtna_echoite",
        "universium": "gtna_universium",
        "ichorium": "gtna_ichorium",
        "tengam_purified": "gtna_tengam_purified",
        "tengam_attuned": "gtna_tengam_attuned",
        "fallking": "gtna_fallking",
        "odyssey": "gtna_odyssey",
        "draconium": "gtna_draconium",
        "awakened_draconium": "gtna_awakened_draconium",
        "cosmic_neutronium": "gtna_cosmic_neutronium",
        "shijima": "gtna_shijima",
        "churitsu": "gtna_churitsu",
        "advanced_nitinol": "gtna_advanced_nitinol",
        "nitinol_60": "gtna_nitinol_60",
        "superconductor_uiv_base": "gtna_superconductor_uiv_base",
        "superconductor_umv_base": "gtna_superconductor_umv_base",
        "atomic_separation_catalyst": "gtna_atomic_separation_catalyst",
        "platinum_manganese_antimony_heusler_alloy": "gtna_platinum_manganese_antimony_heusler_alloy",
        "stellar_alloy": "gtna_stellar_alloy",
        "trinaquadalloy": "gtna_trinaquadalloy",
        "mar_m_200_steel": "gtna_mar_m_200_steel",
        "hastelloy_n_75": "gtna_hastelloy_n_75",
        "stellite": "gtna_stellite",
        "indalloy_140": "gtna_indalloy_140",
        "end_steel": "gtna_end_steel",
        "dark_steel": "gtna_dark_steel"
    }
    
    if args.material == "all":
        for m, s in name_map.items():
            generate_set(s, material_type=m, bd_style=args.style)
    elif args.material == "all_new":
        new_mats = [
            "echoite", "ichorium", "tengam_purified", "tengam_attuned",
            "fallking", "odyssey", "draconium", "awakened_draconium", "cosmic_neutronium",
            "shijima", "churitsu", "advanced_nitinol", "nitinol_60", "superconductor_uiv_base",
            "superconductor_umv_base", "atomic_separation_catalyst",
            "platinum_manganese_antimony_heusler_alloy", "stellar_alloy", "trinaquadalloy",
            "mar_m_200_steel", "hastelloy_n_75", "stellite", "indalloy_140", "end_steel",
            "dark_steel"
        ]
        for m in new_mats:
            generate_set(name_map[m], material_type=m, bd_style=args.style)
    else:
        generate_set(name_map[args.material], material_type=args.material, bd_style=args.style)

