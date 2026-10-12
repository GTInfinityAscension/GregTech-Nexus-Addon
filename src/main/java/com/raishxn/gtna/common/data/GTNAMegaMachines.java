package com.raishxn.gtna.common.data;

import com.gregtechceu.gtceu.GTCEu;
import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.data.RotationState;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.CoilWorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.PartAbility;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;
import com.gregtechceu.gtceu.api.recipe.GTRecipeType;
import com.gregtechceu.gtceu.common.data.GCYMBlocks;
import com.gregtechceu.gtceu.common.data.GCYMRecipeTypes;
import com.gregtechceu.gtceu.common.data.GTBlocks;
import com.gregtechceu.gtceu.common.data.GTMaterials;
import com.gregtechceu.gtceu.common.data.GTRecipeModifiers;
import com.gregtechceu.gtceu.common.data.GTRecipeTypes;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.machine.multiblock.GTNAPartAbility;
import com.raishxn.gtna.common.data.multiblock.GTNAGTOPatterns;
import com.raishxn.gtna.common.data.multiblock.GTOCompressedPatternReader;
import com.raishxn.gtna.common.machine.multiblock.electric.CoilWorkableElectricMultipleRecipesMachine;
import com.raishxn.gtna.common.machine.multiblock.electric.InfinityFluidDrillMachine;
import com.raishxn.gtna.common.machine.multiblock.electric.WorkableElectricMultipleRecipesMachine;

import static com.gregtechceu.gtceu.api.pattern.Predicates.abilities;
import static com.gregtechceu.gtceu.api.pattern.Predicates.any;
import static com.gregtechceu.gtceu.api.pattern.Predicates.autoAbilities;
import static com.gregtechceu.gtceu.api.pattern.Predicates.blocks;
import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;
import static com.gregtechceu.gtceu.api.pattern.Predicates.frames;
import static com.gregtechceu.gtceu.api.pattern.Predicates.heatingCoils;
import static com.raishxn.gtna.api.registry.GTNARegistry.REGISTRATE;

/**
 * GTOCore "mega" multiblocks of ROADMAP-multiblocos Phase B (G-0204): the patterns are GTO's own {@code .mbs} files
 * and every block is a GTCEu block or its GTNA port. GTO's cross-recipe bases map to the GTNA multi-recipe machines
 * (Thread Hatch for extra recipes, coil parallel {@code 2^(coil K / 900)}); GTO's {@code autoThreadLaserAbilities}
 * maps to {@link #threadLaserAbilities}.
 */
public final class GTNAMegaMachines {

    private GTNAMegaMachines() {}

    private static boolean modulesRegistered;

    public static void init() {
        if (modulesRegistered) return;
        modulesRegistered = true;
        registerDesulfurizerModule();
        registerReactionFurnaceModule();
    }

