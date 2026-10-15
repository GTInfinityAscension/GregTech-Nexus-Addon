package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.item.ComponentItem;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.PartAbility;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraftforge.registries.ForgeRegistries;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.machine.feature.collider.ColliderCore;
import com.raishxn.gtna.api.machine.multiblock.GTNAPartAbility;
import com.raishxn.gtna.common.data.multiblock.GTNAMultiBlockFileReader;
import com.raishxn.gtna.common.machine.multiblock.originals.ColliderRingMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.LanceMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.OriginalHatchPartMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.RiftGateMachine;
import com.raishxn.gtna.common.machine.multiblock.originals.StellarChamberMachine;
import com.tterrag.registrate.util.entry.BlockEntry;
import com.tterrag.registrate.util.entry.ItemEntry;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.EnumMap;
import java.util.Map;
import java.util.function.Function;

import static com.gregtechceu.gtceu.api.pattern.Predicates.abilities;
import static com.gregtechceu.gtceu.api.pattern.Predicates.air;
import static com.gregtechceu.gtceu.api.pattern.Predicates.any;
import static com.gregtechceu.gtceu.api.pattern.Predicates.blocks;
import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;
import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * Original GTNA multiblocks (no source mod). Structures come from the author's builds through
 * {@code tools/design/convert_originals.py}, which writes each {@code pattern/<name>.mbs} and a JSON sidecar with
 * the letter -> block table read here. Designs live in {@code docs/roadmap/design/}.
 */
public final class GTNAOriginals {

    /** Centre of the Stellar Containment Chamber; taken into the controller while the star is lit. */
    public static final BlockEntry<Block> DEGENERATE_MATTER_CORE = GTNABlocks
            .createCasingBlock("degenerate_matter_core");

    // ------------------------------------------------------------------ items
    private static final Map<ColliderCore.Particle, ItemEntry<ComponentItem>> PARTICLES = new EnumMap<>(
            ColliderCore.Particle.class);
    static {
        for (var p : ColliderCore.Particle.values()) {
            String id = "contained_" + p.name().toLowerCase();
            PARTICLES.put(p, item(id, "Contained " + english(p)));
        }
    }
    public static final ItemEntry<ComponentItem> ANTIPROTON_CELL = item("antiproton_cell", "Antiproton Penning Cell");
    public static final ItemEntry<ComponentItem> RIFT_PROBE = item("rift_probe", "Rift Probe");
    public static final ItemEntry<ComponentItem> DEPTH_ANCHOR = item("depth_anchor", "Depth Anchor");
    public static final ItemEntry<ComponentItem> RIFT_SINGULARITY = item("rift_singularity", "Rift Singularity");

    private static final Map<com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body, ItemEntry<ComponentItem>> CARTRIDGES = new EnumMap<>(
            com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body.class);
    static {
        for (var b : com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body.values())
            CARTRIDGES.put(b, item("target_cartridge_" + b.name().toLowerCase(),
                    "Target Cartridge (" + bodyName(b) + ")"));
    }

