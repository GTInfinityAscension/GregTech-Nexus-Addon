package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.FactoryBlockPattern;
import com.gregtechceu.gtceu.api.pattern.MultiblockState;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.registries.ForgeRegistries;

import com.google.common.base.Suppliers;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.raishxn.gtna.common.data.multiblock.GTNAMultiBlockFileReader;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;

import static com.gregtechceu.gtceu.api.pattern.Predicates.any;
import static com.gregtechceu.gtceu.api.pattern.Predicates.controller;

/**
 * Moving parts of an original multiblock: the pattern letters tagged {@code #<tag>} in the JSON sidecar (for example
 * the collider's {@code #ring}). Like the Forge of Gods rings, they are taken out of the world while the machine runs
 * and drawn spinning by the renderer, then put back when it stops. Positions come from walking the .mbs with
 * recording predicates, so they follow the controller's orientation.
 */
public final class CapturedParts {

    private static final Map<String, Supplier<Recorded>> CACHE = new HashMap<>();

    private record Recorded(BlockPattern pattern, Map<Character, Block> blocks, Map<Character, String> tags) {}

    private CapturedParts() {}

    private static Recorded recorded(String name) {
        return CACHE.computeIfAbsent(name, n -> Suppliers.memoize(() -> {
            JsonObject letters = sidecar(n).getAsJsonObject("letters");
            Map<Character, Block> blocks = new HashMap<>();
            Map<Character, String> tags = new HashMap<>();
            FactoryBlockPattern pattern = GTNAMultiBlockFileReader.start(null, n).where('~', controller(any()))
                    .where(' ', any());
            for (var e : letters.entrySet()) {
                char c = e.getKey().charAt(0);
                String[] v = e.getValue().getAsString().split("#");
                if (v.length == 2) {
                    blocks.put(c, ForgeRegistries.BLOCKS.getValue(new ResourceLocation(v[0])));
                    tags.put(c, v[1]);
                    pattern.where(c, recorder(c));
                } else pattern.where(c, any());
            }
            return new Recorded(pattern.build(), blocks, tags);
        })).get();
    }

    private static final ThreadLocal<Map<BlockPos, Character>> SINK = new ThreadLocal<>();

    private static TraceabilityPredicate recorder(char symbol) {
        return new TraceabilityPredicate(state -> {
            var sink = SINK.get();
            if (sink != null) sink.put(state.getPos().immutable(), symbol);
            return true;
        }, null);
    }

    private record Key(String name, String tag, BlockPos controller, Direction front, Direction up,
                       boolean flipped) {}

    /** Walking a 2-million-cell pattern takes seconds; the result only depends on placement, so it is kept. */
    private static final Map<Key, Map<BlockPos, Character>> POSITIONS = new java.util.concurrent.ConcurrentHashMap<>();

    /** World position -> letter of every part tagged {@code tag}. */
    public static Map<BlockPos, Character> positions(Level level, String name, String tag, BlockPos controller,
                                                     Direction front, Direction up, boolean flipped) {
        var key = new Key(name, tag, controller.immutable(), front, up, flipped);
        var cached = POSITIONS.get(key);
        if (cached != null) return cached;
        var walked = walk(level, name, tag, controller, front, up, flipped);
        // An incomplete walk (structure not all there) is not cached; it is returned as found so far.
        if (walked == null) return Map.of();
        var result = java.util.Collections.unmodifiableMap(walked);
        if (POSITIONS.size() > 64) POSITIONS.clear();
        POSITIONS.put(key, result);
        return result;
    }

    private static Map<BlockPos, Character> walk(Level level, String name, String tag, BlockPos controller,
                                                 Direction front, Direction up, boolean flipped) {
        var rec = recorded(name);
        Map<BlockPos, Character> all = new LinkedHashMap<>();
        SINK.set(all);
        boolean complete;
        try {
            complete = rec.pattern().checkPatternAt(new MultiblockState(level, controller), controller, front, up,
                    flipped, false);
        } finally {
            SINK.remove();
        }
        all.values().removeIf(c -> !tag.equals(rec.tags().get(c)));
        return complete ? all : null;
    }

    public static Block blockFor(String name, char letter) {
        return recorded(name).blocks().getOrDefault(letter, Blocks.AIR);
    }

    /** Takes the parts out of the world. */
    public static void capture(Level level, Map<BlockPos, Character> parts) {
        var air = Blocks.AIR.defaultBlockState();
        // Clients are told, but neighbours are not reshaped one by one: the whole part leaves at once.
        for (BlockPos p : parts.keySet()) level.setBlock(p, air, 2 | 16);
    }

    /** Puts the parts back where there is air. */
    public static void release(Level level, String name, Map<BlockPos, Character> parts) {
        for (var e : parts.entrySet())
            if (level.getBlockState(e.getKey()).isAir())
                level.setBlock(e.getKey(), blockFor(name, e.getValue()).defaultBlockState(), 2 | 16);
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