    /** GTO {@code autoThreadLaserAbilities}: IO + energy/laser + Thread, Parallel and Overclock hatches. */
    private static TraceabilityPredicate threadLaserAbilities(GTRecipeType... types) {
        return autoAbilities(types, false, false, true, true, true, true)
                .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(2))
                .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                .or(abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1))
                .or(abilities(GTNAPartAbility.OVERCLOCK_HATCH).setMaxGlobalLimited(1));
    }

    private static TraceabilityPredicate absBlocks() {
        return blocks(GTNABlocks.ABS_WHITE_CASING.get(), GTNABlocks.ABS_ORANGE_CASING.get(),
                GTNABlocks.ABS_MAGENTA_CASING.get(), GTNABlocks.ABS_LIGHT_BULL_CASING.get(),
                GTNABlocks.ABS_YELLOW_CASING.get(), GTNABlocks.ABS_LIME_CASING.get(),
                GTNABlocks.ABS_PINK_CASING.get(), GTNABlocks.ABS_GREY_CASING.get(),
                GTNABlocks.ABS_LIGHT_GREY_CASING.get(), GTNABlocks.ABS_CYAN_CASING.get(),
                GTNABlocks.ABS_PURPLE_CASING.get(), GTNABlocks.ABS_BLUE_CASING.get(),
                GTNABlocks.ABS_BROWN_CASING.get(), GTNABlocks.ABS_GREEN_CASING.get(),
                GTNABlocks.ABS_RED_CASING.get(), GTNABlocks.ABS_BLACK_CASING.get());
    }

    /** GTO {@code large_pyrolyse_oven}: Parallel Hatch + GTCEu's coil-scaled Pyrolyse Oven speed. */
    public static final MultiblockMachineDefinition LARGE_PYROLYSE_OVEN = REGISTRATE
            .multiblock("large_pyrolyse_oven", CoilWorkableElectricMultiblockMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.PYROLYSE_RECIPES)
            .recipeModifiers(GTRecipeModifiers::hatchParallel, GTRecipeModifiers::pyrolyseOvenOverclock)
            .appearanceBlock(GTBlocks.CASING_STAINLESS_CLEAN)
            .pattern(definition -> GTOCompressedPatternReader.start("large_pyrolyse_oven")
                    .where('A', frames(GTMaterials.Ruridit))
                    .where('B', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                    .where('C', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1)))
                    .where('D', heatingCoils())
                    .where('E', abilities(PartAbility.MUFFLER))
                    .where('F', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get()))
                    .where('G', frames(GTMaterials.StainlessSteel))
                    .where('H', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_clean_stainless_steel"),
                    GTCEu.id("block/multiblock/pyrolyse_oven"))
            .register();

    /** GTO {@code cracker_hub}: Cracking + Pyrolyse with coil parallel; replaces GTNH/TST mega crackers. */
    public static final MultiblockMachineDefinition CRACKER_HUB = REGISTRATE
            .multiblock("cracker_hub",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.CRACKING_RECIPES)
            .recipeType(GTRecipeTypes.PYROLYSE_RECIPES)
            .appearanceBlock(GTNABlocks.NAQUADAH_ALLOY_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("cracker_hub")
                    .where('A', blocks(GTNABlocks.STRENGTHEN_THE_BASE_BLOCK.get()))
                    .where('B', frames(GTMaterials.Ultimet))
                    .where('C', frames(GTMaterials.HastelloyC276))
                    .where('D', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('E', frames(GTMaterials.StainlessSteel))
                    .where('F', absBlocks())
                    .where('G', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('H', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('I', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('J', abilities(PartAbility.MUFFLER))
                    .where('K', blocks(GTNABlocks.OIL_GAS_TRANSPORTATION_PIPE_CASING.get()))
                    .where('L', blocks(GTNABlocks.HIGH_PRESSURE_PIPE_CASING.get()))
                    .where('M', blocks(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.get()))
                    .where('N', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                    .where('O', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('P', heatingCoils())
                    .where('Q', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('R', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/cracking_unit"))
            .register();

    /** GTO {@code mega_brewer}: Brewing + Fermenting with coil parallel. */
    public static final MultiblockMachineDefinition MEGA_BREWER = REGISTRATE
            .multiblock("mega_brewer",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.BREWING_RECIPES)
            .recipeType(GTRecipeTypes.FERMENTING_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_CORROSION_PROOF)
            .pattern(definition -> GTOCompressedPatternReader.start("mega_brewer")
                    .where('A', blocks(GTBlocks.CASING_PTFE_INERT.get()))
                    .where('B', blocks(GCYMBlocks.CASING_CORROSION_PROOF.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('C', blocks(GCYMBlocks.CASING_CORROSION_PROOF.get()))
                    .where('D', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('E', blocks(GTNABlocks.HERMETIC_CASING_UEV.get()))
                    .where('F', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('G', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('H', controller(blocks(definition.get())))
                    .where('I', blocks(GTNABlocks.CHEMICAL_CORROSION_RESISTANT_PIPE_CASING.get()))
                    .where('J', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('K', frames(GTNAMaterials.HastelloyN))
                    .where('L', heatingCoils())
                    .where('M', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/corrosion_proof_casing"),
                    GTCEu.id("block/multiblock/gcym/large_brewer"))
            .register();

    /**
     * GTO {@code mega_vacuum_drying_furnace}: Vacuum Drying with coil parallel; the coil temperature must meet the
     * recipe's {@code ebf_temp}.
     */
    public static final MultiblockMachineDefinition MEGA_VACUUM_DRYING_FURNACE = REGISTRATE
            .multiblock("mega_vacuum_drying_furnace",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.VACUUM_DRYING_RECIPES)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("mega_vacuum_drying_furnace")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.HIGH_PRESSURE_PIPE_CASING.get()))
                    .where('B', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                    .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('D', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('E', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('F', blocks(GTNABlocks.RED_STEEL_CASING.get()))
                    .where('G', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                    .where('H', heatingCoils())
                    .where('I', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('J', frames(GTMaterials.Tungsten))
                    .where('K', blocks(GTBlocks.COMPUTER_CASING.get()))
                    .where('L', blocks(GTBlocks.COMPUTER_HEAT_VENT.get()))
                    .where('M', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('O', blocks(GTBlocks.HERMETIC_CASING_LuV.get()))
                    .where('P', blocks(GTBlocks.CASING_TUNGSTENSTEEL_GEARBOX.get()))
                    .where('Q', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('a', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code giant_flotation_tank}: the 74-aisle flotation pool; Parallel Hatch + Thread Hatch. */
    public static final MultiblockMachineDefinition GIANT_FLOTATION_TANK = REGISTRATE
            .multiblock("giant_flotation_tank", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.FLOTATING_BENEFICIATION_RECIPES)
            .appearanceBlock(GTNABlocks.HASTELLOY_N_75_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("giant_flotation_tank")
                    .where('A', blocks(GTNABlocks.HASTELLOY_N_75_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('B', controller(blocks(definition.get())))
                    .where('C', blocks(GCYMBlocks.CASING_CORROSION_PROOF.get()))
                    .where('D', blocks(GTNABlocks.ALUMINIUM_BRONZE_CASING.get()))
                    .where('E', blocks(GTNABlocks.HASTELLOY_N_75_CASING.get()))
                    .where('F', blocks(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.get()))
                    .where('G', frames(GTMaterials.WatertightSteel))
                    .where('H', blocks(GTNABlocks.INCONEL_625_PIPE.get()))
                    .where('I', blocks(GTNABlocks.STABILIZED_NAQUADAH_WATER_PLANT_CASING.get()))
                    .where('J', frames(GTMaterials.MaragingSteel300))
                    .where('K', frames(GTMaterials.Duranium))
                    .where('L', blocks(GTNABlocks.HASTELLOY_N_75_GEARBOX.get()))
                    .where('M', blocks(GTNABlocks.HASTELLOY_N_75_PIPE.get()))
                    .where('N', blocks(GTNABlocks.FLOTATION_CELL.get()))
                    .where('O', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hastelloy_n_75_casing"),
                    GTCEu.id("block/multiblock/gcym/large_chemical_bath"))
            .register();

    /** GTO {@code phase_change_cube}: Extractor + Fluid Solidifier with coil parallel. */
    public static final MultiblockMachineDefinition PHASE_CHANGE_CUBE = REGISTRATE
            .multiblock("phase_change_cube",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.EXTRACTOR_RECIPES)
            .recipeType(GTRecipeTypes.FLUID_SOLIDFICATION_RECIPES)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("phase_change_cube")
                    .where('A', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('B', frames(GTMaterials.HastelloyC276))
                    .where('C', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('D', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('E', heatingCoils())
                    .where('F', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('G', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('H', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('I', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code large_incubator}: Incubator with Parallel Hatch; the glass tier caps the voltage tier and the
     * cleanroom filters set the filter tier recipes can ask for. GTO's Radiation Hatch is not ported.
     */
    public static final MultiblockMachineDefinition LARGE_INCUBATOR = REGISTRATE
            .multiblock("large_incubator",
                    com.raishxn.gtna.common.machine.multiblock.electric.LargeIncubatorMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.INCUBATOR_RECIPES)
            .recipeModifiers(com.raishxn.gtna.common.machine.multiblock.electric.LargeIncubatorMachine::filterCheck,
                    GTRecipeModifiers.PARALLEL_HATCH, GTRecipeModifiers.OC_NON_PERFECT_SUBTICK)
            .appearanceBlock(GTBlocks.PLASTCRETE)
            .pattern(definition -> GTOCompressedPatternReader.start("large_incubator")
                    .where('A', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTBlocks.PLASTCRETE.get())
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('C', controller(blocks(definition.get())))
                    .where('D', com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers.glass())
                    .where('E', com.gregtechceu.gtceu.api.pattern.Predicates.cleanroomFilters())
                    .where('F', blocks(net.minecraft.world.level.block.Blocks.SPONGE))
                    .where('G', blocks(GTBlocks.PLASTCRETE.get()))
                    .where('H', blocks(GTBlocks.CASING_POLYTETRAFLUOROETHYLENE_PIPE.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/cleanroom/plascrete"),
                    GTCEu.id("block/multiblock/gcym/large_maceration_tower"))
            .register();

    /**
     * GTO {@code engraving_laser_plant}: Laser Engraver (Parallel Hatch) and Precision Laser
     * Engraving (serial, {@code gtna:precision_laser_engraver}); GTO's Laser Welder mode is not ported; perfect
     * overclock for all three.
     */
    public static final MultiblockMachineDefinition ENGRAVING_LASER_PLANT = REGISTRATE
            .multiblock("engraving_laser_plant", WorkableElectricMultiblockMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.LASER_ENGRAVER_RECIPES)
            .recipeType(GTNARecipeType.PRECISION_LASER_ENGRAVER_RECIPES)
            .recipeModifiers((machine, recipe) -> recipe.recipeType == GTNARecipeType.PRECISION_LASER_ENGRAVER_RECIPES ?
                    com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction.IDENTITY :
                    GTRecipeModifiers.hatchParallel(machine, recipe),
                    GTRecipeModifiers.OC_PERFECT)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("engraving_laser_plant")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('B', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('C', frames(GTMaterials.Neutronium))
                    .where('D', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('E', blocks(GTNABlocks.COMPONENT_ASSEMBLY_LINE_CASING_UV.get()))
                    .where('F', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('G', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where('H', blocks(GTBlocks.HERMETIC_CASING_UHV.get()))
                    .where('I', blocks(GTNABlocks.OPTICAL_RESONANCE_CHAMBER.get()))
                    .where('J', blocks(GTBlocks.FILTER_CASING_STERILE.get()))
                    .where('K', blocks(GTNABlocks.ADVANCED_COMPRESSED_FUSION_COIL.get()))
                    .where('L', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('M', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('a', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(PartAbility.IMPORT_ITEMS).setPreviewCount(1))
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setPreviewCount(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/gcym/large_engraving_laser"))
            .register();

    /** GTO {@code infinity_fluid_drilling_rig}: ZPM rig, 256x yield, no depletion; UV energy adds 50%. */
    public static final MultiblockMachineDefinition INFINITY_FLUID_DRILLING_RIG = REGISTRATE
            .multiblock("infinity_fluid_drilling_rig",
                    holder -> new InfinityFluidDrillMachine(holder, GTValues.ZPM, 256))
            .rotationState(RotationState.ALL)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("infinity_fluid_drilling_rig")
                    .where('S', controller(blocks(definition.get())))
                    .where('X', blocks(GTNABlocks.IRIDIUM_CASING.get()).setMinGlobalLimited(3)
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_FLUIDS).setMaxGlobalLimited(1).setPreviewCount(1)))
                    .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('F', frames(GTMaterials.Ruridit))
                    .where('#', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/fluid_drilling_rig"))
            .register();

    /** GTL {@code mega_distillery}: Distillery, Distillation Tower and Evaporation with a Parallel Hatch. */
    public static final MultiblockMachineDefinition MEGA_DISTILLERY = REGISTRATE
            .multiblock("mega_distillery", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DISTILLERY_RECIPES)
            .recipeType(GTRecipeTypes.DISTILLATION_RECIPES)
            .recipeType(GTNARecipeType.EVAPORATION_RECIPES)
            .appearanceBlock(GTBlocks.CASING_STAINLESS_CLEAN)
            .pattern(definition -> GTOCompressedPatternReader.start("mega_distillery")
                    .where('b', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()).setMinGlobalLimited(600)
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                            .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(1))
                            .or(abilities(GTNAPartAbility.THREAD_HATCH).setMaxGlobalLimited(1)))
                    .where('a', frames(GTMaterials.Trinium))
                    .where('c', blocks(GCYMBlocks.CASING_WATERTIGHT.get()))
                    .where('d', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                    .where('e', blocks(GTBlocks.COIL_TRITANIUM.get()))
                    .where('f', blocks(GTNABlocks.HERMETIC_CASING_UEV.get()))
                    .where('~', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_clean_stainless_steel"),
                    GTCEu.id("block/multiblock/gcym/large_distillery"))
            .register();

    /** GTO {@code super_blast_smelter}: EBF + Alloy Blast; Parallel Hatch, coil temperature gate, Thread Hatch. */
    public static final MultiblockMachineDefinition SUPER_BLAST_SMELTER = REGISTRATE
            .multiblock("super_blast_smelter",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, false, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.BLAST_RECIPES)
            .recipeType(GCYMRecipeTypes.ALLOY_BLAST_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING)
            .pattern(definition -> GTOCompressedPatternReader.start("super_blast_smelter")
                    .where('A', blocks(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('B', controller(blocks(definition.get())))
                    .where('C', blocks(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get()))
                    .where('D', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where('E', blocks(GTBlocks.CASING_ENGINE_INTAKE.get()))
                    .where('F', blocks(GTBlocks.STEEL_HULL.get()))
                    .where('G', blocks(GTBlocks.FIREBOX_BRONZE.get()))
                    .where('H', blocks(GTBlocks.CASING_BRONZE_PIPE.get()))
                    .where('I', blocks(GTBlocks.CASING_POLYTETRAFLUOROETHYLENE_PIPE.get()))
                    .where('J', blocks(GTBlocks.FIREBOX_STEEL.get()))
                    .where('K', blocks(GTBlocks.CASING_EXTREME_ENGINE_INTAKE.get()))
                    .where('L', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('M', blocks(GTBlocks.CASING_STEEL_PIPE.get()))
                    .where('N', blocks(GTBlocks.FIREBOX_TITANIUM.get()))
                    .where('O', blocks(GTBlocks.CASING_TITANIUM_PIPE.get()))
                    .where('P', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('Q', blocks(GTBlocks.FIREBOX_TUNGSTENSTEEL.get()))
                    .where('R', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('S', heatingCoils())
                    .where('T', frames(GTMaterials.Naquadah))
                    .where('U', abilities(PartAbility.MUFFLER))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/high_temperature_smelting_casing"),
                    GTCEu.id("block/multiblock/gcym/blast_alloy_smelter"))
            .register();

    /** GTO {@code large_cracker}: Parallel Hatch + GTCEu's coil-scaled Cracker energy discount. */
    public static final MultiblockMachineDefinition LARGE_CRACKER = REGISTRATE
            .multiblock("large_cracker", CoilWorkableElectricMultiblockMachine::new)
            .rotationState(RotationState.ALL)
            .recipeType(GTRecipeTypes.CRACKING_RECIPES)
            .recipeModifiers(GTRecipeModifiers::hatchParallel, GTRecipeModifiers::crackerOverclock)
            .appearanceBlock(GTBlocks.CASING_STAINLESS_CLEAN)
            .pattern(definition -> GTOCompressedPatternReader.start("large_cracker")
                    .where('~', controller(blocks(definition.get())))
                    .where('a', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()).setMinGlobalLimited(200)
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('b', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('c', heatingCoils())
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_clean_stainless_steel"),
                    GTCEu.id("block/multiblock/cracking_unit"))
            .register();

    /**
     * GTO {@code integrated_assembler}: Assembler (GTO's Laminator mode is not ported) with a Parallel Hatch and Thread
     * Hatch.
     */
    public static final MultiblockMachineDefinition INTEGRATED_ASSEMBLER = REGISTRATE
            .multiblock("integrated_assembler", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.ASSEMBLER_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("integrated_assembler")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('B', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('D', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('E', frames(GTMaterials.HSLASteel))
                    .where('F', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('G', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                    .where('H', blocks(GTNABlocks.SPACETIME_ASSEMBLY_LINE_UNIT.get()))
                    .where('I', frames(GTMaterials.StainlessSteel))
                    .where('J', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('K', blocks(GTBlocks.LAMPS.get(net.minecraft.world.item.DyeColor.WHITE).get()))
                    .where('L', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                    .where('M', blocks(GTNABlocks.PROCESS_MACHINE_CASING.get()))
                    .where('O', blocks(GTBlocks.CASING_ASSEMBLY_LINE.get()))
                    .where('P', blocks(GTBlocks.CLEANROOM_GLASS.get()))
                    .where('Q', blocks(GTNABlocks.MACHINE_CASING_CIRCUIT_ASSEMBLY_LINE.get()))
                    .where('R', blocks(net.minecraft.world.level.block.Blocks.IRON_BARS))
                    .where('S', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('T', blocks(GTBlocks.HERMETIC_CASING_UHV.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/gcym/large_assembler"))
            .register();

    /** GTO {@code neutronium_wire_cutting}: Cutter with Parallel Hatch and Thread Hatch; Amprosium = Neutronium. */
    public static final MultiblockMachineDefinition NEUTRONIUM_WIRE_CUTTING = REGISTRATE
            .multiblock("neutronium_wire_cutting", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.CUTTER_RECIPES)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("neutronium_wire_cutting")
                    .where('A', blocks(GTNABlocks.HIGH_PRESSURE_RESISTANT_CASING.get()))
                    .where('B', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('D', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('E', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('F', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('G', frames(GTNAMaterials.HastelloyN))
                    .where('H', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('I', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('J', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('K', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('L', blocks(GTNABlocks.PRECISION_PROCESSING_MECHANICAL_CASING.get()))
                    .where('M', blocks(GTNABlocks.EXTREME_DENSITY_CASING.get()))
                    .where('N', frames(GTMaterials.Neutronium))
                    .where('O', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('P', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('Q', blocks(GTBlocks.CASING_STAINLESS_TURBINE.get()))
                    .where('R', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('S', controller(blocks(definition.get())))
                    .where('T', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/gcym/large_cutter"))
            .register();

    /**
     * GTO {@code holy_separator}: Centrifuge with Parallel Hatch and Thread Hatch; GTO Mithril frame -> Naquadah Alloy.
     */
    public static final MultiblockMachineDefinition HOLY_SEPARATOR = REGISTRATE
            .multiblock("holy_separator", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.CENTRIFUGE_RECIPES)
            .appearanceBlock(GTNABlocks.MOLECULAR_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("holy_separator")
                    .where('A', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('B', blocks(GTNABlocks.STRENGTHEN_THE_BASE_BLOCK.get()))
                    .where('C', blocks(GTNABlocks.MOLECULAR_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('D', controller(blocks(definition.get())))
                    .where('E', blocks(GTNABlocks.MC_NYLON_TENSILE_MECHANICAL_SHELL.get()))
                    .where('F', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('G', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('H', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('I', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('J', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('K',
                            blocks(GTNABlocks.ZIRCONIA_CERAMIC_HIGH_STRENGTH_BENDING_RESISTANCE_MECHANICAL_BLOCK.get()))
                    .where('L', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('M', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('N', frames(GTMaterials.NaquadahAlloy))
                    .where('O', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('P', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('Q', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/molecular_casing"),
                    GTCEu.id("block/multiblock/gcym/large_cutter"))
            .register();

    /** GTO {@code superconducting_electromagnetism}: Polarizer + Electromagnetic Separator. */
    public static final MultiblockMachineDefinition SUPERCONDUCTING_ELECTROMAGNETISM = REGISTRATE
            .multiblock("superconducting_electromagnetism", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.POLARIZER_RECIPES)
            .recipeType(GTRecipeTypes.ELECTROMAGNETIC_SEPARATOR_RECIPES)
            .appearanceBlock(GTNABlocks.LAFIUM_MECHANICAL_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("superconducting_electromagnetism")
                    .where('A', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('C', blocks(GTNABlocks.IMPROVED_SUPERCONDUCTOR_COIL.get()))
                    .where('D', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('E', blocks(GCYMBlocks.MOLYBDENUM_DISILICIDE_COIL_BLOCK.get()))
                    .where('F', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('G', controller(blocks(definition.get())))
                    .where('H', blocks(GTNABlocks.ACCELERATED_PIPELINE.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/lafium_mechanical_casing"),
                    GTNACORE.id("block/multiblock/general0"))
            .register();

    /** GTO {@code superconducting_magnetic_presser}: Forming Press; Amprosium block = Neutronium block. */
    public static final MultiblockMachineDefinition SUPERCONDUCTING_MAGNETIC_PRESSER = REGISTRATE
            .multiblock("superconducting_magnetic_presser", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.FORMING_PRESS_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("superconducting_magnetic_presser")
                    .where('A', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('B', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('C', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('D', blocks(GTNABlocks.NEUTRONIUM_STABLE_CASING.get()))
                    .where('E', frames(GTMaterials.Naquadria))
                    .where('F', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where('G', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('H', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('I', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('J', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('K', blocks(GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS.get()))
                    .where('L', blocks(GTBlocks.SUPERCONDUCTING_COIL.get()))
                    .where('M', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('N', blocks(com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper
                            .getBlock(com.gregtechceu.gtceu.api.data.tag.TagPrefix.block, GTMaterials.Neutronium)))
                    .where('O', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('P', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('Q', frames(GTMaterials.HastelloyC276))
                    .where('R', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('S', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code magnetic_energy_reaction_furnace}: Arc Furnace with coil parallel. */
    public static final MultiblockMachineDefinition MAGNETIC_ENERGY_REACTION_FURNACE = REGISTRATE
            .multiblock("magnetic_energy_reaction_furnace",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.ARC_FURNACE_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_NONCONDUCTING)
            .pattern(definition -> GTOCompressedPatternReader.start("magnetic_energy_reaction_furnace")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTBlocks.CASING_TUNGSTENSTEEL_TURBINE.get()))
                    .where('B', heatingCoils())
                    .where('C', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('D', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get()))
                    .where('E', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('F', blocks(GTNABlocks.MAGTECH_CASING.get()))
                    .where('G', blocks(GTNABlocks.TRANSCENDENTALLY_AMPLIFIED_MAGNETIC_CONFINEMENT_CASING.get()))
                    .where('H', blocks(com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper
                            .getBlock(com.gregtechceu.gtceu.api.data.tag.TagPrefix.block,
                                    GTMaterials.NeodymiumMagnetic)))
                    .where('I', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get()))
                    .where('J', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('K', blocks(GTBlocks.BATTERY_EMPTY_TIER_III.get()))
                    .where('L', frames(GTMaterials.Neutronium))
                    .where('M', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                    .where('N', blocks(GTNABlocks.RESTRAINT_DEVICE.get()))
                    .where('O', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('a', blocks(GCYMBlocks.CASING_NONCONDUCTING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/nonconducting_casing"),
                    GTNACORE.id("block/multiblock/general1"))
            .register();

    /** GTO {@code particle_stream_matrix_filling_machine}: Canner with coil parallel. */
    public static final MultiblockMachineDefinition PARTICLE_STREAM_MATRIX_FILLING_MACHINE = REGISTRATE
            .multiblock("particle_stream_matrix_filling_machine",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.CANNER_RECIPES)
            .appearanceBlock(GTNABlocks.LAFIUM_MECHANICAL_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("particle_stream_matrix_filling_machine")
                    .where('A', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('B', blocks(GCYMBlocks.CASING_STRESS_PROOF.get()))
                    .where('C', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get()))
                    .where('D', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('E', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('F', blocks(GTNABlocks.STRENGTHEN_THE_BASE_BLOCK.get()))
                    .where('G', frames(GTNAMaterials.Trinaquadalloy))
                    .where('H', frames(GTMaterials.BlackSteel))
                    .where('I', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('J', blocks(GTNABlocks.ELECTRON_PERMEABLE_AMPROSIUM_COATED_GLASS.get()))
                    .where('K', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('L', blocks(GTNABlocks.HIGH_PRESSURE_RESISTANT_CASING.get()))
                    .where('M', heatingCoils())
                    .where('N', blocks(GTNABlocks.MULTI_FUNCTIONAL_CASING.get()))
                    .where('O', blocks(GTNABlocks.SPEEDING_PIPE.get()))
                    .where('P', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/lafium_mechanical_casing"),
                    GTCEu.id("block/multiblock/gcym/large_extractor"))
            .register();

    /** GTO {@code nanites_circuit_assembly_factory}: Circuit Assembler with Parallel Hatch and Thread Hatch. */
    public static final MultiblockMachineDefinition NANITES_CIRCUIT_ASSEMBLY_FACTORY = REGISTRATE
            .multiblock("nanites_circuit_assembly_factory", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.CIRCUIT_ASSEMBLER_RECIPES)
            .appearanceBlock(GTNABlocks.NAQUADAH_ALLOY_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("nanites_circuit_assembly_factory")
                    .where('A', frames(GTNAMaterials.HastelloyN))
                    .where('B', blocks(GTNABlocks.PIKYONIUM_MACHINE_CASING.get()))
                    .where('C', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('D', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('E', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('F', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('G', controller(blocks(definition.get())))
                    .where('H', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('I', frames(GTMaterials.HastelloyX))
                    // GTO Quantanium frame -> Trinium
                    .where('J', frames(GTMaterials.Trinium))
                    .where('K', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('L', blocks(GTNABlocks.MACHINE_CASING_CIRCUIT_ASSEMBLY_LINE.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code mega_wiremill}: Wiremill (GTO's Fiber Extrusion mode is not ported) with coil parallel. */
    public static final MultiblockMachineDefinition MEGA_WIREMILL = REGISTRATE
            .multiblock("mega_wiremill",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.WIREMILL_RECIPES)
            .appearanceBlock(GTBlocks.CASING_INVAR_HEATPROOF)
            .pattern(definition -> GTOCompressedPatternReader.start("mega_wiremill")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.HIGH_STRENGTH_SUPPORT_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get()))
                    .where('C', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('D', frames(GTMaterials.TungstenSteel))
                    .where('E', blocks(GTNABlocks.PIKYONIUM_MACHINE_CASING.get()))
                    .where('F', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                    .where('G', blocks(GTBlocks.CASING_ASSEMBLY_CONTROL.get()))
                    .where('H', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('I', heatingCoils())
                    .where('J', blocks(GTNABlocks.HIGH_STRENGTH_SUPPORT_SPINDLE.get()))
                    .where('K', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('L', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_heatproof"),
                    GTCEu.id("block/multiblock/gcym/large_wiremill"))
            .register();

    /** GTO {@code crystal_builder}: Autoclave (GTO's Crystallization mode is not ported) with coil parallel. */
    public static final MultiblockMachineDefinition CRYSTAL_BUILDER = REGISTRATE
            .multiblock("crystal_builder",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.AUTOCLAVE_RECIPES)
            .appearanceBlock(GTNABlocks.MOLECULAR_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("crystal_builder")
                    .where('A', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('B', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('C', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('D', blocks(GTNABlocks.PIKYONIUM_MACHINE_CASING.get()))
                    .where('E', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('F', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('G', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('H', blocks(GTNABlocks.LASER_CASING.get()))
                    .where('I', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('J', blocks(GTNABlocks.QUANTUM_GLASS.get()))
                    .where('K', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('L', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('M', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('N', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                    .where('O', heatingCoils())
                    .where('P', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('Q', blocks(GTNABlocks.MOLECULAR_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('R', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/molecular_casing"),
                    GTNACORE.id("block/multiblock/general1"))
            .register();

    /** GTO {@code high_energy_laser_lathe}: Lathe with Parallel Hatch and Thread Hatch. */
    public static final MultiblockMachineDefinition HIGH_ENERGY_LASER_LATHE = REGISTRATE
            .multiblock("high_energy_laser_lathe", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.LATHE_RECIPES)
            .appearanceBlock(GTNABlocks.MOLECULAR_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("high_energy_laser_lathe")
                    .where('A', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('B', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('C', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('D', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('E', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('F', blocks(GTNABlocks.LASER_COOLING_CASING.get()))
                    .where('G', blocks(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.get()))
                    .where('H', blocks(GTNABlocks.OPTICAL_RESONANCE_CHAMBER.get()))
                    .where('I', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('J', blocks(GTNABlocks.LASER_CASING.get()))
                    .where('K', blocks(GTNABlocks.ELECTRON_PERMEABLE_AMPROSIUM_COATED_GLASS.get()))
                    .where('L', blocks(GTNABlocks.MOLECULAR_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('M', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('N', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('O', blocks(GTNABlocks.PRECISION_PROCESSING_MECHANICAL_CASING.get()))
                    .where('P', blocks(GTNABlocks.HIGH_ENERGY_LASER_EMITTER.get()))
                    .where('Q', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/molecular_casing"),
                    GTCEu.id("block/multiblock/gcym/large_cutter"))
            .register();

    /**
     * GTO {@code extreme_compressor}: Compressor with Parallel Hatch and Thread Hatch. GTO's Gas Compressor and
     * Thermo Pressing modes are GTO-only recipe types and are not ported; Depleted Uranium Alloy frame ->
     * Tungstensteel.
     */
    public static final MultiblockMachineDefinition EXTREME_COMPRESSOR = REGISTRATE
            .multiblock("extreme_compressor", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.COMPRESSOR_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("extreme_compressor")
                    .where('A', blocks(GCYMBlocks.CASING_STRESS_PROOF.get()))
                    .where('B', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('D', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('E', frames(GTMaterials.IncoloyMA956))
                    .where('F', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                    .where('G', abilities(PartAbility.MUFFLER))
                    .where('H', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('I', frames(GTMaterials.TungstenSteel))
                    .where('J', blocks(GTNABlocks.HIGH_PRESSURE_RESISTANT_CASING.get()))
                    .where('K', blocks(GTNABlocks.IRIDIUM_GEARBOX.get()))
                    .where('L', blocks(GTNABlocks.INCONEL_625_PIPE.get()))
                    .where('M', blocks(GTNABlocks.HIGH_PRESSURE_PIPE_CASING.get()))
                    .where('N', blocks(GTBlocks.HERMETIC_CASING_UV.get()))
                    .where('O', blocks(GTNABlocks.CHEMICAL_CORROSION_RESISTANT_PIPE_CASING.get()))
                    .where('P', blocks(GTNABlocks.HIGH_STRENGTH_SUPPORT_SPINDLE.get()))
                    .where('Q', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('R', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTNACORE.id("block/multiblock/general1"))
            .register();

    /**
     * GTO {@code hyperdimensional_plasma_fusion_core}: the DTPF recipes with Parallel Hatch, Thread Hatch and a coil
     * temperature gate (GTO's {@code DimensionallyTranscendentPlasmaForgeMachine}). GTO's Stellar Forge mode is a
     * GTO-only recipe type and is not ported, nor is its renderer. Amprosium frame -> Neutronium; GTO Dimensional
     * Bridge Casing -> {@link GTNABlocks#PLASMA_FORGE_BRIDGE_CASING} (same GTO texture).
     */
    public static final MultiblockMachineDefinition HYPERDIMENSIONAL_PLASMA_FUSION_CORE = REGISTRATE
            .multiblock("hyperdimensional_plasma_fusion_core",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, false, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.PLASMA_FORGE_RECIPES)
            .appearanceBlock(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("hyperdimensional_plasma_fusion_core")
                    .where('A', blocks(GTNABlocks.STRENGTHEN_THE_BASE_BLOCK.get()))
                    .where('B', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes())))
                    .where('C', frames(GTMaterials.Neutronium))
                    .where('D', blocks(GTNABlocks.SPS_CASING.get()))
                    .where('E', absBlocks())
                    .where('F', blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                    .where('G', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('H', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where('I', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('J', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('K', frames(GTMaterials.Naquadria))
                    .where('L', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('M', blocks(GTNABlocks.PLASMA_FORGE_BRIDGE_CASING.get()))
                    .where('N', blocks(GTNABlocks.ABS_ORANGE_CASING.get()))
                    .where('O', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('P', heatingCoils())
                    .where('Q',
                            blocks(GTNABlocks.COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK.get()))
                    .where('R', blocks(GTNABlocks.RHENIUM_REINFORCED_ENERGY_GLASS.get()))
                    .where('S', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('T', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('U', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/dimensionally_transcendent_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code gemini_containment_system}: Packer with coil parallel. GTCEu's Packer covers packing and unpacking;
     * GTO's separate Unpacker type is GTO-only.
     */
    public static final MultiblockMachineDefinition GEMINI_CONTAINMENT_SYSTEM = REGISTRATE
            .multiblock("gemini_containment_system",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.PACKER_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("gemini_containment_system")
                    .where('A', blocks(GTNABlocks.ABS_GREEN_CASING.get()))
                    .where('B', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('C', blocks(GTNABlocks.ABS_RED_CASING.get()))
                    .where('D', blocks(GTNABlocks.TITANIUM_NITRIDE_CERAMIC_IMPACT_RESISTANT_MECHANICAL_BLOCK.get()))
                    .where('E', blocks(GTNABlocks.ENGINEERING_MECHANICAL_CASING.get()))
                    .where('F', frames(GTMaterials.BlackSteel))
                    .where('G', blocks(GTNABlocks.PEEK_WEAR_RESISTANT_MECHANICAL_HOUSING.get()))
                    .where('H', blocks(GTBlocks.LAMPS.values().stream()
                            .map(com.tterrag.registrate.util.entry.RegistryEntry::get)
                            .toArray(net.minecraft.world.level.block.Block[]::new)))
                    .where('I', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('J', blocks(GTNABlocks.INDUSTRIAL_FRAMELESS_GLASS.get()))
                    .where('K', heatingCoils())
                    .where('L', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                    .where('M', blocks(GTNABlocks.MACHINE_CASING_CIRCUIT_ASSEMBLY_LINE.get()))
                    .where('N', blocks(GTBlocks.CASING_TUNGSTENSTEEL_GEARBOX.get()))
                    .where('O', blocks(GTBlocks.CASING_TITANIUM_GEARBOX.get()))
                    .where('P', blocks(GCYMBlocks.CASING_VIBRATION_SAFE.get()))
                    .where('Q', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('R', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('S', blocks(GTNABlocks.INCONEL_625_GEARBOX.get()))
                    .where('T', blocks(GTNABlocks.LASER_CASING.get()))
                    .where('U', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('V', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code giant_electrochemical_workstation}: Electrolyzer with coil parallel, any rotation. GTO's
     * Electroplating mode is a GTO-only recipe type and its GCYM overclock upgrade is a GTO modifier; neither is
     * ported.
     */
    public static final MultiblockMachineDefinition GIANT_ELECTROCHEMICAL_WORKSTATION = REGISTRATE
            .multiblock("giant_electrochemical_workstation",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.ALL)
            .recipeType(GTRecipeTypes.ELECTROLYZER_RECIPES)
            .appearanceBlock(GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("giant_electrochemical_workstation")
                    .where('A', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('C', blocks(GTNABlocks.CHEMICAL_CORROSION_RESISTANT_PIPE_CASING.get()))
                    .where('D', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                    .where('E', frames(GTNAMaterials.HastelloyN))
                    .where('F', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('G', blocks(GTBlocks.CASING_POLYTETRAFLUOROETHYLENE_PIPE.get()))
                    .where('H', heatingCoils())
                    .where('I', frames(GTMaterials.Polytetrafluoroethylene))
                    .where('J', blocks(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.get()))
                    .where('K', blocks(GTNABlocks.NEUTRONIUM_STABLE_CASING.get()))
                    .where('L', blocks(GTBlocks.HERMETIC_CASING_UHV.get()))
                    .where('M', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('N', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                    .where('O', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/space_elevator_mechanical_casing"),
                    GTCEu.id("block/multiblock/gcym/large_chemical_bath"))
            .register();

    /**
     * GTO {@code desulfurizer}: own recipe type, coil parallel. The main structure takes IO and maintenance; GTO's
     * optional extension (its {@code addSubPattern}) is a {@link GTNASubPatterns} module that unlocks Thread,
     * Overclock,
     * Accelerate, Parallel and Laser hatches plus a Muffler. GTO Inconel-242 frame -> Inconel-792.
     */
    public static final MultiblockMachineDefinition DESULFURIZER = REGISTRATE
            .multiblock("desulfurizer",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.DESULFURIZER_RECIPES)
            .appearanceBlock(GTBlocks.CASING_STAINLESS_CLEAN)
            .pattern(definition -> com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start()
                    .aisle("CCCCCIIIIIII", "CCCCCILILILI", "CCCCCILILILI", "            ", "            ",
                            "            ")
                    .aisle("CCCCCIIIIIII", "CGCCCXXXXXXI", "CCCCCILILILI", "  CCCILILILI", "  CCCIIIIIII",
                            "            ")
                    .aisle("CCCCCIIIIIII", "CGGGGILILILI", "CCCCCILILILI", "  CXXXXXXXXI", "  CCCIIIIIII",
                            "            ")
                    .aisle("CCCCCIIIIIII", "CGCPCXXXXXXI", "CCCCCILILILI", "  DDDILILILI", "  DDDIIIIIII",
                            "  DDD       ")
                    .aisle("CCCCCIIIIIII", "CCCPCILILILI", "CCCPCILILILI", "  DPD       ", "  DPD       ",
                            "  DDD       ")
                    .aisle("  DDD       ", "  D~D       ", "  DDD       ", "  DDD       ", "  DDD       ",
                            "  DDD       ")
                    .where('~', controller(blocks(definition.get())))
                    .where('I', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get()))
                    .where('X', blocks(GTBlocks.CASING_STEEL_PIPE.get()))
                    .where('P', blocks(GTBlocks.CASING_BRONZE_PIPE.get()))
                    .where('G', blocks(GTBlocks.HERMETIC_CASING_MV.get()))
                    .where('D', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()).setMinGlobalLimited(24)
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('L', heatingCoils())
                    .where('C', blocks(GTBlocks.CASING_STEEL_SOLID.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_clean_stainless_steel"),
                    GTCEu.id("block/multiblock/large_chemical_reactor"))
            .register();

    /** GTO {@code dimensional_focus_engraving_array}: own recipe type, coil parallel (GTO renderer not ported). */
    public static final MultiblockMachineDefinition DIMENSIONAL_FOCUS_ENGRAVING_ARRAY = REGISTRATE
            .multiblock("dimensional_focus_engraving_array",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.DIMENSIONAL_FOCUS_ENGRAVING_ARRAY_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING)
            .pattern(definition -> GTOCompressedPatternReader.start("dimensional_focus_engraving_array")
                    .where('I', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where('B', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('C', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('D', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('E', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('F', blocks(GTNABlocks.IMPROVED_SUPERCONDUCTOR_COIL.get()))
                    .where('G', blocks(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.get()))
                    .where('a', blocks(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                            .or(abilities(PartAbility.OPTICAL_DATA_RECEPTION).setMaxGlobalLimited(1)))
                    .where('H', heatingCoils())
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/laser_safe_engraving_casing"),
                    GTCEu.id("block/multiblock/gcym/large_engraver"))
            .register();

    /** GTO {@code star_ultimate_material_forge_factory}: own recipe type, unlimited parallel, any rotation. */
    public static final MultiblockMachineDefinition STAR_ULTIMATE_MATERIAL_FORGE_FACTORY = REGISTRATE
            .multiblock("star_ultimate_material_forge_factory", holder -> new WorkableElectricMultipleRecipesMachine(
                    holder) {

                @Override
                public int getMaxParallel() {
                    return Integer.MAX_VALUE;
                }
            })
            .rotationState(RotationState.ALL)
            .recipeType(GTNARecipeType.ULTIMATE_MATERIAL_FORGE_RECIPES)
            .appearanceBlock(GTNABlocks.MOLECULAR_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("star_ultimate_material_forge_factory")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('I', blocks(GTNABlocks.MOLECULAR_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes())))
                    .where('B', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('C', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('D', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('E', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('F', blocks(GTNABlocks.FORCE_FIELD_GLASS.get()))
                    .where('G', blocks(GTNABlocks.ULTIMATE_STELLAR_CONTAINMENT_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/molecular_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code kerr_newman_homogenizer}: Mixer running several recipes at once (GTO cross-recipe -> Thread Hatch)
     * with Parallel Hatch and lasers. GTO's black-hole effect comes from the closed GTOLib FX library and is not
     * ported (GTO's own ring renderer is switched off).
     */
    public static final MultiblockMachineDefinition KERR_NEWMAN_HOMOGENIZER = REGISTRATE
            .multiblock("kerr_newman_homogenizer", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.MIXER_RECIPES)
            .appearanceBlock(GTNABlocks.DIMENSION_INJECTION_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("kerr_newman_homogenizer")
                    .where('A', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('C', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('D',
                            blocks(GTNABlocks.ZIRCONIA_CERAMIC_HIGH_STRENGTH_BENDING_RESISTANCE_MECHANICAL_BLOCK.get()))
                    .where('E', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('F', frames(GTMaterials.NaquadahAlloy))
                    .where('G', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('H', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('I', blocks(GTNABlocks.OIL_GAS_TRANSPORTATION_PIPE_CASING.get()))
                    .where('J', blocks(GTNABlocks.HIGH_PRESSURE_PIPE_CASING.get()))
                    .where('K', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('L', blocks(GTNABlocks.GRAVITY_STABILIZATION_CASING.get()))
                    .where('M', blocks(GTNABlocks.INDUSTRIAL_FRAMELESS_GLASS.get()))
                    .where('N', blocks(GTNABlocks.SHIELDED_ACCELERATOR.get()))
                    .where('O', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('P', frames(GTNAMaterials.HastelloyN))
                    .where('Q', blocks(GTNABlocks.BIOACTIVE_MECHANICAL_CASING.get()))
                    .where('R', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('S', blocks(GTNABlocks.HIGH_STRENGTH_SUPPORT_SPINDLE.get()))
                    .where('T', blocks(GTNABlocks.ACCELERATOR_ELECTROMAGNETIC_COIL_CONSTRAINT_CASING_UHV.get()))
                    .where('U', blocks(GTNABlocks.EXTREME_DENSITY_CASING.get()))
                    .where('V', blocks(GTNAEyeOfHarmonyContent.SPATIAL_CASING.get()))
                    .where('W', frames(GTMaterials.TungstenCarbide))
                    .where('X', blocks(GTNABlocks.PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING.get()))
                    .where('Y', blocks(GTNABlocks.QUANTUM_GLASS.get()))
                    .where('Z', blocks(GTNABlocks.PLASMA_HEATER_CASING.get()))
                    .where('[', blocks(com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_ATOMIC.get()))
                    .where('\\', blocks(GTNABlocks.RADIATION_ABSORBENT_CASING.get()))
                    .where(']', blocks(GTNABlocks.FUSION_CASING_MK4.get()))
                    .where('^', blocks(GTNABlocks.ADVANCED_FUSION_COIL.get()))
                    .where('_', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('`', frames(GTMaterials.Trinium))
                    .where('a', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('b', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/dimension_injection_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code nyarlathoteps_tentacle}: Assembly Line running several recipes at once with coil parallel (GTO
     * cross-recipe + coil parallel), lasers and an Optical Data Reception Hatch. GTO's Suprachronal Assembly Line
     * and Circuit Assembly Line modes are not ported (GTO-only recipe types). Amprosium frame -> Neutronium,
     * Mithril -> Trinium; GTO's Dimensional Bridge Casing is GTNA's Spatial Casing (the old id migrates to it).
     */
    public static final MultiblockMachineDefinition NYARLATHOTEPS_TENTACLE = REGISTRATE
            .multiblock("nyarlathoteps_tentacle",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.ALL)
            .recipeType(GTRecipeTypes.ASSEMBLY_LINE_RECIPES)
            .appearanceBlock(GTNABlocks.MOLECULAR_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("nyarlathoteps_tentacle")
                    .where('A', blocks(GTNABlocks.MOLECULAR_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.OPTICAL_DATA_RECEPTION).setExactLimit(1)))
                    .where('B', blocks(GTNABlocks.ADVANCED_FUSION_COIL.get()))
                    .where('C', blocks(GTNABlocks.LASER_CASING.get()))
                    .where('D', blocks(GTNABlocks.URUIUM_COIL_BLOCK.get()))
                    .where('E', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('F', frames(GTMaterials.Neutronium))
                    .where('G', blocks(GTNABlocks.SPACETIME_ASSEMBLY_LINE_CASING.get()))
                    .where('H', blocks(GTNABlocks.EXTREME_DENSITY_CASING.get()))
                    .where('I', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('J', blocks(GTNABlocks.LASER_COOLING_CASING.get()))
                    .where('K', blocks(GTNABlocks.QUANTUM_GLASS.get()))
                    .where('L', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('M', blocks(GTNABlocks.SPS_CASING.get()))
                    .where('N', blocks(GTNABlocks.SPACETIME_ASSEMBLY_LINE_UNIT.get()))
                    .where('O', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('P', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('Q', heatingCoils())
                    .where('R', blocks(GTBlocks.FILTER_CASING_STERILE.get()))
                    .where('S', blocks(GTNABlocks.ELECTRON_PERMEABLE_AMPROSIUM_COATED_GLASS.get()))
                    .where('T', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('U', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('V', frames(GTMaterials.Trinium))
                    .where('W',
                            blocks(com.gregtechceu.gtceu.api.data.chemical.ChemicalHelper
                                    .getBlock(com.gregtechceu.gtceu.api.data.tag.TagPrefix.block, GTMaterials.Ruby)))
                    .where('X', blocks(com.gregtechceu.gtceu.common.data.GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('Y', frames(GTMaterials.Trinium))
                    .where('Z', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('[', blocks(GTNAEyeOfHarmonyContent.SPATIAL_CASING.get()))
                    .where('~', blocks(GTNABlocks.RESTRAINT_DEVICE.get()))
                    .where(']', blocks(GTNABlocks.QUARK_PIPE.get()))
                    .where('^', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('_', blocks(GTNABlocks.DEGENERATE_RHENIUM_CONSTRAINED_CASING.get()))
                    .where('`', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where('a', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/molecular_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code giant_sintering_array}: own {@code gtna:sintering_furnace} type; coil temperature gate, parallel
     * {@code 4^glass tier}, lasers and Thread Hatch. Recipe type left empty: GTO's sintering recipes use GTO-only
     * materials and rough blanks.
     */
    public static final MultiblockMachineDefinition GIANT_SINTERING_ARRAY = REGISTRATE
            .multiblock("giant_sintering_array",
                    com.raishxn.gtna.common.machine.multiblock.electric.GiantSinteringArrayMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.SINTERING_FURNACE_RECIPES)
            .appearanceBlock(GTNABlocks.NAQUADAH_ALLOY_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("giant_sintering_array")
                    .where('A', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('B',
                            blocks(GTNABlocks.COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK.get()))
                    .where('C', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('D', blocks(GTNABlocks.PLASMA_HEATER_CASING.get()))
                    .where('E', blocks(GTNABlocks.BLAZE_CASING.get()))
                    .where('F',
                            blocks(com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get()))
                    .where('G', com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers.glass())
                    .where('H', heatingCoils())
                    .where('I', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('J', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('K', blocks(GTNABlocks.IRIDIUM_GEARBOX.get()))
                    .where('L', frames(GTMaterials.NaquadahEnriched))
                    .where('M', controller(blocks(definition.get())))
                    .where('N', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                    .where('O', abilities(PartAbility.MUFFLER))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code integrated_vapor_deposition_system}: CVD + PVD (own types, left empty: GTO's recipes use GTO-only
     * materials), several recipes at once, parallel {@code 4^glass tier}. Babbitt Alloy frame -> Stainless Steel,
     * Laurenium frame -> Duranium.
     */
    public static final MultiblockMachineDefinition INTEGRATED_VAPOR_DEPOSITION_SYSTEM = REGISTRATE
            .multiblock("integrated_vapor_deposition_system",
                    com.raishxn.gtna.common.machine.multiblock.electric.GlassParallelMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.CHEMICAL_VAPOR_DEPOSITION_RECIPES)
            .recipeType(GTNARecipeType.PHYSICAL_VAPOR_DEPOSITION_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("integrated_vapor_deposition_system")
                    .where('A', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('B', frames(GTMaterials.StainlessSteel))
                    .where('C', blocks(GTNABlocks.SPS_CASING.get()))
                    .where('D', com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers.glass())
                    .where('E', frames(GTMaterials.NaquadahAlloy))
                    .where('F', blocks(GTNABlocks.STABILIZED_NAQUADAH_WATER_PLANT_CASING.get()))
                    .where('G', blocks(GTBlocks.CASING_POLYTETRAFLUOROETHYLENE_PIPE.get()))
                    .where('H', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get()))
                    .where('I', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('J', blocks(GTNABlocks.HERMETIC_CASING_UEV.get()))
                    .where('K', blocks(com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_ATOMIC.get()))
                    .where('L', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('M', frames(GTMaterials.Duranium))
                    .where('N', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('O', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('P', controller(blocks(definition.get())))
                    .where('Q', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get()))
                    .where('R', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('S', blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                    .where('T', blocks(GTNABlocks.NEUTRONIUM_STABLE_CASING.get()))
                    .where('U', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('V', frames(GTMaterials.Polytetrafluoroethylene))
                    .where('W', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                    .where('X', blocks(com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_CORROSION_PROOF.get()))
                    .where('Y', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('Z', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('[', blocks(GTNABlocks.QUANTUM_GLASS.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code reaction_furnace}: coil furnace like the Electric Blast Furnace (temperature gate and coil
     * overclock) on its own {@code gtna:reaction_furnace} type, left empty (GTO's recipes use GTO-only materials).
     * The upgrade module (GTO {@code addSubPattern}) unlocks the Parallel and Accelerate hatches. GTO's Machine
     * Access Link is not ported.
     */
    public static final MultiblockMachineDefinition REACTION_FURNACE = REGISTRATE
            .multiblock("reaction_furnace", CoilWorkableElectricMultiblockMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.REACTION_FURNACE_RECIPES)
            .recipeModifiers(GTRecipeModifiers::hatchParallel, GTRecipeModifiers::ebfOverclock)
            .appearanceBlock(GTBlocks.CASING_STEEL_SOLID)
            .pattern(definition -> com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.BACK,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.UP,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.LEFT)
                    .aisle("A   A", "ABBBA", "BBCBB", "BBBBB", " BBB ")
                    .aisle("     ", "BBBBB", "BDCDB", "BDCDB", "BAAAB")
                    .aisle("     ", "~BBBB", "CCCCC", "BCCCB", "BAFAB")
                    .aisle("     ", "BBBBB", "BDCDB", "BDCDB", "BAAAB")
                    .aisle("A   A", "ABBBA", "BBCBB", "BBBBB", " BBB ")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', frames(GTMaterials.Steel))
                    .where('C', heatingCoils())
                    .where('D', blocks(GTBlocks.CASING_STEEL_PIPE.get()))
                    .where('B', blocks(GTBlocks.CASING_STEEL_SOLID.get()).setMinGlobalLimited(20)
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('F', abilities(PartAbility.MUFFLER))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_solid_steel"),
                    GTCEu.id("block/multiblock/electric_blast_furnace"))
            .register();

    /**
     * GTO {@code dyson_sphere_launch_silo}: launches Dyson swarm modules into orbit of the planet it stands on
     * ({@link com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines}). Quantanium frame ->
     * Neutronium, Mithril frame -> Trinium.
     */
    public static final MultiblockMachineDefinition DYSON_SPHERE_LAUNCH_SILO = REGISTRATE
            .multiblock("dyson_sphere_launch_silo",
                    com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.LaunchSilo::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.DYSON_SPHERE_RECIPES)
            .recipeModifiers(
                    com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.LaunchSilo::launchModifier,
                    GTRecipeModifiers.OC_NON_PERFECT)
            .appearanceBlock(GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("dyson_sphere_launch_silo")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('B', blocks(GTNABlocks.SPACE_ELEVATOR_INTERNAL_SUPPORT.get()))
                    .where('C', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('D', blocks(GTNABlocks.SPACE_ELEVATOR_SUPPORT.get()))
                    .where('E', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where('F', blocks(GTNABlocks.DYSON_DEPLOYMENT_MAGNET.get()))
                    .where('G', blocks(GTNABlocks.GRAVITON_FIELD_CONSTRAINT_CASING.get()))
                    .where('H', blocks(GTNAEyeOfHarmonyContent.SPATIAL_CASING.get()))
                    .where('I', blocks(GTNABlocks.SPACE_ELEVATOR_POWER_MODULES.get(4).get()))
                    .where('J', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()))
                    .where('K', blocks(GTNABlocks.DIMENSION_INJECTION_CASING.get()))
                    .where('L', blocks(GTNABlocks.DYSON_DEPLOYMENT_CASING.get()))
                    .where('M', frames(GTMaterials.Neutronium))
                    .where('N', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('O', frames(GTMaterials.Trinium))
                    .where('P', frames(GTMaterials.NaquadahAlloy))
                    .where('Q', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('R', blocks(GTNABlocks.FUSION_CASING_MK5.get()))
                    .where('S', blocks(GTNABlocks.DYSON_CONTROL_CASING.get()))
                    .where('T', blocks(GTNABlocks.DEGENERATE_RHENIUM_CONSTRAINED_CASING.get()))
                    .where('U', blocks(GTNABlocks.ACCELERATED_PIPELINE.get()))
                    .where('V', blocks(GTNABlocks.DYSON_CONTROL_TOROID.get()))
                    .where('W', blocks(GTNABlocks.DYSON_DEPLOYMENT_CORE.get()))
                    .where('X', blocks(GTNABlocks.SPACETIME_ASSEMBLY_LINE_UNIT.get()))
                    .where('Y', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get()))
                    .where('[', blocks(GTNABlocks.HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING.get()))
                    .where('a', blocks(GTNABlocks.DYSON_CONTROL_CASING.get())
                            .or(abilities(PartAbility.COMPUTATION_DATA_RECEPTION).setExactLimit(1))
                            .or(autoAbilities(definition.getRecipeTypes())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/space_elevator_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /**
     * GTO {@code dyson_sphere_receiving_station}: generator fed by the swarm of its planet; laser output, needs
     * computation and liquid helium.
     */
    public static final MultiblockMachineDefinition DYSON_SPHERE_RECEIVING_STATION = REGISTRATE
            .multiblock("dyson_sphere_receiving_station",
                    com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.ReceivingStation::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .generator(true)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("dyson_sphere_receiving_station")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()))
                    .where('B', blocks(GTNABlocks.DYSON_CONTROL_TOROID.get()))
                    .where('C', blocks(GTNABlocks.RADIATION_ABSORBENT_CASING.get()))
                    .where('D', blocks(GTNABlocks.HIGH_STRENGTH_CONCRETE.get()))
                    .where('E', blocks(GTNABlocks.SPACE_ELEVATOR_INTERNAL_SUPPORT.get()))
                    .where('F', frames(GTMaterials.NaquadahAlloy))
                    .where('G', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('H', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('I', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('a', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setExactLimit(1))
                            .or(abilities(PartAbility.COMPUTATION_DATA_RECEPTION).setExactLimit(1))
                            .or(abilities(PartAbility.OUTPUT_LASER).setExactLimit(1)))
                    .where('K', blocks(GTNABlocks.SPACE_ELEVATOR_SUPPORT.get()))
                    .where('L', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('M', blocks(GTNABlocks.DYSON_RECEIVER_CASING.get()))
                    .where('N', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code hand_of_arachne}: Loom with Parallel Hatch and Thread Hatch; GTO Pikyonium casing ported. */
    public static final MultiblockMachineDefinition HAND_OF_ARACHNE = REGISTRATE
            .multiblock("hand_of_arachne", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.LOOM_RECIPES)
            .appearanceBlock(GTNABlocks.PRESSURE_CONTAINMENT_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("hand_of_arachne")
                    .where('A', frames(GTMaterials.Tungsten))
                    .where('B', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('C', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('D', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('E', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get()))
                    .where('F', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                    .where('G', blocks(GTNABlocks.PIKYONIUM_MACHINE_CASING.get()))
                    .where('H', blocks(GTBlocks.CASING_LAMINATED_GLASS.get()))
                    .where('I', blocks(GTBlocks.CASING_GRATE.get()))
                    .where('J', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('K', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/pressure_containment_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code rare_earth_centrifugal}: own recipe type with Parallel Hatch, any rotation. */
    public static final MultiblockMachineDefinition RARE_EARTH_CENTRIFUGAL = REGISTRATE
            .multiblock("rare_earth_centrifugal", WorkableElectricMultipleRecipesMachine::new)
            .rotationState(RotationState.ALL)
            .recipeType(GTNARecipeType.RARE_EARTH_CENTRIFUGAL_RECIPES)
            .appearanceBlock(GTBlocks.CASING_HSSE_STURDY)
            .pattern(definition -> GTOCompressedPatternReader.start("rare_earth_centrifugal")
                    .where('a', controller(blocks(definition.get())))
                    .where('b', blocks(GTBlocks.CASING_HSSE_STURDY.get()).setMinGlobalLimited(80)
                            .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('c', blocks(GTBlocks.CASING_TUNGSTENSTEEL_GEARBOX.get()))
                    .where('d', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_sturdy_hsse"),
                    GTCEu.id("block/multiblock/gcym/large_centrifuge"))
            .register();

    /**
     * GTO {@code heavy_rolling}: coil parallel. The author asked for the GTCEu Bender instead of GTO's Rolling and
     * Cluster types (2026-10-09).
     */
    public static final MultiblockMachineDefinition HEAVY_ROLLING = REGISTRATE
            .multiblock("heavy_rolling",
                    holder -> new CoilWorkableElectricMultipleRecipesMachine(holder, true, new Object[0]))
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.BENDER_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING)
            .pattern(definition -> GTOCompressedPatternReader.start("heavy_rolling")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get()))
                    .where('B', frames(GTMaterials.NaquadahAlloy))
                    .where('C', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('D', blocks(GTNABlocks.AMPROSIUM_GEARBOX.get()))
                    .where('E', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('G', heatingCoils())
                    .where('H', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('I', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('J', blocks(GCYMBlocks.CASING_STRESS_PROOF.get()))
                    .where('K', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('L', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('M', blocks(GTNABlocks.HIGH_STRENGTH_SUPPORT_SPINDLE.get()))
                    .where('N', blocks(GTNABlocks.AMPROSIUM_CASING.get()))
                    .where('O', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where('P', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('Q', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('a', blocks(GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/high_temperature_smelting_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    // ---- G-0246 ----

    /** Any GTCEu or GTNA glass (GTO {@code GTOPredicates.glass()}; GTO's glass-tier parallel is not ported). */
    private static TraceabilityPredicate anyGlass() {
        return blocks(GTBlocks.CASING_TEMPERED_GLASS.get(), GTBlocks.CASING_LAMINATED_GLASS.get(),
                GTBlocks.FUSION_GLASS.get(), GTNABlocks.HSSS_BOROSILICATE_GLASS.get(),
                GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS.get(), GTNABlocks.QUANTUM_GLASS.get(),
                GTNABlocks.INDUSTRIAL_FRAMELESS_GLASS.get(), GTNABlocks.FORCE_FIELD_GLASS.get(),
                GTNABlocks.RHENIUM_REINFORCED_ENERGY_GLASS.get());
    }

    private static TraceabilityPredicate lamps() {
        return blocks(GTBlocks.LAMPS.values().stream().map(com.tterrag.registrate.util.entry.RegistryEntry::get)
                .toArray(net.minecraft.world.level.block.Block[]::new));
    }

    /**
     * GTO {@code lightning_rod}: Arc Generator recipes with Parallel Hatch, Thread Hatch and laser. GTO's glass-tier
     * parallel lives in its sealed library and is not ported; the Parallel Hatch sets the parallel instead.
     */
    public static final MultiblockMachineDefinition LIGHTNING_ROD = REGISTRATE
            .multiblock("lightning_rod",
                    com.raishxn.gtna.common.machine.multiblock.electric.LightningRodMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.ARC_GENERATOR_RECIPES)
            .appearanceBlock(GTBlocks.CASING_PALLADIUM_SUBSTATION)
            .pattern(definition -> GTOCompressedPatternReader.start("lightning_rod")
                    .where('A', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get())
                            .or(threadLaserAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('B', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get()))
                    .where('C', frames(GTMaterials.BlackSteel))
                    .where('D', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('E', blocks(GTNABlocks.LAFIUM_MECHANICAL_CASING.get()))
                    .where('F', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('G', frames(GTMaterials.StainlessSteel))
                    .where('H', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('I', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('J', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('K', anyGlass())
                    .where('L', blocks(GTNABlocks.IMPROVED_SUPERCONDUCTOR_COIL.get()))
                    .where('M', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                    .where('N', blocks(GTBlocks.SUPERCONDUCTING_COIL.get()))
                    .where('O', blocks(
                            GTNABlocks.MAGNESIUM_OXIDE_CERAMIC_HIGH_TEMPERATURE_INSULATION_MECHANICAL_BLOCK.get()))
                    .where('P', blocks(net.minecraft.world.level.block.Blocks.POLISHED_DEEPSLATE_SLAB))
                    .where('Q', lamps())
                    .where('R', controller(blocks(definition.get())))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_palladium_substation"),
                    GTNACORE.id("block/multiblock/general0"))
            .register();

    /** GTO {@code space_probe_surface_reception}; GTO Black Titanium frame -> Tritanium. */
    public static final MultiblockMachineDefinition SPACE_PROBE_SURFACE_RECEPTION = REGISTRATE
            .multiblock("space_probe_surface_reception",
                    com.raishxn.gtna.common.machine.multiblock.electric.SpaceProbeSurfaceReceptionMachine::new)
            .langValue("Space Probe Receiver")
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.SPACE_PROBE_SURFACE_RECEPTION_RECIPES)
            .appearanceBlock(GCYMBlocks.CASING_ATOMIC)
            .pattern(definition -> GTOCompressedPatternReader.start("space_probe_surface_reception")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.DYSON_RECEIVER_CASING.get()))
                    .where('B', blocks(GTNABlocks.NAQUADAH_REINFORCED_PLANT_CASING.get()))
                    .where('C', blocks(GTNABlocks.HIGH_PRESSURE_RESISTANT_CASING.get()))
                    .where('D', frames(GTMaterials.Neutronium))
                    .where('E', blocks(GCYMBlocks.CASING_ATOMIC.get()))
                    .where('F', blocks(GTNABlocks.HYPER_MECHANICAL_CASING.get()))
                    .where('G', blocks(GTNABlocks.NEUTRONIUM_STABLE_CASING.get()))
                    .where('H', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('I', blocks(GCYMBlocks.HEAT_VENT.get()))
                    .where('J', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('K', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('L', frames(GTMaterials.Tritanium))
                    .where('M', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                    .where('b', blocks(GCYMBlocks.CASING_ATOMIC.get())
                            .or(autoAbilities(definition.getRecipeTypes()))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                            .or(abilities(PartAbility.COMPUTATION_DATA_RECEPTION).setExactLimit(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/gcym/atomic_casing"),
                    GTCEu.id("block/multiblock/data_bank"))
            .register();

    /** GTO {@code autoLaserAbilities} + Parallel Hatch + maintenance (PCB Factory, no Thread Hatch). */
    private static TraceabilityPredicate laserParallelAbilities(GTRecipeType... types) {
        return autoAbilities(types, false, false, true, true, true, true)
                .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                .or(abilities(PartAbility.INPUT_LASER).setMaxGlobalLimited(2))
                .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1));
    }

    private static final java.util.Map<String, com.gregtechceu.gtceu.api.pattern.BlockPattern> GTO_PATTERNS = new java.util.concurrent.ConcurrentHashMap<>();

    /** GTO {@code PCBFactoryMachine.getBlockPattern}: the tier 1, 2 or 3 structure. */
    public static com.gregtechceu.gtceu.api.pattern.BlockPattern pcbFactoryPattern(int tier,
                                                                                   MultiblockMachineDefinition definition) {
        return GTO_PATTERNS.computeIfAbsent("pcb" + tier, k -> {
            var types = definition.getRecipeTypes();
            var b = com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start().where(' ', any());
            return switch (tier) {
                case 2 -> GTNAGTOPatterns.aisles(b, GTNAGTOPatterns.PCB_FACTORY_T2)
                        .where('A', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                        .where('B', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                        .where('C', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                        .where('D', frames(GTMaterials.Neutronium))
                        .where('E', blocks(GTNABlocks.BORON_CARBIDE_CERAMIC_RADIATION_RESISTANT_MECHANICAL_CUBE.get()))
                        .where('F', frames(GTMaterials.MaragingSteel300))
                        .where('G', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                        .where('H',
                                blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                        .where('I', blocks(GTNABlocks.GRAVITY_STABILIZATION_CASING.get()))
                        .where('J', blocks(GTNABlocks.RADIATION_ABSORBENT_CASING.get()))
                        .where('K', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                        .where('L', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                        .where('M', blocks(GTNABlocks.IRIDIUM_CASING.get()).or(laserParallelAbilities(types)))
                        .where('N', blocks(GTBlocks.SUPERCONDUCTING_COIL.get()))
                        .where('O', blocks(GTNABlocks.MAGTECH_CASING.get()))
                        .where('P', frames(GTMaterials.Europium))
                        .where('Q', blocks(GTNABlocks.PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING.get()))
                        .where('R', blocks(GTNABlocks.HOLLOW_CASING.get()))
                        .where('S', blocks(GTBlocks.HERMETIC_CASING_ZPM.get()))
                        .where('T', controller(blocks(definition.get())))
                        .build();
                case 3 -> GTNAGTOPatterns.aisles(b, GTNAGTOPatterns.PCB_FACTORY_T3)
                        .where('A', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                        .where('B', blocks(GTNABlocks.PLASMA_HEATER_CASING.get()))
                        .where('C', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                        .where('D', blocks(GTNABlocks.BORON_CARBIDE_CERAMIC_RADIATION_RESISTANT_MECHANICAL_CUBE.get()))
                        .where('E', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                        .where('F', blocks(GTNABlocks.MAGTECH_CASING.get()))
                        .where('G',
                                blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                        .where('H', frames(GTMaterials.Neutronium))
                        .where('I', blocks(GTNABlocks.MOLECULAR_COIL.get()))
                        .where('J', blocks(GTNABlocks.AMPROSIUM_ACTIVE_CASING.get()))
                        .where('K', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                        .where('L', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                        .where('M', blocks(GTNABlocks.GRAVITY_STABILIZATION_CASING.get()))
                        .where('N', blocks(GTNABlocks.HOLLOW_CASING.get()))
                        .where('O', blocks(GTNABlocks.RADIATION_ABSORBENT_CASING.get()))
                        .where('P', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                        .where('Q', frames(GTMaterials.MaragingSteel300))
                        .where('R', blocks(GTNABlocks.HIGH_ENERGY_ULTRAVIOLET_EMITTER_CASING.get()))
                        .where('S', blocks(GTNABlocks.ADVANCED_ASSEMBLY_LINE_UNIT.get()))
                        .where('T', blocks(GTNABlocks.IRIDIUM_CASING.get()).or(laserParallelAbilities(types)))
                        .where('U', blocks(GTBlocks.SUPERCONDUCTING_COIL.get()))
                        .where('V', frames(GTMaterials.Europium))
                        .where('W', blocks(GTNABlocks.PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING.get()))
                        .where('X', blocks(GTBlocks.HERMETIC_CASING_ZPM.get()))
                        .where('Y', controller(blocks(definition.get())))
                        .build();
                default -> GTNAGTOPatterns.aisles(b, GTNAGTOPatterns.PCB_FACTORY_T1)
                        .where('A', blocks(GTNABlocks.BORON_CARBIDE_CERAMIC_RADIATION_RESISTANT_MECHANICAL_CUBE.get()))
                        .where('B', frames(GTMaterials.MaragingSteel300))
                        .where('C', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                        .where('D', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                        .where('E', blocks(GTNABlocks.IRIDIUM_CASING.get()).or(laserParallelAbilities(types)))
                        .where('F', blocks(GTNABlocks.MAGTECH_CASING.get()))
                        .where('G',
                                blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                        .where('H', frames(GTMaterials.Europium))
                        .where('I', blocks(GTNABlocks.PPS_CORROSION_RESISTANT_MECHANICAL_HOUSING.get()))
                        .where('J', blocks(GTBlocks.HERMETIC_CASING_ZPM.get()))
                        .where('K', controller(blocks(definition.get())))
                        .build();
            };
        });
    }

    /** GTO {@code pcb_factory}: tier 1-3 structures (screwdriver), EU/t cap per tier, Parallel Hatch, laser. */
    public static final MultiblockMachineDefinition PCB_FACTORY = REGISTRATE
            .multiblock("pcb_factory", com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.PCB_FACTORY_RECIPES)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> pcbFactoryPattern(1, definition))
            .shapeInfos(definition -> {
                var shapes = new java.util.ArrayList<com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo>();
                for (int tier = 1; tier <= 3; tier++) {
                    var pattern = pcbFactoryPattern(tier, definition);
                    int[] repetitions = new int[pattern.aisleRepetitions.length];
                    for (int i = 0; i < repetitions.length; i++) repetitions[i] = pattern.aisleRepetitions[i][0];
                    shapes.add(new com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo(
                            pattern.getPreview(repetitions)));
                }
                return shapes;
            })
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/gcym/large_maceration_tower"))
            .register();

    /** GTO {@code CompoundExtremeCoolingMachine.getBlockPattern}: vacuum/atomization or plasma structure. */
    public static com.gregtechceu.gtceu.api.pattern.BlockPattern compoundExtremeCoolingPattern(boolean plasma,
                                                                                               MultiblockMachineDefinition definition) {
        return GTO_PATTERNS.computeIfAbsent(plasma ? "cecu_plasma" : "cecu", k -> {
            var types = definition.getRecipeTypes();
            var b = com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.RIGHT,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.UP,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.BACK).where(' ', any());
            TraceabilityPredicate io = blocks(GTBlocks.CASING_ALUMINIUM_FROSTPROOF.get())
                    .or(threadLaserAbilities(types))
                    .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1));
            if (plasma) {
                return GTNAGTOPatterns.aisles(b, GTNAGTOPatterns.COMPOUND_EXTREME_COOLING_PLASMA)
                        .where('A', frames(GTMaterials.WatertightSteel))
                        .where('B', blocks(GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.get()))
                        .where('C', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                        .where('D', blocks(GTNABlocks.LASER_CASING.get()))
                        .where('E', blocks(GTBlocks.SUPERCONDUCTING_COIL.get()))
                        .where('F', blocks(GTNABlocks.OPTICAL_RESONANCE_CHAMBER.get()))
                        .where('G', blocks(GTNABlocks.LASER_COOLING_CASING.get()))
                        .where('H', frames(GTMaterials.Neutronium))
                        .where('I', blocks(GTBlocks.BATTERY_ULTIMATE_UHV.get()))
                        .where('J', blocks(GTBlocks.FUSION_GLASS.get()))
                        .where('K', blocks(GTBlocks.CASING_ALUMINIUM_FROSTPROOF.get()))
                        .where('L', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                        .where('M', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                        .where('N', blocks(GTNABlocks.HOLLOW_CASING.get()))
                        .where('O', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                        .where('P', blocks(GTBlocks.FILTER_CASING.get()))
                        .where('Q', io)
                        .where('R', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                        .where('S', controller(blocks(definition.get())))
                        .build();
            }
            return GTNAGTOPatterns.aisles(b, GTNAGTOPatterns.COMPOUND_EXTREME_COOLING_VACUUM)
                    .where('A', blocks(GTBlocks.CASING_ALUMINIUM_FROSTPROOF.get()))
                    .where('B', frames(GTMaterials.WatertightSteel))
                    .where('C', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('D', blocks(GTNABlocks.LASER_COOLING_CASING.get()))
                    .where('E', blocks(GTNABlocks.LASER_CASING.get()))
                    .where('F', blocks(GTBlocks.CASING_TUNGSTENSTEEL_PIPE.get()))
                    .where('G', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('H', blocks(GTNABlocks.HOLLOW_CASING.get()))
                    .where('I', frames(GTMaterials.Neutronium))
                    .where('J', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('K', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('L', io)
                    .where('M', blocks(GTBlocks.CASING_TEMPERED_GLASS.get()))
                    .where('N', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('O', controller(blocks(definition.get())))
                    .build();
        });
    }

    /**
     * GTO {@code compound_extreme_cooling_unit}: Vacuum Freezer + Atomization Condensation; Plasma Condenser needs the
     * larger plasma structure. Parallel Hatch, Thread Hatch, laser, any rotation.
     */
    public static final MultiblockMachineDefinition COMPOUND_EXTREME_COOLING_UNIT = REGISTRATE
            .multiblock("compound_extreme_cooling_unit",
                    com.raishxn.gtna.common.machine.multiblock.electric.CompoundExtremeCoolingMachine::new)
            .rotationState(RotationState.ALL)
            .recipeType(GTRecipeTypes.VACUUM_RECIPES)
            .recipeType(GTNARecipeType.ATOMIZATION_CONDENSATION_RECIPES)
            .recipeType(GTNARecipeType.PLASMA_CONDENSER_RECIPES)
            .appearanceBlock(GTBlocks.CASING_ALUMINIUM_FROSTPROOF)
            .pattern(definition -> compoundExtremeCoolingPattern(false, definition))
            .shapeInfos(definition -> {
                var shapes = new java.util.ArrayList<com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo>();
                for (boolean plasma : new boolean[] { false, true }) {
                    var pattern = compoundExtremeCoolingPattern(plasma, definition);
                    int[] repetitions = new int[pattern.aisleRepetitions.length];
                    for (int i = 0; i < repetitions.length; i++) repetitions[i] = pattern.aisleRepetitions[i][0];
                    shapes.add(new com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo(
                            pattern.getPreview(repetitions)));
                }
                return shapes;
            })
            .workableCasingModel(GTCEu.id("block/casings/solid/machine_casing_frost_proof"),
                    GTCEu.id("block/multiblock/vacuum_freezer"))
            .register();

    // ---- G-0247 ----

    /** GTO generator hatches: fluid in, maintenance, one dynamo or laser source (no GTO Control Hatch). */
    private static TraceabilityPredicate reactorAbilities(int fluidInputs) {
        return abilities(PartAbility.IMPORT_FLUIDS).setMaxGlobalLimited(fluidInputs).setPreviewCount(fluidInputs)
                .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1))
                .or(abilities(PartAbility.OUTPUT_ENERGY).setMaxGlobalLimited(1))
                .or(abilities(PartAbility.OUTPUT_LASER).setMaxGlobalLimited(1));
    }

    /** GTO {@code hyper_reactor}: generator; booster plasma gives parallel (see HyperReactorMachine). */
    public static final MultiblockMachineDefinition HYPER_REACTOR = REGISTRATE
            .multiblock("hyper_reactor", com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine::new)
            .rotationState(RotationState.ALL)
            .recipeType(GTNARecipeType.HYPER_REACTOR_RECIPES)
            .generator(true)
            .recipeModifiers(com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine::recipeModifier)
            .appearanceBlock(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING)
            .pattern(definition -> GTNAGTOPatterns.aisles(com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.RIGHT,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.UP,
                    com.gregtechceu.gtceu.api.pattern.util.RelativeDirection.BACK), GTNAGTOPatterns.HYPER_REACTOR)
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.MOLECULAR_CASING.get()))
                    .where('B', blocks(GTNABlocks.PIKYONIUM_MACHINE_CASING.get()))
                    .where('C', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()))
                    .where('D', frames(GTMaterials.Neutronium))
                    .where('E', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('F', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('G', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where('H', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('I', blocks(GTNABlocks.AMPROSIUM_PIPE_CASING.get()))
                    .where('a', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()).or(reactorAbilities(2)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/enhance_hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    /** GTO {@code advanced_hyper_reactor}; Dimensional Bridge Casing = {@code plasma_forge_bridge_casing}. */
    public static final MultiblockMachineDefinition ADVANCED_HYPER_REACTOR = REGISTRATE
            .multiblock("advanced_hyper_reactor",
                    com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.ADVANCED_HYPER_REACTOR_RECIPES)
            .generator(true)
            .recipeModifiers(com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine::recipeModifier)
            .appearanceBlock(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("advanced_hyper_reactor")
                    .where('~', controller(blocks(definition.get())))
                    .where('A', blocks(GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get()))
                    .where('B', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()))
                    .where('C', frames(GTMaterials.Naquadria))
                    .where('D', blocks(GTNABlocks.ECHO_CASING.get()))
                    .where('E', blocks(GTNABlocks.DEGENERATE_RHENIUM_CONSTRAINED_CASING.get()))
                    .where('F', blocks(GTNABlocks.PLASMA_FORGE_BRIDGE_CASING.get()))
                    .where('G', blocks(GTNABlocks.CONTAINMENT_FIELD_GENERATOR.get()))
                    .where('H', blocks(GTNABlocks.HYPER_CORE.get()))
                    .where('a', blocks(GTNABlocks.ENHANCE_HYPER_MECHANICAL_CASING.get()).or(reactorAbilities(1)))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/enhance_hyper_mechanical_casing"),
                    GTCEu.id("block/multiblock/fusion_reactor"))
            .register();

    // ---- G-0248 ----

    /** GTO {@code fuel_cell_generator}: absorption / transfer / release modes (FuelCellGeneratorMachine). */
    public static final MultiblockMachineDefinition FUEL_CELL_GENERATOR = REGISTRATE
            .multiblock("fuel_cell_generator",
                    com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.FUEL_CELL_ENERGY_ABSORPTION_RECIPES)
            .recipeType(GTNARecipeType.FUEL_CELL_ENERGY_TRANSFER_RECIPES)
            .recipeType(GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES)
            .recipeModifiers(
                    com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine::recipeModifier)
            .appearanceBlock(GTNABlocks.IRIDIUM_CASING)
            .pattern(definition -> GTOCompressedPatternReader.start("fuel_cell_generator")
                    .where('A', blocks(GTNABlocks.IRIDIUM_CASING.get())
                            .or(abilities(PartAbility.OUTPUT_ENERGY).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setPreviewCount(1))
                            .or(abilities(PartAbility.OUTPUT_LASER).setPreviewCount(0))
                            .or(abilities(PartAbility.IMPORT_ITEMS).setPreviewCount(1))
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setPreviewCount(4))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_FLUIDS).setPreviewCount(2)))
                    .where('B', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('C', controller(blocks(definition.get())))
                    .where('D', blocks(GTNABlocks.FLOCCULATION_CASING.get()))
                    .where('E', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('F', blocks(GCYMBlocks.MOLYBDENUM_DISILICIDE_COIL_BLOCK.get()))
                    .where('G', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('H', frames(GTMaterials.HSSG))
                    .where('I', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                    .where('J', blocks(GTNABlocks.CALCIUM_OXIDE_CERAMIC_ANTI_METAL_CORROSION_MECHANICAL_BLOCK.get()))
                    .where('K', blocks(GTBlocks.FILTER_CASING.get()))
                    .where('L', blocks(GTBlocks.CASING_PALLADIUM_SUBSTATION.get()))
                    .where('M', blocks(GTNABlocks.CHEMICAL_CORROSION_RESISTANT_PIPE_CASING.get()))
                    .where('N',
                            blocks(GTNABlocks.COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK.get()))
                    .where('O', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('P', blocks(GTBlocks.CASING_PTFE_INERT.get()))
                    .where('Q', blocks(GTBlocks.BATTERY_EMPTY_TIER_II.get()))
                    .where('R', blocks(GTBlocks.FUSION_GLASS.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTNACORE.id("block/casings/iridium_casing"),
                    GTCEu.id("block/multiblock/processing_array"))
            .register();

    // ---- G-0249: Supercomputing Center ----

    /** GTO tier glasses at or above {@code minTier} (GTO GLASSMAP: IV, LuV, ZPM, UHV, UIV here). */
    private static TraceabilityPredicate tierGlass(int minTier) {
        var glasses = new java.util.ArrayList<net.minecraft.world.level.block.Block>();
        if (minTier <= GTValues.IV) glasses.add(GTNABlocks.TUNGSTEN_BOROSILICATE_GLASS.get());
        if (minTier <= GTValues.LuV) glasses.add(GTNABlocks.HSSS_BOROSILICATE_GLASS.get());
        if (minTier <= GTValues.ZPM) glasses.add(GTNABlocks.NAQUADAH_BOROSILICATE_GLASS.get());
        if (minTier <= GTValues.UHV) glasses.add(GTNABlocks.AMPROSIUM_BOROSILICATE_GLASS.get());
        glasses.add(GTNABlocks.TARANIUM_BOROSILICATE_GLASS.get());
        return blocks(glasses.toArray(net.minecraft.world.level.block.Block[]::new));
    }

    /**
     * GTO {@code supercomputing_center}: one pattern per tier, with that tier's computer casing ('U'), heat vent ('S')
     * and minimum glass ('V': IV, UHV, UIV). GTO Babbitt Alloy frame -> Stainless Steel.
     */
    public static com.gregtechceu.gtceu.api.pattern.BlockPattern supercomputingPattern(int tier,
                                                                                       MultiblockMachineDefinition definition) {
        return GTO_PATTERNS.computeIfAbsent("supercomputing" + tier, k -> {
            var casing = switch (tier) {
                case 2 -> GTNABlocks.BIOCOMPUTER_CASING.get();
                case 3 -> GTNABlocks.GRAVITON_COMPUTER_CASING.get();
                default -> GTBlocks.COMPUTER_CASING.get();
            };
            var heat = switch (tier) {
                case 2 -> GTNABlocks.PHASE_CHANGE_BIOCOMPUTER_COOLING_VENTS.get();
                case 3 -> GTNABlocks.ANTI_ENTROPY_COMPUTER_CONDENSATION_MATRIX.get();
                default -> GTBlocks.COMPUTER_HEAT_VENT.get();
            };
            int glassTier = tier == 3 ? GTValues.UIV : tier == 2 ? GTValues.UHV : GTValues.IV;
            return GTNAGTOPatterns.aisles(com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(),
                    GTNAGTOPatterns.SUPERCOMPUTING_CENTER)
                    .where('A', blocks(GTNABlocks.NAQUADAH_ALLOY_CASING.get()))
                    .where('B', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('C', frames(GTMaterials.StainlessSteel))
                    .where('D', blocks(GTNABlocks.STRONTIUM_CARBONATE_CERAMIC_RAY_ABSORBING_MECHANICAL_CUBE.get()))
                    .where('E', blocks(GTBlocks.MACHINE_CASING_UHV.get()))
                    .where('F', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                    .where('G', blocks(GTNABlocks.ANTIFREEZE_HEATPROOF_MACHINE_CASING.get()))
                    .where('H', frames(GTNAMaterials.HastelloyN))
                    .where('I', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get()))
                    .where('J', blocks(GTNABlocks.PRESSURE_CONTAINMENT_CASING.get()))
                    .where('K', absBlocks())
                    .where('L', frames(GTMaterials.Ruridit))
                    .where('M', blocks(
                            GTNABlocks.LITHIUM_OXIDE_CERAMIC_HEAT_RESISTANT_SHOCK_RESISTANT_MECHANICAL_CUBE.get()))
                    .where('N', blocks(GTBlocks.ADVANCED_COMPUTER_CASING.get()))
                    .where('O', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('P',
                            blocks(GTNABlocks.COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK.get()))
                    .where('Q', blocks(GTNABlocks.MC_NYLON_TENSILE_MECHANICAL_SHELL.get()))
                    .where('R', blocks(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING.get())
                            .or(blocks(GTNAResearchMachines.THERMAL_CONDUCTOR_HATCH.getBlock()).setMaxGlobalLimited(1))
                            .or(abilities(PartAbility.IMPORT_ITEMS).setPreviewCount(1))
                            .or(abilities(PartAbility.IMPORT_FLUIDS).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setPreviewCount(0))
                            .or(abilities(PartAbility.EXPORT_FLUIDS).setPreviewCount(1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                            .or(abilities(PartAbility.COMPUTATION_DATA_TRANSMISSION).setMaxGlobalLimited(1))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('S', blocks(heat))
                    .where('T', abilities(PartAbility.HPCA_COMPONENT))
                    .where('U', blocks(casing))
                    .where('V', tierGlass(glassTier))
                    .where('W', controller(blocks(definition.get())))
                    .where('X', blocks(net.minecraft.world.level.block.Blocks.ANDESITE_WALL))
                    .where('Y', blocks(net.minecraft.world.level.block.Blocks.IRON_BARS))
                    .where(' ', any())
                    .build();
        });
    }

    /** GTO {@code supercomputing_center}: tiered HPCA (SupercomputingCenterMachine). */
    public static final MultiblockMachineDefinition SUPERCOMPUTING_CENTER = REGISTRATE
            .multiblock("supercomputing_center",
                    com.raishxn.gtna.common.machine.multiblock.electric.SupercomputingCenterMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTNABlocks.OXIDATION_RESISTANT_HASTELLOY_N_MECHANICAL_CASING)
            .pattern(definition -> supercomputingPattern(1, definition))
            .shapeInfos(definition -> {
                var shapes = new java.util.ArrayList<com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo>();
                for (int tier = 1; tier <= 3; tier++) {
                    var pattern = supercomputingPattern(tier, definition);
                    int[] repetitions = new int[pattern.aisleRepetitions.length];
                    for (int i = 0; i < repetitions.length; i++) repetitions[i] = pattern.aisleRepetitions[i][0];
                    shapes.add(new com.gregtechceu.gtceu.api.pattern.MultiblockShapeInfo(
                            pattern.getPreview(repetitions)));
                }
                return shapes;
            })
            .workableCasingModel(GTNACORE.id("block/casings/oxidation_resistant_hastelloy_n_mechanical_casing"),
                    GTCEu.id("block/multiblock/large_miner"))
            .register();

    // ---- G-0250: Data Center ----

    /**
     * GTO {@code data_center}: GTCEu's Data Bank on a larger structure (cooled by NICH Cooling Components). GTO's extra
     * data access hatches (Bio / Black Hole / Virtual Universe) only hold GTO data media and are not ported.
     */
    public static final MultiblockMachineDefinition DATA_CENTER = REGISTRATE
            .multiblock("data_center",
                    com.gregtechceu.gtceu.common.machine.multiblock.electric.research.DataBankMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTRecipeTypes.DUMMY_RECIPES)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTNAGTOPatterns.aisles(com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(),
                    GTNAGTOPatterns.DATA_CENTER)
                    .where('A', blocks(GTBlocks.COMPUTER_CASING.get()))
                    .where('B', controller(blocks(definition.get())))
                    .where('C', abilities(PartAbility.DATA_ACCESS)
                            .or(blocks(GTBlocks.HIGH_POWER_CASING.get()))
                            .or(abilities(PartAbility.OPTICAL_DATA_TRANSMISSION))
                            .or(abilities(PartAbility.OPTICAL_DATA_RECEPTION)))
                    .where('D', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(abilities(PartAbility.OPTICAL_DATA_TRANSMISSION).setMaxGlobalLimited(16, 1))
                            .or(abilities(PartAbility.OPTICAL_DATA_RECEPTION).setMaxGlobalLimited(4, 1))
                            .or(abilities(PartAbility.INPUT_ENERGY).setMinGlobalLimited(1).setMaxGlobalLimited(8, 2))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('E', blocks(GTBlocks.ADVANCED_COMPUTER_CASING.get()))
                    .where('F',
                            blocks(GTNABlocks.COBALT_OXIDE_CERAMIC_STRONG_THERMALLY_CONDUCTIVE_MECHANICAL_BLOCK.get()))
                    .where('G', blocks(GTNABlocks.ELECTRON_PERMEABLE_AMPROSIUM_COATED_GLASS.get()))
                    .where('H', blocks(GTNAResearchMachines.NICH_COOLING_COMPONENTS.getBlock()))
                    .where('I', blocks(GTNABlocks.CHEMICAL_CORROSION_RESISTANT_PIPE_CASING.get()))
                    .where('J', blocks(GTNABlocks.IRIDIUM_CASING.get()))
                    .where('K', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('L', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('M', frames(GTMaterials.Naquadria))
                    .where('N', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/research_station"))
            .register();

    /** GTO {@code analysis_and_research_center}: Data Analysis / Data Integration with computation. */
    public static final MultiblockMachineDefinition ANALYSIS_AND_RESEARCH_CENTER = REGISTRATE
            .multiblock("analysis_and_research_center",
                    com.raishxn.gtna.common.machine.multiblock.electric.AnalysisAndResearchCenterMachine::new)
            .rotationState(RotationState.NON_Y_AXIS)
            .recipeType(GTNARecipeType.DATA_ANALYSIS_RECIPES)
            .recipeType(GTNARecipeType.DATA_INTEGRATION_RECIPES)
            .recipeModifiers(
                    com.raishxn.gtna.common.machine.multiblock.electric.AnalysisAndResearchCenterMachine::recipeModifier)
            .appearanceBlock(GTBlocks.HIGH_POWER_CASING)
            .pattern(definition -> GTNAGTOPatterns.aisles(com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start(),
                    GTNAGTOPatterns.ANALYSIS_AND_RESEARCH_CENTER)
                    .where('A', blocks(GTBlocks.COMPUTER_CASING.get()))
                    .where('B', blocks(GTBlocks.COMPUTER_HEAT_VENT.get()))
                    .where('C', blocks(GTBlocks.ADVANCED_COMPUTER_CASING.get()))
                    .where('D', blocks(GTBlocks.HIGH_POWER_CASING.get()))
                    .where('E', blocks(GTBlocks.HIGH_POWER_CASING.get())
                            .or(abilities(PartAbility.INPUT_ENERGY).setMaxGlobalLimited(2).setPreviewCount(1))
                            .or(abilities(PartAbility.EXPORT_ITEMS).setExactLimit(1))
                            .or(abilities(PartAbility.COMPUTATION_DATA_RECEPTION).setExactLimit(1))
                            .or(abilities(PartAbility.MAINTENANCE).setExactLimit(1)))
                    .where('F', blocks(GCYMBlocks.ELECTROLYTIC_CELL.get()))
                    .where('G', controller(blocks(definition.get())))
                    // GTO Analyze / Research Holder -> one input bus.
                    .where('H', abilities(PartAbility.IMPORT_ITEMS).setExactLimit(1))
                    .where(' ', any())
                    .build())
            .workableCasingModel(GTCEu.id("block/casings/hpca/high_power_casing"),
                    GTCEu.id("block/multiblock/research_station"))
            .register();

    /** GTO's Desulfurizer extension (GTO {@code addSubPattern}); called from {@link #init()}. */
    /** GTO {@code reaction_furnace} sub-pattern: the module that unlocks the Parallel and Accelerate hatches. */
    private static void registerReactionFurnaceModule() {
        com.raishxn.gtna.api.machine.multiblock.GTNASubPatterns.register(REACTION_FURNACE.getId(),
                definition -> com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start()
                        .aisle("EEEEE AAA ", "       A  ", "          ", "          ", "          ")
                        .aisle("EFFFEDBBBA", "      BBB ", "      BBB ", "      BBB ", "       B  ")
                        .aisle("EFFFEDBBBA", "     DBCBA", "      BCB ", "      BCB ", "     CCCB ")
                        .aisle("EFFFEDBBBA", "      BBB ", "      BBB ", "      BBB ", "       B  ")
                        .aisle("EEEEE AAA ", "  G    A  ", "          ", "          ", "          ")
                        .where('A', blocks(GTBlocks.CASING_STEEL_SOLID.get())
                                .or(autoAbilities(definition.getRecipeTypes()))
                                .or(abilities(PartAbility.PARALLEL_HATCH).setMaxGlobalLimited(1))
                                .or(abilities(GTNAPartAbility.ACCELERATE_HATCH).setMaxGlobalLimited(1)))
                        .where('B', blocks(GTBlocks.CASING_PTFE_INERT.get()))
                        .where('C', blocks(GTBlocks.CASING_POLYTETRAFLUOROETHYLENE_PIPE.get()))
                        .where('D', blocks(GTBlocks.CASING_STEEL_SOLID.get()))
                        .where('E', frames(GTMaterials.Steel))
                        .where('F', blocks(GTBlocks.STEEL_HULL.get()))
                        .where('G', controller(blocks(definition.get())))
                        .where(' ', any())
                        .build(),
                net.minecraft.network.chat.Component.translatable("gtna.machine.reaction_furnace.module"));
    }

    private static void registerDesulfurizerModule() {
        com.raishxn.gtna.api.machine.multiblock.GTNASubPatterns.register(DESULFURIZER.getId(),
                definition -> com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern.start()
                        .aisle("  LLLLLEGGG       ", "  L   EEGGG       ", "  L   EEGGG       ", "        GGG       ",
                                "        GGG       ", "        GGG       ")
                        .aisle("NNNNN EEFFFAAAAAAA", "ORORO EHFFFACACACA", "ORLRO EEFDFACACACA", "ORORO   GDF       ",
                                "OOOOO   GDF       ", "        GGG       ")
                        .aisle("NNNNN EEFFFAAAAAAA", "OOOOO EHFFFDDDDDDA", "PRSRP EEFFFACACACA", "OOSOO   GFFACACACA",
                                "OSSSO   GFFAAAAAAA", "        GGG       ")
                        .aisle("NNNNN EEEEEAAAAAAA", "OOOOO EHHHHACACACA", "PRSRP EEEEEACACACA", "OSSSO  BEDDDDDDDDA",
                                "OSSSO  BEEEAAAAAAA", "        BBB       ")
                        .aisle("NNNNN EEEEEAAAAAAA", "OOOOO EHHHHDDDDDDA", "PRSRP EEEEEACACACA", "OOSOO  BEEEACACACA",
                                "OSSSO   EEEAAAAAAA", "                  ")
                        .aisle("NNNNN EEEEEAAAAAAA", "ORORO EEEEEACACACA", "ORORO EEEEEACACACA", "ORORO  BFFFBBBBBBB",
                                "OOOOO   FFFB B B B", "        IFI       ")
                        .aisle("      BEEEEA A A A", "      BEEEEA A A A", "      BEEEEA A A A", "       BFFFA A A A",
                                "        FFFBBBBBBB", "        FFF       ")
                        .aisle("MMMMM             ", "OQOQO             ", "OQOQO             ", "OQOQO  BFFFBBBBBBB",
                                "OOOOO   FFFB B B B", "        IFI       ")
                        .aisle("MMMMM             ", "OOOOO             ", "PQSQP             ", "OOSOO  B          ",
                                "OSSSO             ", "                  ")
                        .aisle("MMMMM             ", "OOOOO             ", "PQSQP             ", "OSSSO  B          ",
                                "OSSSO  B          ", "        BBB       ")
                        .aisle("MMMMM             ", "OOOOO             ", "PQSQP             ", "OOSOO             ",
                                "OSSSO             ", "                  ")
                        .aisle("MMMMM             ", "OQOQO             ", "OQKQO             ", "OQOQO             ",
                                "OOOOO             ", "                  ")
                        .aisle("  KKKKKE          ", "  K   EE J        ", "  K   EE          ", "                  ",
                                "                  ", "                  ")
                        .where('A', blocks(GTBlocks.CASING_INVAR_HEATPROOF.get()))
                        .where('B', frames(GTNAMaterials.Inconel792))
                        .where('C', heatingCoils())
                        .where('D', blocks(GTNABlocks.IRIDIUM_PIPE_CASING.get()))
                        .where('E', blocks(GTBlocks.CASING_STEEL_SOLID.get()))
                        .where('F', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get()))
                        .where('G', blocks(GTBlocks.CASING_STAINLESS_CLEAN.get())
                                .or(threadLaserAbilities(definition.getRecipeTypes())))
                        .where('H', blocks(GTBlocks.HERMETIC_CASING_UV.get()))
                        .where('I', abilities(PartAbility.MUFFLER))
                        .where('J', controller(blocks(definition.get())))
                        .where('K', blocks(GTNABlocks.SMELTING_CONTROL_CASING.get()))
                        .where('L', blocks(GTNABlocks.ELECTRIC_POWER_TRANSMISSION_CASING.get()))
                        .where('M', blocks(GTNABlocks.STABLE_BASE_CASING.get()))
                        .where('N', blocks(GCYMBlocks.CASING_NONCONDUCTING.get()))
                        .where('O', blocks(GTNABlocks.THREE_PROOF_COMPUTER_CASING.get()))
                        .where('P', blocks(GTNABlocks.HSSS_BOROSILICATE_GLASS.get()))
                        .where('Q', blocks(GTNABlocks.MACHINING_CONTROL_CASING_MK2.get()))
                        .where('R', blocks(GTNABlocks.ENERGY_CONTROL_CASING_MK2.get()))
                        .where('S', blocks(GTNABlocks.INSULATION_TILE_MECHANICAL_BLOCK.get()))
                        .where(' ', any())
                        .build(),
                net.minecraft.network.chat.Component.translatable("gtna.machine.desulfurizer.module"));
    }
}
