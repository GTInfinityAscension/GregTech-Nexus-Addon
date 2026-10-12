package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNAMegaMachines;
import com.raishxn.gtna.common.machine.multiblock.electric.CoilWorkableElectricMultipleRecipesMachine;

import java.util.ArrayList;
import java.util.List;

/** GTO mega multiblocks of G-0204: each forms from its own preview and its recipes resolve. */
@PrefixGameTestTemplate(false)
@GameTestHolder("gtna")
public final class GTNAMegaMachineGameTests {

    private GTNAMegaMachineGameTests() {}

    /** Builds the first preview shape of {@code definition} and returns its controller. */
    static IMultiController buildPreview(GameTestHelper helper, MultiblockMachineDefinition definition) {
        return buildPreview(helper, definition, 0);
    }

    static IMultiController buildPreview(GameTestHelper helper, MultiblockMachineDefinition definition, int page) {
        var shape = definition.getMatchingShapes().get(page).getBlocks();
        IMultiController controller = null;
        for (int x = 0; x < shape.length; x++) {
            for (int y = 0; y < shape[x].length; y++) {
                for (int z = 0; z < shape[x][y].length; z++) {
                    var info = shape[x][y][z];
                    var pos = new BlockPos(x + 1, y + 1, z + 1);
                    if (info == null || info.getBlockState().isAir()) {
                        helper.setBlock(pos, Blocks.AIR);
                        continue;
                    }
                    helper.setBlock(pos, info.getBlockState());
                    if (info.getBlockState().is(definition.getBlock()) &&
                            helper.getBlockEntity(pos) instanceof IMachineBlockEntity holder &&
                            holder.getMetaMachine() instanceof IMultiController multi) {
                        controller = multi;
                    }
                }
            }
        }
        return controller;
    }

    private static void assertForms(GameTestHelper helper, MultiblockMachineDefinition definition) {
        IMultiController controller = buildPreview(helper, definition);
        helper.assertTrue(controller != null, definition.getId() + ": the preview has no controller");
        helper.assertTrue(controller.checkPatternWithLock(),
                definition.getId() + " must form from its preview: " + controller.getMultiblockState().error);
        controller.onStructureFormed();
        if (controller instanceof CoilWorkableElectricMultipleRecipesMachine coil && coil.scalesParallelWithCoil()) {
            int expected = 1 << (coil.getCoilType().getCoilTemperature() / 900);
            helper.assertTrue(coil.getMaxParallel() >= expected,
                    definition.getId() + " coil parallel must be at least 2^(K/900) = " + expected + ", got " +
                            coil.getMaxParallel());
        }
        helper.succeed();
    }

