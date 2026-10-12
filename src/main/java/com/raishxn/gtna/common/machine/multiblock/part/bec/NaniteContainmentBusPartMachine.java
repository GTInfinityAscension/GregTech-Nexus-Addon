package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.gui.widget.SlotWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.feature.IDropSaveMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.part.MultiblockPartMachine;
import com.gregtechceu.gtceu.api.transfer.item.CustomItemStackHandler;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;
import com.lowdragmc.lowdraglib.utils.LocalizationUtils;

import net.minecraft.core.Direction;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.items.IItemHandlerModifiable;

import com.raishxn.gtna.api.bec.NaniteTier;
import org.jetbrains.annotations.Nullable;

/**
 * GTNH {@code MTEHatchNanite} (Nanite Containment Bus): holds up to {@link Integer#MAX_VALUE} nanites of one kind,
 * which multiblocks read and never consume. Nanites go in through the top slot (or automation) and come back out of
 * the bottom slot; the bus keeps its contents when broken.
 */
public class NaniteContainmentBusPartMachine extends MultiblockPartMachine implements IDropSaveMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            NaniteContainmentBusPartMachine.class, MultiblockPartMachine.MANAGED_FIELD_HOLDER);

    /** Ordinal of the stored {@link NaniteTier}, -1 when empty. */
    @Persisted
    @DescSynced
    private int nanite = -1;
    @Persisted
    @DescSynced
    private int count;
    private boolean changed;

    private final CustomItemStackHandler input = new CustomItemStackHandler(1) {

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            NaniteTier tier = NaniteTier.fromStack(stack);
            return tier != null && (nanite < 0 || tier.ordinal() == nanite);
        }

        @Override
        public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
            if (!isItemValid(slot, stack)) return stack;
            long room = (long) Integer.MAX_VALUE - count;
            int moved = (int) Math.min(room, stack.getCount());
            if (moved <= 0) return stack;
            if (!simulate) {
                nanite = NaniteTier.fromStack(stack).ordinal();
                count += moved;
                notifyChanged();
            }
            return stack.copyWithCount(stack.getCount() - moved);
        }
    };

    private final CustomItemStackHandler output = new CustomItemStackHandler(1) {

        @Override
        public ItemStack getStackInSlot(int slot) {
            NaniteTier tier = NaniteTier.byOrdinal(nanite);
            if (tier == null || count <= 0) return ItemStack.EMPTY;
            return new ItemStack(tier.getItem(), Math.min(count, tier.getStack().getMaxStackSize()));
        }

        @Override
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            ItemStack shown = getStackInSlot(slot);
            if (shown.isEmpty()) return ItemStack.EMPTY;
            int taken = Math.min(amount, shown.getCount());
            if (!simulate) {
                count -= taken;
                if (count <= 0) {
                    count = 0;
                    nanite = -1;
                }
                notifyChanged();
            }
            return shown.copyWithCount(taken);
        }

        @Override
        public void setStackInSlot(int slot, ItemStack stack) {
            NaniteTier tier = NaniteTier.fromStack(stack);
            if (stack.isEmpty()) {
                ItemStack shown = getStackInSlot(slot);
                extractItem(slot, shown.getCount(), false);
            } else if (tier != null && (nanite < 0 || tier.ordinal() == nanite)) {
                int shown = getStackInSlot(slot).getCount();
                count += stack.getCount() - shown;
                nanite = tier.ordinal();
                notifyChanged();
            }
        }

        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            return false;
        }

        @Override
        public ItemStack insertItem(int slot, ItemStack stack, boolean simulate) {
            return stack;
        }
    };

    public NaniteContainmentBusPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    private void notifyChanged() {
        changed = true;
        markDirty();
    }

    public @Nullable NaniteTier getNaniteTier() {
        return count > 0 ? NaniteTier.byOrdinal(nanite) : null;
    }

    public int getNaniteCount() {
        return getNaniteTier() == null ? 0 : count;
    }

    /** True once after the contents changed (GTNH {@code hasChanged}/{@code unmarkChanged}). */
    public boolean pollChanged() {
        boolean was = changed;
        changed = false;
        return was;
    }

    /** Test hook: puts {@code amount} nanites of {@code tier} in the bus, replacing its contents. */
    public void setContents(@Nullable NaniteTier tier, int amount) {
        nanite = tier == null || amount <= 0 ? -1 : tier.ordinal();
        count = nanite < 0 ? 0 : amount;
        notifyChanged();
    }

    @Override
    public @Nullable IItemHandlerModifiable getItemHandlerCap(@Nullable Direction side, boolean useCoverCapability) {
        return input;
    }

    @Override
    public boolean canShared() {
        return false;
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 120, 70);
        group.addWidget(new SlotWidget(input, 0, 51, 4, true, true).setBackgroundTexture(GuiTextures.SLOT));
        group.addWidget(new SlotWidget(output, 0, 51, 26, true, false).setBackgroundTexture(GuiTextures.SLOT));
        group.addWidget(BECUi.label(4, 50, () -> {
            NaniteTier tier = NaniteTier.byOrdinal(nanite);
            return tier == null || count <= 0 ? LocalizationUtils.format("gtna.bec.gui.none") :
                    LocalizationUtils.format("gtna.bec.gui.nanite_count", tier.getStack().getHoverName().getString(),
                            FormattingUtil.formatNumbers(count));
        }));
        return group;
    }
}
