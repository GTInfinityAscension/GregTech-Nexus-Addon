package com.raishxn.gtna.client.debug;

import net.minecraft.commands.Commands;
import net.minecraftforge.client.event.RegisterClientCommandsEvent;

import com.raishxn.gtna.GTNACORE;

/** {@code /gtna_preview_open <machine id>}: opens the JEI page of a multiblock, for timing. Loaded only with JEI. */
final class JeiPreviewOpen {

    private JeiPreviewOpen() {}

    static void register(RegisterClientCommandsEvent event) {
        event.getDispatcher().register(Commands.literal("gtna_preview_open").then(Commands
                .argument("id", com.mojang.brigadier.arguments.StringArgumentType.word()).executes(ctx -> {
                    var id = GTNACORE.id(com.mojang.brigadier.arguments.StringArgumentType.getString(ctx, "id"));
                    var item = net.minecraftforge.registries.ForgeRegistries.ITEMS.getValue(id);
                    var runtime = com.raishxn.gtna.integration.jei.EyeOfHarmonyJEIPlugin.runtime;
                    if (item == null || runtime == null) return 0;
                    long t0 = System.nanoTime();
                    var focus = runtime.getJeiHelpers().getFocusFactory().createFocus(
                            mezz.jei.api.recipe.RecipeIngredientRole.OUTPUT,
                            mezz.jei.api.constants.VanillaTypes.ITEM_STACK,
                            new net.minecraft.world.item.ItemStack(item));
                    runtime.getRecipesGui().show(focus);
                    GTNACORE.LOGGER.info("[GTNA perf] JEI page for {} opened in {} ms", id,
                            (System.nanoTime() - t0) / 1_000_000);
                    return 1;
                })));
    }
}
