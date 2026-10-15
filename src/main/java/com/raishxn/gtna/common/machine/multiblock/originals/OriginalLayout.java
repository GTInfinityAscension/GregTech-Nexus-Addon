package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.block.MetaMachineBlock;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;
import com.gregtechceu.gtceu.api.pattern.TraceabilityPredicate;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;

import com.raishxn.gtna.mixin.gtceu.BlockPatternAccessor;
import it.unimi.dsi.fastutil.longs.Long2IntOpenHashMap;
import org.jetbrains.annotations.Nullable;

import java.util.ArrayList;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;

/**
 * The world positions of an original multiblock's pattern for one placement, with what each position accepts.
 *
 * <p>
 * GTCEu checks a structure by walking its whole pattern through {@code MultiblockState}: about 8 µs per block, so
 * 1.4 s for the 171 000-block lance, repeated on every block change. The originals have fixed aisles, so their
 * layout is computed once per placement (no world reads) and then a single position can be tested on its own, and a
 * full scan reads chunks directly (tens of milliseconds). GTCEu's walk then only runs when the structure is complete
 * and has to form (it collects the parts).
 */
public final class OriginalLayout {

    public enum Kind {
        /** One block. */
        BLOCK,
        /** A moving part or the stellar core: the block, or air while the machine holds it. */
        BLOCK_OR_AIR,
        /** The hatch casing or any machine part. */
        HATCH,
        CONTROLLER
    }

    /** What one letter of the pattern accepts. */
    public record Matcher(char letter, Kind kind, Block block, @Nullable String tag) {

        public boolean test(BlockState state) {
            return switch (kind) {
                case BLOCK -> state.is(block);
                case BLOCK_OR_AIR -> state.is(block) || state.isAir();
                case HATCH -> state.is(block) || state.getBlock() instanceof MetaMachineBlock;
                case CONTROLLER -> true;
            };
        }
    }

    /**
     * Matchers by the simple predicates inside each registered predicate: {@code FactoryBlockPattern.where} stores a
     * copy of the predicate, but the copy holds the same simple predicates. One shared by several letters (air) maps
     * to {@link #SHARED} and is skipped.
     */
    private static final Map<com.gregtechceu.gtceu.api.pattern.predicates.SimplePredicate, Matcher> MATCHERS = new IdentityHashMap<>();
    private static final Matcher SHARED = new Matcher(' ', Kind.CONTROLLER, net.minecraft.world.level.block.Blocks.AIR,
            null);

    /** Called while building an original's pattern, for each predicate it places. */
    public static synchronized TraceabilityPredicate register(TraceabilityPredicate predicate, Matcher matcher) {
        for (var list : List.of(predicate.common, predicate.limited))
            for (var simple : list) MATCHERS.merge(simple, matcher, (a, b) -> a == b ? a : SHARED);
        return predicate;
    }

    @Nullable
    private static Matcher lookup(Map<com.gregtechceu.gtceu.api.pattern.predicates.SimplePredicate, Matcher> known,
                                  TraceabilityPredicate predicate) {
        if (predicate.isAny()) return null;
        for (var list : List.of(predicate.common, predicate.limited))
            for (var simple : list) {
                var m = known.get(simple);
                if (m != null && m != SHARED) return m;
            }
        return null;
    }

    private final long[] positions;
    private final Matcher[] matchers;
    private final Long2IntOpenHashMap index;

    private OriginalLayout(long[] positions, Matcher[] matchers) {
        this.positions = positions;
        this.matchers = matchers;
        this.index = new Long2IntOpenHashMap(positions.length);
        this.index.defaultReturnValue(-1);
        for (int i = 0; i < positions.length; i++) index.put(positions[i], i);
    }

    /** Lays the pattern out at a controller; same position order and offsets as {@code BlockPattern}. */
    public static OriginalLayout of(BlockPattern pattern, BlockPos controller, Direction front, Direction up,
                                    boolean flipped) {
        var access = (BlockPatternAccessor) pattern;
        TraceabilityPredicate[][][] matches = access.gtna$getBlockMatches();
        int[] center = access.gtna$getCenterOffset();
        var pos = new it.unimi.dsi.fastutil.longs.LongArrayList();
        List<Matcher> found = new ArrayList<>();
        Map<com.gregtechceu.gtceu.api.pattern.predicates.SimplePredicate, Matcher> known;
        synchronized (OriginalLayout.class) {
            known = new IdentityHashMap<>(MATCHERS);
        }
        // The originals' aisles never repeat, so aisle c sits at z = -centerOffset[4] + c.
        for (int c = 0, z = -center[4]; c < matches.length; c++, z++) {
            for (int b = 0, y = -center[1]; b < matches[c].length; b++, y++) {
                for (int a = 0, x = -center[0]; a < matches[c][b].length; a++, x++) {
                    Matcher m = lookup(known, matches[c][b][a]);
                    if (m == null) continue;    // any(): not part of the structure
                    BlockPos p = access.gtna$actualRelativeOffset(x, y, z, front, up, flipped).offset(controller);
                    pos.add(p.asLong());
                    found.add(m);
                }
            }
        }
        return new OriginalLayout(pos.toLongArray(), found.toArray(Matcher[]::new));
    }

    public int size() {
        return positions.length;
    }

    public long position(int i) {
        return positions[i];
    }

    /** Index of a world position in the layout, or -1. */
    public int indexOf(long pos) {
        return index.get(pos);
    }

    public Matcher matcher(int i) {
        return matchers[i];
    }

    /** World position -> letter of every part tagged {@code tag}. */
    public Map<BlockPos, Character> tagged(String tag) {
        Map<BlockPos, Character> out = new java.util.LinkedHashMap<>();
        for (int i = 0; i < positions.length; i++)
            if (tag.equals(matchers[i].tag())) out.put(BlockPos.of(positions[i]), matchers[i].letter());
        return out;
    }

    /** Positions of the whole layout, for GTCEu's block-change mapping. */
    public it.unimi.dsi.fastutil.longs.LongOpenHashSet positionSet() {
        return new it.unimi.dsi.fastutil.longs.LongOpenHashSet(positions);
    }

    /**
     * Indices of the positions that do not match, reading loaded chunks directly; null when a chunk of the structure
     * is not loaded (try again later).
     */
    @Nullable
    public it.unimi.dsi.fastutil.ints.IntOpenHashSet mismatches(Level level) {
        var out = new it.unimi.dsi.fastutil.ints.IntOpenHashSet();
        long chunkKey = Long.MIN_VALUE;
        LevelChunk chunk = null;
        var mutable = new BlockPos.MutableBlockPos();
        for (int i = 0; i < positions.length; i++) {
            mutable.set(positions[i]);
            long key = net.minecraft.world.level.ChunkPos.asLong(mutable.getX() >> 4, mutable.getZ() >> 4);
            if (key != chunkKey) {
                chunkKey = key;
                chunk = level.getChunkSource().getChunkNow(mutable.getX() >> 4, mutable.getZ() >> 4);
                if (chunk == null) return null;
            }
            if (!matchers[i].test(chunk.getBlockState(mutable))) out.add(i);
        }
        return out;
    }
}
