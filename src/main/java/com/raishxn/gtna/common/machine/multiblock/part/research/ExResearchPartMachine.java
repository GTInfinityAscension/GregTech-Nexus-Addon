package com.raishxn.gtna.common.machine.multiblock.part.research;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.IHPCAComputationProvider;
import com.gregtechceu.gtceu.api.capability.IHPCACoolantProvider;
import com.gregtechceu.gtceu.api.gui.GuiTextures;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.common.machine.multiblock.part.hpca.HPCAComponentPartMachine;

import com.lowdragmc.lowdraglib.gui.texture.ResourceTexture;

/**
 * GTOCore {@code ExResearch*PartMachine}: NICH (tier 3, Supercomputing Center tier 2) and GWCA (tier 4, tier 3)
 * HPCA components. Values copied from GTOCore {@code dc4824d}.
 */
public abstract class ExResearchPartMachine extends HPCAComponentPartMachine {

    protected final int tier;

    protected ExResearchPartMachine(IMachineBlockEntity holder, int tier) {
        super(holder);
        this.tier = tier;
    }

    public int getTier() {
        return tier;
    }

    @Override
    public boolean isAdvanced() {
        return true;
    }

    public static class Empty extends ExResearchPartMachine {

        public Empty(IMachineBlockEntity holder, int tier) {
            super(holder, tier);
        }

        @Override
        public ResourceTexture getComponentIcon() {
            return GuiTextures.HPCA_ICON_EMPTY_COMPONENT;
        }

        @Override
        public int getUpkeepEUt() {
            return 0;
        }

        @Override
        public boolean canBeDamaged() {
            return false;
        }
    }

    public static class Computation extends ExResearchPartMachine implements IHPCAComputationProvider {

        public Computation(IMachineBlockEntity holder, int tier) {
            super(holder, tier);
        }

        @Override
        public ResourceTexture getComponentIcon() {
            return isDamaged() ? GuiTextures.HPCA_ICON_DAMAGED_ADVANCED_COMPUTATION_COMPONENT :
                    GuiTextures.HPCA_ICON_ADVANCED_COMPUTATION_COMPONENT;
        }

        @Override
        public int getUpkeepEUt() {
            return tier == 3 ? GTValues.VA[GTValues.LuV] : GTValues.VA[GTValues.UV];
        }

        @Override
        public int getMaxEUt() {
            return tier == 3 ? GTValues.VA[GTValues.UV] : GTValues.VA[GTValues.UEV];
        }

        @Override
        public int getCWUPerTick() {
            if (isDamaged()) return 0;
            return tier == 3 ? 64 : 1024;
        }

        @Override
        public int getCoolingPerTick() {
            return tier == 3 ? 16 : 256;
        }

        @Override
        public boolean canBeDamaged() {
            return true;
        }
    }

    public static class Cooler extends ExResearchPartMachine implements IHPCACoolantProvider {

        public Cooler(IMachineBlockEntity holder, int tier) {
            super(holder, tier);
        }

        @Override
        public ResourceTexture getComponentIcon() {
            return GuiTextures.HPCA_ICON_ACTIVE_COOLER_COMPONENT;
        }

        @Override
        public int getUpkeepEUt() {
            return tier == 3 ? GTValues.VA[GTValues.UV] : GTValues.VA[GTValues.UHV];
        }

        @Override
        public boolean canBeDamaged() {
            return false;
        }

        @Override
        public int getCoolingAmount() {
            return tier == 3 ? 8 : 64;
        }

        @Override
        public boolean isActiveCooler() {
            return true;
        }

        @Override
        public int getMaxCoolantPerTick() {
            return tier == 3 ? 80 : 320;
        }
    }

    public static class Bridge extends ExResearchPartMachine {

        public Bridge(IMachineBlockEntity holder, int tier) {
            super(holder, tier);
        }

        @Override
        public ResourceTexture getComponentIcon() {
            return GuiTextures.HPCA_ICON_BRIDGE_COMPONENT;
        }

        @Override
        public int getUpkeepEUt() {
            return GTValues.VA[GTValues.UHV];
        }

        @Override
        public boolean canBeDamaged() {
            return false;
        }

        @Override
        public boolean doesAllowBridging() {
            return true;
        }
    }
}
