package com.raishxn.gtna.common.machine.multiblock.part;

import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.gui.widget.PhantomSlotWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler;
import com.gregtechceu.gtceu.api.transfer.item.CustomItemStackHandler;
import com.gregtechceu.gtceu.common.machine.multiblock.part.ItemBusPartMachine;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.MethodsReturnNonnullByDefault;
import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;

import javax.annotation.ParametersAreNonnullByDefault;

/**
 * Debug Input Bus, for testing multiblocks: the items marked in its 9 (3x3) ghost slots are offered to recipes in
 * unlimited amounts and never consumed. It keeps the normal circuit slot. Nothing can be inserted or extracted.
 *
 * <p>
 * Behaviour modelled on the GT5-Unofficial Debug Input Bus; written for GTNA on GTCEu's (LGPL) item bus.
 */
@ParametersAreNonnullByDefault
@MethodsReturnNonnullByDefault
public class DebugInputBusPartMachine extends ItemBusPartMachine {

    public static final int SLOTS = 9;

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            DebugInputBusPartMachine.class, ItemBusPartMachine.MANAGED_FIELD_HOLDER);

    // Assigned from the super constructor through createInventory: no field initializer here.
    @Persisted
    @DescSynced
    private CustomItemStackHandler ghosts;

    public DebugInputBusPartMachine(IMachineBlockEntity holder, int tier, Object... args) {
        super(holder, tier, IO.IN, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected int getInventorySize() {
        return SLOTS;
    }

    @Override
    protected NotifiableItemStackHandler createInventory(Object... args) {
        ghosts = new CustomItemStackHandler(SLOTS);
        var handler = new NotifiableItemStackHandler(this, SLOTS, IO.IN, IO.NONE, size -> new EndlessView());
        ghosts.setOnContentsChanged(handler::onContentsChanged);
        return handler;
    }

    /** Marks {@code stack} (one of it) in a ghost slot; used by tests and the GUI. */
    public void setGhost(int slot, ItemStack stack) {
        ghosts.setStackInSlot(slot, stack.copyWithCount(stack.isEmpty() ? 0 : 1));
    }

    // Nothing real is stored, so there is nothing to drop and nothing to swap into an output bus.
    @Override
    public void onMachineRemoved() {}

    @Override
    public boolean swapIO() {
        return false;
    }

    @Override
    protected void updateInventorySubscription() {}

    @Override
    protected void updateInventorySubscription(Direction newFacing) {}

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 18 * 3 + 16, 18 * 3 + 16);
        var container = new WidgetGroup(4, 4, 18 * 3 + 8, 18 * 3 + 8);
        for (int i = 0; i < SLOTS; i++) {
            container.addWidget(new PhantomSlotWidget(ghosts, i, 4 + (i % 3) * 18, 4 + (i / 3) * 18)
                    .setMaxStackSize(1)
                    .setBackgroundTexture(GuiTextures.SLOT));
        }
        container.setBackground(GuiTextures.BACKGROUND_INVERSE);
        group.addWidget(container);
        return group;
    }

    /** What recipes see: every ghost item with {@link Integer#MAX_VALUE} count; extraction never reduces it. */
    private class EndlessView extends CustomItemStackHandler {

        EndlessView() {
            super(SLOTS);
        }

        @Override
        public ItemStack getStackInSlot(int slot) {
            ItemStack ghost = ghosts.getStackInSlot(slot);
            return ghost.isEmpty() ? ItemStack.EMPTY : ghost.copyWithCount(Integer.MAX_VALUE);
        }

        @Override
        public void setStackInSlot(int slot, ItemStack stack) {}

        @Override
        public int getSlotLimit(int slot) {
            return Integer.MAX_VALUE;
        }

        @Override
        public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
            return stack;
        }

        @Override
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            ItemStack ghost = ghosts.getStackInSlot(slot);
            return ghost.isEmpty() || amount <= 0 ? ItemStack.EMPTY : ghost.copyWithCount(amount);
        }
    }
}