    // ------------------------------------------------------------------ special hatches
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition BEAM_DUMP = hatch("beam_dump",
            "Beam Dump", com.gregtechceu.gtceu.api.GTValues.UIV, OriginalHatchPartMachine.Kind.BEAM_DUMP,
            GTNAPartAbility.BEAM_DUMP, null);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition SEISMIC_PROBE = hatch("seismic_probe",
            "Seismic Probe", com.gregtechceu.gtceu.api.GTValues.UXV, OriginalHatchPartMachine.Kind.SEISMIC_PROBE,
            GTNAPartAbility.SEISMIC_PROBE, null);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition LINER_HATCH = hatch("liner_hatch",
            "Barrel Liner Hatch", com.gregtechceu.gtceu.api.GTValues.UEV, OriginalHatchPartMachine.Kind.LINER,
            GTNAPartAbility.LINER_HATCH, s -> LanceMachine.linerLife(s) > 0);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition MASS_INJECTOR = hatch("mass_injector",
            "Mass Injector", com.gregtechceu.gtceu.api.GTValues.UXV, OriginalHatchPartMachine.Kind.MASS_INJECTOR,
            GTNAPartAbility.MASS_INJECTOR, s -> StellarChamberMachine.itemFeedValue(s) > 0);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition DETECTOR_HATCH = hatch("detector_hatch",
            "Collision Detector Hatch", com.gregtechceu.gtceu.api.GTValues.UIV,
            OriginalHatchPartMachine.Kind.DETECTOR, GTNAPartAbility.DETECTOR_HATCH, null);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition CARTRIDGE_HATCH = hatch(
            "target_cartridge_hatch", "Target Cartridge Hatch", com.gregtechceu.gtceu.api.GTValues.UEV,
            OriginalHatchPartMachine.Kind.TARGET_CARTRIDGE, GTNAPartAbility.TARGET_CARTRIDGE,
            s -> cartridgeBody(s) != null);
    public static final com.gregtechceu.gtceu.api.machine.MachineDefinition TUNING_HATCH = hatch("tuning_hatch",
            "Rift Tuning Hatch", com.gregtechceu.gtceu.api.GTValues.UIV, OriginalHatchPartMachine.Kind.TUNING,
            GTNAPartAbility.TUNING_HATCH, null);

