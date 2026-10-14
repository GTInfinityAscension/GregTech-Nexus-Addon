import shutil
import json
from pathlib import Path
from PIL import Image
import numpy as np

REPO_ROOT = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
ITEM_TEX_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets"
BLOCK_TEX_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets"
ITEM_MODEL_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/models/item/material_sets"
BLOCK_MODEL_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/models/block/material_sets"

WD_DIR = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/items/materialicons/CUSTOM/WhiteDwarfMatter")
WD_BLOCKS = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures/blocks/materialicons/CUSTOM/WhiteDwarfMatter")
GTCEU_DULL_BLOCKS = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/block/material_sets/dull")
GTCEU_DULL_ITEMS = REPO_ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/dull"
AXONIUM_BLOCK = Path("/home/raishxn/MineProjects/TST/src/main/resources/assets/gtnhcommunitymod/textures/blocks/MetalBlock/BlockAxonium.png")

dummy_1x1 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))

# Authentic 115-pixel wooden spool bobbin overlay for fine wires
if (WD_DIR / "wireFine_OVERLAY.png").exists():
    WOODEN_SPOOL = Image.open(WD_DIR / "wireFine_OVERLAY.png").convert("RGBA")
else:
    WOODEN_SPOOL = Image.open(GTCEU_DULL_ITEMS / "wire_fine_overlay.png").convert("RGBA")

ITEMS_MAP = {
    'ingot': 'ingot.png',
    'ingot_hot': 'ingotHot.png',
    'ingot_double': 'ingotDouble.png',
    'ingot_triple': 'ingotTriple.png',
    'ingot_quadruple': 'ingotQuadruple.png',
    'ingot_quintuple': 'ingotQuintuple.png',
    'plate': 'plate.png',
    'plate_double': 'plateDouble.png',
    'plate_triple': 'plateTriple.png',
    'plate_quadruple': 'plateQuadruple.png',
    'plate_quintuple': 'plateQuintuple.png',
    'plate_dense': 'plateDense.png',
    'plate_superdense': 'plateSuperdense.png',
    'gear': 'gearGt.png',
    'gear_small': 'gearGtSmall.png',
    'rod': 'stick.png',
    'rod_long': 'stickLong.png',
    'nugget': 'nugget.png',
    'dust': 'dust.png',
    'dust_small': 'dustSmall.png',
    'dust_tiny': 'dustTiny.png',
    'foil': 'foil.png',
    'ring': 'ring.png',
    'round': 'round.png',
    'bolt': 'bolt.png',
    'screw': 'screw.png',
    'spring': 'spring.png',
    'spring_small': 'springSmall.png',
    'wire_fine': 'wireFine.png',
    'rotor': 'rotor.png',
    'turbine_blade': 'turbineBlade.png',
    'gem': 'gem.png'
}

PIPES_MAP = {
    'pipe_side': 'pipeSide.png',
    'pipe_tiny': 'pipeTiny.png',
    'pipe_small': 'pipeSmall.png',
    'pipe_medium': 'pipeMedium.png',
    'pipe_large': 'pipeLarge.png',
    'pipe_huge': 'pipeHuge.png',
    'pipe_quadruple': 'pipeQuadruple.png',
    'pipe_nonuple': 'pipeNonuple.png'
}

# Directories
chaos_tex_dir = ITEM_TEX_ROOT / "gtna_chaos_matter"
chaos_model_dir = ITEM_MODEL_ROOT / "gtna_chaos_matter"
chaos_block_dir = BLOCK_TEX_ROOT / "gtna_chaos_matter"
chaos_block_model_dir = BLOCK_MODEL_ROOT / "gtna_chaos_matter"

axon_tex_dir = ITEM_TEX_ROOT / "gtna_axonium"
axon_model_dir = ITEM_MODEL_ROOT / "gtna_axonium"
axon_block_dir = BLOCK_TEX_ROOT / "gtna_axonium"
axon_block_model_dir = BLOCK_MODEL_ROOT / "gtna_axonium"

