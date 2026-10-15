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
        LINER
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
