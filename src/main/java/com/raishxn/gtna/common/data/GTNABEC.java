package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.item.ComponentItem;
import com.gregtechceu.gtceu.api.machine.MachineDefinition;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.PartAbility;
import com.gregtechceu.gtceu.api.pattern.MultiblockState;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;
import com.gregtechceu.gtceu.common.data.models.GTMachineModels;

import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.client.renderer.RenderType;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.material.MapColor;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.machine.multiblock.GTNAPartAbility;
import com.raishxn.gtna.common.block.BECConduitBlock;
import com.raishxn.gtna.common.data.multiblock.GTNAMultiBlockFileReader;
import com.raishxn.gtna.common.machine.multiblock.electric.bec.*;
import com.raishxn.gtna.common.machine.multiblock.part.bec.*;
import com.tterrag.registrate.util.entry.BlockEntry;
import com.tterrag.registrate.util.entry.ItemEntry;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

import static com.gregtechceu.gtceu.api.pattern.Predicates.abilities;
import static com.gregtechceu.gtceu.api.pattern.Predicates.any;
import static com.gregtechceu.gtceu.api.pattern.Predicates.blocks;
import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;
import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;
import static com.raishxn.gtna.common.data.GTNABlocks.*;

/**
 * GTNH Bose-Einstein Condensate (TecTech, GT5-Unofficial {@code 9b4c2a7}; controller and hatch recipes from
 * NewHorizonsCoreMod): the conduit, the hatches, the metamaterials and the five multiblocks. Structures are converted
 * by {@code tools/convert_bec_structures.py}; art is GT5U's (LGPL-3.0).
 */
public final class GTNABEC {

    private GTNABEC() {}

    static {
        REGISTRATE.creativeModeTab(() -> GTNACreativeModeTabs.BLOCKS);
    }

    // ---- conduits

    public static final BlockEntry<BECConduitBlock> BEC_CONDUIT = conduit("bec_conduit", false);
    public static final BlockEntry<BECConduitBlock> BEC_CONDUIT_CASING = conduit("bec_conduit_casing", true);

    private static BlockEntry<BECConduitBlock> conduit(String name, boolean full) {
        return REGISTRATE.block(name, p -> new BECConduitBlock(p, full))
                .initialProperties(() -> Blocks.IRON_BLOCK)
                .properties(p -> {
                    p.mapColor(MapColor.METAL).strength(5.0f, 6.0f).sound(SoundType.METAL)
                            .requiresCorrectToolForDrops();
                    return full ? p : p.noOcclusion();
                })
                .addLayer(() -> RenderType::cutout)
                .blockstate((ctx, prov) -> {})
                .color(() -> () -> GTNABEC::conduitColor)
                .tag(net.minecraft.tags.BlockTags.MINEABLE_WITH_PICKAXE)
                .item()
                .color(() -> () -> (stack, layer) -> layer == 0 ? 0x26252e : 0xdee6e6)
                .model((ctx, prov) -> prov.withExistingParent(ctx.getName(), prov.modLoc("block/bec/" + name +
                        "_inventory")))
                .build()
                .register();
    }

    /** GTNH conduit colours: background 0x26252e, bar 0xdee6e6 modulated by the dye. */
    private static int conduitColor(net.minecraft.world.level.block.state.BlockState state,
                                    net.minecraft.world.level.BlockAndTintGetter level,
                                    net.minecraft.core.BlockPos pos, int tint) {
        if (tint == 0) return 0x26252e;
        int color = state.getValue(BECConduitBlock.COLOR);
        if (color >= 16) return 0xdee6e6;
        float[] dye = net.minecraft.world.item.DyeColor.byId(color).getTextureDiffuseColors();
        return ((int) (dye[0] * 0xde) << 16) | ((int) (dye[1] * 0xe6) << 8) | (int) (dye[2] * 0xe6);
    }

    // ---- metamaterials (GTNH MetaGeneratedItem03 327..., "primitive/pristine/perfected" and four-tier names)

