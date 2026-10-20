package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;

import net.minecraft.core.BlockPos;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNABlocks;
import com.raishxn.gtna.common.data.GTNANaquadahReactors;
import com.raishxn.gtna.common.machine.multiblock.electric.HyperReactorMachine;

/** The naquadah reactor ladder: both reactors form, break when a block is missing, and the HyperReactor is better. */
@GameTestHolder(GTNACORE.MOD_ID)
@PrefixGameTestTemplate(false)
public final class GTNANaquadahReactorGameTests {

    private GTNANaquadahReactorGameTests() {}

    /** Places the first preview of {@code definition}; the HyperReactor is larger than any template. */
    private static IMultiController build(GameTestHelper helper, MultiblockMachineDefinition definition) {
        var shape = definition.getMatchingShapes().get(0).getBlocks();
        IMultiController controller = null;
        for (int x = 0; x < shape.length; x++) {
            for (int y = 0; y < shape[x].length; y++) {
                for (int z = 0; z < shape[x][y].length; z++) {
                    var info = shape[x][y][z];
                    if (info == null || info.getBlockState().isAir()) continue;
                    var pos = new BlockPos(x, y + 2, z);
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

    /** Forms from the preview, then fails after one block of {@code block} is removed. */
    private static void formsAndBreaks(GameTestHelper helper, MultiblockMachineDefinition definition,
                                       net.minecraft.world.level.block.Block block) {
        var controller = build(helper, definition);
        helper.assertTrue(controller != null, definition.getId() + ": the preview has no controller");
        helper.assertTrue(controller.checkPatternWithLock(), definition.getId() + " must form from its preview: " +
                controller.getMultiblockState().error);
        BlockPos removed = null;
        for (BlockPos pos : controller.getMultiblockState().getCache()) {
            if (helper.getLevel().getBlockState(pos).is(block)) {
                removed = pos;
                break;
            }
        }
        helper.assertTrue(removed != null, definition.getId() + ": no " + block + " in the structure");
        helper.getLevel().setBlockAndUpdate(removed, Blocks.AIR.defaultBlockState());
        helper.assertTrue(!controller.checkPatternWithLock(),
                definition.getId() + " must not form with a missing block");
        helper.succeed();
    }

    @GameTest(template = "empty_48", timeoutTicks = 400, batch = "gtna_naquadah")
    public static void largeNaquadahReactorFormsAndBreaks(GameTestHelper helper) {
        formsAndBreaks(helper, GTNANaquadahReactors.LARGE_NAQUADAH_REACTOR,
                GTNANaquadahReactors.EXTREME_STRENGTH_TRITANIUM_CASING.get());
    }

    @GameTest(template = "empty_16", timeoutTicks = 1200, batch = "gtna_naquadah")
    public static void naquadahHyperReactorFormsAndBreaks(GameTestHelper helper) {
        formsAndBreaks(helper, GTNANaquadahReactors.NAQUADAH_HYPER_REACTOR,
                GTNABlocks.NAQUADAH_BOROSILICATE_GLASS.get());
    }

    private static GTRecipe recipe(GameTestHelper helper, String path) {
        return helper.getLevel().getRecipeManager().byKey(new ResourceLocation(GTNACORE.MOD_ID, path))
                .filter(r -> r instanceof GTRecipe).map(r -> (GTRecipe) r).orElse(null);
    }

    /** Same fuel and duration, four times the power, and the boosters only on the HyperReactor. */
    @GameTest(template = "empty_16", timeoutTicks = 20, batch = "gtna_naquadah")
    public static void hyperReactorIsTheBestNaquadahReactor(GameTestHelper helper) {
        var large = recipe(helper, "large_naquadah_reactor/naquadah_fuel");
        var hyper = recipe(helper, "naquadah_hyper_reactor/naquadah_fuel");
        helper.assertTrue(large != null && hyper != null, "both naquadah fuel recipes must load");
        long largeEu = large.getOutputEUt().getTotalEU() * large.duration;
        long hyperEu = hyper.getOutputEUt().getTotalEU() * hyper.duration;
        helper.assertTrue(hyperEu == 4 * largeEu, "the HyperReactor gives 4x EU per mB: " + hyperEu + " vs " +
                largeEu);
        helper.assertTrue(hyper.data.getList(HyperReactorMachine.BOOSTERS, 10).size() == 2,
                "the HyperReactor recipe carries the oxygen and nitrogen plasma boosters");
        helper.succeed();
    }
}
