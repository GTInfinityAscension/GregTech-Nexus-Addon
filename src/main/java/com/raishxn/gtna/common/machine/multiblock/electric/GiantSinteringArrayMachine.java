package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers;

/**
 * GTOCore {@code giant_sintering_array} ({@code CoilTieredCasingMultiblockMachine.createGlassTieredParallel}): coil
 * temperature gates the recipes like a blast furnace, and the parallel is {@code 4^glass tier} (the formula GTO's
 * tooltip states; GTO's implementation is in its closed GTOLib), or the Parallel Hatch limit if higher.
 */
public class GiantSinteringArrayMachine extends CoilWorkableElectricMultipleRecipesMachine {

    private int glassTier;

    public GiantSinteringArrayMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, false, args);
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        Object glass = getMultiblockState().getMatchContext().get(GTNAGlassTiers.KEY);
        glassTier = glass instanceof Integer tier ? tier : 0;
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        glassTier = 0;
    }

    public int getGlassTier() {
        return glassTier;
    }

    /** {@code 4^glassTier}, saturated at {@link Integer#MAX_VALUE}. */
    public static int glassParallel(int glassTier) {
        return glassTier >= 15 ? Integer.MAX_VALUE : 1 << (2 * glassTier);
    }

    @Override
    public int getMaxParallel() {
        return Math.max(super.getMaxParallel(), glassParallel(glassTier));
    }
}
