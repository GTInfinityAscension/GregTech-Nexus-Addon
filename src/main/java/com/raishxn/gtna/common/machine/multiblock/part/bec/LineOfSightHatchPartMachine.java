package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;
import com.gregtechceu.gtceu.api.machine.feature.multiblock.IMultiController;
import com.gregtechceu.gtceu.api.machine.multiblock.part.MultiblockPartMachine;

import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.annotation.RequireRerender;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.level.Level;

import org.jetbrains.annotations.Nullable;

/**
 * GTNH {@code MTEHatchLoS} (Line-Of-Sight Connector Hatch): pairs with another connector up to {@value #SCAN_DIST}
 * blocks in front of it that faces back, through transparent blocks only. Links the BEC Observation Array to its
 * Teleportation Nodes; the owner is the formed multiblock the hatch belongs to. The pair draws a beam, brighter while
 * the node is crafting.
 */
public class LineOfSightHatchPartMachine extends MultiblockPartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            LineOfSightHatchPartMachine.class, MultiblockPartMachine.MANAGED_FIELD_HOLDER);

    public static final int SCAN_DIST = 128;

    @Persisted
    @DescSynced
    @Nullable
    private BlockPos connection;
    /** When connected, one of the two hatches draws the beam. */
    @Persisted
    @DescSynced
    private boolean renderer;
    @DescSynced
    private boolean beamActive;
    @DescSynced
    @RequireRerender
    private boolean bothOwned;
    @Nullable
    private TickableSubscription scanSubs;

    public LineOfSightHatchPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    public void onLoad() {
        super.onLoad();
        if (!isRemote()) scanSubs = subscribeServerTick(scanSubs, this::tick);
    }

    @Override
    public void onUnload() {
        super.onUnload();
        if (scanSubs != null) {
            scanSubs.unsubscribe();
            scanSubs = null;
        }
        var other = getConnectedHatch();
        if (other != null) other.disconnect();
    }

    private void tick() {
        if (getOffsetTimer() % 100 == 1) doScan();
        var other = getConnectedHatch();
        boolean owned = getOwnerMachine() != null && other != null && other.getOwnerMachine() != null;
        if (owned != bothOwned) bothOwned = owned;
    }

    @Override
    public void onRotated(Direction oldFacing, Direction newFacing) {
        super.onRotated(oldFacing, newFacing);
        if (isRemote()) return;
        var other = getConnectedHatch();
        if (other != null) {
            disconnect();
            other.disconnect();
        }
        doScan();
    }

    /** The formed multiblock this hatch belongs to. */
    public @Nullable IMultiController getOwnerMachine() {
        for (IMultiController controller : getControllers()) if (controller.isFormed()) return controller;
        return null;
    }

    public @Nullable LineOfSightHatchPartMachine getConnectedHatch() {
        if (connection == null || getLevel() == null) return null;
        if (!getLevel().isLoaded(connection)) return null;
        if (getLevel().getBlockEntity(connection) instanceof IMachineBlockEntity mbe &&
                mbe.getMetaMachine() instanceof LineOfSightHatchPartMachine other)
            return other;
        connection = null;
        return null;
    }

    public @Nullable BlockPos getConnection() {
        return connection;
    }

    public boolean isRenderer() {
        return renderer;
    }

    public boolean canRenderBeam() {
        return renderer && connection != null && bothOwned;
    }

    public boolean isBeamActive() {
        var other = getConnectedHatch();
        return beamActive || other != null && other.beamActive;
    }

    public void setBeamActive(boolean active) {
        beamActive = active;
    }

    void disconnect() {
        connection = null;
        renderer = false;
    }

    private void connect(LineOfSightHatchPartMachine other, boolean draw) {
        connection = other.getPos();
        renderer = draw;
    }

    /** GTNH {@code doScan}. */
    public void doScan() {
        Level level = getLevel();
        if (level == null || isRemote()) return;
        Direction facing = getFrontFacing();
        BlockPos.MutableBlockPos pos = getPos().mutable().move(facing);
        for (int i = 0; i < SCAN_DIST; i++) {
            if (!level.isLoaded(pos)) break;
            if (level.getBlockEntity(pos) instanceof IMachineBlockEntity mbe &&
                    mbe.getMetaMachine() instanceof LineOfSightHatchPartMachine other) {
                if (other.getFrontFacing() == facing.getOpposite()) {
                    if (other == getConnectedHatch() && other.getConnectedHatch() == this) return;
                    var mine = getConnectedHatch();
                    if (mine != null) {
                        disconnect();
                        mine.disconnect();
                    }
                    var theirs = other.getConnectedHatch();
                    if (theirs != null) {
                        other.disconnect();
                        theirs.disconnect();
                    }
                    connect(other, true);
                    other.connect(this, false);
                    return;
                }
                break;
            }
            if (level.getBlockState(pos).getLightBlock(level, pos) > 0) break;
            pos.move(facing);
        }
        var existing = getConnectedHatch();
        if (existing != null) {
            disconnect();
            if (existing.getConnectedHatch() == this) existing.disconnect();
        }
    }

    @Override
    public boolean canShared() {
        return false;
    }
}
