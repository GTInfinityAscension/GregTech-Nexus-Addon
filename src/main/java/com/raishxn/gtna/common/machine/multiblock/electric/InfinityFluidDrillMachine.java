package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.GTValues;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.data.worldgen.bedrockfluid.BedrockFluidVeinSavedData;
import com.gregtechceu.gtceu.api.data.worldgen.bedrockfluid.FluidVeinWorldEntry;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.common.machine.multiblock.electric.FluidDrillMachine;
import com.gregtechceu.gtceu.common.machine.trait.FluidDrillLogic;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import net.minecraft.core.SectionPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.FluidStack;

import org.jetbrains.annotations.Nullable;

/**
 * GTOCore {@code INFFluidDrillMachine}: a ZPM fluid rig that never depletes its vein and multiplies the yield by
 * {@code basis} (GTO: 256); an energy hatch above the rig tier (UV) adds GTCEu's 50% overclock bonus. GTO's
 * Drilling Control Center multiplier is not ported.
 */
public final class InfinityFluidDrillMachine extends FluidDrillMachine {

    private final int basis;

    public InfinityFluidDrillMachine(IMachineBlockEntity holder, int tier, int basis) {
        super(holder, tier);
        this.basis = basis;
    }

    public int getBasis() {
        return basis;
    }

    @Override
    protected FluidDrillLogic createRecipeLogic(Object... args) {
        return new Logic(this);
    }

    /** GTCEu's fluid drill logic without depletion and with the fixed {@code basis} multiplier. */
    public static final class Logic extends FluidDrillLogic {

        @Nullable
        private Fluid vein;

        Logic(InfinityFluidDrillMachine machine) {
            super(machine);
        }

        private InfinityFluidDrillMachine rig() {
            return (InfinityFluidDrillMachine) getMachine();
        }

        @Override
        public @Nullable Fluid getVeinFluid() {
            return vein;
        }

        @Override
        public void findAndHandleRecipe() {
            if (!(getMachine().getLevel() instanceof ServerLevel level)) return;
            lastRecipe = null;
            if (vein == null) {
                vein = BedrockFluidVeinSavedData.getOrCreate(level).getFluidInChunk(chunkX(), chunkZ());
                if (vein == null) return;
            }
            GTRecipe match = recipe();
            if (match != null) setupRecipe(match);
        }

        @Nullable
        private GTRecipe recipe() {
            if (!(getMachine().getLevel() instanceof ServerLevel level) || vein == null) return null;
            var entry = BedrockFluidVeinSavedData.getOrCreate(level).getFluidVeinWorldEntry(chunkX(), chunkZ());
            GTRecipe recipe = GTRecipeBuilder.ofRaw()
                    .duration(MAX_PROGRESS)
                    .EUt(GTValues.VA[getMachine().getEnergyTier()])
                    .outputFluids(new FluidStack(vein, produce(entry)))
                    .buildRawRecipe();
            return RecipeHelper.matchContents(getMachine(), recipe).isSuccess() ? recipe : null;
        }

        @Override
        public int getFluidToProduce() {
            if (!(getMachine().getLevel() instanceof ServerLevel level) || vein == null) return 0;
            return produce(BedrockFluidVeinSavedData.getOrCreate(level).getFluidVeinWorldEntry(chunkX(), chunkZ()));
        }

        private int produce(FluidVeinWorldEntry entry) {
            var definition = entry.getDefinition();
            if (definition == null) return 0;
            long produced = Math.max(definition.getDepletedYield(), (long) entry.getFluidYield() *
                    entry.getOperationsRemaining() / BedrockFluidVeinSavedData.MAXIMUM_VEIN_OPERATIONS);
            produced *= rig().getBasis();
            if (isOverclocked()) produced = produced * 3 / 2;
            return (int) Math.min(Integer.MAX_VALUE, produced);
        }

        @Override
        public void onRecipeFinish() {
            machine.afterWorking();
            if (lastRecipe != null) RecipeHelper.handleRecipeIO(machine, lastRecipe, IO.OUT, chanceCaches);
            GTRecipe match = recipe();
            if (match != null) {
                setupRecipe(match);
                return;
            }
            if (suspendAfterFinish) {
                setStatus(Status.SUSPEND);
                suspendAfterFinish = false;
            } else {
                setStatus(Status.IDLE);
            }
            progress = 0;
            duration = 0;
        }

        @Override
        protected void depleteVein() {}

        private int chunkX() {
            return SectionPos.blockToSectionCoord(getMachine().getPos().getX());
        }

        private int chunkZ() {
            return SectionPos.blockToSectionCoord(getMachine().getPos().getZ());
        }
    }
}
