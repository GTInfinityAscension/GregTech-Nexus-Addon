package com.raishxn.gtna.utils;

import net.minecraft.core.BlockPos;

import it.unimi.dsi.fastutil.Hash;
import it.unimi.dsi.fastutil.HashCommon;
import it.unimi.dsi.fastutil.objects.Object2ObjectLinkedOpenCustomHashMap;
import it.unimi.dsi.fastutil.objects.ObjectLinkedOpenCustomHashSet;

/**
 * Hash collections for large sets of {@link BlockPos}. Vanilla's {@code Vec3i.hashCode} is
 * {@code (y + z * 31) * 31 + x}, so neighbouring positions of a big structure share hash codes by the thousand and a
 * {@code HashMap} degrades into tree bins: the 300k-block previews of GTNA's largest multiblocks spent seconds in
 * them. These hash the packed {@code asLong()} with a full avalanche mix instead.
 */
public final class BlockPosHashing {

    public static final Hash.Strategy<BlockPos> STRATEGY = new Hash.Strategy<>() {

        @Override
        public int hashCode(BlockPos pos) {
            return pos == null ? 0 : (int) HashCommon.mix(pos.asLong());
        }

        @Override
        public boolean equals(BlockPos a, BlockPos b) {
            return a == b || a != null && a.equals(b);
        }
    };

    private BlockPosHashing() {}

    public static ObjectLinkedOpenCustomHashSet<BlockPos> newSet() {
        return new ObjectLinkedOpenCustomHashSet<>(STRATEGY);
    }

    public static <V> Object2ObjectLinkedOpenCustomHashMap<BlockPos, V> newMap() {
        return new Object2ObjectLinkedOpenCustomHashMap<>(STRATEGY);
    }
}
