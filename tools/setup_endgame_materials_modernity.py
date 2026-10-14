import os
import shutil
import json
from pathlib import Path
from PIL import Image

REPO_ROOT = Path("/home/raishxn/MineProjects/GregTech-Nexus-Addon")
MOD_ROOT = Path("/home/raishxn/Downloads/Modernity-GTNH-2026-09-07/assets/gregtech/textures")
ITEM_TEX_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets"
BLOCK_TEX_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets"
ITEM_MODEL_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/models/item/material_sets"
BLOCK_MODEL_ROOT = REPO_ROOT / "src/main/resources/assets/gtceu/models/block/material_sets"

WD_ITEMS = MOD_ROOT / "items/materialicons/CUSTOM/WhiteDwarfMatter"
WD_BLOCKS = MOD_ROOT / "blocks/materialicons/CUSTOM/WhiteDwarfMatter"
GTCEU_DULL_BLOCKS = Path("/home/raishxn/MineProjects/GTCEu-7.5.3/src/main/resources/assets/gtceu/textures/block/material_sets/dull")
GTCEU_DULL_ITEMS = REPO_ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets/dull"

dummy_1x1 = Image.new("RGBA", (16, 16), (0, 0, 0, 0))

# Authentic 115-pixel wooden spool bobbin overlay for fine wires
if (WD_ITEMS / "wireFine_OVERLAY.png").exists():
    WOODEN_SPOOL = Image.open(WD_ITEMS / "wireFine_OVERLAY.png").convert("RGBA")
else:
    WOODEN_SPOOL = Image.open(GTCEU_DULL_ITEMS / "wire_fine_overlay.png").convert("RGBA")

mapping = [
    ('ingot', 'ingot.png', 'ingot_OVERLAY.png'),
    ('ingot_hot', 'ingotHot.png', 'ingotHot_OVERLAY.png'),
    ('ingot_double', 'ingotDouble.png', 'ingotDouble_OVERLAY.png'),
    ('ingot_triple', 'ingotTriple.png', 'ingotTriple_OVERLAY.png'),
    ('ingot_quadruple', 'ingotQuadruple.png', 'ingotQuadruple_OVERLAY.png'),
    ('ingot_quintuple', 'ingotQuintuple.png', 'ingotQuintuple_OVERLAY.png'),
    ('plate', 'plate.png', 'plate_OVERLAY.png'),
    ('plate_double', 'plateDouble.png', 'plateDouble_OVERLAY.png'),
    ('plate_triple', 'plateTriple.png', 'plateTriple_OVERLAY.png'),
    ('plate_quadruple', 'plateQuadruple.png', 'plateQuadruple_OVERLAY.png'),
    ('plate_quintuple', 'plateQuintuple.png', 'plateQuintuple_OVERLAY.png'),
    ('plate_dense', 'plateDense.png', 'plateDense_OVERLAY.png'),
    ('plate_superdense', 'plateSuperdense.png', 'plateSuperdense_OVERLAY.png'),
    ('gear', 'gearGt.png', 'gearGt_OVERLAY.png'),
    ('gear_small', 'gearGtSmall.png', 'gearGtSmall_OVERLAY.png'),
    ('rod', 'stick.png', 'stick_OVERLAY.png'),
    ('rod_long', 'stickLong.png', 'stickLong_OVERLAY.png'),
    ('nugget', 'nugget.png', 'nugget_OVERLAY.png'),
    ('dust', 'dust.png', 'dust_OVERLAY.png'),
    ('dust_small', 'dustSmall.png', 'dustSmall_OVERLAY.png'),
    ('dust_tiny', 'dustTiny.png', 'dustTiny_OVERLAY.png'),
    ('foil', 'foil.png', 'foil_OVERLAY.png'),
    ('ring', 'ring.png', 'ring_OVERLAY.png'),
    ('round', 'round.png', 'round_OVERLAY.png'),
    ('bolt', 'bolt.png', 'bolt_OVERLAY.png'),
    ('screw', 'screw.png', 'screw_OVERLAY.png'),
    ('spring', 'spring.png', 'spring_OVERLAY.png'),
    ('spring_small', 'springSmall.png', 'springSmall_OVERLAY.png'),
    ('wire_fine', 'wireFine.png', 'wireFine_OVERLAY.png'),
    ('rotor', 'rotor.png', 'rotor_OVERLAY.png'),
    ('turbine_blade', 'turbineBlade.png', 'turbineBlade_OVERLAY.png'),
    ('gem', 'gem.png', 'gem_OVERLAY.png'),
]

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

