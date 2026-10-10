package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.capability.recipe.IO;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.RecipeHelper;
import com.gregtechceu.gtceu.api.recipe.content.ContentModifier;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;
import com.gregtechceu.gtceu.api.recipe.modifier.ParallelLogic;
import com.gregtechceu.gtceu.data.recipe.builder.GTRecipeBuilder;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.nbt.Tag;
import net.minecraft.resources.ResourceLocation;
import net.minecraftforge.fluids.FluidStack;
import net.minecraftforge.registries.ForgeRegistries;

import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * GTO {@code hyper_reactor} / {@code advanced_hyper_reactor}: fuel in, EU out. A booster plasma present before a run
 * multiplies the run: GTO hard-codes it (Hyper Reactor: 1 mB of a tier plasma gives {@link #DEFAULT_BOOST} parallel;
 * Advanced: Starmetal 8, Dense Neutron 16). Those plasmas are GTO-only, so GTNA reads the boosters from the recipe:
 * data list {@value #BOOSTERS} of {@code {fluid: "<id>", amount: 1, parallel: 16}} (the best one present wins, its
 * amount is consumed once per run). Recipes without boosters run single, as in GTO without plasma.
 */
public class HyperReactorMachine extends WorkableElectricMultiblockMachine {

    public static final String BOOSTERS = "gtna_boosters";
    public static final int DEFAULT_BOOST = 16;

    public HyperReactorMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    /** The booster of {@code recipe} available in the input hatches with the highest parallel, or null. */
    @Nullable
    public Booster availableBooster(GTRecipe recipe) {
        if (!recipe.data.contains(BOOSTERS, Tag.TAG_LIST)) return null;
        Booster best = null;
        for (Tag tag : recipe.data.getList(BOOSTERS, Tag.TAG_COMPOUND)) {
            Booster booster = Booster.of((CompoundTag) tag);
            if (booster == null || (best != null && best.parallel >= booster.parallel)) continue;
            if (RecipeHelper.matchRecipe(this, booster.recipe()).isSuccess()) best = booster;
        }
        return best;
    }

    public static ModifierFunction recipeModifier(@NotNull MetaMachine machine, @NotNull GTRecipe recipe) {
        if (!(machine instanceof HyperReactorMachine reactor) || recipe.getOutputEUt().isEmpty()) {
            return ModifierFunction.IDENTITY;
        }
        Booster booster = reactor.availableBooster(recipe);
        if (booster == null) return ModifierFunction.IDENTITY;
        // GTO accurateParallel: limited by the fuel, not by EU (the run produces EU).
        int parallel = ParallelLogic.getParallelAmountWithoutEU(machine, recipe, booster.parallel);
        if (parallel <= 1) return ModifierFunction.IDENTITY;
        return ModifierFunction.builder()
                .inputModifier(ContentModifier.multiplier(parallel))
                .outputModifier(ContentModifier.multiplier(parallel))
                .eutMultiplier(parallel)
                .parallels(parallel)
                .build();
    }

    @Override
    public boolean beforeWorking(@Nullable GTRecipe recipe) {
        if (!super.beforeWorking(recipe)) return false;
        if (recipe != null && recipe.parallels > 1) {
            Booster booster = availableBooster(recipe);
            if (booster != null) {
                RecipeHelper.handleRecipeIO(this, booster.recipe(), IO.IN, getRecipeLogic().getChanceCaches());
            }
        }
        return true;
    }

    public record Booster(FluidStack fluid, int parallel) {

        @Nullable
        static Booster of(CompoundTag tag) {
            var fluid = ForgeRegistries.FLUIDS.getValue(new ResourceLocation(tag.getString("fluid")));
            if (fluid == null) return null;
            int amount = tag.contains("amount") ? tag.getInt("amount") : 1;
            int parallel = tag.contains("parallel") ? tag.getInt("parallel") : DEFAULT_BOOST;
            return new Booster(new FluidStack(fluid, amount), parallel);
        }

        GTRecipe recipe() {
            return GTRecipeBuilder.ofRaw().inputFluids(fluid).buildRawRecipe();
        }
    }
}
