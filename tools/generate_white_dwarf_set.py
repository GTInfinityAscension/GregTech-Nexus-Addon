import os
import json
import numpy as np
from PIL import Image
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERNITY_ITEMS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
MODERNITY_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")

OUT_ITEMS = ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/white_dwarf_matter"
OUT_BLOCKS = ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets/white_dwarf_matter"
MODEL_ITEMS = ROOT / "src/main/resources/assets/gtceu/models/item/material_sets/white_dwarf_matter"
MODEL_BLOCKS = ROOT / "src/main/resources/assets/gtceu/models/block/material_sets/white_dwarf_matter"

OUT_ITEMS.mkdir(parents=True, exist_ok=True)
OUT_BLOCKS.mkdir(parents=True, exist_ok=True)
MODEL_ITEMS.mkdir(parents=True, exist_ok=True)
MODEL_BLOCKS.mkdir(parents=True, exist_ok=True)

# Complete mapping from Modernity filenames to GTCEu names
ITEM_MAPPING = {
    # Bars & Smelting
    "ingot": "ingot",
    "ingotDouble": "ingot_double",
    "ingotTriple": "ingot_triple",
    "ingotQuadruple": "ingot_quadruple",
    "ingotQuintuple": "ingot_quintuple",
    "ingotHot": "ingot_hot",
    "nugget": "nugget",
    
    # Plates & Foils
    "plate": "plate",
    "plateDouble": "plate_double",
    "plateTriple": "plate_triple",
    "plateQuadruple": "plate_quadruple",
    "plateQuintuple": "plate_quintuple",
    "plateDense": "plate_dense",
    "plateSuperdense": "plate_superdense",
    "foil": "foil",
    
    # Rods & Fasteners
    "stick": "rod",
    "stickLong": "rod_long",
    "bolt": "bolt",
    "screw": "screw",
    "round": "round",
    "ring": "ring",
    
    # Mechanisms & Rotors
    "gearGt": "gear",
    "gearGtSmall": "gear_small",
    "rotor": "rotor",
    "spring": "spring",
    "springSmall": "spring_small",
    
    # Wires, Blades, Optics
    "wireFine": "wire_fine",
    "turbineBlade": "turbine_blade",
    "lens": "lens",
    
    # Powders & Ores
    "dust": "dust",
    "dustSmall": "dust_small",
    "dustTiny": "dust_tiny",
    "dustPure": "dust_pure",
    "dustImpure": "dust_impure",
    "crushed": "crushed",
    "crushedPurified": "crushed_purified",
    "crushedCentrifuged": "crushed_refined",
    "oreRaw": "raw_ore",
    
    # Gems
    "gem": "gem",
    "gemChipped": "gem_chipped",
    "gemFlawed": "gem_flawed",
    "gemFlawless": "gem_flawless",
    "gemExquisite": "gem_exquisite",
    
    # Tool Heads
    "toolHeadSword": "tool_head_sword",
    "toolHeadPickaxe": "tool_head_pickaxe",
    "toolHeadShovel": "tool_head_shovel",
    "toolHeadAxe": "tool_head_axe",
    "toolHeadHoe": "tool_head_hoe",
    "toolHeadHammer": "tool_head_hammer",
    "toolHeadFile": "tool_head_file",
    "toolHeadSaw": "tool_head_saw",
    "toolHeadBuzzSaw": "tool_head_buzz_saw",
    "toolHeadDrill": "tool_head_drill",
    "toolHeadChainsaw": "tool_head_chainsaw",
    "toolHeadSense": "tool_head_scythe",
    "toolHeadScrewdriver": "tool_head_screwdriver",
    "toolHeadWrench": "tool_head_wrench"
}

BLOCK_MAPPING = {
    "block1": "block",
    "frameGt": "frame_gt"
}

def to_celestial_palette(arr):
    res = np.zeros_like(arr)
    res[:, :, 3] = arr[:, :, 3]
    gray = arr[:, :, 0]
    
    t = gray / 255.0
    # Shadow: [60, 64, 92] (deep cosmic indigo-silver)
    # Midtone: [208, 222, 240] (bright star silver with slight cool sheen)
    # Highlight: [255, 255, 255] (pure brilliant white)
    mask_low = t < 0.4
    s_low = np.clip(t / 0.4, 0, 1)
    r_low = 60 + s_low * (208 - 60)
    g_low = 64 + s_low * (222 - 64)
    b_low = 92 + s_low * (240 - 92)
    
    s_high = np.clip((t - 0.4) / 0.6, 0, 1)
    r_high = 208 + s_high * (255 - 208)
    g_high = 222 + s_high * (255 - 222)
    b_high = 240 + s_high * (255 - 240)
    
    res[:, :, 0] = np.where(mask_low, r_low, r_high)
    res[:, :, 1] = np.where(mask_low, g_low, g_high)
    res[:, :, 2] = np.where(mask_low, b_low, b_high)
    return res

