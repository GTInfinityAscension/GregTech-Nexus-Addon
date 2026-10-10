package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.pattern.BlockPattern;

import com.raishxn.gtna.api.machine.multiblock.GTNAStructureRefresh;
import com.raishxn.gtna.common.data.GTNAMegaMachines;
import com.raishxn.gtna.common.data.GTNARecipeType;

/**
 * GTO {@code CompoundExtremeCoolingMachine}: Vacuum Freezer and Atomization Condensation share one structure; the
 * Plasma Condenser mode needs the larger plasma structure, rechecked whenever the mode changes.
 */
public class CompoundExtremeCoolingMachine extends WorkableElectricMultipleRecipesMachine {

    public CompoundExtremeCoolingMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    public boolean plasmaMode() {
        return getRecipeType() == GTNARecipeType.PLASMA_CONDENSER_RECIPES;
    }

    @Override
    public BlockPattern getPattern() {
        return GTNAMegaMachines.compoundExtremeCoolingPattern(plasmaMode(), getDefinition());
    }

    @Override
    public void setActiveRecipeType(int activeRecipeType) {
        boolean before = plasmaMode();
        super.setActiveRecipeType(activeRecipeType);
        if (before != plasmaMode() && !isRemote()) GTNAStructureRefresh.refresh(this, true);
    }
}
