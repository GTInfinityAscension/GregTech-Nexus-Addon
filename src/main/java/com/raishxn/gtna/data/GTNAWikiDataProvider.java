package com.raishxn.gtna.data;

import com.gregtechceu.gtceu.api.machine.MultiblockMachineDefinition;
import com.gregtechceu.gtceu.api.registry.GTRegistries;

import com.lowdragmc.lowdraglib.utils.BlockInfo;

import net.minecraft.data.CachedOutput;
import net.minecraft.data.DataProvider;
import net.minecraft.data.PackOutput;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.registries.ForgeRegistries;

import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.raishxn.gtna.GTNACORE;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

/**
 * Writes {@code build/wiki/multiblocks.json}: every GTNA multiblock with its recipe types and the smallest
 * preview of its structure. {@code tools/wiki/generate_machine_pages.py} turns it into the wiki pages. The file
 * stays outside the generated resources, so nothing of it ships in the jar.
 */
public class GTNAWikiDataProvider implements DataProvider {

    private final Path out;

    public GTNAWikiDataProvider(PackOutput output) {
        // src/generated/resources -> project root
        this.out = output.getOutputFolder().toAbsolutePath().getParent().getParent().getParent()
                .resolve("build/wiki/multiblocks.json");
    }

    @Override
    public CompletableFuture<?> run(CachedOutput cache) {
        var root = new JsonArray();
        for (var definition : GTRegistries.MACHINES) {
            if (!(definition instanceof MultiblockMachineDefinition multi) ||
                    !definition.getId().getNamespace().equals(GTNACORE.MOD_ID))
                continue;
            var machine = new JsonObject();
            machine.addProperty("id", definition.getId().getPath());
            var types = new JsonArray();
            for (var type : definition.getRecipeTypes()) types.add(type.registryName.toString());
            machine.add("recipeTypes", types);
            machine.addProperty("generator", multi.isGenerator());
            try {
                machine.add("shape", shape(multi));
            } catch (Throwable error) {
                machine.addProperty("shapeError", String.valueOf(error));
            }
            root.add(machine);
        }
        try {
            Files.createDirectories(out.getParent());
            Files.writeString(out, new GsonBuilder().setPrettyPrinting().create().toJson(root));
        } catch (IOException e) {
            return CompletableFuture.failedFuture(e);
        }
        return CompletableFuture.completedFuture(null);
    }

    /** Smallest preview: the explicit designs when present, otherwise the minimum aisle repetitions. */
    private static JsonObject shape(MultiblockMachineDefinition multi) {
        BlockInfo[][][] blocks;
        var designs = multi.getShapes() == null ? null : multi.getShapes().get();
        if (designs != null && !designs.isEmpty()) blocks = designs.get(0).getBlocks();
        else {
            var pattern = multi.getPatternFactory().get();
            int[] minimum = new int[pattern.aisleRepetitions.length];
            for (int i = 0; i < minimum.length; i++) minimum[i] = pattern.aisleRepetitions[i][0];
            blocks = pattern.getPreview(minimum);
        }
        Map<String, Integer> palette = new HashMap<>();
        var paletteJson = new JsonArray();
        var layers = new JsonArray();
        for (var aisle : blocks) {
            var rows = new JsonArray();
            for (var row : aisle) {
                var cells = new JsonArray();
                for (var info : row) {
                    BlockState state = info == null ? null : info.getBlockState();
                    if (state == null || state.isAir()) {
                        cells.add(-1);
                        continue;
                    }
                    String id = String.valueOf(ForgeRegistries.BLOCKS.getKey(state.getBlock()));
                    cells.add(palette.computeIfAbsent(id, key -> {
                        paletteJson.add(key);
                        return palette.size();
                    }));
                }
                rows.add(cells);
            }
            layers.add(rows);
        }
        var shape = new JsonObject();
        shape.add("palette", paletteJson);
        shape.add("blocks", layers);
        return shape;
    }

    @Override
    public String getName() {
        return "GTNA wiki data";
    }
}