    public static final List<ItemEntry<ComponentItem>> METAMATERIALS = new ArrayList<>();
    public static final ItemEntry<ComponentItem>[] SHIELDING = metamaterials("shielding", "Shielding", 3);
    public static final ItemEntry<ComponentItem>[] WAVEGUIDE = metamaterials("waveguide", "Waveguide", 3);
    public static final ItemEntry<ComponentItem>[] ENERGY_CONDUIT = metamaterials("energy_conduit",
            "Energy Conduit", 3);
    public static final ItemEntry<ComponentItem>[] ELECTROGRAVITIC_VALVE = metamaterials("electrogravitic_valve",
            "Electrogravitic Valve", 3);
    public static final ItemEntry<ComponentItem>[] WAVE_FOCUS = metamaterials("wave_focus", "Wave Focus", 4);
    public static final ItemEntry<ComponentItem>[] RESONANCE_CHAMBER = metamaterials("resonance_chamber",
            "Resonance Chamber", 4);
    public static final ItemEntry<ComponentItem>[] SENSOR_ARRAY = metamaterials("sensor_array", "Sensor Array", 4);
    public static final ItemEntry<ComponentItem>[] FIELD_MANIPULATOR = metamaterials("field_manipulator",
            "Field Manipulator", 4);

    @SuppressWarnings("unchecked")
    private static ItemEntry<ComponentItem>[] metamaterials(String id, String lang, int tiers) {
        String[] adjectives = tiers == 3 ? new String[] { "Primitive", "Pristine", "Perfected" } :
                new String[] { "Rough", "Reinforced", "Refined", "Resplendent" };
        ItemEntry<ComponentItem>[] out = new ItemEntry[tiers];
        for (int i = 0; i < tiers; i++) {
            String name = "metamaterial_" + id + "_" + (i + 1);
            out[i] = REGISTRATE.item(name, ComponentItem::create)
                    .lang(adjectives[i] + " " + lang)
                    .model((ctx, prov) -> prov.generated(ctx, GTNACORE.id("item/bec/" + name)))
                    .register();
            METAMATERIALS.add(out[i]);
        }
        return out;
    }

    /** GTNH {@code Transdimensional_Alignment_Matrix} (the Convergence item; an Astral Array Fabricator input). */
    public static final ItemEntry<ComponentItem> TRANSDIMENSIONAL_ALIGNMENT_MATRIX = REGISTRATE
            .item("transdimensional_alignment_matrix", ComponentItem::create)
            .lang("Transdimensional Alignment Matrix")
            .model((ctx, prov) -> prov.generated(ctx, GTNACORE.id("item/bec/transdimensional_alignment_matrix")))
            .register();

    // ---- hatches