for d in (chaos_tex_dir, chaos_model_dir, chaos_block_dir, chaos_block_model_dir,
          axon_tex_dir, axon_model_dir, axon_block_dir, axon_block_model_dir):
    d.mkdir(parents=True, exist_ok=True)

# Helper to process an item base image
def process_item(item, filename, tmpl):
    t_arr = np.array(tmpl.convert("RGBA"), dtype=np.float32)
    gray = t_arr[:, :, 0]
    alpha = t_arr[:, :, 3] > 0
    t_norm = gray / 255.0
    
    camel_name = filename.replace(".png", "")
    aliases = {item, camel_name}
    if item == "gear_small":
        aliases.update(["gearSmall", "gearGtSmall"])
    elif item == "gear":
        aliases.add("gearGt")
    elif item == "rod_long":
        aliases.update(["rodLong", "stickLong"])
    elif item == "rod":
        aliases.add("stick")
    elif item == "spring_small":
        aliases.add("springSmall")
    elif item == "turbine_blade":
        aliases.add("turbineBlade")
    elif item == "dust_small":
        aliases.add("dustSmall")
    elif item == "dust_tiny":
        aliases.add("dustTiny")
    elif item == "ingot_hot":
        aliases.add("ingotHot")
    elif item == "wire_fine":
        aliases.add("wireFine")
    
    # 1. Chaos Matter
    # Deep pitch black void: #050508 to #181024
    c_r = np.where(alpha, 8.0 + t_norm * 20.0, 0)
    c_g = np.where(alpha, 6.0 + t_norm * 14.0, 0)
    c_b = np.where(alpha, 14.0 + t_norm * 32.0, 0)
    chaos_base = Image.fromarray(np.dstack([c_r, c_g, c_b, t_arr[:, :, 3]]).astype(np.uint8))
    
    if item in ('wire_fine', 'wireFine'):
        chaos_ov = WOODEN_SPOOL
    else:
        ov_r = np.where(alpha & (t_norm > 0.75), 180.0, 0)
        ov_g = np.where(alpha & (t_norm > 0.75), 30.0, 0)
        ov_b = np.where(alpha & (t_norm > 0.75), 90.0, 0)
        ov_a = np.where(alpha & (t_norm > 0.75), 220, 0)
        chaos_ov = Image.fromarray(np.dstack([ov_r, ov_g, ov_b, ov_a]).astype(np.uint8))
        
    for alias in aliases:
        chaos_base.save(chaos_tex_dir / f"{alias}.png")
        chaos_ov.save(chaos_tex_dir / f"{alias}_overlay.png")
        dummy_1x1.save(chaos_tex_dir / f"{alias}_secondary.png")
        c_model = {
            "parent": "item/generated",
            "textures": {
                "layer0": f"gtceu:item/material_sets/gtna_chaos_matter/{alias}",
                "layer1": f"gtceu:item/material_sets/gtna_chaos_matter/{alias}_secondary",
                "layer2": f"gtceu:item/material_sets/gtna_chaos_matter/{alias}_overlay"
            },
            "loader": "gtna:unstable",
            "unstable": {
                "mask": "gtna:mask/cosmic_wire_fine" if alias in ("wire_fine", "wireFine") else "gtna:mask/cosmic"
            }
        }
        (chaos_model_dir / f"{alias}.json").write_text(json.dumps(c_model, indent=2) + "\n")
    
    # 2. Axonium
    # Radiant harmonic gold: #e5b83b to #fff2a8
    a_r = np.where(alpha, 160.0 + t_norm * 95.0, 0)
    a_g = np.where(alpha, 120.0 + t_norm * 115.0, 0)
    a_b = np.where(alpha, 35.0 + t_norm * 140.0, 0)
    axon_base = Image.fromarray(np.dstack([a_r, a_g, a_b, t_arr[:, :, 3]]).astype(np.uint8))
    
    if item in ('wire_fine', 'wireFine'):
        axon_ov = WOODEN_SPOOL
    else:
        a_ov_r = np.where(alpha & (t_norm > 0.7), 255.0, 0)
        a_ov_g = np.where(alpha & (t_norm > 0.7), 245.0, 0)
        a_ov_b = np.where(alpha & (t_norm > 0.7), 200.0, 0)
        a_ov_a = np.where(alpha & (t_norm > 0.7), 210, 0)
        axon_ov = Image.fromarray(np.dstack([a_ov_r, a_ov_g, a_ov_b, a_ov_a]).astype(np.uint8))
        
    for alias in aliases:
        axon_base.save(axon_tex_dir / f"{alias}.png")
        axon_ov.save(axon_tex_dir / f"{alias}_overlay.png")
        dummy_1x1.save(axon_tex_dir / f"{alias}_secondary.png")
        a_model = {
            "parent": "item/generated",
            "textures": {
                "layer0": f"gtceu:item/material_sets/gtna_axonium/{alias}",
                "layer1": f"gtceu:item/material_sets/gtna_axonium/{alias}_secondary",
                "layer2": f"gtceu:item/material_sets/gtna_axonium/{alias}_overlay"
            },
            "loader": "gtna:glow_edge",
            "glow": {
                "color": 16766720,
                "width": 1.5
            }
        }
        (axon_model_dir / f"{alias}.json").write_text(json.dumps(a_model, indent=2) + "\n")

