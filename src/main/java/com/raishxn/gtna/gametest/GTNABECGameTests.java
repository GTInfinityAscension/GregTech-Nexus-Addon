package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.bec.*;
import com.raishxn.gtna.common.data.GTNABEC;
import com.raishxn.gtna.common.data.GTNARecipeType;
import com.raishxn.gtna.common.machine.multiblock.electric.bec.BECIONodeMachine;

import java.util.*;

/** GTNH Bose-Einstein Condensate port: recipes, structures, network routing and the node's nanite steps. */
@PrefixGameTestTemplate(false)
@GameTestHolder("gtna")
public final class GTNABECGameTests {

    private GTNABECGameTests() {}

    /** One generator recipe per condensate type, and every BEC assembler recipe carries one nanite per item slot. */
    @GameTest(template = "empty_12", timeoutTicks = 40)
    public static void becRecipesAreRegistered(GameTestHelper helper) {
        var manager = helper.getLevel().getRecipeManager();
        var generators = manager.getAllRecipesFor(GTNARecipeType.CONDENSATE_GENERATOR_RECIPES);
        helper.assertTrue(generators.size() == CondensateType.VALUES.length,
                "19 condensate generator recipes, got " + generators.size());
        var assembler = manager.getAllRecipesFor(GTNARecipeType.CONDENSATE_ASSEMBLER_RECIPES);
        Set<String> wanted = new HashSet<>(List.of("transdimensional_alignment_matrix",
                "singularity_shielding_casing", "central_graviton_flow_modulator", "astral_array_fabricator",
                "stabilisation_field_generator_8", "metamaterial_field_manipulator_4",
                "electromagnetically_isolated_casing", "electromagnetic_waveguide"));
        for (GTRecipe recipe : assembler) {
            wanted.removeIf(id -> recipe.id.getPath().endsWith("bec/" + id));
            int[] tiers = BECIONodeMachine.nanitesOf(recipe.data);
            int items = recipe.getInputContents(com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability.CAP)
                    .size();
            helper.assertTrue(tiers.length > 0, recipe.id + " has no nanite tiers");
            helper.assertTrue(tiers.length == items,
                    recipe.id + ": " + tiers.length + " nanite tiers for " + items + " item inputs");
            for (var content : recipe.getInputContents(FluidRecipeCapability.CAP)) {
                Fluid fluid = FluidRecipeCapability.CAP.of(content.content).getStacks()[0].getFluid();
                helper.assertTrue(CondensateType.getCondensateType(fluid) != null,
                        recipe.id + " uses a fluid that is not a condensate: " + fluid);
            }
        }
        helper.assertTrue(wanted.isEmpty(), "missing BEC recipes: " + wanted);
        for (var recipe : manager.getRecipes()) {
            if (recipe instanceof GTRecipe gt && GTNACORE.MOD_ID.equals(gt.id.getNamespace())) {
                helper.assertFalse(gt.id.getPath().equals("godforge_chain/singularity_shielding_casing"),
                        "the provisional G-0199 shielding assembly line must be gone");
            }
        }
        helper.succeed();
    }

    /** GTNH {@code IntDivisionIterator}: the steps cover the whole duration in near-equal parts. */
    @GameTest(template = "empty_12", timeoutTicks = 40)
    public static void nodeStepsSplitTheDuration(GameTestHelper helper) {
        var steps = BECIONodeMachine.steps(100, new int[] { 0, 2, 4 });
        helper.assertTrue(steps.size() == 3, "three steps");
        helper.assertTrue(steps.get(0).start() == 0 && steps.get(2).end() == 100, "covers 0..100");
        helper.assertTrue(steps.get(0).end() == steps.get(1).start() && steps.get(1).end() == steps.get(2).start(),
                "contiguous");
        int[] lengths = { steps.get(0).end(), steps.get(1).end() - steps.get(1).start(),
                steps.get(2).end() - steps.get(2).start() };
        helper.assertTrue(Arrays.stream(lengths).max().getAsInt() - Arrays.stream(lengths).min().getAsInt() <= 1,
                "near-equal: " + Arrays.toString(lengths));
        helper.assertTrue(steps.get(1).nanite() == NaniteTier.Silver, "second step is Silver (ordinal 2)");
        helper.succeed();
    }

    private static final class StubNode implements IBECNode, BECInventory {

        final Level level;
        final double capacity;
        final CondensateList contents = new CondensateList();
        Fluid onlyFluid;

        StubNode(Level level, double capacity) {
            this.level = level;
            this.capacity = capacity;
        }

        @Override
        public Level getBECLevel() {
            return level;
        }

        @Override
        public boolean isBECFormed() {
            return true;
        }

        @Override
        public List<? extends IBECHatch> getBECHatches() {
            return List.of();
        }

        @Override
        public boolean allowsCondensateThrough(Fluid condensate) {
            return onlyFluid == null || onlyFluid == condensate;
        }