    public static final MachineDefinition BEC_HATCH = REGISTRATE
            .machine("bec_hatch", BECHatchPartMachine::new)
            .langValue("Bose-Einstein Condensate Hatch")
            .tier(GTValues.UIV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.BEC_HATCH)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(GTNACORE.id("block/bec/bec_hatch"), null,
                    null))
            .tooltips(Component.translatable("gtna.machine.bec_hatch.tooltip.0"),
                    Component.translatable("gtna.machine.bec_hatch.tooltip.1"))
            .register();

    public static final MachineDefinition NANITE_CONTAINMENT_BUS = REGISTRATE
            .machine("nanite_containment_bus", NaniteContainmentBusPartMachine::new)
            .langValue("Nanite Containment Bus")
            .tier(GTValues.UHV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.NANITE_CONTAINMENT_BUS)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(GTNACORE.id("block/bec/nanite_hatch"),
                    null, GTNACORE.id("block/bec/nanite_hatch_emissive")))
            .tooltips(Component.translatable("gtna.machine.nanite_containment_bus.tooltip.0"),
                    Component.translatable("gtna.machine.nanite_containment_bus.tooltip.1"))
            .register();

    public static final MachineDefinition LINE_OF_SIGHT_HATCH = REGISTRATE
            .machine("line_of_sight_connector_hatch", LineOfSightHatchPartMachine::new)
            .langValue("Line-Of-Sight Connector Hatch")
            .tier(GTValues.UIV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.LINE_OF_SIGHT_HATCH)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(
                    GTNACORE.id("block/bec/bec_hatch_active"), null, null)
                    .andThen(builder -> builder.addDynamicRenderer(
                            com.raishxn.gtna.client.renderer.machine.LineOfSightBeamRenderer::new)))
            .tooltips(Component.translatable("gtna.machine.line_of_sight_connector_hatch.tooltip.0"),
                    Component.translatable("gtna.machine.line_of_sight_connector_hatch.tooltip.1"),
                    Component.translatable("gtna.machine.line_of_sight_connector_hatch.tooltip.2"),
                    Component.translatable("gtna.machine.line_of_sight_connector_hatch.tooltip.3",
                            LineOfSightHatchPartMachine.SCAN_DIST))
            .register();

    public static final MachineDefinition NANITE_DETECTOR_HATCH = REGISTRATE
            .machine("nanite_detector_hatch", NaniteDetectorHatchPartMachine::new)
            .langValue("Nanite Tier Detector Hatch")
            .tier(GTValues.UIV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.NANITE_DETECTOR_HATCH)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(
                    GTNACORE.id("block/bec/nanite_detector"), null, GTNACORE.id("block/bec/nanite_detector_emissive")))
            .tooltips(Component.translatable("gtna.machine.nanite_detector_hatch.tooltip.0"),
                    Component.translatable("gtna.machine.nanite_detector_hatch.tooltip.1"),
                    Component.translatable("gtna.machine.nanite_detector_hatch.tooltip.2"))
            .register();

    public static final MachineDefinition CONDENSATE_DETECTOR_HATCH = REGISTRATE
            .machine("condensate_detector_hatch", CondensateDetectorHatchPartMachine::new)
            .langValue("Bose-Einstein Condensate Detector Hatch")
            .tier(GTValues.UIV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.CONDENSATE_DETECTOR_HATCH)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(
                    GTNACORE.id("block/bec/condensate_detector"), null,
                    GTNACORE.id("block/bec/condensate_detector_emissive")))
            .tooltips(Component.translatable("gtna.machine.condensate_detector_hatch.tooltip.0"),
                    Component.translatable("gtna.machine.condensate_detector_hatch.tooltip.1"),
                    Component.translatable("gtna.machine.condensate_detector_hatch.tooltip.2"))
            .register();

    public static final MachineDefinition IO_NODE_CONTROLLER_HATCH = REGISTRATE
            .machine("io_node_controller_hatch", IONodeControllerHatchPartMachine::new)
            .langValue("Teleportation Node Controller Hatch")
            .tier(GTValues.UIV).rotationState(RotationState.ALL)
            .abilities(GTNAPartAbility.IO_NODE_CONTROLLER_HATCH)
            .model(GTMachineModels.createColorOverlayTieredHullMachineModel(
                    GTNACORE.id("block/bec/io_node_controller"), null,
                    GTNACORE.id("block/bec/io_node_controller_emissive")))
            .tooltips(Component.translatable("gtna.machine.io_node_controller_hatch.tooltip.0"),
                    Component.translatable("gtna.machine.io_node_controller_hatch.tooltip.1"),
                    Component.translatable("gtna.machine.io_node_controller_hatch.tooltip.2"))
            .register();

    // ---- multiblocks

    private static TraceabilityPredicate casing(BlockEntry<Block> block) {
        return blocks(block.get());
    }

    /** The Maxwell Gate's input hatch slot: records the hatch position for {@link BECDiodeMachine}. */
    private static TraceabilityPredicate diodeInput() {
        return new TraceabilityPredicate((MultiblockState state) -> {
            if (state.getTileEntity() instanceof com.gregtechceu.gtceu.api.machine.IMachineBlockEntity mbe &&
                    mbe.getMetaMachine() instanceof BECHatchPartMachine) {
                state.getMatchContext().set(BECDiodeMachine.INPUT_HATCH, state.getPos().immutable());
                return true;
            }
            return false;
        }, () -> new BlockInfo[] { BlockInfo.fromBlockState(BEC_HATCH.getBlock().defaultBlockState()) });
    }

    private static MultiblockMachineDefinition bec(String id, String lang,
                                                   Function<com.gregtechceu.gtceu.api.machine.IMachineBlockEntity, ? extends BECMultiblockMachine> factory,
                                                   com.gregtechceu.gtceu.api.recipe.GTRecipeType type,
                                                   BlockEntry<Block> appearance,
                                                   Function<MultiblockMachineDefinition, com.gregtechceu.gtceu.api.pattern.BlockPattern> pattern,
                                                   String casingTexture) {
        return REGISTRATE.multiblock(id, holder -> factory.apply(holder))
                .langValue(lang)
                .rotationState(RotationState.NON_Y_AXIS)
                .recipeType(type)
                .recipeModifier(
                        (machine, recipe) -> com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction.IDENTITY)
                .appearanceBlock(appearance)
                .pattern(pattern::apply)
                .workableCasingModel(GTNACORE.id("block/casings/bec/" + casingTexture),
                        GTNACORE.id("block/multiblock/bec/" + id))
                .register();
    }

    public static final MultiblockMachineDefinition BEC_GENERATOR = bec("bec_generator",
            "Bose-Einstein Condensate Entanglement Apparatus", BECGeneratorMachine::new,
            GTNARecipeType.CONDENSATE_GENERATOR_RECIPES, ELECTROMAGNETICALLY_ISOLATED_CASING,
            def -> GTNAMultiBlockFileReader.start(def, "bec_generator")
                    .where('A', casing(COHERENCE_PRESERVING_PLASMA_CONDUIT))
                    .where('B', casing(ELECTROMAGNETICALLY_ISOLATED_CASING))
                    .where('C', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR))
                    .where('D', casing(CONFLICT_INDUCEMENT_CASING))
                    .where('E', casing(PEACE_ENFORCEMENT_CASING))
                    .where('F', casing(CONDENSATE_TRANSFORMATIVE_COIL))
                    .where('G', casing(ELECTROMAGNETIC_WAVEGUIDE))
                    .where('1', casing(ELECTROMAGNETICALLY_ISOLATED_CASING)
                            .or(abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(16).setPreviewCount(0)))
                    .where('2', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.BEC_HATCH).setPreviewCount(1)))
                    .where('~', controller(blocks(def.getBlock())))
                    .where(' ', any())
                    .build(),
            "electromagnetically_isolated_casing");

    public static final MultiblockMachineDefinition BEC_STORAGE = bec("bec_storage",
            "Bose-Einstein Condensate Containment Field", BECStorageMachine::new, GTRecipeTypes.DUMMY_RECIPES,
            FINE_STRUCTURE_CONSTANT_MANIPULATOR,
            def -> GTNAMultiBlockFileReader.start(def, "bec_storage")
                    .where('A', casing(COHERENCE_PRESERVING_PLASMA_CONDUIT))
                    .where('B', casing(ELECTROMAGNETICALLY_ISOLATED_CASING)
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(42).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(42).setPreviewCount(0))
                            .or(abilities(GTNAPartAbility.CONDENSATE_DETECTOR_HATCH).setMaxGlobalLimited(42)
                                    .setPreviewCount(0)))
                    .where('C', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR))
                    .where('D', casing(CONFLICT_INDUCEMENT_CASING))
                    .where('E', casing(PEACE_ENFORCEMENT_CASING))
                    .where('F', casing(CONDENSATE_TRANSFORMATIVE_COIL))
                    .where('G', casing(CONDENSATE_GUIDANCE_COIL))
                    .where('H', casing(ELECTROMAGNETIC_WAVEGUIDE))
                    .where('1', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.BEC_HATCH).setMaxGlobalLimited(4).setPreviewCount(1)))
                    .where('~', controller(blocks(def.getBlock())))
                    .where(' ', any())
                    .build(),
            "fine_structure_constant_manipulator");

    public static final MultiblockMachineDefinition BEC_ASSEMBLER = bec("bec_assembler",
            "Bose-Einstein Condensate Observation Array", BECAssemblerMachine::new,
            GTNARecipeType.CONDENSATE_ASSEMBLER_RECIPES, COHERENCE_PRESERVING_PLASMA_CONDUIT,
            def -> GTNAMultiBlockFileReader.start(def, "bec_assembler")
                    .where('A', casing(COHERENCE_PRESERVING_PLASMA_CONDUIT))
                    .where('B', casing(ELECTROMAGNETICALLY_ISOLATED_CASING))
                    .where('C', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR))
                    .where('D', casing(CONFLICT_INDUCEMENT_CASING))
                    .where('E', casing(PEACE_ENFORCEMENT_CASING))
                    .where('F', casing(CONDENSATE_TRANSFORMATIVE_COIL))
                    .where('G', casing(CONDENSATE_GUIDANCE_COIL))
                    .where('H', casing(ELECTROMAGNETIC_WAVEGUIDE))
                    .where('1', casing(ELECTROMAGNETICALLY_ISOLATED_CASING)
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(16).setPreviewCount(0))
                            .or(abilities(GTNAPartAbility.NANITE_CONTAINMENT_BUS).setMaxGlobalLimited(16)
                                    .setPreviewCount(1)))
                    .where('2', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.BEC_HATCH).setMaxGlobalLimited(2).setPreviewCount(1)))
                    .where('3', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.LINE_OF_SIGHT_HATCH).setMaxGlobalLimited(16)
                                    .setPreviewCount(1)))
                    .where('~', controller(blocks(def.getBlock())))
                    .where(' ', any())
                    .build(),
            "coherence_preserving_plasma_conduit");

    public static final MultiblockMachineDefinition BEC_IO_NODE = bec("bec_io_node",
            "Bose-Einstein Condensate Teleportation Node", BECIONodeMachine::new,
            GTNARecipeType.CONDENSATE_ASSEMBLER_RECIPES, COHERENCE_PRESERVING_PLASMA_CONDUIT,
            def -> GTNAMultiBlockFileReader.start(def, "bec_io_node")
                    .where('A', casing(COHERENCE_PRESERVING_PLASMA_CONDUIT))
                    .where('B', casing(ELECTROMAGNETICALLY_ISOLATED_CASING)
                            .or(abilities(PartAbility.IMPORT_ITEMS).setMaxGlobalLimited(32).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setMaxGlobalLimited(32).setPreviewCount(1))
                            .or(abilities(GTNAPartAbility.NANITE_DETECTOR_HATCH).setMaxGlobalLimited(32)
                                    .setPreviewCount(0))
                            .or(abilities(GTNAPartAbility.IO_NODE_CONTROLLER_HATCH).setMaxGlobalLimited(32)
                                    .setPreviewCount(0)))
                    .where('C', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR))
                    .where('D', casing(CONFLICT_INDUCEMENT_CASING))
                    .where('E', casing(PEACE_ENFORCEMENT_CASING))
                    .where('F', casing(CONDENSATE_TRANSFORMATIVE_COIL))
                    .where('G', casing(CONDENSATE_GUIDANCE_COIL))
                    .where('H', casing(ELECTROMAGNETIC_WAVEGUIDE))
                    .where('1', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.LINE_OF_SIGHT_HATCH).setMaxGlobalLimited(1)
                                    .setPreviewCount(1)))
                    .where('~', controller(blocks(def.getBlock())))
                    .where(' ', any())
                    .build(),
            "coherence_preserving_plasma_conduit");

    public static final MultiblockMachineDefinition BEC_DIODE = bec("bec_diode",
            "Bose-Einstein Condensate Maxwell Gate", BECDiodeMachine::new, GTRecipeTypes.DUMMY_RECIPES,
            ELECTROMAGNETICALLY_ISOLATED_CASING,
            def -> GTNAMultiBlockFileReader.start(def, "bec_diode")
                    .where('A', casing(COHERENCE_PRESERVING_PLASMA_CONDUIT))
                    .where('B', casing(ELECTROMAGNETICALLY_ISOLATED_CASING)
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(16).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(16).setPreviewCount(0)))
                    .where('C', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR))
                    .where('D', casing(CONFLICT_INDUCEMENT_CASING))
                    .where('E', casing(PEACE_ENFORCEMENT_CASING))
                    .where('F', casing(CONDENSATE_TRANSFORMATIVE_COIL))
                    .where('G', casing(CONDENSATE_GUIDANCE_COIL))
                    .where('H', casing(ELECTROMAGNETIC_WAVEGUIDE))
                    .where('1', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR).or(diodeInput()))
                    .where('2', casing(FINE_STRUCTURE_CONSTANT_MANIPULATOR)
                            .or(abilities(GTNAPartAbility.BEC_HATCH).setMaxGlobalLimited(1).setPreviewCount(1)))
                    .where('~', controller(blocks(def.getBlock())))
                    .where(' ', any())
                    .build(),
            "electromagnetically_isolated_casing");

    public static void init() {}
}