# Process all standard items
for item, filename in ITEMS_MAP.items():
    tmpl_path = WD_DIR / filename
    if tmpl_path.exists():
        process_item(item, filename, Image.open(tmpl_path))

# Process Singularity
dull_sing = GTCEU_DULL_ITEMS / "singularity.png"
dull_sing_ov = GTCEU_DULL_ITEMS / "singularity_overlay.png"
if dull_sing.exists() and dull_sing_ov.exists():
    c_core = Image.open(dull_sing).convert("RGBA").crop((0, 0, 16, 16))
    c_ring = Image.open(dull_sing_ov).convert("RGBA").crop((0, 0, 16, 16))
    sing_comp = Image.alpha_composite(c_core, c_ring)
    process_item("singularity", "singularity.png", sing_comp)

# Process Blocks
def tint_block(tmpl, out_chaos, out_axon):
    t_arr = np.array(tmpl.convert("RGBA"), dtype=np.float32)
    gray = t_arr[:, :, 0]
    alpha = t_arr[:, :, 3] > 0
    t_norm = gray / 255.0
    
    c_r = np.where(alpha, 8.0 + t_norm * 20.0, 0)
    c_g = np.where(alpha, 6.0 + t_norm * 14.0, 0)
    c_b = np.where(alpha, 14.0 + t_norm * 32.0, 0)
    Image.fromarray(np.dstack([c_r, c_g, c_b, t_arr[:, :, 3]]).astype(np.uint8)).save(out_chaos)
    
    a_r = np.where(alpha, 160.0 + t_norm * 95.0, 0)
    a_g = np.where(alpha, 120.0 + t_norm * 115.0, 0)
    a_b = np.where(alpha, 35.0 + t_norm * 140.0, 0)
    Image.fromarray(np.dstack([a_r, a_g, a_b, t_arr[:, :, 3]]).astype(np.uint8)).save(out_axon)

# Block
chaos_blk = Image.new("RGBA", (16, 16), (10, 8, 16, 255))
chaos_blk.save(chaos_block_dir / "block.png")
dummy_1x1.save(chaos_block_dir / "block_secondary.png")

if AXONIUM_BLOCK.exists():
    shutil.copy2(AXONIUM_BLOCK, axon_block_dir / "block.png")
else:
    Image.new("RGBA", (16, 16), (230, 185, 60, 255)).save(axon_block_dir / "block.png")
dummy_1x1.save(axon_block_dir / "block_secondary.png")

for s_name, b_dir, m_dir in (("gtna_chaos_matter", chaos_block_dir, chaos_block_model_dir),
                             ("gtna_axonium", axon_block_dir, axon_block_model_dir)):
    b_model = {
        "parent": "block/block",
        "loader": "forge:composite",
        "textures": {"particle": f"gtceu:block/material_sets/{s_name}/block"},
        "children": {
            "base": {
                "parent": "gtceu:block/cube/tinted/all_0",
                "render_type": "solid",
                "textures": {"all": f"gtceu:block/material_sets/{s_name}/block"}
            },
            "secondary": {
                "parent": "gtceu:block/cube/tinted/all",
                "render_type": "translucent",
                "textures": {"all": f"gtceu:block/material_sets/{s_name}/block_secondary"}
            }
        },
        "item_render_order": ["base", "secondary"]
    }
    (m_dir / "block.json").write_text(json.dumps(b_model, indent=2) + "\n")

