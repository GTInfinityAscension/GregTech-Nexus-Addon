package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;

import com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers;

/**
 * GTOCore glass-tiered parallel without coils ({@code TierCasingCrossRecipeMultiblockMachine.createGasTieredParallel}):
 * several recipes at once, parallel {@code 4^glass tier} (GTO's tooltip formula) or the Parallel Hatch limit.
 */
public class GlassParallelMultipleRecipesMachine extends WorkableElectricMultipleRecipesMachine {

    private int glassTier;

    public GlassParallelMultipleRecipesMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
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

    @Override
    public int getMaxParallel() {
        return Math.max(super.getMaxParallel(), GiantSinteringArrayMachine.glassParallel(glassTier));
    }
}
