package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.gui.widget.LongInputWidget;
import com.gregtechceu.gtceu.api.gui.widget.PhantomFluidWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.utils.FormattingUtil;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;
import com.lowdragmc.lowdraglib.utils.LocalizationUtils;

import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.api.bec.BECInventory;
import com.raishxn.gtna.api.bec.CondensateType;

/**
 * GTNH {@code MTEHatchCondensateDetector}: emits redstone when the condensate stored in its Containment Field passes a
 * threshold. With no filter it sums every condensate.
 */
public class CondensateDetectorHatchPartMachine extends BECRedstonePartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            CondensateDetectorHatchPartMachine.class, BECRedstonePartMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @DescSynced
    private FluidStack filter = FluidStack.EMPTY;
    @Persisted
    @DescSynced
    private int comparison = BECComparison.EQ.ordinal();
    @Persisted
    @DescSynced
    private long requestedAmount = 1;
    @DescSynced
    private long actualAmount;
    private BECInventory storage;

    public CondensateDetectorHatchPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public void bindStorage(BECInventory storage) {
        this.storage = storage;
        if (storage != null) updateAmount(storage);
    }

    public void updateAmount(BECInventory inv) {
        long amount = 0;
        if (!filter.isEmpty()) amount = inv.getContents().getLong(filter.getFluid());
        else for (long l : inv.getContents().values()) amount += l;
        actualAmount = amount;
        refresh();
    }

    private void refresh() {
        setOutput(BECComparison.byOrdinal(comparison).test(actualAmount, requestedAmount));
    }

    private void refreshFromStorage() {
        if (storage != null) updateAmount(storage);
        else refresh();
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 160, 86);
        group.addWidget(BECUi.label(4, 6, () -> LocalizationUtils.format("gtna.bec.gui.filter")));
        group.addWidget(new PhantomFluidWidget(null, 0, 100, 2, 18, 18, () -> filter, fluid -> {
            filter = fluid == null || fluid.isEmpty() || CondensateType.getCondensateType(fluid.getFluid()) == null ?
                    FluidStack.EMPTY : new FluidStack(fluid.getFluid(), 1);
            refreshFromStorage();
        }).setShowAmount(false));
        group.addWidget(BECUi.label(4, 28, () -> LocalizationUtils.format("gtna.bec.gui.operation")));
        group.addWidget(BECUi.button(100, 24, 56, () -> BECComparison.byOrdinal(comparison).symbol, () -> {
            comparison = BECComparison.byOrdinal(comparison).next(false).ordinal();
            refresh();
        }));
        group.addWidget(BECUi.label(4, 48, () -> LocalizationUtils.format("gtna.bec.gui.threshold")));
        group.addWidget(new LongInputWidget(70, 44, 86, 14, () -> requestedAmount, v -> {
            requestedAmount = Math.max(1, v);
            refresh();
        }).setMin(1L));
        group.addWidget(BECUi.label(4, 68, () -> LocalizationUtils.format("gtna.bec.gui.current",
                FormattingUtil.formatNumbers(actualAmount) + " mB")));
        return group;
    }
}
