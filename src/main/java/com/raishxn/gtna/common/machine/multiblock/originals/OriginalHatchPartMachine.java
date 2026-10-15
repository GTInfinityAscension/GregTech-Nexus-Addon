package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.gui.widget.SlotWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.IMachineLife;
import com.gregtechceu.gtceu.api.machine.multiblock.part.TieredIOPartMachine;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.world.item.ItemStack;

import org.jetbrains.annotations.Nullable;

import java.util.function.Predicate;

/**
 * Special hatch of an original multiblock. Without a filter it is a marker the controller looks for (Beam Dump,
 * Seismic Probe); with one it also holds a small stock the controller draws from (liners for the lance).
 */
public class OriginalHatchPartMachine extends TieredIOPartMachine implements IMachineLife {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            OriginalHatchPartMachine.class, TieredIOPartMachine.MANAGED_FIELD_HOLDER);

    public enum Kind {
        BEAM_DUMP,
        SEISMIC_PROBE,
        LINER,
        MASS_INJECTOR,
        DETECTOR,
        TARGET_CARTRIDGE,
        TUNING
    }

    public final Kind kind;
    @Nullable
    private final NotifiableItemStackHandler inventory;

    public OriginalHatchPartMachine(IMachineBlockEntity holder, int tier, Kind kind,
                                    @Nullable Predicate<ItemStack> filter) {
        super(holder, tier, IO.NONE);
        this.kind = kind;
        this.inventory = filter == null ? null :
                new NotifiableItemStackHandler(this, 4, IO.NONE, IO.NONE).setFilter(filter);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    /** Takes one item from the stock, or EMPTY. */
    public ItemStack takeOne() {
        if (inventory == null) return ItemStack.EMPTY;
        for (int i = 0; i < inventory.storage.getSlots(); i++) {
            var got = inventory.storage.extractItem(i, 1, false);
            if (!got.isEmpty()) return got;
        }
        return ItemStack.EMPTY;
    }

    /** Every stack in the stock, slot by slot (empty ones skipped is up to the caller). */
    public java.util.List<ItemStack> stock() {
        var out = new java.util.ArrayList<ItemStack>();
        if (inventory != null)
            for (int i = 0; i < inventory.storage.getSlots(); i++) out.add(inventory.storage.getStackInSlot(i));
        return out;
    }

    /** Takes up to {@code n} items from slot {@code i}. */
    public ItemStack take(int i, int n) {
        return inventory == null ? ItemStack.EMPTY : inventory.storage.extractItem(i, n, false);
    }

    /** Moves the first stack to the back, so cartridges take turns; returns the new first stack. */
    public ItemStack cycle() {
        if (inventory == null) return ItemStack.EMPTY;
        var s = inventory.storage;
        int n = s.getSlots();
        var first = s.getStackInSlot(0).copy();
        if (first.isEmpty()) return ItemStack.EMPTY;
        int last = 0;
        for (int i = 1; i < n; i++) {
            if (s.getStackInSlot(i).isEmpty()) break;
            s.setStackInSlot(i - 1, s.getStackInSlot(i).copy());
            last = i;
        }
        s.setStackInSlot(last, first);
        return s.getStackInSlot(0);
    }

    /** Strongest redstone signal reaching the hatch, 0–15. */
    public int signal() {
        return getLevel() == null ? 0 : getLevel().getBestNeighborSignal(getPos());
    }

    /** Puts items in the stock (tests and automation); returns what did not fit. */
    public ItemStack insert(ItemStack stack) {
        if (inventory == null) return stack;
        for (int i = 0; i < inventory.storage.getSlots() && !stack.isEmpty(); i++)
            stack = inventory.storage.insertItem(i, stack, false);
        return stack;
    }

    @Override
    public void onMachineRemoved() {
        if (inventory != null) clearInventory(inventory.storage);
    }

    @Override
    public boolean shouldOpenUI(net.minecraft.world.entity.player.Player player,
                                net.minecraft.world.InteractionHand hand,
                                net.minecraft.world.phys.BlockHitResult hit) {
        return inventory != null;
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 8 + 18 * 4, 26);
        if (inventory != null)
            for (int i = 0; i < 4; i++)
                group.addWidget(new SlotWidget(inventory.storage, i, 4 + 18 * i, 4, true, true));
        return group;
    }
}
