package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.gui.widget.IntInputWidget;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;
import com.lowdragmc.lowdraglib.utils.LocalizationUtils;

import com.raishxn.gtna.api.bec.NaniteTier;
import org.jetbrains.annotations.Nullable;

/**
 * GTNH {@code MTEHatchNaniteDetector}: emits redstone from the nanite tier its Teleportation Node currently requests.
 * Analog mode emits the tier itself.
 */
public class NaniteDetectorHatchPartMachine extends BECRedstonePartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            NaniteDetectorHatchPartMachine.class, BECRedstonePartMachine.MANAGED_FIELD_HOLDER);

    @Persisted
    @DescSynced
    private int configuredTier = 1;
    @Persisted
    @DescSynced
    private int comparison = BECComparison.EQ.ordinal();
    /** Ordinal of the requested {@link NaniteTier}, -1 for none. */
    @DescSynced
    private int requiredTier = -1;

    public NaniteDetectorHatchPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public void setRequiredTier(@Nullable NaniteTier tier) {
        requiredTier = tier == null ? -1 : tier.ordinal();
        refresh();
    }

    private void refresh() {
        NaniteTier tier = NaniteTier.byOrdinal(requiredTier);
        BECComparison op = BECComparison.byOrdinal(comparison);
        if (op == BECComparison.ANALOG) setOutput(tier == null ? 0 : tier.tier);
        else setOutput(tier != null && op.test(tier.tier, configuredTier));
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 150, 66);
        group.addWidget(BECUi.label(4, 4, () -> LocalizationUtils.format("gtna.bec.gui.operation")));
        group.addWidget(BECUi.button(90, 2, 56, () -> BECComparison.byOrdinal(comparison) == BECComparison.ANALOG ?
                LocalizationUtils.format("gtna.bec.gui.analog") : BECComparison.byOrdinal(comparison).symbol, () -> {
                    comparison = BECComparison.byOrdinal(comparison).next(true).ordinal();
                    refresh();
                }));
        group.addWidget(BECUi.label(4, 24, () -> LocalizationUtils.format("gtna.bec.gui.threshold")));
        group.addWidget(new IntInputWidget(90, 20, 56, 14, () -> configuredTier, v -> {
            configuredTier = v;
            refresh();
        }).setMin(1).setMax(NaniteTier.MagMatter.tier));
        group.addWidget(BECUi.label(4, 44, () -> {
            NaniteTier tier = NaniteTier.byOrdinal(requiredTier);
            return LocalizationUtils.format("gtna.bec.gui.current", tier == null ?
                    LocalizationUtils.format("gtna.bec.gui.none") :
                    LocalizationUtils.format("gtna.bec.gui.nanite_tier", tier.tier));
        }));
        return group;
    }
}
