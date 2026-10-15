package com.raishxn.gtna.client.debug;

import com.gregtechceu.gtceu.api.gui.widget.PatternPreviewWidget;
import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;

import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraftforge.client.event.RegisterClientCommandsEvent;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNAOriginals;

/**
 * {@code /gtna_preview_bench}: builds the multiblock-info preview of each original multiblock and logs how long the
 * shape and the widget take, the same work EMI/JEI do when the page opens.
 */
public final class PreviewBenchCommand {

    private PreviewBenchCommand() {}

    private static void devBuild(net.minecraft.server.MinecraftServer server, java.util.UUID uuid,
                                 net.minecraft.resources.ResourceLocation id) {
        var player = server.getPlayerList().getPlayer(uuid);
        var block = net.minecraftforge.registries.ForgeRegistries.BLOCKS.getValue(id);
        if (player == null || block == null) return;
        var level = player.serverLevel();
        var facing = player.getDirection();
        var pos = player.blockPosition().relative(facing, 8);
        var state = block.defaultBlockState();
        var prop = state.getBlock().getStateDefinition().getProperty("facing");
        if (prop instanceof net.minecraft.world.level.block.state.properties.DirectionProperty dir &&
                dir.getPossibleValues().contains(facing.getOpposite()))
            state = state.setValue(dir, facing.getOpposite());
        level.setBlock(pos, state, 3);
        if (!(com.gregtechceu.gtceu.api.machine.MetaMachine.getMachine(level,
                pos) instanceof com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController controller))
            return;
        var terminal = new net.minecraft.world.item.ItemStack(
                com.raishxn.gtna.common.data.GTNAItems.NEXUS_STRUCTURE_TERMINAL.get());
        long t0 = System.nanoTime();
        com.raishxn.gtna.common.item.terminal.NexusAutoBuilder.autoBuild(player, controller, terminal);
        GTNACORE.LOGGER.info("[GTNA perf] dev build {} at {}: {} ms", id, pos, (System.nanoTime() - t0) / 1_000_000);
    }

    private static int starPreview(boolean hole) {
        var player = net.minecraft.client.Minecraft.getInstance().player;
        if (player == null) return 0;
        com.raishxn.gtna.client.renderer.machine.StellarChamberRenderer.debugCenter = player.getEyePosition()
                .add(player.getLookAngle().scale(40));
        com.raishxn.gtna.client.renderer.machine.StellarChamberRenderer.debugHole = hole;
        return 1;
    }

    public static void register(RegisterClientCommandsEvent event) {
        // /gtna_material_sheet <page>: every GTNA material item in a grid, to check item effects.
        event.getDispatcher().register(Commands.literal("gtna_material_sheet").then(Commands
                .argument("page", com.mojang.brigadier.arguments.IntegerArgumentType.integer(0)).executes(ctx -> {
                    int page = com.mojang.brigadier.arguments.IntegerArgumentType.getInteger(ctx, "page");
                    var mc = net.minecraft.client.Minecraft.getInstance();
                    mc.tell(() -> mc.setScreen(new MaterialSheetScreen(page)));
                    return 1;
                })));
        // /gtna_rift_preview [off]: the Dimensional Rift Gate's horizon, 60 blocks ahead.
        event.getDispatcher().register(Commands.literal("gtna_rift_preview").executes(ctx -> {
            var player = net.minecraft.client.Minecraft.getInstance().player;
            if (player == null) return 0;
            com.raishxn.gtna.client.renderer.machine.OriginalsRenderer.debugRift = player.getEyePosition()
                    .add(0, 0, 60);
            return 1;
        }).then(Commands.literal("off").executes(ctx -> {
            com.raishxn.gtna.client.renderer.machine.OriginalsRenderer.debugRift = null;
            return 1;
        })));
        // /gtna_dev_build <machine id>: places the controller 8 blocks ahead and runs the Nexus Terminal auto-build
        // as the player (singleplayer only), to reproduce build-time stalls.
        event.getDispatcher().register(Commands.literal("gtna_dev_build").then(Commands
                .argument("id", com.mojang.brigadier.arguments.StringArgumentType.word()).executes(ctx -> {
                    var mc = net.minecraft.client.Minecraft.getInstance();
                    var server = mc.getSingleplayerServer();
                    if (server == null || mc.player == null) return 0;
                    var id = GTNACORE.id(com.mojang.brigadier.arguments.StringArgumentType.getString(ctx, "id"));
                    var uuid = mc.player.getUUID();
                    server.execute(() -> devBuild(server, uuid, id));
                    return 1;
                })));
        // /gtna_preview_open <machine id>: opens the JEI page of the multiblock (what players see), for timing.
        event.getDispatcher().register(Commands.literal("gtna_preview_open").then(Commands
                .argument("id", com.mojang.brigadier.arguments.StringArgumentType.word()).executes(ctx -> {
                    var id = com.raishxn.gtna.GTNACORE.id(com.mojang.brigadier.arguments.StringArgumentType
                            .getString(ctx, "id"));
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
        // /gtna_star_preview [hole]: a free-standing Stellar Chamber star 40 blocks ahead, to look at the render.
        event.getDispatcher().register(Commands.literal("gtna_star_preview").executes(ctx -> starPreview(false))
                .then(Commands.literal("hole").executes(ctx -> starPreview(true)))
                .then(Commands.literal("nolens").executes(ctx -> {
                    com.raishxn.gtna.client.renderer.machine.StellarChamberRenderer.debugNoLens ^= true;
                    return 1;
                }))
                .then(Commands.literal("off").executes(ctx -> {
                    com.raishxn.gtna.client.renderer.machine.StellarChamberRenderer.debugCenter = null;
                    return 1;
                })));
        event.getDispatcher().register(Commands.literal("gtna_preview_bench").executes(ctx -> {
            for (var d : new MultiblockMachineDefinition[] { GTNAOriginals.STELLAR_CONTAINMENT_CHAMBER,
                    GTNAOriginals.ANTIMATTER_COLLIDER_RING, GTNAOriginals.DIMENSIONAL_RIFT_GATE,
                    GTNAOriginals.KINETIC_ORBITAL_LANCE }) {
                long t0 = System.nanoTime();
                int shapes = d.getMatchingShapes().size();
                long shapeMs = (System.nanoTime() - t0) / 1_000_000;
                t0 = System.nanoTime();
                PatternPreviewWidget.getPatternWidget(d);
                long widgetMs = (System.nanoTime() - t0) / 1_000_000;
                String line = String.format("[GTNA perf] preview %s: %d shapes in %d ms, widget %d ms", d.getId(),
                        shapes, shapeMs, widgetMs);
                GTNACORE.LOGGER.info(line);
                ctx.getSource().sendSuccess(() -> Component.literal(line), false);
            }
            return 1;
        }));
    }
}
