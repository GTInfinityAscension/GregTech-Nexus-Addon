package com.raishxn.gtna.integration;

import com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper;
import com.gregtechceu.gtceu.api.data.chemical.material.Material;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;

import net.minecraft.network.chat.Component;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.common.data.GTNAOriginals;
import com.raishxn.gtna.common.data.material.OriginalsMaterials;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Info pages (JEI/EMI) for what only the original multiblocks produce: there is no recipe to show, so the page
 * says which machine makes it and how (G-0272). Text in {@code gtna.originals.jei.<key>}.
 */
public final class OriginalsInfo {

    private static final TagPrefix[] FORMS = { TagPrefix.dust, TagPrefix.dustSmall, TagPrefix.dustTiny, TagPrefix.gem,
            TagPrefix.ingot, TagPrefix.nugget, TagPrefix.plate, TagPrefix.rod, TagPrefix.wireFine, TagPrefix.block };

    private OriginalsInfo() {}

    /** Info key -> every stack it describes. */
    public static Map<String, List<ItemStack>> entries() {
        var out = new LinkedHashMap<String, List<ItemStack>>();
        material(out, "nexium", OriginalsMaterials.Nexium);
        material(out, "primordial_tholin", OriginalsMaterials.PrimordialTholin);
        material(out, "magnetar_crystal", OriginalsMaterials.MagnetarCrystal);
        material(out, "degenerate_core_matter", OriginalsMaterials.DegenerateCoreMatter);
        material(out, "prismatium", OriginalsMaterials.Prismatium);
        material(out, "chronomercury", OriginalsMaterials.Chronomercury);
        material(out, "forgecore", OriginalsMaterials.Forgecore);
        material(out, "vivispore", OriginalsMaterials.Vivispore);
        material(out, "abyssal_antimatter", OriginalsMaterials.AbyssalAntimatter);
        material(out, "precursor_residue", OriginalsMaterials.PrecursorResidue);
        material(out, "void_ash", OriginalsMaterials.VoidAsh);
        out.put("antiproton_cell", List.of(GTNAOriginals.ANTIPROTON_CELL.asStack()));
        var particles = new ArrayList<ItemStack>();
        for (var p : ColliderCore.Particle.values()) particles.add(new ItemStack(GTNAOriginals.particle(p)));
        out.put("particles", particles);
        out.put("rift_singularity", List.of(GTNAOriginals.RIFT_SINGULARITY.asStack()));
        return out;
    }

    public static Component text(String key) {
        return Component.translatable("gtna.originals.jei." + key);
    }

    private static void material(Map<String, List<ItemStack>> out, String key, Material material) {
        var stacks = new ArrayList<ItemStack>();
        for (var form : FORMS) {
            var stack = ChemicalHelper.get(form, material);
            if (!stack.isEmpty()) stacks.add(stack);
        }
        out.put(key, stacks);
    }
}
