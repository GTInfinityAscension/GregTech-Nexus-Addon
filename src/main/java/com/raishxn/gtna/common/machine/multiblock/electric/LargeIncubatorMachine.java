package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.block.IFilterType;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.CleanroomType;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;

import net.minecraft.network.chat.Component;

import com.raishxn.gtna.common.data.GTNARecipeDataKeys;
import com.raishxn.gtna.common.data.multiblock.GTNAGlassTiers;
import org.jetbrains.annotations.NotNull;

import java.util.List;

/**
 * GTOCore {@code large_incubator} ({@code IncubatorMachine}): the glass tier caps the machine's voltage tier, and a
 * recipe that asks for a better filter ({@link GTNARecipeDataKeys#FILTER_CASING}) than the structure's cleanroom
 * filters doesn't start. GTO's Radiation Hatch is not ported (no GTNA recipe uses radioactivity).
 */
public class LargeIncubatorMachine extends WorkableElectricMultiblockMachine {

    private int glassTier = GTValues.MAX;
    private int filterTier = 1;

    public LargeIncubatorMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public void onStructureFormed() {
        super.onStructureFormed();
        Object glass = getMultiblockState().getMatchContext().get(GTNAGlassTiers.KEY);
        glassTier = glass instanceof Integer tier ? tier : GTValues.MV;
        Object filter = getMultiblockState().getMatchContext().get("FilterType");
        filterTier = filter instanceof IFilterType type &&
                type.getCleanroomType() == CleanroomType.STERILE_CLEANROOM ? 2 : 1;
    }

    @Override
    public void onStructureInvalid() {
        super.onStructureInvalid();
        glassTier = GTValues.MAX;
        filterTier = 1;
    }

    public int getGlassTier() {
        return glassTier;
    }

    public int getFilterTier() {
        return filterTier;
    }

    @Override
    public long getMaxVoltage() {
        return Math.min(super.getMaxVoltage(), GTValues.V[glassTier]);
    }

    @Override
    public long getOverclockVoltage() {
        return Math.min(super.getOverclockVoltage(), GTValues.V[glassTier]);
    }

    /** Rejects recipes that need a better filter than the structure has. */
    public static ModifierFunction filterCheck(MetaMachine machine, @NotNull GTRecipe recipe) {
        if (machine instanceof LargeIncubatorMachine incubator &&
                recipe.data.getInt(GTNARecipeDataKeys.FILTER_CASING) > incubator.filterTier) {
            return ModifierFunction.NULL;
        }
        return ModifierFunction.IDENTITY;
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (isFormed()) {
            textList.add(Component.translatable("gtna.multiblock.large_incubator.glass_tier",
                    GTValues.VNF[glassTier]));
            textList.add(Component.translatable("gtna.multiblock.large_incubator.filter_tier", filterTier));
        }
    }
}
