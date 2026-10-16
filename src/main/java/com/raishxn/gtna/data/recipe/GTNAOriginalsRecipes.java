package com.raishxn.gtna.data.recipe;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.tag.TagPrefix;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTItems;
import com.gregtechceu.gtceu.common.data.GTMachines;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.data.recipe.CustomTags;

import net.minecraft.data.recipes.FinishedRecipe;
import net.minecraft.world.item.ItemStack;

import com.raishxn.gtna.api.machine.feature.lance.LanceCore;
import com.raishxn.gtna.common.data.GTNABlocks;
import com.raishxn.gtna.common.data.GTNAMaterials;
import com.raishxn.gtna.common.data.GTNAOriginals;

import java.util.function.Consumer;

import static com.raishxn.gtna.common.data.material.OriginalsMaterials.*;

/**
 * Working recipes of the materials only the four originals produce (G-0270). Their endgame uses sit in the Eye of
 * Harmony, Forge of Gods and antimatter fuel rod recipes.
 */
public final class GTNAOriginalsRecipes {

    private GTNAOriginalsRecipes() {}

    public static void register(Consumer<FinishedRecipe> provider) {
        construction(provider);
        // Nexium (Kinetic Orbital Lance, Nexus-1): wire for the Collider's tier-4 dipoles.
        GTRecipeTypes.BLAST_RECIPES.recipeBuilder("originals/nexium_ingot")
                .inputItems(TagPrefix.dust, Nexium)
                .outputItems(TagPrefix.ingot, Nexium)
                .blastFurnaceTemp(10800).duration(400).EUt(GTValues.VA[GTValues.UEV])
                .save(provider);
        GTRecipeTypes.WIREMILL_RECIPES.recipeBuilder("originals/nexium_fine_wire")
                .inputItems(TagPrefix.ingot, Nexium)
                .outputItems(TagPrefix.wireFine, Nexium, 8)
                .circuitMeta(3).duration(200).EUt(GTValues.VA[GTValues.UHV])
                .save(provider);

        // Forgecore (Dimensional Rift Gate, Forge World): magnetar armour plates for the Stellar Chamber.
        GTRecipeTypes.BLAST_RECIPES.recipeBuilder("originals/forgecore_ingot")
                .inputItems(TagPrefix.dust, Forgecore)
                .outputItems(TagPrefix.ingot, Forgecore)
                .blastFurnaceTemp(9000).duration(300).EUt(GTValues.VA[GTValues.UHV])
                .save(provider);
        GTRecipeTypes.BENDER_RECIPES.recipeBuilder("originals/forgecore_plate")
                .inputItems(TagPrefix.ingot, Forgecore)
                .outputItems(TagPrefix.plate, Forgecore)
                .circuitMeta(1).duration(100).EUt(GTValues.VA[GTValues.UV])
                .save(provider);

        // Magnetarium: the Magnetar Slug, the only projectile that breaks Nexus-1.
        GTRecipeTypes.MIXER_RECIPES.recipeBuilder("originals/magnetarium_dust")
                .inputItems(TagPrefix.dust, Nexium, 2)
                .inputItems(TagPrefix.gem, MagnetarCrystal)
                .inputItems(TagPrefix.dust, GTNAMaterials.WhiteDwarfMatter, 4)
                .outputItems(TagPrefix.dust, Magnetarium, 7)
                .duration(600).EUt(GTValues.VA[GTValues.UIV])
                .save(provider);
        GTRecipeTypes.BLAST_RECIPES.recipeBuilder("originals/magnetarium_ingot")
                .inputItems(TagPrefix.dust, Magnetarium)
                .outputItems(TagPrefix.ingot, Magnetarium)
                .blastFurnaceTemp(12000).duration(600).EUt(GTValues.VA[GTValues.UIV])
                .save(provider);
    }

