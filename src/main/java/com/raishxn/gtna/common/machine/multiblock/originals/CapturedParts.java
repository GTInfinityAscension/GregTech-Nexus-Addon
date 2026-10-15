package com.raishxn.gtna.common.machine.multiblock.originals;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.registries.ForgeRegistries;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;

/**
 * Moving parts of an original multiblock: the pattern letters tagged {@code #<tag>} in the JSON sidecar (for example
 * the collider's {@code #ring}). Like the Forge of Gods rings, they are taken out of the world while the machine runs
 * and drawn spinning by the renderer, then put back when it stops. Positions come from walking the .mbs with
 * the pattern's own offsets ({@link OriginalLayout}), so they follow the controller's orientation.
 */
public final class CapturedParts {

    private record Key(String name, String tag, BlockPos controller, Direction front, Direction up,
                       boolean flipped) {}

    /** Positions only depend on placement, so they are kept (the layout is computed without world reads). */
    private static final Map<Key, Map<BlockPos, Character>> POSITIONS = new java.util.concurrent.ConcurrentHashMap<>();

    /** World position -> letter of every part tagged {@code tag}. */
    public static Map<BlockPos, Character> positions(Level level, String name, String tag, BlockPos controller,
                                                     Direction front, Direction up, boolean flipped) {
        return POSITIONS.computeIfAbsent(new Key(name, tag, controller.immutable(), front, up, flipped), k -> {
            if (POSITIONS.size() > 64) POSITIONS.clear();
            var pattern = com.raishxn.gtna.common.data.GTNAOriginals.byName(name).getPatternFactory().get();
            return java.util.Collections.unmodifiableMap(
                    OriginalLayout.of(pattern, k.controller(), front, up, flipped).tagged(tag));
        });
    }

    private static final Map<String, Map<Character, Block>> BLOCKS = new java.util.concurrent.ConcurrentHashMap<>();

    public static Block blockFor(String name, char letter) {
        return BLOCKS.computeIfAbsent(name, n -> {
            Map<Character, Block> out = new HashMap<>();
            for (var e : sidecar(n).getAsJsonObject("letters").entrySet()) {
                String[] v = e.getValue().getAsString().split("#");
                if (v.length == 2) out.put(e.getKey().charAt(0),
                        ForgeRegistries.BLOCKS.getValue(new ResourceLocation(v[0])));
            }
            return out;
        }).getOrDefault(letter, Blocks.AIR);
    }

    /** Takes the parts out of the world. */
    public static void capture(Level level, Map<BlockPos, Character> parts) {
        var air = Blocks.AIR.defaultBlockState();
        for (BlockPos p : parts.keySet()) set(level, p, air);
    }

    /** Puts the parts back where there is air. */
    public static void release(Level level, String name, Map<BlockPos, Character> parts) {
        for (var e : parts.entrySet())
            if (level.getBlockState(e.getKey()).isAir())
                set(level, e.getKey(), blockFor(name, e.getValue()).defaultBlockState());
    }

    /**
     * Sets a plain block (casings and glass, no block entity) straight in its chunk, then queues the light check and
     * tells watching clients, which batch the changes per section. {@code Level.setBlock} would also run Forge's
     * snapshot capture, GTCEu's multiblock hook and the neighbour notifications for each of the 100 000 blocks.
     */
    private static void set(Level level, BlockPos pos, net.minecraft.world.level.block.state.BlockState state) {
        if (!(level instanceof net.minecraft.server.level.ServerLevel server)) {
            level.setBlock(pos, state, 2 | 16);
            return;
        }
        var chunk = server.getChunkAt(pos);
        var old = chunk.setBlockState(pos, state, false);
        if (old == null || old == state) return;
        server.getChunkSource().getLightEngine().checkBlock(pos);
        server.getChunkSource().blockChanged(pos);
        chunk.setUnsaved(true);
    }

    private static JsonObject sidecar(String name) {
        try (var in = CapturedParts.class.getClassLoader().getResourceAsStream("pattern/" + name + ".json")) {
            if (in == null) throw new IllegalStateException("Missing pattern/" + name + ".json");
            return JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject();
        } catch (java.io.IOException e) {
            throw new RuntimeException(e);
        }
    }
}