def animate_resonance(base_im, n_frames=30):
    base_arr = np.array(base_im.convert("RGBA"), dtype=np.float32)
    # In case the source has frames, take the top 16x16
    h_orig, w_orig = base_arr.shape[:2]
    if h_orig > w_orig:
        base_arr = base_arr[:w_orig, :, :]
    
    h, w = base_arr.shape[:2]
    colored = to_celestial_palette(base_arr)
    alpha = colored[:, :, 3] > 0
    
    # Precompute coordinates
    y_coords, x_coords = np.ogrid[:h, :w]
    t_base = base_arr[:, :, 0] / 255.0
    edge_mask = np.clip((t_base - 0.22) / 0.78, 0, 1)
    
    stacked_frames = []
    for f in range(n_frames):
        frame = colored.copy()
        t = f / n_frames
        
        # Dual harmonic interference wave
        wave1 = np.sin(2 * np.pi * (t + (x_coords + y_coords) / 18.0))
        wave2 = np.cos(2 * np.pi * (t * 2 - (x_coords * 1.5 - y_coords) / 14.0))
        interf = (wave1 + wave2) * 0.5
        
        boost = interf * 45.0 * edge_mask
        
        # Shimmer tint
        frame[:, :, 0] += boost * 0.85
        frame[:, :, 1] += boost * 0.95
        frame[:, :, 2] += boost * 1.15
        
        for c in range(3):
            frame[:, :, c] = np.where(alpha, np.clip(frame[:, :, c], 0, 255), 0)
            
        stacked_frames.append(frame.astype(np.uint8))
        
    full_strip = np.vstack(stacked_frames)
    return Image.fromarray(full_strip, mode="RGBA")

empty_16 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
mcmeta_content = json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=2) + "\n"

# Process Items
processed_items = 0
for src_name, dst_name in ITEM_MAPPING.items():
    src_file = MODERNITY_ITEMS / f"{src_name}.png"
    if not src_file.exists():
        print(f"WARNING: Missing item {src_file}")
        continue
    
    base_im = Image.open(src_file)
    anim_strip = animate_resonance(base_im)
    
    # Save base animated strip
    dst_tex = OUT_ITEMS / f"{dst_name}.png"
    anim_strip.save(dst_tex)
    
    # Save mcmeta
    dst_meta = OUT_ITEMS / f"{dst_name}.png.mcmeta"
    dst_meta.write_text(mcmeta_content)
    
    # Save secondary and overlay
    (OUT_ITEMS / f"{dst_name}_secondary.png").write_bytes(Path("/dev/null").read_bytes() if False else b"")
    empty_16.save(OUT_ITEMS / f"{dst_name}_secondary.png")
    empty_16.save(OUT_ITEMS / f"{dst_name}_overlay.png")
    
    # Save item model JSON
    model_json = {
        "parent": "item/generated",
        "textures": {
            "layer0": f"gtceu:item/material_sets/white_dwarf_matter/{dst_name}",
            "layer1": f"gtceu:item/material_sets/white_dwarf_matter/{dst_name}_secondary",
            "layer2": f"gtceu:item/material_sets/white_dwarf_matter/{dst_name}_overlay"
        }
    }
    (MODEL_ITEMS / f"{dst_name}.json").write_text(json.dumps(model_json, indent=2) + "\n")
    processed_items += 1

print(f"Processed {processed_items} items!")

# Process Blocks
processed_blocks = 0
for src_name, dst_name in BLOCK_MAPPING.items():
    src_file = MODERNITY_BLOCKS / f"{src_name}.png"
    if not src_file.exists():
        print(f"WARNING: Missing block {src_file}")
        continue
        
    base_im = Image.open(src_file)
    anim_strip = animate_resonance(base_im)
    
    dst_tex = OUT_BLOCKS / f"{dst_name}.png"
    anim_strip.save(dst_tex)
    
    dst_meta = OUT_BLOCKS / f"{dst_name}.png.mcmeta"
    dst_meta.write_text(mcmeta_content)
    
    empty_16.save(OUT_BLOCKS / f"{dst_name}_secondary.png")
    
    icon = f"gtceu:block/material_sets/white_dwarf_matter/{dst_name}"
    model_json = {
        "parent": "block/block",
        "loader": "forge:composite",
        "textures": {"particle": icon},
        "children": {
            "base": {
                "parent": "gtceu:block/cube/tinted/all_0",
                "render_type": "cutout" if dst_name == "frame_gt" else "solid",
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
    (MODEL_BLOCKS / f"{dst_name}.json").write_text(json.dumps(model_json, indent=2) + "\n")
    processed_blocks += 1

print(f"Processed {processed_blocks} blocks!")
