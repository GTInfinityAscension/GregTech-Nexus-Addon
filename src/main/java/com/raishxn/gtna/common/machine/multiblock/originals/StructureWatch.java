package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.machine.multiblock.MultiblockControllerMachine;
import com.gregtechceu.gtceu.api.pattern.MultiblockWorldSavedData;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.block.state.BlockState;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;
import it.unimi.dsi.fastutil.ints.IntOpenHashSet;
import org.jetbrains.annotations.Nullable;

/**
 * Structure checks of the original multiblocks, incremental instead of GTCEu's full walks.
 *
 * <p>
 * GTCEu re-walks a whole pattern on every block change inside a formed structure, and every second on its async
 * thread while unformed; each block that thread reads becomes a task on the server thread. For the originals (the
 * lance is 171 000 blocks, 1.4 s a walk) that froze the game on any break and kept server and client lagging while
 * the machine was broken. Here:
 * <ul>
 * <li>the pattern is laid out once per placement ({@link OriginalLayout});</li>
 * <li>a block change tests only that position: a wrong block breaks the structure at once, a right one changes
 * nothing; only a change on a hatch position re-forms (the parts list has to be rebuilt);</li>
 * <li>while broken, the set of wrong positions is kept up to date the same way, and GTCEu's walk runs once, when
 * the set becomes empty, to form the machine;</li>
 * <li>the set is built by one direct chunk scan on load, when the controller screen opens, or after a break.</li>
 * </ul>
 * Everything runs on the server thread; nothing is polled.
 */
public final class StructureWatch {

    /** Machines whose structure checks go through a {@link StructureWatch}. */
    public interface Host {

        StructureWatch structureWatch();
    }

    private final MultiblockControllerMachine machine;
    @Nullable
    private OriginalLayout layout;
    @Nullable
    private BlockPos layoutPos;
    @Nullable
    private Direction layoutFront, layoutUp;
    private boolean layoutFlip;
    /** Wrong positions while unformed; null until scanned. */
    @Nullable
    private IntOpenHashSet missing;
    private boolean scanQueued, formQueued, refreshQueued;
    private long nextScan;

    public StructureWatch(MultiblockControllerMachine machine) {
        this.machine = machine;
    }

    /** The layout at the controller's current placement. */
    public OriginalLayout layout() {
        var pos = machine.getPos();
        if (layout == null || !pos.equals(layoutPos) || machine.getFrontFacing() != layoutFront ||
                machine.getUpwardsFacing() != layoutUp || machine.isFlipped() != layoutFlip) {
            layoutPos = pos.immutable();
            layoutFront = machine.getFrontFacing();
            layoutUp = machine.getUpwardsFacing();
            layoutFlip = machine.isFlipped();
            long t0 = System.nanoTime();
            layout = OriginalLayout.of(machine.getPattern(), layoutPos, layoutFront, layoutUp, layoutFlip);
            GTNACORE.LOGGER.info("[GTNA perf] layout of {} at {}: {} blocks in {} ms",
                    machine.getDefinition().getId(), layoutPos, layout.size(), (System.nanoTime() - t0) / 1_000_000);
            missing = null;
        }
        return layout;
    }

    /** Whether the layout resolved; if not (a pattern this code does not understand), GTCEu's checks stay. */
    public boolean usable() {
        return layout().size() > 0;
    }

    // ------------------------------------------------------------------ events

    /** A block of the structure changed (server thread, from GTCEu's block-change hook). */
    public void blockChanged(BlockPos pos, BlockState state) {
        var layout = layout();
        int i = layout.indexOf(pos.asLong());
        if (i < 0) return;
        var matcher = layout.matcher(i);
        boolean ok = matcher.test(state);
        if (machine.isFormed()) {
            if (!ok) {
                missing = new IntOpenHashSet();
                missing.add(i);
                machine.onStructureInvalid();
                watch();
            } else if (matcher.kind() == OriginalLayout.Kind.HATCH) {
                queueRefresh();   // a hatch came or went: GTCEu has to collect the parts again
            }
            return;
        }
        if (missing == null) {
            queueScan();
            return;
        }
        if (ok) missing.remove(i);
        else missing.add(i);
        if (missing.isEmpty()) queueForm();
    }

    /** {@code onStructureInvalid} from any cause (e.g. GTCEu's own refresh): keep watching the shape. */
    public void invalid() {
        if (missing == null) queueScan();
    }

    /** {@code onStructureFormed}. */
    public void formed() {
        missing = null;
    }

    /** GTCEu's async poll of unformed machines: only ever turns into one scan on the server thread. */
    public void poll() {
        if (missing == null && System.currentTimeMillis() >= nextScan) queueScan();
    }

    /** The controller screen opens. */
    public void opened() {
        if (!machine.isFormed()) {
            missing = null;
            queueScan();
        }
    }

    // ------------------------------------------------------------------ work on the server thread

    private void queueScan() {
        if (scanQueued || !(machine.getLevel() instanceof ServerLevel level)) return;
        scanQueued = true;
        level.getServer().execute(() -> {
            scanQueued = false;
            scan();
        });
    }

    private void queueForm() {
        if (formQueued || !(machine.getLevel() instanceof ServerLevel level)) return;
        formQueued = true;
        level.getServer().execute(() -> {
            formQueued = false;
            form();
        });
    }

    private void queueRefresh() {
        if (refreshQueued || !(machine.getLevel() instanceof ServerLevel level)) return;
        refreshQueued = true;
        level.getServer().execute(() -> {
            refreshQueued = false;
            if (!machine.isInValid() && machine.isFormed() && !GTNAStructureRefresh.refresh(machine, true)) {
                missing = null;
                queueScan();
            }
        });
    }

    private void scan() {
        if (machine.isInValid() || machine.isFormed() || !(machine.getLevel() instanceof ServerLevel level)) return;
        long t0 = System.nanoTime();
        var found = layout().mismatches(level);
        if (found == null) {
            // Part of the structure is not loaded yet: the next poll tries again.
            nextScan = System.currentTimeMillis() + 2000;
            missing = null;
            return;
        }
        missing = found;
        GTNACORE.LOGGER.info("[GTNA perf] scan of {}: {} wrong of {} in {} ms", machine.getDefinition().getId(),
                found.size(), layout().size(), (System.nanoTime() - t0) / 1_000_000);
        if (missing.isEmpty()) form();
        else watch();
    }

    private void form() {
        if (machine.isInValid() || machine.isFormed()) return;
        if (GTNAStructureRefresh.refresh(machine, false)) return;
        // Every block is right but GTCEu disagrees (part limits, a shared part): wait for the next change.
        watch();
    }

    /** Puts the whole layout on GTCEu's block-change mapping and takes the machine off the async poll. */
    private void watch() {
        if (!(machine.getLevel() instanceof ServerLevel level)) return;
        var state = machine.getMultiblockState();
        var data = MultiblockWorldSavedData.getOrCreate(level);
        data.removeMapping(state);
        state.cache = layout().positionSet();
        data.addMapping(state);
        data.removeAsyncLogic(machine);
    }
}