    // ------------------------------------------------------------------ machines
    public static final MultiblockMachineDefinition STELLAR_CONTAINMENT_CHAMBER = REGISTRATE
            .multiblock("stellar_containment_chamber", StellarChamberMachine::new)
            .langValue("Stellar Containment Chamber")
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTNABlocks.RADIANT_NAQUADAH_ALLOY_CASING)
            .pattern(definition -> pattern(definition, "stellar_containment_chamber",
                    "gtna:radiant_naquadah_alloy_casing",
                    h -> h.or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(8).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.SEISMIC_PROBE).setMaxGlobalLimited(1).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.MASS_INJECTOR).setMaxGlobalLimited(4).setPreviewCount(1))))
            .modelProperty(com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.RECIPE_LOGIC_STATUS,
                    com.gregtechceu.gtceu.api.machine.trait.RecipeLogic.Status.IDLE)
            .model(com.gregtechceu.gtceu.common.data.models.GTMachineModels.createWorkableCasingMachineModel(
                    GTNACORE.id("block/casings/radiant_naquadah_alloy_casing"),
                    com.gregtechceu.gtceu.GTCEu.id("block/multiblock/fusion_reactor"))
                    .andThen(builder -> builder.addDynamicRenderer(
                            com.raishxn.gtna.client.renderer.machine.StellarChamberRenderer::new)))
            .register();

    public static final MultiblockMachineDefinition ANTIMATTER_COLLIDER_RING = REGISTRATE
            .multiblock("antimatter_collider_ring", ColliderRingMachine::new)
            .langValue("Antimatter Collider Ring")
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTNABlocks.PRECISION_FIELD_SYNC_CASING)
            .pattern(definition -> pattern(definition, "antimatter_collider_ring", "gtna:precision_field_sync_casing",
                    h -> h.or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(4).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.BEAM_DUMP).setMaxGlobalLimited(1).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.DETECTOR_HATCH).setMaxGlobalLimited(1).setPreviewCount(1))))
            .modelProperty(com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.RECIPE_LOGIC_STATUS,
                    com.gregtechceu.gtceu.api.machine.trait.RecipeLogic.Status.IDLE)
            .model(com.gregtechceu.gtceu.common.data.models.GTMachineModels.createWorkableCasingMachineModel(
                    GTNACORE.id("block/casings/nano_forge/precision_field_sync_casing"),
                    com.gregtechceu.gtceu.GTCEu.id("block/multiblock/fusion_reactor"))
                    .andThen(builder -> builder.addDynamicRenderer(
                            com.raishxn.gtna.client.renderer.machine.OriginalsRenderer.ColliderRender::new)))
            .register();

    public static final MultiblockMachineDefinition DIMENSIONAL_RIFT_GATE = REGISTRATE
            .multiblock("dimensional_rift_gate", RiftGateMachine::new)
            .langValue("Dimensional Rift Gate")
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING)
            .pattern(
                    definition -> pattern(definition, "dimensional_rift_gate", "gtna:dimensionally_transcendent_casing",
                            h -> h.or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(4).setPreviewCount(1))
                                    .or(abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                                    .or(abilities(PartAbility.EXPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                                    .or(abilities(GTNAPartAbility.TUNING_HATCH).setMaxGlobalLimited(1)
                                            .setPreviewCount(1))))
            .modelProperty(com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.RECIPE_LOGIC_STATUS,
                    com.gregtechceu.gtceu.api.machine.trait.RecipeLogic.Status.IDLE)
            .model(com.gregtechceu.gtceu.common.data.models.GTMachineModels.createWorkableCasingMachineModel(
                    GTNACORE.id("block/casings/dimensionally_transcendent_casing"),
                    com.gregtechceu.gtceu.GTCEu.id("block/multiblock/fusion_reactor"))
                    .andThen(builder -> builder.addDynamicRenderer(
                            com.raishxn.gtna.client.renderer.machine.OriginalsRenderer.RiftRender::new)))
            .register();

    public static final MultiblockMachineDefinition KINETIC_ORBITAL_LANCE = REGISTRATE
            .multiblock("kinetic_orbital_lance", LanceMachine::new)
            .langValue("Kinetic Orbital Lance")
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(() -> ForgeRegistries.BLOCKS.getValue(new ResourceLocation("gtceu:clean_machine_casing")))
            .pattern(definition -> pattern(definition, "kinetic_orbital_lance", "gtceu:clean_machine_casing",
                    h -> h.or(abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setMaxGlobalLimited(4).setPreviewCount(1))
                            .or(abilities(PartAbility.COMPUTATION_DATA_RECEPTION).setMaxGlobalLimited(1)
                                    .setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.LINER_HATCH).setMaxGlobalLimited(1).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.TARGET_CARTRIDGE).setMaxGlobalLimited(1)
                                    .setPreviewCount(1))))
            .modelProperty(com.gregtechceu.gtceu.api.machine.property.GTMachineModelProperties.RECIPE_LOGIC_STATUS,
                    com.gregtechceu.gtceu.api.machine.trait.RecipeLogic.Status.IDLE)
            .model(com.gregtechceu.gtceu.common.data.models.GTMachineModels.createWorkableCasingMachineModel(
                    com.gregtechceu.gtceu.GTCEu.id("block/casings/solid/machine_casing_clean_stainless_steel"),
                    com.gregtechceu.gtceu.GTCEu.id("block/multiblock/fusion_reactor"))
                    .andThen(builder -> builder.addDynamicRenderer(
                            com.raishxn.gtna.client.renderer.machine.OriginalsRenderer.LanceRender::new)))
            .register();

    private GTNAOriginals() {}

    private static com.gregtechceu.gtceu.api.machine.MachineDefinition hatch(String id, String name, int tier,
                                                                             OriginalHatchPartMachine.Kind kind,
                                                                             PartAbility ability,
                                                                             java.util.function.Predicate<net.minecraft.world.item.ItemStack> filter) {
        return REGISTRATE.machine(id, holder -> new OriginalHatchPartMachine(holder, tier, kind, filter))
                .langValue(name)
                .tier(tier)
                .rotationState(RotationState.ALL)
                .abilities(ability)
                .model(com.gregtechceu.gtceu.common.data.models.GTMachineModels
                        .createColorOverlayTieredHullMachineModel(GTNACORE.id("block/overlay/machine/" + id), null,
                                null))
                .tooltips(net.minecraft.network.chat.Component.translatable("gtna.machine." + id + ".tooltip.0"),
                        net.minecraft.network.chat.Component.translatable("gtna.machine." + id + ".tooltip.1"))
                .register();
    }

    public static Item particle(ColliderCore.Particle p) {
        return PARTICLES.get(p).get();
    }

    public static void init() {}

    public static Item cartridge(com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body b) {
        return CARTRIDGES.get(b).get();
    }

    /** Body a target cartridge points at, or null. */
    @org.jetbrains.annotations.Nullable
    public static com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body cartridgeBody(
                                                                                          net.minecraft.world.item.ItemStack stack) {
        for (var e : CARTRIDGES.entrySet()) if (stack.is(e.getValue().get())) return e.getKey();
        return null;
    }

    private static String bodyName(com.raishxn.gtna.api.machine.feature.lance.LanceCore.Body b) {
        return switch (b) {
            case MOON -> "Moon";
            case PHOBOS -> "Phobos";
            case VESTA -> "Vesta";
            case CERES -> "Ceres";
            case PSYCHE -> "Psyche";
            case EUROPA -> "Europa";
            case ARROKOTH -> "Arrokoth";
            case NEXUS_1 -> "Nexus-1";
        };
    }

    // ------------------------------------------------------------------ helpers

    private static ItemEntry<ComponentItem> item(String id, String lang) {
        return REGISTRATE.item(id, ComponentItem::create).lang(lang)
                .model((ctx, provider) -> provider.generated(ctx, GTNACORE.id("item/originals/" + id))).register();
    }

    private static String english(ColliderCore.Particle p) {
        return switch (p) {
            case ANTIPROTON -> "Antiprotons";
            case KAON -> "Kaons";
            case LAMBDA -> "Lambda Hyperons";
            case CHARM -> "Charm Quarks";
            case BOTTOM -> "Bottom Quarks";
            case W_BOSON -> "W Bosons";
            case Z_BOSON -> "Z Bosons";
            case HIGGS -> "Higgs Bosons";
            case TOP -> "Top Quarks";
            case X_NEXUS -> "X(Nexus) Particles";
        };
    }

    /**
     * Pattern from {@code pattern/<name>.mbs} and its JSON sidecar: every letter maps to a block id; "hatch" letters
     * accept {@code hatchCasing} or the abilities added by {@code hatches}; the degenerate core may also be air.
     */
    static BlockPattern pattern(MultiblockMachineDefinition definition, String name, String hatchCasing,
                                Function<TraceabilityPredicate, TraceabilityPredicate> hatches) {
        var pattern = GTNAMultiBlockFileReader.start(definition, name);
        for (var entry : sidecar(name).getAsJsonObject("letters").entrySet()) {
            char letter = entry.getKey().charAt(0);
            String raw = entry.getValue().getAsString();
            String id = raw.split("[#|]")[0];
            if ("hatch".equals(id)) pattern.where(letter, hatches.apply(block(hatchCasing)));
            // Moving parts are taken into the controller while it runs, so their place may be air.
            else if (raw.contains("#")) pattern.where(letter, block(id).or(air()));
            else if ("gtna:degenerate_matter_core".equals(id))
                pattern.where(letter, blocks(DEGENERATE_MATTER_CORE.get()).or(air()));
            else pattern.where(letter, block(id));
        }
        return pattern.where('~', controller(blocks(definition.getBlock()))).where(' ', any()).build();
    }

    private static JsonObject sidecar(String name) {
        try (var in = GTNAOriginals.class.getClassLoader().getResourceAsStream("pattern/" + name + ".json")) {
            if (in == null) throw new IllegalStateException("Missing pattern/" + name + ".json");
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (java.io.IOException e) {
            throw new RuntimeException(e);
        }
    }

    private static TraceabilityPredicate block(String id) {
        return blocks(ForgeRegistries.BLOCKS.getValue(new ResourceLocation(id)));
    }
}
