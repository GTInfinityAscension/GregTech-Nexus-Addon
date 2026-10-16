package com.raishxn.gtna.common.data.material;

import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialIconSet;

import com.raishxn.gtna.GTNACORE;

import static com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlags.*;

/**
 * Materials only the four original multiblocks produce (G-0270): each one feeds the endgame and the next original.
 * No fluids, so none of them counts as Stellar Containment Chamber feed; working recipes are explicit.
 */
public final class OriginalsMaterials {

    private OriginalsMaterials() {}

    // Kinetic Orbital Lance
    public static Material Nexium;
    public static Material PrimordialTholin;
    // Stellar Containment Chamber
    public static Material MagnetarCrystal;
    public static Material DegenerateCoreMatter;
    public static Material Magnetarium;
    // Dimensional Rift Gate, one per biome
    public static Material Prismatium;
    public static Material Chronomercury;
    public static Material Forgecore;
    public static Material Vivispore;
    public static Material AbyssalAntimatter;
    public static Material PrecursorResidue;
    public static Material VoidAsh;

    public static void init() {
        Nexium = metal("nexium", "Nexium", 0xffffff, icons("nexium", MaterialIconSet.SHINY), GENERATE_FINE_WIRE)
                .setFormula("Nx");
        PrimordialTholin = dust("primordial_tholin", "Primordial Tholin", 0xffffff,
                icons("primordial_tholin", MaterialIconSet.ROUGH))
                .setFormula("(HCN)ₙ(C₂H₂)ₘ");
        MagnetarCrystal = gem("magnetar_crystal", "Magnetar Crystal", 0xffffff,
                icons("magnetar_crystal", MaterialIconSet.GEM_HORIZONTAL));
        DegenerateCoreMatter = dust("degenerate_core_matter", "Degenerate Core Matter", 0xffffff,
                icons("degenerate_core_matter", MaterialIconSet.FINE)).setFormula("nₙ");
        Magnetarium = metal("magnetarium", "Magnetarium", 0xffffff, icons("magnetarium", MaterialIconSet.MAGNETIC));
        Prismatium = gem("prismatium", "Prismatium", 0xffffff, icons("prismatium", MaterialIconSet.DIAMOND));
        Chronomercury = dust("chronomercury", "Chronomercury", 0xffffff, icons("chronomercury", MaterialIconSet.SHINY))
                .setFormula("Hg⧖");
        Forgecore = metal("forgecore", "Forgecore", 0xffffff, icons("forgecore", MaterialIconSet.METALLIC));
        Vivispore = dust("vivispore", "Vivispore", 0xffffff, icons("vivispore", MaterialIconSet.FINE));
        AbyssalAntimatter = dust("abyssal_antimatter", "Abyssal Antimatter", 0xffffff,
                icons("abyssal_antimatter", MaterialIconSet.SHINY))
                .setFormula("p̄ē");
        PrecursorResidue = dust("precursor_residue", "Precursor Residue", 0xffffff,
                icons("precursor_residue", MaterialIconSet.ROUGH))
                .setFormula("?");
        VoidAsh = dust("void_ash", "Void Ash", 0xffffff, icons("void_ash", MaterialIconSet.ROUGH)).setFormula("∅");
    }

    /** Own icon set (tools/design/generate_originals_icon_sets.py); the parent supplies any missing form. */
    private static MaterialIconSet icons(String name, MaterialIconSet parent) {
        return new MaterialIconSet("gtna_" + name, parent);
    }

    private static Material metal(String id, String name, int color, MaterialIconSet icons,
                                  com.gregtechceu.gtceu.api.data.chemical.material.info.MaterialFlag... extra) {
        var builder = new Material.Builder(GTNACORE.id(id)).langValue(name).ingot().color(color).iconSet(icons)
                .flags(GENERATE_PLATE, GENERATE_ROD, DISABLE_DECOMPOSITION, DISABLE_MATERIAL_RECIPES);
        if (extra.length > 0) builder.flags(extra);
        return builder.buildAndRegister();
    }

    private static Material gem(String id, String name, int color, MaterialIconSet icons) {
        return new Material.Builder(GTNACORE.id(id)).langValue(name).gem().color(color).iconSet(icons)
                .flags(DISABLE_DECOMPOSITION, DISABLE_MATERIAL_RECIPES).buildAndRegister();
    }

    private static Material dust(String id, String name, int color, MaterialIconSet icons) {
        return new Material.Builder(GTNACORE.id(id)).langValue(name).dust().color(color).iconSet(icons)
                .flags(DISABLE_DECOMPOSITION, DISABLE_MATERIAL_RECIPES).buildAndRegister();
    }
}
