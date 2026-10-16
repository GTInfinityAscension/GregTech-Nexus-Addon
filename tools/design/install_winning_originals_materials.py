"""Installer for the 12 selected winning material set options into GTNA resources.
Generates animated 16x512 texture strips, .mcmeta files, 64x2048 animated halos, and GTCEu composite models.
"""

import json
from pathlib import Path
import numpy as np
from PIL import Image

# Import generators from generate_all_originals_proposals
from generate_all_originals_proposals import (
    ROOT, MODERNITY, ICONSETS, CUSTOM, CUSTOM_BLOCK, FRAMES, HALO_SIZE, EMPTY,
    FORMS, base_of, geometry, finish, ramp, halo_gen, render_material_frame, PROPOSALS
)

WINNING_CHOICES = {
    "nexium": 1,
    "primordial_tholin": 3,
    "magnetar_crystal": 1,
    "degenerate_core_matter": 1,
    "magnetarium": 1,
    "prismatium": 1,
    "chronomercury": 1,
    "forgecore": 1,
    "vivispore": 3,
    "abyssal_antimatter": 1,
    "precursor_residue": 3,
    "void_ash": 2
}

MATERIAL_SPECS = {
    "nexium": {
        "items": ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod", "wire_fine"],
        "blocks": ["block", "frame_gt"],
        "profile": "SHINY"
    },
    "primordial_tholin": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "magnetar_crystal": {
        "items": ["gem", "dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": "GEM_HORIZONTAL"
    },
    "degenerate_core_matter": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "magnetarium": {
        "items": ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod"],
        "blocks": ["block", "frame_gt"],
        "profile": "SHINY"
    },
    "prismatium": {
        "items": ["gem", "dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": "DIAMOND"
    },
    "chronomercury": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "forgecore": {
        "items": ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod"],
        "blocks": ["block", "frame_gt"],
        "profile": "SHINY"
    },
    "vivispore": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "abyssal_antimatter": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "precursor_residue": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    },
    "void_ash": {
        "items": ["dust", "dust_small", "dust_tiny"],
        "blocks": ["block"],
        "profile": None
    }
}

TEX_ITEMS_ROOT = ROOT / "src/main/resources/assets/gtceu/textures/item/material_sets"
TEX_BLOCKS_ROOT = ROOT / "src/main/resources/assets/gtceu/textures/block/material_sets"
MODEL_ITEMS_ROOT = ROOT / "src/main/resources/assets/gtceu/models/item/material_sets"
MODEL_BLOCKS_ROOT = ROOT / "src/main/resources/assets/gtceu/models/block/material_sets"
HALO_TEX_ROOT = ROOT / "src/main/resources/assets/gtna/textures/item/effect"

MCMETA_CONTENT = json.dumps({"animation": {"frametime": 2, "interpolate": True}}, indent=2) + "\n"


def overlay_of(name, ingot_profile=None):
    src = FORMS.get(name, name)
    folder = ICONSETS / ingot_profile if name in ("ingot", "nugget", "gem") and ingot_profile else CUSTOM
    p = folder / f"{src}_OVERLAY.png"
    if p.exists():
        return Image.open(p).convert("RGBA").crop((0, 0, 16, 16))
    if name == "wire_fine":
        p_wf = CUSTOM / "wireFine_OVERLAY.png"
        if p_wf.exists():
            return Image.open(p_wf).convert("RGBA").crop((0, 0, 16, 16))
    return EMPTY


def install_halo(mat_id, opt_idx, halo_name):
    HALO_TEX_ROOT.mkdir(parents=True, exist_ok=True)
    frames = [
        np.clip(halo_gen(mat_id, opt_idx, f), 0, 255).astype(np.uint8)
        for f in range(FRAMES)
    ]
    strip = np.concatenate(frames, axis=0) # 64 width, 2048 height
    halo_img = Image.fromarray(strip, "RGBA")
    
    png_path = HALO_TEX_ROOT / f"{halo_name}.png"
    meta_path = HALO_TEX_ROOT / f"{halo_name}.png.mcmeta"
    halo_img.save(png_path)
    meta_path.write_text(MCMETA_CONTENT)
    print(f"  [Halo] Installed {png_path.name} (64x2048)")


def install_item(mat_id, opt_idx, form_name, profile, halo_name):
    folder = f"gtna_{mat_id}"
    tex_dir = TEX_ITEMS_ROOT / folder
    model_dir = MODEL_ITEMS_ROOT / folder
    tex_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    # 1. Texture Strip
    base = base_of(form_name, profile)
    frames = [render_material_frame(mat_id, opt_idx, base, f) for f in range(FRAMES)]
    strip = np.concatenate(frames, axis=0) # 16 width, 512 height
    Image.fromarray(strip, "RGBA").save(tex_dir / f"{form_name}.png")
    (tex_dir / f"{form_name}.png.mcmeta").write_text(MCMETA_CONTENT)

    # 2. Overlays
    overlay_img = overlay_of(form_name, profile)
    overlay_img.save(tex_dir / f"{form_name}_overlay.png")
    EMPTY.save(tex_dir / f"{form_name}_secondary.png")

    # 3. Model JSON with gtna:halo
    model_json = {
        "parent": "item/generated",
        "textures": {
            "layer0": f"gtceu:item/material_sets/{folder}/{form_name}",
            "layer1": f"gtceu:item/material_sets/{folder}/{form_name}_overlay",
            "halo": f"gtna:item/effect/{halo_name}"
        },
        "loader": "gtna:halo",
        "halo": {
            "texture": "#halo",
            "color": -1,
            "size": 4,
            "pulse": True
        }
    }
    (model_dir / f"{form_name}.json").write_text(json.dumps(model_json, indent=2) + "\n")


def install_block(mat_id, opt_idx, block_name, profile):
    folder = f"gtna_{mat_id}"
    tex_dir = TEX_BLOCKS_ROOT / folder
    model_dir = MODEL_BLOCKS_ROOT / folder
    tex_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    # 1. Texture Strip
    src_file = "frameGt.png" if block_name == "frame_gt" else "block1.png"
    src_path = CUSTOM_BLOCK / src_file
    base = np.array(Image.open(src_path).convert("RGBA"), dtype=np.float32)[:16]
    
    frames = [render_material_frame(mat_id, opt_idx, base, f) for f in range(FRAMES)]
    strip = np.concatenate(frames, axis=0) # 16 width, 512 height
    Image.fromarray(strip, "RGBA").save(tex_dir / f"{block_name}.png")
    (tex_dir / f"{block_name}.png.mcmeta").write_text(MCMETA_CONTENT)
    EMPTY.save(tex_dir / f"{block_name}_secondary.png")

    # 2. Model JSON
    render_type = "cutout" if block_name == "frame_gt" else "solid"
    model_json = {
        "parent": "block/block",
        "loader": "forge:composite",
        "textures": {
            "particle": f"gtceu:block/material_sets/{folder}/{block_name}"
        },
        "children": {
            "base": {
                "parent": "gtceu:block/cube/tinted/all_0",
                "render_type": render_type,
                "textures": {
                    "all": f"gtceu:block/material_sets/{folder}/{block_name}"
                }
            },
            "secondary": {
                "parent": "gtceu:block/cube/tinted/all",
                "render_type": "translucent",
                "textures": {
                    "all": f"gtceu:block/material_sets/{folder}/{block_name}_secondary"
                }
            }
        },
        "item_render_order": ["base", "secondary"]
    }
    (model_dir / f"{block_name}.json").write_text(json.dumps(model_json, indent=2) + "\n")
    if block_name == "block":
        (model_dir / "block1.json").write_text(json.dumps(model_json, indent=2) + "\n")


def main():
    print("================================================================================")
    print("Installing 12 Winning Material Set Options into GTNA...")
    print("================================================================================")

    for mat_id, opt_idx in WINNING_CHOICES.items():
        spec = MATERIAL_SPECS[mat_id]
        meta = PROPOSALS[mat_id]["options"][opt_idx - 1]
        halo_name = meta["halo_name"]
        profile = spec["profile"]

        print(f"\n>>> [{mat_id}] Installing Option {opt_idx}: {meta['name']} (Halo: {halo_name})")
        
        # 1. Install Halo
        install_halo(mat_id, opt_idx, halo_name)

        # 2. Install Items
        for form in spec["items"]:
            install_item(mat_id, opt_idx, form, profile, halo_name)
        print(f"  [Items] Installed {len(spec['items'])} forms: {', '.join(spec['items'])}")

        # 3. Install Blocks
        for block in spec["blocks"]:
            install_block(mat_id, opt_idx, block, profile)
        print(f"  [Blocks] Installed {len(spec['blocks'])} forms: {', '.join(spec['blocks'])}")

    print("\n================================================================================")
    print("Installation complete! All 12 material sets installed successfully.")
    print("================================================================================")


if __name__ == "__main__":
    main()
