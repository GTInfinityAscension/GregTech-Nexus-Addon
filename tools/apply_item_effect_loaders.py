"""Applies GTNA item-effect model loaders (gtna:halo, gtna:glow_edge, gtna:cosmic, ...) to GTNA material sets."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "src/main/resources/assets/gtceu/models/item/material_sets"

GLOW = {  # glow_edge: color, width
    "axonium": 0xffd700, "draconium": 0xb02fff, "tengam_purified": 0xbef070, "tengam_attuned": 0xd5ff80,
    "fallking": 0xffcd6b, "odyssey": 0x2dc4bf, "shijima": 0xc4d6f2, "churitsu": 0xe5e5e5,
}
HALO = {  # halo: texture, RGB
    "magmatter": ("halo", 0x212121), "awakened_draconium": ("halo", 0xff7700), "ichorium": ("halo", 0xd37806),
    "advanced_nitinol": ("halo_noise", 0xd2b48c), "nitinol_60": ("halo_noise", 0xc8c8c8),
    "superconductor_uiv_base": ("halo_noise", 0xe558b1), "superconductor_umv_base": ("halo_noise", 0xb526cd),
    "atomic_separation_catalyst": ("halo_noise", 0xe85e0c),
    "platinum_manganese_antimony_heusler_alloy": ("halo_noise", 0xb0b8c0),
    "stellar_alloy": ("halo_noise", 0xc5ced8), "trinaquadalloy": ("halo_noise", 0x2a4d4d),
    "mar_m_200_steel": ("halo_noise", 0x515151), "hastelloy_n_75": ("halo_noise", 0x6b8e6b),
    "stellite": ("halo_noise", 0x9991a5), "indalloy_140": ("halo_noise", 0x59536e),
    "end_steel": ("halo_noise", 0xd6d980), "dark_steel": ("halo_noise", 0x404040),
}
MASKED = {"universium": "cosmic", "cosmic_neutronium": "cosmic", "exo_halkonite": "cosmic",
          "eternity": "eternal", "chaos_matter": "unstable"}


def signed(argb):
    return argb - (1 << 32) if argb >= 1 << 31 else argb


for d in sorted(ROOT.glob("gtna_*")):
    name = d.name[5:]
    for p in sorted(d.glob("*.json")):
        m = json.loads(p.read_text())
        for k in ("loader", "halo", "glow", "glow_edge", "cosmic", "eternal", "unstable"):
            m.pop(k, None)
        m.get("textures", {}).pop("halo", None)
        if name in GLOW:
            m["loader"] = "gtna:glow_edge"
            m["glow_edge"] = {"color": GLOW[name], "width": 1.5}
        elif name in HALO:
            tex, rgb = HALO[name]
            m["textures"]["halo"] = f"gtna:item/effect/{tex}"
            m["loader"] = "gtna:halo"
            m["halo"] = {"texture": "#halo", "color": signed(0xFF000000 | rgb), "size": 4, "pulse": True}
        elif name in MASKED:
            kind = MASKED[name]
            mask = "gtna:mask/cosmic_wire_fine" if p.stem == "wire_fine" else "gtna:mask/cosmic"
            m["loader"] = f"gtna:{kind}"
            m[kind] = {"mask": mask}
        p.write_text(json.dumps(m, indent=2) + "\n")
