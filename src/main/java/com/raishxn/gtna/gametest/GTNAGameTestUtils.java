package com.raishxn.gtna.gametest;

import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;

import net.minecraft.gametest.framework.GameTestHelper;

import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;

/**
 * Small helpers for the GameTest harness.
 *
 * <p>
 * Inspired by GTNH's Horizon-QA discipline ({@code onEachTick} + {@code succeedAtTimeout}): re-check
 * an invariant every tick over the whole test window so a <b>transient</b> violation (a machine that
 * forms and unforms, a state that flickers) fails on the exact tick it happens.
 */
public final class GTNAGameTestUtils {

    private GTNAGameTestUtils() {}

    /**
     * Runs {@code assertion} every tick and only marks the test passed near the end of the window, so
     * any violation in between fails the test on that tick. The owning {@code @GameTest} must use a
     * {@code timeoutTicks} greater than {@code timeoutTicks} passed here.
     */
    public static void assertEveryTickUntilTimeout(GameTestHelper helper, int timeoutTicks, String name,
                                                   Runnable assertion) {
        assertion.run();
        helper.onEachTick(() -> {
            try {
                assertion.run();
            } catch (Throwable failure) {
                helper.fail(name + ": " + failure.getMessage());
            }
        });
        helper.runAtTickTime(Math.max(1, timeoutTicks - 1), helper::succeed);
    }

    /** Forces the first structure check, then rejects even a single tick of accidental formation. */
    public static void assertNeverForms(GameTestHelper helper, MultiblockControllerMachine controller,
                                        int observationTicks, String name) {
        GTNAStructureRefresh.refresh(controller, true);
        assertEveryTickUntilTimeout(helper, observationTicks, name,
                () -> helper.assertFalse(controller.isFormed(), "controller formed"));
    }

    /**
     * Adds test-only recipes to a recipe type's lookup without wiping it: GTCEu's {@code completeStaging()} replaces
     * the whole lookup DB, so every real recipe of the type is staged again first. Staging only the test recipe made
     * every later GameTest see an empty Assembler/Bender/Lathe/... lookup (G-0208).
     */
    public static void stageWithRealRecipes(GameTestHelper helper,
                                            com.gregtechceu.gtceu.api.recipe.GTRecipeType type,
                                            com.gregtechceu.gtceu.api.recipe.GTRecipe... extra) {
        stageWithRealRecipes(type, extra);
    }

    /**
     * {@link #stageWithRealRecipes(GameTestHelper, com.gregtechceu.gtceu.api.recipe.GTRecipeType,
     * com.gregtechceu.gtceu.api.recipe.GTRecipe...)} using the running server's recipe manager.
     */
    public static void stageWithRealRecipes(com.gregtechceu.gtceu.api.recipe.GTRecipeType type,
                                            com.gregtechceu.gtceu.api.recipe.GTRecipe... extra) {
        var server = net.minecraftforge.server.ServerLifecycleHooks.getCurrentServer();
        type.getAdditionHandler().beginStaging();
        for (var recipe : server.getRecipeManager().getAllRecipesFor(type)) {
            type.getAdditionHandler().addStaging(recipe);
        }
        for (var recipe : extra) type.getAdditionHandler().addStaging(recipe);
        type.getAdditionHandler().completeStaging();
    }
}
