package com.raishxn.gtna.utils;

import net.minecraft.core.BlockPos;

import it.unimi.dsi.fastutil.longs.LongOpenHashSet;

import java.util.AbstractSet;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

/**
 * Insertion-ordered set of positions for the multiblock preview scene: membership by packed long, iteration over the
 * original objects. Filling it with a whole structure is several times faster than a hash set of {@link BlockPos}.
 *
 * <p>
 * Equality and hash are by identity: LDLib keys a map by this set, and a content hash walks every position on each
 * put.
 */
public final class BlockPosLongSet extends AbstractSet<BlockPos> {

    private LongOpenHashSet keys = new LongOpenHashSet();
    private final ArrayList<BlockPos> order = new ArrayList<>();

    @Override
    public boolean add(BlockPos pos) {
        if (!keys.add(pos.asLong())) return false;
        order.add(pos);
        return true;
    }

    @Override
    public boolean addAll(Collection<? extends BlockPos> c) {
        if (keys.isEmpty()) keys = new LongOpenHashSet(c.size());
        order.ensureCapacity(order.size() + c.size());
        boolean changed = false;
        for (BlockPos pos : c) changed |= add(pos);
        return changed;
    }

    @Override
    public boolean contains(Object o) {
        return o instanceof BlockPos pos && keys.contains(pos.asLong());
    }

    @Override
    public boolean remove(Object o) {
        if (!(o instanceof BlockPos pos) || !keys.remove(pos.asLong())) return false;
        order.remove(pos);
        return true;
    }

    @Override
    public void clear() {
        keys.clear();
        order.clear();
    }

    @Override
    public int size() {
        return order.size();
    }

    @Override
    public Iterator<BlockPos> iterator() {
        var it = order.iterator();
        return new Iterator<>() {

            private BlockPos last;

            @Override
            public boolean hasNext() {
                return it.hasNext();
            }

            @Override
            public BlockPos next() {
                return last = it.next();
            }

            @Override
            public void remove() {
                it.remove();
                keys.remove(last.asLong());
            }
        };
    }

    @Override
    public boolean equals(Object o) {
        return this == o;
    }

    @Override
    public int hashCode() {
        return System.identityHashCode(this);
    }
}
