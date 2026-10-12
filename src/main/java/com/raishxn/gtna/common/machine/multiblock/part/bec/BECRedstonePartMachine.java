package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.multiblock.part.MultiblockPartMachine;

import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.Direction;

import org.jetbrains.annotations.Nullable;

/** GTNH {@code MTEHatchConfigurableBase}: a BEC hatch that emits or reads a redstone signal on every side. */
public abstract class BECRedstonePartMachine extends MultiblockPartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECRedstonePartMachine.class, MultiblockPartMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @DescSynced
    private int output;

    protected BECRedstonePartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    protected void setOutput(boolean on) {
        setOutput(on ? 15 : 0);
    }

    protected void setOutput(int strength) {
        strength = Math.max(0, Math.min(15, strength));
        if (strength == output) return;
        output = strength;
        if (getLevel() != null && !isRemote()) getLevel().updateNeighborsAt(getPos(), getBlockState().getBlock());
    }

    public int getOutput() {
        return output;
    }

    @Override
    public int getOutputSignal(@Nullable Direction side) {
        return output;
    }

    @Override
    public boolean canConnectRedstone(Direction side) {
        return true;
    }

    /** True when any neighbour powers this hatch. */
    public boolean receivingSignal() {
        return getLevel() != null && getLevel().hasNeighborSignal(getPos());
    }

    @Override
    public boolean canShared() {
        return false;
    }
}
