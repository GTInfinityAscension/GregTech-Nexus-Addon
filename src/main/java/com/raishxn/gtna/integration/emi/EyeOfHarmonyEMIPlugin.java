package com.raishxn.gtna.integration.emi;

import com.raishxn.gtna.GTNACORE;
import com.raishxn.gtna.common.data.GTNAMachines;
import com.raishxn.gtna.common.data.GTNARecipeType;
import com.raishxn.gtna.common.data.multiblock.EyeOfHarmonyCatalog;
import com.raishxn.gtna.common.data.multiblock.EyeOfHarmonyDisplay;
import com.raishxn.gtna.common.data.multiblock.EyeOfHarmonyPrograms;
import dev.emi.emi.api.EmiEntrypoint;
import dev.emi.emi.api.EmiPlugin;
import dev.emi.emi.api.EmiRegistry;
import dev.emi.emi.api.recipe.EmiRecipeCategory;
import dev.emi.emi.api.stack.EmiStack;

@EmiEntrypoint
public final class EyeOfHarmonyEMIPlugin implements EmiPlugin {

    public static final EmiRecipeCategory CATEGORY = new EmiRecipeCategory(GTNACORE.id("eye_of_harmony"),
            EmiStack.of(GTNAMachines.EYE_OF_HARMONY.asStack()));

    @Override
    public void register(EmiRegistry registry) {
        com.raishxn.gtna.integration.OriginalsInfo.entries().forEach((key, stacks) -> registry.addRecipe(
                new dev.emi.emi.api.recipe.EmiInfoRecipe(
                        stacks.stream().map(s -> (dev.emi.emi.api.stack.EmiIngredient) EmiStack.of(s)).toList(),
                        java.util.List.of(com.raishxn.gtna.integration.OriginalsInfo.text(key)),
                        GTNACORE.id("/info/originals/" + key))));
        registry.addCategory(CATEGORY);
        registry.addWorkstation(CATEGORY, EmiStack.of(GTNAMachines.EYE_OF_HARMONY.asStack()));
        registry.removeRecipes(recipe -> recipe.getCategory().getId().equals(
                GTNARecipeType.COSMOS_SIMULATION_RECIPES.getCategory().registryKey));
        for (var program : EyeOfHarmonyPrograms.all()) {
            try {
                var catalog = EyeOfHarmonyCatalog.build(registry.getRecipeManager(), program);
                registry.addRecipe(new EyeOfHarmonyEMIRecipe(EyeOfHarmonyDisplay.singlePage(catalog)));
            } catch (IllegalStateException | ArithmeticException unavailable) {
                GTNACORE.LOGGER.debug("Eye of Harmony EMI catalog unavailable: {}", unavailable.getMessage());
            }
        }
    }
}
