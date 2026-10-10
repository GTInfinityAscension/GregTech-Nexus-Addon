package com.raishxn.gtna.common.machine.multiblock.electric;

import com.gregtechceu.gtceu.api.capability.recipe.ItemRecipeCapability;
import com.gregtechceu.gtceu.api.machine.IMachineBlockEntity;
import com.gregtechceu.gtceu.api.machine.MetaMachine;
import com.gregtechceu.gtceu.api.machine.multiblock.WorkableElectricMultiblockMachine;
import com.gregtechceu.gtceu.api.recipe.GTRecipe;
import com.gregtechceu.gtceu.api.recipe.content.Content;
import com.gregtechceu.gtceu.api.recipe.modifier.ModifierFunction;

import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

/**
 * GTOCore {@code AnalysisAndResearchCenterMachine}: Data Analysis / Data Integration recipes that need computation
 * (CWU/t from a Computation Data Hatch). Each run yields exactly one of the recipe's item outputs, picked by their
 * chances out of 10,000 (GTO {@code getRealRecipe}). GTO feeds it from its Analyze / Research Holder parts and its
 * data-crystal items, a research system GTO ships only in dev builds; GTNA takes an input bus in the holder slot and
 * leaves the recipes to the pack.
 */
public class AnalysisAndResearchCenterMachine extends WorkableElectricMultiblockMachine {

    public static final int CHANCE_SCALE = 10000;

    public AnalysisAndResearchCenterMachine(IMachineBlockEntity holder) {
        super(holder);
    }

    /** Picks one item output weighted by chance (the last one when the roll passes them all). */
    public static List<Content> pickOne(List<Content> outputs, int roll) {
        if (outputs.isEmpty()) return outputs;
        Content selected = outputs.get(outputs.size() - 1);
        int cumulative = 0;
        for (Content content : outputs) {
            if (content.chance <= 0) continue;
            cumulative += content.chance;
            if (roll <= cumulative) {
                selected = content;
                break;
            }
        }
        List<Content> single = new ArrayList<>();
        single.add(new Content(selected.content, CHANCE_SCALE, CHANCE_SCALE, 0));
        return single;
    }

    public static ModifierFunction recipeModifier(@NotNull MetaMachine machine, @NotNull GTRecipe recipe) {
        return original -> {
            int roll = machine.getLevel() != null ? machine.getLevel().random.nextInt(CHANCE_SCALE) : 0;
            List<Content> outputs = original.getOutputContents(ItemRecipeCapability.CAP);
            if (outputs.size() <= 1) return original;
            GTRecipe result = original.copy();
            result.outputs.put(ItemRecipeCapability.CAP, pickOne(outputs, roll));
            return result;
        };
    }
}
