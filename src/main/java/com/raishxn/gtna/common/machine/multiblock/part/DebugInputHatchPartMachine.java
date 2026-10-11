package com.raishxn.gtna.common.machine.multiblock.part;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.gui.widget.PhantomFluidWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;
import com.gregtechceu.gtceu.api.transfer.fluid.CustomFluidTank;
import com.gregtechceu.gtceu.common.machine.multiblock.part.FluidHatchPartMachine;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.MethodsReturnNonnullByDefault;
import net.minecraft.core.Direction;
import net.minecraftforge.fluids.FluidStack;

import java.util.ArrayList;
import java.util.List;

import javax.annotation.ParametersAreNonnullByDefault;

/**
 * Debug Input Hatch, for testing multiblocks: the fluids marked in its 9 ghost tanks are offered to recipes in
 * unlimited amounts and never consumed. It keeps the normal circuit slot. Nothing can be filled or drained.
 *
 * <p>
 * Written for GTNA on GTCEu's (LGPL) fluid hatch; the fluid twin of {@link DebugInputBusPartMachine}.
 */
@ParametersAreNonnullByDefault
@MethodsReturnNonnullByDefault
public class DebugInputHatchPartMachine extends FluidHatchPartMachine {

    public static final int SLOTS = 9;

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            DebugInputHatchPartMachine.class, FluidHatchPartMachine.MANAGED_FIELD_HOLDER);

    // Assigned from the super constructor through createTank: no field initializer here.
    @Persisted
    @DescSynced
    private CustomFluidTank[] ghosts;

    public DebugInputHatchPartMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, GTValues.MAX, IO.IN, 1, SLOTS, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected NotifiableFluidTank createTank(int initialCapacity, int slots, Object... args) {
        ghosts = new CustomFluidTank[SLOTS];
        List<CustomFluidTank> views = new ArrayList<>();
        for (int i = 0; i < SLOTS; i++) {
            ghosts[i] = new CustomFluidTank(1);
            views.add(new EndlessTank(i));
        }
        var tank = new NotifiableFluidTank(this, views, IO.IN, IO.NONE);
        for (var ghost : ghosts) ghost.setOnContentsChanged(tank::onContentsChanged);
        return tank;
    }

    /** Marks {@code fluid} in a ghost tank; used by tests and the GUI. */
    public void setGhost(int tank, FluidStack fluid) {
        FluidStack mark = fluid.copy();
        if (!mark.isEmpty()) mark.setAmount(1);
        ghosts[tank].setFluid(mark);
    }

    // Nothing real is stored, so there is nothing to keep and nothing to swap into an output hatch.
    @Override
    public boolean swapIO() {
        return false;
    }

    @Override
    protected void updateTankSubscription() {}

    @Override
    protected void updateTankSubscription(Direction newFacing) {}

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 18 * 3 + 16, 18 * 3 + 16);
        var container = new WidgetGroup(4, 4, 18 * 3 + 8, 18 * 3 + 8);
        for (int i = 0; i < SLOTS; i++) {
            int index = i;
            container.addWidget(new PhantomFluidWidget(ghosts[i], 0, 4 + (i % 3) * 18, 4 + (i / 3) * 18, 18, 18,
                    () -> ghosts[index].getFluid(), fluid -> setGhost(index, fluid))
                    .setShowAmount(false)
                    .setBackground(GuiTextures.FLUID_SLOT));
        }
        container.setBackground(GuiTextures.BACKGROUND_INVERSE);
        group.addWidget(container);
        return group;
    }

    /** What recipes see: the ghost fluid with {@link Integer#MAX_VALUE} mB; draining never reduces it. */
    private class EndlessTank extends CustomFluidTank {

        private final int index;

        EndlessTank(int index) {
            super(Integer.MAX_VALUE);
            this.index = index;
        }

        private FluidStack endless(int amount) {
            FluidStack ghost = ghosts[index].getFluid();
            if (ghost.isEmpty() || amount <= 0) return FluidStack.EMPTY;
            FluidStack copy = ghost.copy();
            copy.setAmount(amount);
            return copy;
        }

        @Override
        public FluidStack getFluid() {
            return endless(Integer.MAX_VALUE);
        }

        @Override
        public int getFluidAmount() {
            return ghosts[index].getFluid().isEmpty() ? 0 : Integer.MAX_VALUE;
        }

        @Override
        public void setFluid(FluidStack stack) {}

        @Override
        public int fill(FluidStack resource, FluidAction action) {
            return 0;
        }

        @Override
        public FluidStack drain(int maxDrain, FluidAction action) {
            return endless(maxDrain);
        }

        @Override
        public FluidStack drain(FluidStack resource, FluidAction action) {
            return resource.isFluidEqual(ghosts[index].getFluid()) ? endless(resource.getAmount()) : FluidStack.EMPTY;
        }
    }
}