        @Override
        public CondensateList getContents() {
            return contents;
        }

        @Override
        public double getCondensateCapacity() {
            return capacity;
        }

        @Override
        public void addCondensate(CondensateStack request) {
            contents.addTo(request.fluid, request.amount);
            request.amount = 0;
        }

        @Override
        public boolean removeCondensate(CondensateStack request) {
            long have = contents.getLong(request.fluid);
            long taken = Math.min(have, request.amount);
            request.amount -= taken;
            if (have - taken == 0) contents.removeLong(request.fluid);
            else contents.put(request.fluid, have - taken);
            return request.amount == 0;
        }
    }

    /**
     * GTNH {@code BECFactoryNetwork}: injection splits by capacity, draining walks nearest first, a node that refuses
     * a condensate is not stepped through, and unrequested condensates count as slowdowns.
     */
    @GameTest(template = "empty_12", timeoutTicks = 40)
    public static void networkSplitsDrainsAndFilters(GameTestHelper helper) {
        Level level = helper.getLevel();
        Fluid neutronium = CondensateType.Neutronium.getEntangledFluid();
        Fluid infinity = CondensateType.Infinity.getEntangledFluid();
        StubNode source = new StubNode(level, 0);
        StubNode small = new StubNode(level, 100);
        StubNode big = new StubNode(level, 300);
        StubNode gate = new StubNode(level, 0);
        StubNode behindGate = new StubNode(level, 100);
        gate.onlyFluid = neutronium;
        Set<IBECNode> all = new LinkedHashSet<>(List.of(source, small, big, gate, behindGate));
        BECNetwork.invalidate();
        BECNetwork.putTestEdges(source, List.of(small, big, gate), 1, all);
        BECNetwork.putTestEdges(gate, List.of(behindGate), 1, all);
        BECNetwork.putTestEdges(small, List.of(), 1, all);
        BECNetwork.putTestEdges(big, List.of(), 1, all);
        BECNetwork.putTestEdges(behindGate, List.of(), 1, all);

        BECNetwork.inject(source, new CondensateStack(infinity, 400));
        helper.assertTrue(small.contents.getLong(infinity) == 100 && big.contents.getLong(infinity) == 300,
                "split 100/300 by capacity, got " + small.contents + " / " + big.contents);
        helper.assertTrue(behindGate.contents.isEmpty(), "the gate keeps Infinity out");

        BECNetwork.inject(source, new CondensateStack(neutronium, 500));
        helper.assertTrue(behindGate.contents.getLong(neutronium) > 0, "Neutronium passes the gate");

        CondensateStack request = new CondensateStack(infinity, 150);
        BECNetwork.drain(source, request);
        helper.assertTrue(request.amount == 0, "drained all 150");
        helper.assertTrue(BECNetwork.stored(source, infinity) == 250, "250 Infinity left");

        int slowdowns = BECNetwork.slowdowns(source, List.of(infinity));
        helper.assertTrue(slowdowns == 1, "Neutronium is one unrequested condensate, got " + slowdowns);
        BECNetwork.invalidate();
        helper.succeed();
    }

    private static MultiblockControllerMachine buildPreview(GameTestHelper helper, MultiblockMachineDefinition def) {
        var shape = def.getMatchingShapes().get(0).getBlocks();
        MultiblockControllerMachine machine = null;
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
                    if (info.getBlockState().is(def.getBlock())) {
                        machine = (MultiblockControllerMachine) ((IMachineBlockEntity) helper.getBlockEntity(pos))
                                .getMetaMachine();
                    }
                }
            }
        }
        helper.assertTrue(machine != null, def.getId() + ": the preview has a controller");
        return machine;
    }

    private static void formsFromPreview(GameTestHelper helper, MultiblockMachineDefinition def) {
        var machine = buildPreview(helper, def);
        helper.assertTrue(machine.checkPatternWithLock(),
                def.getId() + " must form: " + machine.getMultiblockState().error);
        helper.succeed();
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void becGeneratorFormsFromPreview(GameTestHelper helper) {
        formsFromPreview(helper, GTNABEC.BEC_GENERATOR);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void becStorageFormsFromPreview(GameTestHelper helper) {
        formsFromPreview(helper, GTNABEC.BEC_STORAGE);
    }

    @GameTest(template = "empty_80", timeoutTicks = 600)
    public static void becAssemblerFormsFromPreview(GameTestHelper helper) {
        formsFromPreview(helper, GTNABEC.BEC_ASSEMBLER);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void becIONodeFormsFromPreview(GameTestHelper helper) {
        formsFromPreview(helper, GTNABEC.BEC_IO_NODE);
    }

    @GameTest(template = "empty_48", timeoutTicks = 400)
    public static void becDiodeFormsFromPreview(GameTestHelper helper) {
        formsFromPreview(helper, GTNABEC.BEC_DIODE);
    }
}
