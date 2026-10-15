package com.raishxn.gtna.common.machine.multiblock.originals;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.TickableSubscription;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableItemStackHandler;

import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.capability.IFluidHandler;

import com.raishxn.gtna.api.capability.WirelessEnergyManager;
import com.raishxn.gtna.utils.datastructure.Int128;
import org.jetbrains.annotations.Nullable;

import java.math.BigDecimal;
import java.util.UUID;
import java.util.function.Predicate;

/**
 * Shared base of the original GTNA multiblocks: a once-per-second server tick, the owner's Nexus network as power
 * source and sink, and helpers to drain hatches and fill output buses. The machines do not run GTCEu recipes.
 */
public abstract class OriginalMachine extends WorkableElectricMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(OriginalMachine.class,
            WorkableElectricMultiblockMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @Nullable
    protected UUID networkOwner;
    @Nullable
    private TickableSubscription tick;
    protected int ticker;

    protected OriginalMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        tick = subscribeServerTick(tick, this::originalTick);
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        if (tick != null) {
            tick.unsubscribe();
            tick = null;
        }
    }

    private void originalTick() {
        if (!(getLevel() instanceof ServerLevel level) || ++ticker % 20 != 0) return;
        if (networkOwner == null) networkOwner = getOwnerUUID();
        if (!isWorkingEnabled()) return;
        secondTick(level);
        markDirty();
    }

    /** Runs once per second while formed and enabled. */
    protected abstract void secondTick(ServerLevel level);

    /** A point {@code up} blocks above and {@code back} blocks behind the controller. */
    public BlockPos offset(double up, double back) {
        Direction b = getFrontFacing().getOpposite();
        return getPos().relative(Direction.UP, (int) Math.round(up)).relative(b, (int) Math.round(back));
    }

    /** The special hatch of this kind in the structure, or null. */
    @Nullable
    public OriginalHatchPartMachine hatch(OriginalHatchPartMachine.Kind kind) {
        return hatchOf(getParts(), kind);
    }

    @Nullable
    static OriginalHatchPartMachine hatchOf(Iterable<? extends Object> parts, OriginalHatchPartMachine.Kind kind) {
        for (var part : parts) if (part instanceof OriginalHatchPartMachine h && h.kind == kind) return h;
        return null;
    }

    // ------------------------------------------------------------------ energy

    protected boolean consume(ServerLevel level, double eu) {
        if (eu <= 0) return true;
        if (networkOwner == null) return false;
        return WirelessEnergyManager.consumeEnergy(level, networkOwner, int128(eu));
    }

    protected void deliver(ServerLevel level, double eu) {
        if (eu > 0 && networkOwner != null) WirelessEnergyManager.addEnergy(level, networkOwner, int128(eu));
    }

    protected static Int128 int128(double eu) {
        return Int128.fromBigInteger(BigDecimal.valueOf(Math.max(0, eu)).toBigInteger());
    }

    // ------------------------------------------------------------------ hatches

    /** Drains up to {@code max} mB of fluids matching {@code filter}; returns the amount drained. */
    protected long drain(Predicate<Fluid> filter, long max) {
        long total = 0;
        for (var part : getParts()) {
            for (var handlers : part.getRecipeHandlers()) {
                if (!handlers.isValid(IO.IN)) continue;
                for (var handler : handlers.getCapability(FluidRecipeCapability.CAP)) {
                    if (!(handler instanceof NotifiableFluidTank tank)) continue;
                    for (int t = 0; t < tank.getTanks() && total < max; t++) {
                        var fluid = tank.getFluidInTank(t);
                        if (fluid.isEmpty() || !filter.test(fluid.getFluid())) continue;
                        var take = fluid.copy();
                        take.setAmount((int) Math.min(fluid.getAmount(), max - total));
                        total += tank.drainInternal(take, IFluidHandler.FluidAction.EXECUTE).getAmount();
                    }
                }
            }
        }
        return total;
    }

    /** Takes up to {@code max} items matching {@code filter} from the input buses; returns how many. */
    protected long take(Predicate<ItemStack> filter, long max) {
        long total = 0;
        for (var part : getParts()) {
            for (var handlers : part.getRecipeHandlers()) {
                if (!handlers.isValid(IO.IN)) continue;
                for (var handler : handlers.getCapability(ItemRecipeCapability.CAP)) {
                    if (!(handler instanceof NotifiableItemStackHandler items)) continue;
                    for (int i = 0; i < items.storage.getSlots() && total < max; i++) {
                        var stack = items.storage.getStackInSlot(i);
                        if (stack.isEmpty() || !filter.test(stack)) continue;
                        total += items.storage.extractItem(i, (int) Math.min(stack.getCount(), max - total), false)
                                .getCount();
                    }
                }
            }
        }
        return total;
    }

    /** Puts items in the output buses; returns what did not fit. */
    protected long output(ItemStack stack, long amount) {
        if (stack.isEmpty() || amount <= 0) return 0;
        for (var part : getParts()) {
            for (var handlers : part.getRecipeHandlers()) {
                if (!handlers.isValid(IO.OUT)) continue;
                for (var handler : handlers.getCapability(ItemRecipeCapability.CAP)) {
                    if (!(handler instanceof NotifiableItemStackHandler items)) continue;
                    for (int i = 0; i < items.storage.getSlots() && amount > 0; i++) {
                        var piece = stack.copyWithCount((int) Math.min(stack.getMaxStackSize(), amount));
                        amount -= piece.getCount() - items.storage.insertItem(i, piece, false).getCount();
                    }
                    if (amount <= 0) return 0;
                }
            }
        }
        return amount;
    }

    // ------------------------------------------------------------------ persistence helpers

    protected static long[] bits(double[] values) {
        long[] out = new long[values.length];
        for (int i = 0; i < values.length; i++) out[i] = Double.doubleToRawLongBits(values[i]);
        return out;
    }

    protected static double[] doubles(long[] bits) {
        double[] out = new double[bits.length];
        for (int i = 0; i < bits.length; i++) out[i] = Double.longBitsToDouble(bits[i]);
        return out;
    }
}