    /**
     * Generic construction recipes, so the originals can be built with GTNA alone (no modpack). Only GTCEu items and
     * GTNA's own default UHV+ components: nothing from the Eye of Harmony or Forge of Gods, which now need what the
     * originals produce. A modpack can replace any of them by id.
     */
    private static void construction(Consumer<FinishedRecipe> provider) {
        long uv = GTValues.VA[GTValues.UV], uhv = GTValues.VA[GTValues.UHV], uev = GTValues.VA[GTValues.UEV];
        long uiv = GTValues.VA[GTValues.UIV], uxv = GTValues.VA[GTValues.UXV];

        // Structure blocks with no other GTNA recipe.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/radiant_naquadah_alloy_casing")
                .inputItems(TagPrefix.frameGt, GTMaterials.NaquadahAlloy)
                .inputItems(TagPrefix.plate, GTMaterials.Naquadria, 6)
                .circuitMeta(21).outputItems(GTNABlocks.RADIANT_NAQUADAH_ALLOY_CASING.asStack(4))
                .duration(100).EUt(uv).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/precision_field_sync_casing")
                .inputItems(TagPrefix.frameGt, GTMaterials.Neutronium)
                .inputItems(TagPrefix.plate, GTMaterials.Trinium, 4)
                .inputItems(GTItems.FIELD_GENERATOR_UV)
                .circuitMeta(6).outputItems(GTNABlocks.PRECISION_FIELD_SYNC_CASING.asStack(4))
                .duration(200).EUt(uhv).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/nanite_shielding_glass")
                .inputItems(GTBlocks.FUSION_GLASS.asItem(), 2)
                .inputItems(TagPrefix.plate, GTMaterials.Neutronium, 2)
                .circuitMeta(6).outputItems(GTNABlocks.NANITE_SHIELDING_GLASS.asStack(2))
                .duration(100).EUt(uhv).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/degenerate_matter_core")
                .inputItems(TagPrefix.block, GTMaterials.Neutronium)
                .inputItems(GTItems.FIELD_GENERATOR_UV)
                .circuitMeta(6).outputItems(GTNAOriginals.DEGENERATE_MATTER_CORE.asStack(4))
                .duration(200).EUt(uhv).save(provider);

        // GTNA has no Cosmic Neutronium source of its own and its glass is cast at MAX: a UIV route for the Collider.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/cosmic_neutronium_borosilicate_glass")
                .inputItems(GTNABlocks.BOROSILICATE_GLASS_BLOCK.asStack(4))
                .inputItems(TagPrefix.plateDense, GTMaterials.Neutronium, 2)
                .inputItems(GTItems.FIELD_GENERATOR_UEV)
                .inputFluids(GTMaterials.Naquadria.getFluid(144 * 4))
                .circuitMeta(6).outputItems(GTNABlocks.COSMIC_NEUTRONIUM_BOROSILICATE_GLASS.asStack(4))
                .duration(400).EUt(uiv).save(provider);

        // Consumables.
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/rift_probe")
                .inputItems(GTItems.SENSOR_UHV).inputItems(TagPrefix.plate, GTMaterials.Naquadria, 4)
                .inputItems(CustomTags.UHV_CIRCUITS)
                .outputItems(GTNAOriginals.RIFT_PROBE.asStack(4)).duration(200).EUt(uhv).save(provider);
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/depth_anchor")
                .inputItems(GTItems.FIELD_GENERATOR_UHV).inputItems(TagPrefix.plateDense, GTMaterials.Neutronium, 2)
                .inputItems(GTItems.GRAVI_STAR)
                .outputItems(GTNAOriginals.DEPTH_ANCHOR.asStack()).duration(400).EUt(uev).save(provider);
        for (var body : LanceCore.Body.values()) {
            GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/target_cartridge_" + body.name().toLowerCase())
                    .inputItems(GTItems.SENSOR_UV).inputItems(TagPrefix.plate, GTMaterials.Duranium, 2)
                    .circuitMeta(body.ordinal() + 1)
                    .outputItems(new ItemStack(GTNAOriginals.cartridge(body))).duration(100).EUt(uv)
                    .save(provider);
        }

        // Special hatches.
        hatch(provider, "beam_dump", GTNAOriginals.BEAM_DUMP.asStack(), GTValues.UIV,
                TagPrefix.plateDense, GTMaterials.Neutronium, new ItemStack(GTItems.FIELD_GENERATOR_UEV.get()));
        hatch(provider, "seismic_probe", GTNAOriginals.SEISMIC_PROBE.asStack(), GTValues.UXV,
                TagPrefix.plateDense, GTMaterials.Neutronium, new ItemStack(GTItems.SENSOR_UIV.get(), 2));
        hatch(provider, "liner_hatch", GTNAOriginals.LINER_HATCH.asStack(), GTValues.UEV,
                TagPrefix.plateDense, GTMaterials.NaquadahAlloy, new ItemStack(GTItems.ROBOT_ARM_UEV.get(), 2));
        hatch(provider, "mass_injector", GTNAOriginals.MASS_INJECTOR.asStack(), GTValues.UXV,
                TagPrefix.plateDense, GTMaterials.Neutronium, new ItemStack(GTItems.CONVEYOR_MODULE_UIV.get(), 2));
        hatch(provider, "detector_hatch", GTNAOriginals.DETECTOR_HATCH.asStack(), GTValues.UIV,
                TagPrefix.plateDense, GTMaterials.Neutronium, new ItemStack(GTItems.SENSOR_UIV.get(), 2));
        hatch(provider, "target_cartridge_hatch", GTNAOriginals.CARTRIDGE_HATCH.asStack(), GTValues.UEV,
                TagPrefix.plateDense, GTMaterials.NaquadahAlloy, new ItemStack(GTItems.SENSOR_UEV.get(), 2));
        hatch(provider, "tuning_hatch", GTNAOriginals.TUNING_HATCH.asStack(), GTValues.UIV,
                TagPrefix.plateDense, GTMaterials.Neutronium, new ItemStack(GTItems.FIELD_GENERATOR_UIV.get()));

        // Controllers (assembly line, research station).
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder("originals/kinetic_orbital_lance")
                .inputItems(GTMachines.HULL[GTValues.UEV].asStack(4))
                .inputItems(TagPrefix.plateDense, GTMaterials.Neutronium, 32)
                .inputItems(TagPrefix.frameGt, GTMaterials.NaquadahAlloy, 16)
                .inputItems(GTItems.ELECTRIC_PISTON_UEV, 16).inputItems(GTItems.FIELD_GENERATOR_UEV, 8)
                .inputItems(GTItems.SENSOR_UEV, 8).inputItems(GTItems.ENERGY_LAPOTRONIC_ORB_CLUSTER, 16)
                .inputItems(CustomTags.UEV_CIRCUITS, 16)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(144 * 64))
                .inputFluids(GTMaterials.Naquadria.getFluid(144 * 32))
                .outputItems(GTNAOriginals.KINETIC_ORBITAL_LANCE.asStack()).duration(2400).EUt(uev)
                .stationResearch(b -> b.researchStack(new ItemStack(GTItems.ELECTRIC_PISTON_UEV.get()))
                        .CWUt(128).EUt(uev))
                .save(provider);
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder("originals/antimatter_collider_ring")
                .inputItems(GTMachines.HULL[GTValues.UIV].asStack(4))
                .inputItems(GTNABlocks.PRECISION_FIELD_SYNC_CASING.asStack(16))
                .inputItems(TagPrefix.wireGtQuadruple, GTMaterials.RutheniumTriniumAmericiumNeutronate, 32)
                .inputItems(GTItems.FIELD_GENERATOR_UIV, 8).inputItems(GTItems.EMITTER_UIV, 8)
                .inputItems(GTItems.SENSOR_UIV, 8).inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(144 * 128))
                .inputFluids(GTMaterials.Helium.getFluid(com.gregtechceu.gtceu.api.fluids.store.FluidStorageKeys.LIQUID,
                        64_000))
                .outputItems(GTNAOriginals.ANTIMATTER_COLLIDER_RING.asStack()).duration(3600).EUt(uiv)
                .stationResearch(b -> b.researchStack(new ItemStack(GTItems.EMITTER_UIV.get())).CWUt(192).EUt(uiv))
                .save(provider);
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder("originals/dimensional_rift_gate")
                .inputItems(GTMachines.HULL[GTValues.UIV].asStack(4))
                .inputItems(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UIV, 16).inputItems(GTItems.SENSOR_UIV, 8)
                .inputItems(GTItems.GRAVI_STAR, 16).inputItems(CustomTags.UIV_CIRCUITS, 16)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(144 * 128))
                .inputFluids(GTNAMaterials.SpaceTime.getFluid(144 * 16))
                .outputItems(GTNAOriginals.DIMENSIONAL_RIFT_GATE.asStack()).duration(3600).EUt(uiv)
                .stationResearch(b -> b.researchStack(new ItemStack(GTItems.FIELD_GENERATOR_UIV.get()))
                        .CWUt(192).EUt(uiv))
                .save(provider);
        GTRecipeTypes.ASSEMBLY_LINE_RECIPES.recipeBuilder("originals/stellar_containment_chamber")
                .inputItems(GTMachines.HULL[GTValues.UXV].asStack(4))
                .inputItems(GTNABlocks.RADIANT_NAQUADAH_ALLOY_CASING.asStack(32))
                .inputItems(GTNAOriginals.DEGENERATE_MATTER_CORE.asStack(16))
                .inputItems(GTItems.FIELD_GENERATOR_UXV, 8).inputItems(GTItems.SENSOR_UXV, 4)
                .inputItems(GTItems.GRAVI_STAR, 32).inputItems(CustomTags.UXV_CIRCUITS, 16)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(144 * 256))
                .inputFluids(GTMaterials.Neutronium.getFluid(144 * 256))
                .outputItems(GTNAOriginals.STELLAR_CONTAINMENT_CHAMBER.asStack()).duration(6000).EUt(uxv)
                .stationResearch(b -> b.researchStack(new ItemStack(GTItems.FIELD_GENERATOR_UXV.get()))
                        .CWUt(256).EUt(uxv))
                .save(provider);
    }

    private static void hatch(Consumer<FinishedRecipe> provider, String id, ItemStack out, int tier, TagPrefix prefix,
                              com.gregtechceu.gtceu.api.data.chemical.material.Material plate, ItemStack part) {
        GTRecipeTypes.ASSEMBLER_RECIPES.recipeBuilder("originals/" + id)
                .inputItems(GTMachines.HULL[tier].asStack()).inputItems(prefix, plate, 2).inputItems(part)
                .inputItems(GTItems.ROBOT_ARM_UV, 2)
                .inputFluids(GTMaterials.SolderingAlloy.getFluid(144 * 4))
                .outputItems(out).duration(400).EUt(GTValues.VA[tier - 1]).save(provider);
    }
}
