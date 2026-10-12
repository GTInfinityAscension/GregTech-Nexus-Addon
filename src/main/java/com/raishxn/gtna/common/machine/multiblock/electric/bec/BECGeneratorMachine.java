package com.raishxn.gtna.common.machine.multiblock.electric.bec;

import com.gregtechceu.gtceu.api.capability.recipe.FluidRecipeCapability;
import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.trait.NotifiableFluidTank;
import com.gregtechceu.gtceu.api.machine.trait.RecipeLogic;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import com.lowdragmc.lowdraglib.syncdata.field.ManagedFieldHolder;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.world.level.material.Fluid;
import net.minecraftforge.fluids.FluidStack;

import com.raishxn.gtna.api.bec.BECNetwork;
import com.raishxn.gtna.api.bec.CondensateList;
import com.raishxn.gtna.api.bec.CondensateStack;
import com.raishxn.gtna.common.data.GTNARecipeType;
import org.jetbrains.annotations.NotNull;

import java.util.*;

/**
 * GTNH {@code MTEBECGenerator} (Bose-Einstein Condensate Entanglement Apparatus). Each cycle it looks at every fluid
 * in its input hatches, finds the condensate recipe of each, and runs as many parallels of all of them as the EU/t
 * allows (filled in order); the cycle lasts as long as the slowest recipe. The condensate goes straight into the
 * network's Containment Fields and is voided if there is no room, as in GTNH.
 */
public class BECGeneratorMachine extends BECMultiblockMachine {

    protected static final ManagedFieldHolder MANAGED_FIELD_HOLDER = new ManagedFieldHolder(
            BECGeneratorMachine.class, BECMultiblockMachine.MANAGED_FIELD_HOLDER);

    /** Condensate made by the running cycle, injected when it ends. */
    private final CondensateList pending = new CondensateList();
    /** Condensate of the cycle in progress. */
    private CondensateList running = new CondensateList();

    public BECGeneratorMachine(IMachineBlockEntity holder, Object... args) {
        super(holder, args);
    }

    @Override
    public ManagedFieldHolder getFieldHolder() {
        return MANAGED_FIELD_HOLDER;
    }

    @Override
    protected RecipeLogic createRecipeLogic(Object... args) {
        return new RecipeLogic(this) {

            @Override
            public @NotNull Iterator<GTRecipe> searchRecipe() {
                GTRecipe recipe = planCycle();
                return recipe == null ? Collections.emptyIterator() : List.of(recipe).iterator();
            }

            @Override
            public void onRecipeFinish() {
                for (var e : running.object2LongEntrySet())
                    BECNetwork.inject(BECGeneratorMachine.this, new CondensateStack(e.getKey(), e.getLongValue()));
                running.clear();
                markLastRecipeDirty();
                super.onRecipeFinish();
            }

            @Override
            public void interruptRecipe() {
                running.clear();
                super.interruptRecipe();
            }
        };
    }

    @Override
    public boolean alwaysTryModifyRecipe() {
        return false;
    }

    private record Candidate(GTRecipe recipe, Fluid fluid, int perParallel, int maxByInput, long eut) {}

    /** GTNH {@code checkProcessing_EM}, building one recipe that drains every planned fluid. */
    GTRecipe planCycle() {
        pending.clear();
        Map<Fluid, Long> combined = new LinkedHashMap<>();
        for (var handlerList : getCapabilitiesFlat(IO.IN, FluidRecipeCapability.CAP)) {
            if (!(handlerList instanceof NotifiableFluidTank tank)) continue;
            for (int i = 0; i < tank.getTanks(); i++) {
                FluidStack stack = tank.getFluidInTank(i);
                if (!stack.isEmpty()) combined.merge(stack.getFluid(), (long) stack.getAmount(), Long::sum);
            }
        }
        if (combined.isEmpty()) return null;
        List<Candidate> candidates = new ArrayList<>();
        for (var e : combined.entrySet()) {
            GTRecipe recipe = findRecipe(e.getKey());
            if (recipe == null) continue;
            int per = FluidRecipeCapability.CAP.of(recipe.getInputContents(FluidRecipeCapability.CAP).get(0).content)
                    .getStacks()[0].getAmount();
            int max = (int) Math.min(Integer.MAX_VALUE, e.getValue() / Math.max(1, per));
            if (max <= 0) continue;
            candidates.add(new Candidate(recipe, e.getKey(), per, max, recipe.getInputEUt().getTotalEU()));
        }
        if (candidates.isEmpty()) return null;
        double remainingPower = (double) getMaxVoltage() * getEnergyContainer().getInputAmperage();
        int[] parallels = new int[candidates.size()];
        for (int i = 0; i < candidates.size(); i++) {
            Candidate c = candidates.get(i);
            int added = (int) Math.min(c.maxByInput, remainingPower / Math.max(1, c.eut));
            parallels[i] = added;
            remainingPower -= added * (double) c.eut;
        }
        var builder = GTRecipeBuilder.ofRaw().id(com.raishxn.gtna.GTNACORE.id("bec/entanglement_cycle"));
        int duration = 0;
        double power = 0;
        for (int i = 0; i < candidates.size(); i++) {
            Candidate c = candidates.get(i);
            if (parallels[i] <= 0) continue;
            builder.inputFluids(new FluidStack(c.fluid, c.perParallel * parallels[i]));
            var out = FluidRecipeCapability.CAP.of(c.recipe.getOutputContents(FluidRecipeCapability.CAP).get(0).content)
                    .getStacks()[0];
            pending.addTo(out.getFluid(), (long) out.getAmount() * parallels[i]);
            duration = Math.max(duration, c.recipe.duration);
            power += parallels[i] * (double) c.eut;
        }
        if (duration <= 0) return null;
        long voltage = Math.max(1, getMaxVoltage());
        long amps = (long) Math.ceil(power / voltage);
        return builder.EUt(voltage, Math.max(1, amps)).duration(duration).buildRawRecipe();
    }

    private GTRecipe findRecipe(Fluid fluid) {
        for (GTRecipe recipe : allRecipes(GTNARecipeType.CONDENSATE_GENERATOR_RECIPES)) {
            var inputs = recipe.getInputContents(FluidRecipeCapability.CAP);
            if (inputs.isEmpty()) continue;
            if (FluidRecipeCapability.CAP.of(inputs.get(0).content).test(new FluidStack(fluid, 1 << 30))) return recipe;
        }
        return null;
    }

    @Override
    public boolean beforeWorking(GTRecipe recipe) {
        if (!super.beforeWorking(recipe)) return false;
        running = pending.clone();
        return true;
    }

    @Override
    public void saveCustomPersistedData(@NotNull CompoundTag tag, boolean forDrop) {
        super.saveCustomPersistedData(tag, forDrop);
        tag.put("running", running.save());
    }

    @Override
    public void loadCustomPersistedData(@NotNull CompoundTag tag) {
        super.loadCustomPersistedData(tag);
        running.load(tag.getCompound("running"));
    }

    @Override
    public void addDisplayText(List<Component> textList) {
        super.addDisplayText(textList);
        if (isFormed() && !running.isEmpty()) addCondensateText(textList, "gtna.bec.gui.producing", running);
    }

    public CondensateList getRunning() {
        return running;
    }
}
