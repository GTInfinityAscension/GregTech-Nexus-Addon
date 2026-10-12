package com.raishxn.gtna.common.machine.multiblock.part.bec;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import com.lowdragmc.lowdraglib.gui.widget.Widget;
import com.lowdragmc.lowdraglib.gui.widget.WidgetGroup;
import com.lowdragmc.lowdraglib.syncdata.annotation.DescSynced;
import com.lowdragmc.lowdraglib.syncdata.annotation.Persisted;
import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;
import com.lowdragmc.lowdraglib.utils.LocalizationUtils;

/**
 * GTNH {@code MTEHatchIONodeController} (Teleportation Node Controller Hatch): a redstone signal pauses its node
 * immediately or at the next recipe step.
 */
public class IONodeControllerHatchPartMachine extends BECRedstonePartMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            IONodeControllerHatchPartMachine.class, BECRedstonePartMachine.MANAGED_FIELD_HOLDER);

    public enum Mode {
        PAUSE_INSTANT,
        PAUSE_STEP
    }

    @Persisted
    @DescSynced
    private boolean pauseStep;

    public IONodeControllerHatchPartMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    public Mode getMode() {
        return pauseStep ? Mode.PAUSE_STEP : Mode.PAUSE_INSTANT;
    }

    @Override
    public int getOutputSignal(net.minecraft.core.Direction side) {
        return 0;
    }

    @Override
    public Widget createUIWidget() {
        var group = new WidgetGroup(0, 0, 160, 40);
        group.addWidget(BECUi.label(4, 4, () -> LocalizationUtils.format("gtna.bec.gui.mode")));
        group.addWidget(BECUi.button(4, 18, 152, () -> LocalizationUtils.format(pauseStep ?
                "gtna.bec.gui.pause_next_step" : "gtna.bec.gui.pause_immediately"), () -> pauseStep = !pauseStep));
        return group;
    }
}