    @GameTest(template = "empty_16", timeoutTicks = 200)
    public static void largePyrolyseOvenForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.LARGE_PYROLYSE_OVEN);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void crackerHubForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.CRACKER_HUB);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void megaBrewerForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.MEGA_BREWER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void megaVacuumDryingFurnaceForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.MEGA_VACUUM_DRYING_FURNACE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 600)
    public static void giantFlotationTankForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.GIANT_FLOTATION_TANK);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void phaseChangeCubeForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.PHASE_CHANGE_CUBE);
    }

    /**
     * The preview uses the lowest glass (Tempered, MV): the machine caps itself to MV and rejects a recipe that asks
     * for a better filter than the one in the structure.
     */
    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void largeIncubatorFormsWithGlassAndFilterTiers(GameTestHelper helper) {
        IMultiController controller = buildPreview(helper, GTNAMegaMachines.LARGE_INCUBATOR);
        helper.assertTrue(controller != null, "the Large Incubator preview has no controller");
        helper.assertTrue(controller.checkPatternWithLock(),
                "the Large Incubator must form from its preview: " + controller.getMultiblockState().error);
        controller.onStructureFormed();
        var incubator = (com.raishxn.gtna.common.machine.multiblock.electric.LargeIncubatorMachine) controller;
        helper.assertTrue(incubator.getGlassTier() == com.gregtechceu.gtceu.api.GTValues.MV,
                "Tempered glass is MV, got " + incubator.getGlassTier());
        helper.assertTrue(
                incubator.getMaxVoltage() <=
                        com.gregtechceu.gtceu.api.GTValues.V[com.gregtechceu.gtceu.api.GTValues.MV],
                "the glass caps the voltage: " + incubator.getMaxVoltage());
        int filter = incubator.getFilterTier();
        helper.assertTrue(filter == 1 || filter == 2, "filter tier is 1 (cleanroom) or 2 (sterile), got " + filter);
        var sterile = com.raishxn.gtna.common.data.GTNARecipeType.INCUBATOR_RECIPES
                .recipeBuilder(com.raishxn.gtna.GTNACORE.id("test_sterile"))
                .inputItems(net.minecraft.world.item.Items.BONE_MEAL)
                .outputItems(net.minecraft.world.item.Items.MOSS_BLOCK)
                .addData(com.raishxn.gtna.common.data.GTNARecipeDataKeys.FILTER_CASING, filter + 1)
                .EUt(30).duration(20).buildRawRecipe();
        helper.assertTrue(com.raishxn.gtna.common.machine.multiblock.electric.LargeIncubatorMachine
                .filterCheck(incubator.self(), sterile) ==
                com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction.NULL,
                "a recipe asking for a better filter than the structure's must not start");
        helper.succeed();
    }

    /** The preview's glass is Tempered (MV = tier 2): 4^2 = 16 parallels without a Parallel Hatch. */
    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void giantSinteringArrayFormsWithGlassParallel(GameTestHelper helper) {
        IMultiController controller = buildPreview(helper, GTNAMegaMachines.GIANT_SINTERING_ARRAY);
        helper.assertTrue(controller != null, "the Giant Sintering Array preview has no controller");
        helper.assertTrue(controller.checkPatternWithLock(),
                "the Giant Sintering Array must form from its preview: " + controller.getMultiblockState().error);
        controller.onStructureFormed();
        var sintering = (com.raishxn.gtna.common.machine.multiblock.electric.GiantSinteringArrayMachine) controller;
        helper.assertTrue(sintering.getGlassTier() == com.gregtechceu.gtceu.api.GTValues.MV,
                "Tempered glass is MV, got " + sintering.getGlassTier());
        helper.assertTrue(sintering.getMaxParallel() == 16, "4^2 parallels, got " + sintering.getMaxParallel());
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void integratedVaporDepositionSystemForms(GameTestHelper helper) {
        IMultiController controller = buildPreview(helper, GTNAMegaMachines.INTEGRATED_VAPOR_DEPOSITION_SYSTEM);
        helper.assertTrue(controller != null && controller.checkPatternWithLock(),
                "the Integrated Vapor Deposition System must form from its preview");
        controller.onStructureFormed();
        var ivds = (com.raishxn.gtna.common.machine.multiblock.electric.GlassParallelMultipleRecipesMachine) controller;
        helper.assertTrue(ivds.getMaxParallel() == 16, "Tempered glass: 4^2 parallels, got " + ivds.getMaxParallel());
        helper.succeed();
    }

    @GameTest(template = "empty_16", timeoutTicks = 200)
    public static void reactionFurnaceForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.REACTION_FURNACE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void dysonSphereLaunchSiloForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.DYSON_SPHERE_LAUNCH_SILO);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void dysonSphereReceivingStationForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.DYSON_SPHERE_RECEIVING_STATION);
    }

    /** The swarm is kept per planet; the overworld is a planet at distance 1 or more. */
    @GameTest(template = "empty_12", timeoutTicks = 40)
    public static void dysonSwarmIsKeptPerPlanet(GameTestHelper helper) {
        var level = helper.getLevel();
        var machines = com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.class;
        var planet = com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.planetOf(level);
        helper.assertTrue(planet != null, "the overworld counts as a planet for " + machines.getSimpleName());
        helper.assertTrue(com.raishxn.gtna.common.machine.multiblock.electric.DysonSphereMachines.distance(planet) >= 1,
                "the overworld has a distance");
        var data = com.raishxn.gtna.common.data.DysonSphereData.get(level.getServer());
        int modules = data.modules(planet), damage = data.damage(planet);
        try {
            data.set(planet, 7, 61);
            helper.assertTrue(data.modules(planet) == 7 && data.damage(planet) == 61, "modules and damage are kept");
        } finally {
            data.set(planet, modules, damage);
        }
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void nyarlathotepsTentacleForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.NYARLATHOTEPS_TENTACLE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void kerrNewmanHomogenizerForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.KERR_NEWMAN_HOMOGENIZER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void engravingLaserPlantForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.ENGRAVING_LASER_PLANT);
    }

    @GameTest(template = "empty_16", timeoutTicks = 200)
    public static void infinityFluidDrillingRigForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.INFINITY_FLUID_DRILLING_RIG);
    }

    @GameTest(template = "empty_80", timeoutTicks = 600)
    public static void megaDistilleryForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.MEGA_DISTILLERY);
    }

    @GameTest(template = "empty_80", timeoutTicks = 600)
    public static void superBlastSmelterForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.SUPER_BLAST_SMELTER);
    }

    @GameTest(template = "empty_16", timeoutTicks = 200)
    public static void largeCrackerForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.LARGE_CRACKER);
    }

    @GameTest(template = "empty_80", timeoutTicks = 600)
    public static void integratedAssemblerForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.INTEGRATED_ASSEMBLER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void neutroniumWireCuttingForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.NEUTRONIUM_WIRE_CUTTING);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void holySeparatorForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HOLY_SEPARATOR);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void superconductingElectromagnetismForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.SUPERCONDUCTING_ELECTROMAGNETISM);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void superconductingMagneticPresserForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.SUPERCONDUCTING_MAGNETIC_PRESSER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void largePyrolyseOvenStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.LARGE_PYROLYSE_OVEN,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_STAINLESS_CLEAN.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void crackerHubStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.CRACKER_HUB,
                com.raishxn.gtna.common.data.GTNABlocks.NAQUADAH_ALLOY_CASING.get(), 1, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void crackerHubThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.CRACKER_HUB,
                com.raishxn.gtna.common.data.GTNABlocks.NAQUADAH_ALLOY_CASING.get(), 1);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void megaBrewerStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.MEGA_BREWER,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_CORROSION_PROOF.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void megaVacuumDryingFurnaceStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.MEGA_VACUUM_DRYING_FURNACE,
                com.gregtechceu.gtceu.common.data.GTBlocks.HIGH_POWER_CASING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void megaVacuumDryingFurnaceCoilGate(GameTestHelper helper) {
        coilGate(helper, GTNAMegaMachines.MEGA_VACUUM_DRYING_FURNACE,
                com.gregtechceu.gtceu.common.data.GTBlocks.HIGH_POWER_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void giantFlotationTankStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.GIANT_FLOTATION_TANK,
                com.raishxn.gtna.common.data.GTNABlocks.HASTELLOY_N_75_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void phaseChangeCubeStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.PHASE_CHANGE_CUBE,
                com.gregtechceu.gtceu.common.data.GTBlocks.HIGH_POWER_CASING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void phaseChangeCubeThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.PHASE_CHANGE_CUBE,
                com.gregtechceu.gtceu.common.data.GTBlocks.HIGH_POWER_CASING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void engravingLaserPlantStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.ENGRAVING_LASER_PLANT,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void megaDistilleryStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.MEGA_DISTILLERY,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_STAINLESS_CLEAN.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void superBlastSmelterStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.SUPER_BLAST_SMELTER,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void superBlastSmelterCoilGate(GameTestHelper helper) {
        coilGate(helper, GTNAMegaMachines.SUPER_BLAST_SMELTER,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void superBlastSmelterThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.SUPER_BLAST_SMELTER,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void largeCrackerStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.LARGE_CRACKER,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_STAINLESS_CLEAN.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void integratedAssemblerStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.INTEGRATED_ASSEMBLER,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void integratedAssemblerThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.INTEGRATED_ASSEMBLER,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void neutroniumWireCuttingStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.NEUTRONIUM_WIRE_CUTTING,
                com.gregtechceu.gtceu.common.data.GTBlocks.HIGH_POWER_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void holySeparatorStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.HOLY_SEPARATOR, com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(),
                0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void holySeparatorThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.HOLY_SEPARATOR, com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(),
                0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void superconductingElectromagnetismStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.SUPERCONDUCTING_ELECTROMAGNETISM,
                com.raishxn.gtna.common.data.GTNABlocks.LAFIUM_MECHANICAL_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void superconductingElectromagnetismThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.SUPERCONDUCTING_ELECTROMAGNETISM,
                com.raishxn.gtna.common.data.GTNABlocks.LAFIUM_MECHANICAL_CASING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void superconductingMagneticPresserStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.SUPERCONDUCTING_MAGNETIC_PRESSER,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void superconductingMagneticPresserThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.SUPERCONDUCTING_MAGNETIC_PRESSER,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void magneticEnergyReactionFurnaceForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.MAGNETIC_ENERGY_REACTION_FURNACE);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void magneticEnergyReactionFurnaceStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.MAGNETIC_ENERGY_REACTION_FURNACE,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_NONCONDUCTING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void magneticEnergyReactionFurnaceThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.MAGNETIC_ENERGY_REACTION_FURNACE,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_NONCONDUCTING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void particleStreamMatrixFillingMachineForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.PARTICLE_STREAM_MATRIX_FILLING_MACHINE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void particleStreamMatrixFillingMachineStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.PARTICLE_STREAM_MATRIX_FILLING_MACHINE,
                com.raishxn.gtna.common.data.GTNABlocks.LAFIUM_MECHANICAL_CASING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void particleStreamMatrixFillingMachineThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.PARTICLE_STREAM_MATRIX_FILLING_MACHINE,
                com.raishxn.gtna.common.data.GTNABlocks.LAFIUM_MECHANICAL_CASING.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void nanitesCircuitAssemblyFactoryForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.NANITES_CIRCUIT_ASSEMBLY_FACTORY);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void nanitesCircuitAssemblyFactoryStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.NANITES_CIRCUIT_ASSEMBLY_FACTORY,
                com.raishxn.gtna.common.data.GTNABlocks.NAQUADAH_ALLOY_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void nanitesCircuitAssemblyFactoryThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.NANITES_CIRCUIT_ASSEMBLY_FACTORY,
                com.raishxn.gtna.common.data.GTNABlocks.NAQUADAH_ALLOY_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void megaWiremillForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.MEGA_WIREMILL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void megaWiremillStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.MEGA_WIREMILL,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_INVAR_HEATPROOF.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void megaWiremillThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.MEGA_WIREMILL,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_INVAR_HEATPROOF.get(), 0);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void crystalBuilderForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.CRYSTAL_BUILDER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void crystalBuilderStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.CRYSTAL_BUILDER, com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(),
                0, Limit.COIL);
    }

    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void crystalBuilderThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.CRYSTAL_BUILDER,
                com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void highEnergyLaserLatheForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HIGH_ENERGY_LASER_LATHE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void highEnergyLaserLatheStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.HIGH_ENERGY_LASER_LATHE,
                com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void highEnergyLaserLatheThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.HIGH_ENERGY_LASER_LATHE,
                com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void extremeCompressorForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.EXTREME_COMPRESSOR);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void extremeCompressorStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.EXTREME_COMPRESSOR,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void extremeCompressorThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.EXTREME_COMPRESSOR,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void geminiContainmentSystemForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.GEMINI_CONTAINMENT_SYSTEM);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void geminiContainmentSystemStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.GEMINI_CONTAINMENT_SYSTEM,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void geminiContainmentSystemThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.GEMINI_CONTAINMENT_SYSTEM,
                com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void giantElectrochemicalWorkstationForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.GIANT_ELECTROCHEMICAL_WORKSTATION);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void giantElectrochemicalWorkstationStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.GIANT_ELECTROCHEMICAL_WORKSTATION,
                com.raishxn.gtna.common.data.GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void giantElectrochemicalWorkstationThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.GIANT_ELECTROCHEMICAL_WORKSTATION,
                com.raishxn.gtna.common.data.GTNABlocks.SPACE_ELEVATOR_MECHANICAL_CASING.get(), 0);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void hyperdimensionalPlasmaFusionCoreForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HYPERDIMENSIONAL_PLASMA_FUSION_CORE);
    }

    private static com.gregtechceu.gtceu.api.recipe.GTRecipe plasmaFusionCoreRecipe(String id, int temperature) {
        var type = com.raishxn.gtna.common.data.GTNARecipeType.PLASMA_FORGE_RECIPES;
        var recipe = type.recipeBuilder(com.raishxn.gtna.GTNACORE.id(id))
                .inputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.GLASS))
                .outputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.TINTED_GLASS))
                .EUt(com.gregtechceu.gtceu.api.GTValues.VA[com.gregtechceu.gtceu.api.GTValues.LV]).duration(200)
                .blastFurnaceTemp(temperature).buildRawRecipe();
        GTNAGameTestUtils.stageWithRealRecipes(type, recipe);
        return recipe;
    }

    /** A Plasma Forge recipe within the coil heat runs with the UV Parallel Hatch (16 input sets, 16 parallels). */
    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void hyperdimensionalPlasmaFusionCoreRunsParallel(GameTestHelper helper) {
        var recipe = plasmaFusionCoreRecipe("gametest_hpfc_parallel", 1000);
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, GTNAMegaMachines.HYPERDIMENSIONAL_PLASMA_FUSION_CORE);
        rig.placeIo(com.raishxn.gtna.common.data.GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get(), 2, 2, 0, 0, true,
                false);
        rig.form();
        rig.runAndCheck(recipe, 16, 256);
        helper.succeed();
    }

    /** A recipe hotter than the coils never starts. */
    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void hyperdimensionalPlasmaFusionCoreRejectsHotterRecipe(GameTestHelper helper) {
        var recipe = plasmaFusionCoreRecipe("gametest_hpfc_too_hot", 1_000_000);
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, GTNAMegaMachines.HYPERDIMENSIONAL_PLASMA_FUSION_CORE);
        rig.placeIo(com.raishxn.gtna.common.data.GTNABlocks.DIMENSIONALLY_TRANSCENDENT_CASING.get(), 2, 2, 0, 0, true,
                false);
        rig.form();
        rig.feed(recipe, 1);
        helper.assertFalse(rig.start(40), "a 1,000,000 K recipe must not start on Tritanium coils; " + rig.status());
        helper.succeed();
    }

    /**
     * Builds preview page 0 (main structure) and page {@code page} (a module) with their controllers on the same
     * block, then checks the module forms on the controller.
     */
    private static void assertModuleForms(GameTestHelper helper, MultiblockMachineDefinition definition, int page) {
        var shapes = definition.getMatchingShapes();
        helper.assertTrue(shapes.size() > page, definition.getId() + ": no module preview page " + page);
        BlockPos anchor = new BlockPos(30, 2, 30);
        IMultiController controller = null;
        for (int p : new int[] { page, 0 }) {
            var shape = shapes.get(p).getBlocks();
            BlockPos local = null;
            for (int x = 0; x < shape.length && local == null; x++)
                for (int y = 0; y < shape[x].length && local == null; y++)
                    for (int z = 0; z < shape[x][y].length; z++)
                        if (shape[x][y][z] != null && shape[x][y][z].getBlockState().is(definition.getBlock())) {
                            local = new BlockPos(x, y, z);
                            break;
                        }
            helper.assertTrue(local != null, definition.getId() + ": preview page " + p + " has no controller");
            for (int x = 0; x < shape.length; x++) {
                for (int y = 0; y < shape[x].length; y++) {
                    for (int z = 0; z < shape[x][y].length; z++) {
                        var info = shape[x][y][z];
                        if (info == null || info.getBlockState().isAir()) continue;
                        BlockPos pos = anchor.offset(x - local.getX(), y - local.getY(), z - local.getZ());
                        helper.setBlock(pos, info.getBlockState());
                        if (helper.getBlockEntity(pos) instanceof IMachineBlockEntity holder &&
                                holder.getMetaMachine() instanceof IMultiController multi) {
                            controller = multi;
                        }
                    }
                }
            }
        }
        helper.assertTrue(controller != null && controller.checkPatternWithLock(),
                definition.getId() + " main structure must form with the module attached");
        helper.assertTrue(((com.raishxn.gtna.api.machine.multiblock.IGTNAModuleHost) controller)
                .gtna$formedModuleCount() == 1, definition.getId() + ": the module must form on the controller");
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void desulfurizerForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.DESULFURIZER);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void desulfurizerModuleForms(GameTestHelper helper) {
        assertModuleForms(helper, GTNAMegaMachines.DESULFURIZER, 1);
    }

    /**
     * 64 sets of the GTO natural gas recipe run as 64 coil parallels (300 sets would overflow the rig's single
     * output fluid hatch: 16,000 mB each).
     */
    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void desulfurizerRunsCoilParallel(GameTestHelper helper) {
        var recipe = helper.getLevel().getRecipeManager()
                .byKey(GTNACORE.id("desulfurizer/natural_gas")).orElseThrow();
        var gt = (GTRecipe) recipe;
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, GTNAMegaMachines.DESULFURIZER);
        rig.placeIo(com.gregtechceu.gtceu.common.data.GTBlocks.CASING_STAINLESS_CLEAN.get(), 0, 2, 1, 1, false,
                false);
        rig.form();
        rig.runAndCheck(gt, 64, 1 << (GTNAMultiblockRig.TRITANIUM_COIL_K / 900));
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void dimensionalFocusEngravingArrayForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.DIMENSIONAL_FOCUS_ENGRAVING_ARRAY);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void starUltimateMaterialForgeFactoryForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.STAR_ULTIMATE_MATERIAL_FORGE_FACTORY);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void handOfArachneForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HAND_OF_ARACHNE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void handOfArachneStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.HAND_OF_ARACHNE,
                com.raishxn.gtna.common.data.GTNABlocks.PRESSURE_CONTAINMENT_CASING.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void rareEarthCentrifugalForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.RARE_EARTH_CENTRIFUGAL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void heavyRollingForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HEAVY_ROLLING);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void heavyRollingStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.HEAVY_ROLLING,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get(), 0, Limit.COIL);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void heavyRollingThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.HEAVY_ROLLING,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_HIGH_TEMPERATURE_SMELTING.get(), 0);
    }

    /** Runs a staged one-item recipe of {@code type} on {@code definition}; checks parallels up to the cap. */
    private static void stagedRecipeRuns(GameTestHelper helper, MultiblockMachineDefinition definition,
                                         com.gregtechceu.gtceu.api.recipe.GTRecipeType type,
                                         net.minecraft.world.level.block.Block casing, boolean parallelHatch,
                                         int sets, int cap) {
        var recipe = type.recipeBuilder(com.raishxn.gtna.GTNACORE.id("gametest_" + definition.getId().getPath()))
                .inputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.GLASS))
                .outputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.TINTED_GLASS))
                .EUt(com.gregtechceu.gtceu.api.GTValues.VA[com.gregtechceu.gtceu.api.GTValues.LV]).duration(200)
                .buildRawRecipe();
        GTNAGameTestUtils.stageWithRealRecipes(type, recipe);
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, definition);
        rig.placeIo(casing, 2, 2, 0, 0, parallelHatch, false);
        rig.form();
        rig.runAndCheck(recipe, sets, cap);
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void dimensionalFocusEngravingArrayRunsRecipe(GameTestHelper helper) {
        stagedRecipeRuns(helper, GTNAMegaMachines.DIMENSIONAL_FOCUS_ENGRAVING_ARRAY,
                com.raishxn.gtna.common.data.GTNARecipeType.DIMENSIONAL_FOCUS_ENGRAVING_ARRAY_RECIPES,
                com.gregtechceu.gtceu.common.data.GCYMBlocks.CASING_LASER_SAFE_ENGRAVING.get(), false, 64,
                1 << (GTNAMultiblockRig.TRITANIUM_COIL_K / 900));
    }

    /** Unlimited parallel: 300 input sets run as 300 parallels. */
    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void starUltimateMaterialForgeFactoryRunsRecipe(GameTestHelper helper) {
        stagedRecipeRuns(helper, GTNAMegaMachines.STAR_ULTIMATE_MATERIAL_FORGE_FACTORY,
                com.raishxn.gtna.common.data.GTNARecipeType.ULTIMATE_MATERIAL_FORGE_RECIPES,
                com.raishxn.gtna.common.data.GTNABlocks.MOLECULAR_CASING.get(), false, 300, Integer.MAX_VALUE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void rareEarthCentrifugalRunsRecipe(GameTestHelper helper) {
        stagedRecipeRuns(helper, GTNAMegaMachines.RARE_EARTH_CENTRIFUGAL,
                com.raishxn.gtna.common.data.GTNARecipeType.RARE_EARTH_CENTRIFUGAL_RECIPES,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_HSSE_STURDY.get(), true, 64, 256);
    }

    // ---- G-0246 ----

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void lightningRodForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.LIGHTNING_ROD);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void lightningRodStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.LIGHTNING_ROD,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_PALLADIUM_SUBSTATION.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void spaceProbeSurfaceReceptionForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.SPACE_PROBE_SURFACE_RECEPTION);
    }

    /** Outside space (the GameTest overworld) the probe never starts. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void spaceProbeSurfaceReceptionNeedsSpace(GameTestHelper helper) {
        var controller = buildPreview(helper, GTNAMegaMachines.SPACE_PROBE_SURFACE_RECEPTION);
        helper.assertTrue(
                controller instanceof com.raishxn.gtna.common.machine.multiblock.electric.SpaceProbeSurfaceReceptionMachine probe &&
                        !probe.inSpace() && !probe.beforeWorking(null),
                "the space probe must refuse to work in the overworld");
        helper.succeed();
    }

    /** Each PCB Factory tier forms from its own preview page once the controller is set to that tier. */
    private static void pcbTierForms(GameTestHelper helper, int tier) {
        var controller = buildPreview(helper, GTNAMegaMachines.PCB_FACTORY, tier - 1);
        helper.assertTrue(controller instanceof com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine,
                "pcb_factory: no controller on preview page " + tier);
        var pcb = (com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine) controller;
        pcb.setMachineTier(tier);
        helper.assertTrue(pcb.checkPatternWithLock(),
                "pcb_factory tier " + tier + " must form: " + pcb.getMultiblockState().error);
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void pcbFactoryTier1Forms(GameTestHelper helper) {
        pcbTierForms(helper, 1);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void pcbFactoryTier2Forms(GameTestHelper helper) {
        pcbTierForms(helper, 2);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void pcbFactoryTier3Forms(GameTestHelper helper) {
        pcbTierForms(helper, 3);
    }

    /** GTO tier caps: 30,719 EU/t at tier 1, 491,519 EU/t at tier 2, none at tier 3. */
    @GameTest(template = "empty_16", timeoutTicks = 40)
    public static void pcbFactoryTierCaps(GameTestHelper helper) {
        var pcb = com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine.class;
        helper.assertTrue(com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine.maxEUt(1) == 30719 &&
                com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine.maxEUt(2) == 491519 &&
                com.raishxn.gtna.common.machine.multiblock.electric.PCBFactoryMachine.maxEUt(3) == Long.MAX_VALUE,
                pcb.getSimpleName() + " tier caps differ from GTO");
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void pcbFactoryRunsRealRecipe(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.PCB_FACTORY, com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 0,
                Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void compoundExtremeCoolingUnitForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT);
    }

    /** The plasma structure (preview page 2) forms only in Plasma Condenser mode. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void compoundExtremeCoolingUnitPlasmaStructureForms(GameTestHelper helper) {
        var controller = buildPreview(helper, GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT, 1);
        helper.assertTrue(
                controller instanceof com.raishxn.gtna.common.machine.multiblock.electric.CompoundExtremeCoolingMachine,
                "compound_extreme_cooling_unit: no controller on the plasma page");
        var cecu = (com.raishxn.gtna.common.machine.multiblock.electric.CompoundExtremeCoolingMachine) controller;
        cecu.setActiveRecipeType(2);
        helper.assertTrue(cecu.plasmaMode() && cecu.checkPatternWithLock(),
                "plasma mode must form the plasma structure: " + cecu.getMultiblockState().error);
        helper.succeed();
    }

    /** The vacuum structure alone (preview page 1) does not form in Plasma Condenser mode. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void compoundExtremeCoolingUnitPlasmaModeNeedsPlasmaStructure(GameTestHelper helper) {
        var cecu = (com.raishxn.gtna.common.machine.multiblock.electric.CompoundExtremeCoolingMachine) buildPreview(
                helper, GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT, 0);
        helper.assertTrue(cecu.checkPatternWithLock(), "the vacuum structure must form in vacuum mode");
        cecu.setActiveRecipeType(2);
        helper.assertFalse(cecu.checkPatternWithLock(), "plasma mode must not form on the vacuum structure");
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void compoundExtremeCoolingUnitStress(GameTestHelper helper) {
        stress(helper, GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_ALUMINIUM_FROSTPROOF.get(), 0, Limit.HATCH);
    }

    @GameTest(template = "empty_80", timeoutTicks = 1200)
    public static void compoundExtremeCoolingUnitThreads(GameTestHelper helper) {
        threads(helper, GTNAMegaMachines.COMPOUND_EXTREME_COOLING_UNIT,
                com.gregtechceu.gtceu.common.data.GTBlocks.CASING_ALUMINIUM_FROSTPROOF.get(), 0);
    }

    // ---- G-0247 ----

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void hyperReactorForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.HYPER_REACTOR);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void advancedHyperReactorForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.ADVANCED_HYPER_REACTOR);
    }

    /** A recipe booster present in the hatches gives its parallel; without it the run stays single. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void hyperReactorBoosterGivesParallel(GameTestHelper helper) {
        var type = com.raishxn.gtna.common.data.GTNARecipeType.HYPER_REACTOR_RECIPES;
        var water = com.gregtechceu.gtceu.common.data.GTMaterials.Water;
        var lava = com.gregtechceu.gtceu.common.data.GTMaterials.Lava;
        var booster = new net.minecraft.nbt.CompoundTag();
        booster.putString("fluid", "minecraft:lava");
        booster.putInt("parallel", 16);
        var list = new net.minecraft.nbt.ListTag();
        list.add(booster);
        var recipe = type.recipeBuilder(GTNACORE.id("gametest_hyper_booster"))
                .inputFluids(water.getFluid(10)).duration(20)
                .EUt(-com.gregtechceu.gtceu.api.GTValues.V[com.gregtechceu.gtceu.api.GTValues.LV]).buildRawRecipe();
        recipe.data.put(com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine.BOOSTERS, list);
        var controller = buildPreview(helper, GTNAMegaMachines.HYPER_REACTOR);
        helper.assertTrue(controller != null && controller.checkPatternWithLock(), "hyper_reactor must form");
        controller.onStructureFormed();
        var reactor = (com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine) controller;
        var hatches = new java.util.ArrayList<com.gregtechceu.gtceu.common.machine.multiblock.part.FluidHatchPartMachine>();
        for (var part : reactor.getParts()) {
            if (part instanceof com.gregtechceu.gtceu.common.machine.multiblock.part.FluidHatchPartMachine hatch &&
                    hatch.tank.getHandlerIO() == com.gregtechceu.gtceu.api.capability.recipe.IO.IN) {
                hatches.add(hatch);
            }
        }
        helper.assertTrue(hatches.size() >= 2, "the preview must carry two fluid input hatches, got " + hatches.size());
        hatches.get(0).tank.setFluidInTank(0, water.getFluid(320));
        helper.assertTrue(reactor.availableBooster(recipe) == null, "no lava yet: no booster");
        helper.assertTrue(com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine
                .recipeModifier(reactor, recipe).apply(recipe).parallels == 1, "without booster the run is single");
        hatches.get(1).tank.setFluidInTank(0, lava.getFluid(1));
        helper.assertTrue(reactor.availableBooster(recipe) != null, "1 mB of lava must be found as booster");
        int parallels = com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine
                .recipeModifier(reactor, recipe).apply(recipe).parallels;
        helper.assertTrue(parallels == 16, "the booster must give 16 parallels, got " + parallels);
        helper.succeed();
    }

    // ---- G-0248 ----

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void fuelCellGeneratorForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.FUEL_CELL_GENERATOR);
    }

    private static GTNAMultiblockRig fuelCellRig(GameTestHelper helper) {
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, GTNAMegaMachines.FUEL_CELL_GENERATOR);
        rig.placeIo(com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 1, 0, 4, 2, false, false);
        rig.form();
        return rig;
    }

    /** Release: a charged electrolyte with its membrane runs up to 50 parallel and produces EU. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void fuelCellReleaseRunsParallel(GameTestHelper helper) {
        var recipe = (GTRecipe) helper.getLevel().getRecipeManager()
                .byKey(GTNACORE.id("fuel_cell_energy_release/iron_chromium_release")).orElseThrow();
        GTNAMultiblockRig rig = fuelCellRig(helper);
        var cell = (com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine) rig.machine();
        cell.setActiveRecipeType(2);
        rig.feed(recipe, 64);
        helper.assertTrue(cell.isGenerator(), "release mode must be a generator");
        var modified = com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine
                .recipeModifier(cell, recipe).apply(recipe);
        helper.assertTrue(modified != null && modified.parallels == 50,
                "64 sets must release at the 50 parallel cap, got " + (modified == null ? "null" : modified.parallels) +
                        "; " + rig.status());
        helper.succeed();
    }

    /** Absorption: fuel + LOX charge the released electrolyte; the run lowers the membrane efficiency. */
    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void fuelCellAbsorptionChargesElectrolyte(GameTestHelper helper) {
        var electrolyte = com.raishxn.gtna.common.data.material.FuelCellMaterials.IronChromiumElectrolyte;
        var recipe = (GTRecipe) helper.getLevel().getRecipeManager()
                .byKey(GTNACORE.id("fuel_cell_energy_absorption/diesel")).orElseThrow();
        GTNAMultiblockRig rig = fuelCellRig(helper);
        var cell = (com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine) rig.machine();
        cell.setActiveRecipeType(0);
        rig.feed(recipe, 100);
        var released = com.raishxn.gtna.common.data.GTNARecipeType.FUEL_CELL_ENERGY_RELEASE_RECIPES
                .recipeBuilder(GTNACORE.id("gametest_released"))
                .inputFluids(electrolyte.getFluid(
                        com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_RELEASE_ANODE, 1000))
                .inputFluids(electrolyte.getFluid(
                        com.raishxn.gtna.common.data.material.FuelCellMaterials.ENERGY_RELEASE_CATHODE, 1000))
                .duration(1).buildRawRecipe();
        rig.feed(released, 1);
        helper.assertTrue(cell.bestMembrane() != null, "a membrane electrode must be found; " + rig.status());
        var modified = com.raishxn.gtna.common.machine.multiblock.electric.FuelCellGeneratorMachine
                .recipeModifier(cell, recipe).apply(recipe);
        helper.assertTrue(modified != null &&
                modified.getOutputContents(com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability.CAP)
                        .size() == 2,
                "absorption must output the two charged electrolyte states");
        double before = cell.getAccumulatedDecay();
        cell.beforeWorking(modified);
        helper.assertTrue(cell.getAccumulatedDecay() < before, "each absorption run must lower the efficiency");
        helper.succeed();
    }

    // ---- G-0249 ----

    /** Each Supercomputing Center tier forms from its own preview page at that tier, and not at another tier. */
    private static void supercomputingTierForms(GameTestHelper helper, int tier) {
        var controller = buildPreview(helper, GTNAMegaMachines.SUPERCOMPUTING_CENTER, tier - 1);
        helper.assertTrue(
                controller instanceof com.raishxn.gtna.common.machine.multiblock.electric.SupercomputingCenterMachine,
                "supercomputing_center: no controller on preview page " + tier);
        var center = (com.raishxn.gtna.common.machine.multiblock.electric.SupercomputingCenterMachine) controller;
        center.setMachineTier(tier % 3 + 1);
        helper.assertFalse(center.checkPatternWithLock(),
                "the tier " + tier + " structure must not form at tier " + (tier % 3 + 1));
        center.setMachineTier(tier);
        helper.assertTrue(center.checkPatternWithLock(),
                "supercomputing_center tier " + tier + " must form: " + center.getMultiblockState().error);
        center.onStructureFormed();
        helper.assertTrue(center.requestCWUt(64, true) == 0, "no CWU/t before the first paid cycle");
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void supercomputingCenterTier1Forms(GameTestHelper helper) {
        supercomputingTierForms(helper, 1);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void supercomputingCenterTier2Forms(GameTestHelper helper) {
        supercomputingTierForms(helper, 2);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void supercomputingCenterTier3Forms(GameTestHelper helper) {
        supercomputingTierForms(helper, 3);
    }

    /** GTO component values: NICH 64 CWU/t (16 cooling), GWCA 1024 CWU/t (256 cooling). */
    @GameTest(template = "empty_16", timeoutTicks = 40)
    public static void researchComponentValues(GameTestHelper helper) {
        helper.setBlock(new BlockPos(1, 1, 1),
                com.raishxn.gtna.common.data.GTNAResearchMachines.NICH_COMPUTING_COMPONENTS.getBlock());
        helper.setBlock(new BlockPos(2, 1, 1),
                com.raishxn.gtna.common.data.GTNAResearchMachines.GWCA_COMPUTING_COMPONENTS.getBlock());
        var nich = (com.raishxn.gtna.common.machine.multiblock.part.research.ExResearchPartMachine.Computation) ((IMachineBlockEntity) helper
                .getBlockEntity(new BlockPos(1, 1, 1))).getMetaMachine();
        var gwca = (com.raishxn.gtna.common.machine.multiblock.part.research.ExResearchPartMachine.Computation) ((IMachineBlockEntity) helper
                .getBlockEntity(new BlockPos(2, 1, 1))).getMetaMachine();
        helper.assertTrue(nich.getCWUPerTick() == 64 && nich.getCoolingPerTick() == 16, "NICH values differ from GTO");
        helper.assertTrue(gwca.getCWUPerTick() == 1024 && gwca.getCoolingPerTick() == 256,
                "GWCA values differ from GTO");
        helper.succeed();
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void dataCenterForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.DATA_CENTER);
    }

    @GameTest(template = "empty_80", timeoutTicks = 400)
    public static void analysisAndResearchCenterForms(GameTestHelper helper) {
        assertForms(helper, GTNAMegaMachines.ANALYSIS_AND_RESEARCH_CENTER);
    }

    /** GTO weighted pick: rolls 0-2499 give the first output, 2500-4999 the second, past all chances the last. */
    @GameTest(template = "empty_16", timeoutTicks = 40)
    public static void analysisAndResearchCenterPicksOneOutput(GameTestHelper helper) {
        var a = new com.gregtechceu.gtceu.api.recipe.content.Content(
                net.minecraft.world.item.crafting.Ingredient.of(net.minecraft.world.item.Items.GLASS), 2500, 10000, 0);
        var b = new com.gregtechceu.gtceu.api.recipe.content.Content(
                net.minecraft.world.item.crafting.Ingredient.of(net.minecraft.world.item.Items.STONE), 2500, 10000, 0);
        var c = new com.gregtechceu.gtceu.api.recipe.content.Content(
                net.minecraft.world.item.crafting.Ingredient.of(net.minecraft.world.item.Items.DIRT), 2500, 10000, 0);
        var outputs = List.of(a, b, c);
        java.util.function.BiFunction<List<com.gregtechceu.gtceu.api.recipe.content.Content>, Integer, List<com.gregtechceu.gtceu.api.recipe.content.Content>> pick = com.raishxn.gtna.common.machine.multiblock.electric.AnalysisAndResearchCenterMachine::pickOne;
        helper.assertTrue(pick.apply(outputs, 100).get(0).content == a.content, "roll 100 must give the first");
        helper.assertTrue(pick.apply(outputs, 3000).get(0).content == b.content, "roll 3000 must give the second");
        helper.assertTrue(pick.apply(outputs, 9000).get(0).content == c.content, "roll 9000 falls back to the last");
        helper.assertTrue(pick.apply(outputs, 100).get(0).chance == 10000, "the picked output is guaranteed");
        helper.succeed();
    }

    /** Precision Laser Engraving is serial: even with a UV Parallel Hatch and 16 input sets it runs one. */
    @GameTest(template = "empty_48", timeoutTicks = 1200)
    public static void engravingLaserPlantPrecisionModeIsSerial(GameTestHelper helper) {
        var type = com.raishxn.gtna.common.data.GTNARecipeType.PRECISION_LASER_ENGRAVER_RECIPES;
        var recipe = type.recipeBuilder(com.raishxn.gtna.GTNACORE.id("gametest_precision_engraving"))
                .inputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.GLASS))
                .outputItems(new net.minecraft.world.item.ItemStack(net.minecraft.world.item.Items.TINTED_GLASS))
                .EUt(com.gregtechceu.gtceu.api.GTValues.VA[com.gregtechceu.gtceu.api.GTValues.LV]).duration(40960)
                .buildRawRecipe();
        GTNAGameTestUtils.stageWithRealRecipes(type, recipe);
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, GTNAMegaMachines.ENGRAVING_LASER_PLANT);
        rig.placeIo(com.raishxn.gtna.common.data.GTNABlocks.IRIDIUM_CASING.get(), 2, 2, 0, 0, true, false);
        rig.form();
        selectType(rig, 1);
        rig.feed(recipe, 16);
        helper.assertTrue(rig.start(40), "precision engraving must start; " + rig.status());
        helper.assertTrue(rig.runningParallels() == 1,
                "precision engraving ignores the Parallel Hatch, got " + rig.runningParallels());
        int duration = rig.runningDuration();
        helper.assertTrue(duration == 2,
                "UV energy on an LV recipe: 7 perfect overclocks (40960 / 4^7 = 2), got " + duration);
        helper.succeed();
    }

    /** Parallel source of a stressed machine. */
    enum Limit {
        /** {@code 2^(coil K / 900)}: Tritanium coils give 4096. */
        COIL,
        /** A UV Parallel Hatch: 256. */
        HATCH,
        /** Serial. */
        NONE
    }

    private static final com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability ITEM = com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP;
    private static final com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability FLUID = com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability.CAP;

    private static void selectType(GTNAMultiblockRig rig, int typeIndex) {
        if (rig.machine() instanceof com.gregtechceu.gtceu.api.machine.multiblock.WorkableMultiblockMachine workable) {
            workable.setActiveRecipeType(typeIndex);
        }
    }

    /**
     * Stress run (G-0208): UV hatches placed where the pattern accepts them, Tritanium coils, a real recipe of the
     * machine's {@code typeIndex} recipe type with up to 300 input sets; the parallel count must hit
     * {@code min(limit, sets)} and the outputs must scale with it.
     */
    static void stress(GameTestHelper helper, com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition definition,
                       net.minecraft.world.level.block.Block casing, int typeIndex, Limit limit) {
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, definition);
        var type = definition.getRecipeTypes()[typeIndex];
        com.gregtechceu.gtceu.api.recipe.GTRecipe recipe = null;
        int sets = limit == Limit.NONE ? 4 : 300;
        while (sets >= 1) {
            recipe = rig.pickRecipe(type, sets, GTNAMultiblockRig.TRITANIUM_COIL_K + 600, true);
            if (recipe != null) break;
            sets = sets > 64 ? 64 : sets / 2;
        }
        helper.assertTrue(recipe != null, definition.getId() + ": no usable " + type.registryName + " recipe");
        rig.placeIo(casing, recipe.getInputContents(ITEM).isEmpty() ? 0 : 2,
                recipe.getOutputContents(ITEM).isEmpty() ? 0 : 2, recipe.getInputContents(FLUID).size(),
                recipe.getOutputContents(FLUID).size(), limit == Limit.HATCH, false);
        rig.form();
        selectType(rig, typeIndex);
        int cap = switch (limit) {
            case COIL -> 1 << (GTNAMultiblockRig.TRITANIUM_COIL_K / 900);
            case HATCH -> 256;
            case NONE -> 1;
        };
        rig.runAndCheck(recipe, sets, cap);
        helper.succeed();
    }

    /** Thread Hatch run: two different recipes fed at once must run side by side. */
    static void threads(GameTestHelper helper, com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition definition,
                        net.minecraft.world.level.block.Block casing, int typeIndex) {
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, definition);
        var type = definition.getRecipeTypes()[typeIndex];
        java.util.List<com.gregtechceu.gtceu.api.recipe.GTRecipe> picked = new java.util.ArrayList<>();
        for (var recipe : helper.getLevel().getRecipeManager().getAllRecipesFor(type)) {
            if (picked.size() == 2) break;
            if (!recipe.conditions.isEmpty() || recipe.data.getInt("ebf_temp") > GTNAMultiblockRig.TRITANIUM_COIL_K)
                continue;
            if (recipe.getInputContents(FLUID).size() > 2 || recipe.getOutputContents(FLUID).size() > 2) continue;
            if (recipe.getInputContents(ITEM).isEmpty() && recipe.getInputContents(FLUID).isEmpty()) continue;
            if (com.gregtechceu.gtceu.api.recipe.RecipeHelper.getRealEUt(recipe).getTotalEU() > 8192) continue;
            if (picked.stream().anyMatch(other -> sharesInput(other, recipe))) continue;
            if (!GTNAMultiblockRig.inLookup(recipe)) continue;
            picked.add(recipe);
        }
        helper.assertTrue(picked.size() == 2,
                definition.getId() + ": needs two " + type.registryName + " recipes with distinct inputs");
        int fluidIn = picked.get(0).getInputContents(FLUID).size() + picked.get(1).getInputContents(FLUID).size();
        int fluidOut = Math.max(picked.get(0).getOutputContents(FLUID).size(),
                picked.get(1).getOutputContents(FLUID).size());
        boolean items = picked.stream().anyMatch(r -> !r.getInputContents(ITEM).isEmpty());
        boolean itemOut = picked.stream().anyMatch(r -> !r.getOutputContents(ITEM).isEmpty());
        rig.placeIo(casing, items ? 2 : 0, itemOut ? 2 : 0, fluidIn, fluidOut, false, true);
        rig.form();
        selectType(rig, typeIndex);
        rig.feed(picked.get(0), 1, 0);
        rig.feed(picked.get(1), 1, 1);
        helper.assertTrue(rig.start(40), definition.getId() + " must start with a Thread Hatch; " + rig.status());
        rig.tick(2);
        helper.assertTrue(rig.peakActive >= 2, definition.getId() + " with a UV Thread Hatch must run " +
                picked.get(0).id + " and " + picked.get(1).id + " together, peak=" + rig.peakActive + "; " +
                rig.status());
        helper.succeed();
    }

    private static boolean sharesInput(com.gregtechceu.gtceu.api.recipe.GTRecipe a,
                                       com.gregtechceu.gtceu.api.recipe.GTRecipe b) {
        for (var x : a.getInputContents(ITEM)) {
            var ix = ITEM.of(x.content).getItems();
            for (var y : b.getInputContents(ITEM)) {
                var iy = ITEM.of(y.content).getItems();
                if (x.chance == 0 || y.chance == 0) continue; // circuits and other non-consumed inputs are shared
                if (ix.length > 0 && iy.length > 0 && ix[0].getItem() == iy[0].getItem()) return true;
            }
        }
        return false;
    }

    /** Heating-coil gate: with Cupronickel coils a recipe hotter than 5000K must never start. */
    static void coilGate(GameTestHelper helper,
                         com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition definition,
                         net.minecraft.world.level.block.Block casing, int typeIndex) {
        GTNAMultiblockRig rig = GTNAMultiblockRig.build(helper, definition);
        for (var pos : rig.allPositions) {
            if (helper.getBlockState(pos).getBlock() instanceof com.gregtechceu.gtceu.common.block.CoilBlock) {
                helper.setBlock(pos, com.gregtechceu.gtceu.common.data.GTBlocks.COIL_CUPRONICKEL.get());
            }
        }
        var type = definition.getRecipeTypes()[typeIndex];
        com.gregtechceu.gtceu.api.recipe.GTRecipe hot = null;
        for (var recipe : helper.getLevel().getRecipeManager().getAllRecipesFor(type)) {
            if (recipe.data.getInt("ebf_temp") > 5000 && recipe.conditions.isEmpty() &&
                    recipe.getInputContents(FLUID).size() <= 3 &&
                    com.gregtechceu.gtceu.api.recipe.RecipeHelper.getRealEUt(recipe).getTotalEU() <=
                            com.gregtechceu.gtceu.api.GTValues.V[GTNAMultiblockRig.TIER]) {
                hot = recipe;
                break;
            }
        }
        helper.assertTrue(hot != null, definition.getId() + ": no recipe above 5000K to test the coil gate");
        rig.placeIo(casing, hot.getInputContents(ITEM).isEmpty() ? 0 : 2, hot.getOutputContents(ITEM).isEmpty() ? 0 : 2,
                hot.getInputContents(FLUID).size(), hot.getOutputContents(FLUID).size(), false, false);
        rig.form();
        selectType(rig, typeIndex);
        rig.feed(hot, 1);
        helper.assertTrue(!rig.start(40), definition.getId() + " must refuse " + hot.id + " (" +
                hot.data.getInt("ebf_temp") + "K) with 1800K Cupronickel coils");
        helper.succeed();
    }

    /**
     * Guard (G-0208): the GTCEu recipe lookup of every recipe type with recipes must find most of them. A test that
     * re-stages a type with only its own recipe wipes the lookup for every later test (see
     * {@link GTNAGameTestUtils#stageWithRealRecipes}).
     */
    @GameTest(template = "empty_12", timeoutTicks = 100)
    public static void recipeLookupIsNotWiped(GameTestHelper helper) {
        StringBuilder broken = new StringBuilder();
        for (var type : com.gregtechceu.gtceu.api.registry.GTRegistries.RECIPE_TYPES) {
            int total = 0, found = 0;
            for (var recipe : helper.getLevel().getRecipeManager().getAllRecipesFor(type)) {
                total++;
                if (GTNAMultiblockRig.inLookup(recipe)) found++;
            }
            if (total >= 10 && found * 2 < total) {
                broken.append(type.registryName).append(' ').append(found).append('/').append(total).append("; ");
            }
        }
        helper.assertTrue(broken.isEmpty(), "recipe lookup lost most recipes of: " + broken);
        helper.succeed();
    }

    /** Every {@code gtna:mega/*} recipe has only resolvable item and fluid ingredients. */
    @GameTest(template = "empty_12", timeoutTicks = 40)
    public static void megaMachineRecipesHaveNoEmptyIngredient(GameTestHelper helper) {
        List<String> problems = new ArrayList<>();
        int checked = 0;
        for (var recipe : helper.getLevel().getRecipeManager().getRecipes()) {
            if (!(recipe instanceof GTRecipe gt) || !GTNACORE.MOD_ID.equals(gt.id.getNamespace()) ||
                    !gt.id.getPath().contains("mega/"))
                continue;
            checked++;
            for (var content : gt.getInputContents(ItemRecipeCapability.CAP)) {
                var items = ItemRecipeCapability.CAP.of(content.content).getItems();
                if (items.length == 0 || items[0].isEmpty()) problems.add(gt.id.getPath() + " item");
            }
            for (var content : gt.getInputContents(FluidRecipeCapability.CAP)) {
                var fluids = FluidRecipeCapability.CAP.of(content.content).getStacks();
                if (fluids.length == 0 || fluids[0].isEmpty()) problems.add(gt.id.getPath() + " fluid");
            }
        }
        helper.assertTrue(checked >= 31, "expected the 31 mega machine/block recipes, found " + checked);
        helper.assertTrue(problems.isEmpty(), String.join("; ", problems));
        helper.succeed();
    }
}