def apply_shader(model_data, loader_name, item_name, mask_name):
    if not loader_name:
        return
    model_data["loader"] = loader_name
    if loader_name == "gtna:cosmic":
        model_data["cosmic"] = {
            "mask": "gtna:mask/cosmic_wire_fine" if item_name in ("wire_fine", "wireFine") else mask_name
        }
    elif loader_name == "gtna:eternal":
        model_data["eternal"] = {
            "mask": mask_name
        }
    elif loader_name == "gtna:unstable":
        model_data["unstable"] = {
            "mask": mask_name
        }
    elif loader_name == "gtna:halo":
        name = model_data["textures"]["layer0"].split("/")[-2].removeprefix("gtna_")
        profile = json.loads((REPO_ROOT / "tools/material_effect_profiles.json").read_text())[name]
        model_data["textures"]["halo"] = profile["texture"]
        model_data["halo"] = {**profile, "texture": "#halo"}

def port_material(set_name, mod_folder, loader_name, custom_block_path=None, mask_name="gtna:mask/cosmic"):
    src_items = MOD_ROOT / f"items/materialicons/CUSTOM/{mod_folder}"
    src_blocks = MOD_ROOT / f"blocks/materialicons/CUSTOM/{mod_folder}"
    
    dest_item_tex = ITEM_TEX_ROOT / set_name
    dest_block_tex = BLOCK_TEX_ROOT / set_name
    dest_item_model = ITEM_MODEL_ROOT / set_name
    dest_block_model = BLOCK_MODEL_ROOT / set_name
    
    dest_item_tex.mkdir(parents=True, exist_ok=True)
    dest_block_tex.mkdir(parents=True, exist_ok=True)
    dest_item_model.mkdir(parents=True, exist_ok=True)
    dest_block_model.mkdir(parents=True, exist_ok=True)
    
    for name, base_file, ov_file in mapping:
        p_base = src_items / base_file
        if not p_base.exists():
            p_base = WD_ITEMS / base_file
            
        p_ov = src_items / ov_file
        
        # Determine all aliases (camelCase and snake_case)
        camel_name = base_file.replace(".png", "")
        aliases = {name, camel_name}
        if name == "gear_small":
            aliases.update(["gearSmall", "gearGtSmall"])
        elif name == "gear":
            aliases.add("gearGt")
        elif name == "rod_long":
            aliases.update(["rodLong", "stickLong"])
        elif name == "rod":
            aliases.add("stick")
        elif name == "spring_small":
            aliases.add("springSmall")
        elif name == "turbine_blade":
            aliases.add("turbineBlade")
        elif name == "dust_small":
            aliases.add("dustSmall")
        elif name == "dust_tiny":
            aliases.add("dustTiny")
        elif name == "ingot_hot":
            aliases.add("ingotHot")
        elif name == "wire_fine":
            aliases.add("wireFine")
            
        # Load or generate base texture
        if p_base.exists():
            base_img = Image.open(p_base).convert("RGBA")
            mcmeta_base = p_base.with_name(p_base.name + ".mcmeta")
            mcmeta_content = mcmeta_base.read_text() if mcmeta_base.exists() else None
        else:
            base_img = dummy_1x1
            mcmeta_content = None
            
        # Determine overlay
        if name in ("wire_fine", "wireFine"):
            overlay_img = WOODEN_SPOOL
            mcmeta_ov_content = None
        elif p_ov.exists():
            overlay_img = Image.open(p_ov).convert("RGBA")
            mcm_ov = p_ov.with_name(p_ov.name + ".mcmeta")
            mcmeta_ov_content = mcm_ov.read_text() if mcm_ov.exists() else None
        else:
            overlay_img = dummy_1x1
            mcmeta_ov_content = None
            
        for alias in aliases:
            base_img.save(dest_item_tex / f"{alias}.png")
            if mcmeta_content:
                (dest_item_tex / f"{alias}.png.mcmeta").write_text(mcmeta_content)
                
            overlay_img.save(dest_item_tex / f"{alias}_overlay.png")
            if mcmeta_ov_content:
                (dest_item_tex / f"{alias}_overlay.png.mcmeta").write_text(mcmeta_ov_content)
                
            dummy_1x1.save(dest_item_tex / f"{alias}_secondary.png")
            
            # Model JSON
            model_data = {
                "parent": "item/generated",
                "textures": {
                    "layer0": f"gtceu:item/material_sets/{set_name}/{alias}",
                    "layer1": f"gtceu:item/material_sets/{set_name}/{alias}_secondary",
                    "layer2": f"gtceu:item/material_sets/{set_name}/{alias}_overlay"
                }
            }
            apply_shader(model_data, loader_name, alias, mask_name)
            (dest_item_model / f"{alias}.json").write_text(json.dumps(model_data, indent=2) + "\n")
        
    # Singularity
    dull_sing = GTCEU_DULL_ITEMS / "singularity.png"
    dull_sing_ov = GTCEU_DULL_ITEMS / "singularity_overlay.png"
    if dull_sing.exists() and dull_sing_ov.exists():
        c_core = Image.open(dull_sing).convert("RGBA").crop((0, 0, 16, 16))
        c_ring = Image.open(dull_sing_ov).convert("RGBA").crop((0, 0, 16, 16))
        sing_comp = Image.alpha_composite(c_core, c_ring)
        sing_comp.save(dest_item_tex / "singularity.png")
        dummy_1x1.save(dest_item_tex / "singularity_secondary.png")
        dummy_1x1.save(dest_item_tex / "singularity_overlay.png")
        sing_model = {
            "parent": "item/generated",
            "textures": {
                "layer0": f"gtceu:item/material_sets/{set_name}/singularity",
                "layer1": f"gtceu:item/material_sets/{set_name}/singularity_secondary",
                "layer2": f"gtceu:item/material_sets/{set_name}/singularity_overlay"
            }
        }
        apply_shader(sing_model, loader_name, "singularity", mask_name)
        (dest_item_model / "singularity.json").write_text(json.dumps(sing_model, indent=2) + "\n")

    # Blocks
    block_aliases = {"block"}
    if custom_block_path and custom_block_path.exists():
        shutil.copy2(custom_block_path, dest_block_tex / "block.png")
        mcm = custom_block_path.with_name(custom_block_path.name + ".mcmeta")
        if mcm.exists():
            shutil.copy2(mcm, dest_block_tex / "block.png.mcmeta")
    elif (src_blocks / "block1.png").exists():
        shutil.copy2(src_blocks / "block1.png", dest_block_tex / "block.png")
        mcm = (src_blocks / "block1.png.mcmeta")
        if mcm.exists():
            shutil.copy2(mcm, dest_block_tex / "block.png.mcmeta")
    elif (WD_BLOCKS / "block1.png").exists():
        shutil.copy2(WD_BLOCKS / "block1.png", dest_block_tex / "block.png")
    else:
        dummy_1x1.save(dest_block_tex / "block.png")
        
    dummy_1x1.save(dest_block_tex / "block_secondary.png")
    b_model = {
        "parent": "block/block",
        "loader": "forge:composite",
        "textures": {"particle": f"gtceu:block/material_sets/{set_name}/block"},
        "children": {
            "base": {
                "parent": "gtceu:block/cube/tinted/all_0",
                "render_type": "solid",
                "textures": {"all": f"gtceu:block/material_sets/{set_name}/block"}
            },
            "secondary": {
                "parent": "gtceu:block/cube/tinted/all",
                "render_type": "translucent",
                "textures": {"all": f"gtceu:block/material_sets/{set_name}/block_secondary"}
            }
        },
        "item_render_order": ["base", "secondary"]
    }
    (dest_block_model / "block.json").write_text(json.dumps(b_model, indent=2) + "\n")
    
    # Frame GT (both frame_gt and frameGt)
    frame_src = src_blocks / "frameGt.png" if (src_blocks / "frameGt.png").exists() else WD_BLOCKS / "frameGt.png"
    if frame_src.exists():
        frame_img = Image.open(frame_src).convert("RGBA")
        mcm_frame = frame_src.with_name(frame_src.name + ".mcmeta")
        mcm_frame_content = mcm_frame.read_text() if mcm_frame.exists() else None
    else:
        frame_img = dummy_1x1
        mcm_frame_content = None
        
    for f_name in ("frame_gt", "frameGt"):
        frame_img.save(dest_block_tex / f"{f_name}.png")
        if mcm_frame_content:
            (dest_block_tex / f"{f_name}.png.mcmeta").write_text(mcm_frame_content)
        dummy_1x1.save(dest_block_tex / f"{f_name}_secondary.png")
        
        f_model = {
            "parent": "block/block",
            "loader": "forge:composite",
            "textures": {"particle": f"gtceu:block/material_sets/{set_name}/{f_name}"},
            "children": {
                "base": {
                    "parent": "gtceu:block/cube/tinted/all_0",
                    "render_type": "cutout",
                    "textures": {"all": f"gtceu:block/material_sets/{set_name}/{f_name}"}
                },
                "secondary": {
                    "parent": "gtceu:block/cube/tinted/all",
                    "render_type": "translucent",
                    "textures": {"all": f"gtceu:block/material_sets/{set_name}/{f_name}_secondary"}
                }
            },
            "item_render_order": ["base", "secondary"]
        }
        (dest_block_model / f"{f_name}.json").write_text(json.dumps(f_model, indent=2) + "\n")

    # Pipes (both pipe_side and pipeSide, etc.)
    for dst_name, src_file in PIPES_MAP.items():
        p_src = src_blocks / src_file if (src_blocks / src_file).exists() else WD_BLOCKS / src_file
        if p_src.exists():
            p_img = Image.open(p_src).convert("RGBA")
            p_mcm = p_src.with_name(p_src.name + ".mcmeta")
            p_mcm_content = p_mcm.read_text() if p_mcm.exists() else None
            camel_pipe = src_file.replace(".png", "")
            for p_alias in (dst_name, camel_pipe):
                p_img.save(dest_block_tex / f"{p_alias}.png")
                if p_mcm_content:
                    (dest_block_tex / f"{p_alias}.png.mcmeta").write_text(p_mcm_content)

    # Wires (both wire_side and wireSide, etc.)
    wire_src = src_blocks / "wire.png" if (src_blocks / "wire.png").exists() else GTCEU_DULL_BLOCKS / "wire_side.png"
    if wire_src.exists():
        wire_img = Image.open(wire_src).convert("RGBA").crop((0, 0, 16, 16))
        mcm_wire = wire_src.with_name(wire_src.name + ".mcmeta")
        mcm_wire_content = mcm_wire.read_text() if mcm_wire.exists() else None
    else:
        wire_img = dummy_1x1
        mcm_wire_content = None
        
    for w_name in ("wire_side", "wireSide", "wire_end", "wireEnd"):
        wire_img.save(dest_block_tex / f"{w_name}.png")
        if mcm_wire_content:
            (dest_block_tex / f"{w_name}.png.mcmeta").write_text(mcm_wire_content)
        dummy_1x1.save(dest_block_tex / f"{w_name}_overlay.png")

    # Fluids
    for fluid_file in ("liquid", "molten"):
        fl_src = GTCEU_DULL_BLOCKS / f"{fluid_file}.png"
        if fl_src.exists():
            Image.open(fl_src).convert("RGBA").crop((0, 0, 16, 16)).save(dest_block_tex / f"{fluid_file}.png")
    
    print(f"Ported {set_name} from {mod_folder} with loader {loader_name}")


if __name__ == "__main__":
    # 1. Cosmic Neutronium
    port_material("gtna_cosmic_neutronium", "cosmicneutronium", "gtna:cosmic")

    # 2. Eternity
    port_material("gtna_eternity", "eternity", "gtna:eternal",
                  custom_block_path=MOD_ROOT / "blocks/iconsets/BLOCK_ETERNITY.png")

    # 3. Magmatter
    port_material("gtna_magmatter", "magmatter", "gtna:halo",
                  custom_block_path=MOD_ROOT / "blocks/iconsets/BLOCK_MAGMATTER.png")

    # 4. Exo-Halkonite
    port_material("gtna_exo_halkonite", "exohalkonite", "gtna:cosmic")

    # 5. Infinity
    port_material("gtna_infinity", "infinity", None)

    # 6. Spacetime
    port_material("gtna_spacetime", "spacetime", "gtna:eternal")

    # 7. MHDCSM
    port_material("gtna_mhdcsm", "MagnetohydrodynamicallyConstrainedStarMatter", "gtna:halo")

    # 8. Graviton Shard
    port_material("gtna_graviton_shard", "GravitonShard", "gtna:cosmic")

    print("All endgame Modernity materials ported successfully!")
