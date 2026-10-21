"""Icon sets of the materials only the four originals produce (G-0272).

Usage: python3 tools/design/generate_originals_icon_sets.py [GTCEu 7.5.3 checkout] [--preview out.png]

Each material keeps the shape of a GTCEu icon set (the parent below) and gets its own palette and motif: the
parent's greyscale base is gradient-mapped through four colour stops, then a motif (sweep, pulse, sparkle, hue
cycle, specks, motes) is drawn inside the shape. Animated motifs become vertical frame strips with an .mcmeta.
The materials are registered white, so GTCEu's tint leaves the colours as drawn. Output goes to
gtceu:{textures,models}/{item,block}/material_sets/gtna_<set>/ like the other GTNA icon sets.
"""

import colorsys
import json
import math
import random
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
GTCEU = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else \
    Path.home() / "MineProjects/references/GTCEu-7.5.3"
SRC = GTCEU / "src/main/resources/assets/gtceu/textures"
OUT_TEX = ROOT / "src/main/resources/assets/gtceu/textures"
OUT_MODEL = ROOT / "src/main/resources/assets/gtceu/models"

PARENTS = {
    "dull": None, "metallic": "dull", "magnetic": "metallic", "shiny": "metallic", "diamond": "shiny",
    "emerald": "diamond", "gem_horizontal": "emerald", "fine": "dull", "rough": "fine",
}

# set name: parent shape set, colour stops dark -> light, motif, frames, prefixes
SETS = {
    "nexium": ("shiny", ["#06262b", "#167a76", "#3fd6c8", "#d8fff8"], "sweep", 8,
               ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod", "wire_fine"]),
    "primordial_tholin": ("rough", ["#1f0905", "#5e1d10", "#a8432a", "#eb9a62"], "specks", 1,
                          ["dust", "dust_small", "dust_tiny"]),
    "magnetar_crystal": ("gem_horizontal", ["#12073a", "#4024c4", "#8a72ff", "#f0eaff"], "pulse", 8,
                         ["gem", "dust", "dust_small", "dust_tiny"]),
    "degenerate_core_matter": ("fine", ["#5a6894", "#aab8e8", "#eef2ff", "#ffffff"], "sparkle", 6,
                               ["dust", "dust_small", "dust_tiny"]),
    "magnetarium": ("magnetic", ["#1d1048", "#5a3fc0", "#a58cff", "#f3edff"], "sweep", 8,
                    ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod"]),
    "prismatium": ("diamond", ["#4a5a78", "#9ec8e8", "#e6f7ff", "#ffffff"], "hue", 12,
                   ["gem", "dust", "dust_small", "dust_tiny"]),
    "chronomercury": ("shiny", ["#2b303b", "#7d8698", "#c9d1de", "#ffffff"], "sweep_back", 8,
                      ["dust", "dust_small", "dust_tiny"]),
    "forgecore": ("metallic", ["#2e0900", "#9c2e00", "#ff6a1f", "#ffe08a"], "pulse", 8,
                  ["ingot", "nugget", "dust", "dust_small", "dust_tiny", "plate", "rod"]),
    "vivispore": ("fine", ["#142a08", "#3f7a1a", "#7fbf3a", "#e2fba6"], "specks", 1,
                  ["dust", "dust_small", "dust_tiny"]),
    "abyssal_antimatter": ("shiny", ["#030108", "#1a0f2e", "#4b2a7a", "#d088ff"], "sparkle", 8,
                           ["dust", "dust_small", "dust_tiny"]),
    "precursor_residue": ("rough", ["#3a2a0c", "#806128", "#c9a85a", "#f8e9b4"], "glyphs", 1,
                          ["dust", "dust_small", "dust_tiny"]),
    "void_ash": ("rough", ["#030305", "#101016", "#262632", "#7a7a98"], "motes", 8,
                 ["dust", "dust_small", "dust_tiny"]),
}
BLOCK_PREFIX = "block"


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def lookup(kind, set_name, name):
    s = set_name
    while s is not None:
        p = SRC / kind / "material_sets" / s / f"{name}.png"
        if p.exists():
            return p
        s = PARENTS.get(s, "dull" if s != "dull" else None)
    return None


def ramp(stops, v):
    v = max(0.0, min(1.0, v)) * (len(stops) - 1)
    i = min(int(v), len(stops) - 2)
    t = v - i
    a, b = stops[i], stops[i + 1]
    return tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))