# Frame GT (both frame_gt and frameGt)
frame_src = WD_BLOCKS / "frameGt.png"
if frame_src.exists():
    tint_block(Image.open(frame_src), chaos_block_dir / "frame_gt.png", axon_block_dir / "frame_gt.png")
    tint_block(Image.open(frame_src), chaos_block_dir / "frameGt.png", axon_block_dir / "frameGt.png")
else:
    dummy_1x1.save(chaos_block_dir / "frame_gt.png")
    dummy_1x1.save(chaos_block_dir / "frameGt.png")
    dummy_1x1.save(axon_block_dir / "frame_gt.png")
    dummy_1x1.save(axon_block_dir / "frameGt.png")
dummy_1x1.save(chaos_block_dir / "frame_gt_secondary.png")
dummy_1x1.save(chaos_block_dir / "frameGt_secondary.png")
dummy_1x1.save(axon_block_dir / "frame_gt_secondary.png")
dummy_1x1.save(axon_block_dir / "frameGt_secondary.png")

for s_name, m_dir in (("gtna_chaos_matter", chaos_block_model_dir), ("gtna_axonium", axon_block_model_dir)):
    for f_alias in ("frame_gt", "frameGt"):
        f_model = {
            "parent": "block/block",
            "loader": "forge:composite",
            "textures": {"particle": f"gtceu:block/material_sets/{s_name}/{f_alias}"},
            "children": {
                "base": {
                    "parent": "gtceu:block/cube/tinted/all_0",
                    "render_type": "cutout",
                    "textures": {"all": f"gtceu:block/material_sets/{s_name}/{f_alias}"}
                },
                "secondary": {
                    "parent": "gtceu:block/cube/tinted/all",
                    "render_type": "translucent",
                    "textures": {"all": f"gtceu:block/material_sets/{s_name}/{f_alias}_secondary"}
                }
            },
            "item_render_order": ["base", "secondary"]
        }
        (m_dir / f"{f_alias}.json").write_text(json.dumps(f_model, indent=2) + "\n")

# Pipes (both snake_case and camelCase)
for dst_name, src_file in PIPES_MAP.items():
    p_src = WD_BLOCKS / src_file
    if p_src.exists():
        im = Image.open(p_src)
        camel_pipe = src_file.replace(".png", "")
        for p_alias in (dst_name, camel_pipe):
            tint_block(im, chaos_block_dir / f"{p_alias}.png", axon_block_dir / f"{p_alias}.png")

# Wires (both snake_case and camelCase)
for wire_file in ("wire_side", "wire_end"):
    w_src = GTCEU_DULL_BLOCKS / f"{wire_file}.png"
    if w_src.exists():
        im = Image.open(w_src).crop((0, 0, 16, 16))
        camel_wire = "wireSide" if wire_file == "wire_side" else "wireEnd"
        for w_alias in (wire_file, camel_wire):
            tint_block(im, chaos_block_dir / f"{w_alias}.png", axon_block_dir / f"{w_alias}.png")
            dummy_1x1.save(chaos_block_dir / f"{w_alias}_overlay.png")
            dummy_1x1.save(axon_block_dir / f"{w_alias}_overlay.png")

# Fluids
for fluid_file in ("liquid", "molten"):
    fl_src = GTCEU_DULL_BLOCKS / f"{fluid_file}.png"
    if fl_src.exists():
        im = Image.open(fl_src).crop((0, 0, 16, 16))
        tint_block(im, chaos_block_dir / f"{fluid_file}.png", axon_block_dir / f"{fluid_file}.png")

print("Chaos Matter and Axonium generated successfully with all items and blocks (dual naming included)!")