def frame(base, stops, motif, f, frames, seed):
    w, h = base.size
    out = Image.new("RGBA", (w, h))
    rnd = random.Random(seed)
    specks = {(rnd.randrange(w), rnd.randrange(h)) for _ in range(w * h // 9)}
    glyph_rows = {y for y in range(2, h, 4)}
    for y in range(h):
        for x in range(w):
            r, g, b, a = base.getpixel((x, y))
            if a == 0:
                continue
            v = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            phase = f / frames
            if motif in ("sweep", "sweep_back"):
                d = (x + y) / (w + h)
                band = (d - phase) if motif == "sweep" else (d - (1 - phase))
                band = band - math.floor(band)
                v += 0.35 * max(0.0, 1 - abs(band - 0.5) * 8)
            elif motif == "pulse":
                v *= 0.85 + 0.25 * (0.5 + 0.5 * math.sin(2 * math.pi * phase))
            elif motif == "sparkle":
                fr = random.Random(seed * 31 + f * 7 + x * 131 + y)
                if fr.random() < 0.06:
                    v = 1.0
            elif motif == "specks":
                if (x, y) in specks:
                    v = v * 0.55 if (x + y) % 2 else min(1.0, v + 0.3)
            elif motif == "glyphs":
                if y in glyph_rows and (x * 7 + y) % 5 < 2:
                    v = min(1.0, v + 0.35)
            elif motif == "motes":
                fr = random.Random(seed * 17 + x * 97 + ((y + f) % h) * 13)
                if fr.random() < 0.05:
                    v = min(1.0, v + 0.6)
            c = ramp(stops, v)
            if motif == "hue":
                hh, ll, ss = colorsys.rgb_to_hls(*(k / 255 for k in c))
                hh = (phase + (x + y) / (2.0 * (w + h))) % 1.0
                ss, ll = 0.75, min(ll, 0.72)
                c = tuple(int(k * 255) for k in colorsys.hls_to_rgb(hh, ll, ss))
            out.putpixel((x, y), (*c, a))
    return out


def build(set_name, spec):
    parent, stops_hex, motif, frames, prefixes = spec
    stops = [hexrgb(s) for s in stops_hex]
    folder = f"gtna_{set_name}"
    seed = sum(map(ord, set_name))
    made = []
    for kind, names in (("item", prefixes), ("block", [BLOCK_PREFIX])):
        for name in names:
            src = lookup(kind, parent, name)
            if src is None:
                continue
            base = Image.open(src).convert("RGBA")
            w = base.width
            base = base.crop((0, 0, w, w))  # first frame of any animated base
            strip = Image.new("RGBA", (w, w * frames))
            for f in range(frames):
                strip.paste(frame(base, stops, motif, f, frames, seed), (0, w * f))
            tex_dir = OUT_TEX / kind / "material_sets" / folder
            tex_dir.mkdir(parents=True, exist_ok=True)
            strip.save(tex_dir / f"{name}.png")
            meta = tex_dir / f"{name}.png.mcmeta"
            if frames > 1:
                meta.write_text(json.dumps({"animation": {"frametime": 3}}, indent=2) + "\n")
            elif meta.exists():
                meta.unlink()
            made.append((kind, name, strip))
            model_dir = OUT_MODEL / kind / "material_sets" / folder
            model_dir.mkdir(parents=True, exist_ok=True)
            if kind == "item":
                textures = {"layer0": f"gtceu:item/material_sets/{folder}/{name}"}
                overlay = lookup("item", parent, f"{name}_overlay")
                if overlay is not None:
                    textures["layer1"] = "gtceu:item/material_sets/%s/%s_overlay" % (overlay.parent.name, name)
                model = {"parent": "item/generated", "textures": textures}
            else:
                model = {"parent": "block/block", "loader": "forge:composite",
                         "textures": {"particle": f"gtceu:block/material_sets/{folder}/block"},
                         "children": {"base": {"parent": "gtceu:block/cube/tinted/all_0", "render_type": "solid",
                                               "textures": {"all": f"gtceu:block/material_sets/{folder}/block"}}},
                         "item_render_order": ["base"]}
            (model_dir / f"{name}.json").write_text(json.dumps(model, indent=2) + "\n")
    return made


def main():
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    rows = []
    for set_name, spec in SETS.items():
        rows.append((set_name, build(set_name, spec)))
        print(f"{set_name}: {len(rows[-1][1])} textures")
    if preview:
        scale, cols = 4, 9
        sheet = Image.new("RGBA", (cols * 16 * scale + 8, len(rows) * (16 * scale + 4) + 4), (40, 40, 48, 255))
        for r, (_, made) in enumerate(rows):
            for c, (_, _, strip) in enumerate(made[:cols]):
                tile = strip.crop((0, 0, strip.width, strip.width)).resize((16 * scale, 16 * scale), Image.NEAREST)
                sheet.alpha_composite(tile, (4 + c * 16 * scale, 4 + r * (16 * scale + 4)))
        sheet.save(preview)


if __name__ == "__main__":
    main()
